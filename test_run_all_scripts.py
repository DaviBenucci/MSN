from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import run_all_scripts


class RunAllScriptsTest(unittest.TestCase):
    def test_expected_conciliador_output_uses_default_when_saida_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args = Namespace(saida=None, wordpress=None)

            self.assertEqual(run_all_scripts.expected_conciliador_output(args, root), root / "todos-os-produtos.xlsx")

    def test_expected_conciliador_output_respects_saida_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            wordpress = root / "Wordpress.xlsx"
            wordpress.write_bytes(b"fake")
            saida = root / "custom.xlsx"
            args = Namespace(saida=saida, wordpress=wordpress)

            self.assertEqual(run_all_scripts.expected_conciliador_output(args, root), saida.resolve())

    def test_expected_conciliador_output_respects_saida_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = root / "saida"
            output_dir.mkdir()
            wordpress = root / "Wordpress.xlsx"
            wordpress.write_bytes(b"fake")
            args = Namespace(saida=output_dir, wordpress=wordpress)

            self.assertEqual(
                run_all_scripts.expected_conciliador_output(args, root),
                output_dir / "Wordpress_atualizada.xlsx",
            )


if __name__ == "__main__":
    unittest.main()
