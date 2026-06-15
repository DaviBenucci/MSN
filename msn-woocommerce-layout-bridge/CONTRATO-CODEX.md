# Contrato para Codex - MSN WooCommerce Layout Bridge

## Regra central

HTML/CSS/JS do Elementor nao deve tentar acessar `$product`, `WC()->cart`, `WC()->customer` ou variaveis PHP diretamente. O front-end deve consumir somente:

- `window.MSNWoo`
- `window.MSNWooLayout`
- containers `data-msn-products`
- shortcodes renderizados pelo PHP
- widgets/shortcodes nativos do WooCommerce para compra, carrinho, checkout e conta

## Renderer de vitrines

Use:

```html
<div data-msn-products data-msn-query='{"per_page":8,"orderby":"date","order":"DESC"}'></div>
```

O renderer chama `MSNWooLayout.api.getProducts()` e monta cards no front-end.

Campos principais por produto:

```js
product.id
product.type
product.name
product.sku
product.permalink
product.image.src
product.price.html
product.stock.label
product.actions.actionType
product.actions.ctaUrl
product.actions.ctaText
product.actions.requiresOptions
```

Tipos de acao:

- `simple_add_to_cart_url`: produto simples compravel; pode usar URL nativa do WooCommerce.
- `requires_options`: produto variavel/agrupado; sempre abrir pagina do produto.
- `view_product`: abrir pagina do produto.

## Carrinho

Para contador visual:

```html
<span data-msn-cart-count hidden></span>
```

O plugin atualiza texto, remove `hidden` e sincroniza apos eventos nativos do WooCommerce quando disponiveis.

## Dados que o JS nao deve pedir nem manipular

- Consumer key ou consumer secret do WooCommerce.
- Pedidos de outros usuarios.
- Dados administrativos.
- E-mail, telefone e endereco do cliente sem necessidade explicita.
- Calculo manual de preco, frete, cupom, imposto ou total.
- Checkout manual fora do WooCommerce.
- Seletor customizado de variacoes na Home v1.

## Orientacao de implementacao

- Header: usar busca nativa com `post_type=product`, links de conta/carrinho e contador `data-msn-cart-count`.
- Home: usar containers separados e `data-msn-products` para produtos em destaque.
- Loja/categoria/busca: preferir Loop Grid Products, Products/Archive Products ou shortcode `[products]` quando precisar de query nativa completa.
- Produto individual: usar widgets WooCommerce/Elementor para galeria, preco, estoque, variacoes e Add To Cart; complementar com `[msn_product_whatsapp]` e `[msn_product_data context="detail"]`.
- Carrinho: usar `[woocommerce_cart]` ou widget Cart e apenas estilizar.
- Checkout: usar `[woocommerce_checkout]` ou widget Checkout e apenas estilizar.
- Minha conta: usar `[woocommerce_my_account]` ou widget My Account e apenas estilizar.
