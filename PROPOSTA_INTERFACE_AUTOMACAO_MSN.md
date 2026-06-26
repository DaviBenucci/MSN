# Proposta: interface web para automacao de planilhas e imagens MSN

## Objetivo

Criar uma interface em HTML/CSS com backend Python para transformar o fluxo atual de scripts em um assistente visual por etapas.

A interface deve permitir que o usuario:

1. Envie a planilha base que sera atualizada.
2. Envie a planilha do cliente.
3. Rode a conciliacao automaticamente.
4. Baixe o resultado da conciliacao em `.xlsx` e `.csv`.
5. Avance para a busca de imagens.
6. Baixe imagens/candidatas encontradas ou avance para a etapa seguinte.
7. Rode a tratativa/otimizacao das imagens.
8. Baixe uma pasta `.zip` com os produtos tratados e organizados por SKU.
9. Acompanhe logs e progresso em tempo real.
10. Receba aviso final de limpeza de cache temporario.

## Observacao importante

HTML e CSS sozinhos nao conseguem executar scripts Python nem manipular arquivos locais de forma segura.

Para essa ideia funcionar, a aplicacao precisa de duas partes:

- **Frontend:** tela em HTML, CSS e JavaScript.
- **Backend local:** servidor Python, por exemplo FastAPI ou Flask, responsavel por receber arquivos, executar scripts, gerar downloads, zipar pastas e limpar cache.

O usuario acessaria algo como:

```text
http://localhost:8000
```

## Scripts envolvidos

Scripts atuais que podem ser integrados:

- `conciliador_planilhas_sku.py`
- `buscador_candidatas_imagens.py`
- `otimizador_imagens.py`

Eles seriam chamados pelo backend Python, nao diretamente pelo navegador.

## Fluxo proposto

### Etapa 1: upload das planilhas

Tela inicial com dois campos:

- `Planilha WordPress/base`
- `Planilha do cliente`

Tambem pode haver campos opcionais:

- Nome da aba da planilha do cliente.
- Nome da coluna de produto/nome.
- Nome da coluna de estoque.
- Nome da coluna de preco.
- Nome da aba da planilha WordPress.

Botao principal:

```text
Iniciar conciliacao
```

Ao clicar, o backend:

1. Cria uma pasta temporaria de trabalho.
2. Salva as planilhas enviadas nessa pasta.
3. Executa o script de conciliacao.
4. Gera os arquivos de saida.

Saidas esperadas:

```text
wordpress_atualizada.xlsx
wordpress_atualizada.csv
relatorio_conciliacao.xlsx
relatorio_conciliacao.csv
```

### Etapa 2: resultado da conciliacao

A tela deve mostrar:

- Quantidade de produtos atualizados.
- Quantidade de produtos novos adicionados.
- Quantidade de produtos ignorados ou com erro.
- Link para baixar `.xlsx`.
- Link para baixar `.csv`.
- Link para baixar relatorio.

Botoes:

```text
Baixar conciliacao
Ir para busca de imagens
```

### Etapa 3: busca de imagens

Ao avancar, a aplicacao usa a planilha atualizada gerada na etapa anterior.

O backend deve:

1. Criar uma estrutura temporaria de produtos por SKU.
2. Executar `buscador_candidatas_imagens.py`.
3. Baixar imagens fortes/boas.
4. Opcionalmente baixar rejeitadas em `_review`.
5. Gerar relatorios HTML/CSV.

Saidas esperadas:

```text
candidatas-imagens.csv
candidatas-aprovacao.csv
revisao-candidatas.html
skus-pulados-imagens.csv
imagens-candidatas.zip
```

A tela deve mostrar:

- Produtos analisados.
- Imagens baixadas.
- Produtos sem imagem encontrada.
- Produtos que foram para `_review`.
- Link para abrir/baixar relatorio HTML.
- Link para baixar pacote das candidatas.

Botoes:

```text
Baixar arquivos de imagens
Ir para tratativa
```

### Etapa 4: tratativa/otimizacao das imagens

Ao avancar, o backend executa `otimizador_imagens.py` sobre as imagens aprovadas ou localizadas.

O script deve:

- Padronizar imagens em WebP.
- Criar arquivos em 800x800.
- Centralizar o produto.
- Usar fundo branco quando configurado.
- Ignorar `_review`.
- Organizar tudo em pastas por SKU.

Saida esperada:

```text
products_tratados.zip
```

Estrutura do zip:

```text
products/
  TON-HP-CE253AZ-MAG/
    TON-HP-CE253AZ-MAG-01.webp
    TON-HP-CE253AZ-MAG-02.webp
  IMP-SAM-C3060FR/
    IMP-SAM-C3060FR-01.webp
```

Tela final:

- Resumo de produtos tratados.
- Quantidade de imagens geradas.
- Produtos com falha.
- Link para baixar `.zip`.

Botao:

```text
Baixar produtos tratados
```

### Etapa 5: limpeza de cache

Depois que o usuario baixar o `.zip`, a interface deve exibir aviso:

```text
Download iniciado. Aguarde alguns instantes: os arquivos temporarios serao removidos do cache.
```

O backend deve:

1. Aguardar um pequeno intervalo de seguranca.
2. Apagar a pasta temporaria daquele processamento.
3. Registrar no log que o cache foi limpo.

Mensagem final:

```text
Processo finalizado. Cache limpo com sucesso.
```

## Logs em tempo real

A interface precisa exibir uma area de log com tudo que esta acontecendo.

Exemplo:

```text
[10:05:12] Upload recebido: cliente.xlsx
[10:05:13] Upload recebido: wordpress.xlsx
[10:05:14] Iniciando conciliacao
[10:05:20] Produtos atualizados: 320
[10:05:20] Produtos adicionados: 18
[10:05:21] Arquivo gerado: wordpress_atualizada.xlsx
[10:06:01] Iniciando busca de imagens
[10:08:43] Imagens baixadas: 92
[10:09:10] Iniciando otimizacao
[10:12:55] ZIP final gerado
[10:13:20] Cache limpo
```

Tecnologias possiveis para logs:

- Server-Sent Events (SSE)
- WebSocket
- Polling em `/jobs/{job_id}/status`

Para comecar simples, SSE ou polling ja resolvem bem.

## Estrutura de cache temporario

Cada processamento deve ter um ID unico.

Exemplo:

```text
cache/
  jobs/
    20260626-110500-a1b2c3/
      uploads/
        cliente.xlsx
        wordpress.xlsx
      conciliacao/
        wordpress_atualizada.xlsx
        wordpress_atualizada.csv
        relatorio_conciliacao.xlsx
        relatorio_conciliacao.csv
      imagens/
        products/
        _reports/
        imagens-candidatas.zip
      final/
        products/
        products_tratados.zip
      logs/
        job.log
```

Ao terminar e apos download final:

```text
cache/jobs/20260626-110500-a1b2c3/
```

deve ser removida.

## Backend sugerido

Sugestao: FastAPI.

Motivos:

- Facil de criar upload de arquivos.
- Facil de retornar downloads.
- Bom suporte a tarefas em background.
- Facil de expor logs por SSE/WebSocket.
- Documentacao automatica em `/docs`.

Rotas possiveis:

```text
GET  /
POST /api/jobs
POST /api/jobs/{job_id}/conciliar
POST /api/jobs/{job_id}/buscar-imagens
POST /api/jobs/{job_id}/otimizar
GET  /api/jobs/{job_id}/status
GET  /api/jobs/{job_id}/logs
GET  /api/jobs/{job_id}/download/conciliacao-xlsx
GET  /api/jobs/{job_id}/download/conciliacao-csv
GET  /api/jobs/{job_id}/download/imagens
GET  /api/jobs/{job_id}/download/final-zip
DELETE /api/jobs/{job_id}
```

## Frontend sugerido

Tela unica com etapas:

1. Upload
2. Conciliacao
3. Busca de imagens
4. Tratativa
5. Download final
6. Limpeza

Componentes:

- Barra de progresso geral.
- Cards de etapa.
- Campos de upload.
- Botoes de acao.
- Area de log.
- Lista de arquivos gerados.
- Avisos de erro.
- Aviso de limpeza de cache.

## Estados da interface

Estados por etapa:

- `aguardando`
- `em_execucao`
- `concluido`
- `erro`
- `cancelado`

Exemplo visual:

```text
[1] Upload              concluido
[2] Conciliacao         concluido
[3] Busca de imagens    em_execucao
[4] Tratativa           aguardando
[5] Download final      aguardando
```

## Cuidados importantes

### Nao sobrescrever arquivos originais

A aplicacao nao deve alterar diretamente:

- planilha enviada pelo cliente;
- planilha WordPress/base enviada;
- arquivos originais fora do cache.

Sempre trabalhar com copias dentro do cache do job.

### Limpeza de cache

O cache deve ser limpo:

- apos download final;
- manualmente se o usuario cancelar;
- automaticamente se o job ficar velho, por exemplo mais de 24 horas.

### Erros e recuperacao

Se uma etapa falhar:

- manter os arquivos ja gerados;
- mostrar erro legivel no log;
- permitir baixar os arquivos parciais;
- permitir repetir a etapa, se fizer sentido.

### Segurança

Mesmo sendo local, validar:

- extensoes permitidas: `.xlsx`, `.xls`, `.csv`;
- tamanho maximo de arquivo;
- nomes de arquivo seguros;
- caminhos sempre dentro do cache;
- nunca permitir que o usuario envie um caminho arbitrario para apagar arquivos.

## Ordem recomendada de desenvolvimento

### Fase 1: prototipo local simples

- Backend FastAPI.
- HTML/CSS simples.
- Upload das duas planilhas.
- Execucao da conciliacao.
- Download `.xlsx` e `.csv`.
- Log basico.

### Fase 2: busca de imagens

- Integrar `buscador_candidatas_imagens.py`.
- Mostrar progresso.
- Gerar relatorios.
- Baixar pacote de candidatas.

### Fase 3: otimizacao e zip final

- Integrar `otimizador_imagens.py`.
- Gerar `products_tratados.zip`.
- Download final.
- Limpeza de cache.

### Fase 4: refinamento

- Melhorar interface.
- Adicionar historico temporario de jobs.
- Permitir cancelar processo.
- Melhorar mensagens de erro.
- Adicionar validacoes pre-processamento.

## Resultado esperado

Ao final, o usuario tera uma ferramenta local com fluxo guiado:

```text
Upload das planilhas
-> Conciliacao
-> Download dos resultados
-> Busca de imagens
-> Revisao/Download de candidatas
-> Tratativa final
-> Download do ZIP final
-> Limpeza automatica do cache
```

Essa ferramenta reduz o risco de erro manual, torna o processo repetivel e permite acompanhar tudo por logs na tela.
