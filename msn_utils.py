from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote


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


def safe_folder_name(value: str) -> str:
    text = strip_accents(str(value)).strip()
    text = re.sub(r"[<>:\"/\\|?*\x00-\x1F]", "-", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .") or "produto"


def path_to_str(path: Path | None) -> str:
    return "" if path is None else str(path)
