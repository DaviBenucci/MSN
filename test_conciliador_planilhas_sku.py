from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import pandas as pd

import conciliador_planilhas_sku as conciliador


def make_args(root: Path, cliente: Path, wordpress: Path, saida: Path, **overrides: object) -> Namespace:
    values = dict(
        cliente=cliente,
        wordpress=wordpress,
        sem_wordpress=False,
        dry_run=False,
        saida=saida,
        relatorio=root / "relatorio.xlsx",
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
        conciliacao_folder=root,
        saida_novos_produtos=root / "produtos-novos.xlsx",
    )
    values.update(overrides)
    return Namespace(**values)


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
            saida_novos_produtos = root / "produtos-novos.xlsx"

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
                dry_run=False,
                conciliacao_folder=root,
                saida_novos_produtos=saida_novos_produtos,
            )

            result = conciliador.processar_planilha(args)
            wordpress_output = pd.read_excel(result.saida, sheet_name="Controle de Estoque")
            report = pd.read_excel(result.relatorio, sheet_name="conciliacao")

            self.assertEqual(wordpress_output.loc[0, "SKU"], "SKU-ANTIGO-MANTIDO")
            self.assertEqual(wordpress_output.loc[0, "Estoque"], 3)
            self.assertEqual(wordpress_output.loc[0, "Preço"], 125.5)
            self.assertTrue(pd.isna(wordpress_output.loc[1, "ID"]))
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

            novos_importacao = pd.read_excel(result.novos_produtos, sheet_name="novos")
            self.assertNotIn("ID", novos_importacao.columns.tolist())
            self.assertEqual(novos_importacao["SKU"].tolist(), ["TON-LEX-64018HB"])
            self.assertEqual(novos_importacao["Nome"].tolist(), ["Toner Lexmark 64018HB"])

    def test_new_products_receive_unique_sku_when_generated_sku_already_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"
            saida_novos_produtos = root / "produtos-novos.xlsx"

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
                dry_run=False,
                conciliacao_folder=root,
                saida_novos_produtos=saida_novos_produtos,
            )

            result = conciliador.processar_planilha(args)
            wordpress_output = pd.read_excel(result.saida, sheet_name="Controle de Estoque")

            self.assertTrue(pd.isna(wordpress_output.loc[1, "ID"]))
            self.assertEqual(wordpress_output.loc[1, "SKU"], "TON-HP-CE253AZ-MAG-2")

    def test_match_by_client_sku_before_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"

            pd.DataFrame([{"Codigo": "SKU-EXISTENTE", "Nome": "Nome alterado pelo cliente", "Estoque": 9}]).to_excel(
                cliente,
                index=False,
            )
            pd.DataFrame(
                [{"ID": 77, "SKU": "SKU-EXISTENTE", "Nome": "Nome original WordPress", "Estoque": 1}]
            ).to_excel(wordpress, index=False, sheet_name="Controle de Estoque")

            result = conciliador.processar_planilha(make_args(root, cliente, wordpress, saida))
            report = pd.read_excel(result.relatorio, sheet_name="conciliacao")
            wordpress_output = pd.read_excel(result.saida, sheet_name="Controle de Estoque")

            self.assertEqual(report.loc[0, "Status_Conciliacao"], "atualizado_por_sku")
            self.assertEqual(wordpress_output.loc[0, "ID"], 77)
            self.assertEqual(wordpress_output.loc[0, "Estoque"], 9)
            self.assertEqual(len(wordpress_output), 1)

    def test_brazilian_price_and_stock_are_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"

            pd.DataFrame([{"Nome": "Toner HP CE253AZ Magenta", "Estoque": "7,0", "Preco": "R$ 1.234,56"}]).to_excel(
                cliente,
                index=False,
            )
            pd.DataFrame([{"ID": 10, "SKU": "OLD", "Nome": "Toner HP CE253AZ Magenta", "Estoque": 1, "Preço": 99}]).to_excel(
                wordpress,
                index=False,
                sheet_name="Controle de Estoque",
            )

            result = conciliador.processar_planilha(make_args(root, cliente, wordpress, saida))
            wordpress_output = pd.read_excel(result.saida, sheet_name="Controle de Estoque")

            self.assertEqual(wordpress_output.loc[0, "Estoque"], 7)
            self.assertEqual(wordpress_output.loc[0, "Preço"], 1234.56)

    def test_invalid_price_blocks_outputs_with_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"

            pd.DataFrame([{"Nome": "Toner HP CE253AZ Magenta", "Estoque": 2, "Preco": "consultar"}]).to_excel(
                cliente,
                index=False,
            )
            pd.DataFrame([{"ID": 10, "SKU": "OLD", "Nome": "Toner HP CE253AZ Magenta", "Estoque": 1, "Preço": 99}]).to_excel(
                wordpress,
                index=False,
                sheet_name="Controle de Estoque",
            )

            with self.assertRaises(conciliador.ValidationFailure):
                conciliador.processar_planilha(make_args(root, cliente, wordpress, saida))

            self.assertFalse(saida.exists())
            validation = pd.read_excel(root / "relatorio.xlsx", sheet_name="validacao")
            self.assertIn("preco_invalido", validation["code"].tolist())

    def test_dry_run_writes_validation_report_without_final_import_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"
            novos = root / "produtos-novos.xlsx"

            pd.DataFrame([{"Nome": "Toner HP CE253AZ Magenta", "Estoque": 2, "Preco": 100}]).to_excel(
                cliente,
                index=False,
            )
            pd.DataFrame([{"ID": 10, "SKU": "OLD", "Nome": "Toner HP CE253AZ Magenta", "Estoque": 1}]).to_excel(
                wordpress,
                index=False,
                sheet_name="Controle de Estoque",
            )

            result = conciliador.processar_planilha(
                make_args(root, cliente, wordpress, saida, dry_run=True, saida_novos_produtos=novos)
            )

            self.assertFalse(saida.exists())
            self.assertFalse(novos.exists())
            self.assertTrue(result.relatorio.exists())
            validation = pd.read_excel(result.relatorio, sheet_name="validacao")
            self.assertIn("severity", validation.columns.tolist())

    def test_existing_product_without_id_is_warning_when_sku_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"

            pd.DataFrame([{"Nome": "Toner HP CE253AZ Magenta", "Estoque": 2, "Preco": 100}]).to_excel(
                cliente,
                index=False,
            )
            pd.DataFrame(
                [{"ID": "", "SKU": "TON-HP-CE253AZ-MAG", "Nome": "Toner HP CE253AZ Magenta", "Estoque": 1, "Preço": 99}]
            ).to_excel(wordpress, index=False, sheet_name="Controle de Estoque")

            result = conciliador.processar_planilha(make_args(root, cliente, wordpress, saida))
            validation = pd.read_excel(result.relatorio, sheet_name="validacao")

            self.assertTrue(result.saida.exists())
            self.assertIn("id_existente_ausente_com_sku", validation["code"].tolist())
            self.assertNotIn("id_existente_e_sku_ausentes", validation["code"].tolist())

    def test_possible_name_match_goes_to_review_without_creating_product(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cliente = root / "cliente.xlsx"
            wordpress = root / "wordpress.xlsx"
            saida = root / "saida.xlsx"

            pd.DataFrame([{"Nome": "Toner HP CE253AZ Magenta", "Estoque": 2, "Preco": 100}]).to_excel(
                cliente,
                index=False,
            )
            pd.DataFrame([{"ID": 10, "SKU": "OLD", "Nome": "Toner HP CE253A Magenta", "Estoque": 1, "Preço": 99}]).to_excel(
                wordpress,
                index=False,
                sheet_name="Controle de Estoque",
            )

            result = conciliador.processar_planilha(make_args(root, cliente, wordpress, saida))
            report = pd.read_excel(result.relatorio, sheet_name="conciliacao")
            wordpress_output = pd.read_excel(result.saida, sheet_name="Controle de Estoque")

            self.assertEqual(report.loc[0, "Status_Conciliacao"], "revisar_possivel_match")
            self.assertEqual(len(wordpress_output), 1)


if __name__ == "__main__":
    unittest.main()
