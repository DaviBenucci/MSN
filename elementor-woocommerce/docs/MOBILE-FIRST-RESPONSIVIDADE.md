# Regras mobile-first e responsividade

Este projeto deve ser tratado como mobile-first. Como a maior parte dos usuarios acessa pelo celular, nenhuma pagina, section ou ajuste visual deve ser aprovado olhando primeiro para desktop.

## Regra de prioridade

1. Mobile real vem antes de desktop.
2. Aprovacao visual comeca em 360px, 375px, 390px, 412px e 430px.
3. Tablet vem depois: 768px, 820px e 1024px.
4. Desktop so pode ser aprovado depois que mobile e tablet estiverem sem quebras.
5. Se houver conflito entre densidade mobile e espacamento desktop, preserve a usabilidade mobile e ajuste desktop em breakpoint proprio.

## Regras obrigatorias de layout mobile

- Nao pode existir rolagem horizontal em 320px ou maior.
- Elementos clicaveis devem ter area minima de 44px de altura ou largura.
- Texto nao pode cortar, sobrepor, sair do card, sair do botao ou ficar escondido atras de header, banner ou barra fixa.
- Botoes principais devem aparecer cedo, especialmente em produto, carrinho e checkout.
- Formularios devem ser de uma coluna no mobile, com labels visiveis e campos largos.
- Cards de produto devem manter imagem, titulo, preco e CTA legiveis sem depender de hover.
- Header, busca, carrinho, WhatsApp e navegacao principal precisam continuar acessiveis em 360px.
- Quickbars, menus de categorias e filtros podem rolar horizontalmente, mas devem esconder a barra visual de scroll e manter o primeiro item totalmente visivel.
- Modais, filtros e banners de consentimento nao podem cobrir CTA de compra, campos de checkout, login/cadastro ou botoes de pagamento.
- Componentes sticky ou fixos devem respeitar `env(safe-area-inset-*)` quando estiverem proximos das bordas da tela.

## Regras obrigatorias de CSS

- Comece os estilos pelo comportamento mobile e aumente complexidade com `@media (min-width: ...)` quando criar algo novo.
- Em sections existentes que ja usam `max-width`, adicione ajustes mobile sem quebrar o padrao atual.
- Use `grid-template-columns: 1fr` no mobile para conteudos que nao precisam ficar lado a lado.
- Use `minmax(0, 1fr)` em grids para evitar overflow de texto, busca, preco e botoes.
- Use `max-width: 100%`, `min-width: 0` e `box-sizing: border-box` em wrappers com conteudo dinamico.
- Evite larguras fixas em px para cards, colunas, imagens e formularios.
- Use `clamp()` para espacamentos e tamanhos controlados, mas nunca para fonte gigante em painel, card ou botao.
- Nunca use `100vw` em containers internos quando houver padding lateral; prefira `width: 100%` ou `calc(100% - ...)`.
- Use `overflow-x: auto` somente em navegacao curta, filtros, tabelas inevitaveis ou carrosseis. Conteudo principal nao deve depender de scroll horizontal.
- Todo breakpoint mobile importante deve ser testado no navegador antes de aprovar.

## Regras para Elementor

- Configure primeiro o modo responsivo Mobile no Elementor e so depois ajuste Tablet e Desktop.
- Evite margens negativas para "encaixar" mobile. Corrija estrutura, gap, padding e grid.
- Slots WooCommerce devem continuar como Containers reais com widget WooCommerce ou Shortcode como filho. Nao coloque shortcode dentro de HTML widget.
- Cada section nova deve ser validada isoladamente em mobile antes de ser combinada com o restante da pagina.
- Ao usar Container do Elementor, revise `Direction`, `Wrap`, `Gap`, `Padding` e `Width` nos modos Mobile e Tablet.
- Nao esconda conteudo essencial no mobile para resolver quebra visual. Reorganize, compacte ou mova para acordeao quando fizer sentido.

## Regras por area critica

### Header

- Em mobile, logo, carrinho e busca precisam caber sem corte.
- A busca pode ocupar linha propria, mas nao deve ultrapassar a tela.
- A navegacao principal em mobile fica na quickbar simplificada.
- A quickbar mobile deve mostrar somente: Especialista, Mais Vendidos, Novidades, Minha Conta, Contato e Visite nosso outro site.
- Topbar deve mostrar apenas beneficios essenciais em telas pequenas.

### Loja e categorias

- Filtros devem abrir/fechar facilmente no mobile.
- Grade de produtos deve priorizar leitura de imagem, titulo, preco e CTA.
- Se o produto tiver nome longo, o card deve crescer sem sobrepor preco ou botao.

### Produto

- Preco, estoque e botao de compra devem aparecer cedo.
- Galeria nao pode empurrar o CTA para muito abaixo sem necessidade.
- Barra mobile de compra, quando usada, nao pode cobrir conteudo nem banner de consentimento.

### Carrinho e checkout

- Checkout mobile deve chegar aos campos principais rapidamente.
- Nao esconder campos obrigatorios do WooCommerce, Mercado Pago ou plugin brasileiro.
- Mensagens de erro, frete, pagamento e totais precisam ficar legiveis em 360px.
- Banner de consentimento nao pode cobrir finalizar compra, login, cupom, frete ou pagamento.

## Checklist minimo antes de aprovar qualquer mudanca visual

- [ ] 320px sem rolagem horizontal.
- [ ] 360px sem corte em header, busca, botoes, cards e formularios.
- [ ] 375px e 390px com CTA principal visivel e tocavel.
- [ ] 412px e 430px sem sobreposicao de textos ou botoes.
- [ ] 768px e 820px com layout de tablet organizado.
- [ ] 1024px sem quebra intermediaria.
- [ ] Teste em celular real quando a mudanca afetar checkout, produto, carrinho, conta ou header.
- [ ] Depois de salvar no Elementor, regenerar CSS, limpar cache e testar em aba anonima.
