from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import run_all_scripts


def make_run_args(**overrides: object) -> Namespace:
    values = dict(
        cliente=None,
        wordpress=None,
        saida=None,
        relatorio=None,
        saida_novos_produtos=None,
        sheet_cliente=None,
        sheet_wordpress=None,
        proximo_id=None,
        search_sheet=None,
        include_existing_products=False,
        overwrite=False,
        white_background=False,
        no_download=False,
        timeout=None,
        download_timeout=None,
        retries=None,
        retry_backoff=None,
        woo_workbook=None,
        woo_limit=5,
        woo_status="draft",
        woo_apply=False,
        woo_preflight_only=False,
        woo_update_existing=False,
        woo_env_file=None,
        woo_site_url=None,
        woo_consumer_key=None,
        woo_consumer_secret=None,
        log_dir=None,
    )
    values.update(overrides)
    return Namespace(**values)


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

    def test_expected_woo_pilot_workbook_prefers_explicit_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            explicit = root / "piloto.xlsx"
            args = Namespace(woo_workbook=explicit)

            self.assertEqual(
                run_all_scripts.expected_woo_pilot_workbook(args, root / "produtos-novos.xlsx", root),
                explicit.resolve(),
            )

    def test_expected_woo_pilot_workbook_uses_sample_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            sample = root / "produtos-novos-amostra-5.xlsx"
            sample.write_bytes(b"fake")
            args = Namespace(woo_workbook=None)

            self.assertEqual(
                run_all_scripts.expected_woo_pilot_workbook(args, root / "produtos-novos.xlsx", root),
                sample,
            )

    def test_expected_verification_output_uses_conciliacao_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            self.assertEqual(
                run_all_scripts.expected_verification_output(root),
                root / "verificacao-fluxo-msn.json",
            )

    def test_manifest_args_redacts_woo_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args = Namespace(
                desktop_folder_name="Produtos",
                woo_consumer_key="ck_secret",
                woo_consumer_secret="cs_secret",
                skip_verify=False,
            )

            payload = run_all_scripts.manifest_args(args, root, root / "manifesto.json", root / "run.log")

            self.assertEqual(payload["woo_consumer_key"], "***")
            self.assertEqual(payload["woo_consumer_secret"], "***")

    def test_manifest_args_keeps_woo_env_file_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            env_file = root / "woocommerce.env"
            args = Namespace(
                desktop_folder_name="Produtos",
                woo_consumer_key=None,
                woo_consumer_secret=None,
                woo_env_file=env_file,
            )

            payload = run_all_scripts.manifest_args(args, root, root / "manifesto.json", root / "run.log")

            self.assertEqual(payload["woo_env_file"], str(env_file))

    def test_build_woo_command_redacts_secret_display_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workbook = Path(temp_dir) / "piloto.xlsx"
            args = make_run_args(
                woo_apply=True,
                woo_consumer_key="ck_secret",
                woo_consumer_secret="cs_secret",
                timeout=5,
            )

            command, display_command = run_all_scripts.build_woo_command(args, workbook)

            self.assertIn("ck_secret", command)
            self.assertIn("cs_secret", command)
            self.assertNotIn("ck_secret", display_command)
            self.assertNotIn("cs_secret", display_command)
            self.assertIn("***", display_command)
            self.assertIn("--apply", command)
            self.assertIn("--timeout", command)

    def test_build_buscador_command_respects_network_options(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args = make_run_args(no_download=True, search_sheet="Controle", timeout=5, retries=2, retry_backoff=1.5)

            command = run_all_scripts.build_buscador_command(args, root, root / "todos.xlsx", root / "downloads")

            self.assertIn("--sheet", command)
            self.assertIn("Controle", command)
            self.assertIn("--timeout", command)
            self.assertIn("5", command)
            self.assertNotIn("--download", command)

    def test_build_otimizador_command_respects_flags(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args = make_run_args(white_background=True, overwrite=True, download_timeout=10)

            command = run_all_scripts.build_otimizador_command(args, root / "downloads", root / "todos.xlsx")

            self.assertIn("--white-background", command)
            self.assertIn("--overwrite", command)
            self.assertIn("--download-timeout", command)
            self.assertIn("10", command)


if __name__ == "__main__":
    unittest.main()
