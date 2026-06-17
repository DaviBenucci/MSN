# MSN WooCommerce Layout Bridge

Plugin de ponte segura entre WooCommerce, Elementor e containers HTML/CSS/JS da MSN Distribuidora.

## Papel do plugin

- Entregar dados publicos do WooCommerce para layouts customizados.
- Renderizar vitrines em containers HTML usando `data-msn-products`.
- Atualizar contador visual do carrinho em elementos `data-msn-cart-count`.
- Complementar Elementor/WooCommerce sem substituir checkout, conta, pagamento, frete ou selecao de variacoes.

## Instalacao

1. Compacte a pasta `msn-woocommerce-layout-bridge` em ZIP.
2. No WordPress, acesse Plugins > Adicionar novo > Enviar plugin.
3. Ative o plugin.
4. Use os shortcodes ou containers documentados dentro do Elementor.

## Renderer de produtos

Cole um container HTML com:

```html
<div data-msn-products data-msn-query='{"per_page":8,"orderby":"date","order":"DESC"}'></div>
```

O JavaScript carrega `/wp-json/msn/v1/products` e renderiza cards com imagem, nome, SKU, preco, estoque e CTA seguro.

### CTAs retornados

`actions.actionType` pode ser:

- `simple_add_to_cart_url`: produto simples compravel; usa URL nativa do WooCommerce.
- `requires_options`: produto variavel ou agrupado; leva para a pagina do produto para escolher opcoes.
- `view_product`: produto sem compra direta segura; leva para a pagina do produto.

## Shortcodes

```txt
[msn_product_search]
[msn_cart_link]
[msn_account_link]
[msn_product_card]
[msn_product_card id="123"]
[msn_product_data]
[msn_product_data context="detail"]
[msn_product_whatsapp phone="5511999999999"]
```

`[msn_product_search]` renderiza o formulario nativo de busca de produtos do WooCommerce (`get_product_search_form()`), mantendo a consulta limitada a produtos. Use esse shortcode dentro de um widget Shortcode do Elementor e estilize o resultado pelos slots do layout, como `msn-header__search-slot` e `msn-header__drawer-search`.

`[msn_product_card]` e um fallback. Para venda real em loja/categoria, prefira o renderer `data-msn-products`, Loop Grid tipo Products, widget Products/Archive Products ou shortcodes nativos.

## Objeto JavaScript global

O plugin injeta:

```js
window.MSNWoo
window.MSNWooLayout
```

Exemplos:

```js
await window.MSNWooLayout.helpers.renderProductContainers();
await window.MSNWooLayout.helpers.refreshCartCount();
const products = await window.MSNWooLayout.api.getProducts({ per_page: 8, orderby: 'date' });
```

`api.addToCart()` permanece disponivel como legado tecnico, mas nao e usado na Home v1. Compra customizada via JS fica fora do escopo inicial.

## Endpoints customizados

```txt
GET /wp-json/msn/v1/bootstrap
GET /wp-json/msn/v1/products
GET /wp-json/msn/v1/product/{id}
```

## Seguranca

- Nao expoe chaves da REST API administrativa do WooCommerce.
- Nao expoe pedidos, enderecos, telefone ou e-mail do usuario.
- Expoe apenas dados publicos e uteis para layout.
- Usa `wc_get_products()` para consultas de produto.
- Usa Store API somente para dados do carrinho do cliente atual.
- Usa `wp_create_nonce('wc_store_api')` para operacoes legadas de carrinho via Store API.
- Valida e sanitiza parametros REST.
- Limita `per_page` a 24 produtos por requisicao.

## Regra de ouro

Produto variavel deve escolher atributos no fluxo nativo do WooCommerce. Carrinho, checkout, conta, pedidos, frete, cupom, pagamento e login tambem continuam nativos.
