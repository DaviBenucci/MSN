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
4. `00-header.js` no Head, footer ou Custom Code do template

O arquivo `04-mobile-drawer.html` foi desativado de proposito. A navegacao mobile usa a mesma quickbar do desktop para evitar links duplicados e facilitar manutencao.

O script do header aguarda o DOM e tambem observa reinjecoes do Elementor. Ele apenas controla o estado compacto do header no scroll.

O contador do carrinho depende do plugin `msn-woocommerce-layout-bridge` ativo.

## Busca de produtos WooCommerce

A busca do header nao deve ser recriada manualmente no widget HTML. Ela deve usar a busca nativa do WooCommerce por meio do shortcode da ponte:

```txt
[msn_product_search]
```

Use o `02-main.html` como estrutura e coloque um unico widget **Shortcode** dentro do espaco com a classe `msn-header__search-slot`.

O shortcode renderiza `get_product_search_form()` do WooCommerce, mantendo `post_type=product` e a compatibilidade com traducoes, tema e plugins. O arquivo `02-main.css` estiliza o formulario gerado pelo WooCommerce para desktop e mobile.

Se estiver montando tudo com containers do Elementor, a ordem ideal no header principal e:

1. Logo
2. Container `msn-header__search-slot` com o shortcode `[msn_product_search]`
3. Links de conta, pedidos e carrinho

A quickbar (`03-quickbar.html`) e a navegacao principal em desktop e mobile. Para alterar categorias, WhatsApp ou atalhos, edite somente esse arquivo.
