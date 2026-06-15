# Fluxo de trabalho no Elementor

Este projeto sera feito em conjunto, por blocos. A regra agora e simples:

- O que for visual, institucional ou comercial pode ser montado manualmente no Elementor.
- O que depender de produto, preco, estoque, carrinho, conta, pedido, filtro ou checkout deve vir do WooCommerce, Elementor Pro ou plugin especifico.

## Blocos manuais no Elementor

Use containers, titulos, textos, botoes, imagens e icones do Elementor para:

- Hero da Home.
- Beneficios.
- Categorias comerciais.
- CTA de WhatsApp.
- Blocos de confianca.
- Contato.
- Areas institucionais.
- Conteudo de apoio para SEO.

Esses blocos nao precisam conversar com o WooCommerce.

## Blocos dinamicos

Use widgets nativos para:

- Produtos em destaque.
- Lista de produtos.
- Produto unico.
- Preco.
- Estoque.
- Botao comprar.
- Carrinho.
- Minha conta.
- Checkout.
- Filtros.

Nao recriar essas partes em HTML manual.

## Como vamos trabalhar pagina por pagina

1. Definir o objetivo da pagina.
2. Dividir a pagina em secoes.
3. Marcar cada secao como `Manual Elementor` ou `Dinamica WooCommerce`.
4. Montar visualmente no Elementor.
5. Aplicar classes CSS apenas onde precisar acabamento.
6. Testar desktop, tablet e mobile.
7. Limpar cache e validar em aba anonima.

## Padrao de classes

Use classes apenas quando precisar estilizar:

- `msn-home-hero`
- `msn-home-benefits`
- `msn-home-featured`
- `msn-product-card-model`
- `msn-whatsapp-cta`

Evite criar classe para tudo. Quanto menos CSS customizado, mais facil manter.

