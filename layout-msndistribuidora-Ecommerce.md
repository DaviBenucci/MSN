# Documentação Final de Layout — E-commerce MSN Distribuidora

## 1. Status da documentação

Esta é a documentação consolidada do layout do e-commerce da **MSN Distribuidora**, reunindo as decisões finais sobre:

- direção visual;
- estrutura responsiva;
- header;
- footer;
- escopo de todas as telas;
- uso de HTML, CSS e JavaScript no Elementor Pro;
- segurança em WordPress, WooCommerce e código customizado;
- checklist de aprovação.

Esta versão substitui as documentações separadas anteriores e deve ser usada como referência principal para implementação.

---

## 2. Decisões finais aprovadas

### 2.1 Plataforma

```text
WordPress + WooCommerce + Elementor Pro
```

O Elementor Pro será usado para estrutura, templates globais, responsividade e páginas principais.

O HTML, CSS e JavaScript customizados serão usados somente para componentes específicos, como:

- header customizado;
- hero comercial;
- barras de benefício;
- cards visuais;
- CTA de WhatsApp;
- footer elaborado;
- microinterações;
- menu mobile;
- filtro mobile;
- pequenos carrosséis leves.

Não usar HTML, CSS ou JavaScript próprio para substituir funcionalidades críticas do WooCommerce, como preço, frete, carrinho, checkout, pagamento, login ou dados da conta.

---

### 2.2 Direção visual

O visual final deve ser:

```text
Técnico + limpo + confiável + comercial + mobile-first
```

A MSN Distribuidora deve parecer uma loja de suprimentos e equipamentos de impressão confiável, e não uma landing page institucional ou site de agência.

A estética deve comunicar:

- segurança;
- organização;
- facilidade de compra;
- atendimento especializado;
- catálogo técnico;
- compatibilidade de produtos;
- credibilidade para cliente B2B e B2C.

---

### 2.3 Header aprovado

A decisão final para o header é:

```text
Desktop: Opção A — Busca Forte + Confiança
Tablet:  Opção A compactada
Mobile:  Estrutura app-like, com busca forte, carrinho e WhatsApp
```

Ajuste solicitado e aprovado:

```text
No desktop e tablet, remover o item "Departamentos" como primeiro item visual do menu.
No lugar, inserir um botão/atalho de WhatsApp para conversa direta com atendimento.
```

Portanto, a linha de navegação principal não deve começar com:

```text
☰ Departamentos
```

Ela deve começar com:

```text
WhatsApp / Fale com especialista
```

As categorias continuam disponíveis diretamente no menu:

```text
Impressoras | Toners | Cartuchos | Ofertas | Cotação rápida
```

No mobile, o menu hambúrguer continua existindo para abrir as categorias completas, pois o espaço é reduzido.

---

### 2.4 Prioridade mobile

O projeto será tratado como **mobile-first**.

Ordem de prioridade:

```text
1. Mobile
2. Tablet
3. Desktop
```

Motivo: a maioria dos clientes acessa pelo celular. Portanto, todo layout deve ser aprovado primeiro em telas pequenas.

---

## 3. Breakpoints oficiais

```text
Mobile pequeno:      320px até 374px
Mobile padrão:       375px até 767px
Tablet:              768px até 1024px
Desktop:             1025px até 1440px
Desktop grande:      acima de 1440px
```

Regra de construção:

```text
Celular primeiro → Tablet adaptado → Desktop expandido
```

---

## 4. Paleta visual recomendada

A paleta deve usar azul, branco, cinza e verde para transmitir tecnologia, clareza e confiança.

```css
:root {
  --msn-primary: #0F4C81;
  --msn-primary-dark: #0B2F4F;
  --msn-primary-soft: #EAF4FF;

  --msn-success: #16A34A;
  --msn-warning: #F59E0B;
  --msn-danger: #EF4444;

  --msn-bg: #F8FAFC;
  --msn-surface: #FFFFFF;
  --msn-surface-alt: #EEF6FB;

  --msn-text: #1F2937;
  --msn-muted: #6B7280;
  --msn-border: #E5E7EB;

  --msn-shadow: 0 18px 45px rgba(15, 76, 129, 0.12);
}
```

### Uso das cores

| Cor | Uso |
|---|---|
| Azul principal | Botões, links, elementos de navegação e confiança |
| Azul escuro | Topbar, rodapé, áreas institucionais |
| Azul claro | Fundos suaves, estados de hover e blocos informativos |
| Verde | Compra segura, WhatsApp, status positivo |
| Amarelo | Ofertas, avisos comerciais e destaques promocionais |
| Cinza | Bordas, textos secundários e organização visual |
| Branco | Fundo principal dos cards, header e áreas comerciais |

---

## 5. Tipografia recomendada

### Títulos

```text
Poppins ou Montserrat
```

### Texto comum

```text
Inter, Roboto ou fonte padrão configurada no Elementor
```

### Preços

```text
Peso 700/800, alto contraste, leitura rápida
```

### Hierarquia CSS sugerida

```css
h1 {
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 1.05;
  font-weight: 800;
}

h2 {
  font-size: clamp(1.6rem, 3vw, 2.4rem);
  line-height: 1.15;
  font-weight: 700;
}

p {
  font-size: 1rem;
  line-height: 1.65;
}
```

---

# 6. Estrutura global do site

Todas as telas devem seguir a mesma estrutura mental:

```text
+-------------------------------------+
|                                     |
|               HEADER                |
|                                     |
+-------------------------------------+
|                                     |
|                                     |
|              CONTEÚDO               |
|                                     |
|                                     |
+-------------------------------------+
|                                     |
|               FOOTER                |
|                                     |
+-------------------------------------+
```

---

## 6.1 Estrutura global desktop

```text
+--------------------------------------------------------------------------------+
|                              HEADER DESKTOP                                    |
|--------------------------------------------------------------------------------|
| Topbar: frete | compra segura | +15 anos | WhatsApp                           |
|--------------------------------------------------------------------------------|
| Logo          Busca central grande                  Conta | Pedidos | Carrinho |
|--------------------------------------------------------------------------------|
| WhatsApp | Impressoras | Toners | Cartuchos | Ofertas | Cotação rápida         |
+--------------------------------------------------------------------------------+
|                                                                                |
|                              CONTEÚDO DA TELA                                  |
|                                                                                |
+--------------------------------------------------------------------------------+
|                              FOOTER DESKTOP                                    |
|--------------------------------------------------------------------------------|
| Marca | Categorias | Atendimento | Políticas | Segurança | Endereço            |
+--------------------------------------------------------------------------------+
```

---

## 6.2 Estrutura global tablet

```text
+------------------------------------------------------------+
|                        HEADER TABLET                       |
|------------------------------------------------------------|
| Frete SP | Compra segura | WhatsApp                        |
|------------------------------------------------------------|
| Logo                         Conta | Carrinho               |
|------------------------------------------------------------|
| Busca em largura total                                    |
|------------------------------------------------------------|
| WhatsApp | Modelo da impressora | Ofertas | Categorias      |
+------------------------------------------------------------+
|                                                            |
|                        CONTEÚDO                            |
|                                                            |
+------------------------------------------------------------+
|                        FOOTER TABLET                       |
|------------------------------------------------------------|
| Blocos em 2 colunas: atendimento, categorias, políticas    |
+------------------------------------------------------------+
```

---

## 6.3 Estrutura global mobile

```text
+-------------------------------------+
|            HEADER MOBILE            |
|-------------------------------------|
| Frete SP | Compra segura            |
|-------------------------------------|
| Menu       Logo              Carrinho|
|-------------------------------------|
| Busca em largura total              |
|-------------------------------------|
| Modelo da impressora | WhatsApp     |
+-------------------------------------+
|                                     |
|              CONTEÚDO               |
|                                     |
| Uma coluna                          |
| Botões grandes                      |
| Cards limpos                        |
| Textos curtos                       |
|                                     |
+-------------------------------------+
|            FOOTER MOBILE            |
|-------------------------------------|
| Atendimento                         |
| Categorias                          |
| Políticas                           |
| Segurança                           |
| Endereço                            |
+-------------------------------------+
```

---

# 7. Header final

## 7.1 Conceito aprovado

```text
Header Assistivo de Compra
```

O header deve funcionar como um assistente de compra, porque o cliente pode não saber exatamente qual toner, cartucho ou impressora precisa comprar.

O header deve responder rapidamente:

```text
Onde eu busco?
Como encontro pelo modelo da impressora?
Como falo com atendimento?
Onde estão as categorias?
Onde está meu carrinho?
Como acompanho meus pedidos?
```

---

## 7.2 Header desktop final

```text
+--------------------------------------------------------------------------------+
| FRETE GRÁTIS SP E CAPITAL | COMPRA SEGURA | +15 ANOS | ATENDIMENTO WHATSAPP    |
+--------------------------------------------------------------------------------+
| LOGO MSN      [ Buscar toner, cartucho, impressora ou código...          🔍 ]  |
|               [ Buscar pelo modelo da impressora ]     Conta  Pedidos Carrinho |
+--------------------------------------------------------------------------------+
| WhatsApp | Impressoras | Toners | Cartuchos | Ofertas | Cotação rápida         |
+--------------------------------------------------------------------------------+
```

### Decisão importante

O antigo item:

```text
☰ Departamentos
```

foi substituído por:

```text
WhatsApp / Fale com especialista
```

Motivo: para esse e-commerce, a conversa pelo WhatsApp é uma ação de alta conversão, principalmente para clientes com dúvida sobre compatibilidade de toner, cartucho ou impressora.

---

## 7.3 Header tablet final

```text
+--------------------------------------------------------------+
| Frete SP | Compra segura | WhatsApp                          |
+--------------------------------------------------------------+
| LOGO MSN                              Conta    Carrinho       |
| [ Buscar toner, cartucho ou impressora...                🔍 ] |
+--------------------------------------------------------------+
| WhatsApp | Modelo da impressora | Ofertas | Categorias        |
+--------------------------------------------------------------+
```

### Regras para tablet

- Busca em linha própria.
- Carrinho sempre visível.
- WhatsApp presente como atalho de atendimento.
- Categorias podem abrir em menu compacto.
- Não quebrar o header em muitas linhas desorganizadas.

---

## 7.4 Header mobile final

```text
+-------------------------------------+
| Frete SP | Compra segura            |
+-------------------------------------+
| ☰       LOGO MSN              🛒     |
+-------------------------------------+
| [ Buscar toner ou impressora... 🔍 ] |
+-------------------------------------+
| Modelo da impressora | WhatsApp      |
+-------------------------------------+
```

### Regras para mobile

- Logo centralizada.
- Menu hambúrguer à esquerda.
- Carrinho à direita com contador.
- Busca visível logo abaixo da logo.
- WhatsApp e modelo da impressora como atalhos imediatos.
- Header compacto para não ocupar altura excessiva.
- Menu lateral para categorias completas.

---

## 7.5 Barra inferior mobile opcional

```text
+-------------------------------------+
| Início | Categorias | WhatsApp | Conta | 🛒 |
+-------------------------------------+
```

### Regras

- Não usar no checkout.
- Não cobrir o botão de compra.
- Em página de produto, pode ser substituída por uma barra fixa de compra.
- Deve respeitar a área segura do celular.

---

## 7.6 Menu mobile off-canvas

```text
+-------------------------------------+
| MENU                            X   |
+-------------------------------------+
| Buscar produto                      |
| Minha conta                         |
| Meus pedidos                        |
| Carrinho                            |
+-------------------------------------+
| Categorias                          |
| Impressoras                         |
| Toners                              |
| Cartuchos                           |
| Tintas                              |
| Peças e Acessórios                  |
| Ofertas                             |
+-------------------------------------+
| Atendimento                         |
| WhatsApp                            |
| Cotação rápida                      |
| Trocas e devoluções                 |
+-------------------------------------+
```

### Regras

- Abrir lateralmente.
- Escurecer o fundo.
- Bloquear rolagem do fundo enquanto aberto.
- Ter botão de fechar grande.
- Ter navegação por teclado.
- Fechar ao clicar fora.

---

## 7.7 Elementos obrigatórios do header

| Elemento | Obrigatório | Observação |
|---|---:|---|
| Logo | Sim | Link para home |
| Busca principal | Sim | Deve usar busca nativa do WooCommerce |
| Busca por modelo | Sim | Pode começar como link para página de busca/filtro |
| WhatsApp | Sim | Atendimento consultivo |
| Conta | Sim | Desktop/tablet; mobile no menu ou barra inferior |
| Pedidos | Sim | Desktop; mobile no menu |
| Carrinho | Sim | Sempre visível |
| Topbar de confiança | Sim | Reduzida no mobile |
| Categorias | Sim | Visíveis no desktop; off-canvas no mobile |

---

## 7.8 Placeholders aprovados

### Busca principal desktop/tablet

```text
Buscar toner, cartucho, impressora ou código...
```

### Busca principal mobile

```text
Buscar toner ou impressora...
```

### Busca por modelo

```text
Buscar pelo modelo da impressora
```

### WhatsApp

```text
Fale com especialista
```

---

# 8. Footer final

## 8.1 Footer desktop

```text
+--------------------------------------------------------------------------------+
|                                 FOOTER DESKTOP                                 |
|--------------------------------------------------------------------------------|
|  MSN Distribuidora       Categorias          Atendimento        Políticas       |
|  Breve descrição         Impressoras         WhatsApp           Privacidade     |
|  Endereço                Toners              Telefone           Trocas          |
|  CNPJ                    Cartuchos           E-mail             Frete           |
|  Redes sociais           Ofertas             Horário            Termos          |
|--------------------------------------------------------------------------------|
|  Selos de segurança | Formas de pagamento | Copyright                         |
+--------------------------------------------------------------------------------+
```

---

## 8.2 Footer tablet

```text
+------------------------------------------------------------+
|                        FOOTER TABLET                       |
|------------------------------------------------------------|
|  Atendimento                  Categorias                   |
|  Políticas                    Segurança                    |
|  Endereço                     Pagamento                    |
+------------------------------------------------------------+
```

---

## 8.3 Footer mobile

```text
+-------------------------------------+
|            FOOTER MOBILE            |
|-------------------------------------|
| Atendimento                         |
|  WhatsApp                           |
|  Telefone                           |
|  E-mail                             |
|-------------------------------------|
| Categorias                          |
|  Impressoras                        |
|  Toners                             |
|  Cartuchos                          |
|-------------------------------------|
| Políticas                           |
|  Trocas e devoluções                |
|  Privacidade                        |
|  Frete e entrega                    |
|  Termos de uso                      |
|-------------------------------------|
| Segurança                           |
|  Compra segura                      |
|  Formas de pagamento                |
|-------------------------------------|
| Endereço                            |
| CNPJ                                |
+-------------------------------------+
```

### Regras do footer

- Não deve ser apenas decorativo.
- Deve reforçar confiança.
- Deve conter atendimento, políticas, endereço e CNPJ, quando aplicável.
- Em mobile, pode usar sanfonas para reduzir altura.
- Links legais devem ficar acessíveis.
- Evitar carrossel pesado no footer.

---

# 9. Tela Home

## 9.1 Objetivo

A home deve apresentar a loja rapidamente, conduzir para categorias/produtos e reforçar confiança antes da compra.

---

## 9.2 Home desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| HERO                                                                           |
| Título comercial direto                  Banner/imagem de produtos             |
| Subtítulo de confiança                   CTA: Ver produtos                     |
| Benefícios: frete | segurança | atendimento | experiência                      |
+--------------------------------------------------------------------------------+
| CATEGORIAS PRINCIPAIS                                                          |
| [Impressoras] [Toners] [Cartuchos] [Ofertas]                                   |
+--------------------------------------------------------------------------------+
| PRODUTOS EM DESTAQUE                                                           |
| Card | Card | Card | Card                                                      |
+--------------------------------------------------------------------------------+
| MAIS VENDIDOS / OFERTAS                                                        |
| Card | Card | Card | Card                                                      |
+--------------------------------------------------------------------------------+
| BLOCO DE CONFIANÇA                                                             |
| +15 anos | atendimento personalizado | compra segura | endereço físico         |
+--------------------------------------------------------------------------------+
| CTA WHATSAPP                                                                   |
| Não sabe qual toner comprar? Fale com especialista                             |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 9.3 Home tablet

```text
+------------------------------------------------------------+
| HEADER                                                     |
+------------------------------------------------------------+
| HERO                                                       |
| Título                                                     |
| Texto curto                                                |
| Botão principal                                            |
+------------------------------------------------------------+
| Benefícios em 2 colunas                                    |
+------------------------------------------------------------+
| Categorias em 2 colunas                                    |
+------------------------------------------------------------+
| Produtos em 2 colunas                                      |
+------------------------------------------------------------+
| CTA WhatsApp                                               |
+------------------------------------------------------------+
| FOOTER                                                     |
+------------------------------------------------------------+
```

---

## 9.4 Home mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| HERO MOBILE                         |
| Título curto                        |
| Texto de confiança                  |
| [Ver produtos]                      |
| [Chamar no WhatsApp]                |
+-------------------------------------+
| BENEFÍCIOS                          |
| Frete SP                            |
| Compra segura                       |
| Atendimento especializado           |
+-------------------------------------+
| CATEGORIAS                          |
| [Impressoras]                       |
| [Toners]                            |
| [Cartuchos]                         |
+-------------------------------------+
| PRODUTOS                            |
| Card produto                        |
| Card produto                        |
| Card produto                        |
+-------------------------------------+
| AJUDA NA COMPRA                     |
| Não sabe qual produto escolher?     |
| [Falar com especialista]            |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras da home

- Primeiro CTA deve aparecer antes da dobra no mobile.
- Categorias devem vir antes de textos institucionais longos.
- Produtos precisam de imagem, nome, preço e CTA.
- Evitar banners altos no celular.
- Não usar intro animada bloqueante.

---

# 10. Tela Categoria / Departamento

## 10.1 Exemplos de categorias

- Impressoras;
- Toners;
- Cartuchos;
- Tintas;
- Peças e Acessórios;
- Ofertas;
- Marcas;
- Suprimentos.

---

## 10.2 Categoria desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| Breadcrumb: Home > Categoria                                                   |
+--------------------------------------------------------------------------------+
| TÍTULO DA CATEGORIA                                                            |
| Texto curto explicando a categoria                                             |
+--------------------------------------------------------------------------------+
| FILTROS LATERAIS            LISTAGEM DE PRODUTOS                               |
| Marca                       Ordenar por: relevância/preço/mais vendidos        |
| Preço                       Card | Card | Card                                  |
| Tipo                        Card | Card | Card                                  |
| Compatibilidade             Card | Card | Card                                  |
| Disponibilidade             Card | Card | Card                                  |
+--------------------------------------------------------------------------------+
| Paginação / Carregar mais                                                       |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 10.3 Categoria tablet

```text
+------------------------------------------------------------+
| HEADER                                                     |
+------------------------------------------------------------+
| Breadcrumb                                                 |
| Título da categoria                                        |
+------------------------------------------------------------+
| [Filtrar] [Ordenar]                                        |
+------------------------------------------------------------+
| Card produto        Card produto                           |
| Card produto        Card produto                           |
+------------------------------------------------------------+
| FOOTER                                                     |
+------------------------------------------------------------+
```

---

## 10.4 Categoria mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| Home > Categoria                    |
+-------------------------------------+
| TÍTULO                              |
| Texto curto                         |
+-------------------------------------+
| [Filtrar]        [Ordenar]          |
+-------------------------------------+
| Card produto                        |
| Card produto                        |
| Card produto                        |
+-------------------------------------+
| Carregar mais / Paginação           |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- No desktop, filtros laterais.
- No tablet/mobile, filtros em gaveta/modal.
- Produto indisponível deve ser marcado claramente.
- Card precisa mostrar imagem, nome, preço, CTA e compatibilidade quando necessário.

---

# 11. Tela Subcategoria

## 11.1 Exemplos

- Toner HP;
- Toner Brother;
- Cartucho Epson;
- Impressora Laser;
- Impressora Multifuncional.

---

## 11.2 Subcategoria desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| Home > Toners > Toner HP                                                       |
+--------------------------------------------------------------------------------+
| TÍTULO: Toner HP                                                               |
| Texto curto com orientação de compatibilidade                                  |
+--------------------------------------------------------------------------------+
| FILTROS POR MODELO/MARCA             PRODUTOS                                  |
| Modelo da impressora                 Card | Card | Card                        |
| Cor                                  Card | Card | Card                        |
| Rendimento                           Card | Card | Card                        |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 11.3 Subcategoria mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| Home > Toners > Toner HP            |
+-------------------------------------+
| Toner HP                            |
| Encontre pelo modelo da impressora  |
+-------------------------------------+
| [Buscar dentro da categoria]         |
| [Filtrar] [Ordenar]                 |
+-------------------------------------+
| Card produto                        |
| Card produto                        |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regra crítica

Para produtos técnicos, a subcategoria deve ajudar o cliente a evitar erro de compra. A informação de compatibilidade precisa estar visível.

---

# 12. Tela de Busca

## 12.1 Busca com resultados — desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| Resultado da busca por: "toner hp"                                             |
+--------------------------------------------------------------------------------+
| FILTROS                    PRODUTOS ENCONTRADOS                                |
| Categoria                  Card | Card | Card                                  |
| Marca                      Card | Card | Card                                  |
| Preço                      Card | Card | Card                                  |
+--------------------------------------------------------------------------------+
| Sugestões relacionadas                                                        |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 12.2 Busca com resultados — mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| Resultado para: "toner hp"          |
+-------------------------------------+
| [Filtrar] [Ordenar]                 |
+-------------------------------------+
| Card produto                        |
| Card produto                        |
| Card produto                        |
+-------------------------------------+
| Sugestões                           |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

## 12.3 Busca sem resultado

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| Nenhum produto encontrado           |
|                                     |
| Tente buscar por:                   |
| - modelo da impressora              |
| - marca                             |
| - código do toner/cartucho          |
|                                     |
| [Falar com especialista]            |
| [Ver categorias]                    |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Nunca mostrar página vazia.
- Sempre oferecer alternativa.
- CTA de WhatsApp deve aparecer quando não houver resultado.
- O termo pesquisado deve aparecer na tela.

---

# 13. Tela Produto

## 13.1 Produto desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| Breadcrumb: Home > Categoria > Produto                                         |
+--------------------------------------------------------------------------------+
| GALERIA DE IMAGENS                 INFORMAÇÕES DO PRODUTO                      |
| Imagem principal                   Nome do produto                             |
| Miniaturas                         Código/SKU                                  |
|                                    Preço                                       |
|                                    Parcelamento                                |
|                                    Estoque                                     |
|                                    Quantidade                                  |
|                                    [Comprar]                                   |
|                                    [Chamar no WhatsApp]                        |
+--------------------------------------------------------------------------------+
| Benefícios: compra segura | entrega | atendimento                              |
+--------------------------------------------------------------------------------+
| DESCRIÇÃO / ESPECIFICAÇÕES / COMPATIBILIDADE / ENTREGA                         |
+--------------------------------------------------------------------------------+
| Produtos relacionados                                                          |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 13.2 Produto tablet

```text
+------------------------------------------------------------+
| HEADER                                                     |
+------------------------------------------------------------+
| Breadcrumb                                                 |
+------------------------------------------------------------+
| Imagem do produto                                          |
| Miniaturas                                                 |
+------------------------------------------------------------+
| Nome, preço, estoque                                       |
| [Comprar]                                                  |
| [WhatsApp]                                                 |
+------------------------------------------------------------+
| Descrição / Especificações / Compatibilidade               |
+------------------------------------------------------------+
| Produtos relacionados                                      |
+------------------------------------------------------------+
| FOOTER                                                     |
+------------------------------------------------------------+
```

---

## 13.3 Produto mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| Home > Categoria                    |
+-------------------------------------+
| Imagem do produto                   |
| Miniaturas                          |
+-------------------------------------+
| Nome do produto                     |
| Código/SKU                          |
| Preço                               |
| Parcelamento                        |
| Estoque                             |
+-------------------------------------+
| Quantidade                          |
| [COMPRAR]                           |
| [FALAR NO WHATSAPP]                 |
+-------------------------------------+
| Compra segura | Entrega | Suporte   |
+-------------------------------------+
| Descrição                           |
| Especificações                      |
| Compatibilidade                     |
+-------------------------------------+
| Produtos relacionados               |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

## 13.4 CTA fixo de produto mobile

```text
+-------------------------------------+
| Preço resumido        [Comprar]     |
+-------------------------------------+
```

### Regras

- Só aparece depois que o usuário rolar além do botão original.
- Não deve cobrir conteúdo.
- Deve respeitar teclado aberto e áreas seguras.
- Em produto, pode substituir a barra inferior mobile.

---

## 13.5 Regras da página de produto

- Botão comprar deve aparecer antes de textos longos.
- WhatsApp deve ajudar em dúvidas de compatibilidade.
- Compatibilidade deve ser informação crítica.
- Não esconder preço, disponibilidade ou frete.
- No mobile, preferir sanfonas em vez de abas pequenas.
- Preço e estoque devem vir do WooCommerce.

---

# 14. Tela Carrinho com produtos

## 14.1 Carrinho desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| CARRINHO                                                                       |
+--------------------------------------------------------------------------------+
| PRODUTOS NO CARRINHO                         RESUMO DO PEDIDO                 |
| Imagem | Produto | Preço | Qtd | Subtotal     Subtotal                         |
| Imagem | Produto | Preço | Qtd | Subtotal     Cupom                            |
|                                                Frete                           |
|                                                Total                           |
|                                                [Finalizar compra]              |
|                                                [Continuar comprando]           |
+--------------------------------------------------------------------------------+
| Produtos recomendados / relacionados                                           |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 14.2 Carrinho tablet

```text
+------------------------------------------------------------+
| HEADER                                                     |
+------------------------------------------------------------+
| CARRINHO                                                   |
+------------------------------------------------------------+
| Produto                                                    |
| Preço | Quantidade | Subtotal                              |
+------------------------------------------------------------+
| Produto                                                    |
| Preço | Quantidade | Subtotal                              |
+------------------------------------------------------------+
| RESUMO DO PEDIDO                                           |
| Cupom                                                      |
| Frete                                                      |
| Total                                                      |
| [Finalizar compra]                                         |
+------------------------------------------------------------+
| FOOTER                                                     |
+------------------------------------------------------------+
```

---

## 14.3 Carrinho mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| CARRINHO                            |
+-------------------------------------+
| Produto                             |
| Imagem pequena + nome               |
| Preço                               |
| Quantidade [-] [1] [+]              |
| Subtotal                            |
| [Remover]                           |
+-------------------------------------+
| Produto                             |
| Imagem pequena + nome               |
| Preço                               |
| Quantidade                          |
| Subtotal                            |
+-------------------------------------+
| Cupom de desconto                   |
| [Aplicar cupom]                     |
+-------------------------------------+
| RESUMO                              |
| Subtotal                            |
| Frete                               |
| Total                               |
| [FINALIZAR COMPRA]                  |
| [CONTINUAR COMPRANDO]               |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Botão finalizar compra é o CTA principal.
- Continuar comprando é secundário.
- Alterar quantidade deve ser fácil no celular.
- Remover item deve ter confirmação visual.
- Nunca manipular preço, frete ou total com JS customizado.

---

# 15. Tela Carrinho vazio

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| Seu carrinho está vazio             |
|                                     |
| Parece que você ainda não adicionou |
| nenhum produto ao carrinho.         |
|                                     |
| [Ver produtos]                      |
| [Falar com especialista]            |
+-------------------------------------+
| Categorias sugeridas                |
| Impressoras                         |
| Toners                              |
| Cartuchos                           |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- A tela não deve parecer erro.
- Deve orientar o cliente.
- Deve ter CTA para produtos e atendimento.

---

# 16. Tela Checkout

## 16.1 Checkout desktop

```text
+--------------------------------------------------------------------------------+
| HEADER SIMPLIFICADO                                                            |
| LOGO                                      Compra segura                         |
+--------------------------------------------------------------------------------+
| CHECKOUT                                                                       |
+--------------------------------------------------------------------------------+
| DADOS DO CLIENTE / ENTREGA                    RESUMO DO PEDIDO                 |
| Nome                                          Produtos                         |
| E-mail                                        Subtotal                         |
| Telefone                                      Frete                            |
| CPF/CNPJ                                      Total                            |
| Endereço                                      Método de pagamento              |
| Método de entrega                             [Finalizar pedido]               |
+--------------------------------------------------------------------------------+
| Selos: SSL | pagamento seguro | dados protegidos                               |
+--------------------------------------------------------------------------------+
```

---

## 16.2 Checkout tablet

```text
+------------------------------------------------------------+
| HEADER CHECKOUT                                            |
+------------------------------------------------------------+
| Dados do cliente                                           |
| Endereço                                                   |
| Entrega                                                    |
+------------------------------------------------------------+
| Resumo do pedido                                           |
| Pagamento                                                  |
| [Finalizar pedido]                                         |
+------------------------------------------------------------+
```

---

## 16.3 Checkout mobile

```text
+-------------------------------------+
| CHECKOUT MOBILE                     |
| Logo          Compra segura         |
+-------------------------------------+
| 1. Dados do cliente                 |
| Nome                                |
| E-mail                              |
| Telefone                            |
+-------------------------------------+
| 2. Endereço de entrega              |
| CEP                                 |
| Rua                                 |
| Número                              |
| Bairro                              |
| Cidade                              |
+-------------------------------------+
| 3. Entrega                          |
| Opções de frete                     |
+-------------------------------------+
| 4. Pagamento                        |
| Método de pagamento                 |
+-------------------------------------+
| Resumo do pedido                    |
| Total                               |
| [FINALIZAR PEDIDO]                  |
+-------------------------------------+
```

### Regras do checkout

- Header simplificado.
- Remover distrações.
- Evitar links que tirem o usuário do checkout.
- Campos grandes no mobile.
- Mensagens de erro abaixo do campo correspondente.
- Não tratar dados sensíveis com scripts visuais customizados.
- Usar plugins confiáveis para pagamento, frete, nota fiscal e antifraude.
- Não usar barra inferior mobile comum no checkout.

---

# 17. Tela Pedido recebido / Obrigado

## 17.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| Pedido recebido com sucesso                                                    |
| Número do pedido | Data | Total | Forma de pagamento                           |
+--------------------------------------------------------------------------------+
| Próximos passos                                                                |
| 1. Confirmação por e-mail                                                      |
| 2. Separação do pedido                                                         |
| 3. Envio / retirada                                                            |
+--------------------------------------------------------------------------------+
| Resumo do pedido                                                               |
| Endereço de entrega                                                            |
| [Acompanhar pedido] [Voltar para loja]                                         |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 17.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| Pedido recebido                     |
| Nº do pedido                        |
| Total                               |
| Pagamento                           |
+-------------------------------------+
| Próximos passos                     |
| Confirmação                         |
| Separação                           |
| Entrega                             |
+-------------------------------------+
| [Acompanhar pedido]                 |
| [Voltar para loja]                  |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Confirmar que o pedido foi criado.
- Mostrar número do pedido.
- Oferecer acompanhamento.
- Não deixar o cliente em dúvida.

---

# 18. Minha Conta — Login e cadastro

## 18.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| MINHA CONTA                                                                    |
+--------------------------------------------------------------------------------+
| LOGIN                                      CADASTRO                             |
| E-mail                                     Nome                                 |
| Senha                                      E-mail                               |
| [Entrar]                                   Senha                                |
| Esqueci minha senha                        [Criar conta]                        |
+--------------------------------------------------------------------------------+
| Benefícios: pedidos, endereços, compras rápidas                                |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 18.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| MINHA CONTA                         |
+-------------------------------------+
| Entrar                              |
| E-mail                              |
| Senha                               |
| [Entrar]                            |
| Esqueci minha senha                 |
+-------------------------------------+
| Criar conta                         |
| Nome                                |
| E-mail                              |
| Senha                               |
| [Criar conta]                       |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Formulários em uma coluna.
- Campos grandes e legíveis.
- Mensagens de erro claras.
- Não solicitar dados desnecessários no cadastro inicial.

---

# 19. Minha Conta — Painel principal

## 19.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| MINHA CONTA                                                                    |
+--------------------------------------------------------------------------------+
| MENU LATERAL                 CONTEÚDO                                          |
| Painel                       Olá, [Nome]                                       |
| Pedidos                      Acesse seus pedidos, endereços e dados da conta.   |
| Endereços                    Cards rápidos: [Pedidos] [Endereços] [Dados]      |
| Dados da conta                                                                |
| Sair                                                                          |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 19.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| MINHA CONTA                         |
+-------------------------------------+
| Olá, [Nome]                         |
| Acesse seus dados e pedidos.        |
+-------------------------------------+
| [Pedidos]                           |
| [Endereços]                         |
| [Dados da conta]                    |
| [Sair]                              |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

# 20. Minha Conta — Pedidos

## 20.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| MINHA CONTA > PEDIDOS                                                          |
+--------------------------------------------------------------------------------+
| MENU LATERAL       TABELA DE PEDIDOS                                           |
|                    Pedido | Data | Status | Total | Ações                      |
|                    #1234  | ...  | Pago   | R$... | [Ver]                      |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 20.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| MEUS PEDIDOS                        |
+-------------------------------------+
| Pedido #1234                        |
| Data                                |
| Status                              |
| Total                               |
| [Ver detalhes]                      |
+-------------------------------------+
| Pedido #1235                        |
| Data                                |
| Status                              |
| Total                               |
| [Ver detalhes]                      |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- No mobile, não usar tabela larga.
- Cada pedido deve virar card.
- Status precisa ser visualmente claro.

---

# 21. Minha Conta — Detalhes do pedido

## 21.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| Pedido #1234                                                                   |
| Status: Processando                                                            |
+--------------------------------------------------------------------------------+
| Produtos do pedido                                                             |
| Produto | Quantidade | Total                                                   |
+--------------------------------------------------------------------------------+
| Endereço de cobrança | Endereço de entrega                                     |
+--------------------------------------------------------------------------------+
| [Falar sobre este pedido] [Voltar aos pedidos]                                 |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 21.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| Pedido #1234                        |
| Status                              |
+-------------------------------------+
| Produto                             |
| Quantidade                          |
| Total                               |
+-------------------------------------+
| Entrega                             |
| Endereço                            |
+-------------------------------------+
| [Falar sobre este pedido]           |
| [Voltar]                            |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

# 22. Minha Conta — Endereços

## 22.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| MINHA CONTA > ENDEREÇOS                                                        |
+--------------------------------------------------------------------------------+
| MENU LATERAL       ENDEREÇO DE COBRANÇA        ENDEREÇO DE ENTREGA             |
|                    Dados do endereço           Dados do endereço               |
|                    [Editar]                     [Editar]                        |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 22.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| ENDEREÇOS                           |
+-------------------------------------+
| Cobrança                            |
| Endereço salvo                      |
| [Editar]                            |
+-------------------------------------+
| Entrega                             |
| Endereço salvo                      |
| [Editar]                            |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

# 23. Minha Conta — Editar dados

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| DADOS DA CONTA                      |
+-------------------------------------+
| Nome                                |
| Sobrenome                           |
| E-mail                              |
| Senha atual                         |
| Nova senha                          |
| Confirmar nova senha                |
| [Salvar alterações]                 |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Não mostrar senha em texto puro.
- Alteração de senha deve ser clara.
- Validação visual não deve depender apenas de cor.

---

# 24. Minha Conta — Recuperar senha

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| RECUPERAR SENHA                     |
| Informe seu e-mail para receber     |
| instruções de redefinição.          |
+-------------------------------------+
| E-mail                              |
| [Enviar instruções]                 |
+-------------------------------------+
| Voltar para login                   |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regra de segurança

A mensagem deve ser neutra, sem confirmar se o e-mail existe ou não.

---

# 25. Tela Contato / Atendimento

## 25.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| CONTATO                                                                        |
| Fale com a MSN Distribuidora                                                   |
+--------------------------------------------------------------------------------+
| FORMULÁRIO DE CONTATO                   INFORMAÇÕES DE ATENDIMENTO             |
| Nome                                     WhatsApp                               |
| E-mail                                   Telefone                               |
| Telefone                                 E-mail                                 |
| Assunto                                  Endereço                               |
| Mensagem                                 Horário de atendimento                 |
| [Enviar mensagem]                        Mapa                                   |
+--------------------------------------------------------------------------------+
| CTA: Precisa de ajuda para encontrar um toner/cartucho?                         |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 25.2 Tablet

```text
+------------------------------------------------------------+
| HEADER                                                     |
+------------------------------------------------------------+
| CONTATO                                                    |
+------------------------------------------------------------+
| Informações rápidas                                        |
| WhatsApp | Telefone | E-mail                               |
+------------------------------------------------------------+
| Formulário                                                 |
+------------------------------------------------------------+
| Mapa                                                       |
+------------------------------------------------------------+
| FOOTER                                                     |
+------------------------------------------------------------+
```

---

## 25.3 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| CONTATO                             |
| Como podemos ajudar?                |
+-------------------------------------+
| [Chamar no WhatsApp]                |
| [Ligar agora]                       |
| [Enviar e-mail]                     |
+-------------------------------------+
| Formulário                          |
| Nome                                |
| E-mail                              |
| Telefone                            |
| Assunto                             |
| Mensagem                            |
| [Enviar]                            |
+-------------------------------------+
| Endereço                            |
| Mapa                                |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- WhatsApp deve ser o CTA mais forte.
- Telefone deve ser clicável no mobile.
- E-mail deve usar `mailto:`.
- Formulário precisa de proteção contra spam.
- Mapa não deve ser pesado; carregar apenas se necessário.

---

# 26. Tela Sobre a empresa

## 26.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| SOBRE A MSN DISTRIBUIDORA                                                      |
| Texto institucional + imagem da empresa/produtos                               |
+--------------------------------------------------------------------------------+
| Blocos de confiança                                                            |
| Experiência | Atendimento | Produtos | Entrega                                  |
+--------------------------------------------------------------------------------+
| Nossa atuação                                                                  |
| Impressoras, toners, cartuchos e suprimentos                                   |
+--------------------------------------------------------------------------------+
| Localização / atendimento                                                      |
+--------------------------------------------------------------------------------+
| CTA: Fale com a equipe                                                         |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 26.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| SOBRE A MSN                         |
| Texto curto                         |
+-------------------------------------+
| Experiência                         |
| Atendimento                         |
| Produtos                            |
| Entrega                             |
+-------------------------------------+
| Nossa atuação                       |
+-------------------------------------+
| [Falar com a equipe]                |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Evitar texto institucional longo no topo.
- Usar blocos de confiança.
- Mostrar diferenciais reais.

---

# 27. Telas de políticas

## 27.1 Trocas e devoluções

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| TROCAS E DEVOLUÇÕES                 |
+-------------------------------------+
| 1. Prazo para solicitação           |
| 2. Condições do produto             |
| 3. Produtos com defeito             |
| 4. Como solicitar troca             |
| 5. Canais de atendimento            |
+-------------------------------------+
| [Falar com atendimento]             |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

## 27.2 Política de privacidade

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| POLÍTICA DE PRIVACIDADE             |
+-------------------------------------+
| Dados coletados                     |
| Finalidade                          |
| Compartilhamento                    |
| Cookies                             |
| Segurança                           |
| Direitos do usuário                 |
| Contato                             |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

## 27.3 Termos de uso

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| TERMOS DE USO                       |
+-------------------------------------+
| Uso do site                         |
| Cadastro                            |
| Compra                              |
| Pagamento                           |
| Entrega                             |
| Responsabilidades                   |
| Alterações dos termos               |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

## 27.4 Frete e entrega

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| FRETE E ENTREGA                     |
+-------------------------------------+
| Regiões atendidas                   |
| Prazos                              |
| Frete grátis                        |
| Retirada, se existir                |
| Rastreamento                        |
| Problemas com entrega               |
+-------------------------------------+
| [Consultar atendimento]             |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Linguagem clara.
- Evitar excesso de juridiquês.
- Políticas acessíveis no footer e no checkout.
- Política de privacidade deve estar alinhada com LGPD.

---

# 28. Tela FAQ / Dúvidas frequentes

## 28.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| DÚVIDAS FREQUENTES                                                             |
+--------------------------------------------------------------------------------+
| Categorias de dúvida                                                           |
| Compra | Pagamento | Entrega | Produto | Troca                                 |
+--------------------------------------------------------------------------------+
| Sanfonas de perguntas                                                          |
| Pergunta 1                                                                     |
| Resposta                                                                       |
| Pergunta 2                                                                     |
| Resposta                                                                       |
+--------------------------------------------------------------------------------+
| CTA atendimento                                                                |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 28.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| DÚVIDAS FREQUENTES                  |
+-------------------------------------+
| [Compra] [Entrega] [Produto]        |
+-------------------------------------+
| Pergunta em sanfona                 |
| Pergunta em sanfona                 |
| Pergunta em sanfona                 |
+-------------------------------------+
| [Falar com atendimento]             |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Usar accordion/sanfona.
- Evitar blocos gigantes de texto.
- Responder dúvidas que reduzem abandono de carrinho.

---

# 29. Tela Marcas

## 29.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| MARCAS                                                                         |
| Encontre produtos por fabricante                                               |
+--------------------------------------------------------------------------------+
| Grade de marcas                                                                |
| HP | Brother | Epson | Canon | Samsung | Outras                                |
+--------------------------------------------------------------------------------+
| Produtos por marca selecionada                                                 |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 29.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| MARCAS                              |
+-------------------------------------+
| [Buscar marca]                      |
+-------------------------------------+
| HP                                  |
| Brother                             |
| Epson                               |
| Canon                               |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

# 30. Tela Ofertas

## 30.1 Desktop

```text
+--------------------------------------------------------------------------------+
| HEADER                                                                         |
+--------------------------------------------------------------------------------+
| OFERTAS                                                                        |
| Produtos com condições especiais                                               |
+--------------------------------------------------------------------------------+
| Filtros                         Produtos em oferta                             |
| Categoria                       Card | Card | Card                              |
| Preço                           Card | Card | Card                              |
+--------------------------------------------------------------------------------+
| FOOTER                                                                         |
+--------------------------------------------------------------------------------+
```

---

## 30.2 Mobile

```text
+-------------------------------------+
| HEADER MOBILE                       |
+-------------------------------------+
| OFERTAS                             |
| Condições especiais                 |
+-------------------------------------+
| [Filtrar] [Ordenar]                 |
+-------------------------------------+
| Card produto                        |
| Card produto                        |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

# 31. Blog / Conteúdo

Esta tela é opcional, mas recomendada para SEO e educação do cliente.

## 31.1 Blog listagem

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| BLOG                                |
| Conteúdos sobre impressoras,        |
| toners, cartuchos e manutenção.     |
+-------------------------------------+
| Card artigo                         |
| Card artigo                         |
| Card artigo                         |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

---

## 31.2 Artigo

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| Título do artigo                    |
| Data / categoria                    |
+-------------------------------------+
| Conteúdo                            |
| Imagens                             |
| Links para produtos relacionados    |
+-------------------------------------+
| CTA atendimento/produtos            |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Artigos devem direcionar para produtos relacionados.
- Evitar conteúdo genérico sem conexão com venda.

---

# 32. Tela 404

```text
+-------------------------------------+
| HEADER                              |
+-------------------------------------+
| Página não encontrada               |
|                                     |
| O link pode ter mudado ou o produto |
| pode não estar mais disponível.     |
|                                     |
| [Buscar produto]                    |
| [Voltar para home]                  |
| [Falar com especialista]            |
+-------------------------------------+
| Categorias principais               |
+-------------------------------------+
| FOOTER                              |
+-------------------------------------+
```

### Regras

- Não deixar o usuário preso.
- Oferecer busca, categorias e atendimento.
- A 404 deve recuperar navegação e venda.

---

# 33. Tela de manutenção

```text
+-------------------------------------+
| LOGO                                |
+-------------------------------------+
| Estamos ajustando nossa loja        |
| para melhorar sua experiência.      |
|                                     |
| Atendimento continua disponível:    |
| [WhatsApp]                          |
| [E-mail]                            |
+-------------------------------------+
```

---

# 34. Componentes reutilizáveis

## 34.1 Card de benefício

```text
+-------------------------------+
| Ícone                         |
| Título                        |
| Texto curto                   |
+-------------------------------+
```

Exemplos:

- Frete para São Paulo e Capital;
- Compra segura;
- Atendimento especializado;
- Mais de 15 anos de mercado;
- Produtos para impressoras, toners e cartuchos.

---

## 34.2 Card de produto desktop

```text
+------------------------------+
| Imagem                       |
| Nome do produto              |
| Código/SKU                   |
| Preço                        |
| Parcelamento                 |
| [Comprar]                    |
+------------------------------+
```

---

## 34.3 Card de produto mobile

```text
+-------------------------------------+
| Imagem grande                       |
| Nome do produto                     |
| Código/SKU                          |
| Preço destacado                     |
| [Comprar]                           |
| [WhatsApp] opcional                 |
+-------------------------------------+
```

### Regras do card de produto

- Imagem limpa.
- Nome legível.
- Preço destacado.
- CTA claro.
- Compatibilidade visível quando necessário.
- Altura consistente em grids.

---

## 34.4 Formulários

```text
+-------------------------------------+
| Label do campo                      |
| [Input]                             |
| Mensagem de erro/sucesso            |
+-------------------------------------+
```

### Regras

- Label sempre visível.
- Placeholder não substitui label.
- Mensagem de erro específica.
- Campos com altura confortável no mobile.
- Telefone, CEP e e-mail com teclado correto no celular.

---

## 34.5 Bloco CTA WhatsApp

```text
+-------------------------------------+
| Precisa de ajuda para escolher?     |
| Nossa equipe pode orientar você.    |
| [Falar com especialista]            |
+-------------------------------------+
```

### Onde usar

- Home;
- Produto;
- Categoria;
- Busca sem resultado;
- Contato;
- Footer;
- Carrinho vazio.

---

# 35. Mini carrinho / carrinho lateral

## 35.1 Desktop

```text
+-------------------------------------+
| MINI CARRINHO                       |
+-------------------------------------+
| Produto                             |
| Qtd | Subtotal                      |
+-------------------------------------+
| Produto                             |
| Qtd | Subtotal                      |
+-------------------------------------+
| Total                               |
| [Ver carrinho]                      |
| [Finalizar compra]                  |
+-------------------------------------+
```

---

## 35.2 Mobile

```text
+-------------------------------------+
| CARRINHO                            |
+-------------------------------------+
| Produto                             |
| Qtd                                 |
| Subtotal                            |
+-------------------------------------+
| Total                               |
| [Finalizar compra]                  |
| [Ver carrinho]                      |
+-------------------------------------+
```

### Regras

- Abrir rápido.
- Fechar facilmente.
- Não cobrir botões críticos sem opção de fechar.
- Não substituir o carrinho completo.

---

# 36. Modal de filtro mobile

```text
+-------------------------------------+
| FILTRAR PRODUTOS              X     |
+-------------------------------------+
| Categoria                           |
| Marca                               |
| Preço                               |
| Compatibilidade                     |
| Disponibilidade                     |
+-------------------------------------+
| [Limpar filtros] [Aplicar filtros]  |
+-------------------------------------+
```

### Regras

- Sempre ter botão de fechar.
- Aplicar filtros com feedback visual.
- Evitar filtros pequenos demais para toque.

---

# 37. Uso de HTML, CSS e JS no Elementor

## 37.1 Onde usar HTML customizado

Usar HTML customizado para:

- hero especial da home;
- blocos de benefício;
- banners de confiança;
- footer mais elaborado;
- carrossel leve de marcas/clientes;
- CTA de WhatsApp;
- microinterações visuais;
- header customizado, se necessário.

Evitar HTML customizado para:

- carrinho;
- checkout;
- cálculo de frete;
- preço;
- pagamento;
- login;
- cadastro;
- dados da conta.

---

## 37.2 Padrão obrigatório de classes

Todas as classes customizadas devem usar prefixo:

```css
.msn-
```

Exemplos:

```css
.msn-header {}
.msn-topbar {}
.msn-search {}
.msn-hero {}
.msn-benefits {}
.msn-product-card {}
.msn-footer {}
.msn-whatsapp-cta {}
.msn-mobile-menu {}
```

Evitar:

```css
.header {}
.menu {}
.btn {}
.logo {}
.card {}
.container {}
.footer {}
```

Motivo: evitar conflito com Elementor, WooCommerce, tema e plugins.

---

## 37.3 JavaScript permitido

Usar JavaScript para:

- abrir/fechar menu mobile;
- abrir/fechar filtro mobile;
- accordion do footer;
- accordion do FAQ;
- carrossel leve;
- CTA fixo ao rolar;
- pequenos feedbacks visuais;
- scroll suave.

---

## 37.4 JavaScript proibido

Não usar JS customizado para:

- alterar preço;
- recalcular frete;
- manipular pagamento;
- validar dados sensíveis sozinho;
- sobrescrever checkout;
- esconder erros do WooCommerce;
- alterar totais do carrinho;
- criar botão falso de compra.

---

# 38. Esqueleto HTML do header final

> Este é um esqueleto estrutural. URLs, textos e ícones devem ser ajustados no Elementor/WooCommerce.

```html
<header class="msn-header" role="banner">
  <div class="msn-topbar" aria-label="Benefícios da loja">
    <span>Frete grátis SP e Capital</span>
    <span>Compra segura</span>
    <span>+15 anos no mercado</span>
    <a class="msn-topbar__whatsapp" href="https://wa.me/55XXXXXXXXXXX">
      Atendimento WhatsApp
    </a>
  </div>

  <div class="msn-mainbar">
    <button class="msn-menu-toggle" type="button" aria-label="Abrir menu">
      ☰
    </button>

    <a class="msn-logo" href="/" aria-label="MSN Distribuidora - Página inicial">
      MSN Distribuidora
    </a>

    <form class="msn-search" role="search" method="get" action="/">
      <label class="screen-reader-text" for="msn-search-field">
        Buscar produtos
      </label>
      <input
        id="msn-search-field"
        type="search"
        name="s"
        placeholder="Buscar toner, cartucho, impressora ou código..."
      >
      <input type="hidden" name="post_type" value="product">
      <button type="submit" aria-label="Pesquisar">🔍</button>
    </form>

    <nav class="msn-actions" aria-label="Ações do usuário">
      <a href="/minha-conta/">Conta</a>
      <a href="/minha-conta/orders/">Pedidos</a>
      <a href="/carrinho/" class="msn-cart-link">Carrinho</a>
    </nav>
  </div>

  <nav class="msn-quickbar" aria-label="Navegação principal da loja">
    <a class="msn-quickbar__whatsapp" href="https://wa.me/55XXXXXXXXXXX">
      Fale com especialista
    </a>
    <a href="/categoria-produto/impressoras/">Impressoras</a>
    <a href="/categoria-produto/toners/">Toners</a>
    <a href="/categoria-produto/cartuchos/">Cartuchos</a>
    <a href="/ofertas/">Ofertas</a>
    <a href="/cotacao/">Cotação rápida</a>
  </nav>
</header>
```

---

# 39. CSS inicial do header final

```css
:root {
  --msn-primary: #0F4C81;
  --msn-primary-dark: #0B2F4F;
  --msn-primary-soft: #EAF4FF;
  --msn-success: #16A34A;
  --msn-warning: #F59E0B;
  --msn-text: #1F2937;
  --msn-muted: #6B7280;
  --msn-border: #E5E7EB;
  --msn-white: #FFFFFF;
}

.msn-header {
  width: 100%;
  background: var(--msn-white);
  color: var(--msn-text);
  border-bottom: 1px solid var(--msn-border);
  position: sticky;
  top: 0;
  z-index: 999;
}

.msn-topbar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  padding: 8px 16px;
  font-size: 13px;
  background: var(--msn-primary-dark);
  color: #fff;
}

.msn-topbar a {
  color: #fff;
  text-decoration: none;
  font-weight: 700;
}

.msn-mainbar {
  display: grid;
  grid-template-columns: auto minmax(160px, 220px) minmax(320px, 1fr) auto;
  align-items: center;
  gap: 20px;
  max-width: 1240px;
  margin: 0 auto;
  padding: 16px 20px;
}

.msn-logo {
  font-weight: 800;
  text-decoration: none;
  color: var(--msn-primary-dark);
}

.msn-search {
  display: flex;
  border: 2px solid var(--msn-border);
  border-radius: 999px;
  overflow: hidden;
  background: #fff;
}

.msn-search:focus-within {
  border-color: var(--msn-primary);
  box-shadow: 0 0 0 4px rgba(15, 76, 129, 0.12);
}

.msn-search input {
  flex: 1;
  border: 0;
  padding: 12px 18px;
  outline: none;
  min-width: 0;
}

.msn-search button {
  border: 0;
  padding: 0 18px;
  background: var(--msn-primary);
  color: #fff;
  cursor: pointer;
}

.msn-actions,
.msn-quickbar {
  display: flex;
  align-items: center;
  gap: 18px;
}

.msn-actions a,
.msn-quickbar a {
  color: var(--msn-text);
  text-decoration: none;
  font-weight: 600;
}

.msn-quickbar {
  justify-content: center;
  padding: 10px 20px;
  border-top: 1px solid var(--msn-border);
}

.msn-quickbar__whatsapp {
  color: var(--msn-success) !important;
  font-weight: 800 !important;
}

.msn-menu-toggle {
  display: none;
}

@media (max-width: 1024px) {
  .msn-mainbar {
    grid-template-columns: minmax(140px, 220px) 1fr auto;
  }

  .msn-search {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .msn-topbar {
    justify-content: flex-start;
    gap: 12px;
    font-size: 12px;
    overflow-x: auto;
    white-space: nowrap;
  }

  .msn-mainbar {
    grid-template-columns: auto 1fr auto;
    gap: 12px;
    padding: 12px 16px;
  }

  .msn-menu-toggle {
    display: inline-flex;
    border: 0;
    background: transparent;
    font-size: 24px;
  }

  .msn-logo {
    text-align: center;
  }

  .msn-search {
    grid-column: 1 / -1;
    order: 4;
  }

  .msn-actions a:not(.msn-cart-link) {
    display: none;
  }

  .msn-quickbar {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    padding: 8px 16px;
  }

  .msn-quickbar a:not(.msn-quickbar__whatsapp) {
    display: none;
  }

  .msn-quickbar::before {
    content: "Modelo da impressora";
    display: inline-flex;
    justify-content: center;
    align-items: center;
    border: 1px solid var(--msn-border);
    border-radius: 999px;
    padding: 8px 10px;
    font-weight: 700;
    color: var(--msn-primary-dark);
  }

  .msn-quickbar__whatsapp {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    border: 1px solid rgba(22, 163, 74, .35);
    border-radius: 999px;
    padding: 8px 10px;
    background: rgba(22, 163, 74, .08);
  }
}
```

---

# 40. JS inicial

```html
<script>
document.addEventListener('DOMContentLoaded', function () {
  const header = document.querySelector('.msn-header');
  const menuButton = document.querySelector('.msn-menu-toggle');

  if (header) {
    window.addEventListener('scroll', function () {
      header.classList.toggle('is-compact', window.scrollY > 80);
    });
  }

  if (menuButton) {
    menuButton.addEventListener('click', function () {
      document.body.classList.toggle('msn-menu-open');
    });
  }
});
</script>
```

### Observação

Esse JS é apenas estrutural. Para produção, o menu off-canvas precisa ter:

- controle de foco;
- fechamento com tecla `Esc`;
- fechamento ao clicar fora;
- atributo `aria-expanded`;
- bloqueio de rolagem do body.

---

# 41. Segurança

## 41.1 Segurança no WordPress/WooCommerce

Checklist obrigatório:

```text
[ ] WordPress atualizado.
[ ] WooCommerce atualizado.
[ ] Elementor e Elementor Pro atualizados.
[ ] Tema atualizado.
[ ] Plugins inativos removidos.
[ ] Plugins abandonados removidos.
[ ] Nenhum plugin ou tema nulled/pirata.
[ ] HTTPS ativo.
[ ] Senhas fortes.
[ ] 2FA para administradores.
[ ] Limite de tentativas de login.
[ ] Backups automáticos.
[ ] Ambiente de staging para mudanças críticas.
[ ] Monitoramento de logs.
[ ] Plugin de segurança confiável.
[ ] Permissões corretas de usuários.
```

---

## 41.2 Segurança no header

- Links de conta e carrinho devem usar URLs oficiais do WooCommerce.
- WhatsApp deve usar link correto e mensagem pré-definida sem dados sensíveis.
- Menu não deve apontar para URLs temporárias.
- Não inserir scripts externos desconhecidos.

---

## 41.3 Segurança no produto

- Preço e estoque devem vir do WooCommerce.
- Não criar preço manual em HTML para produto vendido pelo carrinho.
- Não criar botão falso de compra.
- SKU e compatibilidade devem ser informativos, não substitutos da lógica do produto.

---

## 41.4 Segurança no carrinho

- Totais, cupons e frete devem ser processados pelo WooCommerce.
- Não usar JS para calcular total final.
- Não esconder mensagens de erro.
- Não alterar subtotal visualmente fora da lógica do WooCommerce.

---

## 41.5 Segurança no checkout

- Usar SSL.
- Usar plugins de pagamento confiáveis.
- Minimizar scripts.
- Não adicionar scripts externos desconhecidos.
- Não manipular campos de pagamento com JS próprio.
- Testar checkout em celular real.
- Manter políticas acessíveis.

---

## 41.6 Segurança em formulários

- Usar reCAPTCHA, Turnstile ou honeypot.
- Validar dados no servidor.
- Não confiar apenas em validação front-end.
- Evitar exposição de e-mails administrativos.
- Mensagens de erro devem ser claras e não revelar dados sensíveis.

---

## 41.7 Cuidados com XSS

Evitar:

```js
element.innerHTML = valorVindoDoUsuario;
```

Preferir:

```js
element.textContent = valorSeguro;
```

Nunca inserir no HTML/JS:

- tokens;
- chaves de API;
- credenciais;
- dados sensíveis;
- informações internas.

---

# 42. Performance

## 42.1 Boas práticas

```text
[ ] Usar imagens WebP.
[ ] Comprimir imagens.
[ ] Ativar lazy loading.
[ ] Evitar vídeos pesados no hero.
[ ] Evitar animações pesadas.
[ ] Reduzir plugins.
[ ] Usar cache.
[ ] Não carregar scripts em páginas onde não são usados.
[ ] Reduzir CSS duplicado.
[ ] Testar em celular real.
```

---

## 42.2 Elementor

- Usar Containers/Flexbox.
- Evitar excesso de widgets aninhados.
- Criar templates globais.
- Padronizar cores e fontes no Design System do Elementor.
- Evitar copiar blocos com IDs duplicados.
- Usar classes CSS personalizadas.

---

# 43. Acessibilidade

Checklist:

```text
[ ] Botões com texto claro.
[ ] Contraste suficiente.
[ ] Links com aria-label quando necessário.
[ ] Imagens com alt.
[ ] Navegação por teclado.
[ ] Foco visível.
[ ] Não depender apenas de cor.
[ ] Respeitar prefers-reduced-motion.
```

CSS recomendado:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    scroll-behavior: auto !important;
  }
}
```

---

# 44. SEO e conteúdo

## 44.1 Regras gerais

- H1 único por página.
- H2 para seções principais.
- Descrições de categoria com palavras-chave naturais.
- Descrições de produtos completas.
- URLs amigáveis.
- Imagens com nomes descritivos.
- Schema de produto via WooCommerce/plugin SEO.
- Meta title e meta description por produto/categoria.
- Blog técnico opcional para atrair buscas orgânicas.

---

## 44.2 Conteúdo recomendado para blog

- Como escolher toner correto.
- Diferença entre toner original, compatível e remanufaturado.
- Como saber se o cartucho é compatível.
- Cuidados com impressora laser.
- Quando trocar toner.
- Como reduzir custo de impressão em empresas.
- Guia de impressoras para escritórios.

---

# 45. Ordem de implementação

## Fase 1 — Estrutura global

```text
1. Header desktop/tablet/mobile.
2. Footer desktop/tablet/mobile.
3. Paleta visual e tipografia.
4. Padrões de botão, card e formulário.
```

---

## Fase 2 — Telas comerciais

```text
1. Home.
2. Categorias.
3. Subcategorias.
4. Busca.
5. Produto.
```

---

## Fase 3 — Fluxo de compra

```text
1. Carrinho com produto.
2. Carrinho vazio.
3. Checkout.
4. Pedido recebido.
5. Mini carrinho.
```

---

## Fase 4 — Área do cliente

```text
1. Login/cadastro.
2. Painel minha conta.
3. Pedidos.
4. Detalhes do pedido.
5. Endereços.
6. Dados da conta.
7. Recuperar senha.
```

---

## Fase 5 — Telas institucionais

```text
1. Contato.
2. Sobre.
3. Políticas.
4. FAQ.
5. Marcas.
6. Blog, se necessário.
7. 404.
```

---

## Fase 6 — Otimização

```text
1. Responsividade final.
2. Performance mobile.
3. Segurança.
4. Testes de compra.
5. Testes de formulário.
6. Testes em celulares reais.
```

---

# 46. Checklist geral por tela

Cada tela só deve ser aprovada após cumprir:

```text
[ ] Header aparece corretamente.
[ ] Busca funciona no desktop, tablet e mobile.
[ ] Carrinho está visível.
[ ] WhatsApp está acessível.
[ ] Conteúdo principal está claro.
[ ] CTA principal aparece antes da dobra no mobile, quando aplicável.
[ ] Footer está completo.
[ ] Não há rolagem horizontal no mobile.
[ ] Botões têm tamanho confortável para toque.
[ ] Textos são legíveis em 320px.
[ ] Imagens não quebram layout.
[ ] Formulários têm labels visíveis.
[ ] Mensagens de erro são claras.
[ ] Nenhum JS customizado altera preço, frete ou pagamento.
[ ] Página carrega rápido no celular.
[ ] Checkout foi testado em celular real.
```

---

# 47. Checklist específico mobile

```text
[ ] Layout em uma coluna.
[ ] Header não ocupa espaço exagerado.
[ ] Busca visível no topo.
[ ] Carrinho acessível no topo.
[ ] Menu abre em gaveta.
[ ] Produtos têm imagem e preço claros.
[ ] Botão comprar é grande.
[ ] Footer não fica confuso.
[ ] Elementos fixos não cobrem conteúdo.
[ ] Modais têm botão fechar.
[ ] Formulários são fáceis de preencher.
[ ] Teclado aberto não quebra checkout.
[ ] WhatsApp não cobre botão comprar.
```

---

# 48. Checklist de segurança

```text
[ ] Nenhum JS altera preço, frete, total ou pagamento.
[ ] Nenhum script externo desconhecido foi adicionado.
[ ] O código foi testado antes da publicação.
[ ] Header não quebra checkout, carrinho ou login.
[ ] Formulários têm proteção antispam.
[ ] Links de conta/carrinho usam rotas oficiais.
[ ] Checkout usa SSL.
[ ] Plugins estão atualizados.
[ ] Admin tem 2FA.
[ ] Backups automáticos estão ativos.
```

---

# 49. Conclusão

A documentação final define um e-commerce com foco em:

```text
Busca forte + atendimento pelo WhatsApp + confiança + compra mobile simples
```

A decisão mais importante para o header é usar a **Opção A em desktop e tablet**, mas substituindo o item “Departamentos” por um acesso direto ao **WhatsApp / Fale com especialista**. As categorias continuam disponíveis no menu, e no mobile continuam acessíveis pelo menu hambúrguer.

O resultado esperado é uma loja mais profissional, mais clara, mais segura e mais adequada ao comportamento do cliente que acessa pelo celular.

A prioridade de design deve ser:

```text
1. Encontrar o produto certo.
2. Entender compatibilidade.
3. Comprar com segurança.
4. Falar com atendimento sem atrito.
5. Navegar bem no celular.
```
