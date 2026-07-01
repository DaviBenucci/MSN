from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from msn_utils import (
    ValidationIssue,
    emit,
    emit_error,
    normalize_header,
    normalize_price_value,
    normalize_sku,
    normalize_stock_value,
    normalize_words,
    setup_script_logging,
    validate_new_products_dataframe,
    write_json,
)


ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_WORDPRESS_FILE = (
    Path.home()
    / "Desktop"
    / "cópia de produtos"
    / "Produtos"
    / "Controle_de_estoque_Com_Filtro.xlsx"
)
DEFAULT_CONCILIACAO_FOLDER = Path.home() / "Desktop" / "Conciliacao"

NAME_ALIASES = {
    "nome",
    "produto",
    "descricao",
    "descricaoproduto",
    "descricaodoproduto",
    "item",
    "itens",
    "mercadoria",
    "modelo",
}
SKU_ALIASES = {
    "sku",
    "codigo",
    "codigoproduto",
    "codigodoproduto",
    "cod",
    "referencia",
    "ref",
    "partnumber",
    "mpn",
}
ID_ALIASES = {
    "id",
    "codigoid",
    "codigointerno",
    "idproduto",
}
STOCK_ALIASES = {
    "estoque",
    "stock",
    "quantidade",
    "qtd",
    "saldo",
    "disponivel",
    "disponibilidade",
}
PRICE_ALIASES = {
    "preco",
    "valor",
    "valorunitario",
    "precounitario",
    "precodevenda",
    "venda",
}

CATEGORY_RULES = [
    ("TON", ["TONER"]),
    ("CRT", ["CARTUCHO", "INK CARTRIDGE", "PRINT CARTRIDGE"]),
    ("DRU", ["DRUM", "TAMBOR", "CILINDRO", "UNIDADE DE IMAGEM", "UNIDADE DE TAMBOR"]),
    ("FUS", ["FUSOR", "FUSER"]),
    ("IMP", ["IMPRESSORA", "MULTIFUNCIONAL", "PRINTER"]),
    ("PAP", ["PAPEL", "SULFITE"]),
    ("DEV", ["DEVELOPER", "REVELADOR"]),
    ("RES", ["RESIDUO", "RESIDUAL", "WASTE TONER"]),
    ("KIT", ["KIT MANUTENCAO", "KIT DE MANUTENCAO", "MAINTENANCE KIT"]),
]

BRAND_RULES = [
    ("HP", ["HP", "HEWLETT PACKARD", "HEWLETT-PACKARD"]),
    ("SAM", ["SAMSUNG"]),
    ("BRO", ["BROTHER"]),
    ("CAN", ["CANON"]),
    ("EPS", ["EPSON"]),
    ("LEX", ["LEXMARK"]),
    ("XER", ["XEROX"]),
    ("RIC", ["RICOH"]),
    ("MIN", ["MINOLTA", "KONICA MINOLTA", "KONICA"]),
    ("KYO", ["KYOCERA"]),
    ("OKI", ["OKI"]),
    ("APC", ["APC"]),
    ("ZEB", ["ZEBRA"]),
    ("ELG", ["ELGIN"]),
]

COLOR_RULES = [
    ("MAG", ["MAGENTA"]),
    ("PRT", ["PRETO", "BLACK", "NEGRO"]),
    ("AMR", ["AMARELO", "YELLOW"]),
    ("CIA", ["CIANO", "CYAN"]),
]

PACKAGE_RULES = [
    ("AZ", ["AZUL E BRANCA", "AZUL BRANCA", "CX AZUL", "CAIXA AZUL"]),
    ("NV", ["NOVA PRETA", "CX NOVA PRETA", "CAIXA NOVA PRETA"]),
    ("BR", ["CX BRANCA", "CAIXA BRANCA"]),
]

MODEL_STOP_WORDS = {
    "TONER",
    "CARTUCHO",
    "IMPRESSORA",
    "MULTIFUNCIONAL",
    "DRUM",
    "TAMBOR",
    "CILINDRO",
    "FUSOR",
    "FUSER",
    "HP",
    "HEWLETT",
    "PACKARD",
    "SAMSUNG",
    "BROTHER",
    "CANON",
    "EPSON",
    "LEXMARK",
    "XEROX",
    "RICOH",
    "MINOLTA",
    "KONICA",
    "OKI",
    "COLOR",
    "PRETO",
    "BLACK",
    "MAGENTA",
    "AMARELO",
    "YELLOW",
    "CIANO",
    "CYAN",
    "CX",
    "CAIXA",
    "NOVA",
    "PRETA",
    "BRANCA",
    "AZUL",
    "CONTADOR",
    "PROXPRESS",
    "ORIGINAL",
    "COMPATIVEL",
}


@dataclass(frozen=True)
class ProcessResult:
    saida: Path
    relatorio: Path | None = None
    novos_produtos: Path | None = None
    summary_json: Path | None = None
    log_path: Path | None = None


@dataclass(frozen=True)
class WordPressColumns:
    id: str
    sku: str
    nome: str
    estoque: str | None
    preco: str | None


class ValidationFailure(RuntimeError):
    def __init__(self, issues: list[ValidationIssue], report_path: Path | None = None) -> None:
        self.issues = issues
        self.report_path = report_path
        errors = [issue for issue in issues if issue.severity == "erro"]
        super().__init__(f"{len(errors)} erro(s) de validacao encontrados")


def main() -> int:
    args = parse_args()
    logger, log_path = setup_script_logging("conciliador_planilhas_sku", ROOT_DIR, getattr(args, "log_dir", None))
    args._logger = logger
    args._log_path = log_path

    try:
        result = processar_planilha(args)
    except ValidationFailure as exc:
        logger.error("Erro ao validar: %s", exc)
        emit_error(logger, f"Erro ao validar: {exc}")
        for issue in exc.issues[:10]:
            if issue.severity == "erro":
                emit_error(logger, f"- linha {issue.row_number or '-'} {issue.field}: {issue.message}")
        if exc.report_path:
            emit_error(logger, f"Relatorio de validacao: {exc.report_path}")
        write_execution_summary(args, None, exit_code=2, issues=exc.issues, error=str(exc))
        return 2
    except Exception as exc:
        logger.exception("Erro ao processar")
        emit_error(logger, f"Erro ao processar: {exc}")
        write_execution_summary(args, None, exit_code=1, error=str(exc))
        return 1

    if args.dry_run:
        emit(logger, f"Arquivo final planejado (nao gravado): {result.saida}")
        if result.relatorio:
            emit(logger, f"Relatorio de dry-run gerado: {result.relatorio}")
        if result.novos_produtos:
            emit(logger, f"Novos produtos planejados (nao gravado): {result.novos_produtos}")
    else:
        emit(logger, f"Arquivo gerado: {result.saida}")
        if result.relatorio:
            emit(logger, f"Relatorio gerado: {result.relatorio}")
        if result.novos_produtos:
            emit(logger, f"Novos produtos gerados: {result.novos_produtos}")
    write_execution_summary(args, result, exit_code=0)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Atualiza uma copia da planilha WordPress usando a planilha do cliente "
            "como fonte de estoque/preco e gera SKUs para novos produtos sem predefinir IDs."
        )
    )
    parser.add_argument(
        "--conciliacao-folder",
        type=Path,
        default=DEFAULT_CONCILIACAO_FOLDER,
        help="Pasta onde ficam os arquivos xlsx de conciliacao: cliente e wordpress.",
    )
    parser.add_argument("--cliente", type=Path, nargs="?", help="Caminho da planilha do cliente. Se ausente, procura em --conciliacao-folder.")
    parser.add_argument(
        "--wordpress",
        type=Path,
        nargs="?",
        help="Caminho da planilha do WordPress. Se ausente, procura em --conciliacao-folder.",
    )
    parser.add_argument("--sem-wordpress", action="store_true", help="Somente gera SKU, sem atualizar WordPress.")
    parser.add_argument("--dry-run", action="store_true", help="Processa e valida sem gravar arquivos finais.")
    parser.add_argument(
        "--saida",
        type=Path,
        help="Arquivo WordPress atualizado. Padrao: [conciliacao_folder]/todos-os-produtos.xlsx.",
    )
    parser.add_argument(
        "--relatorio",
        type=Path,
        help="Relatorio de conciliacao. Padrao: [conciliacao_folder]/relatorio-conciliacao.xlsx.",
    )
    parser.add_argument(
        "--saida-novos-produtos",
        type=Path,
        help="Arquivo de novos produtos com apenas SKU, sem ID. Padrao: [conciliacao_folder]/produtos-novos.xlsx.",
    )
    parser.add_argument("--sheet-cliente", help="Nome da aba da planilha do cliente. Padrao: primeira aba.")
    parser.add_argument("--sheet-wordpress", default="Controle de Estoque", help="Aba da planilha WordPress.")
    parser.add_argument("--nome-coluna", help="Coluna de nome/produto na planilha do cliente.")
    parser.add_argument("--sku-coluna", help="Coluna de SKU/codigo na planilha do cliente, se existir.")
    parser.add_argument("--estoque-coluna", help="Coluna de estoque na planilha do cliente.")
    parser.add_argument("--preco-coluna", help="Coluna de preco na planilha do cliente.")
    parser.add_argument("--wordpress-id-coluna", help="Coluna de ID na planilha WordPress.")
    parser.add_argument("--wordpress-nome-coluna", help="Coluna de nome/produto na planilha WordPress.")
    parser.add_argument("--wordpress-sku-coluna", help="Coluna de SKU/codigo na planilha WordPress.")
    parser.add_argument("--wordpress-estoque-coluna", help="Coluna de estoque na planilha WordPress.")
    parser.add_argument("--wordpress-preco-coluna", help="Coluna de preco na planilha WordPress.")
    parser.add_argument("--log-dir", type=Path, help="Pasta para gravar logs da execucao. Padrao: MSN/logs.")
    parser.add_argument(
        "--summary-json",
        type=Path,
        help="Arquivo JSON de resumo final. Padrao: arquivo ao lado do log da execucao.",
    )
    parser.add_argument(
        "--proximo-id",
        type=int,
        help="Opcao legada. Novos produtos ficam sem ID para o WooCommerce gerar IDs seguros pelo SKU.",
    )
    return parser.parse_args()


def resolve_input_paths(args: argparse.Namespace) -> dict[str, Path]:
    if args.cliente and args.wordpress:
        return {
            "cliente": args.cliente.expanduser().resolve(),
            "wordpress": args.wordpress.expanduser().resolve(),
        }

    if args.cliente or args.wordpress:
        raise ValueError(
            "Informe ambos os arquivos --cliente e --wordpress ou nenhum dos dois; caso contrario use --conciliacao-folder."
        )

    conciliacao_folder = args.conciliacao_folder.expanduser().resolve()
    if not conciliacao_folder.exists():
        raise FileNotFoundError(f"Pasta de conciliacao nao encontrada: {conciliacao_folder}")

    cliente_file = find_xlsx_by_keyword(conciliacao_folder, "cliente")
    wordpress_file = find_xlsx_by_keyword(conciliacao_folder, "wordpress")
    return {"cliente": cliente_file, "wordpress": wordpress_file}


def find_xlsx_by_keyword(folder: Path, keyword: str) -> Path:
    keyword = keyword.lower()
    candidates = [
        path for path in folder.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".xlsx", ".xls", ".xlsm"}
        and keyword in path.stem.lower()
        and not path.name.startswith("~$")
    ]
    if not candidates:
        raise FileNotFoundError(f"Nenhum arquivo xlsx contendo '{keyword}' encontrado em: {folder}")
    if len(candidates) > 1:
        exact = [path for path in candidates if path.stem.lower() == keyword]
        if len(exact) == 1:
            return exact[0].resolve()
        raise ValueError(
            f"Mais de um arquivo xlsx contendo '{keyword}' encontrado em {folder}: {', '.join(str(path.name) for path in candidates)}"
        )
    return candidates[0].resolve()


def processar_planilha(args: argparse.Namespace) -> ProcessResult:
    paths = resolve_input_paths(args)
    cliente_path = paths["cliente"]
    if not cliente_path.exists():
        raise FileNotFoundError(f"Planilha do cliente nao encontrada: {cliente_path}")

    cliente_df = read_table(cliente_path, sheet_name=args.sheet_cliente)
    nome_col = resolve_column(cliente_df, args.nome_coluna, NAME_ALIASES, "nome/produto do cliente")
    sku_col = resolve_column(cliente_df, args.sku_coluna, SKU_ALIASES, "SKU do cliente", required=False)
    estoque_col = resolve_column(
        cliente_df,
        getattr(args, "estoque_coluna", None),
        STOCK_ALIASES,
        "estoque do cliente",
        required=False,
    )
    preco_col = resolve_column(
        cliente_df,
        getattr(args, "preco_coluna", None),
        PRICE_ALIASES,
        "preco do cliente",
        required=False,
    )

    resultado = cliente_df.copy()
    resultado["SKU_Gerado"] = resultado[nome_col].apply(gerar_sku)
    resultado["Status_Conciliacao"] = "sem_wordpress"
    resultado["ID_WordPress"] = ""
    resultado["SKU_Encontrado_WordPress"] = ""
    resultado["Nome_WordPress"] = ""
    resultado["Observacao_Conciliacao"] = ""

    if args.sem_wordpress:
        marcar_duplicados(resultado)
        args._last_status_counts = status_counts(resultado)
        args._last_validation_issues = []
        saida = output_path(cliente_path, args.saida, fallback_suffix="_conciliada")
        if getattr(args, "dry_run", False):
            print_summary(resultado, getattr(args, "_logger", None))
            emit(getattr(args, "_logger", None), "Dry-run: nenhum arquivo gravado.")
            return ProcessResult(saida=saida)
        write_report_output(resultado, saida)
        print_summary(resultado, getattr(args, "_logger", None))
        return ProcessResult(saida=saida)

    if args.wordpress:
        wordpress_path = args.wordpress.expanduser().resolve()
    else:
        wordpress_path = paths["wordpress"]
    if not wordpress_path.exists():
        raise FileNotFoundError(f"Planilha WordPress nao encontrada: {wordpress_path}")

    wordpress_df = read_table(wordpress_path, sheet_name=args.sheet_wordpress)
    wordpress_atualizada, validation_issues = atualizar_wordpress_com_cliente(
        resultado,
        wordpress_df,
        nome_col=nome_col,
        sku_col=sku_col,
        estoque_col=estoque_col,
        preco_col=preco_col,
        args=args,
    )

    marcar_duplicados(resultado)
    if args.saida:
        saida = output_path(wordpress_path, args.saida, fallback_suffix="_atualizada")
    else:
        conciliacao_folder = args.conciliacao_folder.expanduser().resolve()
        saida = conciliacao_folder / "todos-os-produtos.xlsx"
    if args.relatorio:
        relatorio = report_path(saida, getattr(args, "relatorio", None))
    else:
        conciliacao_folder = args.conciliacao_folder.expanduser().resolve()
        relatorio = conciliacao_folder / "relatorio-conciliacao.xlsx"
    if getattr(args, "saida_novos_produtos", None):
        saida_novos = output_path(saida, getattr(args, "saida_novos_produtos", None), fallback_suffix="_novos")
    else:
        conciliacao_folder = args.conciliacao_folder.expanduser().resolve()
        saida_novos = conciliacao_folder / "produtos-novos.xlsx"

    validation_issues.extend(validate_import_outputs(resultado, wordpress_atualizada))
    if getattr(args, "proximo_id", None) is not None:
        validation_issues.append(
            ValidationIssue(
                "aviso",
                None,
                "proximo_id",
                "parametro_legado",
                "--proximo-id foi ignorado; novos produtos ficam sem ID para o WooCommerce criar.",
            )
        )
    args._last_status_counts = status_counts(resultado)
    args._last_validation_issues = validation_issues

    if has_validation_errors(validation_issues):
        write_report_output(resultado, relatorio, validation_issues)
        raise ValidationFailure(validation_issues, report_path=relatorio)

    if getattr(args, "dry_run", False):
        write_report_output(resultado, relatorio, validation_issues)
        print_summary(resultado, getattr(args, "_logger", None))
        emit(getattr(args, "_logger", None), f"Dry-run: relatorio de validacao gerado em {relatorio}.")
        emit(getattr(args, "_logger", None), "Dry-run: arquivos finais de importacao nao foram gravados.")
        return ProcessResult(saida=saida, relatorio=relatorio, novos_produtos=saida_novos)

    write_wordpress_output(wordpress_atualizada, saida, sheet_name=args.sheet_wordpress)
    write_report_output(resultado, relatorio, validation_issues)
    write_new_products_output(resultado, wordpress_atualizada, saida_novos)
    print_summary(resultado, getattr(args, "_logger", None))
    emit(getattr(args, "_logger", None), f"Novos produtos gerados: {saida_novos}")
    return ProcessResult(saida=saida, relatorio=relatorio, novos_produtos=saida_novos)


def atualizar_wordpress_com_cliente(
    resultado: pd.DataFrame,
    wordpress_df: pd.DataFrame,
    *,
    nome_col: str,
    sku_col: str | None,
    estoque_col: str | None,
    preco_col: str | None,
    args: argparse.Namespace,
) -> tuple[pd.DataFrame, list[ValidationIssue]]:
    wordpress_atualizada = wordpress_df.copy()
    validation_issues: list[ValidationIssue] = []
    wp_id_col = resolve_or_create_column(
        wordpress_atualizada,
        getattr(args, "wordpress_id_coluna", None),
        ID_ALIASES,
        "ID",
    )
    wp_sku_col = resolve_or_create_column(
        wordpress_atualizada,
        getattr(args, "wordpress_sku_coluna", None),
        SKU_ALIASES,
        "SKU",
    )
    wp_nome_col = resolve_or_create_column(
        wordpress_atualizada,
        getattr(args, "wordpress_nome_coluna", None),
        NAME_ALIASES,
        "Nome",
    )
    wp_estoque_col = resolve_or_create_column(
        wordpress_atualizada,
        getattr(args, "wordpress_estoque_coluna", None),
        STOCK_ALIASES,
        "Estoque",
        create=estoque_col is not None,
    )
    wp_preco_col = resolve_or_create_column(
        wordpress_atualizada,
        getattr(args, "wordpress_preco_coluna", None),
        PRICE_ALIASES,
        "Preço",
        create=preco_col is not None,
    )

    wp_columns = WordPressColumns(
        id=wp_id_col,
        sku=wp_sku_col,
        nome=wp_nome_col,
        estoque=wp_estoque_col,
        preco=wp_preco_col,
    )
    wp_by_name, wp_by_sku, used_skus = build_wordpress_indexes(wordpress_atualizada, wp_columns)

    for index, row in resultado.iterrows():
        row_number = index + 2
        generated_sku = clean_cell(row.get("SKU_Gerado"))
        client_sku = clean_cell(row.get(sku_col)) if sku_col else ""
        client_name = clean_cell(row.get(nome_col))
        obs = []
        added_new_product = False

        if not client_name:
            resultado.at[index, "Status_Conciliacao"] = "ignorado_sem_nome"
            resultado.at[index, "Observacao_Conciliacao"] = "Linha sem nome/produto na planilha do cliente."
            continue

        stock_value, stock_issue = normalize_stock_value(row.get(estoque_col) if estoque_col else None, row_number, estoque_col)
        price_value, price_issue = normalize_price_value(row.get(preco_col) if preco_col else None, row_number, preco_col)
        row_issues = [issue for issue in (stock_issue, price_issue) if issue is not None]
        if row_issues:
            validation_issues.extend(row_issues)
            resultado.at[index, "Status_Conciliacao"] = "erro_validacao"
            resultado.at[index, "Observacao_Conciliacao"] = " ".join(issue.message for issue in row_issues)
            continue

        normalized_name = normalize_name(client_name)
        normalized_client_sku = normalize_sku(client_sku) if client_sku else ""
        match_status = ""
        wp_index: int | None = None
        if normalized_client_sku and normalized_client_sku in wp_by_sku:
            wp_index = wp_by_sku[normalized_client_sku]
            match_status = "atualizado_por_sku"
        elif normalized_name in wp_by_name:
            wp_index = wp_by_name[normalized_name]
            match_status = "atualizado_por_nome"

        if wp_index is not None:
            update_existing_wordpress_row(
                wordpress_atualizada,
                wp_index,
                stock_value=stock_value,
                price_value=price_value,
                wp_estoque_col=wp_columns.estoque,
                wp_preco_col=wp_columns.preco,
            )
            resultado.at[index, "Status_Conciliacao"] = match_status
            fill_result_from_wordpress_row(resultado, index, wordpress_atualizada, wp_index, wp_columns)
        else:
            possible_index, possible_score = find_possible_name_match(normalized_name, wp_by_name)
            if possible_index is not None:
                resultado.at[index, "Status_Conciliacao"] = "revisar_possivel_match"
                fill_result_from_wordpress_row(resultado, index, wordpress_atualizada, possible_index, wp_columns)
                obs.append(f"Possivel produto existente por nome similar ({possible_score:.0%}); revisar manualmente.")
                validation_issues.append(
                    ValidationIssue(
                        "aviso",
                        row_number,
                        "Nome",
                        "possivel_match",
                        "Produto nao foi criado por existir possivel match por nome.",
                    )
                )
            else:
                sku = unique_sku(generated_sku or client_sku or "SKU-MOD", used_skus)
                new_wp_index = append_new_wordpress_product(
                    wordpress_atualizada,
                    wp_columns,
                    sku=sku,
                    name=client_name,
                    stock_value=stock_value if estoque_col else "",
                    price_value=price_value if preco_col else "",
                )
                wp_by_name[normalized_name] = new_wp_index
                wp_by_sku[normalize_sku(sku)] = new_wp_index
                used_skus.add(normalize_sku(sku))
                resultado.at[index, "Status_Conciliacao"] = "adicionado_ao_wordpress"
                resultado.at[index, "SKU_Encontrado_WordPress"] = sku
                resultado.at[index, "Nome_WordPress"] = client_name
                added_new_product = True

        if added_new_product:
            obs.append("ID deixado em branco; WooCommerce criara o ID usando o SKU.")
        if not estoque_col:
            obs.append("Coluna de estoque do cliente nao encontrada.")
        if not preco_col:
            obs.append("Coluna de preco do cliente nao encontrada.")
        resultado.at[index, "Observacao_Conciliacao"] = " ".join(obs)

    return wordpress_atualizada, validation_issues


def build_wordpress_indexes(
    wordpress_df: pd.DataFrame,
    columns: WordPressColumns,
) -> tuple[dict[str, int], dict[str, int], set[str]]:
    by_name: dict[str, int] = {}
    by_sku: dict[str, int] = {}
    used_skus: set[str] = set()
    for wp_index, row in wordpress_df.iterrows():
        sku = clean_cell(row.get(columns.sku))
        name = clean_cell(row.get(columns.nome))
        if sku:
            normalized_sku = normalize_sku(sku)
            used_skus.add(normalized_sku)
            by_sku.setdefault(normalized_sku, wp_index)
        if name:
            by_name.setdefault(normalize_name(name), wp_index)
    return by_name, by_sku, used_skus


def fill_result_from_wordpress_row(
    resultado: pd.DataFrame,
    result_index: int,
    wordpress_df: pd.DataFrame,
    wordpress_index: int,
    columns: WordPressColumns,
) -> None:
    resultado.at[result_index, "ID_WordPress"] = clean_cell(wordpress_df.at[wordpress_index, columns.id])
    resultado.at[result_index, "SKU_Encontrado_WordPress"] = clean_cell(wordpress_df.at[wordpress_index, columns.sku])
    resultado.at[result_index, "Nome_WordPress"] = clean_cell(wordpress_df.at[wordpress_index, columns.nome])


def append_new_wordpress_product(
    wordpress_df: pd.DataFrame,
    columns: WordPressColumns,
    *,
    sku: str,
    name: str,
    stock_value: Any,
    price_value: Any,
) -> int:
    new_row = {column: "" for column in wordpress_df.columns}
    # WooCommerce cria o ID quando a linha nova chega sem ID; SKU atua como chave estavel.
    new_row[columns.sku] = sku
    new_row[columns.nome] = name
    if columns.estoque and has_value(stock_value):
        new_row[columns.estoque] = stock_value
    if columns.preco and has_value(price_value):
        new_row[columns.preco] = price_value
    wordpress_df.loc[len(wordpress_df)] = new_row
    return len(wordpress_df) - 1


def find_possible_name_match(normalized_name: str, wp_by_name: dict[str, int]) -> tuple[int | None, float]:
    best_index: int | None = None
    best_score = 0.0
    for candidate_name, wp_index in wp_by_name.items():
        score = SequenceMatcher(None, normalized_name, candidate_name).ratio()
        if score > best_score:
            best_score = score
            best_index = wp_index
    if best_index is not None and best_score >= 0.92:
        return best_index, best_score
    return None, best_score


def update_existing_wordpress_row(
    wordpress_df: pd.DataFrame,
    wp_index: int,
    *,
    stock_value: Any,
    price_value: Any,
    wp_estoque_col: str | None,
    wp_preco_col: str | None,
) -> None:
    if wp_estoque_col and has_value(stock_value):
        wordpress_df.at[wp_index, wp_estoque_col] = stock_value
    if wp_preco_col and has_value(price_value):
        wordpress_df.at[wp_index, wp_preco_col] = price_value


def marcar_duplicados(resultado: pd.DataFrame) -> None:
    duplicated_generated = resultado["SKU_Gerado"].map(normalize_sku).duplicated(keep=False)
    for index, duplicated in duplicated_generated.items():
        if not duplicated:
            continue
        current = clean_cell(resultado.at[index, "Observacao_Conciliacao"])
        note = "SKU_Gerado duplicado na planilha do cliente."
        resultado.at[index, "Observacao_Conciliacao"] = f"{current} {note}".strip()


def gerar_sku(nome: Any) -> str:
    if pd.isna(nome):
        return ""

    text = normalize_words(nome)
    parts = [
        infer_by_rules(text, CATEGORY_RULES, default="OUT"),
        infer_by_rules(text, BRAND_RULES, default="GEN"),
        infer_model(text),
    ]

    for suffix, terms in COLOR_RULES:
        if text_has_any(text, terms):
            parts.append(suffix)

    for suffix, terms in PACKAGE_RULES:
        if text_has_any(text, terms):
            parts.append(suffix)
            break

    return "-".join(part for part in parts if part)


def infer_by_rules(text: str, rules: list[tuple[str, list[str]]], default: str) -> str:
    for code, terms in rules:
        if text_has_any(text, terms):
            return code
    return default


def infer_model(text: str) -> str:
    candidates: list[str] = []
    for match in re.findall(r"\b[A-Z]{0,8}\d[A-Z0-9]{2,}(?:-[A-Z0-9]{2,})?\b", text):
        token = match.strip("-")
        if token and token not in MODEL_STOP_WORDS:
            candidates.append(token.replace("-", ""))

    if not candidates:
        words = [word for word in re.findall(r"\b[A-Z0-9]{4,24}\b", text) if word not in MODEL_STOP_WORDS]
        candidates.extend([word for word in words if any(char.isdigit() for char in word)])

    return candidates[0] if candidates else "MOD"


def read_table(path: Path, sheet_name: str | None = None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return read_csv(path)
    if suffix in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet_name or 0, dtype=object)
    raise ValueError(f"Formato nao suportado: {path.suffix}")


def read_csv(path: Path) -> pd.DataFrame:
    errors: list[str] = []
    for encoding in ("utf-8-sig", "utf-8", "latin1"):
        try:
            return pd.read_csv(path, sep=None, engine="python", encoding=encoding, dtype=object)
        except Exception as exc:
            errors.append(f"{encoding}: {exc}")
    raise RuntimeError("Nao foi possivel ler CSV. " + " | ".join(errors))


def _atomic_excel_write(writer_func: Callable[[Any], None], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp")
    try:
        with pd.ExcelWriter(temp_path, engine="openpyxl") as writer:
            writer_func(writer)
        temp_path.replace(path)
    except PermissionError as exc:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
        raise PermissionError(
            f"Permissão negada ao gravar {path}. Feche o arquivo se estiver aberto no Excel e tente novamente."
        ) from exc


def write_report_output(
    df: pd.DataFrame,
    path: Path,
    validation_issues: list[ValidationIssue] | None = None,
) -> None:
    if path.suffix.lower() == ".csv":
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        if validation_issues:
            issues_path = path.with_name(f"{path.stem}-validacao.csv")
            validation_issues_frame(validation_issues).to_csv(issues_path, index=False, encoding="utf-8-sig")
        return

    def writer_func(writer: Any) -> None:
        df.to_excel(writer, index=False, sheet_name="conciliacao")
        df[df["Status_Conciliacao"].isin(["novo_para_wordpress", "adicionado_ao_wordpress"])].to_excel(
            writer,
            index=False,
            sheet_name="novos",
        )
        df[df["Status_Conciliacao"] == "adicionado_ao_wordpress"].to_excel(
            writer,
            index=False,
            sheet_name="adicionados",
        )
        df[df["Status_Conciliacao"].isin(["atualizado_por_nome", "atualizado_por_sku"])].to_excel(
            writer,
            index=False,
            sheet_name="atualizados",
        )
        validation_issues_frame(validation_issues or []).to_excel(
            writer,
            index=False,
            sheet_name="validacao",
        )

    _atomic_excel_write(writer_func, path)


def validation_issues_frame(issues: list[ValidationIssue]) -> pd.DataFrame:
    fields = ["severity", "row_number", "field", "code", "message"]
    if not issues:
        return pd.DataFrame(columns=fields)
    return pd.DataFrame([issue.as_row() for issue in issues], columns=fields)


def write_wordpress_output(df: pd.DataFrame, path: Path, sheet_name: str) -> None:
    if path.suffix.lower() == ".csv":
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        return

    def writer_func(writer: Any) -> None:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31] or "Planilha")

    _atomic_excel_write(writer_func, path)


def output_path(input_path: Path, output_arg: Path | None, fallback_suffix: str) -> Path:
    if output_arg:
        output_arg = output_arg.expanduser()
        if output_arg.exists() and output_arg.is_dir():
            return output_arg / f"{input_path.stem}{fallback_suffix}.xlsx"
        if output_arg.suffix:
            return output_arg.resolve()
        return output_arg.resolve() / f"{input_path.stem}{fallback_suffix}.xlsx"
    return input_path.with_name(f"{input_path.stem}{fallback_suffix}.xlsx")


def report_path(output_file: Path, report_arg: Path | None) -> Path:
    if report_arg:
        report_arg = report_arg.expanduser()
        if report_arg.exists() and report_arg.is_dir():
            return report_arg / f"{output_file.stem}_relatorio.xlsx"
        if report_arg.suffix:
            return report_arg.resolve()
        return report_arg.resolve() / f"{output_file.stem}_relatorio.xlsx"
    return output_file.with_name(f"{output_file.stem}_relatorio.xlsx")


def validate_import_outputs(resultado: pd.DataFrame, wordpress_df: pd.DataFrame) -> list[ValidationIssue]:
    novos_import = new_products_import_frame(resultado, wordpress_df)
    issues = validate_new_products_dataframe(
        novos_import,
        id_error_code="id_em_novos",
        id_error_message="produtos-novos nao pode conter coluna ID.",
        missing_sku_message="produtos-novos precisa conter coluna SKU.",
        empty_sku_message="SKU vazio em produtos novos.",
        duplicated_sku_message_prefix="SKU duplicado em produtos novos",
    )

    wp_id_col = resolve_column(wordpress_df, None, ID_ALIASES, "ID WordPress", required=False)
    wp_sku_col = resolve_column(wordpress_df, None, SKU_ALIASES, "SKU WordPress", required=False)
    wp_id_by_sku: dict[str, Any] = {}
    if wp_id_col and wp_sku_col:
        for _, row in wordpress_df.iterrows():
            sku = normalize_sku(row.get(wp_sku_col))
            if sku:
                wp_id_by_sku[sku] = row.get(wp_id_col)

    for index, row in resultado.iterrows():
        row_number = index + 2
        status = clean_cell(row.get("Status_Conciliacao"))
        result_sku = clean_cell(row.get("SKU_Encontrado_WordPress"))
        result_id = clean_cell(row.get("ID_WordPress"))
        if status == "adicionado_ao_wordpress":
            if result_id:
                issues.append(ValidationIssue("erro", row_number, "ID_WordPress", "id_novo_preenchido", "Produto novo deve ficar sem ID."))
            wp_id = wp_id_by_sku.get(normalize_sku(result_sku))
            if has_value(wp_id):
                issues.append(
                    ValidationIssue(
                        "erro",
                        row_number,
                        "ID",
                        "id_novo_na_planilha",
                        f"Produto novo {result_sku} foi gravado com ID na planilha WordPress.",
                    )
                )
        if status in {"atualizado_por_nome", "atualizado_por_sku"} and not result_id:
            if result_sku:
                issues.append(
                    ValidationIssue(
                        "aviso",
                        row_number,
                        "ID_WordPress",
                        "id_existente_ausente_com_sku",
                        "Produto existente sem ID; importacao deve usar SKU como chave.",
                    )
                )
            else:
                issues.append(
                    ValidationIssue(
                        "erro",
                        row_number,
                        "ID_WordPress",
                        "id_existente_e_sku_ausentes",
                        "Produto existente atualizado sem ID e sem SKU.",
                    )
                )

    return issues


def has_validation_errors(issues: list[ValidationIssue]) -> bool:
    return any(issue.severity == "erro" for issue in issues)


def write_new_products_output(resultado: pd.DataFrame, wordpress_df: pd.DataFrame, path: Path) -> None:
    output = new_products_import_frame(resultado, wordpress_df)
    if path.suffix.lower() == ".csv":
        path.parent.mkdir(parents=True, exist_ok=True)
        output.to_csv(path, index=False, encoding="utf-8-sig")
        return

    def writer_func(writer: Any) -> None:
        output.to_excel(writer, index=False, sheet_name="novos")

    _atomic_excel_write(writer_func, path)


def new_products_import_frame(resultado: pd.DataFrame, wordpress_df: pd.DataFrame | None = None) -> pd.DataFrame:
    novos = resultado[resultado["Status_Conciliacao"] == "adicionado_ao_wordpress"].copy()
    new_skus = {normalize_sku(value) for value in novos["SKU_Encontrado_WordPress"].tolist() if normalize_sku(value)}
    if wordpress_df is None:
        return novos[["SKU_Encontrado_WordPress"]].rename(
            columns={"SKU_Encontrado_WordPress": "SKU"}
        ).reset_index(drop=True)

    wp_sku_col = resolve_column(wordpress_df, None, SKU_ALIASES, "SKU WordPress", required=False)
    if not wp_sku_col or not new_skus:
        return pd.DataFrame(columns=[column for column in wordpress_df.columns if normalize_header(column) != "id"])

    mask = wordpress_df[wp_sku_col].map(lambda value: normalize_sku(value) in new_skus)
    output = wordpress_df.loc[mask].copy().reset_index(drop=True)
    id_columns = [column for column in output.columns if normalize_header(column) in ID_ALIASES]
    if id_columns:
        output = output.drop(columns=id_columns)
    return output


def resolve_or_create_column(
    df: pd.DataFrame,
    explicit: str | None,
    aliases: set[str],
    default_name: str,
    *,
    create: bool = True,
) -> str | None:
    column = resolve_column(df, explicit, aliases, default_name, required=False)
    if column:
        return column
    if not create:
        return None
    df[default_name] = pd.Series([""] * len(df), index=df.index, dtype=object)
    return default_name


def resolve_column(
    df: pd.DataFrame,
    explicit: str | None,
    aliases: set[str],
    label: str,
    *,
    required: bool = True,
) -> str | None:
    columns = [str(column).strip() for column in df.columns]
    by_normalized = {normalize_header(column): column for column in columns}

    if explicit:
        normalized = normalize_header(explicit)
        if normalized in by_normalized:
            return by_normalized[normalized]
        if required:
            raise ValueError(f"Coluna informada para {label} nao encontrada: {explicit}")
        return None

    for alias in aliases:
        if alias in by_normalized:
            return by_normalized[alias]

    if required:
        raise ValueError(f"Nao encontrei coluna de {label}. Colunas disponiveis: {', '.join(columns)}")
    return None


def print_summary(df: pd.DataFrame, logger: Any | None = None) -> None:
    emit(logger, "Resumo:")
    for status, count in status_counts(df).items():
        emit(logger, f"- {status}: {count}")


def status_counts(df: pd.DataFrame) -> dict[str, int]:
    if "Status_Conciliacao" not in df.columns:
        return {}
    counts = df["Status_Conciliacao"].value_counts(dropna=False)
    return {str(status): int(count) for status, count in counts.items()}


def validation_counts(issues: list[ValidationIssue] | None) -> dict[str, int]:
    counts: dict[str, int] = {}
    for issue in issues or []:
        key = f"{issue.severity}:{issue.code}"
        counts[key] = counts.get(key, 0) + 1
    return counts


def default_summary_path(args: argparse.Namespace) -> Path:
    explicit = getattr(args, "summary_json", None)
    if explicit:
        return explicit.expanduser().resolve()
    log_path = getattr(args, "_log_path", None)
    if log_path:
        return Path(log_path).with_suffix(".json")
    return (ROOT_DIR / "logs" / "conciliador_planilhas_sku-summary.json").resolve()


def write_execution_summary(
    args: argparse.Namespace,
    result: ProcessResult | None,
    *,
    exit_code: int,
    issues: list[ValidationIssue] | None = None,
    error: str | None = None,
) -> None:
    summary_path = default_summary_path(args)
    payload = {
        "script": "conciliador_planilhas_sku.py",
        "exit_code": exit_code,
        "dry_run": bool(getattr(args, "dry_run", False)),
        "inputs": {
            "cliente": str(getattr(args, "cliente", "") or ""),
            "wordpress": str(getattr(args, "wordpress", "") or ""),
            "conciliacao_folder": str(getattr(args, "conciliacao_folder", "") or ""),
        },
        "outputs": {
            "todos_os_produtos": str(result.saida) if result else "",
            "relatorio": str(result.relatorio) if result and result.relatorio else "",
            "produtos_novos": str(result.novos_produtos) if result and result.novos_produtos else "",
            "log": str(getattr(args, "_log_path", "") or ""),
        },
        "status_counts": getattr(args, "_last_status_counts", {}),
        "validation_counts": validation_counts(issues or getattr(args, "_last_validation_issues", [])),
        "error": error or "",
    }
    write_json(summary_path, payload)


def unique_sku(base_sku: str, used_skus: set[str]) -> str:
    base = safe_sku(base_sku)
    candidate = base
    suffix = 2
    while normalize_sku(candidate) in used_skus:
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


def safe_sku(value: str) -> str:
    text = normalize_words(value).replace(" ", "-")
    text = re.sub(r"[^A-Z0-9-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "SKU-MOD"


def text_has_any(text: str, values: list[str]) -> bool:
    padded = f" {text} "
    for value in values:
        target = normalize_words(value)
        if f" {target} " in padded:
            return True
    return False


def normalize_name(value: Any) -> str:
    return normalize_words(value)


def clean_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def has_value(value: Any) -> bool:
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    return str(value).strip() != ""


if __name__ == "__main__":
    raise SystemExit(main())
