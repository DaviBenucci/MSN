(function () {
  'use strict';

  const config = window.MSNWoo || {};

  function buildUrl(base, params) {
    const url = new URL(base, window.location.origin);
    Object.entries(params || {}).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, value);
      }
    });
    return url.toString();
  }

  async function requestJson(url, options = {}) {
    const response = await fetch(url, {
      credentials: 'same-origin',
      ...options,
      headers: {
        Accept: 'application/json',
        ...(options.headers || {})
      }
    });

    const nextStoreNonce = response.headers.get('Nonce') || response.headers.get('X-WC-Store-API-Nonce');
    if (nextStoreNonce && config.rest) {
      config.rest.storeApiNonce = nextStoreNonce;
    }

    if (!response.ok) {
      let details = null;
      try {
        details = await response.json();
      } catch (error) {
        details = { message: response.statusText };
      }
      throw new Error(details && details.message ? details.message : 'Erro na requisicao.');
    }

    return response.json();
  }

  async function getBootstrap() {
    return requestJson((config.rest && config.rest.base ? config.rest.base : '/wp-json/msn/v1/') + 'bootstrap');
  }

  async function getProducts(params = {}) {
    const base = (config.rest && config.rest.base ? config.rest.base : '/wp-json/msn/v1/') + 'products';
    return requestJson(buildUrl(base, params));
  }

  async function getProduct(id) {
    const base = (config.rest && config.rest.base ? config.rest.base : '/wp-json/msn/v1/') + 'product/' + encodeURIComponent(id);
    return requestJson(base);
  }

  async function getCart() {
    const base = (config.rest && config.rest.storeApiBase ? config.rest.storeApiBase : '/wp-json/wc/store/v1/') + 'cart';
    return requestJson(base);
  }

  async function getCartItems() {
    const base = (config.rest && config.rest.storeApiBase ? config.rest.storeApiBase : '/wp-json/wc/store/v1/') + 'cart/items';
    return requestJson(base);
  }

  async function addToCart(productId, quantity = 1, variation = []) {
    const base = (config.rest && config.rest.storeApiBase ? config.rest.storeApiBase : '/wp-json/wc/store/v1/') + 'cart/items';

    return requestJson(base, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Nonce: config.rest && config.rest.storeApiNonce ? config.rest.storeApiNonce : ''
      },
      body: JSON.stringify({
        id: Number(productId),
        quantity: Number(quantity),
        variation: variation
      })
    });
  }

  function parseJsonAttribute(node, attribute, fallback = {}) {
    const raw = node.getAttribute(attribute);
    if (!raw) return fallback;

    try {
      return JSON.parse(raw);
    } catch (error) {
      console.warn('MSN: atributo JSON invalido em ' + attribute + '.', error);
      return fallback;
    }
  }

  function readInlineProductData(scope = document) {
    return Array.from(scope.querySelectorAll('.msn-product-data')).map((node) => {
      try {
        return JSON.parse(node.textContent || '{}');
      } catch (error) {
        console.warn('MSN: dados de produto invalidos.', error);
        return {};
      }
    });
  }

  function readProductCards(scope = document) {
    return Array.from(scope.querySelectorAll('[data-msn-product]')).map((node) => {
      try {
        return {
          element: node,
          product: JSON.parse(node.dataset.msnProduct || '{}')
        };
      } catch (error) {
        console.warn('MSN: card com JSON invalido.', error);
        return {
          element: node,
          product: {}
        };
      }
    });
  }

  function setCartCount(count) {
    const safeCount = Number.isFinite(Number(count)) ? Number(count) : 0;
    document.querySelectorAll('[data-msn-cart-count]').forEach((element) => {
      element.textContent = String(safeCount);
      element.hidden = false;
      element.removeAttribute('hidden');
      element.setAttribute('aria-live', 'polite');
      element.setAttribute('aria-label', safeCount === 1 ? '1 item no carrinho' : safeCount + ' itens no carrinho');
    });
  }

  async function refreshCartCount() {
    try {
      const cart = await getCart();
      setCartCount(cart.items_count || 0);
      return cart;
    } catch (error) {
      console.warn('MSN: nao foi possivel atualizar o carrinho.', error);
      return null;
    }
  }

  function createProductCard(product) {
    const actions = product.actions || {};
    const actionType = actions.actionType || 'view_product';
    const image = product.image || {};
    const price = product.price || {};
    const stock = product.stock || {};

    const article = document.createElement('article');
    article.className = 'msn-bridge-product-card msn-bridge-product-card--' + actionType;
    article.dataset.msnProduct = JSON.stringify(product);

    if (stock.status) {
      article.classList.add('msn-product-card--stock-' + stock.status);
    }

    const imageLink = document.createElement('a');
    imageLink.className = 'msn-bridge-product-card__image-link';
    imageLink.href = product.permalink || actions.viewUrl || '#';

    const img = document.createElement('img');
    img.className = 'msn-bridge-product-card__image';
    img.src = image.src || '';
    img.alt = image.alt || product.name || 'Produto MSN Distribuidora';
    img.loading = 'lazy';
    imageLink.appendChild(img);
    article.appendChild(imageLink);

    const body = document.createElement('div');
    body.className = 'msn-bridge-product-card__body';

    if (product.sku) {
      const sku = document.createElement('span');
      sku.className = 'msn-bridge-product-card__sku';
      sku.textContent = 'SKU: ' + product.sku;
      body.appendChild(sku);
    }

    const title = document.createElement('h3');
    title.className = 'msn-bridge-product-card__title';

    const titleLink = document.createElement('a');
    titleLink.href = product.permalink || actions.viewUrl || '#';
    titleLink.textContent = product.name || 'Produto';
    title.appendChild(titleLink);
    body.appendChild(title);

    const priceNode = document.createElement('div');
    priceNode.className = 'msn-bridge-product-card__price';
    priceNode.innerHTML = price.html || '';
    body.appendChild(priceNode);

    const stockNode = document.createElement('div');
    stockNode.className = 'msn-bridge-product-card__stock msn-stock-' + (stock.status || 'unknown');
    stockNode.textContent = stock.label || 'Consultar estoque';
    body.appendChild(stockNode);

    const button = document.createElement('a');
    button.className = 'button msn-bridge-product-card__button msn-bridge-product-card__button--' + actionType;
    button.href = actions.ctaUrl || actions.viewUrl || product.permalink || '#';
    button.textContent = actions.ctaText || 'Ver produto';
    button.dataset.msnAction = actionType;
    button.setAttribute('rel', 'nofollow');

    if (actionType === 'simple_add_to_cart_url') {
      button.dataset.product_id = String(product.id || '');
      button.dataset.product_sku = product.sku || '';
      button.setAttribute('aria-label', actions.ctaText || 'Adicionar ao carrinho');

      if (actions.supportsAjax) {
        button.classList.add('ajax_add_to_cart', 'add_to_cart_button');
      }
    }

    body.appendChild(button);
    article.appendChild(body);

    return article;
  }

  function renderProducts(container, response) {
    const products = response && Array.isArray(response.products) ? response.products : [];
    container.innerHTML = '';
    container.classList.add('msn-bridge-products');
    container.classList.remove('is-loading', 'has-error');
    container.setAttribute('aria-busy', 'false');

    if (!products.length) {
      const empty = document.createElement('p');
      empty.className = 'msn-bridge-products__status';
      empty.textContent = 'Nenhum produto encontrado no momento.';
      container.appendChild(empty);
      return;
    }

    const grid = document.createElement('div');
    grid.className = 'msn-bridge-products__grid';
    products.forEach((product) => {
      grid.appendChild(createProductCard(product));
    });
    container.appendChild(grid);
  }

  async function renderProductContainer(container) {
    const query = parseJsonAttribute(container, 'data-msn-query', {});
    container.classList.add('msn-bridge-products', 'is-loading');
    container.classList.remove('has-error');
    container.setAttribute('aria-busy', 'true');
    container.innerHTML = '<p class="msn-bridge-products__status">Carregando produtos...</p>';

    try {
      const response = await getProducts(query);
      renderProducts(container, response);
      return response;
    } catch (error) {
      container.classList.remove('is-loading');
      container.classList.add('has-error');
      container.setAttribute('aria-busy', 'false');
      container.innerHTML = '<p class="msn-bridge-products__status">Nao foi possivel carregar os produtos agora.</p>';
      console.warn('MSN: falha ao renderizar produtos.', error);
      return null;
    }
  }

  function renderProductContainers(scope = document) {
    const containers = Array.from(scope.querySelectorAll('[data-msn-products]'));
    return Promise.all(containers.map((container) => renderProductContainer(container)));
  }

  function bindWooCartEvents() {
    if (!window.jQuery) return;

    window.jQuery(document.body).on(
      'added_to_cart removed_from_cart updated_cart_totals wc_fragments_refreshed updated_wc_div',
      function () {
        refreshCartCount();
      }
    );
  }

  window.MSNWooLayout = {
    config,
    api: {
      getBootstrap,
      getProducts,
      getProduct,
      getCart,
      getCartItems,
      addToCart
    },
    helpers: {
      readInlineProductData,
      readProductCards,
      refreshCartCount,
      renderProductContainers,
      renderProducts,
      setCartCount
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    readProductCards().forEach(({ element, product }) => {
      if (product && product.stock && product.stock.status) {
        element.classList.add('msn-product-card--stock-' + product.stock.status);
      }
    });

    renderProductContainers();
    refreshCartCount();
    bindWooCartEvents();
  });
})();
