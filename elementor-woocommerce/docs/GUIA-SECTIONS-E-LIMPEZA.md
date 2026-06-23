# Guia de sections e limpeza do workspace

Este projeto usa uma regra simples: paginas e templates ficam em `sections`. Arquivos combinados antigos nao devem voltar para o workspace.

## Estrutura oficial

Cada pagina/template deve seguir:

```text
components/<pagina>/sections/
```

Exemplos:

- `components/home/sections/01-hero.html`
- `components/home/sections/01-hero.css`
- `components/shop/sections/02-products-layout.js`

Use `.js` apenas quando a section tiver comportamento proprio. CSS e JS globais continuam em `shared/`.

## O que fica fora de sections

- `shared/msn-global-css.html`: tokens, base visual e ajustes WooCommerce globais.
- `shared/msn-global-js.html`: utilitarios globais pequenos no Footer.
- `components/product-card/*`: estilo reutilizavel para cards/Loop Grid.
- `msn-woocommerce-layout-bridge/*`: plugin da ponte WooCommerce.

## O que nao deve existir

Evite recriar arquivos combinados fora de `sections`, por exemplo:

```text
components/<pagina>/msn-*.html
components/<pagina>/msn-*.css
components/<pagina>/msn-*.js
```

Se uma pagina precisar de novo bloco, crie uma nova section numerada. Se um bloco antigo for substituido, remova o arquivo antigo no mesmo trabalho.

## Ordem de montagem

Leia o `README.md` dentro de cada pasta `sections`. Ele informa a ordem dos blocos e quais scripts carregar.

Toda section deve nascer ou ser revisada com regra mobile-first:

- Primeiro valide 360px no Elementor.
- Depois confira 375px, 390px, 412px e 430px.
- So avance para tablet e desktop quando o mobile estiver sem corte, sobreposicao ou rolagem horizontal.
- Use `MOBILE-FIRST-RESPONSIVIDADE.md` como regra de aceite.

Para CSS, escolha uma das duas formas:

- Colar CSS da section junto do bloco quando o Elementor permitir.
- Juntar os CSS das sections usadas no CSS da pagina/template.

Para JS, carregue apenas os scripts das sections presentes na pagina.

## Limpeza obrigatoria

Antes de finalizar qualquer mudanca:

1. Rode uma busca por arquivos combinados antigos fora de `sections`.
2. Confirme que cada pagina tem apenas `sections`.
3. Remova arquivos substituidos no mesmo PR/tarefa.
4. Revalide mobile pelo checklist de `MOBILE-FIRST-RESPONSIVIDADE.md`.
5. Atualize `README.md`, `GUIA-DE-INSTALACAO.md` e `MAPA-DE-COMPONENTES.md` quando criar, mover ou apagar sections.

## WooCommerce

Dados vivos de produto podem vir da bridge `data-msn-products` ou de widgets/shortcodes nativos. Carrinho, checkout, conta, frete, cupom, pagamento e variacoes continuam nativos do WooCommerce.
