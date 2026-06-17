# Minha Conta em containers

Use estes blocos na ordem:

1. `01-hero.html` + `01-hero.css`
2. `02-account-slot.html` + `02-account-slot.css` + `02-account-slot.js`
3. `03-help.html` + `03-help.css`

## Como montar o slot WooCommerce no Elementor

Nao e possivel colocar o widget My Account ou um widget Shortcode dentro de um widget HTML ja colado. O comentario dentro de `02-account-slot.html` e apenas uma referencia visual de onde o conteudo vivo deve ficar.

Para montar corretamente:

1. Crie um Container principal com as classes:

```text
msn-account-content msn-section
```

2. Dentro dele, crie um Container interno com a classe:

```text
msn-container
```

3. Dentro desse Container, crie um Container para o WooCommerce com a classe:

```text
msn-account-woo-slot
```

4. Dentro desse slot, insira um widget nativo **My Account** ou um widget **Shortcode** com:

```text
[woocommerce_my_account]
```

Regra: login, cadastro, recuperacao de senha, pedidos, enderecos e dados da conta devem continuar vindo do WooCommerce. O HTML/CSS deste kit apenas cria a moldura visual ao redor desses dados.

## Menu dos endpoints

O arquivo `02-account-slot.js` melhora o menu da area Minha Conta sem alterar as URLs do WooCommerce. Ele adiciona:

- `aria-current="page"` no endpoint ativo.
- Numeracao visual nos links.
- Subtitulos curtos como "Historico e status", "Entrega e cobranca" e "Senha e dados pessoais".

Carregue este JS apenas na pagina Minha Conta, depois do shortcode ou no footer do template.

## Onde colar o CSS

Cole `02-account-slot.css` no CSS da pagina/template, no CSS global do Elementor ou em Aparencia > Personalizar > CSS adicional.

Evite colar este CSS dentro do painel **Editar Shortcode > CSS personalizado**. Esse painel pertence ao widget Shortcode e pode limitar o escopo do CSS, alem de exibir avisos em variaveis como `var(--msn-border)`. Esses avisos do editor nao significam, sozinhos, que o CSS esta invalido, mas a forma mais estavel e carregar:

1. `shared/msn-global-css.html` primeiro.
2. `01-hero.css`, `02-account-slot.css` e os CSS das sections usadas depois.
3. O shortcode `[woocommerce_my_account]` dentro de um Container com a classe `msn-account-woo-slot`.

Se no editor do Elementor a formatacao parecer parcial, confira se o shortcode esta realmente dentro de um Container com esta classe:

```text
msn-account-woo-slot
```
