# Guia de execucao dos scripts MSN

## Visao geral

Este projeto tem tres scripts principais:

- `conciliador_planilhas_sku.py`: gera SKUs e concilia planilha do cliente com a planilha WordPress.
- `buscador_candidatas_imagens.py`: busca, pontua e baixa candidatas de imagem por SKU.
- `otimizador_imagens.py`: trata imagens locais e salva WebP 800x800 em `MSN/products/[SKU]`.

Use sempre a `.venv` do projeto para evitar diferenca de dependencias entre maquinas.

## Entrar na pasta do projeto

PowerShell:

```powershell
cd "$env:USERPROFILE\Desktop\MSN"
```

Git Bash:

```bash
cd "/c/Users/Sama Contabilidade/Desktop/MSN"
```

## Instalar dependencias

Dependencias de imagens:

PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-imagens.txt
```

Git Bash:

```bash
./.venv/Scripts/python.exe -m pip install -r requirements-imagens.txt
```

Dependencias de planilhas:

PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-planilhas.txt
```

Git Bash:

```bash
./.venv/Scripts/python.exe -m pip install -r requirements-planilhas.txt
```

## 1. Atualizar planilha WordPress com a planilha do cliente

Uso padrao:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  --conciliacao-folder "/c/Users/Sama Contabilidade/Desktop/Conciliacao"
```

Ou, para rodar o fluxo completo em sequencia (conciliacao, buscador e otimizador):

```bash
./.venv/Scripts/python.exe -B run_all_scripts.py \
  --desktop-folder-name "Produtos" \
  --conciliacao-folder "/c/Users/Sama Contabilidade/Desktop/Conciliacao"
```

Esse comando:

1. procura em `Desktop/Conciliacao` os arquivos xlsx com `cliente` e `wordpress` no nome;
2. gera `Desktop/Conciliacao/todos-os-produtos.xlsx`;
3. gera `Desktop/Conciliacao/relatorio-conciliacao.xlsx`;
4. gera `Desktop/Conciliacao/produtos-novos.xlsx`;
5. executa o buscador de imagens usando esse workbook;
6. salva as pastas de imagens no desktop em `Desktop/[NomeDaPasta]/[SKU]`;
7. executa o otimizador usando essas pastas.

Neste fluxo, a planilha do cliente tem precedencia para `Estoque` e `Preço`.

O script compara pelo nome do produto:

- se o nome ja existir na planilha WordPress, atualiza estoque e preco;
- se o nome nao existir, adiciona o produto ao final da planilha WordPress;
- produtos novos ficam com ID vazio e SKU gerado automaticamente.

O script gera tres arquivos:

```text
Controle_de_estoque_Com_Filtro_atualizada.xlsx
Controle_de_estoque_Com_Filtro_atualizada_relatorio.xlsx
produtos-novos.xlsx
```

O arquivo `produtos-novos.xlsx` exporta somente a coluna `SKU`, sem `ID`, para que o WooCommerce crie IDs seguros durante a importacao.

Antes de gravar os arquivos finais, o conciliador valida SKU, ID, estoque e preco. Se encontrar erro critico, ele retorna codigo `2`, grava a aba `validacao` no relatorio e bloqueia a geracao dos arquivos de importacao.

Ele usa automaticamente esta planilha WordPress como base:

```text
C:\Users\Sama Contabilidade\Desktop\cópia de produtos\Produtos\Controle_de_estoque_Com_Filtro.xlsx
```

### Informar outra planilha WordPress

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --wordpress "/c/caminho/Controle_de_estoque_Com_Filtro.xlsx"
```

### Informar nome da coluna do cliente

Use quando a planilha nao tiver coluna `Nome`, `Produto` ou `Descricao`.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --nome-coluna "Descricao do Produto"
```

### Informar colunas de estoque e preco do cliente

Use quando os nomes das colunas nao forem detectados automaticamente.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --nome-coluna "Produto" \
  --estoque-coluna "Saldo Atual" \
  --preco-coluna "Valor Venda"
```

### Informar coluna de SKU do cliente

Use apenas se a planilha do cliente vier com algum codigo proprio. A atualizacao principal continua sendo feita pelo nome.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --sku-coluna "Codigo"
```

### Informar abas especificas

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --sheet-cliente "Estoque" \
  --sheet-wordpress "Controle de Estoque"
```

### Escolher arquivo WordPress atualizado e relatorio

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --saida "/c/caminho/wordpress_atualizada.xlsx" \
  --relatorio "/c/caminho/relatorio_conciliacao.xlsx"
```

### Parametro legado de ID

O `--proximo-id` foi mantido apenas por compatibilidade. No fluxo atual, produtos novos ficam com `ID` vazio para o WooCommerce criar IDs seguros usando o `SKU`.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --proximo-id 2000
```

### Somente gerar SKU sem atualizar WordPress

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --sem-wordpress
```

### Validar sem gravar arquivos finais

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --dry-run
```

## 2. Buscar candidatas de imagens

O buscador sempre tira a lista de SKUs da planilha, nao das pastas.

Padrao esperado:

```text
Desktop/cópia de produtos/Produtos/
  Controle_de_estoque_Com_Filtro.xlsx
  [SKU]/
  [SKU]/
```

### Buscar apenas produtos sem imagem na planilha

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --source-root "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --only-missing \
  --web \
  --download
```

O script pula SKUs que ja tem imagem em:

```text
MSN/products/[SKU]
Desktop/cópia de produtos/Produtos/[SKU]
```

Importante: pasta vazia nao conta como imagem existente. Se a pasta `[SKU]` existir mas estiver vazia, o SKU continua pendente.

### Buscar e tambem baixar rejeitadas para revisao

Use este modo para SKUs dificeis. As rejeitadas vao para `[SKU]/_review`.

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --source-root "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --only-missing \
  --web \
  --download \
  --download-rejected-review \
  --review-per-product 8
```

Imagens em `_review` nao fazem o SKU ser pulado e tambem nao sao otimizadas automaticamente pelo `otimizador_imagens.py`.

### Limitar quantidade para teste

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --source-root "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --only-missing \
  --web \
  --download \
  --limit 5
```

### Simular busca sem consultar nem baixar

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --source-root "/c/Users/Sama Contabilidade/Desktop/copia de produtos/Produtos" \
  --web \
  --dry-run
```

### Processar apenas um SKU

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --source-root "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --sku "TON-HP-W9060X-PRT" \
  --web \
  --download \
  --download-rejected-review
```

### Baixar em outra pasta

Por padrao, os downloads vao para:

```text
[source-root]/[SKU]
```

Para salvar dentro de `MSN/products/[SKU]`:

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --source-root "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --download-root "/c/Users/Sama Contabilidade/Desktop/MSN/products" \
  --only-missing \
  --web \
  --download
```

### Relatorios gerados

```text
MSN/products/_reports/candidatas-imagens.csv
MSN/products/_reports/candidatas-aprovacao.csv
MSN/products/_reports/revisao-candidatas.html
MSN/products/_reports/skus-pulados-imagens.csv
MSN/products/_reports/skus-sem-candidatas-confiaveis.csv
MSN/products/_reports/skus-invalidos.csv
```

Abrir HTML de revisao no Git Bash:

```bash
explorer.exe "products\\_reports\\revisao-candidatas.html"
```

### Aplicar aprovacao manual

Fluxo:

1. Abra `products/_reports/candidatas-aprovacao.csv`.
2. Marque `approved=1` nas imagens escolhidas.
3. Rode:

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --apply-approvals "products/_reports/candidatas-aprovacao.csv"
```

As imagens aprovadas serao copiadas para:

```text
MSN/products/_approved_raw/[SKU]
```

Depois otimize:

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "products/_approved_raw" \
  --white-background
```

## 3. Otimizar imagens para WooCommerce

O otimizador gera WebP 800x800 em:

```text
MSN/products/[SKU]
```

### Testar antes de processar

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --dry-run
```

### Otimizar imagens locais com fundo branco

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --white-background
```

### Otimizar apenas um SKU

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --sku "TON-HP-W9060X-PRT" \
  --white-background
```

### Recriar imagens existentes

Use `--overwrite` quando quiser gerar novamente arquivos que ja existem em `MSN/products/[SKU]`.

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --white-background \
  --overwrite
```

### Otimizar sem remover fundo

Use quando a imagem ja estiver boa e voce so quiser padronizar tamanho/formato.

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --skip-rembg
```

### Salvar WebPs em outra pasta

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "/c/Users/Sama Contabilidade/Desktop/copia de produtos/Produtos" \
  --output-root "/c/Users/Sama Contabilidade/Desktop/MSN/products-teste" \
  --white-background
```

### Processar imagens aprovadas manualmente

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "products/_approved_raw" \
  --white-background
```

## 4. Fluxo recomendado completo

1. Atualizar uma copia da planilha WordPress com a planilha do cliente:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx"
```

2. Revisar o arquivo `Controle_de_estoque_Com_Filtro_atualizada_relatorio.xlsx`.

3. Usar `Controle_de_estoque_Com_Filtro_atualizada.xlsx` como a planilha preparada para importacao no WordPress; produtos novos ficam sem `ID` para serem criados pelo WooCommerce via `SKU`.

4. Buscar imagens pendentes usando a planilha/pasta de produtos:

```bash
./.venv/Scripts/python.exe -B buscador_candidatas_imagens.py \
  --source-root "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --only-missing \
  --web \
  --download \
  --download-rejected-review \
  --review-per-product 8
```

5. Revisar `revisao-candidatas.html`.

6. Colocar imagens aprovadas na raiz da pasta `[SKU]` ou usar `candidatas-aprovacao.csv`.

7. Otimizar:

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "/c/Users/Sama Contabilidade/Desktop/cópia de produtos/Produtos" \
  --white-background
```

8. Conferir `MSN/products/[SKU]`.

## 5. Comandos PowerShell equivalentes

Conciliador:

```powershell
.\.venv\Scripts\python.exe -B conciliador_planilhas_sku.py `
  "C:\caminho\cliente.xlsx"
```

Buscador:

```powershell
.\.venv\Scripts\python.exe -B buscador_candidatas_imagens.py `
  --source-root "$env:USERPROFILE\Desktop\cópia de produtos\Produtos" `
  --only-missing `
  --web `
  --download `
  --download-rejected-review `
  --review-per-product 8
```

Otimizador:

```powershell
.\.venv\Scripts\python.exe -B otimizador_imagens.py `
  --input "$env:USERPROFILE\Desktop\cópia de produtos\Produtos" `
  --white-background
```

## 6. Testes

Rodar todos os testes:

```bash
./.venv/Scripts/python.exe -B -m unittest -v \
  test_conciliador_planilhas_sku.py \
  test_buscador_candidatas_imagens.py \
  test_otimizador_imagens.py \
  test_run_all_scripts.py
```

## 7. Cuidados importantes

- Nao use imagens de `_review` como finais sem revisao humana.
- Pasta vazia de SKU e mantida como pendente.
- O buscador le SKUs pela planilha, nao pelas pastas.
- O otimizador salva o resultado final em `MSN/products/[SKU]`.
- Use `--dry-run` antes de otimizar lotes grandes.
- Use `--overwrite` apenas quando quiser substituir WebPs ja existentes.

### Executar todos os scripts juntos

```bash
python run_all_scripts.py \
  --cliente "C:\Users\Sama Contabilidade\Downloads\Lista materiais.xlsx" \
  --wordpress "C:\Users\Sama Contabilidade\Desktop\cópia de produtos\Produtos\Controle_de_estoque_Com_Filtro.backup-preco-div10-20260626-110723.xlsx" \
  --saida "C:\Users\Sama Contabilidade\Desktop\Produtos" \
  --relatorio "C:\Users\Sama Contabilidade\Desktop\Produtos" \
  --saida-novos-produtos "C:\Users\Sama Contabilidade\Downloads" \
  --manifesto "C:\Users\Sama Contabilidade\Desktop\Produtos\manifesto-execucao.json" \
  --all
```
  
Esse comando roda em sequencia:

1. `conciliador_planilhas_sku.py`
2. `buscador_candidatas_imagens.py`
3. `otimizador_imagens.py`

### Observações

- `--saida`, `--relatorio` e `--saida-novos-produtos` podem ser pastas.
- O `run_all_scripts.py` usa o caminho real gerado por `--saida` para alimentar buscador e otimizador.
- O manifesto JSON registra comandos, artefatos, exit codes e resumo da conciliacao.
- Se você passar uma pasta, o nome do arquivo será derivado automaticamente do nome do arquivo WordPress.
- Se quiser apenas rodar a conciliação, remova `--all`.
