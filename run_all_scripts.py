from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import conciliador_planilhas_sku as conciliador

DEFAULT_CONCILIACAO_FOLDER = Path.home() / "Desktop" / "Conciliacao"
DEFAULT_DESKTOP = Path.home() / "Desktop"

SCRIPT_ROOT = Path(__file__).resolve().parent
CONCILIADOR = SCRIPT_ROOT / "conciliador_planilhas_sku.py"
BUSCADOR = SCRIPT_ROOT / "buscador_candidatas_imagens.py"
OTIMIZADOR = SCRIPT_ROOT / "otimizador_imagens.py"


def run_script(command: list[str]) -> int:
    print("\n=> Executando:", " ".join(command))
    completed = subprocess.run(command, text=True)
    if completed.returncode != 0:
        print(f"Erro: comando retornou {completed.returncode}")
    return completed.returncode


def expected_conciliador_output(args: argparse.Namespace, conciliacao_folder: Path) -> Path:
    if not args.saida:
        return conciliacao_folder / "todos-os-produtos.xlsx"

    if args.wordpress:
        wordpress_path = args.wordpress.expanduser().resolve()
    else:
        wordpress_path = conciliador.find_xlsx_by_keyword(conciliacao_folder, "wordpress")
    return conciliador.output_path(wordpress_path, args.saida, fallback_suffix="_atualizada")


def expected_relatorio_output(args: argparse.Namespace, todos_workbook: Path, conciliacao_folder: Path) -> Path:
    if args.relatorio:
        return conciliador.report_path(todos_workbook, args.relatorio)
    return conciliacao_folder / "relatorio-conciliacao.xlsx"


def expected_novos_output(args: argparse.Namespace, todos_workbook: Path, conciliacao_folder: Path) -> Path:
    if args.saida_novos_produtos:
        return conciliador.output_path(todos_workbook, args.saida_novos_produtos, fallback_suffix="_novos")
    return conciliacao_folder / "produtos-novos.xlsx"


def json_safe(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def write_manifest(path: Path | None, manifest: dict[str, object]) -> None:
    if path is None:
        return
    target = path.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def summarize_conciliacao_report(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        from openpyxl import load_workbook

        workbook = load_workbook(path, read_only=True, data_only=True)
        worksheet = workbook["conciliacao"] if "conciliacao" in workbook.sheetnames else workbook.active
        headers = [str(cell.value or "").strip() for cell in worksheet[1]]
        try:
            status_index = headers.index("Status_Conciliacao") + 1
        except ValueError:
            workbook.close()
            return {}
        counts: dict[str, int] = {}
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            status = str(row[status_index - 1] or "").strip() or "vazio"
            counts[status] = counts.get(status, 0) + 1
        workbook.close()
        return {
            "status_counts": counts,
            "atualizados": counts.get("atualizado_por_nome", 0) + counts.get("atualizado_por_sku", 0),
            "novos": counts.get("adicionado_ao_wordpress", 0),
            "ignorados": counts.get("ignorado_sem_nome", 0),
            "erros": counts.get("erro_validacao", 0),
        }
    except Exception as exc:
        return {"summary_error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Executa os scripts MSN em sequencia local.")
    parser.add_argument(
        "--conciliacao-folder",
        type=Path,
        default=DEFAULT_CONCILIACAO_FOLDER,
        help="Pasta Desktop/Conciliacao onde estao os arquivos cliente e wordpress.",
    )
    parser.add_argument(
        "--desktop-folder-name",
        required=True,
        help="Nome da pasta no Desktop onde o buscador criará as subpastas por SKU.",
    )
    parser.add_argument("--cliente", type=Path, help="Caminho da planilha do cliente para conciliador.")
    parser.add_argument("--wordpress", type=Path, help="Caminho da planilha do WordPress para conciliador.")
    parser.add_argument("--saida", type=Path, help="Pasta ou arquivo de saida para o conciliador. Recomendado usar default no Conciliacao.")
    parser.add_argument("--relatorio", type=Path, help="Pasta ou arquivo de relatorio para o conciliador.")
    parser.add_argument(
        "--saida-novos-produtos",
        type=Path,
        help="Pasta ou arquivo de saida para o arquivo de novos produtos do conciliador.",
    )
    parser.add_argument("--all", action="store_true", help="Executa todos os passos: conciliador, buscador e otimizador.")
    parser.add_argument("--sheet-cliente", help="Aba da planilha do cliente.")
    parser.add_argument("--sheet-wordpress", help="Aba da planilha WordPress.")
    parser.add_argument(
        "--proximo-id",
        type=int,
        help="Opcao legada; novos produtos ficam sem ID para o WooCommerce gerar IDs pelo SKU.",
    )
    parser.add_argument("--search-sheet", help="Aba da planilha para busca de imagens.")
    parser.add_argument(
        "--include-existing-products",
        action="store_true",
        help="Faz o buscador processar todos os produtos, mesmo os que já têm imagens locais.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Força reprocessar imagens existentes no otimizador.")
    parser.add_argument("--white-background", action="store_true", help="Gera WebP com fundo branco no otimizador.")
    parser.add_argument("--no-download", action="store_true", help="Nao baixa imagens durante a busca de candidatas.")
    parser.add_argument("--skip-images", action="store_true", help="Roda apenas o conciliador e para antes do buscador/otimizador.")
    parser.add_argument("--manifesto", type=Path, help="Arquivo JSON com resumo dos comandos, artefatos e exit codes.")
    args = parser.parse_args()

    conciliacao_folder = args.conciliacao_folder.expanduser().resolve()
    candidate_root = DEFAULT_DESKTOP / args.desktop_folder_name
    candidate_root.mkdir(parents=True, exist_ok=True)
    todos_workbook = expected_conciliador_output(args, conciliacao_folder)
    relatorio_workbook = expected_relatorio_output(args, todos_workbook, conciliacao_folder)
    novos_workbook = expected_novos_output(args, todos_workbook, conciliacao_folder)
    manifesto_path = args.manifesto or (conciliacao_folder / "manifesto-execucao.json")
    manifest: dict[str, object] = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "conciliacao_folder": str(conciliacao_folder),
        "candidate_root": str(candidate_root),
        "artifacts": {
            "todos_workbook": str(todos_workbook),
            "produtos_novos": str(novos_workbook),
            "relatorio": str(relatorio_workbook),
        },
        "steps": [],
        "args": json_safe(vars(args) | {
            "conciliacao_folder": str(conciliacao_folder),
            "desktop_folder_name": args.desktop_folder_name,
            "manifesto": str(manifesto_path),
        }),
    }

    conciliador_command = [
        sys.executable,
        str(CONCILIADOR),
        "--conciliacao-folder",
        str(conciliacao_folder),
    ]
    if args.sheet_cliente:
        conciliador_command.extend(["--sheet-cliente", args.sheet_cliente])
    if args.sheet_wordpress:
        conciliador_command.extend(["--sheet-wordpress", args.sheet_wordpress])
    if args.proximo_id is not None:
        conciliador_command.extend(["--proximo-id", str(args.proximo_id)])
    if args.cliente:
        conciliador_command.extend(["--cliente", str(args.cliente)])
    if args.wordpress:
        conciliador_command.extend(["--wordpress", str(args.wordpress)])
    if args.saida:
        conciliador_command.extend(["--saida", str(args.saida)])
    if args.relatorio:
        conciliador_command.extend(["--relatorio", str(args.relatorio)])
    if args.saida_novos_produtos:
        conciliador_command.extend(["--saida-novos-produtos", str(args.saida_novos_produtos)])

    code = run_script(conciliador_command)
    manifest["steps"].append({"name": "conciliador", "command": conciliador_command, "exit_code": code})  # type: ignore[index]
    if code != 0:
        manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
        manifest["exit_code"] = code
        write_manifest(manifesto_path, manifest)
        return code
    manifest["summary"] = summarize_conciliacao_report(relatorio_workbook)

    if args.skip_images:
        manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
        manifest["exit_code"] = 0
        write_manifest(manifesto_path, manifest)
        return 0

    if not todos_workbook.exists():
        print(f"Erro: arquivo de conciliacao esperado nao encontrado: {todos_workbook}")
        manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
        manifest["exit_code"] = 1
        write_manifest(manifesto_path, manifest)
        return 1

    buscador_command = [
        sys.executable,
        str(BUSCADOR),
        "--source-root",
        str(conciliacao_folder),
        "--workbook",
        str(todos_workbook),
        "--web",
    ]
    if not args.no_download:
        buscador_command.extend(["--download", "--download-root", str(candidate_root)])
    if args.search_sheet:
        buscador_command.extend(["--sheet", args.search_sheet])
    if args.include_existing_products:
        buscador_command.append("--include-existing-products")

    code = run_script(buscador_command)
    manifest["steps"].append({"name": "buscador", "command": buscador_command, "exit_code": code})  # type: ignore[index]
    if code != 0:
        manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
        manifest["exit_code"] = code
        write_manifest(manifesto_path, manifest)
        return code

    otimizador_command = [
        sys.executable,
        str(OTIMIZADOR),
        "--downloads-dir",
        str(candidate_root),
        "--workbook",
        str(todos_workbook),
    ]
    if args.white_background:
        otimizador_command.append("--white-background")
    if args.overwrite:
        otimizador_command.append("--overwrite")

    code = run_script(otimizador_command)
    manifest["steps"].append({"name": "otimizador", "command": otimizador_command, "exit_code": code})  # type: ignore[index]
    if code != 0:
        manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
        manifest["exit_code"] = code
        write_manifest(manifesto_path, manifest)
        return code

    manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
    manifest["exit_code"] = 0
    write_manifest(manifesto_path, manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
