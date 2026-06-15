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

## Card montado manualmente no Elementor

Use classes no campo `Avancado > CSS Classes`. E melhor que ID porque permite repetir o card.

| Parte no Elementor | Classe recomendada | ID opcional | Variavel/dynamic tag |
|---|---|---|---|
| Container geral do card | `msn-product-card` | `msn-card-produto` | Nenhuma |
| Imagem do produto | `msn-product-card__image` | `msn-card-imagem` | `Product Image` ou `Featured Image` do produto |
| Nome/titulo | `msn-product-card__title` | `msn-card-nome` | `Product Title` ou `Post Title` em Loop Product |
| Preco | `msn-product-card__price` | `msn-card-preco` | Widget `Product Price` |
| Botao comprar | `msn-product-card__button` | `msn-card-botao` | Widget `Add To Cart` |

Texto do botao:

```text
Compre Agora
```

Se o botao permitir icone, use o icone de `+` pelo Elementor. Se nao usar icone, o CSS ja adiciona o sinal `+` antes do texto.

## Estrutura ideal dentro do card

1. Container principal com classe `msn-product-card`.
2. Widget de imagem com classe `msn-product-card__image`.
3. Widget titulo com classe `msn-product-card__title`.
4. Widget preco com classe `msn-product-card__price`.
5. Widget Add To Cart com classe `msn-product-card__button`.

Observacao: se voce estiver dentro de um Loop Item do tipo Products, use as dynamic tags do produto atual. Se estiver fora de loop, selecione manualmente o produto no widget WooCommerce quando o Elementor permitir.

## CSS direto no Container do Loop Item

Se voce estiver editando o template `Card de produto` no Theme Builder, selecione o container principal do card e cole este arquivo no painel:

```text
components/product-card/msn-product-card-loop-item.css
```

Esse CSS usa `selector`, entao ele afeta apenas o card atual do Loop Item e nao mexe na pagina individual do produto.

Variaveis/widgets para colocar no card:

| Elemento | Widget Elementor | Conteudo dinamico |
|---|---|---|
| Imagem | Featured Image ou Product Image | Imagem do produto atual |
| Nome | Heading, Post Title ou Product Title | Titulo do produto atual |
| Preco | Product Price | Preco do WooCommerce |
| Botao | Add To Cart | Produto atual |

Texto recomendado do botao:

```text
Compre Agora
```

## Por que os produtos podem nao aparecer

- Loop Grid criado como `Posts`, nao `Products`.
- Query do Loop Grid sem source correto.
- Em arquivo de loja/categoria/busca, use `Current Query`.
- Produto sem status publicado.
- Produto sem visibilidade de catalogo.
- Cache do WP Rocket servindo CSS/HTML antigo.
- Filtro WBW aplicado sem produtos correspondentes.
