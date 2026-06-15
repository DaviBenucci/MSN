# Guia de instalacao no Elementor

## 1. Preparacao

- Trabalhe primeiro em staging.
- Faca backup completo do WordPress, banco e uploads.
- Atualize WordPress, WooCommerce, Elementor, Elementor Pro e tema.
- Desative plugins abandonados ou duplicados.
- Confirme HTTPS ativo.

## 2. Globais

1. Copie `shared/msn-global.css` para o CSS global do Elementor ou CSS adicional do tema.
2. Copie `shared/msn-global.js` para Custom Code no footer.
3. Ative o plugin `msn-woocommerce-layout-bridge` quando for usar vitrines com `data-msn-products`.

Nao cole `msn-woo-layout.css` ou `msn-woo-layout.js` manualmente no Elementor; o plugin carrega esses arquivos.

## 3. Templates por sections

Use apenas os arquivos dentro de `sections`:

- Header: `components/header/sections`
- Footer: `components/footer/sections`
- Home: `components/home/sections`
- Loja/categorias/busca: `components/shop/sections`
- Produto unico: `components/product/sections`
- Carrinho: `components/cart/sections`
- Minha conta: `components/account/sections`
- Contato: `components/contact/sections`

Cada pasta tem um `README.md` com a ordem de colagem.

## 4. Uso de WooCommerce

Nos pontos marcados como slot WooCommerce, use widgets nativos do Elementor Pro ou widget Shortcode. Exemplos:

- Produtos recentes: bridge `data-msn-products` ou `[products limit="8" columns="4" orderby="date" order="DESC" visibility="visible"]`
- Loja com paginacao: `[products limit="12" columns="3" paginate="true" visibility="visible"]`
- Ofertas: `[sale_products limit="8" columns="4"]`
- Carrinho: `[woocommerce_cart]`
- Minha conta: `[woocommerce_my_account]`

Nao cole preco, estoque, subtotal, frete ou checkout como HTML fixo. Esses dados precisam continuar vindo do WooCommerce.

Importante: shortcode WooCommerce deve ser colado em widget Shortcode, nao em widget HTML comum.

## 5. Publicacao

- Publique primeiro header e footer.
- Depois home.
- Depois loja, filtros e busca usando produtos dinamicos do WooCommerce.
- Depois produto.
- Depois carrinho, minha conta e contato.
- Por fim, saneie catalogo e teste o fluxo completo de compra.

## 6. Limpeza

Depois de criar ou trocar sections:

1. Remova arquivos antigos substituidos.
2. Confirme que nao existem arquivos combinados `components/<pagina>/msn-*.html/css/js`.
3. Atualize `MAPA-DE-COMPONENTES.md`.
4. Limpe cache do WP Rocket e regenere CSS do Elementor.

Documento de referencia: `GUIA-SECTIONS-E-LIMPEZA.md`.
