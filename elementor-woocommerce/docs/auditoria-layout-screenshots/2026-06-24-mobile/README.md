# Auditoria mobile - 2026-06-24

URL auditada:

```text
https://msndistribuidora.com.br/?woo-share=3xcDTZDRImj3WwYuMAeOt0q0ndNLVaxP
```

## Cobertura

Paginas:

- Home
- Loja
- Produto
- Carrinho
- Checkout
- Minha conta
- Contato
- Privacidade
- Reembolso e devolucoes

Dimensoes:

- Mobile: 320, 360, 375, 390, 412 e 430 px
- Tablet: 768 e 820 px
- Desktop: 1024 e 1440 px

Arquivos gerados:

- `responsive-audit.json`: resultado completo por pagina e viewport.
- `responsive-audit-summary.json`: resumo dos cenarios com status, overflow e erros de console.
- `*-390.png`, `*-768.png`, `*-1440.png`: capturas de referencia visual por pagina.
- `checkout-cpf-local-after-fix.png`: validacao do checkout com CSS/JS local injetado.

## Achados antes dos ajustes locais

- A loja em 320 px tinha largura real de 354 px por cards de produto.
- O produto em 320 px tinha largura real de 396 px por galeria/zoom e cards relacionados.
- O banner do Complianz ocupava altura alta no mobile e competia com formularios e CTAs.
- A quickbar do header funciona como trilho horizontal; seus links aparecem como overflowers na auditoria, mas devem continuar rolando dentro do proprio trilho.

## Ajustes aplicados no codigo local

- CPF Mercado Pago:
  - O seletor tecnico `#form-checkout__identificationType` e mantido como `CPF`.
  - O seletor e a divisoria visual do Mercado Pago ficam ocultos.
  - O cliente ve apenas `input[name="identificationNumber"]`.
  - O input aceita somente 11 digitos, alinhado ao CPF usado nos testes oficiais do Mercado Pago.

- Responsivo:
  - Produtos, cards e imagens receberam `min-width: 0`, `max-width: 100%` e restricoes de grid para nao empurrar o viewport.
  - Galeria de produto e imagem de zoom foram contidas no mobile.
  - Banner do Complianz ficou mais compacto em telas pequenas.
  - `html` e `body` receberam protecao contra overflow horizontal com fallback.

## Validacao depois dos ajustes locais

Com o CSS/JS local injetado no site ao vivo:

- Loja em 320 px: `document.scrollWidth = 320`.
- Produto em 320 px: `document.scrollWidth = 320`.
- Checkout em 320 px: `document.scrollWidth = 320`.
- CPF Mercado Pago:
  - `selectValue = CPF`
  - `selectDisplay = none`
  - `lineDisplay = none`
  - `inputDisplay = block`
  - valor digitado como `123.456.789-09` e sanitizado para `12345678909`
  - `inputmode = numeric`
  - `maxlength = 11`

## Observacao de publicacao

O site ao vivo ainda precisa receber estes arquivos atualizados no WordPress/Elementor e ter cache/CSS regenerado. A validacao acima foi feita injetando o codigo local em runtime pelo Playwright, portanto confirma o comportamento esperado, mas nao publica automaticamente as alteracoes.
