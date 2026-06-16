# Checklist de QA

## Responsividade

- [ ] 320px sem rolagem horizontal.
- [ ] 375px com busca, carrinho e WhatsApp visiveis.
- [ ] 768px com layout de tablet organizado.
- [ ] 1024px sem quebra de header.
- [ ] 1440px com conteudo centralizado e sem espacos vazios excessivos.

## Fluxos

- [ ] Busca por produto.
- [ ] Busca sem resultado.
- [ ] Teste minimo `[products limit="12" columns="3" visibility="visible"]` mostra produtos.
- [ ] Loop Grid usa template tipo Products, nao Posts.
- [ ] Loja/categoria/busca usa Current Query quando aplicavel.
- [ ] Categoria com filtros.
- [ ] Abrir e fechar filtro mobile.
- [ ] Produto com galeria, preco, estoque e CTA.
- [ ] Adicionar ao carrinho.
- [ ] Alterar quantidade no carrinho.
- [ ] Aplicar cupom, se houver.
- [ ] Calcular frete, se houver.
- [ ] Ir para checkout.
- [ ] Checkout mostra campos, frete, pagamento, totais e mensagens nativas do WooCommerce.
- [ ] Login e cadastro em Minha Conta.
- [ ] Recuperar senha.
- [ ] Formulario de contato abre WhatsApp com mensagem organizada.
- [ ] Formulario Avalie seu pedido abre WhatsApp com mensagem organizada.
- [ ] Links de Privacidade, Trocas e Devolucoes, Finalizacao de Compra e Avalie seu pedido funcionam.

## Seguranca funcional

- [ ] Nenhum JS customizado altera preco.
- [ ] Nenhum JS customizado altera total.
- [ ] Nenhum JS customizado altera frete.
- [ ] Nenhum JS customizado altera pagamento.
- [ ] Mensagens de erro do WooCommerce continuam visiveis.
- [ ] Checkout foi testado em celular real.

## Acessibilidade

- [ ] Menu mobile abre e fecha por teclado.
- [ ] Tecla Esc fecha menu e modal.
- [ ] Foco fica preso dentro de menu/modal aberto.
- [ ] Labels visiveis nos formularios.
- [ ] Contraste suficiente.
- [ ] Imagens com alt.
