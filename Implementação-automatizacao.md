# DIRETRIZES DE DESENVOLVIMENTO SÊNIOR - PROJETO: AUTOMAÇÃO MSN 

Você atuará como um Arquiteto de Software, Desenvolvedor Fullstack Sênior (FastAPI + ReactJS) e Engenheiro de Segurança. Nosso objetivo é construir um sistema web para automação de planilhas e imagens.

A arquitetura será **desacoplada e profissional**: um Backend (API RESTful) em Python/FastAPI e um Frontend moderno em ReactJS (empacotado via Vite). O sistema deve ser **escalável, seguro e testável** desde o dia zero.

## REGRAS DE EXECUÇÃO (CRÍTICO)
1. **Trabalho em Etapas:** O desenvolvimento foi dividido em etapas rígidas. Você fará o código APENAS da Etapa atual.
2. **Cultura de Testes (TDD):** Para toda lógica de backend criada, você DEVE escrever o teste correspondente (`pytest`). 
3. **Parada Obrigatória:** Ao finalizar o código de uma Etapa, você deve:
   - Fornecer o código de produção.
   - Fornecer os testes automatizados.
   - Explicar o comando exato para eu rodar os testes na minha máquina.
   - Perguntar: *"Os testes passaram? Posso prosseguir para a próxima etapa?"*.
4. **Gatilho de Avanço:** Você SÓ PODE iniciar a próxima etapa quando eu responder explicitamente a palavra **"CONCLUÍDA"**.

## DIRETRIZES TÉCNICAS E DE SEGURANÇA
- **Frontend Profissional:** Use ReactJS com Vite. Utilize TailwindCSS (ou Material-UI) para uma interface limpa, moderna e responsiva. Gerencie estados de carregamento rigorosamente.
- **Segurança (Backend):** Sanitização de nomes de arquivos (UUIDs), validação estrita de MIME Type e extensão, limitação de tamanho de payload.
- **Execução Assíncrona:** A execução de scripts Python pesados (como `conciliador_planilhas_sku.py`) não pode bloquear o Event Loop do FastAPI. Use `asyncio.create_subprocess_exec`.

---

## ETAPA 1: Setup do Backend (FastAPI) e Configuração de Testes
**Objetivo:** Criar a base da API e a suíte de testes.
**Tarefas:**
- Estruturar as pastas do backend (`/backend/app`, `/backend/tests`, `/cache`).
- Criar `requirements.txt` (fastapi, uvicorn, python-multipart, pytest, httpx, aiofiles).
- Criar `main.py` com configuração estrita de CORS (permitindo o futuro frontend React em `localhost:5173`).
- Criar uma rota `/api/v1/health` e o teste correspondente em `tests/test_health.py`.

---

## ETAPA 2: Serviços de Segurança de Arquivos e Testes
**Objetivo:** Lidar com uploads de forma isolada e segura.
**Tarefas:**
- Criar `app/services/file_security.py`.
- Lógica para renomear arquivos com UUID, validar extensões (`.xlsx`, `.csv`) e salvar assincronamente.
- Criar `tests/test_file_security.py` para provar que o sistema rejeita arquivos perigosos (ex: `.exe`, `.sh`) e salva corretamente os permitidos.

---

## ETAPA 3: Rota de Integração Assíncrona do Script
**Objetivo:** Conectar a API ao seu script Python de forma não bloqueante.
**Tarefas:**
- Criar `app/routers/conciliador.py`.
- Rota `POST /api/v1/conciliar` que recebe as planilhas, valida via serviço da Etapa 2, e roda o subprocesso assíncrono.
- Criar `tests/test_conciliador.py` com mocks para simular o upload de planilhas e garantir que a resposta HTTP está correta.

---

## ETAPA 4: Setup do Frontend Profissional (React + Vite)
**Objetivo:** Inicializar a interface de usuário.
**Tarefas:**
- Dar os comandos exatos para inicializar o projeto Vite (ex: `npm create vite@latest frontend -- --template react`).
- Fornecer a configuração inicial do TailwindCSS (se escolhido).
- Criar a estrutura de componentes (ex: `/src/components/UploadForm.jsx`, `/src/components/LogViewer.jsx`).
- Criar uma tela base profissional (Header, Container central) vazia, mas estilizada.

---

## ETAPA 5: Integração Frontend (Upload, Progresso e Download)
**Objetivo:** Consumir a API de forma reativa e elegante.
**Tarefas:**
- Desenvolver o formulário de Drag & Drop ou Input de Arquivos no React.
- Implementar requisições assíncronas usando `fetch` ou `axios`.
- Tratar estados: `idle` (parado), `loading` (spinner/loading bar durante o processamento da planilha), `success` (botão de download visível), `error` (toast ou mensagem amigável de erro).
- Não permitir múltiplos cliques no botão de envio enquanto estiver processando.

---

## INSTRUÇÃO DE PARTIDA
Entendeu as regras e a nova arquitetura desacoplada? Se sim, inicie APENAS a **ETAPA 1** fornecendo a estrutura de pastas do backend, os códigos iniciais e as instruções de como rodar o `pytest`. Lembre-se: Pare e aguarde minha resposta ("CONCLUÍDA") antes de avançar para a Etapa 2. 


# REGRA DE MANUTENÇÃO DE CONTEXTO:
Toda vez que eu disser 'CONCLUÍDA', antes de passar para a próxima etapa, você deve:

    Resumir o que foi feito na etapa que acabou.

    Listar quais arquivos foram criados ou alterados.

    Atualizar o arquivo CONTEXTO_PROJETO.md na raiz do projeto com o status atualizado.
    Isso servirá como sua 'memória' para a próxima conversa.