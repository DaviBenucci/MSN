# Como colar codigo no Elementor

## HTML widget

Use o HTML widget para estrutura visual pequena e scripts pontuais.

Formato:

```html
<section class="msn-exemplo">
	Conteudo HTML aqui
</section>

<style>
	.msn-exemplo {
		color: var(--msn-primary);
	}
</style>

<script>
	(function () {
		/* JS aqui */
	})();
</script>
```

## CSS adicional

Para CSS de pagina/template, prefira:

- Elementor > Pagina/template > Avancado > CSS personalizado.
- Aparencia > Personalizar > CSS adicional.
- Tema filho, se houver.

Nao precisa usar `<style>` quando estiver em campo exclusivo de CSS.

## JavaScript

Se estiver em widget HTML, sempre use:

```html
<script>
	/* codigo JS */
</script>
```

Se estiver em Elementor Pro > Custom Code, siga o formato exigido pela tela do proprio Elementor.

## Shortcodes WooCommerce

Shortcodes devem ir em widget Shortcode:

```text
[products limit="12" columns="3" paginate="true" visibility="visible"]
[woocommerce_cart]
[woocommerce_my_account]
```

Evite colar shortcode em widget HTML.

## Produtos dinamicos

Para listar produtos:

- Use Loop Grid do tipo `Products`.
- Use Products/Archive Products widget.
- Use shortcode `[products]`.

O HTML widget nao tem acesso automatico a imagem, preco, estoque, variacao ou botao de compra.

