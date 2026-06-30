from __future__ import annotations

import json
import logging
import re
import time
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar
from urllib.parse import unquote


T = TypeVar("T")


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    row_number: int | None
    field: str
    code: str
    message: str

    def as_row(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "row_number": self.row_number or "",
            "field": self.field,
            "code": self.code,
            "message": self.message,
        }


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_header(value: Any) -> str:
    text = strip_accents(str(value or "")).lower()
    return re.sub(r"[^a-z0-9]+", "", text)


def normalize_words(value: Any) -> str:
    text = strip_accents(unquote(str(value or ""))).upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_sku(value: Any) -> str:
    return re.sub(r"[^A-Z0-9]+", "", normalize_words(value))


def has_cell_value(value: Any) -> bool:
    if value is None:
        return False
    try:
        if value != value:
            return False
    except Exception:
        pass
    if isinstance(value, str):
        return bool(value.strip())
    return True


def normalize_numeric_text(value: Any) -> str:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    text = str(value).strip()
    text = re.sub(r"[R$\s]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[^0-9,.-]", "", text)
    if not text:
        raise ValueError("numero vazio")
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(".", "").replace(",", ".")
    if text in {"", "-", ".", "-."}:
        raise ValueError("numero vazio")
    float(text)
    return text


def normalize_stock_value(
    value: Any,
    row_number: int,
    column_name: str | None,
) -> tuple[Any, ValidationIssue | None]:
    if not has_cell_value(value):
        return "", None
    try:
        number = float(normalize_numeric_text(value))
    except ValueError:
        return "", ValidationIssue("erro", row_number, column_name or "Estoque", "estoque_invalido", f"Estoque invalido: {value}")
    if not number.is_integer():
        return "", ValidationIssue(
            "erro",
            row_number,
            column_name or "Estoque",
            "estoque_decimal",
            f"Estoque deve ser inteiro: {value}",
        )
    return int(number), None


def normalize_price_value(
    value: Any,
    row_number: int,
    column_name: str | None,
) -> tuple[Any, ValidationIssue | None]:
    if not has_cell_value(value):
        return "", None
    try:
        return float(normalize_numeric_text(value)), None
    except ValueError:
        return "", ValidationIssue("erro", row_number, column_name or "Preco", "preco_invalido", f"Preco invalido: {value}")


def safe_folder_name(value: str) -> str:
    text = strip_accents(str(value)).strip()
    text = re.sub(r"[<>:\"/\\|?*\x00-\x1F]", "-", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .") or "produto"


def path_to_str(path: Path | None) -> str:
    return "" if path is None else str(path)


def timestamp_slug() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def setup_script_logging(script_name: str, root_dir: Path, log_dir: Path | None = None) -> tuple[logging.Logger, Path]:
    target_dir = (log_dir or root_dir / "logs").expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    log_path = target_dir / f"{script_name}-{timestamp_slug()}.log"
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    return logger, log_path


def emit(logger: logging.Logger | None, message: str, *, error: bool = False) -> None:
    print(message)
    if logger is None:
        return
    if error:
        logger.error(message)
    else:
        logger.info(message)


def json_safe(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(item) for item in value]
    return value


def write_json(path: Path, payload: object) -> None:
    target = path.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(json_safe(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def retry_call(
    operation: Callable[[], T],
    *,
    attempts: int,
    backoff_seconds: float,
    retry_exceptions: Iterable[type[BaseException]] = (Exception,),
    logger: logging.Logger | None = None,
    label: str = "operacao",
) -> T:
    allowed = tuple(retry_exceptions)
    attempts = max(1, attempts)
    delay = max(0.0, backoff_seconds)
    last_error: BaseException | None = None
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except allowed as exc:
            last_error = exc
            if attempt >= attempts:
                break
            if logger:
                logger.warning("%s falhou na tentativa %s/%s: %s", label, attempt, attempts, exc)
            if delay:
                time.sleep(delay * attempt)
    assert last_error is not None
    raise last_error
