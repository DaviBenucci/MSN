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

## 1. Conciliar planilha do cliente com WordPress

Uso padrao:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/planilha-do-cliente.xlsx"
```

O script gera:

```text
planilha-do-cliente_conciliada.xlsx
```

Ele compara automaticamente com:

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

### Informar coluna de SKU do cliente

Use quando a planilha do cliente ja vier com codigo/SKU proprio.

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --nome-coluna "Produto" \
  --sku-coluna "Codigo"
```

### Informar abas especificas

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --sheet-cliente "Estoque" \
  --sheet-wordpress "Controle de Estoque"
```

### Somente gerar SKU sem conciliar

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --sem-wordpress
```

### Escolher arquivo de saida

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx" \
  --saida "/c/caminho/cliente_conciliado_final.xlsx"
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
  --white-background \
  --skip-rembg
```

### Processar imagens aprovadas manualmente

```bash
./.venv/Scripts/python.exe -B otimizador_imagens.py \
  --input "products/_approved_raw" \
  --white-background
```

## 4. Fluxo recomendado completo

1. Conciliar planilha do cliente:

```bash
./.venv/Scripts/python.exe -B conciliador_planilhas_sku.py \
  "/c/caminho/cliente.xlsx"
```

2. Revisar a aba `novos` da planilha conciliada.

3. Atualizar/importar a planilha WordPress quando necessario.

4. Buscar imagens pendentes:

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
  test_otimizador_imagens.py
```

## 7. Cuidados importantes

- Nao use imagens de `_review` como finais sem revisao humana.
- Pasta vazia de SKU e mantida como pendente.
- O buscador le SKUs pela planilha, nao pelas pastas.
- O otimizador salva o resultado final em `MSN/products/[SKU]`.
- Use `--dry-run` antes de otimizar lotes grandes.
- Use `--overwrite` apenas quando quiser substituir WebPs ja existentes.
