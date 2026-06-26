# Documentacao do conciliador de planilhas e SKUs

## Objetivo

O script `conciliador_planilhas_sku.py` serve para receber uma planilha de estoque/produtos enviada por cliente, gerar um SKU padronizado a partir do nome do produto e comparar essa planilha com a planilha usada para importacao no WordPress/WooCommerce.

Ele foi criado para responder rapidamente tres perguntas:

1. Quais produtos do cliente ja existem na planilha WordPress?
2. Quais produtos parecem ser novos e precisam ser importados?
3. Qual SKU padronizado pode ser usado para organizar imagens, pastas e importacao?

## Arquivo de entrada

O script aceita:

- `.xlsx`
- `.xls`
- `.csv`

A planilha do cliente precisa ter uma coluna com nome/produto. O script tenta encontrar automaticamente colunas comuns, como:

- `Nome`
- `Produto`
- `Descricao`
- `Descricao Produto`
- `Mercadoria`
- `Item`

Se a coluna tiver outro nome, informe no comando com `--nome-coluna`.

Exemplo:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --nome-coluna "Descricao do item"
```

## Planilha WordPress

Por padrao, o script compara a planilha do cliente com:

```text
C:\Users\Sama Contabilidade\Desktop\cópia de produtos\Produtos\Controle_de_estoque_Com_Filtro.xlsx
```

Essa planilha deve ter uma coluna de SKU e uma coluna de nome/produto. Se as colunas tiverem nomes diferentes, use:

```bash
--wordpress-sku-coluna "Codigo"
--wordpress-nome-coluna "Produto"
```

Tambem e possivel informar outro arquivo WordPress:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --wordpress "/c/caminho/Controle_de_estoque_Com_Filtro.xlsx"
```

## Geracao de SKU

O SKU gerado segue esta estrutura:

```text
CATEGORIA-MARCA-MODELO-VARIACOES
```

Exemplos:

```text
Toner HP CE253AZ Magenta
=> TON-HP-CE253AZ-MAG

Impressora Multifuncional Samsung C3060FR
=> IMP-SAM-C3060FR

Toner Lexmark 64018HB
=> TON-LEX-64018HB
```

Categorias reconhecidas:

- `TON`: toner
- `CRT`: cartucho
- `DRU`: drum, tambor, cilindro ou unidade de imagem
- `FUS`: fusor
- `IMP`: impressora ou multifuncional
- `PAP`: papel ou sulfite
- `DEV`: developer ou revelador
- `RES`: residuo ou waste toner
- `KIT`: kit de manutencao
- `OUT`: outros produtos

Marcas reconhecidas:

- `HP`
- `SAM`: Samsung
- `BRO`: Brother
- `CAN`: Canon
- `EPS`: Epson
- `LEX`: Lexmark
- `XER`: Xerox
- `RIC`: Ricoh
- `MIN`: Minolta/Konica Minolta
- `KYO`: Kyocera
- `OKI`
- `APC`
- `ZEB`: Zebra
- `ELG`: Elgin
- `GEN`: generico ou marca nao identificada

Variacoes reconhecidas:

- `MAG`: magenta
- `PRT`: preto/black
- `AMR`: amarelo/yellow
- `CIA`: ciano/cyan
- `AZ`: caixa azul e branca
- `NV`: caixa nova preta
- `BR`: caixa branca

## Conciliacao

O script compara a planilha do cliente com a planilha WordPress nesta ordem:

1. SKU original do cliente, se existir.
2. SKU gerado pelo script.
3. Nome do produto normalizado.

O resultado vai para a coluna `Status_Conciliacao`.

Status possiveis:

- `novo_para_wordpress`: nao foi encontrado na planilha WordPress.
- `existe_por_sku_cliente`: o SKU que veio do cliente ja existe na planilha WordPress.
- `existe_por_sku_gerado`: o SKU gerado pelo script ja existe na planilha WordPress.
- `possivel_existente_por_nome`: o nome bate com um produto da planilha WordPress, mesmo sem SKU igual.
- `sem_wordpress`: o script foi executado com `--sem-wordpress`.

Outras colunas adicionadas:

- `SKU_Gerado`: SKU padronizado criado pelo script.
- `SKU_Encontrado_WordPress`: SKU correspondente encontrado na base WordPress.
- `Nome_WordPress`: nome correspondente encontrado na base WordPress.
- `Observacao_Conciliacao`: avisos, como SKU duplicado ou nome divergente.

## Arquivo de saida

Por padrao, a saida e criada ao lado da planilha do cliente:

```text
cliente_conciliada.xlsx
```

O arquivo `.xlsx` gerado tem tres abas:

- `conciliacao`: todos os itens analisados.
- `novos`: somente itens com `novo_para_wordpress`.
- `existentes`: itens encontrados ou possivelmente encontrados na base WordPress.

Para escolher outro destino:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --saida "/c/caminho/cliente_conciliado_final.xlsx"
```

## Modo somente gerar SKU

Use `--sem-wordpress` quando voce quiser apenas gerar os SKUs, sem comparar com a planilha WordPress.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --sem-wordpress
```

## Quando revisar manualmente

Revise manualmente quando:

- `SKU_Gerado` terminar com `MOD`, pois o modelo nao foi identificado.
- `Observacao_Conciliacao` indicar SKU duplicado.
- O status for `possivel_existente_por_nome`.
- O nome do cliente estiver muito diferente do nome WordPress.
- O produto tiver variacao de caixa, cor ou rendimento que nao esteja clara no nome.

## Dependencias

As dependencias ficam em:

```text
requirements-planilhas.txt
```

Para instalar:

```bash
./.venv/Scripts/python.exe -m pip install -r requirements-planilhas.txt
```

Principais bibliotecas:

- `pandas`: leitura, tratamento e escrita das planilhas.
- `openpyxl`: leitura/escrita de `.xlsx`.
- `xlrd`: leitura de `.xls`.
