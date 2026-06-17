# Guia de instalacao no Elementor

## 1. Preparacao

- Trabalhe primeiro em staging.
- Faca backup completo do WordPress, banco e uploads.
- Atualize WordPress, WooCommerce, Elementor, Elementor Pro e tema.
- Desative plugins abandonados ou duplicados.
- Confirme HTTPS ativo.

## 2. Globais

1. Copie `shared/msn-theme-init-js.html` para Custom Code no **Head**, sem `defer`, sem `async` e sem atraso por plugin de cache. Ele e pequeno e evita piscar/quebrar o tema na primeira carga.
2. Copie `shared/msn-global-css.html` para o CSS global do Elementor, CSS adicional do tema ou Custom Code no **Head**.
3. Copie `shared/msn-global-js.html` para Custom Code no **Footer**. Nao coloque esse arquivo no Head.
4. Ative o plugin `msn-woocommerce-layout-bridge` quando for usar vitrines com `data-msn-products`.

Nao cole `msn-woo-layout.css` ou `msn-woo-layout.js` manualmente no Elementor; o plugin carrega esses arquivos.

O seletor de tema usa `localStorage` na chave `msn-theme-preference` e aceita `system`, `light` e `dark`.

## 2.1 Performance e primeira carga

Nao mova todos os scripts globais para o Head. Isso bloqueia a renderizacao inicial e piora o tempo de carregamento, especialmente com muitos usuarios simultaneos.

Use esta ordem:

1. Head imediato: apenas `msn-theme-init-js.html`.
2. Head/CSS global: `msn-global-css.html`.
3. Footer: `msn-global-js.html`.
4. Footer ou widget da pagina: somente os JS das sections presentes naquela pagina.

Em plugins como WP Rocket, nao atrase o `msn-theme-init-js.html`. Se usar atraso de JavaScript, teste com cuidado `msn-global-js.html`, `00-header.js`, carrinho, checkout e minha conta, porque esses scripts afetam interacao visivel.

Para paginas publicas com alto trafego, mantenha cache de pagina ativo. Exclua do cache completo carrinho, finalizacao de compra, minha conta e endpoints dinamicos do WooCommerce.

## 3. Templates por sections

Use apenas os arquivos dentro de `sections`:

- Header: `components/header/sections`
- Footer: `components/footer/sections`
- Home: `components/home/sections`
- Loja/categorias/busca: `components/shop/sections`
- Produto unico: `components/product/sections`
- Carrinho: `components/cart/sections`
- Finalizacao de compra: `components/checkout/sections`
- Minha conta: `components/account/sections`
- Contato: `components/contact/sections`
- Politica de devolucao: `components/returns/sections`
- Politica de privacidade: `components/privacy/sections`
- Avalie seu pedido: `components/order-review/sections`

Cada pasta tem um `README.md` com a ordem de colagem.

## 4. Uso de WooCommerce

Nos pontos marcados como slot WooCommerce, use widgets nativos do Elementor Pro ou widget Shortcode. Exemplos:

- Produtos recentes: bridge `data-msn-products` ou `[products limit="8" columns="4" orderby="date" order="DESC" visibility="visible"]`
- Loja com paginacao: `[products limit="12" columns="3" paginate="true" visibility="visible"]`
- Ofertas: `[sale_products limit="8" columns="4"]`
- Carrinho: `[woocommerce_cart]`
- Finalizacao de compra: `[woocommerce_checkout]`
- Minha conta: `[woocommerce_my_account]`

Nao cole preco, estoque, subtotal, frete ou checkout como HTML fixo. Esses dados precisam continuar vindo do WooCommerce.

Importante: shortcode WooCommerce deve ser colado em widget Shortcode, nao em widget HTML comum.

Tambem nao tente inserir widget WooCommerce dentro de widget HTML. O Elementor nao permite esse encaixe. Quando um `.html` deste kit tiver um comentario dizendo para inserir widget em um slot, use essa logica:

1. Recrie o wrapper do slot com um Container do Elementor.
2. Coloque a classe do slot no Container, por exemplo `msn-cart-woo-slot` ou `msn-account-woo-slot`.
3. Insira o widget WooCommerce ou widget Shortcode dentro desse Container.
4. Use o HTML widget apenas para textos, cards, sidebars e blocos visuais estaticos.

Exemplos de slots que exigem essa logica:

- Carrinho: `msn-cart-woo-slot` com `[woocommerce_cart]` ou widget Cart.
- Finalizacao de compra: `msn-checkout-woo-slot` com `[woocommerce_checkout]` ou widget Checkout.
- Minha conta: `msn-account-woo-slot` com `[woocommerce_my_account]` ou widget My Account.
- Loja: `msn-shop-filter__plugin-slot` para filtros e `msn-shop__woo-slot msn-product-card-model` para produtos.
- Produto unico: `msn-product-media-slot`, `msn-product-price-slot`, `msn-product-add-to-cart-slot`, `msn-product-description-slot` e relacionados.

## 5. Publicacao

- Publique primeiro header e footer.
- Depois home.
- Depois loja, filtros e busca usando produtos dinamicos do WooCommerce.
- Depois produto.
- Depois carrinho, finalizacao de compra, minha conta e contato.
- Depois politica de privacidade, trocas/devolucoes e avalie seu pedido.
- Por fim, saneie catalogo e teste o fluxo completo de compra.

## 6. Limpeza

Depois de criar ou trocar sections:

1. Remova arquivos antigos substituidos.
2. Confirme que nao existem arquivos combinados `components/<pagina>/msn-*.html/css/js`.
3. Atualize `MAPA-DE-COMPONENTES.md`.
4. Limpe cache do WP Rocket e regenere CSS do Elementor.

Documento de referencia: `GUIA-SECTIONS-E-LIMPEZA.md`.
