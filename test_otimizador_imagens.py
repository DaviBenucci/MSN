from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import otimizador_imagens as otimizador


class OtimizadorLocalInputTest(unittest.TestCase):
    def test_input_root_with_sku_subfolders_creates_one_product_per_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "Produtos"
            first = root / "TON-HP-AAA111A-PRT"
            second = root / "TON-HP-BBB222A-CIA"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            (first / "imagem.jpg").write_bytes(b"fake")
            (second / "imagem.png").write_bytes(b"fake")

            products = otimizador.products_from_local_input(root, None)

            self.assertEqual([product.sku for product in products], ["TON-HP-AAA111A-PRT", "TON-HP-BBB222A-CIA"])
            self.assertEqual([product.source_dir for product in products], [first.resolve(), second.resolve()])

    def test_input_folder_with_direct_images_is_single_product(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "TON-HP-AAA111A-PRT"
            root.mkdir()
            (root / "imagem.jpg").write_bytes(b"fake")

            products = otimizador.products_from_local_input(root, None)

            self.assertEqual([product.sku for product in products], ["TON-HP-AAA111A-PRT"])
            self.assertEqual(products[0].source_dir, root.resolve())

    def test_input_file_is_single_product_from_file_stem(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            image = Path(temp_dir) / "TON-HP-AAA111A-PRT.jpg"
            image.write_bytes(b"fake")

            products = otimizador.products_from_local_input(image, None)

            self.assertEqual([product.sku for product in products], ["TON-HP-AAA111A-PRT"])
            self.assertEqual(products[0].source_dir, image.resolve())

    def test_collect_image_files_ignores_review_subfolder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "TON-HP-AAA111A-PRT"
            review = root / "_review"
            review.mkdir(parents=True)
            expected = root / "imagem-aprovada.jpg"
            expected.write_bytes(b"fake")
            (review / "candidata-rejeitada.jpg").write_bytes(b"fake")

            images = otimizador.collect_image_files(root)

            self.assertEqual(images, [expected])


if __name__ == "__main__":
    unittest.main()
