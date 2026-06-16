# Produto individual em containers

Use estes blocos na ordem:

1. `01-summary.html` + `01-summary.css`
2. `02-details.html` + `02-details.css`
3. `03-mobile-bar.html` + `03-mobile-bar.css` + `03-mobile-bar.js`
4. `04-related.html` + `04-related.css`

## Como montar os slots WooCommerce no Elementor

Nao e possivel colocar widgets de produto dentro de um widget HTML ja colado. Os comentarios nos arquivos `.html` sao referencias visuais para voce recriar a estrutura com Containers no template Single Product.

No template de produto unico, crie os Containers com as classes indicadas e coloque os widgets vivos como filhos reais desses Containers:

```text
msn-product-media-slot
```

Widget recomendado: Product Images/Gallery.

```text
msn-product-title-slot
```

Widget recomendado: Product Title.

```text
msn-product-price-slot
```

Widget recomendado: Product Price.

```text
msn-product-stock-slot
```

Widget recomendado: Product Meta, Stock ou bloco nativo equivalente do WooCommerce/Elementor.

```text
msn-product-add-to-cart-slot
```

Widget recomendado: Add To Cart. Este slot deve manter o `id`:

```text
msn-comprar-produto
```

Nas sections de detalhes:

```text
msn-product-attributes-slot
msn-product-description-slot
msn-product-related-slot
```

Use Product Data Tabs/Additional Information, Product Content/Description e Related Products/Upsells.

Regra: galeria, titulo, preco, estoque, variacoes, Add To Cart, descricao e relacionados devem continuar vindo do WooCommerce/Elementor. O HTML/CSS deste kit apenas cria a moldura visual.
