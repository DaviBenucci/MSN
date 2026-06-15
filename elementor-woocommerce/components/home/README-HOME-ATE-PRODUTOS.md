# Home ate Produtos em destaque

Arquivos:

- `msn-home-ate-produtos.html`
- `msn-home-ate-produtos.css`

## Como usar no Elementor

1. Cole o HTML em um widget HTML.
2. Cole o CSS em CSS adicional da pagina ou do site.
3. Logo abaixo do bloco HTML, adicione o widget Products do Elementor Pro ou um widget Shortcode.
4. No wrapper do widget de produtos, adicione a classe:

```text
msn-product-card-model
```

5. Cole tambem o CSS:

```text
components/product-card/msn-product-card.css
```

## Shortcode de teste

Use em widget Shortcode:

```text
[products limit="4" columns="4" visibility="featured"]
```

Se nao aparecer produto destacado, teste:

```text
[products limit="4" columns="4" visibility="visible"]
```

