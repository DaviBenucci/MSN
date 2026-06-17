# Mapa de componentes

## Global

Arquivos:

- `shared/msn-global-css.html`
- `shared/msn-theme-init-js.html`
- `shared/msn-global-js.html`

Onde aplicar:

- `msn-theme-init-js.html` no Head pelo Elementor Pro Custom Code.
- CSS global do Elementor ou CSS adicional do tema.
- JS global no footer pelo Elementor Pro Custom Code.

Funcoes:

- Tokens premium claro/escuro por `:root[data-theme]`.
- Seletor de tema por `data-msn-theme-toggle` e `data-msn-theme-choice`.
- Preferencia persistida em `msn-theme-preference`.

## Regra para slots WooCommerce no Elementor

Os slots WooCommerce nao devem ser entendidos como widgets dentro de widget HTML. O comentario dentro dos arquivos `.html` marca apenas a posicao visual.

Monte esses trechos com Containers do Elementor:

- Container wrapper com a classe da section.
- Container interno com `msn-container`.
- Container do slot com a classe indicada.
- Widget WooCommerce, Loop Grid, Products/Archive Products ou widget Shortcode como filho real do slot.

Use essa regra em Loja, Produto, Carrinho, Finalizacao de Compra e Minha Conta.

## Header

Sections:

- `components/header/sections/01-topbar`
- `components/header/sections/02-main`
- `components/header/sections/03-quickbar`
- `components/header/sections/04-mobile-drawer`
- `components/header/sections/00-header.js`

Funcoes:

- Busca nativa WooCommerce.
- Conta, pedidos e carrinho.
- Contador de carrinho por `data-msn-cart-count`, preenchido pela bridge.
- Seletor de tema desktop e no menu mobile.
- Categorias principais, WhatsApp e menu mobile.

## Footer

Sections:

- `components/footer/sections/00-footer-layout.css`
- `components/footer/sections/00-footer-accordion.js`
- `components/footer/sections/01-brand`
- `components/footer/sections/02-categories`
- `components/footer/sections/03-service`
- `components/footer/sections/04-policies`
- `components/footer/sections/05-bottom`

Funcoes:

- Atendimento, categorias, politicas, CNPJ, endereco e sanfonas mobile.

## Home

Sections:

- `components/home/sections/01-hero`
- `components/home/sections/02-benefits`
- `components/home/sections/03-categories`
- `components/home/sections/04-featured-products`
- `components/home/sections/05-help`
- `components/home/sections/00-smooth-scroll.js`

Dados WooCommerce:

- Produtos em destaque: bridge `data-msn-products` com query `{"per_page":8,"orderby":"date","order":"DESC"}`.
- Fallback: widget Products ou shortcode `[products limit="8" columns="4" orderby="date" order="DESC"]`.

## Loja, categorias e busca

Sections:

- `components/shop/sections/01-hero-search`
- `components/shop/sections/02-products-layout`

Slots WooCommerce:

- Produtos: Loop Grid tipo `Products`, Products/Archive Products ou shortcode `[products]`.
- Filtros: widget Woofilters do WBW ou shortcode copiado do plugin.

## Card de produto

Arquivos:

- `components/product-card/msn-product-card.css`
- `components/product-card/msn-product-card-loop-item.css`
- `components/product-card/README.md`

Onde aplicar:

- Classe `msn-product-card-model` no wrapper do Loop Grid, Products widget ou shortcode.

## Produto

Sections:

- `components/product/sections/01-summary`
- `components/product/sections/02-details`
- `components/product/sections/03-mobile-bar`
- `components/product/sections/04-related`
- `components/product/sections/04-related.css`

Slots WooCommerce:

- Product Images, Product Title, Product Price, Stock/Product Meta, Add To Cart, Product Data Tabs, Product Content e Related Products/Upsells.

## Carrinho

Sections:

- `components/cart/sections/01-hero`
- `components/cart/sections/02-cart-slot`
- `components/cart/sections/03-empty-state`

Slot WooCommerce:

- Shortcode `[woocommerce_cart]` ou widget Cart.
- Montagem: Container `msn-cart-woo-slot` contendo o widget Cart/Shortcode. Nao cole esse shortcode dentro do widget HTML.

## Finalizacao de Compra

Sections:

- `components/checkout/sections/01-hero`
- `components/checkout/sections/02-checkout-slot`
- `components/checkout/sections/03-checkout-woocommerce`

Slot WooCommerce:

- Shortcode `[woocommerce_checkout]` ou widget Checkout.
- Montagem: Container `msn-checkout-woo-slot` contendo o widget Checkout/Shortcode. Nao cole esse shortcode dentro do widget HTML.
- Manutencao: `02-checkout-slot.css` cuida da moldura Elementor; `03-checkout-woocommerce.css` cuida dos elementos internos gerados pelo WooCommerce/checkout em etapas.

## Minha Conta

Sections:

- `components/account/sections/01-hero`
- `components/account/sections/02-account-slot`
- `components/account/sections/03-help`

Slot WooCommerce:

- Shortcode `[woocommerce_my_account]` ou widget My Account.
- Montagem: Container `msn-account-woo-slot` contendo o widget My Account/Shortcode. Nao cole esse shortcode dentro do widget HTML.

## Contato

Sections:

- `components/contact/sections/01-hero`
- `components/contact/sections/02-contact-form`

Funcoes:

- Canais oficiais, formulario com honeypot simples e abertura de WhatsApp com mensagem organizada.

## Politica de Devolucao

Sections:

- `components/returns/sections/01-hero`
- `components/returns/sections/02-policy-content`

Funcoes:

- Conteudo institucional de trocas, devolucoes, arrependimento, conferencia e atendimento.
- Revisar texto final com responsavel juridico/administrativo antes de publicar.

## Politica de Privacidade

Sections:

- `components/privacy/sections/01-hero`
- `components/privacy/sections/02-privacy-content`

Funcoes:

- Conteudo institucional sobre dados pessoais, pedidos, cookies, WooCommerce e canais de contato.
- Revisar texto final com responsavel juridico/administrativo antes de publicar.

## Avalie seu Pedido

Sections:

- `components/order-review/sections/01-hero`
- `components/order-review/sections/02-review-form`
- `components/order-review/sections/03-guidelines`

Funcoes:

- Formulario com honeypot simples e abertura de WhatsApp com mensagem organizada.
- Nao consulta pedidos no WooCommerce e nao grava dados no banco.
