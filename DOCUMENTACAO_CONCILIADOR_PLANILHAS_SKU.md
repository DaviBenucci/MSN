# Documentacao do conciliador de planilhas e SKUs

## Objetivo

O script `conciliador_planilhas_sku.py` atualiza uma copia da planilha usada para importacao no WordPress/WooCommerce usando a planilha do cliente como fonte principal de informacao.

Regra central: **a planilha do cliente tem precedencia para estoque e preco**.

O script faz quatro coisas:

1. Le a planilha do cliente.
2. Localiza produtos existentes na planilha WordPress pelo nome do produto.
3. Atualiza estoque e preco dos produtos existentes.
4. Adiciona produtos novos ao final da planilha WordPress com novo ID e novo SKU.

A planilha WordPress original nao e sobrescrita por padrao. O script gera uma copia atualizada.

## Arquivos de entrada

### Planilha do cliente

Aceita:

- `.xlsx`
- `.xls`
- `.csv`

Colunas importantes na planilha do cliente:

- Nome/produto: obrigatoria.
- Estoque: opcional, mas recomendada.
- Preco: opcional, mas recomendada.
- SKU/codigo: opcional; normalmente o cliente nao usa SKU.

O script tenta encontrar automaticamente nomes comuns de coluna.

Para nome/produto:

- `Nome`
- `Produto`
- `Descricao`
- `Descricao Produto`
- `Mercadoria`
- `Item`

Para estoque:

- `Estoque`
- `Stock`
- `Quantidade`
- `Qtd`
- `Saldo`

Para preco:

- `Preco`
- `Preço`
- `Valor`
- `Valor Unitario`
- `Preco de Venda`

Se a coluna tiver outro nome, informe no comando:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --nome-coluna "Descricao do Produto" \
  --estoque-coluna "Saldo Atual" \
  --preco-coluna "Valor Venda"
```

### Planilha WordPress

Por padrao, o script usa:

```text
C:\Users\Sama Contabilidade\Desktop\cópia de produtos\Produtos\Controle_de_estoque_Com_Filtro.xlsx
```

Colunas esperadas na planilha WordPress:

- `ID`
- `SKU`
- `Nome`
- `Estoque`
- `Preço`

Se a planilha tiver nomes diferentes:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --wordpress-id-coluna "ID Produto" \
  --wordpress-sku-coluna "Codigo" \
  --wordpress-nome-coluna "Produto" \
  --wordpress-estoque-coluna "Qtd" \
  --wordpress-preco-coluna "Valor"
```

## Como a conciliacao funciona

O produto do cliente e comparado com a planilha WordPress pelo nome normalizado.

Exemplo:

```text
Toner HP CE253AZ Magenta
```

Se o mesmo nome ja existe na planilha WordPress:

- O `ID` existente e mantido.
- O `SKU` existente e mantido.
- O `Nome` existente e mantido.
- O `Estoque` e atualizado com o valor do cliente.
- O `Preço` e atualizado com o valor do cliente.

Se o nome nao existe na planilha WordPress:

- O produto e adicionado ao final da planilha WordPress.
- O novo `ID` sera o maior ID existente + 1.
- O novo `SKU` sera gerado pelo script.
- `Nome`, `Estoque` e `Preço` virao da planilha do cliente.
- Outras colunas da planilha WordPress ficam vazias, salvo preenchimento posterior.

Se o SKU gerado para um produto novo ja existir, o script cria uma variacao unica:

```text
TON-HP-CE253AZ-MAG
TON-HP-CE253AZ-MAG-2
TON-HP-CE253AZ-MAG-3
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

## Arquivos gerados

Em modo normal, o script gera dois arquivos:

1. Planilha WordPress atualizada:

```text
Controle_de_estoque_Com_Filtro_atualizada.xlsx
```

2. Relatorio de conciliacao:

```text
Controle_de_estoque_Com_Filtro_atualizada_relatorio.xlsx
```

O relatorio tem abas:

- `conciliacao`: todas as linhas da planilha do cliente analisadas.
- `novos`: produtos adicionados ao WordPress.
- `adicionados`: mesmo recorte dos produtos adicionados.
- `atualizados`: produtos ja existentes que tiveram estoque/preco atualizados.

## Status de conciliacao

Principais status:

- `atualizado_por_nome`: produto ja existia na planilha WordPress e foi atualizado pelo nome.
- `adicionado_ao_wordpress`: produto nao existia e foi anexado ao final da planilha WordPress.
- `ignorado_sem_nome`: linha sem nome/produto na planilha do cliente.
- `sem_wordpress`: usado quando o comando roda com `--sem-wordpress`.

Colunas adicionadas ao relatorio:

- `SKU_Gerado`
- `Status_Conciliacao`
- `ID_WordPress`
- `SKU_Encontrado_WordPress`
- `Nome_WordPress`
- `Observacao_Conciliacao`

## Comando principal

Git Bash:

```bash
cd "/c/Users/Sama Contabilidade/Desktop/MSN"

./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx"
```

PowerShell:

```powershell
cd "$env:USERPROFILE\Desktop\MSN"

.\.venv\Scripts\python.exe -B conciliador_planilhas_sku.py `
  "C:\caminho\cliente.xlsx"
```

## Informar outra planilha WordPress

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --wordpress "/c/caminho/Controle_de_estoque_Com_Filtro.xlsx"
```

## Escolher saida e relatorio

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --saida "/c/caminho/wordpress_atualizada.xlsx" \
  --relatorio "/c/caminho/relatorio_conciliacao.xlsx"
```

## Definir ID inicial manualmente

Use `--proximo-id` quando quiser forcar o ID inicial dos novos produtos.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --proximo-id 2000
```

## Modo somente gerar SKU

Use `--sem-wordpress` quando quiser apenas gerar o relatorio com `SKU_Gerado`, sem atualizar a planilha WordPress.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --sem-wordpress
```

## Quando revisar manualmente

Revise manualmente quando:

- `SKU_Gerado` terminar com `MOD`, pois o modelo nao foi identificado.
- `Observacao_Conciliacao` indicar SKU duplicado.
- O produto tiver variacao de caixa, cor ou rendimento que nao esteja clara no nome.
- A planilha do cliente vier com nomes muito diferentes dos nomes da planilha WordPress.
- O cliente tiver dois produtos diferentes com nomes iguais.

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
