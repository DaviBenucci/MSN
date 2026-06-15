# Guia de instalacao no Elementor

## 1. Preparacao

- Trabalhe primeiro em staging.
- Faca backup completo do WordPress, banco e uploads.
- Atualize WordPress, WooCommerce, Elementor, Elementor Pro e tema.
- Desative plugins abandonados ou duplicados.
- Confirme HTTPS ativo.

## 2. CSS e JS globais

1. Copie `shared/msn-global.css` para o CSS global do Elementor ou para CSS adicional do tema.
2. Copie CSS especifico de pagina no CSS adicional da propria pagina/template.
3. Cole HTML em widget HTML.
4. Se o CSS for colado dentro do widget HTML, envolva com `<style>...</style>`.
5. Se o JS for colado dentro do widget HTML, envolva com `<script>...</script>`.
6. Mantenha o carregamento global leve. JS de componentes deve ser ativado apenas onde o componente aparece.

Observacao: os arquivos `.js` usam sintaxe ES5, sem arrow functions (`=>`), para evitar erro de caracteres especiais no editor do Elementor.

## 3. Templates Elementor

Crie templates separados:

- Header global: `components/header/msn-header.html`, `.css`, `.js`.
- Footer global: `components/footer/msn-footer.html`, `.css`, `.js`.
- Home: `components/home/msn-home.html`, `.css`, `.js`.
- Loja/categorias/busca: `components/shop/msn-shop.html`, `.css`, `.js`.
- Produto unico: `components/product/msn-product.html`, `.css`, `.js`.
- Carrinho: `components/cart/msn-cart.html`, `.css`, `.js`.
- Minha conta: `components/account/msn-account.html`, `.css`, `.js`.
- Contato: `components/contact/msn-contact.html`, `.css`, `.js`.

## 4. Uso de WooCommerce

Nos pontos marcados como slot WooCommerce, use widgets nativos do Elementor Pro ou widget Shortcode. Exemplos:

- Produtos recentes: `[products limit="8" columns="4" orderby="date" order="DESC" visibility="visible"]`
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

## 6. Documentos de apoio

- `COMO-COLAR-NO-ELEMENTOR.md`
- `VERSOES-E-COMPATIBILIDADE.md`
- `PRODUTOS-NAO-APARECEM.md`
- `MAPA-DE-COMPONENTES.md`
- `AUDITORIA-CATALOGO.md`
