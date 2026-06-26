import asyncio
from io import BytesIO
from pathlib import Path

import pytest

from app.services.file_security import FileValidationError, save_upload_file


class FakeUploadFile:
    def __init__(self, filename: str, content_type: str, content: bytes) -> None:
        self.filename = filename
        self.content_type = content_type
        self._file = BytesIO(content)

    async def read(self, size: int = -1) -> bytes:
        return self._file.read(size)

    async def seek(self, offset: int) -> None:
        self._file.seek(offset)


def run_async(coro):
    return asyncio.run(coro)


def test_save_upload_file_renames_allowed_xlsx_with_uuid(tmp_path: Path) -> None:
    upload = FakeUploadFile(
        filename="estoque_cliente.xlsx",
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        content=b"xlsx-content",
    )

    saved = run_async(save_upload_file(upload, tmp_path))

    assert saved.original_filename == "estoque_cliente.xlsx"
    assert saved.extension == ".xlsx"
    assert saved.saved_filename.endswith(".xlsx")
    assert saved.saved_filename != "estoque_cliente.xlsx"
    assert saved.path.parent == tmp_path.resolve()
    assert saved.path.read_bytes() == b"xlsx-content"


def test_save_upload_file_sanitizes_original_name_and_prevents_path_traversal(tmp_path: Path) -> None:
    upload = FakeUploadFile(
        filename="../../cliente.csv",
        content_type="text/csv",
        content=b"Nome,Preco\nProduto,10\n",
    )

    saved = run_async(save_upload_file(upload, tmp_path))

    assert saved.original_filename == "cliente.csv"
    assert saved.path.parent == tmp_path.resolve()
    assert saved.path.name != "cliente.csv"
    assert not (tmp_path.parent / "cliente.csv").exists()


@pytest.mark.parametrize("filename", ["virus.exe", "script.sh"])
def test_save_upload_file_rejects_dangerous_extensions(tmp_path: Path, filename: str) -> None:
    upload = FakeUploadFile(
        filename=filename,
        content_type="application/octet-stream",
        content=b"danger",
    )

    with pytest.raises(FileValidationError, match="Extensao nao permitida"):
        run_async(save_upload_file(upload, tmp_path))

    assert list(tmp_path.iterdir()) == []


def test_save_upload_file_rejects_wrong_mime_type(tmp_path: Path) -> None:
    upload = FakeUploadFile(
        filename="cliente.csv",
        content_type="application/x-msdownload",
        content=b"Nome,Preco\nProduto,10\n",
    )

    with pytest.raises(FileValidationError, match="Tipo MIME"):
        run_async(save_upload_file(upload, tmp_path))

    assert list(tmp_path.iterdir()) == []


def test_save_upload_file_removes_partial_file_when_size_exceeds_limit(tmp_path: Path) -> None:
    upload = FakeUploadFile(
        filename="cliente.csv",
        content_type="text/csv",
        content=b"123456",
    )

    with pytest.raises(FileValidationError, match="tamanho maximo"):
        run_async(save_upload_file(upload, tmp_path, max_size_bytes=3))

    assert list(tmp_path.iterdir()) == []
