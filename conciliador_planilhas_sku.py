from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_WORDPRESS_FILE = (
    Path.home()
    / "Desktop"
    / "cópia de produtos"
    / "Produtos"
    / "Controle_de_estoque_Com_Filtro.xlsx"
)

NAME_ALIASES = {
    "nome",
    "produto",
    "descricao",
    "descricaoproduto",
    "descricaodoproduto",
    "item",
    "itens",
    "mercadoria",
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


def main() -> int:
    args = parse_args()

    try:
        result = processar_planilha(args)
    except Exception as exc:
        print(f"Erro ao processar: {exc}", file=sys.stderr)
        return 1

    print(f"Arquivo gerado: {result.saida}")
    if result.relatorio:
        print(f"Relatorio gerado: {result.relatorio}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Atualiza uma copia da planilha WordPress usando a planilha do cliente "
            "como fonte de estoque/preco e gera SKUs para novos produtos."
        )
    )
    parser.add_argument("cliente", type=Path, help="Caminho da planilha do cliente (.xlsx, .xls ou .csv).")
    parser.add_argument(
        "--wordpress",
        type=Path,
        default=DEFAULT_WORDPRESS_FILE,
        help="Planilha base de importacao do WordPress. Padrao: Desktop/cópia de produtos/Produtos.",
    )
    parser.add_argument("--sem-wordpress", action="store_true", help="Somente gera SKU, sem atualizar WordPress.")
    parser.add_argument(
        "--saida",
        type=Path,
        help="Arquivo WordPress atualizado. Padrao: [wordpress]_atualizada.xlsx.",
    )
    parser.add_argument(
        "--relatorio",
        type=Path,
        help="Relatorio de conciliacao. Padrao: [saida]_relatorio.xlsx.",
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
    parser.add_argument("--proximo-id", type=int, help="ID inicial para novos produtos. Padrao: maior ID + 1.")
    return parser.parse_args()


def processar_planilha(args: argparse.Namespace) -> ProcessResult:
    cliente_path = args.cliente.expanduser().resolve()
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
        saida = output_path(cliente_path, args.saida, fallback_suffix="_conciliada")
        write_report_output(resultado, saida)
        print_summary(resultado)
        return ProcessResult(saida=saida)

    wordpress_path = args.wordpress.expanduser().resolve()
    if not wordpress_path.exists():
        raise FileNotFoundError(f"Planilha WordPress nao encontrada: {wordpress_path}")

    wordpress_df = read_table(wordpress_path, sheet_name=args.sheet_wordpress)
    wordpress_atualizada = atualizar_wordpress_com_cliente(
        resultado,
        wordpress_df,
        nome_col=nome_col,
        sku_col=sku_col,
        estoque_col=estoque_col,
        preco_col=preco_col,
        args=args,
    )

    marcar_duplicados(resultado)
    saida = output_path(wordpress_path, args.saida, fallback_suffix="_atualizada")
    relatorio = report_path(saida, getattr(args, "relatorio", None))
    write_wordpress_output(wordpress_atualizada, saida, sheet_name=args.sheet_wordpress)
    write_report_output(resultado, relatorio)
    print_summary(resultado)
    return ProcessResult(saida=saida, relatorio=relatorio)


def atualizar_wordpress_com_cliente(
    resultado: pd.DataFrame,
    wordpress_df: pd.DataFrame,
    *,
    nome_col: str,
    sku_col: str | None,
    estoque_col: str | None,
    preco_col: str | None,
    args: argparse.Namespace,
) -> pd.DataFrame:
    wordpress_atualizada = wordpress_df.copy()
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

    wp_by_name: dict[str, int] = {}
    used_skus: set[str] = set()
    for wp_index, row in wordpress_atualizada.iterrows():
        sku = clean_cell(row.get(wp_sku_col))
        name = clean_cell(row.get(wp_nome_col))
        if sku:
            used_skus.add(normalize_sku(sku))
        if name:
            wp_by_name.setdefault(normalize_name(name), wp_index)

    proximo_id = getattr(args, "proximo_id", None)
    next_id = proximo_id if proximo_id is not None else next_numeric_id(wordpress_atualizada[wp_id_col])
    for index, row in resultado.iterrows():
        generated_sku = clean_cell(row.get("SKU_Gerado"))
        client_sku = clean_cell(row.get(sku_col)) if sku_col else ""
        client_name = clean_cell(row.get(nome_col))
        obs = []

        if not client_name:
            resultado.at[index, "Status_Conciliacao"] = "ignorado_sem_nome"
            resultado.at[index, "Observacao_Conciliacao"] = "Linha sem nome/produto na planilha do cliente."
            continue

        normalized_name = normalize_name(client_name)
        if normalized_name in wp_by_name:
            wp_index = wp_by_name[normalized_name]
            update_existing_wordpress_row(
                wordpress_atualizada,
                wp_index,
                row,
                estoque_col=estoque_col,
                preco_col=preco_col,
                wp_estoque_col=wp_estoque_col,
                wp_preco_col=wp_preco_col,
            )
            resultado.at[index, "Status_Conciliacao"] = "atualizado_por_nome"
            resultado.at[index, "ID_WordPress"] = clean_cell(wordpress_atualizada.at[wp_index, wp_id_col])
            resultado.at[index, "SKU_Encontrado_WordPress"] = clean_cell(wordpress_atualizada.at[wp_index, wp_sku_col])
            resultado.at[index, "Nome_WordPress"] = clean_cell(wordpress_atualizada.at[wp_index, wp_nome_col])
        else:
            sku = unique_sku(generated_sku or client_sku or "SKU-MOD", used_skus)
            new_row = {column: "" for column in wordpress_atualizada.columns}
            new_row[wp_id_col] = next_id
            new_row[wp_sku_col] = sku
            new_row[wp_nome_col] = client_name
            if estoque_col and wp_estoque_col:
                new_row[wp_estoque_col] = row.get(estoque_col)
            if preco_col and wp_preco_col:
                new_row[wp_preco_col] = row.get(preco_col)

            wordpress_atualizada.loc[len(wordpress_atualizada)] = new_row
            wp_by_name[normalized_name] = len(wordpress_atualizada) - 1
            used_skus.add(normalize_sku(sku))
            resultado.at[index, "Status_Conciliacao"] = "adicionado_ao_wordpress"
            resultado.at[index, "ID_WordPress"] = str(next_id)
            resultado.at[index, "SKU_Encontrado_WordPress"] = sku
            resultado.at[index, "Nome_WordPress"] = client_name
            next_id += 1

        if not estoque_col:
            obs.append("Coluna de estoque do cliente nao encontrada.")
        if not preco_col:
            obs.append("Coluna de preco do cliente nao encontrada.")
        resultado.at[index, "Observacao_Conciliacao"] = " ".join(obs)

    return wordpress_atualizada


def update_existing_wordpress_row(
    wordpress_df: pd.DataFrame,
    wp_index: int,
    client_row: pd.Series,
    *,
    estoque_col: str | None,
    preco_col: str | None,
    wp_estoque_col: str | None,
    wp_preco_col: str | None,
) -> None:
    if estoque_col and wp_estoque_col and has_value(client_row.get(estoque_col)):
        wordpress_df.at[wp_index, wp_estoque_col] = client_row.get(estoque_col)
    if preco_col and wp_preco_col and has_value(client_row.get(preco_col)):
        wordpress_df.at[wp_index, wp_preco_col] = client_row.get(preco_col)


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


def write_report_output(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        df.to_csv(path, index=False, encoding="utf-8-sig")
        return

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
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
        df[df["Status_Conciliacao"] == "atualizado_por_nome"].to_excel(
            writer,
            index=False,
            sheet_name="atualizados",
        )


def write_wordpress_output(df: pd.DataFrame, path: Path, sheet_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        df.to_csv(path, index=False, encoding="utf-8-sig")
        return
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31] or "Planilha")


def output_path(input_path: Path, output_arg: Path | None, fallback_suffix: str) -> Path:
    if output_arg:
        return output_arg.expanduser().resolve()
    return input_path.with_name(f"{input_path.stem}{fallback_suffix}.xlsx")


def report_path(output_file: Path, report_arg: Path | None) -> Path:
    if report_arg:
        return report_arg.expanduser().resolve()
    return output_file.with_name(f"{output_file.stem}_relatorio.xlsx")


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
    df[default_name] = ""
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


def print_summary(df: pd.DataFrame) -> None:
    counts = df["Status_Conciliacao"].value_counts(dropna=False)
    print("Resumo:")
    for status, count in counts.items():
        print(f"- {status}: {count}")


def next_numeric_id(values: pd.Series) -> int:
    max_id = 0
    for value in values:
        try:
            if pd.isna(value):
                continue
            number = int(float(str(value).strip()))
        except (TypeError, ValueError):
            continue
        max_id = max(max_id, number)
    return max_id + 1


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


def normalize_header(value: Any) -> str:
    text = strip_accents(str(value or "")).lower()
    return re.sub(r"[^a-z0-9]+", "", text)


def normalize_words(value: Any) -> str:
    text = strip_accents(str(value or "")).upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_name(value: Any) -> str:
    return normalize_words(value)


def normalize_sku(value: Any) -> str:
    return re.sub(r"[^A-Z0-9]+", "", normalize_words(value))


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


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
