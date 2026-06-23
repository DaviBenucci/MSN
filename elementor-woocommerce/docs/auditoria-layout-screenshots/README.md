# Prints de referencia para refinamento visual

Captura feita em 2026-06-23 usando o link de pre-visualizacao com `woo-share`.

Use estes arquivos como referencia diagnostica para o proximo ciclo de layout. Eles nao sao proposta visual final; mostram o estado real encontrado no site publicado em pre-visualizacao.

## Como usar em um chat novo

Peca para o novo chat ler primeiro:

```text
elementor-woocommerce/docs/AUDITORIA-LAYOUT-E-CHECKOUT-MERCADO-PAGO.md
elementor-woocommerce/docs/auditoria-layout-screenshots/README.md
```

Depois, peca para abrir os prints mais relevantes com `view_image` antes de editar CSS.

## Prints principais

- `desktop-checkout-com-banner.png`: checkout com produto no carrinho antes de aceitar consentimento. Mostra o banner interferindo em area critica.
- `desktop-checkout.png`: checkout desktop com produto e consentimento aceito. Bom para revisar altura do hero, dobra inicial e distancia ate os campos.
- `mobile-checkout.png`: checkout mobile. Mostra que o usuario passa por muito conteudo antes de chegar ao primeiro campo.
- `desktop-produto.png`: produto individual desktop. Ajuda a revisar proporcao de imagem, coluna de compra, CTA e espacos verticais.
- `mobile-produto.png`: produto individual mobile. Use para checar se preco, estoque e CTA aparecem cedo o bastante.
- `desktop-loja.png`: grid de produtos desktop. Ajuda a avaliar densidade, alinhamento, tamanhos de imagem e leitura de preco.
- `mobile-loja.png`: grid/listagem em mobile. Use para revisar ritmo vertical e visibilidade de produtos.
- `desktop-minha-conta.png` e `mobile-minha-conta.png`: login/cadastro. Use para ajustar proximidade entre hero e formularios.

## Acervo completo

Desktop:

- `desktop-home.png`
- `desktop-loja.png`
- `desktop-produto.png`
- `desktop-carrinho.png`
- `desktop-checkout-com-banner.png`
- `desktop-checkout.png`
- `desktop-contato.png`
- `desktop-minha-conta.png`
- `desktop-privacidade.png`
- `desktop-devolucao.png`

Mobile:

- `mobile-home.png`
- `mobile-loja.png`
- `mobile-produto.png`
- `mobile-checkout.png`
- `mobile-minha-conta.png`

## Pontos visuais observados

- O banner de consentimento pode cobrir botoes, campos e conteudos importantes.
- Algumas primeiras secoes usam muito espaco vertical antes dos campos ou acoes principais.
- No checkout mobile, a etapa do formulario fica abaixo da primeira dobra, depois de titulo, texto lateral e barra de progresso.
- O header mobile mostra a busca como um grande elemento visual; verificar se ela deve ocupar esse peso em paginas de fluxo como checkout e conta.
- Produto individual e checkout precisam priorizar CTA/campos acima da dobra sem remover informacoes de confianca.
- Loja e produto estao em modo claro e visiveis; a melhoria agora e de densidade, hierarquia e polimento.

## Regras ao estilizar

- Nao substituir widgets/shortcodes WooCommerce por HTML manual.
- Nao esconder campos obrigatorios de WooCommerce, Fluid Checkout ou Mercado Pago.
- Nao mexer em preco, estoque, frete, pagamento, carrinho ou variacoes por JavaScript customizado.
- Ajustar layout por CSS/estrutura Elementor preservando os slots nativos.
