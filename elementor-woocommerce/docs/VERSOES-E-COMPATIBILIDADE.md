# Versoes e compatibilidade

Data da pesquisa: 2026-06-15.

## Ambiente observado

- WordPress: 7.0 no rodape do admin.
- Elementor: 4.1.3.
- Elementor Pro: 4.1.1.
- WooCommerce: 10.8.1.
- Product Filter for WooCommerce by WBW: 3.1.7.
- WP Rocket: 3.21.1.
- WooPayments: 10.8.0.
- Mercado Pago: 8.7.24.

## Elementor 4.1.3

Fonte oficial: https://wordpress.org/plugins/elementor/

Pontos relevantes:

- 4.1.3 corrige erro de screenshot da Cloud Library que podia impedir salvar templates localmente.
- 4.1.2 corrige falhas ligadas a Global Classes e estilos faltando no site publicado.
- 4.1.1 reforca seguranca no tratamento de conteudo/templates e corrige problema em filtros.
- 4.1.0 introduz Design System para Variables e Classes, Angie no Atomic Editor e aumenta dependencias/expectativas do fluxo Atomic.

Impacto pratico:

- Evitar depender de classes globais recem-criadas sem publicar/salvar novamente o template.
- Depois de colar CSS/JS, salvar template, regenerar CSS do Elementor e limpar cache.
- Para codigo customizado, preferir HTML Widget com `<style>` e `<script>` quando o codigo estiver no proprio elemento.

## Elementor Pro 4.1.1

Fonte oficial: https://elementor.com/pro/changelog/

Pontos relevantes:

- Corrige contagem de Live Results em tablet/mobile no Search widget.
- Corrige erro com Taxonomy Filter em Loop Grid baseado em Current Query.
- A serie 4.1 adiciona elementos Atomic Form e recursos de Atomic Editor em templates de Loop Grid.

Impacto pratico:

- Para loja/categoria/busca, usar Loop Grid do tipo `Products`.
- Em arquivos de loja/categoria/busca, usar Source = `Current Query`.
- Se usar Taxonomy Filter do Elementor com Loop Grid e aparecer erro, limpar cache, salvar novamente o template e testar sem plugins de cache.

## WooCommerce 10.8.1

Fonte oficial: https://developer.woocommerce.com/2026/05/28/woocommerce-10-8-1-release/

Pontos relevantes:

- 10.8.1 e uma correcao de 10.8.0.
- Corrige regressao no onboarding do WooPayments.
- Corrige erro fatal em upgrades in-place vindos da versao 10.7.

Impacto pratico:

- Nao montar produto por variaveis manuais no HTML.
- Usar widgets/shortcodes nativos: `[products]`, `[woocommerce_cart]`, `[woocommerce_checkout]`, `[woocommerce_my_account]`.
- Preco, estoque, imagem, botao de compra e variacoes devem vir do WooCommerce.

## WooCommerce shortcodes

Fonte oficial: https://woocommerce.com/document/woocommerce-shortcodes/

Shortcodes uteis para este projeto:

```text
[products limit="12" columns="3" paginate="true" visibility="visible"]
[products category="toner" limit="12" columns="3" paginate="true"]
[woocommerce_cart]
[woocommerce_checkout]
[woocommerce_my_account]
```

Observacao:

- Shortcode deve ir em widget Shortcode, nao em widget HTML comum.
- O HTML widget nao processa shortcode de forma confiavel em todos os contextos.

## Product Filter by WBW

Fonte oficial: https://woobewoo.com/documentation/getting-started-with-woocommerce-filter/

Pontos relevantes:

- O plugin permite inserir filtro por shortcode copiado do proprio painel.
- Tambem possui widget Elementor `Woofilters`.
- O filtro deve ser configurado no painel do plugin e depois selecionado no Elementor.

Impacto pratico:

- Nao usar formularios manuais com `filter_marca`, `stock_status` etc.
- Use o shortcode/widget do WBW para ele gerar a query correta.
- Antes de filtros por marca/compatibilidade, padronize atributos e categorias dos produtos.

## Ordem segura depois de alterar codigo

1. Salvar template do Elementor.
2. Elementor > Ferramentas > Regenerar CSS e Dados.
3. Limpar cache do WP Rocket.
4. Limpar cache do navegador.
5. Testar em aba anonima.
6. Se produtos nao aparecem, desativar temporariamente filtro/cache e testar apenas `[products limit="12" columns="3"]`.
