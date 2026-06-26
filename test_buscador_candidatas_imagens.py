from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

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

    def test_existing_source_product_folder_is_skipped(self) -> None:
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

            existing_source_dir = source_root / "TON-HP-AAA111A-PRT"
            existing_source_dir.mkdir()
            (existing_source_dir / "manual.jpg").write_bytes(b"fake")

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

    def test_empty_source_product_folder_is_not_skipped(self) -> None:
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

            (source_root / "TON-HP-AAA111A-PRT").mkdir()

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

            self.assertEqual([product.sku for product in products], ["TON-HP-AAA111A-PRT", "TON-HP-BBB222A-CIA"])
            self.assertEqual(args._skipped_existing_products, [])

    def test_review_subfolder_images_do_not_skip_product(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "Produtos"
            source_root.mkdir()
            workbook_path = source_root / buscador.DEFAULT_WORKBOOK_NAME
            write_workbook(workbook_path, [("TON-HP-AAA111A-PRT", "Toner HP AAA111A Preto", "")])

            review_dir = source_root / "TON-HP-AAA111A-PRT" / "_review"
            review_dir.mkdir(parents=True)
            (review_dir / "candidata-rejeitada.jpg").write_bytes(b"fake")

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

            self.assertEqual([product.sku for product in products], ["TON-HP-AAA111A-PRT"])
            self.assertEqual(args._skipped_existing_products, [])

    def test_download_folder_is_created_even_without_downloaded_images(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            download_root = Path(temp_dir) / "Produtos"
            product = buscador.Product(
                row_number=2,
                sku="TON-HP-AAA111A-PRT",
                name="Toner HP AAA111A Preto",
                brand="HP",
                code="AAA111A",
                codes=["AAA111A"],
                kind="toner",
                color="preto",
                package=None,
            )
            args = Namespace(download_root=download_root)

            target = buscador.ensure_product_download_folder(product, args)

            self.assertTrue(target.exists())
            self.assertTrue(target.is_dir())
            self.assertEqual(target, download_root.resolve() / "TON-HP-AAA111A-PRT")

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
                download_root=None,
            )

            buscador.normalize_runtime_paths(args)

            self.assertEqual(args.source_root, source_root.resolve())
            self.assertEqual(args.workbook, workbook_path.resolve())
            self.assertEqual(args.local_root, source_root.resolve())
            self.assertEqual(args.download_root, source_root.resolve())

    def test_download_per_product_limits_saved_candidates(self) -> None:
        product = buscador.Product(
            row_number=2,
            sku="TON-HP-W2011A-CIA",
            name="Toner HP W2011A Ciano",
            brand="HP",
            code="W2011A",
            codes=["W2011A"],
            kind="toner",
            color="ciano",
            package=None,
        )
        fake_results = [
            {
                "title": f"HP W2011A Cyan toner candidate {index}",
                "image": f"https://example.com/w2011a-{index}.jpg",
                "url": f"https://example.com/p/{index}",
            }
            for index in range(5)
        ]
        args = Namespace(
            max_queries=1,
            max_results=5,
            delay=0,
            download=True,
            download_per_product=2,
        )
        downloaded: list[str] = []

        def fake_download(candidate: buscador.Candidate, _product: buscador.Product, _args: Namespace) -> None:
            candidate.local_path = f"C:/tmp/{candidate.rank}.jpg"
            downloaded.append(candidate.image_url)

        with patch.object(buscador, "duckduckgo_image_search", return_value=fake_results), patch.object(
            buscador,
            "download_candidate",
            side_effect=fake_download,
        ), patch.object(buscador, "analyze_image_candidate"), patch.object(buscador, "maybe_ocr_candidate"):
            candidates = buscador.collect_duckduckgo_candidates(product, args)

        self.assertEqual(len(downloaded), 2)
        self.assertEqual(len(candidates), 5)


if __name__ == "__main__":
    unittest.main()
