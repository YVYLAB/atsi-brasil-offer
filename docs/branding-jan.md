# JAN — aplicação do kit visual fornecido

## Escopo

Identidade aplicada somente quando `company=jan`. Não altera ATSI, funcionalidades,
preços, horas, planos, descontos, dependências, campanhas ou serviços mensais.
O fundo fotográfico e os textos das features continuam compartilhados.

Kit: `JAN_Kit_Branding_YvyLab_OpenCode.zip`, fornecido pelo usuário.
SHA-256: `510025725edf80fba27a33b5db8cc33bde4b78ba05bf338b63752c905f76948d`.

## Visual

- Azul-petróleo `#24363F`, antracite `#2F3A3D` e laranja `#FF8031`, conforme
  tokens aproximados do kit. Não são códigos homologados pela JAN.
- Textos claros nos painéis escuros; cartões claros no mockup.
- Laranja escuro `#A84600` em rótulos pequenos sobre fundo claro e botões
  com texto branco. Botão principal laranja tem texto escuro, não branco.
- Montserrat local: fonte observada no CSS do site da JAN, reutilizando o
  arquivo compartilhado, sem dependência do Google Fonts.
- Faixa geométrica do kit como detalhe sutil no cabeçalho. Não substitui a
  marca nem remove o fundo fotográfico padrão.
- Título **JAN+**, pela decisão posterior do vendedor de padronizar todas as
  plataformas como nome curto da empresa + `+`. Isso substitui a sugestão de
  naming do kit; não altera a arte institucional nem afirma registro de marca.
- Apresentação comercial sem avisos de falta de aprovação na entrada,
  configurador ou PDF, por decisão do vendedor. As ressalvas sobre a origem
  do kit e homologação da marca ficam apenas na documentação interna.

## Assets

O ZIP não continha os bytes dos logos, apenas referências e instruções.
Na integração, os dois assets de campanha citados pelo kit foram obtidos e
validados temporariamente, mas não aplicados como logo institucional.

Também foi consultada a página `https://www.jan.com.br/contato`, que publica
o logo institucional usado no cabeçalho e o favicon. Esses dois arquivos foram
baixados e preservados **sem edição, recoloração, recorte ou reconstrução**:

- `assets/companies/jan/logo-institucional.svg`
- `assets/companies/jan/icon.png`

URLs de origem, tamanhos e hashes SHA-256 constam em
`assets/companies/jan/sources.json`. O mesmo SVG original é usado nas aplicações
institucional e conceitual da plataforma, sem inventar uma segunda marca.
Isso não equivale a autorização de uso em produção.

Arquivos de referência extraídos do kit, sem alteração:

- `branding/jan-kit/branding-jan.md`
- `branding/jan-kit/README.md`
- `branding/jan-kit/jan-theme.css`
- `branding/jan-kit/jan-theme.json`
- `branding/jan-kit/fontes-oficiais.json`
- `assets/companies/jan/decor/faixa-agro.svg`
- `assets/companies/jan/decor/linhas-campo.svg`

Os documentos originais descrevem a situação anterior dos downloads e uma
estrutura de kit completa. Neste repositório foram preservadas as referências
acima; não é uma cópia executável integral do kit.

## Configuração e alterações

- `assets/companies/jan/theme.css`: tokens adaptados e regras exclusivas JAN.
- `branding/product-config.js`: caminhos da arte original, título e MIME.
- `index.html` e `home.html`: título derivado do nome curto da empresa + `+`.
- `tests/test_white_label.py`: identidade, integridade dos originais, PDFs,
  igualdade comercial ATSI/JAN e layouts mobile/tablet/desktop.

As correções anteriores da logo ATSI Brasil na entrada foram preservadas.

## Validação e publicação

Executar a suíte Python e os testes Node usuais. O teste de identidade verifica
assets carregados e ausência de avisos de falta de aprovação em 390, 768 e 1440 px. Os testes existentes
cobrem geração de PDF, manutenção, presets e restauração das campanhas.

Esta alteração é local: não publica nem envia a demonstração à JAN. Solicitar
autorização e arquivos de marca aprovados antes de tratar o estudo como
plataforma oficial da empresa.
