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

O drawer mobile inclui links para carrinho, finalizacao de compra, minha conta, avalie seu pedido, trocas/devolucoes e privacidade. Crie essas paginas antes de publicar o menu definitivo.
