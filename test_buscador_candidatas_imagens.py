from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from openpyxl import Workbook

import buscador_candidatas_imagens as buscador


def write_workbook(path: Path, rows: list[tuple[str, str, str]]) -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = buscador.DEFAULT_SHEET
    worksheet.append(["ID", "SKU", "Nome", "Estoque", "Preço", "Imagem"])
    for index, (sku, name, image_status) in enumerate(rows, start=1):
        worksheet.append([index, sku, name, 1, 100, image_status])
    workbook.save(path)


class BuscadorCandidatasTest(unittest.TestCase):
    def test_skus_come_from_workbook_not_source_folders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "Produtos"
            source_root.mkdir()
            workbook_path = source_root / buscador.DEFAULT_WORKBOOK_NAME
            write_workbook(
                workbook_path,
                [
                    ("TON-HP-AAA111A-PRT", "Toner HP AAA111A Preto", ""),
                    ("TON-HP-BBB222A-CIA", "Toner HP BBB222A Ciano", ""),
                ],
            )

            (source_root / "SKU-EXTRA-QUE-NAO-ESTA-NA-PLANILHA").mkdir()
            (source_root / "SKU-EXTRA-QUE-NAO-ESTA-NA-PLANILHA" / "imagem.jpg").write_bytes(b"fake")

            args = Namespace(
                source_root=source_root,
                workbook=None,
                sheet=buscador.DEFAULT_SHEET,
                sku=None,
                only_missing=False,
                include_existing_products=True,
                limit=None,
            )

            products = buscador.load_products(args)

            self.assertEqual([product.sku for product in products], ["TON-HP-AAA111A-PRT", "TON-HP-BBB222A-CIA"])

    def test_existing_msn_product_folder_is_skipped(self) -> None:
        original_products_dir = buscador.PRODUCTS_DIR
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                source_root = root / "Produtos"
                source_root.mkdir()
                workbook_path = source_root / buscador.DEFAULT_WORKBOOK_NAME
                write_workbook(
                    workbook_path,
                    [
                        ("TON-HP-AAA111A-PRT", "Toner HP AAA111A Preto", ""),
                        ("TON-HP-BBB222A-CIA", "Toner HP BBB222A Ciano", ""),
                    ],
                )

                buscador.PRODUCTS_DIR = root / "MSN-products"
                existing_dir = buscador.PRODUCTS_DIR / "TON-HP-AAA111A-PRT"
                existing_dir.mkdir(parents=True)
                (existing_dir / "TON-HP-AAA111A-PRT-01.webp").write_bytes(b"fake")

                args = Namespace(
                    source_root=source_root,
                    workbook=None,
                    sheet=buscador.DEFAULT_SHEET,
                    sku=None,
                    only_missing=False,
                    include_existing_products=False,
                    limit=None,
                )

                products = buscador.load_products(args)

                self.assertEqual([product.sku for product in products], ["TON-HP-BBB222A-CIA"])
                self.assertEqual([product.sku for product in args._skipped_existing_products], ["TON-HP-AAA111A-PRT"])
        finally:
            buscador.PRODUCTS_DIR = original_products_dir

    def test_runtime_paths_default_local_root_to_source_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "Produtos"
            source_root.mkdir()
            workbook_path = source_root / buscador.DEFAULT_WORKBOOK_NAME
            write_workbook(workbook_path, [("TON-HP-AAA111A-PRT", "Toner HP AAA111A Preto", "")])

            args = Namespace(
                source_root=source_root,
                workbook=None,
                local_root=None,
                no_local_source=False,
            )

            buscador.normalize_runtime_paths(args)

            self.assertEqual(args.source_root, source_root.resolve())
            self.assertEqual(args.workbook, workbook_path.resolve())
            self.assertEqual(args.local_root, source_root.resolve())


if __name__ == "__main__":
    unittest.main()
