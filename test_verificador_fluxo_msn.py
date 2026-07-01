from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import pandas as pd

import verificador_fluxo_msn as verifier


def write_flow_files(root: Path, *, include_id_in_new: bool = False) -> None:
    report = pd.DataFrame(
        [
            {
                "SKU_Encontrado_WordPress": "TON-HP-AAA111A-PRT",
                "Status_Conciliacao": "adicionado_ao_wordpress",
            }
        ]
    )
    validation = pd.DataFrame(columns=["severity", "row_number", "field", "code", "message"])
    with pd.ExcelWriter(root / "relatorio-conciliacao.xlsx", engine="openpyxl") as writer:
        report.to_excel(writer, index=False, sheet_name="conciliacao")
        validation.to_excel(writer, index=False, sheet_name="validacao")

    new_row = {"SKU": "TON-HP-AAA111A-PRT", "Nome": "Toner HP"}
    if include_id_in_new:
        new_row["ID"] = 123
    pd.DataFrame([new_row]).to_excel(root / "produtos-novos.xlsx", index=False, sheet_name="novos")
    pd.DataFrame([{"ID": "", "SKU": "TON-HP-AAA111A-PRT", "Nome": "Toner HP"}]).to_excel(
        root / "todos-os-produtos.xlsx",
        index=False,
        sheet_name="Controle de Estoque",
    )
    pd.DataFrame([{"SKU": "TON-HP-AAA111A-PRT", "Nome": "Toner HP"}]).to_excel(
        root / "produtos-novos-amostra-5.xlsx",
        index=False,
        sheet_name="novos",
    )


class VerificadorFluxoMsnTest(unittest.TestCase):
    def test_verify_flow_accepts_valid_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_flow_files(root)
            args = Namespace(
                conciliacao_folder=root,
                todos=None,
                novos=None,
                relatorio=None,
                sample=None,
                summary_json=None,
                log_dir=None,
            )

            result = verifier.verify_flow(args)

            self.assertFalse(result.has_errors)
            self.assertEqual(result.summary["novos_rows"], 1)
            self.assertEqual(result.summary["sample_rows"], 1)

    def test_verify_flow_rejects_id_in_new_products(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_flow_files(root, include_id_in_new=True)
            args = Namespace(
                conciliacao_folder=root,
                todos=None,
                novos=None,
                relatorio=None,
                sample=None,
                summary_json=None,
                log_dir=None,
            )

            result = verifier.verify_flow(args)

            self.assertTrue(result.has_errors)
            self.assertIn("id_em_produtos_novos", [issue.code for issue in result.issues])


if __name__ == "__main__":
    unittest.main()
