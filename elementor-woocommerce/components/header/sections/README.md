# Header em sections

Para manutencao por containers, crie um container pai no Elementor com:

```text
Classe CSS: msn-header
Atributo: data-msn-header
Role: banner, se o Elementor permitir
```

Depois insira os blocos nesta ordem:

1. `01-topbar.html` + `01-topbar.css`
2. `02-main.html` + `02-main.css`
3. `03-quickbar.html` + `03-quickbar.css`
4. `04-mobile-drawer.html` + `04-mobile-drawer.css`
5. `00-header.js` no footer ou Custom Code do template

O contador do carrinho depende do plugin `msn-woocommerce-layout-bridge` ativo.

## Busca de produtos WooCommerce

A busca do header nao deve ser recriada manualmente no widget HTML. Ela deve usar a busca nativa do WooCommerce por meio do shortcode da ponte:

```txt
[msn_product_search]
```

No desktop, use o `02-main.html` como estrutura e coloque um widget **Shortcode** dentro do espaco com a classe `msn-header__search-slot`.

No mobile, coloque outro widget **Shortcode** dentro do espaco com a classe `msn-header__drawer-search`, logo abaixo do cabecalho do drawer.

O shortcode renderiza `get_product_search_form()` do WooCommerce, mantendo `post_type=product` e a compatibilidade com traducoes, tema e plugins. Os arquivos `02-main.css` e `04-mobile-drawer.css` apenas estilizam o formulario gerado pelo WooCommerce.

Se estiver montando tudo com containers do Elementor, a ordem ideal no header principal e:

1. Logo
2. Container `msn-header__search-slot` com o shortcode `[msn_product_search]`
3. Links de conta, pedidos e carrinho

O drawer mobile inclui links para carrinho, finalizacao de compra, minha conta, avalie seu pedido, trocas/devolucoes e privacidade. Crie essas paginas antes de publicar o menu definitivo.
