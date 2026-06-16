# Kit Elementor/WooCommerce - MSN Distribuidora

Este pacote implementa a reforma planejada para o e-commerce da MSN Distribuidora em blocos separados para WordPress, WooCommerce e Elementor Pro.

## Estrutura

- `shared/msn-global.css`: base visual, tokens, botoes, cards, formularios e ajustes seguros para WooCommerce.
- `shared/msn-theme-init.js`: inicializacao do tema claro/escuro no Head, antes do CSS renderizar.
- `shared/msn-global.js`: tema, utilidades e comportamentos reutilizaveis, sem alterar preco, frete, estoque, carrinho ou pagamento.
- `components/*/sections`: blocos oficiais de cada pagina/template.
- `components/product-card`: modelo visual reutilizavel para Loop Grid, Products widget ou shortcode WooCommerce.
- `docs`: instalacao, mapa de componentes, QA, compatibilidade e limpeza do workspace.

## Regra principal

Paginas e templates devem ser montados por `sections`. Nao mantenha arquivos combinados antigos do tipo `msn-*.html`, `msn-*.css` ou `msn-*.js` fora das pastas de sections.

## Como usar

1. Cadastre `shared/msn-theme-init.js` no Head pelo Elementor Pro Custom Code.
2. Cadastre `shared/msn-global.css` no CSS global do Elementor ou em Aparencia > Personalizar > CSS adicional.
3. Cadastre `shared/msn-global.js` no footer pelo Elementor Pro Custom Code.
4. Para cada pagina, abra `components/<pagina>/sections/README.md`.
5. Cole os blocos `.html` na ordem indicada.
6. Cole os `.css` das sections usadas no template/pagina ou junto do widget HTML com `<style>`.
7. Carregue apenas os `.js` das sections presentes na pagina.
8. Para areas WooCommerce, use widgets nativos do WooCommerce/Elementor ou widget Shortcode nos slots marcados.

Importante: um widget WooCommerce ou Shortcode nao entra dentro de um widget HTML ja colado. Quando um arquivo `.html` mostrar um comentario de slot, recrie esse wrapper como Container do Elementor, aplique a classe do slot nele e coloque o widget WooCommerce/Shortcode como filho real desse Container.

## Regras criticas

- Nao substituir checkout, carrinho, login, preco, estoque, frete, pagamento ou variacoes por HTML manual.
- Nao colar `[woocommerce_cart]`, `[woocommerce_my_account]` ou `[products]` dentro de widget HTML; use widget Shortcode ou widget WooCommerce em um Container.
- Nao usar JavaScript customizado para recalcular valores.
- Manter classes customizadas com prefixo `.msn-`.
- Manter o seletor de tema com `data-msn-theme-toggle` e `data-msn-theme-choice`.
- Testar primeiro em staging.
- Validar mobile antes de aprovar desktop.
- Produtos, preco, imagem, estoque e CTA devem vir da bridge `data-msn-products` ou de Loop Grid tipo `Products`, widget Products/Archive Products ou shortcode WooCommerce.
- Checkout deve usar widget Checkout ou `[woocommerce_checkout]` em Container proprio, nunca HTML manual.
- Politica de privacidade e trocas/devolucoes devem ser revisadas pelo responsavel juridico/administrativo antes da publicacao.

## Documentos principais

- `docs/GUIA-DE-INSTALACAO.md`
- `docs/MAPA-DE-COMPONENTES.md`
- `docs/GUIA-SECTIONS-E-LIMPEZA.md`
- `docs/FLUXO-DE-TRABALHO-ELEMENTOR.md`
- `docs/HOME-ELEMENTOR-PASSO-A-PASSO.md`
