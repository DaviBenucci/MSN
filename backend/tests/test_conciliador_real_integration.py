from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.routers import conciliador


XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_conciliar_executes_real_script_and_downloads_outputs(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(conciliador, "CACHE_ROOT", tmp_path / "cache")

    wordpress_bytes = make_xlsx(
        pd.DataFrame(
            [
                {
                    "ID": 1,
                    "SKU": "TON-HP-Q2612A-PRT",
                    "Nome": "Toner HP Q2612A Preto",
                    "Estoque": 1,
                    "Preço": 100.0,
                }
            ]
        ),
        sheet_name="Controle de Estoque",
    )
    cliente_bytes = make_xlsx(
        pd.DataFrame(
            [
                {
                    "Nome": "Toner HP Q2612A Preto",
                    "Estoque": 7,
                    "Preço": 123.45,
                },
                {
                    "Nome": "Toner Ricoh 3503H Ciano",
                    "Estoque": 2,
                    "Preço": 88.0,
                },
            ]
        ),
    )

    client = TestClient(app)
    response = client.post(
        "/api/v1/conciliar",
        files={
            "cliente": ("cliente.xlsx", cliente_bytes, XLSX_MIME),
            "wordpress": ("wordpress.xlsx", wordpress_bytes, XLSX_MIME),
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "concluido"
    assert payload["outputs"]["wordpress_atualizado"]["download_url"]
    assert payload["outputs"]["relatorio"]["download_url"]

    wordpress_response = client.get(payload["outputs"]["wordpress_atualizado"]["download_url"])
    relatorio_response = client.get(payload["outputs"]["relatorio"]["download_url"])

    assert wordpress_response.status_code == 200
    assert relatorio_response.status_code == 200

    wordpress_result = pd.read_excel(
        BytesIO(wordpress_response.content),
        sheet_name="Controle de Estoque",
    )
    relatorio_result = pd.read_excel(BytesIO(relatorio_response.content), sheet_name="conciliacao")

    existing = wordpress_result[wordpress_result["Nome"] == "Toner HP Q2612A Preto"].iloc[0]
    added = wordpress_result[wordpress_result["Nome"] == "Toner Ricoh 3503H Ciano"].iloc[0]

    assert int(existing["Estoque"]) == 7
    assert float(existing["Preço"]) == 123.45
    assert int(added["ID"]) == 2
    assert added["SKU"] == "TON-RIC-3503H-CIA"
    assert int(added["Estoque"]) == 2
    assert float(added["Preço"]) == 88.0
    assert set(relatorio_result["Status_Conciliacao"]) == {
        "atualizado_por_nome",
        "adicionado_ao_wordpress",
    }


def make_xlsx(df: pd.DataFrame, sheet_name: str = "Sheet1") -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()
