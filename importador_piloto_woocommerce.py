from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from msn_utils import (
    emit,
    emit_error,
    has_cell_value,
    normalize_header,
    normalize_numeric_text,
    normalize_sku,
    retry_call,
    setup_script_logging,
    write_json,
)


ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_CONCILIACAO_FOLDER = Path.home() / "Desktop" / "Conciliacao"
DEFAULT_SAMPLE_WORKBOOK = DEFAULT_CONCILIACAO_FOLDER / "produtos-novos-amostra-5.xlsx"
DEFAULT_NEW_PRODUCTS_WORKBOOK = DEFAULT_CONCILIACAO_FOLDER / "produtos-novos.xlsx"

NAME_ALIASES = {"nome", "name", "produto", "descricao", "descricaoproduto"}
SKU_ALIASES = {"sku", "codigo", "codigoproduto", "ref", "referencia"}
PRICE_ALIASES = {"preco", "price", "regularprice", "valor", "valorunitario"}
STOCK_ALIASES = {"estoque", "stock", "stockquantity", "quantidade", "qtd"}
ID_ALIASES = {"id", "codigoid", "idproduto"}


@dataclass(frozen=True)
class WooConfig:
    site_url: str
    consumer_key: str
    consumer_secret: str

    @property
    def products_url(self) -> str:
        return f"{self.site_url.rstrip('/')}/wp-json/wc/v3/products"


@dataclass
class ImportResult:
    sku: str
    status: str
    product_id: int | None = None
    message: str = ""


class PilotImportValidationError(RuntimeError):
    pass


class WooCommerceApiError(RuntimeError):
    pass


def main() -> int:
    args = parse_args()
    logger, log_path = setup_script_logging("importador_piloto_woocommerce", ROOT_DIR, args.log_dir)
    args._logger = logger
    args._log_path = log_path
    args._has_woo_credentials = False
    args._resolved_site_url = ""

    try:
        rows = load_import_rows(args.workbook, args.sheet, args.limit)
        config = resolve_config(args)
        args._has_woo_credentials = config is not None and not is_placeholder_config(config)
        args._resolved_site_url = config.site_url if config else ""
        if (args.apply or args.preflight_only) and (config is None or is_placeholder_config(config)):
            raise PilotImportValidationError(
                "Para importar de verdade, informe WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY "
                "e WOOCOMMERCE_CONSUMER_SECRET, ou use as flags correspondentes."
            )
        if args.preflight_only:
            assert config is not None
            preflight_woocommerce(config, args)
            results = [ImportResult(sku="preflight", status="ok", message="API WooCommerce autenticada")]
        elif args.apply:
            assert config is not None
            preflight_woocommerce(config, args)
            results = run_import(rows, config, args)
        else:
            results = run_import(rows, config, args)
    except PilotImportValidationError as exc:
        emit_error(logger, f"Erro de validacao: {exc}")
        write_execution_summary(args, [], exit_code=2, error=str(exc))
        return 2
    except Exception as exc:
        logger.exception("Erro ao importar piloto")
        emit_error(logger, f"Erro ao importar piloto: {exc}")
        write_execution_summary(args, [], exit_code=1, error=str(exc))
        return 1

    for result in results:
        suffix = f" id={result.product_id}" if result.product_id else ""
        detail = f" - {result.message}" if result.message else ""
        emit(logger, f"{result.sku}: {result.status}{suffix}{detail}")
    write_execution_summary(args, results, exit_code=0)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Importa um lote piloto de produtos novos no WooCommerce usando SKU como chave. "
            "Sem --apply, apenas valida e mostra o plano."
        )
    )
    parser.add_argument(
        "--workbook",
        type=Path,
        default=DEFAULT_SAMPLE_WORKBOOK if DEFAULT_SAMPLE_WORKBOOK.exists() else DEFAULT_NEW_PRODUCTS_WORKBOOK,
        help="Planilha de produtos novos. Padrao: Desktop/Conciliacao/produtos-novos-amostra-5.xlsx.",
    )
    parser.add_argument("--sheet", default="novos", help="Aba da planilha.")
    parser.add_argument("--limit", type=int, default=5, help="Quantidade maxima de produtos no piloto.")
    parser.add_argument("--apply", action="store_true", help="Executa criacao real no WooCommerce.")
    parser.add_argument("--preflight-only", action="store_true", help="Valida credenciais/API WooCommerce e nao cria produtos.")
    parser.add_argument("--update-existing", action="store_true", help="Atualiza produto existente encontrado por SKU.")
    parser.add_argument("--status", choices=["draft", "publish", "private"], default="draft", help="Status dos produtos criados.")
    parser.add_argument("--env-file", type=Path, help="Arquivo local com credenciais WOOCOMMERCE_URL/KEY/SECRET.")
    parser.add_argument("--site-url", help="URL base da loja.")
    parser.add_argument(
        "--consumer-key",
        help="Consumer key WooCommerce.",
    )
    parser.add_argument(
        "--consumer-secret",
        help="Consumer secret WooCommerce.",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout HTTP em segundos.")
    parser.add_argument("--retries", type=int, default=1, help="Retentativas HTTP em erro de rede/429.")
    parser.add_argument("--retry-backoff", type=float, default=3.0, help="Backoff progressivo entre retentativas.")
    parser.add_argument("--log-dir", type=Path, help="Pasta para logs. Padrao: MSN/logs.")
    parser.add_argument("--summary-json", type=Path, help="Arquivo JSON de resumo final.")
    return parser.parse_args()


def resolve_config(args: argparse.Namespace) -> WooConfig | None:
    env_file_values = read_env_file(args.env_file) if getattr(args, "env_file", None) else {}
    site_url = first_config_value(args.site_url, env_file_values, "WOOCOMMERCE_URL", "WC_SITE_URL")
    consumer_key = first_config_value(
        args.consumer_key,
        env_file_values,
        "WOOCOMMERCE_CONSUMER_KEY",
        "WC_CONSUMER_KEY",
    )
    consumer_secret = first_config_value(
        args.consumer_secret,
        env_file_values,
        "WOOCOMMERCE_CONSUMER_SECRET",
        "WC_CONSUMER_SECRET",
    )
    if not site_url or not consumer_key or not consumer_secret:
        return None
    return WooConfig(
        site_url=str(site_url).strip(),
        consumer_key=str(consumer_key).strip(),
        consumer_secret=str(consumer_secret).strip(),
    )


def is_placeholder_config(config: WooConfig) -> bool:
    values = [config.site_url, config.consumer_key, config.consumer_secret]
    placeholders = ("sua-loja.com.br", "substitua", "ck_...", "cs_...")
    return any(any(marker in value.lower() for marker in placeholders) for value in values)


def first_config_value(explicit: str | None, env_file_values: dict[str, str], *names: str) -> str | None:
    if explicit:
        return explicit
    for name in names:
        if env_file_values.get(name):
            return env_file_values[name]
    for name in names:
        if os.getenv(name):
            return os.getenv(name)
    return None


def read_env_file(path: Path) -> dict[str, str]:
    env_path = path.expanduser().resolve()
    if not env_path.exists():
        raise PilotImportValidationError(f"Arquivo de credenciais nao encontrado: {env_path}")
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(env_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            raise PilotImportValidationError(f"Linha invalida no env-file {env_path}:{line_number}")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def load_import_rows(workbook: Path, sheet: str, limit: int) -> list[dict[str, Any]]:
    workbook = workbook.expanduser().resolve()
    if not workbook.exists():
        raise PilotImportValidationError(f"Planilha nao encontrada: {workbook}")
    df = pd.read_excel(workbook, sheet_name=sheet, dtype=object)
    if df.empty:
        raise PilotImportValidationError("Planilha de importacao esta vazia.")

    columns_by_normalized = {normalize_header(column): column for column in df.columns}
    if any(alias in columns_by_normalized for alias in ID_ALIASES):
        raise PilotImportValidationError("Planilha piloto nao pode conter coluna ID.")

    sku_col = find_column(columns_by_normalized, SKU_ALIASES, "SKU")
    name_col = find_column(columns_by_normalized, NAME_ALIASES, "Nome")
    price_col = find_column(columns_by_normalized, PRICE_ALIASES, "Preco", required=False)
    stock_col = find_column(columns_by_normalized, STOCK_ALIASES, "Estoque", required=False)

    rows: list[dict[str, Any]] = []
    seen_skus: set[str] = set()
    for index, row in df.head(max(0, limit)).iterrows():
        row_number = int(index) + 2
        sku = str(row.get(sku_col) or "").strip()
        name = str(row.get(name_col) or "").strip()
        normalized_sku = normalize_sku(sku)
        if not normalized_sku:
            raise PilotImportValidationError(f"SKU vazio na linha {row_number}.")
        if normalized_sku in seen_skus:
            raise PilotImportValidationError(f"SKU duplicado no piloto: {sku}")
        if not name:
            raise PilotImportValidationError(f"Nome vazio na linha {row_number}.")
        seen_skus.add(normalized_sku)
        rows.append(
            {
                "sku": sku,
                "name": name,
                "price": normalize_optional_price(row.get(price_col) if price_col else None, row_number),
                "stock": normalize_optional_stock(row.get(stock_col) if stock_col else None, row_number),
            }
        )
    if not rows:
        raise PilotImportValidationError("Nenhuma linha selecionada para o piloto.")
    return rows


def find_column(columns_by_normalized: dict[str, str], aliases: set[str], label: str, *, required: bool = True) -> str | None:
    for alias in aliases:
        if alias in columns_by_normalized:
            return columns_by_normalized[alias]
    if required:
        raise PilotImportValidationError(f"Coluna obrigatoria nao encontrada: {label}")
    return None


def normalize_optional_price(value: Any, row_number: int) -> str:
    if not has_cell_value(value):
        return ""
    try:
        number = float(normalize_numeric_text(value))
    except ValueError as exc:
        raise PilotImportValidationError(f"Preco invalido na linha {row_number}: {value}") from exc
    if number < 0:
        raise PilotImportValidationError(f"Preco negativo na linha {row_number}: {value}")
    return f"{number:.2f}"


def normalize_optional_stock(value: Any, row_number: int) -> int | None:
    if not has_cell_value(value):
        return None
    try:
        number = float(normalize_numeric_text(value))
    except ValueError as exc:
        raise PilotImportValidationError(f"Estoque invalido na linha {row_number}: {value}") from exc
    if not number.is_integer() or number < 0:
        raise PilotImportValidationError(f"Estoque deve ser inteiro positivo na linha {row_number}: {value}")
    return int(number)


def product_payload(row: dict[str, Any], status: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": row["name"],
        "sku": row["sku"],
        "type": "simple",
        "status": status,
    }
    if row.get("price"):
        payload["regular_price"] = row["price"]
    if row.get("stock") is not None:
        payload["manage_stock"] = True
        payload["stock_quantity"] = row["stock"]
    return payload


def run_import(rows: list[dict[str, Any]], config: WooConfig | None, args: argparse.Namespace) -> list[ImportResult]:
    results: list[ImportResult] = []
    for row in rows:
        sku = row["sku"]
        payload = product_payload(row, args.status)
        if not args.apply:
            results.append(ImportResult(sku=sku, status="dry_run", message="criacao planejada; --apply nao informado"))
            continue

        assert config is not None
        existing = find_existing_product(config, sku, args)
        if existing:
            product_id = int(existing.get("id") or 0) or None
            if not args.update_existing:
                results.append(ImportResult(sku=sku, status="skipped_existing", product_id=product_id))
                continue
            updated = update_product(config, product_id, payload, args)
            results.append(ImportResult(sku=sku, status="updated", product_id=int(updated.get("id") or product_id or 0)))
            continue

        created = create_product(config, payload, args)
        results.append(ImportResult(sku=sku, status="created", product_id=int(created.get("id") or 0)))
    return results


def preflight_woocommerce(config: WooConfig, args: argparse.Namespace) -> None:
    response = request_woocommerce(
        "get",
        config.products_url,
        config,
        args,
        params={"per_page": 1},
        label="preflight WooCommerce",
    )
    if not isinstance(response.json(), list):
        raise RuntimeError("Resposta inesperada da API WooCommerce no preflight.")


def find_existing_product(config: WooConfig, sku: str, args: argparse.Namespace) -> dict[str, Any] | None:
    response = request_woocommerce(
        "get",
        config.products_url,
        config,
        args,
        params={"sku": sku, "per_page": 1},
        label=f"buscar SKU {sku}",
    )
    data = response.json()
    if isinstance(data, list) and data:
        return data[0]
    return None


def create_product(config: WooConfig, payload: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    response = request_woocommerce("post", config.products_url, config, args, json=payload, label=f"criar SKU {payload['sku']}")
    return response.json()


def update_product(config: WooConfig, product_id: int | None, payload: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if not product_id:
        raise RuntimeError("Produto existente sem ID retornado pela API.")
    url = f"{config.products_url}/{product_id}"
    response = request_woocommerce("put", url, config, args, json=payload, label=f"atualizar SKU {payload['sku']}")
    return response.json()


def request_woocommerce(method: str, url: str, config: WooConfig, args: argparse.Namespace, *, label: str, **kwargs: Any) -> requests.Response:
    session = requests.Session()

    def operation() -> requests.Response:
        response = session.request(
            method.upper(),
            url,
            auth=(config.consumer_key, config.consumer_secret),
            timeout=args.timeout,
            **kwargs,
        )
        if response.status_code == 429:
            response.raise_for_status()
        response.raise_for_status()
        return response

    try:
        return retry_call(
            operation,
            attempts=max(1, args.retries + 1),
            backoff_seconds=args.retry_backoff,
            retry_exceptions=(requests.RequestException,),
            logger=getattr(args, "_logger", None),
            label=label,
        )
    except requests.HTTPError as exc:
        raise WooCommerceApiError(format_http_error(label, exc)) from exc
    except requests.RequestException as exc:
        raise WooCommerceApiError(f"{label}: falha de comunicacao com WooCommerce: {exc}") from exc


def format_http_error(label: str, exc: requests.HTTPError) -> str:
    response = exc.response
    if response is None:
        return f"{label}: erro HTTP sem resposta detalhada."
    detail = response_error_detail(response)
    base = f"{label}: WooCommerce retornou HTTP {response.status_code}"
    if response.status_code in {401, 403}:
        base += " (verifique URL, consumer key/secret e permissoes)"
    if response.status_code == 429:
        base += " (limite de requisicoes; tente novamente com backoff maior)"
    return f"{base}. {detail}".strip()


def response_error_detail(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        text = response.text.strip()
        return truncate_text(text, 240) if text else ""
    if isinstance(payload, dict):
        parts = []
        for key in ("code", "message"):
            if payload.get(key):
                parts.append(f"{key}={payload[key]}")
        if parts:
            return truncate_text("; ".join(parts), 240)
    return truncate_text(str(payload), 240)


def truncate_text(value: str, limit: int) -> str:
    text = value.replace("\n", " ").replace("\r", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def default_summary_path(args: argparse.Namespace) -> Path:
    if args.summary_json:
        return args.summary_json.expanduser().resolve()
    log_path = getattr(args, "_log_path", None)
    if log_path:
        return Path(log_path).with_suffix(".json")
    return (ROOT_DIR / "logs" / "importador_piloto_woocommerce-summary.json").resolve()


def write_execution_summary(
    args: argparse.Namespace,
    results: list[ImportResult],
    *,
    exit_code: int,
    error: str | None = None,
) -> None:
    status_counts: dict[str, int] = {}
    for result in results:
        status_counts[result.status] = status_counts.get(result.status, 0) + 1
    payload = {
        "script": "importador_piloto_woocommerce.py",
        "exit_code": exit_code,
        "apply": bool(args.apply),
        "preflight_only": bool(getattr(args, "preflight_only", False)),
        "workbook": str(args.workbook),
        "limit": args.limit,
        "site_url": str(getattr(args, "_resolved_site_url", "") or args.site_url or ""),
        "env_file": str(args.env_file) if args.env_file else "",
        "has_credentials": bool(getattr(args, "_has_woo_credentials", False)),
        "status_counts": status_counts,
        "results": [result.__dict__ for result in results],
        "log": str(getattr(args, "_log_path", "") or ""),
        "error": error or "",
    }
    write_json(default_summary_path(args), payload)


if __name__ == "__main__":
    raise SystemExit(main())
