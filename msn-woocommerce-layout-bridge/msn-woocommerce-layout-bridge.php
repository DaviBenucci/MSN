<?php
/**
 * Plugin Name: MSN WooCommerce Layout Bridge
 * Description: Camada segura de dados entre WooCommerce, Elementor e componentes HTML/CSS/JS da MSN Distribuidora.
 * Version: 1.1.1
 * Author: MSN Distribuidora / Davi Benucci
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Text Domain: msn-woocommerce-layout-bridge
 */

if (!defined('ABSPATH')) {
    exit;
}

final class MSN_WooCommerce_Layout_Bridge
{
    private const VERSION = '1.1.1';
    private const REST_NAMESPACE = 'msn/v1';

    public static function init(): void
    {
        add_action('wp_enqueue_scripts', [__CLASS__, 'enqueue_assets']);
        add_action('rest_api_init', [__CLASS__, 'register_rest_routes']);

        add_shortcode('msn_product_data', [__CLASS__, 'shortcode_product_data']);
        add_shortcode('msn_product_card', [__CLASS__, 'shortcode_product_card']);
        add_shortcode('msn_product_search', [__CLASS__, 'shortcode_product_search']);
        add_shortcode('msn_cart_link', [__CLASS__, 'shortcode_cart_link']);
        add_shortcode('msn_account_link', [__CLASS__, 'shortcode_account_link']);
        add_shortcode('msn_product_whatsapp', [__CLASS__, 'shortcode_product_whatsapp']);

        add_filter('woocommerce_add_to_cart_fragments', [__CLASS__, 'cart_count_fragment']);
    }

    private static function is_woo_active(): bool
    {
        return class_exists('WooCommerce') && function_exists('WC') && function_exists('wc_get_product');
    }

    public static function enqueue_assets(): void
    {
        $base_url = plugin_dir_url(__FILE__);

        wp_enqueue_style(
            'msn-woo-layout-bridge',
            $base_url . 'assets/msn-woo-layout.css',
            [],
            self::VERSION
        );

        wp_enqueue_script(
            'msn-woo-layout-bridge',
            $base_url . 'assets/msn-woo-layout.js',
            [],
            self::VERSION,
            true
        );

        wp_add_inline_script(
            'msn-woo-layout-bridge',
            'window.MSNWoo = ' . wp_json_encode(self::get_bootstrap_data(false)) . ';',
            'before'
        );
    }

    public static function register_rest_routes(): void
    {
        register_rest_route(self::REST_NAMESPACE, '/bootstrap', [
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => [__CLASS__, 'rest_bootstrap'],
            'permission_callback' => '__return_true',
        ]);

        register_rest_route(self::REST_NAMESPACE, '/products', [
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => [__CLASS__, 'rest_products'],
            'permission_callback' => '__return_true',
            'args'                => [
                'page' => [
                    'default'           => 1,
                    'sanitize_callback' => 'absint',
                ],
                'per_page' => [
                    'default'           => 12,
                    'sanitize_callback' => 'absint',
                ],
                'category' => [
                    'sanitize_callback' => 'sanitize_title',
                ],
                'tag' => [
                    'sanitize_callback' => 'sanitize_title',
                ],
                'sku' => [
                    'sanitize_callback' => 'sanitize_text_field',
                ],
                'orderby' => [
                    'default'           => 'date',
                    'sanitize_callback' => 'sanitize_key',
                ],
                'order' => [
                    'default'           => 'DESC',
                    'sanitize_callback' => 'sanitize_key',
                ],
                'featured' => [
                    'default'           => false,
                    'sanitize_callback' => [__CLASS__, 'sanitize_bool'],
                ],
                'on_sale' => [
                    'default'           => false,
                    'sanitize_callback' => [__CLASS__, 'sanitize_bool'],
                ],
                'stock_status' => [
                    'sanitize_callback' => 'sanitize_key',
                ],
            ],
        ]);

        register_rest_route(self::REST_NAMESPACE, '/product/(?P<id>\d+)', [
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => [__CLASS__, 'rest_single_product'],
            'permission_callback' => '__return_true',
            'args'                => [
                'id' => [
                    'required'          => true,
                    'validate_callback' => static function ($param): bool {
                        return absint($param) > 0;
                    },
                    'sanitize_callback' => 'absint',
                ],
            ],
        ]);
    }

    public static function sanitize_bool($value): bool
    {
        return filter_var($value, FILTER_VALIDATE_BOOLEAN);
    }

    public static function rest_bootstrap(WP_REST_Request $request): WP_REST_Response
    {
        return rest_ensure_response(self::get_bootstrap_data(true));
    }

    public static function rest_products(WP_REST_Request $request)
    {
        if (!self::is_woo_active()) {
            return new WP_Error('msn_woo_inactive', 'WooCommerce não está ativo.', ['status' => 503]);
        }

        $page     = max(1, absint($request->get_param('page')));
        $per_page = min(24, max(1, absint($request->get_param('per_page'))));
        $orderby  = self::sanitize_product_orderby($request->get_param('orderby'));
        $order    = strtoupper((string) $request->get_param('order')) === 'ASC' ? 'ASC' : 'DESC';

        $args = [
            'status'     => 'publish',
            'visibility' => 'visible',
            'limit'      => $per_page,
            'page'       => $page,
            'paginate'   => true,
            'orderby'    => $orderby,
            'order'      => $order,
        ];

        $category = sanitize_title((string) $request->get_param('category'));
        if ($category !== '') {
            $args['category'] = [$category];
        }

        $tag = sanitize_title((string) $request->get_param('tag'));
        if ($tag !== '') {
            $args['tag'] = [$tag];
        }

        $sku = sanitize_text_field((string) $request->get_param('sku'));
        if ($sku !== '') {
            $args['sku'] = $sku;
        }

        if (self::sanitize_bool($request->get_param('featured'))) {
            $args['featured'] = true;
        }

        if (self::sanitize_bool($request->get_param('on_sale'))) {
            $args['include'] = wc_get_product_ids_on_sale();
        }

        $stock_status = sanitize_key((string) $request->get_param('stock_status'));
        if (in_array($stock_status, ['instock', 'outofstock', 'onbackorder'], true)) {
            $args['stock_status'] = $stock_status;
        }

        $result = wc_get_products($args);
        $products = [];

        foreach ($result->products ?? [] as $product) {
            if ($product instanceof WC_Product) {
                $products[] = self::product_to_layout_data($product, 'card');
            }
        }

        return rest_ensure_response([
            'page'        => $page,
            'per_page'    => $per_page,
            'total'       => isset($result->total) ? absint($result->total) : count($products),
            'total_pages' => isset($result->max_num_pages) ? absint($result->max_num_pages) : 1,
            'products'    => array_values(array_filter($products)),
        ]);
    }

    public static function rest_single_product(WP_REST_Request $request)
    {
        if (!self::is_woo_active()) {
            return new WP_Error('msn_woo_inactive', 'WooCommerce não está ativo.', ['status' => 503]);
        }

        $product_id = absint($request->get_param('id'));
        $product = wc_get_product($product_id);

        if (!$product || get_post_status($product_id) !== 'publish' || !$product->is_visible()) {
            return new WP_Error('msn_product_not_found', 'Produto não encontrado.', ['status' => 404]);
        }

        return rest_ensure_response(self::product_to_layout_data($product, 'detail'));
    }

    private static function sanitize_product_orderby($orderby): string
    {
        $orderby = sanitize_key((string) $orderby);
        $allowed = ['date', 'title', 'menu_order', 'price', 'popularity', 'rating'];

        return in_array($orderby, $allowed, true) ? $orderby : 'date';
    }

    private static function get_bootstrap_data(bool $include_catalog): array
    {
        $data = [
            'version' => self::VERSION,
            'rest'    => [
                'base'          => esc_url_raw(rest_url(self::REST_NAMESPACE . '/')),
                'nonce'         => wp_create_nonce('wp_rest'),
                'storeApiBase'  => esc_url_raw(rest_url('wc/store/v1/')),
                'storeApiNonce' => wp_create_nonce('wc_store_api'),
            ],
            'site' => [
                'name'        => sanitize_text_field(get_bloginfo('name')),
                'description' => sanitize_text_field(get_bloginfo('description')),
                'homeUrl'     => esc_url_raw(home_url('/')),
                'locale'      => sanitize_text_field(get_locale()),
            ],
            'urls' => self::get_urls(),
            'user' => self::get_safe_user_data(),
            'woo'  => [
                'active' => self::is_woo_active(),
            ],
        ];

        if (self::is_woo_active()) {
            $data['woo'] = array_merge($data['woo'], [
                'currency' => [
                    'code'              => get_woocommerce_currency(),
                    'symbol'            => get_woocommerce_currency_symbol(),
                    'decimalSeparator'  => wc_get_price_decimal_separator(),
                    'thousandSeparator' => wc_get_price_thousand_separator(),
                    'decimals'          => wc_get_price_decimals(),
                    'priceFormat'       => get_woocommerce_price_format(),
                ],
                'cart' => self::get_cart_summary(),
            ]);

            if ($include_catalog) {
                $data['catalog'] = self::get_catalog_data();
            }
        }

        return $data;
    }

    private static function get_urls(): array
    {
        $urls = [
            'home' => esc_url_raw(home_url('/')),
        ];

        if (self::is_woo_active()) {
            $urls = array_merge($urls, [
                'shop'     => esc_url_raw(wc_get_page_permalink('shop')),
                'cart'     => esc_url_raw(wc_get_cart_url()),
                'checkout' => esc_url_raw(wc_get_checkout_url()),
                'account'  => esc_url_raw(wc_get_page_permalink('myaccount')),
            ]);
        }

        return $urls;
    }

    private static function get_safe_user_data(): array
    {
        if (!is_user_logged_in()) {
            return [
                'isLoggedIn' => false,
                'displayName' => '',
                'accountUrls' => self::get_account_urls(),
            ];
        }

        $user = wp_get_current_user();

        return [
            'isLoggedIn'  => true,
            'displayName' => sanitize_text_field($user->display_name),
            'firstName'   => sanitize_text_field($user->first_name),
            'accountUrls' => self::get_account_urls(),
        ];
    }

    private static function get_account_urls(): array
    {
        if (!self::is_woo_active()) {
            return [];
        }

        $myaccount = wc_get_page_permalink('myaccount');

        return [
            'dashboard'     => esc_url_raw($myaccount),
            'orders'        => esc_url_raw(wc_get_endpoint_url('orders', '', $myaccount)),
            'downloads'     => esc_url_raw(wc_get_endpoint_url('downloads', '', $myaccount)),
            'editAddress'   => esc_url_raw(wc_get_endpoint_url('edit-address', '', $myaccount)),
            'editAccount'   => esc_url_raw(wc_get_endpoint_url('edit-account', '', $myaccount)),
            'lostPassword'  => esc_url_raw(wp_lostpassword_url()),
            'logout'        => esc_url_raw(wc_logout_url()),
        ];
    }

    private static function get_cart_summary(): array
    {
        if (!self::is_woo_active() || !WC()->cart) {
            return [
                'count' => 0,
                'subtotalHtml' => '',
                'needsStoreApiRefresh' => true,
            ];
        }

        return [
            'count' => absint(WC()->cart->get_cart_contents_count()),
            'subtotalHtml' => wp_kses_post(WC()->cart->get_cart_subtotal()),
            'needsStoreApiRefresh' => true,
        ];
    }

    private static function get_catalog_data(): array
    {
        return [
            'categories' => self::get_product_categories(),
            'attributes' => self::get_product_attributes(),
            'sortOptions' => [
                ['value' => 'date', 'label' => 'Novidades'],
                ['value' => 'popularity', 'label' => 'Mais vendidos'],
                ['value' => 'rating', 'label' => 'Melhor avaliados'],
                ['value' => 'price', 'label' => 'Preço'],
                ['value' => 'title', 'label' => 'Nome'],
            ],
            'stockOptions' => [
                ['value' => 'instock', 'label' => 'Em estoque'],
                ['value' => 'onbackorder', 'label' => 'Sob encomenda'],
                ['value' => 'outofstock', 'label' => 'Fora de estoque'],
            ],
        ];
    }

    private static function get_product_categories(): array
    {
        $terms = get_terms([
            'taxonomy'   => 'product_cat',
            'hide_empty' => false,
            'number'     => 100,
        ]);

        if (is_wp_error($terms)) {
            return [];
        }

        $categories = [];

        foreach ($terms as $term) {
            $categories[] = [
                'id'     => absint($term->term_id),
                'name'   => sanitize_text_field($term->name),
                'slug'   => sanitize_title($term->slug),
                'count'  => absint($term->count),
                'parent' => absint($term->parent),
                'url'    => esc_url_raw(get_term_link($term)),
            ];
        }

        return $categories;
    }

    private static function get_product_attributes(): array
    {
        if (!function_exists('wc_get_attribute_taxonomies')) {
            return [];
        }

        $attributes = [];

        foreach (wc_get_attribute_taxonomies() as $attribute) {
            $taxonomy = wc_attribute_taxonomy_name($attribute->attribute_name);

            if (!taxonomy_exists($taxonomy)) {
                continue;
            }

            $terms = get_terms([
                'taxonomy'   => $taxonomy,
                'hide_empty' => false,
                'number'     => 100,
            ]);

            if (is_wp_error($terms)) {
                continue;
            }

            $attributes[] = [
                'id'       => absint($attribute->attribute_id),
                'name'     => sanitize_key($attribute->attribute_name),
                'label'    => sanitize_text_field($attribute->attribute_label),
                'taxonomy' => sanitize_key($taxonomy),
                'terms'    => array_values(array_map(static function ($term): array {
                    return [
                        'id'    => absint($term->term_id),
                        'name'  => sanitize_text_field($term->name),
                        'slug'  => sanitize_title($term->slug),
                        'count' => absint($term->count),
                    ];
                }, $terms)),
            ];
        }

        return $attributes;
    }

    private static function product_to_layout_data(WC_Product $product, string $context = 'card'): ?array
    {
        $product_id = $product->get_id();

        if (!$product_id || get_post_status($product_id) !== 'publish' || !$product->is_visible()) {
            return null;
        }

        $data = [
            'id'        => absint($product_id),
            'type'      => sanitize_key($product->get_type()),
            'name'      => wp_strip_all_tags($product->get_name()),
            'slug'      => sanitize_title($product->get_slug()),
            'sku'       => sanitize_text_field($product->get_sku()),
            'permalink' => esc_url_raw(get_permalink($product_id)),
            'summary'   => [
                'shortDescriptionHtml' => wp_kses_post($product->get_short_description()),
                'shortDescriptionText' => wp_strip_all_tags($product->get_short_description()),
            ],
            'image'      => self::image_to_layout_data($product->get_image_id(), 'woocommerce_thumbnail'),
            'price'      => self::price_to_layout_data($product),
            'stock'      => self::stock_to_layout_data($product),
            'rating'     => [
                'average' => (float) $product->get_average_rating(),
                'count'   => absint($product->get_rating_count()),
                'reviews' => absint($product->get_review_count()),
            ],
            'flags'      => [
                'featured'       => (bool) $product->is_featured(),
                'onSale'         => (bool) $product->is_on_sale(),
                'virtual'        => (bool) $product->is_virtual(),
                'downloadable'   => (bool) $product->is_downloadable(),
                'soldIndividually' => (bool) $product->is_sold_individually(),
            ],
            'taxonomy'   => [
                'categories' => self::get_product_terms($product_id, 'product_cat'),
                'tags'       => self::get_product_terms($product_id, 'product_tag'),
                'attributes' => self::get_product_attribute_data($product),
            ],
            'actions'    => self::product_actions_to_layout_data($product),
        ];

        if ($context === 'detail') {
            $data['descriptionHtml'] = wp_kses_post($product->get_description());
            $data['gallery'] = self::gallery_to_layout_data($product);
            $data['relatedProductIds'] = array_map('absint', wc_get_related_products($product_id, 8));
            $data['dimensions'] = [
                'weight' => sanitize_text_field($product->get_weight()),
                'length' => sanitize_text_field($product->get_length()),
                'width'  => sanitize_text_field($product->get_width()),
                'height' => sanitize_text_field($product->get_height()),
            ];
        }

        return apply_filters('msnwc_product_layout_data', $data, $product, $context);
    }

    private static function price_to_layout_data(WC_Product $product): array
    {
        return [
            'html'         => wp_kses_post($product->get_price_html()),
            'price'        => sanitize_text_field((string) $product->get_price()),
            'regularPrice' => sanitize_text_field((string) $product->get_regular_price()),
            'salePrice'    => sanitize_text_field((string) $product->get_sale_price()),
            'onSale'       => (bool) $product->is_on_sale(),
            'currency'     => [
                'code'   => get_woocommerce_currency(),
                'symbol' => get_woocommerce_currency_symbol(),
            ],
        ];
    }

    private static function stock_to_layout_data(WC_Product $product): array
    {
        $status = sanitize_key($product->get_stock_status());
        $labels = [
            'instock'     => 'Em estoque',
            'outofstock'  => 'Fora de estoque',
            'onbackorder' => 'Sob encomenda',
        ];

        $expose_quantity = (bool) apply_filters('msnwc_expose_stock_quantity', false, $product);

        return [
            'status'          => $status,
            'label'           => $labels[$status] ?? 'Consultar estoque',
            'isInStock'       => (bool) $product->is_in_stock(),
            'managingStock'   => (bool) $product->managing_stock(),
            'quantity'        => $expose_quantity && $product->managing_stock() ? $product->get_stock_quantity() : null,
            'backordersAllowed' => (bool) $product->backorders_allowed(),
            'lowStockRemaining' => method_exists($product, 'get_low_stock_amount') ? $product->get_low_stock_amount() : null,
        ];
    }

    private static function product_actions_to_layout_data(WC_Product $product): array
    {
        $view_url = get_permalink($product->get_id());
        $action_type = 'view_product';
        $cta_url = $view_url;
        $cta_text = $product->add_to_cart_text() ?: 'Ver produto';
        $supports_ajax = false;

        if ($product->is_type(['variable', 'grouped'])) {
            $action_type = 'requires_options';
            $cta_url = $view_url;
            $cta_text = $product->add_to_cart_text() ?: 'Ver opções';
        } elseif ($product->is_type('simple') && $product->is_purchasable() && $product->is_in_stock()) {
            $action_type = 'simple_add_to_cart_url';
            $cta_url = $product->add_to_cart_url();
            $cta_text = $product->add_to_cart_text() ?: 'Comprar';
            $supports_ajax = (bool) $product->supports('ajax_add_to_cart');
        } elseif ($product->is_type('external') && $product->is_purchasable()) {
            $cta_url = $product->add_to_cart_url() ?: $view_url;
            $cta_text = $product->add_to_cart_text() ?: 'Ver produto';
        }

        return [
            'actionType'       => sanitize_key($action_type),
            'ctaUrl'           => esc_url_raw($cta_url),
            'ctaText'          => sanitize_text_field($cta_text),
            'addToCartUrl'     => esc_url_raw($cta_url),
            'addToCartText'    => sanitize_text_field($cta_text),
            'isPurchasable'    => (bool) $product->is_purchasable(),
            'supportsAjax'     => $supports_ajax,
            'requiresOptions'  => $action_type === 'requires_options',
            'usesNativeFlow'   => true,
            'viewUrl'          => esc_url_raw($view_url),
        ];
    }

    private static function image_to_layout_data($attachment_id, string $size = 'woocommerce_thumbnail'): array
    {
        $attachment_id = absint($attachment_id);

        if (!$attachment_id) {
            return [
                'id'    => 0,
                'src'   => esc_url_raw(wc_placeholder_img_src($size)),
                'alt'   => '',
                'title' => '',
            ];
        }

        return [
            'id'    => $attachment_id,
            'src'   => esc_url_raw(wp_get_attachment_image_url($attachment_id, $size)),
            'full'  => esc_url_raw(wp_get_attachment_image_url($attachment_id, 'full')),
            'alt'   => sanitize_text_field(get_post_meta($attachment_id, '_wp_attachment_image_alt', true)),
            'title' => sanitize_text_field(get_the_title($attachment_id)),
        ];
    }

    private static function gallery_to_layout_data(WC_Product $product): array
    {
        $ids = array_merge([$product->get_image_id()], $product->get_gallery_image_ids());
        $ids = array_values(array_filter(array_map('absint', array_unique($ids))));

        return array_map(static function ($id): array {
            return self::image_to_layout_data($id, 'woocommerce_single');
        }, $ids);
    }

    private static function get_product_terms(int $product_id, string $taxonomy): array
    {
        $terms = get_the_terms($product_id, $taxonomy);

        if (!$terms || is_wp_error($terms)) {
            return [];
        }

        return array_values(array_map(static function ($term): array {
            return [
                'id'   => absint($term->term_id),
                'name' => sanitize_text_field($term->name),
                'slug' => sanitize_title($term->slug),
                'url'  => esc_url_raw(get_term_link($term)),
            ];
        }, $terms));
    }

    private static function get_product_attribute_data(WC_Product $product): array
    {
        $attributes = [];

        foreach ($product->get_attributes() as $attribute) {
            if (!$attribute instanceof WC_Product_Attribute) {
                continue;
            }

            if (!$attribute->get_visible()) {
                continue;
            }

            $name = $attribute->get_name();
            $label = wc_attribute_label($name, $product);
            $values = [];

            if ($attribute->is_taxonomy()) {
                $terms = wc_get_product_terms($product->get_id(), $name, ['fields' => 'all']);

                foreach ($terms as $term) {
                    $values[] = [
                        'id'   => absint($term->term_id),
                        'name' => sanitize_text_field($term->name),
                        'slug' => sanitize_title($term->slug),
                    ];
                }
            } else {
                foreach ($attribute->get_options() as $option) {
                    $values[] = [
                        'name' => sanitize_text_field((string) $option),
                    ];
                }
            }

            $attributes[] = [
                'name'   => sanitize_key($name),
                'label'  => sanitize_text_field($label),
                'values' => $values,
            ];
        }

        return $attributes;
    }

    private static function current_product_from_context(array $atts = [])
    {
        if (!self::is_woo_active()) {
            return false;
        }

        $product_id = !empty($atts['id']) ? absint($atts['id']) : 0;

        if (!$product_id) {
            global $product;
            if ($product instanceof WC_Product) {
                $product_id = $product->get_id();
            }
        }

        if (!$product_id && is_singular('product')) {
            $product_id = get_queried_object_id();
        }

        if (!$product_id) {
            $product_id = get_the_ID();
        }

        return $product_id ? wc_get_product($product_id) : false;
    }

    public static function shortcode_product_data($atts): string
    {
        $atts = shortcode_atts([
            'id'      => 0,
            'context' => 'card',
        ], $atts, 'msn_product_data');

        $product = self::current_product_from_context($atts);

        if (!$product instanceof WC_Product) {
            return '<script type="application/json" class="msn-product-data">{}</script>';
        }

        $context = $atts['context'] === 'detail' ? 'detail' : 'card';
        $data = self::product_to_layout_data($product, $context);

        return '<script type="application/json" class="msn-product-data" data-product-id="' . esc_attr($product->get_id()) . '">' . wp_json_encode($data) . '</script>';
    }

    public static function shortcode_product_card($atts): string
    {
        $atts = shortcode_atts([
            'id' => 0,
        ], $atts, 'msn_product_card');

        $product = self::current_product_from_context($atts);

        if (!$product instanceof WC_Product) {
            return '<!-- MSN: produto não encontrado -->';
        }

        $data = self::product_to_layout_data($product, 'card');

        ob_start();
        ?>
        <?php
        $actions = $data['actions'];
        $is_simple_add = $actions['actionType'] === 'simple_add_to_cart_url';
        $button_classes = 'button msn-product-card__button msn-bridge-product-card__button msn-product-card__button--' . sanitize_html_class($actions['actionType']);
        if ($is_simple_add && !empty($actions['supportsAjax'])) {
            $button_classes .= ' ajax_add_to_cart add_to_cart_button';
        }
        ?>
        <article class="msn-product-card msn-bridge-product-card" data-msn-product='<?php echo esc_attr(wp_json_encode($data)); ?>'>
            <a class="msn-product-card__image-link" href="<?php echo esc_url($data['permalink']); ?>">
                <img class="msn-product-card__image" src="<?php echo esc_url($data['image']['src']); ?>" alt="<?php echo esc_attr($data['image']['alt'] ?: $data['name']); ?>" loading="lazy">
            </a>
            <div class="msn-product-card__body">
                <?php if (!empty($data['sku'])) : ?>
                    <span class="msn-product-card__sku">SKU: <?php echo esc_html($data['sku']); ?></span>
                <?php endif; ?>

                <h3 class="msn-product-card__title">
                    <a href="<?php echo esc_url($data['permalink']); ?>"><?php echo esc_html($data['name']); ?></a>
                </h3>

                <div class="msn-product-card__price"><?php echo wp_kses_post($data['price']['html']); ?></div>
                <div class="msn-product-card__stock msn-stock-<?php echo esc_attr($data['stock']['status']); ?>"><?php echo esc_html($data['stock']['label']); ?></div>

                <a class="<?php echo esc_attr($button_classes); ?>"
                   href="<?php echo esc_url($actions['ctaUrl']); ?>"
                   data-product_id="<?php echo esc_attr($product->get_id()); ?>"
                   data-product_sku="<?php echo esc_attr($product->get_sku()); ?>"
                   data-msn-action="<?php echo esc_attr($actions['actionType']); ?>"
                   aria-label="<?php echo esc_attr($product->add_to_cart_description()); ?>"
                   rel="nofollow">
                    <?php echo esc_html($actions['ctaText']); ?>
                </a>
            </div>
        </article>
        <?php

        return ob_get_clean();
    }

    public static function shortcode_product_search(): string
    {
        if (!self::is_woo_active() || !function_exists('get_product_search_form')) {
            return '';
        }

        $form = get_product_search_form(false);

        if (!is_string($form) || trim($form) === '') {
            return '';
        }

        return '<div class="msn-product-search-slot">' . $form . '</div>';
    }

    public static function shortcode_cart_link(): string
    {
        if (!self::is_woo_active()) {
            return '';
        }

        $count = WC()->cart ? WC()->cart->get_cart_contents_count() : 0;

        return sprintf(
            '<a class="msn-cart-link" href="%s"><span class="msn-cart-link__label">Carrinho</span><span class="msn-cart-link__count" data-msn-cart-count>%s</span></a>',
            esc_url(wc_get_cart_url()),
            esc_html((string) absint($count))
        );
    }

    public static function shortcode_account_link(): string
    {
        if (!self::is_woo_active()) {
            return '';
        }

        $label = is_user_logged_in() ? 'Minha conta' : 'Entrar';

        return sprintf(
            '<a class="msn-account-link" href="%s">%s</a>',
            esc_url(wc_get_page_permalink('myaccount')),
            esc_html($label)
        );
    }

    public static function shortcode_product_whatsapp($atts): string
    {
        $atts = shortcode_atts([
            'id'    => 0,
            'phone' => '',
            'label' => 'Confirmar compatibilidade',
        ], $atts, 'msn_product_whatsapp');

        $product = self::current_product_from_context($atts);

        if (!$product instanceof WC_Product) {
            return '';
        }

        $phone = preg_replace('/\D+/', '', (string) $atts['phone']);
        if ($phone === '') {
            return '<!-- MSN: informe o telefone no shortcode msn_product_whatsapp -->';
        }

        $message = 'Olá! Gostaria de confirmar a compatibilidade deste produto: ' . $product->get_name();

        if ($product->get_sku()) {
            $message .= ' | SKU: ' . $product->get_sku();
        }

        $message .= ' | Link: ' . get_permalink($product->get_id());
        $url = 'https://wa.me/' . $phone . '?text=' . rawurlencode($message);

        return sprintf(
            '<a class="msn-product-whatsapp" href="%s" target="_blank" rel="noopener noreferrer">%s</a>',
            esc_url($url),
            esc_html($atts['label'])
        );
    }

    public static function cart_count_fragment(array $fragments): array
    {
        if (!self::is_woo_active() || !WC()->cart) {
            return $fragments;
        }

        $fragments['[data-msn-cart-count]'] = '<span class="msn-cart-link__count msn-header__cart-count msn-cart-count" data-msn-cart-count aria-live="polite">' . esc_html((string) WC()->cart->get_cart_contents_count()) . '</span>';

        return $fragments;
    }
}

MSN_WooCommerce_Layout_Bridge::init();
