# MSN WooCommerce Layout Bridge

Plugin leve para ajustes seguros do WooCommerce usados pelos componentes Elementor da MSN Distribuidora.

## Checkout Mercado Pago

A bridge implementa a documentacao tecnica de checkout mobile e Mercado Pago:

- Torna `billing_phone` obrigatorio e com placeholder brasileiro.
- Adiciona o campo real `billing_cpf` no checkout do WooCommerce.
- Valida CPF com digitos verificadores antes de criar o pedido.
- Salva o CPF em `_billing_cpf` no pedido, seguindo a convencao lida por gateways no WooCommerce.
- Salva `billing_cpf` no perfil do cliente quando existe usuario logado.
- Exibe o CPF na area de faturamento do pedido no admin.

O checkout deve continuar sendo renderizado pelo widget Checkout ou pelo shortcode:

```text
[woocommerce_checkout]
```

Nao crie CPF, telefone ou dados de pagamento como HTML manual no Elementor.

## Homologacao

1. Ative ou atualize o plugin no WordPress.
2. Limpe cache do WP Rocket, cache do navegador e CSS gerado do Elementor quando aplicavel.
3. Abra o checkout em mobile e confirme que `Telefone` e `CPF` aparecem como campos reais.
4. Teste CPF invalido e confirme a mensagem de erro.
5. Conclua uma compra em sandbox Mercado Pago.
6. No admin do pedido, confira se o CPF aparece nos dados de faturamento.
