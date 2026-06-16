# Carrinho em containers

Use estes blocos na ordem:

1. `01-hero.html` + `01-hero.css`
2. `02-cart-slot.html` + `02-cart-slot.css` + `02-cart-slot.js`
3. `03-empty-state.html` + `03-empty-state.css`

## Como montar o slot WooCommerce no Elementor

Nao e possivel colocar o widget Cart ou um widget Shortcode dentro de um widget HTML ja colado. O comentario dentro de `02-cart-slot.html` e apenas uma referencia visual de onde o conteudo vivo deve ficar.

Para montar corretamente:

1. Crie um Container principal com as classes:

```text
msn-cart-content msn-section
```

2. Dentro dele, crie um Container interno com as classes:

```text
msn-container msn-cart-content__grid
```

3. Dentro do grid, crie um Container para o WooCommerce com a classe:

```text
msn-cart-woo-slot
```

4. Dentro desse Container, insira um widget nativo **Cart** ou um widget **Shortcode** com:

```text
[woocommerce_cart]
```

5. Ao lado do slot, adicione o bloco visual da sidebar com a classe:

```text
msn-cart-sidebar
```

Regra: carrinho, cupom, frete, totais e checkout devem continuar vindo do WooCommerce. O HTML/CSS deste kit apenas cria a moldura visual ao redor desses dados.
