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
5. `00-header.js` no Head, footer ou Custom Code do template

O `04-mobile-drawer.html` e o menu hamburger mobile para paginas principais, como Loja, Minha Conta, Carrinho e Contato. A quickbar continua ativa para categorias e atalhos comerciais.

O script do header aguarda o DOM e tambem observa reinjecoes do Elementor. Ele controla o estado compacto no scroll e o abre/fecha do menu mobile.

O contador do carrinho depende do plugin `msn-woocommerce-layout-bridge` ativo.

## Responsividade mobile obrigatoria

O header e area critica de mobile. Antes de aprovar qualquer alteracao, siga `../../../docs/MOBILE-FIRST-RESPONSIVIDADE.md` e valide:

- 320px sem rolagem horizontal.
- 360px com logo, carrinho, busca e quickbar sem corte.
- 375px, 390px, 412px e 430px com busca funcional, hamburger, carrinho e botoes tocaveis.
- 768px, 820px e 1024px sem quebra de layout intermediario.
- Menu hamburger abre/fecha por clique, Escape e botao Fechar.
- Quickbar com rolagem horizontal suave e primeiro item visivel.

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
3. Botao hamburger mobile, links de conta, pedidos e carrinho

A quickbar (`03-quickbar.html`) organiza categorias, WhatsApp e atalhos comerciais. O drawer (`04-mobile-drawer.html`) organiza as paginas principais no mobile.
