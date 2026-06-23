# Checklist de QA

## Responsividade

- [ ] `MOBILE-FIRST-RESPONSIVIDADE.md` foi lido antes da aprovacao visual.
- [ ] 320px sem rolagem horizontal.
- [ ] 360px sem corte em header, busca, botoes, cards e formularios.
- [ ] 375px com busca, carrinho, WhatsApp e CTA principal visiveis.
- [ ] 390px com conteudo principal legivel acima da primeira dobra quando aplicavel.
- [ ] 412px sem sobreposicao de textos, botoes ou imagens.
- [ ] 430px sem espacos laterais excessivos ou elementos espremidos.
- [ ] 768px com layout de tablet organizado.
- [ ] 820px com tablet intermediario organizado.
- [ ] 1024px sem quebra de header, grid, filtro ou checkout.
- [ ] 1440px com conteudo centralizado e sem espacos vazios excessivos.

## Mobile-first rigoroso

- [ ] Toda mudanca visual foi avaliada primeiro no modo mobile do Elementor.
- [ ] A pagina nao depende de hover para mostrar informacao ou acao essencial.
- [ ] Elementos tocaveis tem area minima aproximada de 44px.
- [ ] Nao ha texto cortado, botao com label quebrado de forma ruim ou conteudo sobreposto.
- [ ] Formulario mobile esta em uma coluna com labels visiveis.
- [ ] Header, quickbar, busca, carrinho e WhatsApp continuam acessiveis em 360px.
- [ ] Quickbar mobile mostra Especialista, Mais Vendidos, Novidades, Minha Conta, Contato e Visite nosso outro site.
- [ ] Filtros, menus horizontais e quickbars rolam sem criar overflow no body.
- [ ] Banners, barras fixas e consentimento nao cobrem CTA, campos ou botoes de pagamento.
- [ ] Apos salvar, o CSS do Elementor foi regenerado e o cache foi limpo antes do teste final.

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
- [ ] Checkout exige telefone no campo real do WooCommerce.
- [ ] Checkout exige CPF para pessoa fisica e CNPJ para pessoa juridica.
- [ ] CPF, CNPJ e telefone aparecem no admin do pedido depois de um pedido teste.
- [ ] Mercado Pago em modo teste permite chegar ao pagamento com CPF/CNPJ/telefone preenchidos.
- [ ] Console nao mostra script do Mercado Pago tentando configurar checkout em paginas sem checkout.
- [ ] Banner de consentimento nao cobre botao de compra, checkout, login/cadastro ou CTAs principais.
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

- [ ] Quickbar mobile pode ser navegada por toque e teclado.
- [ ] Tecla Esc fecha modal, filtro ou painel aberto.
- [ ] Foco fica preso dentro de modal, filtro ou painel aberto.
- [ ] Labels visiveis nos formularios.
- [ ] Contraste suficiente.
- [ ] Imagens com alt.
