# Home no Elementor - passo a passo

Objetivo da Home:

> Fazer o cliente entender rapidamente que a MSN vende impressoras, toners, cartuchos e suprimentos, consegue ajudar na compatibilidade e permite compra pela loja com suporte no WhatsApp.

## Estrutura oficial

Use somente:

```text
components/home/sections/
```

Ordem de montagem:

1. `01-hero`
2. `02-benefits`
3. `03-categories`
4. `04-featured-products`
5. `05-help`

O CSS pode ser colado por section ou reunido no CSS da pagina. O JS `00-smooth-scroll.js` e opcional e so deve ser usado se houver links internos com ancora.

## 1. Hero comercial

Arquivo:

```text
components/home/sections/01-hero.html
components/home/sections/01-hero.css
```

Tipo: Manual Elementor.

Conteudo:

- Chamada comercial direta.
- CTAs para loja, WhatsApp e toner.
- Imagem real de impressora/produto.

## 2. Barra de beneficios

Arquivo:

```text
components/home/sections/02-benefits.html
components/home/sections/02-benefits.css
```

Tipo: Manual Elementor.

Beneficios:

- Atendimento consultivo.
- Compra segura.
- Estoque visivel.
- Venda B2B e B2C.

## 3. Categorias principais

Arquivo:

```text
components/home/sections/03-categories.html
components/home/sections/03-categories.css
```

Tipo: Manual Elementor.

Categorias iniciais:

- Impressoras.
- Toners.
- Cartuchos.
- Novidades.

## 4. Produtos em destaque

Arquivo:

```text
components/home/sections/04-featured-products.html
components/home/sections/04-featured-products.css
```

Tipo: Dinamico via bridge WooCommerce.

O bloco usa:

```html
<div class="msn-home__woo-slot" data-msn-products data-msn-query='{"per_page":8,"orderby":"date","order":"DESC"}'></div>
```

Produto simples recebe CTA por URL nativa do WooCommerce. Produto variavel ou agrupado recebe CTA para a pagina do produto para escolha correta das opcoes.

Fallback, se necessario:

- Widget Products do Elementor Pro.
- Loop Grid tipo Products.
- Widget Shortcode com `[products]`.

## 5. Ajuda por WhatsApp

Arquivo:

```text
components/home/sections/05-help.html
components/home/sections/05-help.css
```

Tipo: Manual Elementor.

Objetivo:

- Resolver duvida de compatibilidade.
- Reforcar atendimento consultivo.
- Dar uma alternativa para quem nao encontrou o produto.

## Ordem de validacao

1. O hero carrega sem quebra no mobile.
2. Os beneficios ficam legiveis em 375px.
3. As categorias apontam para URLs reais.
4. A bridge renderiza produtos na section 04.
5. Produto variavel abre a pagina do produto, nao adiciona direto.
6. WhatsApp abre com mensagem correta.
7. Nao existem arquivos combinados antigos fora de `sections`.
