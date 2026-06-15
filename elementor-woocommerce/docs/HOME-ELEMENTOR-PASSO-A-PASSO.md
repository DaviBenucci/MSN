# Home no Elementor - passo a passo

Objetivo da Home:

> Fazer o cliente entender rapidamente que a MSN vende impressoras, toners, cartuchos e suprimentos, consegue ajudar na compatibilidade e permite compra pela loja com suporte no WhatsApp.

## Estrutura recomendada

1. Hero comercial.
2. Barra de beneficios.
3. Produtos em destaque.
4. Categorias principais.
5. Bloco de ajuda por WhatsApp.
6. Bloco de confianca.

## Arquivos prontos ate a parte 3

Use estes arquivos para montar a Home ate a area de produtos:

- `components/home/msn-home-ate-produtos.html`
- `components/home/msn-home-ate-produtos.css`
- `components/home/README-HOME-ATE-PRODUTOS.md`

Eles incluem:

- Hero comercial.
- Barra de beneficios.
- Cabecalho da secao Produtos em destaque.
- Aviso/slot para voce inserir o widget Products ou Shortcode do WooCommerce.

## 1. Hero comercial

Tipo: Manual Elementor.

Container:

- Classe: `msn-home-hero`
- Largura do conteudo: 1180px.
- Desktop: 2 colunas.
- Mobile: 1 coluna.
- Fundo: `#f8fafc` ou azul muito claro.

Conteudo sugerido:

Titulo:

```text
Suprimentos de impressao com compra simples e atendimento especializado.
```

Texto:

```text
Encontre impressoras, toners, cartuchos e itens de reposicao com apoio para confirmar compatibilidade antes da compra.
```

Botoes:

- `Ver produtos` apontando para `/loja/`.
- `Falar no WhatsApp` apontando para `https://wa.me/551134393836`.

Imagem:

- Usar imagem real de impressora, toner ou composicao de produtos.
- Evitar imagem escura ou generica.

## 2. Barra de beneficios

Tipo: Manual Elementor.

Criar 4 cards pequenos:

- Atendimento especializado.
- Compra segura.
- Estoque visivel.
- Entrega/frete conforme calculo no carrinho.

Texto curto. Evite paragrafos grandes.

## 3. Produtos em destaque

Tipo: Dinamico WooCommerce.

Esta e a secao mais importante para comecar a vender.

### Configuracao recomendada

No WooCommerce:

1. Va em `Produtos > Todos os produtos`.
2. Marque como destaque os produtos que devem aparecer na Home.
3. Use a estrela de destaque do WooCommerce.
4. Confirme que os produtos estao publicados, com preco e visibilidade de catalogo ativa.

No Elementor:

1. Crie um container para a secao.
2. Adicione titulo: `Produtos em destaque`.
3. Adicione subtitulo curto: `Itens selecionados para compra rapida e reposicao.`
4. Insira widget `Products` do Elementor Pro.
5. Configure Query para produtos em destaque.
6. Colunas:
   - Desktop: 4.
   - Tablet: 2.
   - Mobile: 1.
7. Limite inicial: 4 produtos.
8. Ative imagem, titulo, preco e botao de compra.
9. No container externo do widget, adicione a classe:

```text
msn-product-card-model
```

10. Cole o CSS de `components/product-card/msn-product-card.css` no CSS adicional da pagina ou do site.

### Alternativa com shortcode

Use widget Shortcode, nao widget HTML:

```text
[products limit="4" columns="4" visibility="featured"]
```

Se nao aparecer nada, use o teste minimo:

```text
[products limit="4" columns="4" visibility="visible"]
```

Se o teste minimo aparecer e featured nao aparecer, o problema e que nenhum produto foi marcado como destaque.

## 4. Categorias principais

Tipo: Manual Elementor.

Criar 4 cards:

- Impressoras.
- Toners.
- Cartuchos.
- Sulfite.

Cada card aponta para a URL real da categoria:

- `/categoria-produto/impressora/`
- `/categoria-produto/toner/`
- `/categoria-produto/cartucho/`
- `/categoria-produto/sulfite/`

## 5. Bloco WhatsApp

Tipo: Manual Elementor.

Titulo:

```text
Nao sabe qual toner ou cartucho comprar?
```

Texto:

```text
Envie o modelo da impressora para nossa equipe confirmar a compatibilidade antes do pedido.
```

Botao:

```text
Falar com especialista
```

Link:

```text
https://wa.me/551134393836?text=Ola!%20Quero%20confirmar%20compatibilidade%20de%20um%20produto.
```

## 6. Bloco de confianca

Tipo: Manual Elementor.

Itens:

- CNPJ visivel.
- Endereco/atendimento em Diadema-SP.
- Telefone e e-mail.
- Politica de troca e privacidade.
- Compra processada pelo WooCommerce.

## Estetica recomendada

- Fundo geral claro.
- Cards brancos ou levemente rosados, como no modelo visual enviado.
- Azul forte para botoes de compra.
- Verde apenas para WhatsApp.
- Bordas discretas.
- Sombra moderada.
- Pouco texto nos cards.

## Ordem de validacao

1. O produto aparece no widget?
2. A imagem esta boa?
3. O titulo quebra bem no mobile?
4. O preco aparece?
5. O botao comprar funciona?
6. O WhatsApp abre?
7. O layout fica bom em 375px?
