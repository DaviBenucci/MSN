# Documentação de Reforma do E-commerce MSN Distribuidora

## Resumo

Reformular o e-commerce WordPress + WooCommerce + Elementor Pro com a mesma linguagem visual da landing `MSNsuprimentos`: visual técnico, limpo, confiável, comercial e mobile-first. A prioridade será facilitar três ações: encontrar o produto correto, confirmar compatibilidade e comprar/falar com atendimento sem atrito.

A implementação deverá ser feita por componentes separados em HTML, CSS e JS puro dentro de containers do Elementor, mantendo WooCommerce responsável por preço, estoque, carrinho, checkout, login, pedidos, frete e pagamentos.

Fontes analisadas: documentação local [layout-msndistribuidora-Ecommerce.md](<C:\Users\Sama Contabilidade\Desktop\MSN\layout-msndistribuidora-Ecommerce.md>), landing `MSNsuprimentos`, site atual `https://msndistribuidora.com.br/`, Store API pública `https://msndistribuidora.com.br/wp-json/wc/store/v1/products`.

## Diagnóstico Semântico

- A documentação existente aponta a direção central: **busca forte + WhatsApp + confiança + compra mobile simples**.
- A landing atual usa azul técnico, branco, cinza, verde para WhatsApp, bordas discretas, cards objetivos, tipografia Inter/Poppins e comunicação consultiva.
- O site público está em manutenção na home, mas a API do WooCommerce responde com catálogo ativo.
- Auditoria pública inicial encontrou 477 produtos, categorias principais `Cartucho`, `Impressora`, `Sulfite`, `Toner` e `Sem categoria`; há sinais de saneamento necessário em SKU, imagens, atributos técnicos, categorias e estoque baixo.
- O layout novo deve parecer loja técnica de suprimentos, não uma landing institucional nem um marketplace genérico.

## Mudanças Principais

- **Header:** criar header assistivo de compra com topbar de confiança, logo, busca WooCommerce em destaque, carrinho sempre visível, conta/pedidos, WhatsApp e categorias. No mobile: menu lateral, busca abaixo da logo, carrinho no topo e atalhos “Modelo da impressora” + “WhatsApp”.
- **Footer:** transformar o rodapé em bloco de confiança com atendimento, categorias, políticas, endereço, CNPJ, formas de pagamento, segurança e links úteis; em mobile, usar sanfonas.
- **Home:** refazer a primeira dobra com chamada comercial direta, CTA para loja/produtos, benefícios, categorias principais, destaques, ofertas, bloco de confiança e CTA consultivo para WhatsApp.
- **Loja, busca e filtros:** organizar categorias, criar grid de produto consistente, filtro mobile em modal, filtros por categoria, marca, preço, disponibilidade e compatibilidade quando os atributos forem saneados.
- **Produto:** redesenhar tela com galeria limpa, título, preço WooCommerce, estoque real, CTA comprar, CTA WhatsApp, compatibilidade, especificações, descrição técnica, política de entrega/troca e relacionados.
- **Carrinho:** melhorar clareza de itens, quantidade, subtotal, cupons, frete, totais e CTA de checkout; criar estado de carrinho vazio com retorno para loja e WhatsApp.
- **Minha Conta:** redesenhar login/cadastro, painel, pedidos, detalhes, endereços, dados da conta e recuperar senha usando formulários nativos do WooCommerce.
- **Contato:** alinhar com a landing, priorizando WhatsApp, telefone, e-mail, horário, endereço, mapa e formulário simples com proteção antispam.
- **Estoque e catálogo:** auditar `SKU`, categorias, imagens, alt text, marcas, atributos técnicos, produtos sem imagem, itens em `Sem categoria`, estoque baixo, limites de compra e produtos vencidos/usados.

## Interfaces e Padrões

- Classes customizadas sempre com prefixo `.msn-`, por exemplo `.msn-header`, `.msn-product-card`, `.msn-filter-modal`.
- Separar os componentes por arquivos de manutenção, seguindo o padrão: `msn-header.html/css/js`, `msn-footer.html/css/js`, `msn-product.html/css/js`, e equivalentes para home, loja, carrinho, conta e contato.
- Usar HTML customizado apenas para estrutura visual, CTAs, menus, modais, accordions e microinterações.
- Não usar JS próprio para alterar preço, total, frete, pagamento, login, estoque ou checkout.
- Busca principal deve usar a busca nativa de produtos do WooCommerce com `post_type=product`.
- Filtros devem depender de categorias, marcas e atributos reais do WooCommerce, não de listas manuais em HTML.
- Estoque deve vir do WooCommerce; o layout só exibe status, alertas e mensagens comerciais.

## Testes e Aceitação

- Testar todas as telas em 320, 375, 768, 1024, 1440px e desktop grande.
- Validar fluxos: busca com resultado, busca vazia, filtro aplicado, produto, adicionar ao carrinho, alterar quantidade, carrinho vazio, login, pedido, contato e WhatsApp.
- Verificar se carrinho, conta, checkout, pagamentos, frete e cupons continuam funcionando nativamente.
- Confirmar que não há rolagem horizontal, sobreposição de botões fixos, quebra de header ou CTA coberto no mobile.
- Auditar acessibilidade: foco visível, labels em formulários, contraste, navegação por teclado, `aria-expanded` em menus e modais.
- Auditar performance: imagens WebP, lazy loading, CSS sem duplicação excessiva, JS pequeno e carregado apenas onde necessário.

## Assumptions

- A implementação será feita primeiro em staging ou ambiente seguro do WordPress.
- O tema atual e Elementor Pro continuarão sendo usados.
- Checkout e pagamento não serão redesenhados com HTML manual; apenas estilizados com segurança.
- Antes dos filtros finais, será necessário saneamento do catálogo: categorias, SKU, imagens, marcas e atributos.
- A ordem recomendada é: header, footer, home, loja/busca/filtros, produto, carrinho, minha conta, contato, estoque/catálogo e testes finais.
