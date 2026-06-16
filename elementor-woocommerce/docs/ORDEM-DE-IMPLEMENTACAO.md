# Ordem de implementacao recomendada

## Fase 1 - Base global

- Instalar `msn-global.css`.
- Instalar `msn-global.js`.
- Conferir fonte, cores, botoes e estilos WooCommerce basicos.

## Fase 2 - Estrutura global

- Publicar header.
- Publicar footer.
- Testar menu mobile e sanfonas do footer.
- Confirmar links de conta, pedidos, carrinho, finalizacao de compra, avalie seu pedido, politicas e WhatsApp.

## Fase 3 - Paginas comerciais

- Publicar home.
- Publicar loja/categorias/busca usando Loop Grid tipo `Products`, Products/Archive Products widget ou shortcode `[products]`.
- Aplicar `components/product-card/msn-product-card.css` no wrapper do grid.
- Publicar produto unico.
- Conferir produtos, imagens, precos, estoque e CTAs.

## Fase 4 - Fluxo de compra

- Publicar carrinho.
- Publicar finalizacao de compra com widget Checkout ou `[woocommerce_checkout]`.
- Revisar checkout sem substituir a logica nativa.
- Testar cupom, frete, quantidade e finalizacao.

## Fase 5 - Area do cliente e contato

- Publicar Minha Conta.
- Publicar Contato.
- Publicar Avalie seu pedido.
- Testar login, recuperacao de senha e formulario WhatsApp.

## Fase 6 - Paginas legais

- Publicar Politica de Privacidade.
- Publicar Trocas e Devolucoes.
- Validar textos legais com responsavel juridico/administrativo.

## Fase 7 - Catalogo

- Corrigir categorias.
- Preencher SKU.
- Adicionar imagens e alt text.
- Padronizar marcas e atributos.
- Revalidar filtros.

## Rotina apos cada alteracao no Elementor

- Salvar template.
- Regenerar CSS e Dados no Elementor.
- Limpar cache do WP Rocket.
- Testar em aba anonima.
- Se produtos sumirem, testar shortcode minimo `[products limit="12" columns="3" visibility="visible"]` sem filtros.
