# Loja, categorias e busca em containers

Use estes blocos na ordem:

1. `01-hero-search.html` + `01-hero-search.css`
2. `02-products-layout.html` + `02-products-layout.css` + `02-products-layout.js`

## Como montar os slots WooCommerce no Elementor

Nao e possivel colocar um widget de filtro, Products, Archive Products, Loop Grid ou Shortcode dentro de um widget HTML ja colado. Os comentarios dentro de `02-products-layout.html` sao apenas referencias visuais.

Para montar corretamente:

1. Crie um Container principal com a classe:

```text
msn-shop-layout
```

2. Dentro dele, crie um Container interno com as classes:

```text
msn-container msn-shop-layout__grid
```

3. No lado de filtros, crie um Container com a classe:

```text
msn-shop-filter__plugin-slot
```

Dentro dele, insira o widget **Woofilters** do WBW ou um widget **Shortcode** com o shortcode copiado do plugin de filtros.

4. No lado de produtos, crie um Container com as classes:

```text
msn-shop__woo-slot msn-product-card-model
```

Dentro dele, insira um destes recursos vivos:

```text
Loop Grid tipo Products
Products/Archive Products widget
[products limit="12" columns="3" paginate="true" visibility="visible"]
```

Regra: filtros, paginacao, ordenacao, preco, estoque, imagem e botao de compra devem continuar vindo do WooCommerce, Elementor Pro ou plugin de filtro.
