# Kit Elementor/WooCommerce - MSN Distribuidora

Este pacote implementa a reforma planejada para o e-commerce da MSN Distribuidora em arquivos separados para uso no WordPress, WooCommerce e Elementor Pro.

## Estrutura

- `shared/msn-global.css`: base visual, tokens, botoes, cards, formularios e ajustes seguros para WooCommerce.
- `shared/msn-global.js`: comportamentos reutilizaveis, sem alterar preco, frete, estoque, carrinho ou pagamento.
- `components/header`: header assistivo de compra.
- `components/footer`: footer de confianca e atendimento.
- `components/home`: secoes da home.
- `components/shop`: loja, busca, filtros e grid.
- `components/product-card`: modelo visual de card para Loop Grid, Products widget ou shortcode WooCommerce.
- `components/product`: template da tela de produto.
- `components/cart`: carrinho e carrinho vazio.
- `components/account`: minha conta.
- `components/contact`: contato e formulario para WhatsApp.
- `docs`: guia de instalacao, QA, compatibilidade de versoes, diagnostico de produtos e auditoria do catalogo.
- `docs/GUIA-CONTAINERS-HOME-HEADER.md`: montagem por containers separados para Home e Header usando a bridge.

## Como usar

1. Cadastre `shared/msn-global.css` no CSS global do Elementor ou em Aparencia > Personalizar > CSS adicional.
2. Para CSS especifico de pagina, cole o `.css` em CSS adicional da pagina/template.
3. Para HTML widget, cole HTML normalmente.
4. Se for colar CSS dentro do HTML widget, envolva com `<style>...</style>`.
5. Se for colar JS dentro do HTML widget, envolva com `<script>...</script>`.
6. Para areas WooCommerce, use widgets nativos do WooCommerce/Elementor ou widgets Shortcode nos pontos marcados nos arquivos HTML.

## Regras criticas

- Nao substituir checkout, carrinho, login, preco, estoque, frete ou pagamento por HTML manual.
- Nao usar JavaScript customizado para recalcular valores.
- Manter classes customizadas com prefixo `.msn-`.
- Testar primeiro em staging.
- Validar mobile antes de aprovar desktop.
- Os arquivos `.js` foram escritos em sintaxe ES5, sem `=>`, para evitar erro de caracteres especiais no editor do Elementor.
- Ao colar JS em um widget HTML, envolva o conteudo com `<script>...</script>`. No Elementor Pro Custom Code, use o padrao exigido pela propria tela.
- Produtos, preco, imagem, estoque e CTA devem vir da bridge `data-msn-products` ou de Loop Grid tipo `Products`, widget Products/Archive Products ou shortcode WooCommerce. O HTML widget sozinho nao puxa produtos sem a bridge.

## Fluxo novo de producao

Para construir as paginas em conjunto, use primeiro:

- `docs/FLUXO-DE-TRABALHO-ELEMENTOR.md`
- `docs/HOME-ELEMENTOR-PASSO-A-PASSO.md`
- `docs/GUIA-CONTAINERS-HOME-HEADER.md`
