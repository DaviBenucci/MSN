from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.routers import conciliador
from app.routers.conciliador import SubprocessResult


XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_conciliar_uploads_files_and_runs_subprocess(monkeypatch, tmp_path: Path) -> None:
    cache_root = tmp_path / "cache"
    captured: dict[str, Path] = {}

    async def fake_run_conciliador_subprocess(
        *,
        cliente_path: Path,
        wordpress_path: Path,
        saida_path: Path,
        relatorio_path: Path,
    ) -> SubprocessResult:
        captured["cliente_path"] = cliente_path
        captured["wordpress_path"] = wordpress_path
        captured["saida_path"] = saida_path
        captured["relatorio_path"] = relatorio_path
        return SubprocessResult(
            returncode=0,
            stdout="Resumo:\n- atualizado_por_nome: 1\n",
            stderr="",
            command=["fake"],
        )

    monkeypatch.setattr(conciliador, "CACHE_ROOT", cache_root)
    monkeypatch.setattr(conciliador, "run_conciliador_subprocess", fake_run_conciliador_subprocess)

    client = TestClient(app)
    response = client.post(
        "/api/v1/conciliar",
        files={
            "cliente": ("cliente.xlsx", b"cliente", XLSX_MIME),
            "wordpress": ("wordpress.csv", b"Nome,Preco\nProduto,10\n", "text/csv"),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "concluido"
    assert data["uploads"]["cliente"]["original_filename"] == "cliente.xlsx"
    assert data["uploads"]["wordpress"]["original_filename"] == "wordpress.csv"
    assert data["uploads"]["cliente"]["saved_filename"].endswith(".xlsx")
    assert data["uploads"]["wordpress"]["saved_filename"].endswith(".csv")
    assert data["outputs"]["wordpress_atualizado"]["filename"] == "wordpress_atualizada.xlsx"
    assert data["outputs"]["relatorio"]["filename"] == "relatorio_conciliacao.xlsx"
    assert data["outputs"]["wordpress_atualizado"]["download_url"].startswith(
        f"/api/v1/conciliar/{data['job_id']}/download/"
    )
    assert data["outputs"]["relatorio"]["download_url"].endswith("/download/relatorio")
    assert "atualizado_por_nome" in data["logs"]["stdout"]

    assert captured["cliente_path"].exists()
    assert captured["cliente_path"].read_bytes() == b"cliente"
    assert captured["wordpress_path"].exists()
    assert captured["wordpress_path"].read_bytes() == b"Nome,Preco\nProduto,10\n"
    assert captured["saida_path"].parent.name == "outputs"
    assert captured["relatorio_path"].parent == captured["saida_path"].parent


def test_conciliar_rejects_invalid_upload_before_subprocess(monkeypatch, tmp_path: Path) -> None:
    async def fail_if_called(**kwargs) -> SubprocessResult:
        raise AssertionError("Subprocesso nao deveria ser chamado para upload invalido.")

    monkeypatch.setattr(conciliador, "CACHE_ROOT", tmp_path / "cache")
    monkeypatch.setattr(conciliador, "run_conciliador_subprocess", fail_if_called)

    client = TestClient(app)
    response = client.post(
        "/api/v1/conciliar",
        files={
            "cliente": ("cliente.exe", b"danger", "application/octet-stream"),
            "wordpress": ("wordpress.xlsx", b"wordpress", XLSX_MIME),
        },
    )

    assert response.status_code == 400
    assert "Extensao nao permitida" in response.json()["detail"]


def test_conciliar_returns_500_when_subprocess_fails(monkeypatch, tmp_path: Path) -> None:
    async def fake_run_conciliador_subprocess(**kwargs) -> SubprocessResult:
        return SubprocessResult(
            returncode=1,
            stdout="Resumo parcial",
            stderr="Erro ao processar planilha",
            command=["fake"],
        )

    monkeypatch.setattr(conciliador, "CACHE_ROOT", tmp_path / "cache")
    monkeypatch.setattr(conciliador, "run_conciliador_subprocess", fake_run_conciliador_subprocess)

    client = TestClient(app)
    response = client.post(
        "/api/v1/conciliar",
        files={
            "cliente": ("cliente.xlsx", b"cliente", XLSX_MIME),
            "wordpress": ("wordpress.xlsx", b"wordpress", XLSX_MIME),
        },
    )

    assert response.status_code == 500
    detail = response.json()["detail"]
    assert detail["message"] == "Falha ao executar o conciliador."
    assert detail["returncode"] == 1
    assert detail["stdout"] == "Resumo parcial"
    assert detail["stderr"] == "Erro ao processar planilha"


def test_download_conciliacao_artifact_returns_file(monkeypatch, tmp_path: Path) -> None:
    cache_root = tmp_path / "cache"
    output_dir = cache_root / "abc123" / "outputs"
    output_dir.mkdir(parents=True)
    expected_file = output_dir / "wordpress_atualizada.xlsx"
    expected_file.write_bytes(b"xlsx-result")

    monkeypatch.setattr(conciliador, "CACHE_ROOT", cache_root)

    client = TestClient(app)
    response = client.get("/api/v1/conciliar/abc123/download/wordpress_atualizado")

    assert response.status_code == 200
    assert response.content == b"xlsx-result"
    assert "wordpress_atualizada.xlsx" in response.headers["content-disposition"]


def test_download_conciliacao_artifact_rejects_unknown_artifact(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(conciliador, "CACHE_ROOT", tmp_path / "cache")

    client = TestClient(app)
    response = client.get("/api/v1/conciliar/abc123/download/../../secret")

    assert response.status_code == 404
