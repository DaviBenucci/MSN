# Contexto Codex - Projeto MSN

## Estado atual
- Data da atualizacao: 26/06/2026
- Fase atual: Etapa 2 concluida
- Proxima etapa bloqueada: Etapa 3 - Rota de Integracao Assincrona do Script
- Regra de avanço: iniciar a Etapa 3 somente quando o usuario responder explicitamente `CONCLUÍDA`.

## Observacao de alinhamento
- O contexto inicial indicava Etapa 3 em progresso, mas o workspace nao tinha a estrutura `backend/`.
- A implementacao foi realinhada com o estado do filesystem e com o documento `Implementação-automatizacao.md`, iniciando pela Etapa 1.

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

Validacao executada:
- Comando: `cd backend; ..\.venv\Scripts\python.exe -m pytest -v`
- Resultado: `8 passed, 1 warning`
- Aviso observado: `StarletteDeprecationWarning` relacionado ao `TestClient`; nao bloqueia a Etapa 2.

## Proximo passo
Quando o usuario responder `CONCLUÍDA`, iniciar a Etapa 3:
- criar `backend/app/routers/conciliador.py`;
- criar rota `POST /api/v1/conciliar`;
- receber duas planilhas via upload;
- validar os arquivos usando `app/services/file_security.py`;
- executar `conciliador_planilhas_sku.py` via subprocesso assincrono;
- criar `backend/tests/test_conciliador.py` com mocks para o upload e subprocesso.
