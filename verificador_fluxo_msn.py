from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from msn_utils import (
    ValidationIssue,
    column_by_normalized_name,
    emit,
    emit_error,
    normalize_header,
    normalize_sku,
    setup_script_logging,
    validate_new_products_dataframe,
    write_json,
)


ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_CONCILIACAO_FOLDER = Path.home() / "Desktop" / "Conciliacao"


@dataclass(frozen=True)
class VerificationResult:
    issues: list[ValidationIssue]
    summary: dict[str, Any]

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == "erro" for issue in self.issues)


def main() -> int:
    args = parse_args()
    logger, log_path = setup_script_logging("verificador_fluxo_msn", ROOT_DIR, args.log_dir)
    args._log_path = log_path
    try:
        result = verify_flow(args)
    except Exception as exc:
        emit_error(logger, f"Erro ao verificar fluxo: {exc}")
        write_summary(args, VerificationResult([ValidationIssue("erro", None, "fluxo", "erro_execucao", str(exc))], {}), 1)
        return 1

    for issue in result.issues:
        prefix = issue.severity.upper()
        emit(logger, f"{prefix} {issue.code}: {issue.message}")
    if not result.issues:
        emit(logger, "OK: artefatos locais prontos para piloto WooCommerce.")

    exit_code = 2 if result.has_errors else 0
    write_summary(args, result, exit_code)
    return exit_code


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verifica os artefatos locais do fluxo MSN antes do piloto WooCommerce.")
    parser.add_argument("--conciliacao-folder", type=Path, default=DEFAULT_CONCILIACAO_FOLDER)
    parser.add_argument("--todos", type=Path, help="Arquivo todos-os-produtos.xlsx.")
    parser.add_argument("--novos", type=Path, help="Arquivo produtos-novos.xlsx.")
    parser.add_argument("--relatorio", type=Path, help="Arquivo relatorio-conciliacao.xlsx.")
    parser.add_argument("--sample", type=Path, help="Arquivo de amostra piloto, se houver.")
    parser.add_argument("--summary-json", type=Path, help="Arquivo JSON de saida da verificacao.")
    parser.add_argument("--log-dir", type=Path, help="Pasta para logs. Padrao: MSN/logs.")
    return parser.parse_args()


def verify_flow(args: argparse.Namespace) -> VerificationResult:
    folder = args.conciliacao_folder.expanduser().resolve()
    todos_path = resolve_artifact(args.todos, folder / "todos-os-produtos.xlsx")
    novos_path = resolve_artifact(args.novos, folder / "produtos-novos.xlsx")
    relatorio_path = resolve_artifact(args.relatorio, folder / "relatorio-conciliacao.xlsx")
    sample_path = resolve_artifact(args.sample, folder / "produtos-novos-amostra-5.xlsx", required=False)

    issues: list[ValidationIssue] = []
    summary: dict[str, Any] = {
        "artifacts": {
            "todos": str(todos_path),
            "novos": str(novos_path),
            "relatorio": str(relatorio_path),
            "sample": str(sample_path) if sample_path else "",
        },
        "status_counts": {},
        "novos_rows": 0,
        "sample_rows": 0,
        "remaining_external_blocker": "credenciais reais WooCommerce para executar --woo-apply",
    }

    for label, path in (("todos", todos_path), ("novos", novos_path), ("relatorio", relatorio_path)):
        if not path.exists():
            issues.append(ValidationIssue("erro", None, label, "arquivo_ausente", f"Arquivo obrigatorio ausente: {path}"))
    if issues:
        return VerificationResult(issues, summary)

    report_df, validation_df = read_report(relatorio_path)
    summary["status_counts"] = status_counts(report_df)
    issues.extend(validate_report(validation_df))

    novos_df = pd.read_excel(novos_path, sheet_name=0, dtype=object)
    summary["novos_rows"] = len(novos_df)
    issues.extend(validate_new_products_file(novos_df))

    todos_df = pd.read_excel(todos_path, sheet_name=0, dtype=object)
    issues.extend(validate_new_products_in_todos(novos_df, todos_df))

    added_count = int(summary["status_counts"].get("adicionado_ao_wordpress", 0))
    if added_count and added_count != len(novos_df):
        issues.append(
            ValidationIssue(
                "erro",
                None,
                "produtos-novos",
                "quantidade_novos_inconsistente",
                f"Relatorio tem {added_count} adicionados, mas produtos-novos tem {len(novos_df)} linhas.",
            )
        )

    if sample_path and sample_path.exists():
        sample_df = pd.read_excel(sample_path, sheet_name=0, dtype=object)
        summary["sample_rows"] = len(sample_df)
        sample_issues = validate_new_products_file(sample_df)
        for issue in sample_issues:
            issues.append(
                ValidationIssue(issue.severity, issue.row_number, "sample", f"sample_{issue.code}", issue.message)
            )
        if len(sample_df) > 5:
            issues.append(ValidationIssue("aviso", None, "sample", "sample_maior_que_5", "Amostra piloto tem mais de 5 linhas."))
    else:
        issues.append(ValidationIssue("aviso", None, "sample", "sample_ausente", "Amostra piloto nao encontrada."))

    return VerificationResult(issues, summary)


def resolve_artifact(path: Path | None, default: Path, *, required: bool = True) -> Path | None:
    if path:
        return path.expanduser().resolve()
    if required or default.exists():
        return default.resolve()
    return None


def read_report(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    report_df = pd.read_excel(path, sheet_name="conciliacao", dtype=object)
    try:
        validation_df = pd.read_excel(path, sheet_name="validacao", dtype=object)
    except ValueError:
        validation_df = pd.DataFrame(columns=["severity", "code", "message"])
    return report_df, validation_df


def validate_report(validation_df: pd.DataFrame) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if validation_df.empty:
        return issues
    normalized_columns = {normalize_header(column): column for column in validation_df.columns}
    severity_col = normalized_columns.get("severity")
    code_col = normalized_columns.get("code")
    message_col = normalized_columns.get("message")
    if not severity_col:
        return [ValidationIssue("erro", None, "validacao", "validacao_sem_severity", "Aba validacao sem coluna severity.")]
    for index, row in validation_df.iterrows():
        severity = str(row.get(severity_col) or "").strip().lower()
        if severity != "erro":
            continue
        issues.append(
            ValidationIssue(
                "erro",
                int(index) + 2,
                "validacao",
                str(row.get(code_col) or "erro_validacao") if code_col else "erro_validacao",
                str(row.get(message_col) or "Erro critico na aba validacao.") if message_col else "Erro critico na aba validacao.",
            )
        )
    return issues


def validate_new_products_file(df: pd.DataFrame) -> list[ValidationIssue]:
    return validate_new_products_dataframe(df)


def validate_new_products_in_todos(novos_df: pd.DataFrame, todos_df: pd.DataFrame) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    novos_sku_col = column_by_name(novos_df, "sku")
    todos_sku_col = column_by_name(todos_df, "sku")
    todos_id_col = column_by_name(todos_df, "id")
    if not novos_sku_col or not todos_sku_col:
        return issues
    if not todos_id_col:
        return issues + [ValidationIssue("erro", None, "ID", "id_ausente_em_todos", "todos-os-produtos precisa ter coluna ID.")]

    todos_by_sku = {normalize_sku(row.get(todos_sku_col)): row.get(todos_id_col) for _, row in todos_df.iterrows()}
    for index, row in novos_df.iterrows():
        sku = normalize_sku(row.get(novos_sku_col))
        if not sku:
            continue
        if sku not in todos_by_sku:
            issues.append(ValidationIssue("erro", int(index) + 2, "SKU", "sku_novo_ausente_em_todos", f"SKU novo ausente em todos-os-produtos: {row.get(novos_sku_col)}"))
            continue
        if has_value(todos_by_sku[sku]):
            issues.append(ValidationIssue("erro", int(index) + 2, "ID", "id_novo_preenchido_em_todos", f"SKU novo esta com ID preenchido em todos-os-produtos: {row.get(novos_sku_col)}"))
    return issues


def column_by_name(df: pd.DataFrame, normalized_name: str) -> str | None:
    return column_by_normalized_name(df, normalized_name)


def has_value(value: Any) -> bool:
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except TypeError:
        pass
    if isinstance(value, str):
        return bool(value.strip())
    return True


def status_counts(df: pd.DataFrame) -> dict[str, int]:
    status_col = column_by_name(df, "statusconciliacao")
    if not status_col:
        return {}
    counts = df[status_col].value_counts(dropna=False)
    return {str(status): int(count) for status, count in counts.items()}


def default_summary_path(args: argparse.Namespace) -> Path:
    if args.summary_json:
        return args.summary_json.expanduser().resolve()
    folder = args.conciliacao_folder.expanduser().resolve()
    return folder / "verificacao-fluxo-msn.json"


def write_summary(args: argparse.Namespace, result: VerificationResult, exit_code: int) -> None:
    payload = {
        "script": "verificador_fluxo_msn.py",
        "exit_code": exit_code,
        "has_errors": result.has_errors,
        "summary": result.summary,
        "issues": [issue.as_row() for issue in result.issues],
        "log": str(getattr(args, "_log_path", "") or ""),
    }
    write_json(default_summary_path(args), payload)


if __name__ == "__main__":
    raise SystemExit(main())
