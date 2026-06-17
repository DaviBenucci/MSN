# Finalizacao de compra em containers

Use estes blocos na ordem:

1. `01-hero.html` + `01-hero.css`
2. `02-checkout-slot.html` + `02-checkout-slot.css`
3. `03-checkout-woocommerce.css`

## Separacao dos CSS

Para facilitar manutencao, o checkout esta separado em duas camadas:

- `02-checkout-slot.css`: cuida somente da estrutura HTML criada no Elementor, como container principal, slot do WooCommerce e cards laterais.
- `03-checkout-woocommerce.css`: cuida somente dos elementos que o WooCommerce, WooCommerce Blocks ou plugin de checkout em etapas geram dentro de `msn-checkout-woo-slot`.

Cole `03-checkout-woocommerce.css` depois de `02-checkout-slot.css`, porque ele precisa sobrescrever estilos nativos do WooCommerce e do plugin de checkout.

## Como montar o slot WooCommerce no Elementor

Nao e possivel colocar o widget Checkout ou um widget Shortcode dentro de um widget HTML ja colado. O comentario dentro de `02-checkout-slot.html` e apenas uma referencia visual.

Para montar corretamente:

1. Crie um Container principal com as classes:

```text
msn-checkout-content msn-section
```

2. Dentro dele, crie um Container interno com as classes:

```text
msn-container msn-checkout-content__grid
```

3. Dentro do grid, crie um Container para o WooCommerce com a classe:

```text
msn-checkout-woo-slot
```

4. Dentro desse Container, insira um widget nativo **Checkout** ou um widget **Shortcode** com:

```text
[woocommerce_checkout]
```

5. Ao lado do slot, adicione a sidebar visual com a classe:

```text
msn-checkout-side
```

Regra: dados do cliente, endereco, frete, pagamento, cupons, totais e validacoes devem continuar vindo do WooCommerce e dos gateways instalados. O HTML/CSS deste kit apenas cria a moldura visual.
