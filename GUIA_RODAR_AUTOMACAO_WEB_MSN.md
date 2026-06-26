# Guia para rodar a Automacao Web MSN em outra maquina

Este guia instala e executa a interface web local criada para conciliar planilhas do WordPress com a planilha do cliente.

## 1. Requisitos

Instale antes:

- Python 3.11 ou superior.
- Node.js 20 ou superior.
- Git, se for baixar o projeto por repositorio.
- Tesseract OCR, somente quando for usar os scripts de imagens/OCR.

No Windows, se o PowerShell bloquear `npm.ps1`, use sempre `npm.cmd` e `npx.cmd`.

## 2. Estrutura esperada

O projeto deve ficar em uma pasta como:

```text
C:\Users\SEU_USUARIO\Desktop\MSN
```

Pastas principais:

```text
MSN/
  backend/
  frontend/
  cache/
  conciliador_planilhas_sku.py
  buscador_candidatas_imagens.py
  otimizador_imagens.py
```

## 3. Instalar dependencias do Python

PowerShell:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt -r requirements-planilhas.txt -r requirements-imagens.txt
```

Git Bash:

```bash
cd "/c/Users/SEU_USUARIO/Desktop/MSN"
python -m venv .venv
./.venv/Scripts/python.exe -m pip install --upgrade pip
./.venv/Scripts/python.exe -m pip install -r backend/requirements.txt -r requirements-planilhas.txt -r requirements-imagens.txt
```

## 4. Instalar dependencias do frontend

PowerShell:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN\frontend"
npm.cmd install
```

Git Bash:

```bash
cd "/c/Users/SEU_USUARIO/Desktop/MSN/frontend"
npm install
```

## 5. Rodar o backend

Abra um terminal separado.

PowerShell:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN\backend"
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Git Bash:

```bash
cd "/c/Users/SEU_USUARIO/Desktop/MSN/backend"
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Teste se o backend respondeu:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/health" -UseBasicParsing
```

Resposta esperada:

```json
{"status":"ok"}
```

## 6. Rodar o frontend

Abra outro terminal separado.

PowerShell:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN\frontend"
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

Git Bash:

```bash
cd "/c/Users/SEU_USUARIO/Desktop/MSN/frontend"
npm run dev -- --host 127.0.0.1 --port 5173
```

Acesse no navegador:

```text
http://127.0.0.1:5173/
```

## 7. Como usar a tela

1. No campo `Planilha WordPress`, selecione a exportacao/base do WordPress.
2. No campo `Planilha do cliente`, selecione a planilha atualizada enviada pelo cliente.
3. Clique em `Processar conciliacao`.
4. Aguarde os logs aparecerem no painel lateral.
5. Ao finalizar, baixe:
   - `Planilha WordPress atualizada`;
   - `Relatorio de conciliacao`.

Formatos aceitos no upload:

- `.xlsx`
- `.csv`

## 8. Rodar testes automatizados

Backend:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN\backend"
..\.venv\Scripts\python.exe -m pytest -v
```

Resultado esperado no estado atual:

```text
14 passed
```

Frontend:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN\frontend"
npm.cmd run build
npm.cmd run lint
```

Resultado esperado:

- build concluido com sucesso;
- lint sem erros.

## 9. Smoke test manual da API

Depois de subir o backend, abra:

```text
http://127.0.0.1:8000/docs
```

Use a rota:

```text
POST /api/v1/conciliar
```

Envie dois arquivos:

- `cliente`
- `wordpress`

Se funcionar, a API retornara um JSON com:

- `job_id`;
- `outputs.wordpress_atualizado.download_url`;
- `outputs.relatorio.download_url`;
- `logs.stdout`.

## 10. Cache e arquivos gerados

Os uploads e resultados ficam temporariamente em:

```text
MSN/cache/conciliacoes/[job_id]
```

Cada job tem:

```text
uploads/
outputs/
```

No momento, a limpeza automatica apos download ainda nao foi implementada. Se precisar limpar manualmente:

```powershell
Remove-Item -LiteralPath "C:\Users\SEU_USUARIO\Desktop\MSN\cache\conciliacoes\*" -Recurse -Force
```

Use esse comando somente dentro da pasta `cache\conciliacoes`.

## 11. Problemas comuns

### `npm.ps1 nao pode ser carregado`

Use:

```powershell
npm.cmd install
npm.cmd run dev
```

### Porta 8000 ocupada

Rode o backend em outra porta:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Depois ajuste o frontend:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN\frontend"
$env:VITE_API_BASE_URL="http://127.0.0.1:8001"
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

### Porta 5173 ocupada

Rode o frontend em outra porta:

```powershell
npm.cmd run dev -- --host 127.0.0.1 --port 5174
```

Se mudar a porta do frontend, ajuste o CORS do backend em `backend/app/main.py`.

### Erro `No module named pandas`

Instale novamente as dependencias:

```powershell
cd "C:\Users\SEU_USUARIO\Desktop\MSN"
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt -r requirements-planilhas.txt
```

### Erro com aba da planilha WordPress

O backend chama o script usando a aba padrao:

```text
Controle de Estoque
```

Se a planilha WordPress tiver outro nome de aba, sera necessario adaptar a rota para aceitar esse parametro ou renomear a aba antes do upload.

### Erro de CORS

O backend aceita por padrao:

```text
http://localhost:5173
http://127.0.0.1:5173
```

Se o frontend rodar em outra porta, atualize `ALLOWED_ORIGINS` em `backend/app/main.py`.

## 12. Proxima melhoria recomendada

Depois de confirmar a conciliacao pela tela, a proxima etapa natural e conectar:

1. busca de imagens com base na planilha conciliada;
2. tratamento/otimizacao das imagens;
3. download final em `.zip`;
4. limpeza automatica do cache apos o download final.
