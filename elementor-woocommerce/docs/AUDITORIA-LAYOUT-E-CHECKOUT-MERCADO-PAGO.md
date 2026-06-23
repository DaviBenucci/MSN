# Auditoria de layout e checkout Mercado Pago

Data da auditoria: 2026-06-23.

URL usada para acesso ao site em pre-publicacao:

```text
https://msndistribuidora.com.br/?woo-share=3xcDTZDRImj3WwYuMAeOt0q0ndNLVaxP
```

## Objetivo

Registrar os problemas encontrados no site publicado em pre-visualizacao e orientar as proximas correcoes sem quebrar WooCommerce, Fluid Checkout, Mercado Pago, carrinho, conta, busca, frete, estoque ou a bridge de produtos.

Este documento nao substitui homologacao do gateway. Ele organiza o que precisa ser ajustado antes de ativar a conta Mercado Pago em producao.

## Diagnostico da auditoria ao vivo

Paginas verificadas com o link compartilhado:

- Home.
- Loja.
- Produto individual.
- Carrinho.
- Finalizacao de compra.
- Contato.
- Minha conta.
- Politica de privacidade.
- Politica de reembolso e devolucoes.

Resultados principais:

- O site carregou com visual claro fixo.
- Header e footer apareceram nas paginas verificadas.
- Produtos, preco, estoque e botao de adicionar ao carrinho apareceram no produto individual.
- Carrinho vazio redireciona corretamente o checkout para o carrinho.
- Com produto no carrinho, a finalizacao de compra carregou formulario, area de pagamento e botao de finalizar pedido.
- A URL correta da pagina de devolucao observada foi `/reembolso_devolucoes/`.
- O banner de consentimento aparece grande no canto inferior direito e encobre parte de formularios, botoes e conteudos ate o usuario aceitar ou fechar.
- Foi visto erro de console do script do Mercado Pago em pagina que nao e checkout: `No checkout form found after 10 attempts`.

Leitura tecnica:

- O erro do Mercado Pago fora do checkout provavelmente ocorre porque o script de checkout do gateway esta sendo carregado em paginas onde nao existe formulario de checkout.
- A falta de conta Mercado Pago configurada pode impedir testes reais de pagamento, mas nao deve ser usada como unica explicacao ate retestar com credenciais em modo teste.
- CPF, CNPJ e telefone nao devem ser criados como campos HTML manuais no Elementor. Eles precisam ser campos reais do WooCommerce para serem validados, salvos no pedido e enviados aos gateways quando aplicavel.

## Plano para melhorar o layout

Prints de referencia foram salvos em:

```text
elementor-woocommerce/docs/auditoria-layout-screenshots/
```

Leia `auditoria-layout-screenshots/README.md` antes de iniciar o refinamento visual em um novo chat.

Prioridade 1: remover bloqueios visuais.

- Reconfigurar o banner de consentimento para nao cobrir a area de checkout, produto, conta e contato.
- Preferir banner inferior em faixa, modal central com fechamento claro, ou posicao que nao cubra botoes de compra.
- Testar pagina de produto, carrinho, checkout e minha conta antes e depois de aceitar consentimento.

Prioridade 2: reduzir espacos excessivos nas primeiras secoes.

- Revisar alturas, `padding`, `min-height` e gaps dos heroes de carrinho, checkout, conta e contato.
- Manter a hierarquia visual, mas trazer o formulario principal mais perto da primeira dobra.
- No checkout, garantir que o usuario veja rapidamente o primeiro campo acionavel depois do titulo.

Prioridade 3: profissionalizar a leitura sem redesenhar o sistema.

- Preservar logo, busca, conta, pedidos e carrinho no header.
- Melhorar densidade visual dos grids de produtos sem esconder preco, estoque ou CTA.
- Garantir que labels, mensagens de erro e campos obrigatorios tenham contraste suficiente.
- Evitar cards dentro de cards e manter secoes em largura consistente.

Criterios de aceite de layout:

- Seguir `MOBILE-FIRST-RESPONSIVIDADE.md` como criterio obrigatorio.
- 320px, 360px, 375px, 390px, 412px, 430px, 768px, 820px, 1024px e 1440px sem rolagem horizontal.
- Produto individual mostra imagem, preco, estoque e CTA sem elementos sobrepostos.
- Checkout mostra primeiro campo util sem depender de rolagem longa desnecessaria.
- Banner de consentimento nao cobre botao de compra, campos de checkout, login/cadastro ou CTA principal.
- Mensagens nativas do WooCommerce continuam visiveis.

## Plano para CPF, CNPJ e telefone no checkout

### Decisao de arquitetura

O projeto deve continuar usando checkout nativo do WooCommerce:

```text
[woocommerce_checkout]
```

ou o widget Checkout do Elementor/WooCommerce dentro de:

```text
msn-checkout-woo-slot
```

Nao criar CPF, CNPJ ou telefone como HTML solto em bloco Elementor, porque esses dados nao entram automaticamente no pedido nem no gateway.

### Opcao recomendada

Usar uma solucao de campos brasileiros para WooCommerce que crie campos reais no checkout, com validacao e salvamento no pedido.

Configurar no minimo:

- Tipo de pessoa: Pessoa fisica / Pessoa juridica.
- CPF obrigatorio quando Pessoa fisica.
- CNPJ obrigatorio quando Pessoa juridica.
- Telefone obrigatorio, preferencialmente no campo padrao `billing_phone`.
- Mascara de CPF, CNPJ e telefone.
- Numero e bairro, se forem necessarios para entrega/frete.

Um plugin candidato documentado no WordPress.org e o `Brazilian Checkout Toolkit for WooCommerce`, que declara suporte a CPF/CNPJ, tipo de pessoa, telefone/celular, mascaras, checkout classico e Checkout Block. Antes de adotar, validar em staging junto com Fluid Checkout, Mercado Pago e a versao atual do WooCommerce.

### Opcao com codigo proprio

Se a escolha for implementar sem plugin, criar um pequeno plugin proprio ou snippet controlado, nunca dentro de HTML do Elementor.

O snippet deve:

- Tornar `billing_phone` obrigatorio.
- Adicionar `billing_persontype`, `billing_cpf` e `billing_cnpj`.
- Validar CPF quando o tipo de pessoa for fisica.
- Validar CNPJ quando o tipo de pessoa for juridica.
- Salvar os dados no pedido como metadados.
- Exibir os dados no admin do pedido.
- Ser testado com Fluid Checkout e Mercado Pago antes de producao.

Chaves sugeridas para compatibilidade:

```text
billing_phone
billing_persontype
billing_cpf
billing_cnpj
```

Se o plugin escolhido usar outras chaves, documentar o mapeamento e confirmar se o Mercado Pago consegue ler os dados esperados.

### CSS do checkout

Depois de adicionar os campos:

- Garantir que `03-checkout-woocommerce.css` estilize os novos campos dentro de `.msn-checkout-woo-slot`.
- Nao esconder campos de faturamento com CSS para "limpar" a tela.
- Testar estados normal, foco, erro, preenchido e mensagem de validacao.
- Conferir se os campos aparecem na etapa correta do Fluid Checkout.

## Plano para Mercado Pago

Antes da ativacao:

- Instalar e manter o plugin oficial `Mercado Pago payments for WooCommerce`.
- Configurar credenciais em modo teste.
- Ativar o metodo desejado em WooCommerce > Mercado Pago.
- Testar cartao, Pix ou Checkout Pro conforme a estrategia da loja.
- Confirmar se moeda, pais da loja e URLs do WooCommerce estao corretos.

Depois de configurar a conta:

- Testar checkout com Pessoa fisica, CPF e telefone.
- Testar checkout com Pessoa juridica, CNPJ e telefone.
- Confirmar que o pedido salva CPF/CNPJ/telefone no admin.
- Confirmar que o Mercado Pago nao bloqueia por falta de documento ou telefone.
- Revisar console apenas na pagina de checkout.

Erro de console fora do checkout:

- Se `No checkout form found after 10 attempts` continuar aparecendo em Contato, Home ou Loja depois da configuracao do Mercado Pago, tratar como carregamento indevido de script.
- A correcao deve ser condicional: scripts de checkout do Mercado Pago so devem rodar onde existe checkout.
- Nao desativar scripts do Mercado Pago globalmente sem testar pagamento, porque isso pode quebrar o gateway na finalizacao.

## Checklist de homologacao

- [ ] Produto adicionado ao carrinho.
- [ ] Checkout abre sem redirecionar para carrinho.
- [ ] Telefone aparece, e obrigatorio e salva no pedido.
- [ ] Pessoa fisica exige CPF valido.
- [ ] Pessoa juridica exige CNPJ valido.
- [ ] Mensagens de erro aparecem no checkout sem ficarem escondidas.
- [ ] Mercado Pago em modo teste mostra o metodo de pagamento esperado.
- [ ] Pedido teste e criado no WooCommerce.
- [ ] CPF/CNPJ/telefone aparecem no admin do pedido.
- [ ] Console sem erro Mercado Pago em paginas que nao sao checkout, ou erro classificado e aceito temporariamente.
- [ ] Banner de consentimento nao cobre o botao de finalizar pedido.
- [ ] Checklist de `MOBILE-FIRST-RESPONSIVIDADE.md` aprovado.
- [ ] Teste realizado em desktop e celular real.

## Referencias tecnicas

- Mercado Pago para WooCommerce: https://woocommerce.com/document/mercado-pago/
- Configuracao de pagamentos Mercado Pago no WooCommerce: https://www.mercadopago.com.br/developers/
- WooCommerce, customizacao de campos do checkout classico: https://developer.woocommerce.com/docs/code-snippets/customising-checkout-fields/
- WooCommerce, campos adicionais no Checkout Block: https://developer.woocommerce.com/docs/block-development/extensible-blocks/cart-and-checkout-blocks/additional-checkout-fields/
- Brazilian Checkout Toolkit for WooCommerce: https://wordpress.org/plugins/brazilian-checkout-toolkit-for-woocommerce/
