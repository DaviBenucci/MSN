from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import pandas as pd

import importador_piloto_woocommerce as importer


class FakeWooHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        self.server.requests_seen.append(("GET", parsed.path, query, None))  # type: ignore[attr-defined]
        if parsed.path != "/wp-json/wc/v3/products":
            self.send_json({"code": "not_found", "message": "not found"}, status=404)
            return
        self.send_json([])

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        self.server.requests_seen.append(("POST", parsed.path, {}, payload))  # type: ignore[attr-defined]
        self.send_json({"id": 987, **payload}, status=201)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def send_json(self, payload: object, status: int = 200) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class ImportadorPilotoCliIntegrationTest(unittest.TestCase):
    def test_cli_apply_creates_product_against_fake_woocommerce(self) -> None:
        server = HTTPServer(("127.0.0.1", 0), FakeWooHandler)
        server.requests_seen = []  # type: ignore[attr-defined]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                workbook = root / "produtos.xlsx"
                env_file = root / "woocommerce.env"
                summary_json = root / "summary.json"
                pd.DataFrame(
                    [{"SKU": "TON-HP-AAA111A-PRT", "Nome": "Toner HP", "Preco": "10,50", "Estoque": "2"}]
                ).to_excel(workbook, index=False, sheet_name="novos")
                env_file.write_text(
                    "\n".join(
                        [
                            f"WOOCOMMERCE_URL=http://127.0.0.1:{server.server_port}",
                            "WOOCOMMERCE_CONSUMER_KEY=ck_real_local",
                            "WOOCOMMERCE_CONSUMER_SECRET=cs_real_local",
                        ]
                    ),
                    encoding="utf-8",
                )

                completed = subprocess.run(
                    [
                        sys.executable,
                        "-B",
                        str(Path(importer.__file__).resolve()),
                        "--workbook",
                        str(workbook),
                        "--env-file",
                        str(env_file),
                        "--apply",
                        "--limit",
                        "1",
                        "--retries",
                        "0",
                        "--timeout",
                        "5",
                        "--summary-json",
                        str(summary_json),
                    ],
                    cwd=Path(importer.__file__).resolve().parent,
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
                summary = json.loads(summary_json.read_text(encoding="utf-8"))
                self.assertEqual(summary["status_counts"], {"created": 1})
                self.assertTrue(summary["has_credentials"])
                self.assertIn("TON-HP-AAA111A-PRT: created id=987", completed.stdout)
                requests_seen = server.requests_seen  # type: ignore[attr-defined]
                self.assertEqual([item[0] for item in requests_seen], ["GET", "GET", "POST"])
                created_payload = requests_seen[-1][3]
                self.assertEqual(created_payload["sku"], "TON-HP-AAA111A-PRT")
                self.assertEqual(created_payload["regular_price"], "10.50")
                self.assertEqual(created_payload["stock_quantity"], 2)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
