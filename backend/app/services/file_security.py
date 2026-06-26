from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from uuid import uuid4

import aiofiles


MAX_UPLOAD_SIZE_BYTES = 25 * 1024 * 1024
CHUNK_SIZE_BYTES = 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    ".csv": {
        "text/csv",
        "application/csv",
        "application/vnd.ms-excel",
        "text/plain",
    },
    ".xlsx": {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    },
}


class UploadLike(Protocol):
    filename: str | None
    content_type: str | None

    async def read(self, size: int = -1) -> bytes:
        ...

    async def seek(self, offset: int) -> None:
        ...


@dataclass(frozen=True)
class SavedUpload:
    original_filename: str
    saved_filename: str
    path: Path
    size_bytes: int
    extension: str
    content_type: str


class FileValidationError(ValueError):
    """Raised when an uploaded file does not satisfy security rules."""


async def save_upload_file(
    upload_file: UploadLike,
    destination_dir: Path,
    *,
    max_size_bytes: int = MAX_UPLOAD_SIZE_BYTES,
) -> SavedUpload:
    original_filename = sanitize_original_filename(upload_file.filename)
    extension = validate_extension(original_filename)
    content_type = validate_content_type(upload_file.content_type, extension)
    destination = prepare_destination_dir(destination_dir)
    saved_filename = f"{uuid4().hex}{extension}"
    saved_path = (destination / saved_filename).resolve()

    if saved_path.parent != destination:
        raise FileValidationError("Caminho de destino invalido.")

    size_bytes = 0
    await upload_file.seek(0)
    try:
        async with aiofiles.open(saved_path, "wb") as output_file:
            while True:
                chunk = await upload_file.read(CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                size_bytes += len(chunk)
                if size_bytes > max_size_bytes:
                    raise FileValidationError("Arquivo excede o tamanho maximo permitido.")

                await output_file.write(chunk)
    except Exception:
        if saved_path.exists():
            saved_path.unlink()
        raise

    return SavedUpload(
        original_filename=original_filename,
        saved_filename=saved_filename,
        path=saved_path,
        size_bytes=size_bytes,
        extension=extension,
        content_type=content_type,
    )


def sanitize_original_filename(filename: str | None) -> str:
    if not filename:
        raise FileValidationError("Nome de arquivo ausente.")

    name = Path(filename).name.strip()
    name = re.sub(r"[\x00-\x1f]+", "", name)
    if not name or name in {".", ".."}:
        raise FileValidationError("Nome de arquivo invalido.")
    return name


def validate_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_CONTENT_TYPES:
        allowed = ", ".join(sorted(ALLOWED_CONTENT_TYPES))
        raise FileValidationError(f"Extensao nao permitida. Use apenas: {allowed}.")
    return extension


def validate_content_type(content_type: str | None, extension: str) -> str:
    normalized = normalize_content_type(content_type)
    allowed = ALLOWED_CONTENT_TYPES[extension]
    if normalized not in allowed:
        raise FileValidationError("Tipo MIME nao permitido para este arquivo.")
    return normalized


def normalize_content_type(content_type: str | None) -> str:
    if not content_type:
        raise FileValidationError("Tipo MIME ausente.")
    return content_type.split(";", 1)[0].strip().lower()


def prepare_destination_dir(destination_dir: Path) -> Path:
    destination = destination_dir.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    return destination
