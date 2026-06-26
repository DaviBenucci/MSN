from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import pandas as pd

import conciliador_planilhas_sku as conciliador


class ConciliadorPlanilhasSkuTest(unittest.TestCase):
    def test_gerar_sku_from_common_product_names(self) -> None:
        self.assertEqual(conciliador.gerar_sku("Toner HP CE253AZ Magenta"), "TON-HP-CE253AZ-MAG")
        self.assertEqual(
            conciliador.gerar_sku("Impressora Multifuncional Samsung C3060FR"),
            "IMP-SAM-C3060FR",
        )
        self.assertEqual(conciliador.gerar_sku("Toner Lexmark 64018HB"), "TON-LEX-64018HB")

    def test_processar_planilha_conciliates_with_wordpress_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"

            pd.DataFrame(
                [
                    {"Descricao": "Toner HP CE253AZ Magenta", "Estoque": 3},
                    {"Descricao": "Toner Lexmark 64018HB", "Estoque": 7},
                ]
            ).to_excel(cliente, index=False)
            pd.DataFrame(
                [
                    {"SKU": "TON-HP-CE253AZ-MAG", "Nome": "Toner HP CE253AZ Magenta"},
                ]
            ).to_excel(wordpress, index=False, sheet_name="Controle de Estoque")

            args = Namespace(
                cliente=cliente,
                wordpress=wordpress,
                sem_wordpress=False,
                saida=saida,
                sheet_cliente=None,
                sheet_wordpress="Controle de Estoque",
                nome_coluna=None,
                sku_coluna=None,
                wordpress_nome_coluna=None,
                wordpress_sku_coluna=None,
            )

            result = conciliador.processar_planilha(args)
            output = pd.read_excel(result, sheet_name="conciliacao")

            self.assertEqual(output.loc[0, "SKU_Gerado"], "TON-HP-CE253AZ-MAG")
            self.assertEqual(output.loc[0, "Status_Conciliacao"], "existe_por_sku_gerado")
            self.assertEqual(output.loc[1, "SKU_Gerado"], "TON-LEX-64018HB")
            self.assertEqual(output.loc[1, "Status_Conciliacao"], "novo_para_wordpress")

            novos = pd.read_excel(result, sheet_name="novos")
            self.assertEqual(novos["SKU_Gerado"].tolist(), ["TON-LEX-64018HB"])


if __name__ == "__main__":
    unittest.main()
