# Contexto Codex - Projeto MSN

## Estado atual
- Data da atualizacao: 26/06/2026
- Fase atual: Etapa 5 concluida
- Proxima etapa: a definir fora do documento `Implementação-automatizacao.md`
- Regra de avanço: o documento atual foi concluido ate a Etapa 5.

## Observacao de alinhamento
- O contexto inicial indicava Etapa 3 em progresso, mas o workspace nao tinha a estrutura `backend/`.
- A implementacao foi realinhada com o estado do filesystem e com o documento `Implementação-automatizacao.md`, iniciando pela Etapa 1.
- No PowerShell desta maquina, `npm.ps1` e bloqueado pela politica de execucao. Use `npm.cmd` e `npx.cmd`.

## Etapa 1 - Setup do Backend FastAPI
Arquivos criados:
- `backend/app/__init__.py`
- `backend/app/main.py`
- `backend/requirements.txt`
- `backend/tests/test_health.py`

Pastas criadas:
- `backend/app`
- `backend/tests`
- `cache`

Dependencias instaladas na `.venv`:
- `fastapi`
- `uvicorn`
- `python-multipart`
- `pytest`
- `httpx`
- `aiofiles`

Implementacao entregue:
- Aplicacao FastAPI criada com factory `create_app`.
- CORS configurado com origens permitidas para o futuro frontend React em `http://localhost:5173` e `http://127.0.0.1:5173`.
- Rota `GET /api/v1/health` retornando `{"status": "ok"}`.
- Teste automatizado validando resposta do health check.
- Teste automatizado validando CORS para `http://localhost:5173`.

## Etapa 2 - Servico de Seguranca de Arquivos
Arquivos criados:
- `backend/app/services/__init__.py`
- `backend/app/services/file_security.py`
- `backend/tests/test_file_security.py`

Implementacao entregue:
- Servico `save_upload_file` para salvar uploads de forma assincrona com `aiofiles`.
- Nome final gerado com UUID, sem reaproveitar o nome enviado pelo usuario.
- Sanitizacao do nome original para remover caminho externo/path traversal.
- Validacao estrita de extensoes permitidas: `.csv` e `.xlsx`.
- Validacao de MIME Type de acordo com a extensao.
- Limite padrao de upload: 25 MB.
- Remocao automatica de arquivo parcial caso a validacao de tamanho falhe durante o salvamento.
- Excecao de dominio `FileValidationError` para a futura rota HTTP traduzir em resposta adequada.
- Dataclass `SavedUpload` com metadados do arquivo salvo.

Testes criados:
- Salva `.xlsx` permitido com UUID.
- Sanitiza nome original com path traversal.
- Rejeita `.exe`.
- Rejeita `.sh`.
- Rejeita MIME Type incorreto.
- Remove arquivo parcial quando excede limite de tamanho.

## Etapa 3 - Rota de Integracao Assincrona do Script
Arquivos criados:
- `backend/app/routers/__init__.py`
- `backend/app/routers/conciliador.py`
- `backend/tests/test_conciliador.py`

Arquivos alterados:
- `backend/app/main.py`

Implementacao entregue:
- Router `conciliador` conectado ao FastAPI.
- Rota `POST /api/v1/conciliar`.
- Recebimento de dois uploads multipart: `cliente` e `wordpress`.
- Validacao dos arquivos usando `app/services/file_security.py`.
- Criacao de pasta de job em `cache/conciliacoes/<job_id>`.
- Salvamento dos uploads em `uploads/` com nomes UUID.
- Preparacao dos caminhos de saida em `outputs/wordpress_atualizada.xlsx` e `outputs/relatorio_conciliacao.xlsx`.
- Execucao de `conciliador_planilhas_sku.py` por `asyncio.create_subprocess_exec`, sem bloquear o event loop.
- Captura de `stdout` e `stderr` para futura exibicao de logs no frontend.
- Resposta JSON com `job_id`, status, metadados dos uploads, caminhos dos outputs e logs.
- Tratamento HTTP 400 para arquivo invalido.
- Tratamento HTTP 500 para falha do subprocesso.
- Cleanup seguro de job invalido limitado a `cache/conciliacoes`.

Testes criados:
- Upload valido chama o subprocesso mockado e retorna HTTP 200.
- Upload invalido `.exe` retorna HTTP 400 antes de chamar o subprocesso.
- Falha mockada do subprocesso retorna HTTP 500 com logs.

Validacao executada:
- Comando: `cd backend; ..\.venv\Scripts\python.exe -m pytest -v`
- Resultado: `11 passed, 1 warning`
- Aviso observado: `StarletteDeprecationWarning` relacionado ao `TestClient`; nao bloqueia a Etapa 3.

## Etapa 4 - Setup do Frontend React + Vite
Comandos usados:
- `npm.cmd create vite@latest frontend -- --template react`
- `cd frontend`
- `npm.cmd install`
- `npm.cmd install -D tailwindcss@3.4.17 postcss autoprefixer`
- `npx.cmd tailwindcss init -p`
- `npm.cmd install lucide-react`

Arquivos principais criados ou alterados:
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/index.html`
- `frontend/tailwind.config.js`
- `frontend/postcss.config.js`
- `frontend/src/App.jsx`
- `frontend/src/index.css`
- `frontend/src/components/UploadForm.jsx`
- `frontend/src/components/LogViewer.jsx`

Arquivos removidos:
- `frontend/src/App.css`
- `frontend/src/assets/react.svg`
- `frontend/src/assets/vite.svg`
- `frontend/src/assets/hero.png`
- `frontend/public/icons.svg`

Implementacao entregue:
- Projeto React criado com Vite.
- TailwindCSS configurado com `content` apontando para `index.html` e `src/**/*.{js,jsx}`.
- `lucide-react` instalado para uso de icones na interface.
- Tela base profissional com header, status da etapa, fluxo em 3 fases, painel de conciliacao e visor de logs.
- Componente `UploadForm` criado com campos de arquivo para `Planilha WordPress` e `Planilha do cliente`.
- Componente `LogViewer` criado para exibir logs/status da automacao.
- Botao de processamento deixado desabilitado, pois a chamada real da API pertence a Etapa 5.

Validacao executada:
- Comando: `cd frontend; npm.cmd run build`
- Resultado: build concluido com sucesso.
- Comando: `cd frontend; npm.cmd run lint`
- Resultado: lint concluido sem erros.
- Servidor local iniciado com `npm.cmd run dev -- --host 127.0.0.1 --port 5173`.
- URL local validada: `http://127.0.0.1:5173/`.
- PID observado do processo iniciado: `4932`.
- PID observado ouvindo a porta `5173`: `20844`.

## Etapa 5 - Integracao Frontend (Upload, Progresso e Download)
Arquivos criados:
- `frontend/src/api/conciliador.js`
- `frontend/src/components/DownloadPanel.jsx`

Arquivos alterados:
- `backend/app/routers/conciliador.py`
- `backend/tests/test_conciliador.py`
- `frontend/src/App.jsx`
- `frontend/src/components/UploadForm.jsx`
- `frontend/src/components/LogViewer.jsx`

Implementacao entregue:
- Frontend conectado ao endpoint `POST /api/v1/conciliar`.
- Configuracao de URL da API via `VITE_API_BASE_URL`, com padrao `http://127.0.0.1:8000`.
- Envio multipart real com os campos `cliente` e `wordpress`.
- Estados de tela `idle`, `loading`, `success` e `error`.
- Botao de processamento desabilitado enquanto a requisicao esta em andamento.
- Barra visual de carregamento durante processamento.
- Logs dinamicos com mensagens de envio, processamento, sucesso e erro.
- Erros da API convertidos em mensagem amigavel na interface.
- Painel `DownloadPanel` exibido apos sucesso.
- Botões de download para `wordpress_atualizado` e `relatorio`.
- Backend ajustado para retornar `download_url` em vez de expor caminhos internos do Windows.
- Endpoint `GET /api/v1/conciliar/{job_id}/download/{artifact}` criado para baixar artefatos com seguranca.
- Artefatos aceitos no download: `wordpress_atualizado` e `relatorio`.

Testes criados ou ajustados:
- Resposta de conciliacao validando `download_url`.
- Download de artefato existente retorna HTTP 200 e conteudo do arquivo.
- Artefato desconhecido retorna HTTP 404.

Validacao executada:
- Comando: `cd backend; ..\.venv\Scripts\python.exe -m pytest -v`
- Resultado: `13 passed, 1 warning`
- Comando: `cd frontend; npm.cmd run build`
- Resultado: build concluido com sucesso.
- Comando: `cd frontend; npm.cmd run lint`
- Resultado: lint concluido sem erros.
- Backend local iniciado em `http://127.0.0.1:8000`.
- Health check validado: `GET /api/v1/health` retornou `{"status":"ok"}`.
- Frontend local segue em `http://127.0.0.1:5173/`.

## Proximo passo sugerido
- Testar manualmente a conciliacao pela tela usando uma planilha WordPress e uma planilha do cliente.
- Depois disso, definir a proxima etapa fora deste documento: conectar a busca de imagens ao resultado gerado.
