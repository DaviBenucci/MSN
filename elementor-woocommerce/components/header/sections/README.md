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

No mobile, a navegacao principal usa somente a quickbar com atalhos essenciais.

O script do header aguarda o DOM e tambem observa reinjecoes do Elementor. Ele apenas controla o estado compacto do header no scroll.

O contador do carrinho depende do plugin `msn-woocommerce-layout-bridge` ativo.

## Responsividade mobile obrigatoria

O header e area critica de mobile. Antes de aprovar qualquer alteracao, siga `../../../docs/MOBILE-FIRST-RESPONSIVIDADE.md` e valide:

- 320px sem rolagem horizontal.
- 360px com logo, carrinho, busca e quickbar sem corte.
- 375px, 390px, 412px e 430px com busca funcional, carrinho e atalhos tocaveis.
- 768px, 820px e 1024px sem quebra de layout intermediario.
- Quickbar mobile com Especialista, Mais Vendidos, Novidades, Minha Conta, Contato e Visite nosso outro site.
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
3. Links de conta, pedidos e carrinho

A quickbar (`03-quickbar.html`) organiza categorias, WhatsApp e atalhos comerciais no desktop. No mobile, ela mostra somente os atalhos essenciais definidos no proprio `03-quickbar.html`.
