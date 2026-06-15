# Mapa de componentes

## Global

Arquivos:

- `shared/msn-global.css`
- `shared/msn-global.js`

Onde aplicar:

- CSS global do Elementor ou CSS adicional do tema.
- JS global no footer pelo Elementor Pro Custom Code.

## Header

Arquivos:

- `components/header/msn-header.html`
- `components/header/msn-header.css`
- `components/header/msn-header.js`
- `components/header/sections/*` para montagem por containers separados.

Onde aplicar:

- Elementor Theme Builder > Header.
- HTML em widget HTML.
- CSS no template do header ou CSS global.
- JS no footer, carregado em todo o site.

Funcoes:

- Busca nativa WooCommerce.
- Conta, pedidos e carrinho.
- Contador de carrinho usa `data-msn-cart-count` e e preenchido pela bridge.
- Categorias principais.
- WhatsApp consultivo.
- Menu mobile off-canvas.

## Footer

Arquivos:

- `components/footer/msn-footer.html`
- `components/footer/msn-footer.css`
- `components/footer/msn-footer.js`

Onde aplicar:

- Elementor Theme Builder > Footer.

Funcoes:

- Atendimento.
- Categorias.
- Politicas.
- CNPJ e endereco.
- Sanfonas mobile.

## Home

Arquivos:

- `components/home/msn-home.html`
- `components/home/msn-home.css`
- `components/home/msn-home.js`

Containers:

- Versao combinada: `components/home/msn-home.html`
- Versao por partes: `components/home/sections/01-hero` ate `05-help`

Dados WooCommerce:

- Produtos em destaque: preferir bridge `data-msn-products` com query `{"per_page":8,"orderby":"date","order":"DESC"}`.
- Fallback: widget Products ou shortcode `[products limit="8" columns="4" orderby="date" order="DESC"]`.

## Loja, categorias e busca

Arquivos:

- `components/shop/msn-shop.html`
- `components/shop/msn-shop.css`
- `components/shop/msn-shop.js`

Slots WooCommerce:

- Recomendado: Loop Grid com template do tipo `Products` e Source = `Current Query` em loja/categorias/busca.
- Alternativa: widget Products/Archive Products ou Shortcode com `[products limit="12" columns="3" paginate="true" visibility="visible"]`.
- Filtros: usar widget Woofilters do WBW ou shortcode copiado do plugin. Nao usar formularios manuais.

## Card de produto

Arquivos:

- `components/product-card/msn-product-card.css`
- `components/product-card/README.md`

Onde aplicar:

- CSS adicional da pagina/template.
- Classe `msn-product-card-model` no wrapper do Loop Grid, Products widget ou shortcode.

Funcoes:

- Aproxima o card do modelo visual aprovado: imagem grande, titulo azul, preco destacado e botao arredondado azul.
- Nao cria produto dinamico sozinho; apenas estiliza markup gerado pelo WooCommerce/Elementor.

## Produto

Arquivos:

- `components/product/msn-product.html`
- `components/product/msn-product.css`
- `components/product/msn-product.js`

Slots WooCommerce:

- Product Images.
- Product Title.
- Product Price.
- Stock ou Product Meta.
- Add To Cart.
- Product Data Tabs.
- Product Content.
- Related Products/Upsells.

## Carrinho

Arquivos:

- `components/cart/msn-cart.html`
- `components/cart/msn-cart.css`
- `components/cart/msn-cart.js`

Slot WooCommerce:

- Shortcode `[woocommerce_cart]` ou widget Cart.

## Minha Conta

Arquivos:

- `components/account/msn-account.html`
- `components/account/msn-account.css`
- `components/account/msn-account.js`

Slot WooCommerce:

- Shortcode `[woocommerce_my_account]` ou widget My Account.

## Contato

Arquivos:

- `components/contact/msn-contact.html`
- `components/contact/msn-contact.css`
- `components/contact/msn-contact.js`

Funcoes:

- Canais oficiais.
- Formulario com honeypot simples.
- Abertura de WhatsApp com mensagem organizada.
