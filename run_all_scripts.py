from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

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
    parser.add_argument("--proximo-id", type=int, help="ID inicial para novos produtos.")
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
    args = parser.parse_args()

    conciliacao_folder = args.conciliacao_folder.expanduser().resolve()
    candidate_root = DEFAULT_DESKTOP / args.desktop_folder_name
    candidate_root.mkdir(parents=True, exist_ok=True)

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
    if code != 0:
        return code

    if args.skip_images:
        return 0

    todos_workbook = conciliacao_folder / "todos-os-produtos.xlsx"
    if not todos_workbook.exists():
        print(f"Erro: arquivo de conciliacao esperado nao encontrado: {todos_workbook}")
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
    if code != 0:
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
    if code != 0:
        return code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
