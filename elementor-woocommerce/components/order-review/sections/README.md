# Avalie seu pedido em containers

Use estes blocos na ordem:

1. `01-hero.html` + `01-hero.css`
2. `02-review-form.html` + `02-review-form.css` + `02-review-form.js`
3. `03-guidelines.html` + `03-guidelines.css`

Esta pagina nao consulta pedidos no WooCommerce e nao grava dados no banco. O formulario organiza a mensagem e abre o WhatsApp oficial da MSN Distribuidora.

Slug sugerido:

```text
/avalie-seu-pedido/
```

Se futuramente a loja instalar um plugin de avaliacoes pos-compra, substitua o formulario por um widget/shortcode do plugin dentro de um Container com a classe `msn-review-form-slot`.
