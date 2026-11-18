# Apresentação white label por empresa

O configurador e a página de entrada usam a mesma oferta, os mesmos 55 recursos,
dependências, presets, horas, preços e regras de manutenção para todas as empresas.
O parâmetro `company` muda somente a apresentação.

## Links para compartilhar por e-mail

- `index.html?company=atsi-brasil` — entrada com identidade ATSI+.
- `index.html?company=jan` — entrada com identidade JAN.
- `home.html?company=jan` — apresentação direta, sem passar pela entrada.
- Em uma URL que já tenha parâmetros: `home.html?origem=email&company=jan`.

Ao entrar, a navegação preserva a empresa. `company` é obrigatório: ausente,
vazio ou desconhecido redireciona para `404.html`, sem mostrar a apresentação
de outra empresa. Isso vale para entrada, configurador e emissor interno.
O valor é comparado a uma lista explícita; nunca é interpolado livremente
em caminhos de arquivos.

A página exibe **404 — Página não encontrada**. Em hospedagem estática,
o redirecionamento pelo navegador não altera o status HTTP da resposta original;
um status HTTP 404 real para a URL sem empresa exige regra no servidor/hosting.
Essa validação visual não substitui autenticação.

**Não há envio de e-mail, cadastro de clientes nem autenticação real.** Os links
podem ser enviados manualmente. A barreira visual existente não protege os
arquivos públicos e não oferece credenciais próprias por empresa. Esta entrega
personaliza a apresentação comercial, não implementa um aplicativo multiempresa
com bancos, usuários ou permissões isolados.

## Onde editar

```text
assets/companies/
  atsi-brasil/
    logo-dark.svg
    logo-light.svg
    icon.svg
    theme.css
  jan/
    logo-institucional.svg
    icon.png
    theme.css
    sources.json
    decor/
```

Cada `theme.css` sobrescreve somente a identidade da empresa. **Tudo que não
for informado herda a base compartilhada** em `branding/company-theme.css`:
cores de referência, Montserrat, fundo `branding/assets/parallax.jpg`, contraste,
layout e comportamentos. ATSI e JAN usam a mesma imagem de fundo padrão.

Textos comerciais são únicos em `product-copy.js`, com os nomes da plataforma
e da instituição adaptados pela configuração. Não criar cópias dos textos
ou HTMLs por empresa. Catálogo, valores e regras também continuam únicos.

As personalizações previstas são cores, fontes, títulos/nomes, logos e,
opcionalmente, imagens. Um tema pode informar apenas parte das cores.
Para tipografia própria, adicionar um `@font-face` com arquivo local no
`theme.css` da empresa e definir `--brand-font-family`. Sem isso, usa Montserrat.
Inputs, botões e demais controles acompanham a fonte da página.
O PDF mantém sua fonte técnica própria; não incorpora fontes web automaticamente.

Exemplo de personalização opcional em `assets/companies/jan/theme.css`:

```css
/* Exemplo: só usar após adicionar os arquivos oficiais correspondentes. */
@font-face{
  font-family:FonteEmpresa;
  src:url('./fonte.woff2') format('woff2');
  font-display:swap;
}
:root{--brand-font-family:FonteEmpresa,Montserrat,Arial,sans-serif}
:root[data-company="jan"] body{
  background-image:linear-gradient(180deg,#0005,#0009),url('./fundo.jpg');
}
```

O caminho de imagens deve estar em uma propriedade CSS no arquivo da empresa,
como no exemplo, e não em uma variável com URL consumida por outro stylesheet:
nesse último caso, o navegador resolve o caminho relativo ao arquivo consumidor.
Para voltar ao fundo padrão, basta remover a regra `background-image`.

O nome curto da empresa e arquivos de identidade ficam no registro
`branding/product-config.js`. A camada visual comum é
`branding/company-theme.css`. A API `CompanyBranding` resolve identidade, textos,
links e chaves locais. Os nomes internos `ATSIProduct` e IDs técnicos permanecem
por compatibilidade; não são um catálogo diferente por empresa.

O nome/título da plataforma é sempre **nome curto da empresa + `+`**:
`shortName: 'ATSI'` gera **ATSI+** e `shortName: 'JAN'` gera **JAN+**.
A mesma regra vale para entrada, configurador, mockups e identificação nas
propostas/PDF. O nome institucional (`client`) e suas logos não recebem o `+`.
O nome é derivado em um único ponto, sem configurar títulos divergentes por página.

No login, o cabeçalho é simplificado: logo institucional seguida apenas da frase
**“Vamos apresentar a plataforma NOME+.”**, sem título grande ou chamada extra.

### Logo institucional e logo da plataforma

São aplicações distintas:

- `logoDark` / `logoLight`: marca da plataforma, usada nos mockups
  (ATSI+ no caso da ATSI).
- `logoInstitutional`: marca da empresa, usada na entrada e no cabeçalho da apresentação
  (ATSI Brasil, preservando `branding/assets/atsi-logo-cabecalho.svg` sem edição).
  Campo opcional do registro, com caminho relativo à raiz do site. Para outra
  empresa, pode apontar para `assets/companies/<slug>/logo-institucional.svg`.
- Sem `logoInstitutional`, o cabeçalho usa a logo da plataforma daquela empresa,
  nunca a logo institucional ATSI por padrão.

`data-company-logo="institutional"` identifica a aplicação institucional;
`data-company-logo` sem valor identifica a marca da plataforma.

**JAN usa o kit visual fornecido pelo usuário**, com azul-petróleo e laranja
aproximados, Montserrat local e logo/ícone originais obtidos no site da JAN.
A identificação da plataforma é **JAN+**, sem avisos de falta de aprovação
na apresentação comercial ou PDF. A paleta não é um brandbook
homologado; fontes e hashes estão em `assets/companies/jan/sources.json`.
Ver `docs/branding-jan.md` para aplicação, limites e referências do kit.
Os assets ATSI+ também preservam o caráter de proposta de identidade existente.

## Adicionar uma empresa

1. Criar `assets/companies/nome-da-empresa/` com tema e arquivos de identidade.
2. Registrar o slug em `companies`, em `branding/product-config.js`, com
   `client`, `shortName`, `slug` e nomes dos arquivos.
   O nome da plataforma é gerado automaticamente como `shortName` + `+`,
   sem mudar o catálogo ou os valores das features.
   `faviconType` permite ícone PNG; o padrão continua `image/svg+xml`.
3. Revisar contraste, nome, mockups e PDF.
   Incluir a logo institucional em `SOURCES` de
   `branding/scripts/gerar_logos_pdf.py` e regenerar `branding/pdf-logos.js`.
   Esse pacote local coloca a marca no cabeçalho de todas as páginas do PDF,
   sem depender de rede e sem repetir o título.
4. Compartilhar `index.html?company=nome-da-empresa`.

Não copiar `home.html`, catálogo ou tabelas de preço. Não colocar valores,
credenciais ou regras de acesso nos assets de identidade.

## Consistência e limites

- Títulos, metadados no navegador, favicon, logotipos, cores, textos comerciais,
  previews e popups acompanham a empresa.
- JSON inclui `project.company`, nome da empresa e identidade visual.
  PDF usa o cliente, título, cores e nome de arquivo correspondentes.
  Seus textos técnicos são personalizados em uma cópia, sem editar as specs.
- Snapshots de preços preservam os títulos técnicos originais, evitando
  invalidar campanhas por mudanças exclusivamente visuais.
- As campanhas locais da ATSI mantêm a chave `atsi-campaign-v2`.
  Outras empresas recebem o sufixo `:company:slug`; uma campanha não é
  automaticamente aplicada a outra empresa. As regras e valores de tabela
  continuam os mesmos. Importar explicitamente um JSON ainda permite reutilizar
  suas condições; isso não representa autorização comercial no servidor.
- Metadados são alterados com JavaScript. Robôs que não executem JavaScript
  podem continuar exibindo a prévia padrão ATSI ao compartilhar um link.
- Funciona em hospedagem estática e abrindo os HTMLs localmente. As limitações
  anteriores de login/HTTPS e persistência local continuam existindo.

## Testes

`python3 -m unittest discover -s tests -v`

`tests/test_white_label.py` compara snapshots, seleções, horas, implantação,
manutenção e operação dos três planos entre ATSI e JAN; valida identidade,
55 mockups/popups, PDF, isolamento local de campanhas, not found e mobile.
Também verifica o carregamento real do fundo padrão nas três páginas para as
duas empresas, tipografia herdada e temas parciais com personalização.
Exige Chrome para os testes de navegador.
