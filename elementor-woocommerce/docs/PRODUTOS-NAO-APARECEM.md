# Diagnostico: produtos nao aparecem

Use esta ordem para encontrar o problema sem mexer no checkout ou no banco.

## 1. Teste minimo com shortcode

Crie uma pagina de teste e insira um widget Shortcode com:

```text
[products limit="12" columns="3" visibility="visible"]
```

Resultado esperado:

- Se aparecer produto, WooCommerce esta entregando produtos.
- Se nao aparecer, revisar status, visibilidade, categoria e cache.

## 2. Confirmar widget correto

Nao use widget HTML para shortcode.

Use:

- Widget Shortcode para `[products]`.
- Widget Products/Archive Products.
- Loop Grid com template tipo `Products`.

## 3. Confirmar Loop Grid

No Elementor Pro:

- Template type precisa ser `Products`.
- Em loja/categoria/busca, Source deve ser `Current Query`.
- Nao usar template tipo `Posts` para produto.

## 4. Confirmar produto no WooCommerce

Em Produtos > Todos os produtos, conferir:

- Produto publicado.
- Visibilidade do catalogo: loja e resultados de pesquisa.
- Preco preenchido.
- Estoque configurado ou produto compravel.
- Categoria atribuida.
- Imagem destacada quando possivel.

## 5. Isolar filtro WBW

Temporariamente remova o widget Woofilters ou shortcode do filtro.

- Se produtos voltarem, o filtro esta restringindo demais a query.
- Recrie filtro usando categorias e atributos existentes.
- Evite filtro por atributo que quase nenhum produto possui.

## 6. Limpar cache

Depois de alterar template ou CSS:

1. Elementor > Ferramentas > Regenerar CSS e Dados.
2. WP Rocket > Limpar cache.
3. Navegador em aba anonima.

## 7. O que nao fazer

- Nao criar cards de produto estaticos no HTML widget para venda real.
- Nao inserir preco fixo em HTML.
- Nao criar botao falso de compra.
- Nao tentar puxar variaveis WooCommerce via JavaScript no front-end.

