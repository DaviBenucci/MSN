# Card de produto MSN

Este componente define o modelo visual dos produtos mostrado na referencia enviada.

## Regra mais importante

O HTML widget nao consegue puxar produto, preco, imagem ou botao de compra sozinho. Para produtos aparecerem dinamicamente, use uma destas opcoes:

1. Elementor Pro Loop Grid com template do tipo `Products`.
2. Elementor Pro Products ou Archive Products widget.
3. Widget Shortcode com shortcode WooCommerce, por exemplo:

```text
[products limit="12" columns="3" paginate="true" visibility="visible"]
```

## Loop Grid recomendado

No Elementor:

1. Crie um Loop Item do tipo `Products`.
2. Dentro do card, use widgets dinamicos:
   - Product Image.
   - Product Title.
   - Product Price.
   - Add To Cart.
3. No container externo do Loop Grid, adicione a classe:

```text
msn-product-card-model
```

4. Cole `msn-product-card.css` no CSS adicional da pagina ou do site.

## Por que os produtos podem nao aparecer

- Loop Grid criado como `Posts`, nao `Products`.
- Query do Loop Grid sem source correto.
- Em arquivo de loja/categoria/busca, use `Current Query`.
- Produto sem status publicado.
- Produto sem visibilidade de catalogo.
- Cache do WP Rocket servindo CSS/HTML antigo.
- Filtro WBW aplicado sem produtos correspondentes.

