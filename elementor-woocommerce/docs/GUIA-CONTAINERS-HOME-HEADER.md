# Guia de containers - Home e Header

Este guia organiza a montagem por partes no Elementor mantendo WooCommerce como fonte dos dados vivos.

## Pre-requisitos

- Plugin `msn-woocommerce-layout-bridge` ativo.
- CSS global `shared/msn-global.css` carregado.
- JS global `shared/msn-global.js` carregado.
- JS do header `components/header/msn-header.js` carregado no footer.

## Header

Opcao mais simples:

- Cole `components/header/msn-header.html`.
- Cole `components/header/msn-header.css`.
- Carregue `components/header/msn-header.js`.

Opcao por containers:

1. Crie um container pai com classe `msn-header` e atributo `data-msn-header`.
2. Cole os blocos de `components/header/sections` nesta ordem:
   - `01-topbar`
   - `02-main`
   - `03-quickbar`
   - `04-mobile-drawer`
3. Cole o CSS de cada bloco ou mantenha `components/header/msn-header.css` como CSS unico.

O formulario de busca ja envia `post_type=product`. O contador visual usa `data-msn-cart-count` e e preenchido pela bridge.

## Home

Opcao combinada:

- Cole `components/home/msn-home.html`.
- Cole `components/home/msn-home.css`.

Opcao por containers:

1. Cole os blocos de `components/home/sections` nesta ordem:
   - `01-hero`
   - `02-benefits`
   - `03-categories`
   - `04-featured-products`
   - `05-help`
2. Cole o CSS de cada bloco ou mantenha `components/home/msn-home.css` como CSS unico.

O bloco `04-featured-products` usa:

```html
<div data-msn-products data-msn-query='{"per_page":8,"orderby":"date","order":"DESC"}'></div>
```

Produto simples recebe CTA por URL nativa do WooCommerce. Produto variavel ou agrupado recebe CTA para a pagina do produto, onde o WooCommerce escolhe atributos corretamente.

## Depois de publicar

1. Elementor > Ferramentas > Regenerar CSS e Dados.
2. Limpar cache do WP Rocket.
3. Testar em aba anonima.
4. Validar busca, contador do carrinho, produtos da Home e CTA de produto variavel.
