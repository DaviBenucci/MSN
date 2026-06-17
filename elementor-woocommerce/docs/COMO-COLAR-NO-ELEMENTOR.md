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

Evite colar CSS de uma section inteira dentro do painel de CSS personalizado de um unico widget, como **Editar Shortcode > Avancado > CSS personalizado**. Esse campo pertence ao widget atual e pode confundir o escopo do estilo. Para slots WooCommerce, coloque o CSS da section no nivel da pagina/template ou no CSS global.

Alguns editores do Elementor exibem avisos em funcoes modernas como `var(...)`, `clamp(...)` ou `color-mix(...)`. Quando o site esta com `shared/msn-global-css.html` carregado, esses avisos normalmente sao apenas do validador visual do editor. Se a formatacao nao aplicar, confira primeiro se o CSS global foi carregado antes da section e se o Container tem a classe esperada.

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
[woocommerce_checkout]
[woocommerce_my_account]
```

Evite colar shortcode em widget HTML.

## Widgets dentro de slots

O Elementor nao permite inserir um widget WooCommerce dentro de um widget HTML ja colado. Quando um arquivo deste kit mostrar um comentario como:

```html
<!-- Elementor: recriar este slot como Container e inserir dentro dele o widget Cart ou Shortcode com [woocommerce_cart]. -->
```

isso significa: recrie essa parte com Containers do Elementor e coloque o widget WooCommerce como filho real do Container marcado.

Padrao recomendado:

1. Use o HTML widget para blocos visuais estaticos.
2. Use Container do Elementor para wrappers como `msn-cart-woo-slot`, `msn-checkout-woo-slot`, `msn-account-woo-slot`, `msn-shop__woo-slot` e `msn-product-add-to-cart-slot`.
3. Use widget Shortcode ou widget WooCommerce dentro desse Container.
4. Cole o CSS da section na pagina/template ou no CSS global indicado.

Exemplo para Minha Conta:

```text
Container: msn-account-content msn-section
  Container: msn-container
    Container: msn-account-woo-slot
      Widget Shortcode: [woocommerce_my_account]
```

Exemplo para Carrinho:

```text
Container: msn-cart-content msn-section
  Container: msn-container msn-cart-content__grid
    Container: msn-cart-woo-slot
      Widget Shortcode: [woocommerce_cart]
    Container/HTML: msn-cart-sidebar
```

Exemplo para Finalizacao de Compra:

```text
Container: msn-checkout-content msn-section
  Container: msn-container msn-checkout-content__grid
    Container: msn-checkout-woo-slot
      Widget Shortcode: [woocommerce_checkout]
    Container/HTML: msn-checkout-side
```

CSS da Finalizacao de Compra:

```text
01-hero.css
02-checkout-slot.css
03-checkout-woocommerce.css
```

O `02-checkout-slot.css` estiliza a estrutura HTML/Elementor. O `03-checkout-woocommerce.css` deve vir depois e estiliza somente o que o WooCommerce ou o plugin de checkout em etapas renderiza dentro de `msn-checkout-woo-slot`.

## Produtos dinamicos

Para listar produtos:

- Use Loop Grid do tipo `Products`.
- Use Products/Archive Products widget.
- Use shortcode `[products]`.

O HTML widget nao tem acesso automatico a imagem, preco, estoque, variacao ou botao de compra.
