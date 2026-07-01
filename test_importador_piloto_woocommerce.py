from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import requests

import importador_piloto_woocommerce as importer


class ImportadorPilotoWooCommerceTest(unittest.TestCase):
    def test_load_import_rows_rejects_id_column(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workbook = Path(temp_dir) / "produtos.xlsx"
            pd.DataFrame([{"ID": "", "SKU": "TON-HP-AAA111A-PRT", "Nome": "Toner HP", "Preco": 10}]).to_excel(
                workbook,
                index=False,
                sheet_name="novos",
            )

            with self.assertRaises(importer.PilotImportValidationError):
                importer.load_import_rows(workbook, "novos", 5)

    def test_load_import_rows_normalizes_price_and_stock(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workbook = Path(temp_dir) / "produtos.xlsx"
            pd.DataFrame(
                [{"SKU": "TON-HP-AAA111A-PRT", "Nome": "Toner HP", "Preco": "R$ 1.234,50", "Estoque": "7,0"}]
            ).to_excel(workbook, index=False, sheet_name="novos")

            rows = importer.load_import_rows(workbook, "novos", 5)

            self.assertEqual(rows[0]["price"], "1234.50")
            self.assertEqual(rows[0]["stock"], 7)

    def test_dry_run_does_not_require_credentials_or_network(self) -> None:
        rows = [{"sku": "TON-HP-AAA111A-PRT", "name": "Toner HP", "price": "10.00", "stock": 2}]
        args = Namespace(apply=False, status="draft")

        results = importer.run_import(rows, None, args)

        self.assertEqual(results[0].sku, "TON-HP-AAA111A-PRT")
        self.assertEqual(results[0].status, "dry_run")

    def test_apply_creates_product_when_sku_does_not_exist(self) -> None:
        rows = [{"sku": "TON-HP-AAA111A-PRT", "name": "Toner HP", "price": "10.00", "stock": 2}]
        config = importer.WooConfig("https://loja.test", "ck_real", "cs_real")
        args = Namespace(apply=True, update_existing=False, status="draft")

        with patch.object(importer, "find_existing_product", return_value=None), patch.object(
            importer,
            "create_product",
            return_value={"id": 123},
        ) as create_product:
            results = importer.run_import(rows, config, args)

        self.assertEqual(results[0].status, "created")
        self.assertEqual(results[0].product_id, 123)
        create_product.assert_called_once()

    def test_apply_skips_existing_product_by_default(self) -> None:
        rows = [{"sku": "TON-HP-AAA111A-PRT", "name": "Toner HP", "price": "10.00", "stock": 2}]
        config = importer.WooConfig("https://loja.test", "ck_real", "cs_real")
        args = Namespace(apply=True, update_existing=False, status="draft")

        with patch.object(importer, "find_existing_product", return_value={"id": 456}), patch.object(
            importer,
            "create_product",
        ) as create_product:
            results = importer.run_import(rows, config, args)

        self.assertEqual(results[0].status, "skipped_existing")
        self.assertEqual(results[0].product_id, 456)
        create_product.assert_not_called()

    def test_apply_updates_existing_product_when_requested(self) -> None:
        rows = [{"sku": "TON-HP-AAA111A-PRT", "name": "Toner HP", "price": "10.00", "stock": 2}]
        config = importer.WooConfig("https://loja.test", "ck_real", "cs_real")
        args = Namespace(apply=True, update_existing=True, status="draft")

        with patch.object(importer, "find_existing_product", return_value={"id": 456}), patch.object(
            importer,
            "update_product",
            return_value={"id": 456},
        ) as update_product:
            results = importer.run_import(rows, config, args)

        self.assertEqual(results[0].status, "updated")
        self.assertEqual(results[0].product_id, 456)
        update_product.assert_called_once()

    def test_product_payload_uses_sku_name_price_and_stock(self) -> None:
        row = {"sku": "TON-HP-AAA111A-PRT", "name": "Toner HP", "price": "10.00", "stock": 2}

        payload = importer.product_payload(row, "draft")

        self.assertEqual(payload["sku"], "TON-HP-AAA111A-PRT")
        self.assertEqual(payload["name"], "Toner HP")
        self.assertEqual(payload["regular_price"], "10.00")
        self.assertEqual(payload["stock_quantity"], 2)
        self.assertTrue(payload["manage_stock"])
        self.assertEqual(payload["status"], "draft")

    def test_resolve_config_reads_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / "woocommerce.env"
            env_file.write_text(
                "\n".join(
                    [
                        "WOOCOMMERCE_URL=https://loja.test",
                        "WOOCOMMERCE_CONSUMER_KEY=ck_file",
                        "WOOCOMMERCE_CONSUMER_SECRET=cs_file",
                    ]
                ),
                encoding="utf-8",
            )
            args = Namespace(site_url=None, consumer_key=None, consumer_secret=None, env_file=env_file)

            config = importer.resolve_config(args)

            self.assertIsNotNone(config)
            assert config is not None
            self.assertEqual(config.site_url, "https://loja.test")
            self.assertEqual(config.consumer_key, "ck_file")
            self.assertEqual(config.consumer_secret, "cs_file")

    def test_explicit_config_overrides_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / "woocommerce.env"
            env_file.write_text(
                "\n".join(
                    [
                        "WOOCOMMERCE_URL=https://loja-file.test",
                        "WOOCOMMERCE_CONSUMER_KEY=ck_file",
                        "WOOCOMMERCE_CONSUMER_SECRET=cs_file",
                    ]
                ),
                encoding="utf-8",
            )
            args = Namespace(
                site_url="https://loja-cli.test",
                consumer_key="ck_cli",
                consumer_secret="cs_cli",
                env_file=env_file,
            )

            config = importer.resolve_config(args)

            self.assertIsNotNone(config)
            assert config is not None
            self.assertEqual(config.site_url, "https://loja-cli.test")
            self.assertEqual(config.consumer_key, "ck_cli")
            self.assertEqual(config.consumer_secret, "cs_cli")

    def test_placeholder_config_is_not_considered_real_credentials(self) -> None:
        config = importer.WooConfig(
            site_url="https://sua-loja.com.br",
            consumer_key="ck_substitua_aqui",
            consumer_secret="cs_substitua_aqui",
        )

        self.assertTrue(importer.is_placeholder_config(config))

    def test_preflight_woocommerce_accepts_product_list_response(self) -> None:
        config = importer.WooConfig("https://loja.test", "ck_real", "cs_real")
        args = Namespace(timeout=30, retries=0, retry_backoff=0, _logger=None)
        response = Mock()
        response.json.return_value = []

        with patch.object(importer, "request_woocommerce", return_value=response) as request:
            importer.preflight_woocommerce(config, args)

        request.assert_called_once()

    def test_preflight_woocommerce_rejects_unexpected_response(self) -> None:
        config = importer.WooConfig("https://loja.test", "ck_real", "cs_real")
        args = Namespace(timeout=30, retries=0, retry_backoff=0, _logger=None)
        response = Mock()
        response.json.return_value = {"unexpected": True}

        with patch.object(importer, "request_woocommerce", return_value=response), self.assertRaises(RuntimeError):
            importer.preflight_woocommerce(config, args)

    def test_format_http_error_includes_woo_message_without_secret(self) -> None:
        response = requests.Response()
        response.status_code = 401
        response._content = b'{"code":"woocommerce_rest_cannot_view","message":"Sorry, you cannot list resources."}'
        error = requests.HTTPError(response=response)

        message = importer.format_http_error("preflight WooCommerce", error)

        self.assertIn("HTTP 401", message)
        self.assertIn("woocommerce_rest_cannot_view", message)
        self.assertIn("verifique URL", message)
        self.assertNotIn("ck_real", message)
        self.assertNotIn("cs_real", message)

    def test_request_woocommerce_wraps_http_errors(self) -> None:
        config = importer.WooConfig("https://loja.test", "ck_real", "cs_real")
        args = Namespace(timeout=30, retries=0, retry_backoff=0, _logger=None)
        response = requests.Response()
        response.status_code = 429
        response.url = config.products_url
        response._content = b'{"code":"too_many_requests","message":"Rate limited"}'

        with patch("importador_piloto_woocommerce.requests.Session.request", return_value=response):
            with self.assertRaises(importer.WooCommerceApiError) as context:
                importer.request_woocommerce("get", config.products_url, config, args, label="preflight WooCommerce")

        self.assertIn("HTTP 429", str(context.exception))
        self.assertIn("backoff", str(context.exception))


if __name__ == "__main__":
    unittest.main()
