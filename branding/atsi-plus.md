# ATSI+ — proposta de identidade de produto

ATSI+ é o nome comercial proposto da plataforma digital. ATSI Brasil permanece
a instituição cliente e proprietária; YvyLab, a desenvolvedora e autora da
proposta tecnológica. Não há afirmação de registro de marca ou disponibilidade
em lojas. Identidade sujeita à aprovação da ATSI.

Slogan proposto: **Conhecimento. Conexões. Oportunidades.**

## Aplicação
- Configuração central em `branding/product-config.js`.
- Tratamento tipográfico vetorial: `assets/atsi-plus-dark.svg` para fundos escuros
  e `assets/atsi-plus-light.svg` para claros; símbolo em `atsi-plus-icon.svg`.
- SVGs usam texto vetorial com fallback Arial; não são alterações dos logos
  institucionais. A fonte do SVG pode variar conforme o ambiente; para arte-final
  homologada, converter a tipografia aprovada em curvas.
- Paleta usa exclusivamente cores do kit local: navy #173850, verde #59C478,
  texto claro #EFF8F7. São tokens de interface provisórios, não HEX homologados.
- Montserrat local no configurador e telas; preservar proporções e contraste.
- Marca ATSI+ nos mockups, apresentação comercial e propostas exportadas.
- Logo institucional ATSI Brasil preservado, sem edição, no crédito institucional.
- `atsi-plus` é o slug de apresentação; IDs de features e dados persistidos não
  foram renomeados. O snapshot financeiro da oferta não recebe a identidade,
  para não suspender promoções por mudança exclusivamente visual.

## Escopo e limitações
Os mockups são conceitos, não um aplicativo funcional. Features opcionais vistas
isoladamente continuam sinalizadas como apenas visualizadas; superfícies compostas
exibem complementos conforme seleção. Não foram alteradas horas, preços,
mensalidades, dependências, políticas de desconto nem prazo da oferta.
Menu administrativo, senha visual e agendamento de campanha são solicitações
separadas e não foram implementadas neste rebranding.

Manter `branding/` e `pricing-promotion.js` junto ao HTML para funcionamento local.
