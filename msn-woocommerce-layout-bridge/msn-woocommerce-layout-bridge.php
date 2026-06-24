<?php
/**
 * Plugin Name: MSN WooCommerce Layout Bridge
 * Description: Camada segura de dados entre WooCommerce, Elementor e componentes HTML/CSS/JS da MSN Distribuidora.
 * Version: 1.1.7
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
    private const VERSION = '1.1.7';
    private const REST_NAMESPACE = 'msn/v1';
    private const MERCADO_PAGO_CUSTOM_CHECKOUT_SCRIPT = 'wc_mercadopago_custom_checkout';
    private const MERCADO_PAGO_CART_PAYMENT_SCRIPTS = [
        'wc_mercadopago_woocommerce_scripts',
        'wc_mercadopago_health_monitor',
        'wc_mercadopago_checkout_error_dispatcher',
        'wc_mercadopago_checkout_fields_dispatcher',
        'wc_mercadopago_checkout_session_data_register',
        'wc_mercadopago_checkout_components',
        'wc_mercadopago_checkout_update',
        'wc_mercadopago_checkout_metrics',
        'wc_mercadopago_sdk_metrics',
        'wc_mercadopago_security_session',
        'wc_mercadopago_sdk',
        'wc_mercadopago_custom_card_form',
        'wc_mercadopago_custom_three_ds_handler',
        'wc_mercadopago_custom_mobile_checkout_classic_observer',
        'wc_mercadopago_custom_event_handler',
        'wc_mercadopago_custom_page',
        'wc_mercadopago_custom_elements',
        'wc_mercadopago_supertoken',
        'wc_mercadopago_ticket_page',
        'wc_mercadopago_ticket_elements',
        'wc_mercadopago_ticket_checkout',
    ];

    public static function init(): void
    {
        add_action('wp_enqueue_scripts', [__CLASS__, 'enqueue_assets']);
        add_action('wp_enqueue_scripts', [__CLASS__, 'dequeue_mercado_pago_scripts_outside_checkout'], 100);
        add_action('wp_head', [__CLASS__, 'print_critical_header_css'], 1);
        add_action('wp_head', [__CLASS__, 'print_google_cookie_domain_config'], 2);
        add_action('rest_api_init', [__CLASS__, 'register_rest_routes']);
        add_filter('rocket_delay_js_exclusions', [__CLASS__, 'exclude_catalog_wp_dependencies_from_rocket_delay']);
        add_filter('rocket_exclude_defer_js', [__CLASS__, 'exclude_catalog_wp_dependencies_from_rocket_delay']);
        add_filter('rocket_exclude_js', [__CLASS__, 'exclude_catalog_wp_dependencies_from_rocket_delay']);
        add_filter('rocket_defer_inline_exclusions', [__CLASS__, 'exclude_catalog_wp_inline_dependencies_from_rocket']);
        add_filter('rocket_excluded_inline_js_content', [__CLASS__, 'exclude_catalog_wp_inline_dependencies_from_rocket']);
        add_filter('script_loader_tag', [__CLASS__, 'add_nowprocket_to_catalog_dependency_scripts'], 10, 3);
        add_filter('woocommerce_checkout_fields', [__CLASS__, 'customize_brazilian_checkout_fields'], 20);
        add_action('woocommerce_checkout_process', [__CLASS__, 'validate_brazilian_checkout_fields']);
        add_action('woocommerce_checkout_create_order', [__CLASS__, 'save_brazilian_checkout_order_fields'], 20, 2);
        add_action('woocommerce_checkout_update_order_meta', [__CLASS__, 'save_brazilian_checkout_order_meta'], 20);
        add_action('woocommerce_checkout_update_user_meta', [__CLASS__, 'save_brazilian_checkout_customer_fields'], 20, 2);
        add_action('woocommerce_admin_order_data_after_billing_address', [__CLASS__, 'display_admin_billing_cpf']);

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
            'window.MSNWoo = ' . self::json_encode_for_script(self::get_bootstrap_data(false)) . ';',
            'before'
        );
    }

    public static function print_critical_header_css(): void
    {
        echo <<<'HTML'
<style id="msn-woo-layout-critical-header">
:root{--msn-primary:#0f3d5e;--msn-primary-dark:#082f49;--msn-primary-soft:#eaf4ff;--msn-accent:#0ea5e9;--msn-success:#10b981;--msn-bg:#f4f7fa;--msn-bg-soft:#eef6fb;--msn-surface:#fff;--msn-surface-alt:#f8fafc;--msn-text:#111827;--msn-muted:#64748b;--msn-border:#dbe7f0;--msn-border-strong:#bfdbfe;--msn-radius:8px;--msn-font-sans:Inter,Roboto,Arial,sans-serif;--msn-font-display:Poppins,Montserrat,Inter,Roboto,Arial,sans-serif}
.msn-header{position:sticky;top:0;z-index:999;width:100%;max-width:100%;border-bottom:1px solid var(--msn-border,#dbe7f0);background:rgba(255,255,255,.96);color:var(--msn-text,#111827);box-shadow:0 1px 0 rgba(15,23,42,.03);container:msn-header/inline-size}
.msn-header,.msn-header *{box-sizing:border-box;min-width:0}
.msn-header__topbar{display:flex;max-width:100%;align-items:center;justify-content:center;gap:16px;overflow:hidden;background:var(--msn-primary-dark,#082f49);color:#fff;padding:7px 16px;font:850 .78rem/1.2 var(--msn-font-sans,Arial,sans-serif);white-space:nowrap}
.msn-header__topbar span,.msn-header__topbar a{display:inline-flex;align-items:center;gap:8px;color:#fff!important;text-decoration:none!important}
.msn-header__main{display:grid!important;grid-template-areas:"brand search actions";grid-template-columns:minmax(190px,270px) minmax(220px,1fr) auto;align-items:center;gap:clamp(12px,1.7vw,24px);width:min(calc(100% - 32px),1180px);max-width:1180px;margin-inline:auto;padding-block:12px}
.msn-header__logo{grid-area:brand;display:inline-flex;align-items:center;gap:12px;color:var(--msn-primary,#0f3d5e);text-decoration:none}
.msn-header__logo img{width:74px;height:auto;flex:0 0 auto;object-fit:contain}
.msn-header__logo span{display:block;min-width:0}
.msn-header__logo strong,.msn-header__logo small{display:block;line-height:1.15}
.msn-header__logo strong{font-family:var(--msn-font-display,Arial,sans-serif);font-size:1rem;font-weight:950;letter-spacing:0}
.msn-header__logo small{margin-top:3px;color:var(--msn-muted,#64748b);font-size:.76rem;font-weight:800}
.msn-header__search-slot{grid-area:search;display:grid;width:100%;min-width:0;max-width:100%;gap:6px;justify-self:stretch}
.msn-header__search-kicker{color:var(--msn-muted,#64748b);font-size:.72rem;font-weight:900;letter-spacing:0;text-transform:uppercase}
.msn-header__search,.msn-header__search-slot .woocommerce-product-search,.msn-header__search-slot .wp-block-search__inside-wrapper,.msn-header__search-slot form.woocommerce-product-search{display:flex!important;flex-direction:row!important;width:100%;min-width:0;min-height:46px;align-items:stretch;overflow:hidden;border:1px solid var(--msn-border,#dbe7f0);border-radius:999px;background:var(--msn-surface,#fff);box-shadow:inset 0 1px 2px rgba(15,23,42,.04)}
.msn-header__search-slot:not(:has(input[type="search"]))::after{content:"";display:block;width:100%;min-height:46px;border:1px solid var(--msn-border,#dbe7f0);border-radius:999px;background:linear-gradient(90deg,var(--msn-surface,#fff) 0%,var(--msn-bg-soft,#eef6fb) 48%,var(--msn-surface,#fff) 100%)}
.msn-header__search input,.msn-header__search-slot .search-field,.msn-header__search-slot .wp-block-search__input,.msn-header__search-slot input[type="search"]{width:0;min-width:0;min-height:46px;flex:1 1 0%;border:0!important;background:transparent!important;color:var(--msn-text,#111827)!important;padding:0 18px;box-shadow:none!important;font:inherit;outline:0;appearance:none}
.msn-header__search button,.msn-header__search-slot .wp-block-search__button,.msn-header__search-slot button,.msn-header__search-slot input[type="submit"]{display:inline-flex!important;min-width:clamp(88px,9vw,108px);min-height:46px;align-items:center;justify-content:center;border:0!important;border-radius:0!important;background:var(--msn-primary,#0f3d5e)!important;color:#fff!important;padding:0 clamp(14px,1.6vw,20px)!important;box-shadow:none!important;font-size:.92rem;font-weight:950;line-height:1;text-decoration:none!important;white-space:nowrap;cursor:pointer;appearance:none}
.msn-header__actions{grid-area:actions;display:flex;align-items:center;justify-content:flex-end;gap:8px}
.msn-header__action-link{display:inline-flex;min-height:42px;align-items:center;justify-content:center;gap:8px;border:1px solid var(--msn-border,#dbe7f0);border-radius:999px;background:var(--msn-surface,#fff);color:var(--msn-text,#111827);padding:0 13px;font-size:.86rem;font-weight:900;text-decoration:none}
.msn-header__action-icon{display:inline-grid;width:22px;height:22px;place-items:center;border-radius:999px;background:var(--msn-primary-soft,#eaf4ff);color:var(--msn-primary,#0f3d5e);font-size:.7rem;font-weight:950;line-height:1}
.msn-header__cart{position:relative}.msn-header__cart-icon{display:block;width:19px;height:19px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2}.msn-header__cart-count{display:inline-grid;min-width:21px;height:21px;place-items:center;border-radius:999px;background:var(--msn-primary,#0f3d5e);color:#fff;font-size:.72rem;font-weight:950;line-height:1}.msn-header__cart-count[hidden]{display:none}
.msn-header__quickbar{display:flex!important;width:100%;max-width:100%;align-items:center;justify-content:center;gap:8px;overflow:hidden;border-top:1px solid var(--msn-border,#dbe7f0);background:var(--msn-surface-alt,#f8fafc);padding:8px 16px}
.msn-header__quickbar a{display:inline-flex;min-height:34px;align-items:center;justify-content:center;border:1px solid transparent;border-radius:999px;color:var(--msn-text,#111827)!important;padding:0 12px;font-size:.86rem;font-weight:850;line-height:1.1;text-decoration:none!important;white-space:nowrap}
.msn-header__quickbar-label--short,.msn-header__quickbar-mobile-only{display:none!important}
@media (max-width:1200px){.msn-header__main{grid-template-areas:"brand actions" "search search";grid-template-columns:minmax(0,1fr) auto;gap:10px 14px}.msn-header__action-link:not(.msn-header__cart){display:none!important}.msn-header__cart{display:inline-flex!important;width:46px;height:46px;padding:0;border-radius:var(--msn-radius,8px)}.msn-header__cart-label{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.msn-header__quickbar{justify-content:flex-start;overflow-x:auto;overflow-y:hidden;padding:8px 12px;scrollbar-width:none;-webkit-overflow-scrolling:touch}.msn-header__quickbar::-webkit-scrollbar{display:none}.msn-header__quickbar a{min-height:36px;flex:0 0 auto;border-color:var(--msn-border,#dbe7f0);background:var(--msn-surface,#fff);font-size:.82rem}}
@media (max-width:1024px){.msn-header__main{width:min(calc(100% - 24px),1180px);gap:10px 12px;padding-block:9px}.msn-header__logo{gap:10px}.msn-header__logo img{width:62px}.msn-header__logo strong{font-size:.92rem}.msn-header__logo small{font-size:.72rem}.msn-header__cart{width:44px;height:44px}.msn-header__cart-count{position:absolute;top:-7px;right:-7px;min-width:20px;height:20px;border:2px solid var(--msn-surface,#fff);font-size:.68rem}.msn-header__search-kicker{display:none}.msn-header__search,.msn-header__search-slot .woocommerce-product-search,.msn-header__search-slot .wp-block-search__inside-wrapper,.msn-header__search-slot form.woocommerce-product-search{min-height:42px;max-height:42px}.msn-header__search-slot:not(:has(input[type="search"]))::after{min-height:42px;max-height:42px}.msn-header__search input,.msn-header__search-slot .search-field,.msn-header__search-slot .wp-block-search__input,.msn-header__search-slot input[type="search"]{min-height:42px;padding-inline:14px}.msn-header__search button,.msn-header__search-slot .wp-block-search__button,.msn-header__search-slot button,.msn-header__search-slot input[type="submit"]{min-width:86px;min-height:42px;padding-inline:14px!important;font-size:.86rem}}
@media (max-width:640px){.msn-header__quickbar-mobile-hide{display:none!important}.msn-header__quickbar-mobile-only{display:inline-flex!important}.msn-header__quickbar-label{display:none}.msn-header__quickbar-label--short{display:inline!important}}
@media (max-width:520px){.msn-header__main{width:min(calc(100% - 20px),1180px);gap:8px 10px}.msn-header__logo{gap:8px}.msn-header__logo img{width:56px}.msn-header__logo strong{font-size:.88rem}.msn-header__logo small{display:none}.msn-header__search-slot{justify-items:stretch}.msn-header__search-slot .elementor-widget,.msn-header__search-slot .elementor-widget-container,.msn-header__search-slot .msn-product-search-slot{width:100%;max-width:100%}.msn-header__topbar span:nth-of-type(n+2){display:none}}
@media (max-width:420px){.msn-header__search input,.msn-header__search-slot .search-field,.msn-header__search-slot .wp-block-search__input,.msn-header__search-slot input[type="search"]{padding-inline:12px}.msn-header__search button,.msn-header__search-slot .wp-block-search__button,.msn-header__search-slot button,.msn-header__search-slot input[type="submit"]{min-width:78px;padding-inline:12px!important}}
</style>
HTML;
    }

    public static function print_google_cookie_domain_config(): void
    {
        $cookie_domain = self::get_first_party_cookie_domain();

        if ($cookie_domain === '') {
            return;
        }

        echo '<script id="msn-google-cookie-domain-config">';
        echo 'window.dataLayer=window.dataLayer||[];';
        echo 'function gtag(){window.dataLayer.push(arguments);}';
        echo 'gtag("set","cookie_domain",' . self::json_encode_for_script($cookie_domain) . ');';
        echo 'gtag("set","linker",{"domains":[' . self::json_encode_for_script($cookie_domain) . ']});';
        echo '</script>';
    }

    private static function get_first_party_cookie_domain(): string
    {
        $host = wp_parse_url(home_url('/'), PHP_URL_HOST);

        if (!is_string($host) || $host === '') {
            return '';
        }

        $host = strtolower(trim($host));
        $host = preg_replace('/^www\./', '', $host);

        if (!is_string($host) || $host === '' || strpos($host, '.') === false) {
            return '';
        }

        if (filter_var($host, FILTER_VALIDATE_IP)) {
            return '';
        }

        return sanitize_text_field($host);
    }

    public static function customize_brazilian_checkout_fields(array $fields): array
    {
        if (!isset($fields['billing']) || !is_array($fields['billing'])) {
            $fields['billing'] = [];
        }

        if (isset($fields['billing']['billing_phone']) && is_array($fields['billing']['billing_phone'])) {
            $phone_field = $fields['billing']['billing_phone'];

            $fields['billing']['billing_phone'] = array_merge($phone_field, [
                'label'        => __('Telefone', 'msn-woocommerce-layout-bridge'),
                'placeholder'  => __('(11) 99999-9999', 'msn-woocommerce-layout-bridge'),
                'required'     => true,
                'type'         => 'tel',
                'class'        => self::checkout_field_classes($phone_field['class'] ?? [], 'form-row-first'),
                'input_class'  => self::merge_html_classes($phone_field['input_class'] ?? [], ['msn-checkout-phone-field']),
                'autocomplete' => 'tel',
                'priority'     => 24,
            ]);
        }

        $cpf_field = isset($fields['billing']['billing_cpf']) && is_array($fields['billing']['billing_cpf'])
            ? $fields['billing']['billing_cpf']
            : [];

        $fields['billing']['billing_cpf'] = array_merge($cpf_field, [
            'type'              => 'text',
            'label'             => __('CPF', 'msn-woocommerce-layout-bridge'),
            'placeholder'       => __('000.000.000-00', 'msn-woocommerce-layout-bridge'),
            'required'          => true,
            'class'             => self::checkout_field_classes($cpf_field['class'] ?? [], 'form-row-last'),
            'input_class'       => self::merge_html_classes($cpf_field['input_class'] ?? [], ['msn-checkout-cpf-field']),
            'clear'             => true,
            'priority'          => 25,
            'custom_attributes' => array_merge($cpf_field['custom_attributes'] ?? [], [
                'autocomplete' => 'off',
                'inputmode'    => 'numeric',
                'maxlength'    => '14',
            ]),
        ]);

        return $fields;
    }

    public static function validate_brazilian_checkout_fields(): void
    {
        if (!function_exists('wc_add_notice')) {
            return;
        }

        $phone_digits = self::only_digits(self::get_posted_checkout_field('billing_phone'));

        if ($phone_digits === '') {
            wc_add_notice(__('Informe um telefone para contato.', 'msn-woocommerce-layout-bridge'), 'error');
        } elseif (strlen($phone_digits) < 10 || strlen($phone_digits) > 11) {
            wc_add_notice(__('Informe um telefone brasileiro valido, com DDD.', 'msn-woocommerce-layout-bridge'), 'error');
        }

        $cpf = self::get_posted_checkout_field('billing_cpf');

        if ($cpf === '') {
            wc_add_notice(__('Informe o CPF do titular.', 'msn-woocommerce-layout-bridge'), 'error');
        } elseif (!self::is_valid_cpf($cpf)) {
            wc_add_notice(__('Informe um CPF valido para continuar o pagamento.', 'msn-woocommerce-layout-bridge'), 'error');
        }
    }

    public static function save_brazilian_checkout_order_fields($order, array $data): void
    {
        if (!is_object($order) || !method_exists($order, 'update_meta_data')) {
            return;
        }

        $cpf = self::format_cpf(self::get_posted_checkout_field('billing_cpf'));

        if ($cpf === '') {
            return;
        }

        $order->update_meta_data('_billing_cpf', $cpf);
        $order->update_meta_data('billing_cpf', $cpf);
    }

    public static function save_brazilian_checkout_order_meta($order_id): void
    {
        if (!function_exists('wc_get_order')) {
            return;
        }

        $order = wc_get_order(absint($order_id));

        if (!is_object($order) || !method_exists($order, 'update_meta_data')) {
            return;
        }

        self::save_brazilian_checkout_order_fields($order, []);

        if (method_exists($order, 'save')) {
            $order->save();
        }
    }

    public static function save_brazilian_checkout_customer_fields($customer_id, array $posted): void
    {
        $customer_id = absint($customer_id);

        if ($customer_id <= 0) {
            return;
        }

        $cpf_source = isset($posted['billing_cpf']) ? (string) $posted['billing_cpf'] : self::get_posted_checkout_field('billing_cpf');
        $cpf = self::format_cpf($cpf_source);

        if ($cpf !== '') {
            update_user_meta($customer_id, 'billing_cpf', $cpf);
        }
    }

    public static function display_admin_billing_cpf($order): void
    {
        if (!is_object($order) || !method_exists($order, 'get_meta')) {
            return;
        }

        $cpf = (string) $order->get_meta('_billing_cpf');

        if ($cpf === '') {
            $cpf = (string) $order->get_meta('billing_cpf');
        }

        if ($cpf === '') {
            return;
        }

        echo '<p><strong>' . esc_html__('CPF', 'msn-woocommerce-layout-bridge') . ':</strong> ' . esc_html($cpf) . '</p>';
    }

    private static function checkout_field_classes($existing_classes, string $row_class): array
    {
        $classes = self::merge_html_classes($existing_classes, []);
        $classes = array_values(array_filter($classes, static function (string $class): bool {
            return !in_array($class, ['form-row-first', 'form-row-last', 'form-row-wide'], true);
        }));

        if (!in_array($row_class, $classes, true)) {
            $classes[] = $row_class;
        }

        return $classes;
    }

    private static function merge_html_classes($existing_classes, array $required_classes): array
    {
        $classes = is_array($existing_classes) ? $existing_classes : [$existing_classes];
        $classes = array_filter(array_map(static function ($class): string {
            return sanitize_html_class((string) $class);
        }, $classes));

        foreach ($required_classes as $required_class) {
            $required_class = sanitize_html_class($required_class);

            if ($required_class !== '' && !in_array($required_class, $classes, true)) {
                $classes[] = $required_class;
            }
        }

        return array_values($classes);
    }

    private static function get_posted_checkout_field(string $key): string
    {
        if (!isset($_POST[$key])) {
            return '';
        }

        return sanitize_text_field(wp_unslash($_POST[$key]));
    }

    private static function only_digits(string $value): string
    {
        return preg_replace('/\D+/', '', $value) ?: '';
    }

    private static function format_cpf(string $cpf): string
    {
        $digits = self::only_digits($cpf);

        if (strlen($digits) !== 11) {
            return sanitize_text_field($cpf);
        }

        return substr($digits, 0, 3) . '.' . substr($digits, 3, 3) . '.' . substr($digits, 6, 3) . '-' . substr($digits, 9, 2);
    }

    private static function is_valid_cpf(string $cpf): bool
    {
        $digits = self::only_digits($cpf);

        if (strlen($digits) !== 11 || preg_match('/^(\d)\1{10}$/', $digits)) {
            return false;
        }

        for ($position = 9; $position < 11; $position++) {
            $sum = 0;

            for ($index = 0; $index < $position; $index++) {
                $sum += (int) $digits[$index] * (($position + 1) - $index);
            }

            $check_digit = ((10 * $sum) % 11) % 10;

            if ((int) $digits[$position] !== $check_digit) {
                return false;
            }
        }

        return true;
    }

    public static function exclude_catalog_wp_dependencies_from_rocket_delay($exclusions): array
    {
        if (!is_array($exclusions)) {
            $exclusions = [];
        }

        if (!self::is_catalog_script_dependency_context()) {
            return $exclusions;
        }

        $required_exclusions = [
            '/wp-includes/js/dist/private-apis',
            '/wp-includes/js/dist/data',
            '/wp-includes/js/dist/data-controls',
            '/wp-includes/js/dist/dom-ready',
            '/wp-includes/js/dist/hooks',
            '/wp-includes/js/dist/i18n',
            '/wp-includes/js/dist/api-fetch',
            '/wp-includes/js/dist/url',
            '/wp-content/plugins/wordpress-seo/assets/js/dist/frontend-inspector',
            '/wp-content/plugins/wordpress-seo-premium/assets/js/dist/frontend-inspector',
            'private-apis.min.js',
            'data.min.js',
            'frontend-inspector',
            'wp-private-apis-js',
            'wp-data-js-after',
            'wp.data.use',
            'wp.data.register',
            'wp.apiFetch.use',
            'wp.i18n.setLocaleData',
        ];

        foreach ($required_exclusions as $required_exclusion) {
            if (!in_array($required_exclusion, $exclusions, true)) {
                $exclusions[] = $required_exclusion;
            }
        }

        return $exclusions;
    }

    public static function exclude_catalog_wp_inline_dependencies_from_rocket($exclusions): array
    {
        if (!is_array($exclusions)) {
            $exclusions = [];
        }

        if (!self::is_catalog_script_dependency_context()) {
            return $exclusions;
        }

        $required_exclusions = [
            'wp-private-apis-js-after',
            'wp-data-js-after',
            'wp-api-fetch-js-after',
            'wp-i18n-js-after',
            'wp-hooks-js-after',
            'wp-url-js-after',
            '__dangerousOptInToUnstableAPIsOnlyForCoreModules',
            'wp.data.use',
            'wp.data.register',
            'wp.apiFetch.use',
            'wp.i18n.setLocaleData',
            'frontend-inspector',
        ];

        foreach ($required_exclusions as $required_exclusion) {
            if (!in_array($required_exclusion, $exclusions, true)) {
                $exclusions[] = $required_exclusion;
            }
        }

        return $exclusions;
    }

    public static function add_nowprocket_to_catalog_dependency_scripts(string $tag, string $handle, string $src): string
    {
        if (!self::is_catalog_script_dependency_context() || strpos($tag, ' nowprocket') !== false) {
            return $tag;
        }

        $protected_handles = [
            'wp-private-apis',
            'wp-data',
            'wp-data-controls',
            'wp-dom-ready',
            'wp-hooks',
            'wp-i18n',
            'wp-api-fetch',
            'wp-url',
        ];

        $protected_src_parts = [
            '/wp-includes/js/dist/private-apis',
            '/wp-includes/js/dist/data',
            '/wp-includes/js/dist/data-controls',
            '/wp-includes/js/dist/dom-ready',
            '/wp-includes/js/dist/hooks',
            '/wp-includes/js/dist/i18n',
            '/wp-includes/js/dist/api-fetch',
            '/wp-includes/js/dist/url',
            '/wp-content/plugins/wordpress-seo/assets/js/dist/frontend-inspector',
            '/wp-content/plugins/wordpress-seo-premium/assets/js/dist/frontend-inspector',
        ];

        $should_protect = in_array($handle, $protected_handles, true);

        if (!$should_protect) {
            foreach ($protected_src_parts as $protected_src_part) {
                if (strpos($src, $protected_src_part) !== false) {
                    $should_protect = true;
                    break;
                }
            }
        }

        if (!$should_protect) {
            return $tag;
        }

        return preg_replace('/^<script\b/', '<script nowprocket', $tag, 1) ?: $tag;
    }

    private static function is_catalog_script_dependency_context(): bool
    {
        return (function_exists('is_shop') && is_shop())
            || (function_exists('is_product_category') && is_product_category())
            || (function_exists('is_product_tag') && is_product_tag())
            || (function_exists('is_product_taxonomy') && is_product_taxonomy())
            || (function_exists('is_search') && is_search() && get_query_var('post_type') === 'product');
    }

    public static function dequeue_mercado_pago_scripts_outside_checkout(): void
    {
        if (self::is_mercado_pago_checkout_context()) {
            return;
        }

        $script_handles = [self::MERCADO_PAGO_CUSTOM_CHECKOUT_SCRIPT];

        if (function_exists('is_cart') && is_cart()) {
            $script_handles = array_merge($script_handles, self::MERCADO_PAGO_CART_PAYMENT_SCRIPTS);
        }

        foreach (array_unique($script_handles) as $script_handle) {
            if (wp_script_is($script_handle, 'enqueued')) {
                wp_dequeue_script($script_handle);
            }
        }
    }

    private static function is_mercado_pago_checkout_context(): bool
    {
        return (function_exists('is_checkout') && is_checkout())
            || (function_exists('is_checkout_pay_page') && is_checkout_pay_page())
            || (function_exists('is_add_payment_method_page') && is_add_payment_method_page())
            || (function_exists('get_query_var') && (bool) get_query_var('order-pay'));
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
                'search' => [
                    'sanitize_callback' => 'sanitize_text_field',
                ],
                's' => [
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

    private static function json_encode_for_script($data): string
    {
        $json = wp_json_encode($data, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT);

        return is_string($json) ? $json : 'null';
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

        $search = sanitize_text_field((string) ($request->get_param('search') ?: $request->get_param('s')));
        if ($search !== '') {
            $args['search'] = $search;
            $args['s'] = $search;
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
            'displayName' => '',
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
            $term_link = get_term_link($term);

            $categories[] = [
                'id'     => absint($term->term_id),
                'name'   => sanitize_text_field($term->name),
                'slug'   => sanitize_title($term->slug),
                'count'  => absint($term->count),
                'parent' => absint($term->parent),
                'url'    => is_wp_error($term_link) ? '' : esc_url_raw($term_link),
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
            $term_link = get_term_link($term);

            return [
                'id'   => absint($term->term_id),
                'name' => sanitize_text_field($term->name),
                'slug' => sanitize_title($term->slug),
                'url'  => is_wp_error($term_link) ? '' : esc_url_raw($term_link),
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

        if (!is_array($data)) {
            return '<script type="application/json" class="msn-product-data">{}</script>';
        }

        return '<script type="application/json" class="msn-product-data" data-product-id="' . esc_attr($product->get_id()) . '">' . self::json_encode_for_script($data) . '</script>';
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

        if (!is_array($data)) {
            return '<!-- MSN: produto nao publicado ou indisponivel -->';
        }

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
        <article class="msn-product-card msn-bridge-product-card" data-msn-product='<?php echo esc_attr(self::json_encode_for_script($data)); ?>'>
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

        $message = 'Olá! Gostaria de confirmar a compatibilidade deste produto: ' . wp_strip_all_tags($product->get_name());

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
