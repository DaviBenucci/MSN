# Estoque e catalogo

## O que o layout pode fazer

- Exibir status de estoque vindo do WooCommerce.
- Destacar estoque baixo quando o WooCommerce informar poucas unidades.
- Mostrar mensagem de compra assistida quando houver duvida de compatibilidade.
- Orientar o cliente a falar no WhatsApp antes de comprar item tecnico.

## O que o layout nao deve fazer

- Alterar quantidade maxima disponivel.
- Recalcular estoque via JavaScript.
- Esconder produto fora de estoque sem regra do WooCommerce.
- Criar mensagem falsa de disponibilidade.
- Alterar preco, frete, total ou pagamento.

## Configuracoes recomendadas no WooCommerce

- Ativar gerenciamento de estoque para produtos fisicos.
- Definir limite de estoque baixo por categoria quando fizer sentido.
- Usar `Permitir encomendas` apenas quando a operacao conseguir atender.
- Exibir produtos fora de estoque somente se houver estrategia comercial clara.
- Preencher peso e dimensoes para produtos com frete calculado.
- Revisar produtos com validade vencida e deixar isso explicito no nome, descricao e atributos.

## Atributos recomendados

- Marca.
- Modelo compativel.
- Codigo do suprimento.
- Cor.
- Tipo.
- Rendimento.
- Condicao.
- Validade.
- Peso.
- Dimensoes.

## Rotina de manutencao

- Semanal: revisar produtos com estoque baixo.
- Quinzenal: revisar produtos sem imagem ou sem categoria.
- Mensal: revisar SKU, atributos e alt text.
- Apos importacao: validar amostra de produtos antes de publicar filtros.

