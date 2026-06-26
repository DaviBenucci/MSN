from __future__ import annotations

import argparse
import re
import sys
import unicodedata
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


def main() -> int:
    args = parse_args()

    try:
        result = processar_planilha(args)
    except Exception as exc:
        print(f"Erro ao processar: {exc}", file=sys.stderr)
        return 1

    print(f"Arquivo gerado: {result}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Gera SKUs padronizados para a planilha do cliente e, opcionalmente, "
            "concilia com a planilha usada para importar no WordPress."
        )
    )
    parser.add_argument("cliente", type=Path, help="Caminho da planilha do cliente (.xlsx, .xls ou .csv).")
    parser.add_argument(
        "--wordpress",
        type=Path,
        default=DEFAULT_WORDPRESS_FILE,
        help="Planilha base de importacao do WordPress. Padrao: Desktop/copia de produtos/Produtos.",
    )
    parser.add_argument("--sem-wordpress", action="store_true", help="Somente gera SKU, sem conciliar.")
    parser.add_argument("--saida", type=Path, help="Arquivo de saida. Padrao: [cliente]_conciliada.xlsx.")
    parser.add_argument("--sheet-cliente", help="Nome da aba da planilha do cliente. Padrao: primeira aba.")
    parser.add_argument("--sheet-wordpress", default="Controle de Estoque", help="Aba da planilha WordPress.")
    parser.add_argument("--nome-coluna", help="Coluna de nome/produto na planilha do cliente.")
    parser.add_argument("--sku-coluna", help="Coluna de SKU/codigo na planilha do cliente, se existir.")
    parser.add_argument("--wordpress-nome-coluna", help="Coluna de nome/produto na planilha WordPress.")
    parser.add_argument("--wordpress-sku-coluna", help="Coluna de SKU/codigo na planilha WordPress.")
    return parser.parse_args()


def processar_planilha(args: argparse.Namespace) -> Path:
    cliente_path = args.cliente.expanduser().resolve()
    if not cliente_path.exists():
        raise FileNotFoundError(f"Planilha do cliente nao encontrada: {cliente_path}")

    cliente_df = read_table(cliente_path, sheet_name=args.sheet_cliente)
    nome_col = resolve_column(cliente_df, args.nome_coluna, NAME_ALIASES, "nome/produto do cliente")
    sku_col = resolve_column(cliente_df, args.sku_coluna, SKU_ALIASES, "SKU do cliente", required=False)

    resultado = cliente_df.copy()
    resultado["SKU_Gerado"] = resultado[nome_col].apply(gerar_sku)
    resultado["Status_Conciliacao"] = "sem_wordpress"
    resultado["SKU_Encontrado_WordPress"] = ""
    resultado["Nome_WordPress"] = ""
    resultado["Observacao_Conciliacao"] = ""

    if not args.sem_wordpress:
        wordpress_path = args.wordpress.expanduser().resolve()
        if not wordpress_path.exists():
            resultado["Observacao_Conciliacao"] = f"Planilha WordPress nao encontrada: {wordpress_path}"
        else:
            wordpress_df = read_table(wordpress_path, sheet_name=args.sheet_wordpress)
            conciliar_com_wordpress(
                resultado,
                wordpress_df,
                nome_col=nome_col,
                sku_col=sku_col,
                wordpress_nome_col_arg=args.wordpress_nome_coluna,
                wordpress_sku_col_arg=args.wordpress_sku_coluna,
            )

    marcar_duplicados(resultado)
    saida = output_path(cliente_path, args.saida)
    write_output(resultado, saida)
    print_summary(resultado)
    return saida


def conciliar_com_wordpress(
    resultado: pd.DataFrame,
    wordpress_df: pd.DataFrame,
    *,
    nome_col: str,
    sku_col: str | None,
    wordpress_nome_col_arg: str | None,
    wordpress_sku_col_arg: str | None,
) -> None:
    wp_sku_col = resolve_column(wordpress_df, wordpress_sku_col_arg, SKU_ALIASES, "SKU WordPress")
    wp_nome_col = resolve_column(wordpress_df, wordpress_nome_col_arg, NAME_ALIASES, "nome/produto WordPress")

    wp_by_sku: dict[str, dict[str, str]] = {}
    wp_by_name: dict[str, dict[str, str]] = {}
    for _, row in wordpress_df.iterrows():
        sku = clean_cell(row.get(wp_sku_col))
        name = clean_cell(row.get(wp_nome_col))
        if sku:
            wp_by_sku.setdefault(normalize_sku(sku), {"sku": sku, "name": name})
        if name:
            wp_by_name.setdefault(normalize_name(name), {"sku": sku, "name": name})

    for index, row in resultado.iterrows():
        generated_sku = clean_cell(row.get("SKU_Gerado"))
        client_sku = clean_cell(row.get(sku_col)) if sku_col else ""
        client_name = clean_cell(row.get(nome_col))

        match = None
        status = "novo_para_wordpress"
        obs = []

        if client_sku and normalize_sku(client_sku) in wp_by_sku:
            match = wp_by_sku[normalize_sku(client_sku)]
            status = "existe_por_sku_cliente"
        elif generated_sku and normalize_sku(generated_sku) in wp_by_sku:
            match = wp_by_sku[normalize_sku(generated_sku)]
            status = "existe_por_sku_gerado"
        elif client_name and normalize_name(client_name) in wp_by_name:
            match = wp_by_name[normalize_name(client_name)]
            status = "possivel_existente_por_nome"
            obs.append("Nome igual encontrado na base WordPress.")

        if match:
            resultado.at[index, "SKU_Encontrado_WordPress"] = match["sku"]
            resultado.at[index, "Nome_WordPress"] = match["name"]
            if client_name and normalize_name(client_name) != normalize_name(match["name"]):
                obs.append("Nome do cliente difere do nome WordPress.")

        resultado.at[index, "Status_Conciliacao"] = status
        resultado.at[index, "Observacao_Conciliacao"] = " ".join(obs)


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


def write_output(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        df.to_csv(path, index=False, encoding="utf-8-sig")
        return

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="conciliacao")
        df[df["Status_Conciliacao"] == "novo_para_wordpress"].to_excel(writer, index=False, sheet_name="novos")
        df[df["Status_Conciliacao"] != "novo_para_wordpress"].to_excel(writer, index=False, sheet_name="existentes")


def output_path(input_path: Path, output_arg: Path | None) -> Path:
    if output_arg:
        return output_arg.expanduser().resolve()
    return input_path.with_name(f"{input_path.stem}_conciliada.xlsx")


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


if __name__ == "__main__":
    raise SystemExit(main())
