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

    def test_processar_planilha_updates_wordpress_from_client_by_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"
            relatorio = root / "relatorio.xlsx"

            pd.DataFrame(
                [
                    {"Descricao": "Toner HP CE253AZ Magenta", "Estoque": 3, "Preco": 125.5},
                    {"Descricao": "Toner Lexmark 64018HB", "Estoque": 7, "Preco": 210},
                ]
            ).to_excel(cliente, index=False)
            pd.DataFrame(
                [
                    {
                        "ID": 10,
                        "SKU": "SKU-ANTIGO-MANTIDO",
                        "Nome": "Toner HP CE253AZ Magenta",
                        "Estoque": 1,
                        "Preço": 99,
                        "Imagem": "",
                    },
                ]
            ).to_excel(wordpress, index=False, sheet_name="Controle de Estoque")

            args = Namespace(
                cliente=cliente,
                wordpress=wordpress,
                sem_wordpress=False,
                saida=saida,
                relatorio=relatorio,
                sheet_cliente=None,
                sheet_wordpress="Controle de Estoque",
                nome_coluna=None,
                sku_coluna=None,
                estoque_coluna=None,
                preco_coluna=None,
                wordpress_id_coluna=None,
                wordpress_nome_coluna=None,
                wordpress_sku_coluna=None,
                wordpress_estoque_coluna=None,
                wordpress_preco_coluna=None,
                proximo_id=None,
            )

            result = conciliador.processar_planilha(args)
            wordpress_output = pd.read_excel(result.saida, sheet_name="Controle de Estoque")
            report = pd.read_excel(result.relatorio, sheet_name="conciliacao")

            self.assertEqual(wordpress_output.loc[0, "SKU"], "SKU-ANTIGO-MANTIDO")
            self.assertEqual(wordpress_output.loc[0, "Estoque"], 3)
            self.assertEqual(wordpress_output.loc[0, "Preço"], 125.5)
            self.assertEqual(wordpress_output.loc[1, "ID"], 11)
            self.assertEqual(wordpress_output.loc[1, "SKU"], "TON-LEX-64018HB")
            self.assertEqual(wordpress_output.loc[1, "Nome"], "Toner Lexmark 64018HB")
            self.assertEqual(wordpress_output.loc[1, "Estoque"], 7)
            self.assertEqual(wordpress_output.loc[1, "Preço"], 210)

            self.assertEqual(report.loc[0, "SKU_Gerado"], "TON-HP-CE253AZ-MAG")
            self.assertEqual(report.loc[0, "Status_Conciliacao"], "atualizado_por_nome")
            self.assertEqual(report.loc[0, "SKU_Encontrado_WordPress"], "SKU-ANTIGO-MANTIDO")
            self.assertEqual(report.loc[1, "SKU_Gerado"], "TON-LEX-64018HB")
            self.assertEqual(report.loc[1, "Status_Conciliacao"], "adicionado_ao_wordpress")

            novos = pd.read_excel(result.relatorio, sheet_name="novos")
            self.assertEqual(novos["SKU_Gerado"].tolist(), ["TON-LEX-64018HB"])

    def test_new_products_receive_unique_sku_when_generated_sku_already_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"

            pd.DataFrame([{"Nome": "Toner HP CE253AZ Magenta", "Estoque": 2, "Preco": 180}]).to_excel(
                cliente,
                index=False,
            )
            pd.DataFrame(
                [
                    {"ID": 20, "SKU": "TON-HP-CE253AZ-MAG", "Nome": "Outro Produto", "Estoque": 1, "Preço": 99},
                ]
            ).to_excel(wordpress, index=False, sheet_name="Controle de Estoque")

            args = Namespace(
                cliente=cliente,
                wordpress=wordpress,
                sem_wordpress=False,
                saida=saida,
                relatorio=None,
                sheet_cliente=None,
                sheet_wordpress="Controle de Estoque",
                nome_coluna=None,
                sku_coluna=None,
                estoque_coluna=None,
                preco_coluna=None,
                wordpress_id_coluna=None,
                wordpress_nome_coluna=None,
                wordpress_sku_coluna=None,
                wordpress_estoque_coluna=None,
                wordpress_preco_coluna=None,
                proximo_id=None,
            )

            result = conciliador.processar_planilha(args)
            wordpress_output = pd.read_excel(result.saida, sheet_name="Controle de Estoque")

            self.assertEqual(wordpress_output.loc[1, "ID"], 21)
            self.assertEqual(wordpress_output.loc[1, "SKU"], "TON-HP-CE253AZ-MAG-2")


if __name__ == "__main__":
    unittest.main()
