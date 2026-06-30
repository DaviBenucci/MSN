from __future__ import annotations

import asyncio
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.services.file_security import FileValidationError, SavedUpload, save_upload_file


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CACHE_ROOT = PROJECT_ROOT / "cache" / "conciliacoes"
SCRIPT_PATH = PROJECT_ROOT / "conciliador_planilhas_sku.py"
ARTIFACTS = {
    "wordpress_atualizado": "wordpress_atualizada.xlsx",
    "relatorio": "relatorio_conciliacao.xlsx",
}

router = APIRouter(prefix="/api/v1", tags=["conciliador"])


@dataclass(frozen=True)
class SubprocessResult:
    returncode: int
    stdout: str
    stderr: str
    command: list[str]


@router.post("/conciliar")
async def conciliar_planilhas(
    cliente: UploadFile = File(...),
    wordpress: UploadFile = File(...),
) -> dict[str, Any]:
    job_id = uuid4().hex
    job_dir = (CACHE_ROOT / job_id).resolve()
    uploads_dir = job_dir / "uploads"
    outputs_dir = job_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    try:
        cliente_salvo = await save_upload_file(cliente, uploads_dir)
        wordpress_salvo = await save_upload_file(wordpress, uploads_dir)
    except FileValidationError as exc:
        cleanup_job_dir(job_dir)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    saida_path = outputs_dir / "wordpress_atualizada.xlsx"
    relatorio_path = outputs_dir / "relatorio_conciliacao.xlsx"

    result = await run_conciliador_subprocess(
        cliente_path=cliente_salvo.path,
        wordpress_path=wordpress_salvo.path,
        saida_path=saida_path,
        relatorio_path=relatorio_path,
    )

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Falha ao executar o conciliador.",
                "job_id": job_id,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            },
        )

    return {
        "job_id": job_id,
        "status": "concluido",
        "message": "Conciliacao finalizada.",
        "uploads": {
            "cliente": serialize_upload(cliente_salvo),
            "wordpress": serialize_upload(wordpress_salvo),
        },
        "outputs": {
            "wordpress_atualizado": serialize_artifact(
                job_id,
                "wordpress_atualizado",
                saida_path,
            ),
            "relatorio": serialize_artifact(job_id, "relatorio", relatorio_path),
        },
        "summary": extract_product_summary(relatorio_path),
        "logs": {
            "stdout": result.stdout,
            "stderr": result.stderr,
        },
    }


@router.get("/conciliar/{job_id}/download/{artifact}")
async def download_conciliacao_artifact(job_id: str, artifact: str) -> FileResponse:
    artifact_path = resolve_artifact_path(job_id, artifact)
    if not artifact_path.exists() or not artifact_path.is_file():
        raise HTTPException(status_code=404, detail="Arquivo nao encontrado.")

    return FileResponse(
        artifact_path,
        filename=artifact_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


async def run_conciliador_subprocess(
    *,
    cliente_path: Path,
    wordpress_path: Path,
    saida_path: Path,
    relatorio_path: Path,
) -> SubprocessResult:
    command = [
        sys.executable,
        str(SCRIPT_PATH),
        str(cliente_path),
        "--wordpress",
        str(wordpress_path),
        "--saida",
        str(saida_path),
        "--relatorio",
        str(relatorio_path),
    ]

    return await asyncio.to_thread(run_conciliador_command, command, str(PROJECT_ROOT))


def run_conciliador_command(command: list[str], cwd: str) -> SubprocessResult:
    completed = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return SubprocessResult(
        returncode=completed.returncode or 0,
        stdout=completed.stdout,
        stderr=completed.stderr,
        command=command,
    )


def extract_product_summary(relatorio_path: Path) -> list[dict[str, Any]]:
    try:
        df = pd.read_excel(relatorio_path, sheet_name='conciliacao', dtype=object)
    except Exception:
        return []

    def find_column(keys: list[str]) -> str | None:
        for column in df.columns:
            normalized = str(column).strip().lower()
            for key in keys:
                if key in normalized:
                    return column
        return None

    sku_col = find_column(['sku', 'codigo'])
    quantity_col = find_column(['estoque', 'quantidade', 'qtd', 'valor'])
    status_col = find_column(['status'])
    product_col = find_column(['nome', 'modelo', 'produto'])

    def clean_value(value: Any) -> str:
        if pd.isna(value):
            return ''
        return str(value).strip()

    summary: list[dict[str, Any]] = []
    for row in df.to_dict(orient='records'):
        sku = clean_value(row.get(sku_col)) if sku_col else ''
        quantity = clean_value(row.get(quantity_col)) if quantity_col else ''
        status_value = clean_value(row.get(status_col)) if status_col else ''
        product_name = clean_value(row.get(product_col)) if product_col else ''

        if not sku and not product_name:
            continue

        summary.append(
            {
                'sku': sku or product_name,
                'product_name': product_name,
                'quantity': quantity,
                'status': status_value,
            }
        )

    return summary[:30]


def serialize_upload(upload: SavedUpload) -> dict[str, Any]:
    return {
        "original_filename": upload.original_filename,
        "saved_filename": upload.saved_filename,
        "size_bytes": upload.size_bytes,
        "extension": upload.extension,
        "content_type": upload.content_type,
    }


def serialize_artifact(job_id: str, artifact: str, path: Path) -> dict[str, str]:
    return {
        "filename": path.name,
        "download_url": f"/api/v1/conciliar/{job_id}/download/{artifact}",
    }


def resolve_artifact_path(job_id: str, artifact: str) -> Path:
    if not job_id.isalnum() or len(job_id) > 64:
        raise HTTPException(status_code=404, detail="Job nao encontrado.")
    if artifact not in ARTIFACTS:
        raise HTTPException(status_code=404, detail="Arquivo nao encontrado.")

    root = CACHE_ROOT.expanduser().resolve()
    target = (root / job_id / "outputs" / ARTIFACTS[artifact]).resolve()
    if root not in target.parents:
        raise HTTPException(status_code=404, detail="Arquivo nao encontrado.")
    return target


def cleanup_job_dir(job_dir: Path) -> None:
    root = CACHE_ROOT.expanduser().resolve()
    target = job_dir.expanduser().resolve()
    if target.exists() and root in target.parents:
        shutil.rmtree(target)
