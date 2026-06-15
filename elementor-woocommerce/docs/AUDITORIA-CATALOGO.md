# Auditoria inicial de catalogo

Data da leitura: 2026-06-15.

Fonte publica consultada:

`https://msndistribuidora.com.br/wp-json/wc/store/v1/products`

## Resumo encontrado

- Produtos publicos retornados pela Store API: 477.
- Produtos sem SKU no retorno publico: 477.
- Produtos sem imagem no retorno publico: 455.
- Produtos com alguma imagem sem alt text: 18.
- Produtos sem marca: 2.
- Produtos sem atributos tecnicos: 475.
- Produtos fora de estoque: 0.
- Produtos com alerta de estoque baixo no retorno publico: 219.
- Categorias publicas: Cartucho, Impressora, Sem categoria, Sulfite, Toner.
- Categoria `Sem categoria` aparecia com 457 itens na listagem de categorias.

## Riscos

- Busca por codigo/SKU fica fraca se os SKUs nao estiverem preenchidos.
- Filtros tecnicos nao conseguem funcionar bem sem atributos padronizados.
- Produtos sem imagem reduzem confianca e conversao.
- Alt text vazio prejudica acessibilidade e SEO.
- Muitos itens com estoque baixo precisam de revisao de reposicao e regra comercial.
- A categoria `Sem categoria` indica necessidade de organizacao antes de filtros finais.

## Plano de saneamento

1. Definir categorias finais: Impressoras, Toners, Cartuchos, Tintas, Papel/Sulfite, Pecas e Acessorios, Ofertas.
2. Preencher SKU em todos os produtos.
3. Padronizar marcas: HP, Samsung, Brother, Canon, Epson e outras conforme catalogo.
4. Criar atributos WooCommerce para Marca, Cor, Compatibilidade, Tipo, Rendimento, Condicao, Validade e Disponibilidade.
5. Inserir imagem principal em todos os produtos vendaveis.
6. Preencher alt text com nome do produto, marca e codigo.
7. Revisar itens vencidos/usados e exibir essa condicao de forma transparente.
8. Configurar alerta de estoque baixo e limite maximo de compra quando houver poucas unidades.
9. Reindexar busca/filtros apos o saneamento.

