# Branding ATSI Brasil — pacote de identidade para YvyLab / OpenCode

> **Fonte visual:** site institucional da ATSI Brasil — https://www.atsibrasil.com.br/capa#institucional  
> **Data de referência:** 16/11/2026.  
> **Status:** guia operacional de aplicação visual, **não** manual de marca homologado pela ATSI. Cores são aproximações de interface. A marca e os logotipos pertencem aos seus titulares.

## 1. Objetivo

Aplicar a identidade da **ATSI Brasil — Pesquisa e Consultoria** ao configurador comercial construído pela **YvyLab**, preservando integralmente a lógica de seleção, horas, precificação, dependências, exportação, regras de negócio, layouts responsivos e catálogo de 54 funcionalidades da versão mais atual do projeto OpenCode.

A referência visual desejada é **corporativa, agronômica e tecnológica**, com azul-marinho profundo como base do tema escuro, verde como sinal principal de destaque e padrões agrícolas discretos como textura. Não transformar a interface em tema verde saturado nem confundir a identidade da ATSI com a da YvyLab.

## 2. Logos oficiais identificados no site

| Ativo | URL original, no domínio da ATSI | Uso inicial sugerido |
|---|---|---|
| Logo institucional (`Logo dif`) | `https://www.atsibrasil.com.br/assets/logo-dif-c56ad7a9c36c4768a56ea416da4f0d9b.svg` | Marca principal em superfícies claras |
| Logo do cabeçalho (`Logo`) | `https://www.atsibrasil.com.br/assets/logo-6dbdce245eead0fed844a9778975f7f2.svg` | Verificar visualmente se contrasta com cabeçalho escuro |

Ambas as URLs foram confirmadas como imagens do site institucional; **os arquivos SVG oficiais não foram baixados nesta geração**, porque o ambiente não conseguiu acessar os bytes. Para obter os arquivos originais, execute no computador que tem acesso à internet:

```bash
python3 scripts/baixar_logos_oficiais.py
```

O script grava em `assets/atsi-logo-institucional.svg` e `assets/atsi-logo-cabecalho.svg`, valida que o conteúdo é realmente SVG e registra o hash SHA-256. **Não substitua esses arquivos por marcas desenhadas de memória.** Antes de uso público, conferir permissão de uso junto à ATSI e avaliar a variante correta para fundos claros e escuros.

## 3. Cores de interface

**Paleta provisória inferida visualmente, não HEX oficiais fornecidos pela ATSI.** Se houver um manual de marca, este prevalece.

| Token | HEX | Aplicação |
|---|---|---|
| `--atsi-navy` | `#173850` | Azul-marinho de marca, superfícies e tipografia em fundo claro |
| `--atsi-navy-deep` | `#08131D` | Fundo profundo da aplicação |
| `--atsi-surface` | `#0F2430` | Cards, seções e painéis |
| `--atsi-card` | `#15303B` | Componentes internos |
| `--atsi-green` | `#59C478` | Seleção, progresso e realces |
| `--atsi-green-strong` | `#2C9D54` | Botões e recursos de ação (validar contraste) |
| `--atsi-white` | `#EFF8F7` | Texto em fundo escuro |
| `--atsi-muted` | `#B1C8CF` | Texto secundário |
| `--atsi-border` | `#2A4D56` | Bordas e divisórias |
| `--atsi-amber` | `#E6C67F` | Destaques secundários para feature de escolha única |

Tokens completos em [`branding-tokens.css`](branding-tokens.css) e [`branding-tokens.json`](branding-tokens.json). Não presumir que a aparência escura do configurador corresponda ao site institucional original.

## 4. Aplicação no configurador de features

- **Desktop:** manter duas colunas próximas de 50%/50%: à esquerda três presets no topo e seções expansíveis de features; à direita celular com mockup por feature e total abaixo. No mobile, empilhar sem perder acesso ao total.
- **Cabeçalho:** ATSI Brasil como marca principal; “Desenvolvido por YvyLab” como crédito secundário. Colocar logo em recipiente claro caso necessário para preservar contraste.
- **Seções:** cores discretas por categoria com a paleta ATSI; não usar cores de categoria como identificação única (sempre exibir texto/ícone).
- **Feature cards:** obrigatório, opcional ou escolha única; mostrar horas, complexidade, preço e descrição; foco e seleção com realce verde acessível.
- **Mockup:** mostrar marca ATSI sem esticar SVG ou encobrir o conteúdo; a troca de preview não altera seleção nem preço.
- **Total:** atualizar automaticamente quando for selecionada/deselecionada uma feature ou alterados horas/preço, preservando cálculos existentes. Custo interno real ≠ referência comercial de R$ 200/h.
- **Exportação:** preservar JSON, CSV/PDF caso já implementados. O branding não deve mudar os números do orçamento.
- **Dependências:** preservar escolhas exclusivas de YouTube, Cloudflare Stream e Stream com offline, e regras de dependência já aprovadas.
- **Ambiente:** armazenar logos originais localmente no projeto para não depender do domínio externo em produção; usar fallback textual acessível se faltar o arquivo.

## 5. Assets SVG anexos

### Assets originais deste pacote (não são logos oficiais)

- `assets/atsi-agro-contornos.svg`: padrão vetorial de curvas de nível agrícolas, próprio para fundo discreto.
- `assets/atsi-agro-horizonte.svg`: ilustração geométrica abstrata de campos, própria para hero/banner ou fundo de mockup.

Os dois são **artes decorativas novas** produzidas para este pacote e podem ser ajustados, reduzidos ou removidos sem prejuízo à marca. Não confundir com o logotipo registrado.

### Logos oficiais

Os logos originais devem ser obtidos por `scripts/baixar_logos_oficiais.py`. O ZIP não inclui cópias binárias desses logos, pois o download não pôde ser concluído no ambiente de criação. Em produção, evitar apontar a tag `<img>` diretamente para URLs remotas.

## 6. Exemplos de código

Carregamento local após executar o script de download:

```html
<img src="/assets/atsi-logo-institucional.svg"
     alt="ATSI Brasil — Pesquisa e Consultoria"
     style="width: 150px; height: auto; object-fit: contain" />
```

Exemplo de painel com tokens:

```css
.at-home {
  color: var(--atsi-white);
  background: var(--atsi-navy-deep);
}
.at-card {
  background: var(--atsi-surface);
  border: 1px solid var(--atsi-border);
  border-radius: 16px;
}
.at-selection { border-color: var(--atsi-green); }
```

## 7. Regras de QA para o OpenCode

1. Validar que os SVGs oficiais baixados são íntegros, mantêm `viewBox` e não contêm conteúdo inesperado; registrar origem e hash.
2. Verificar marca em fundo claro, escuro e no mockup; sem distorção e sem texto ilegível.
3. Validar teclado, leitor de tela, foco visível e contraste dos estados principais.
4. Validar responsividade em 390, 768 e 1440 px.
5. Presets Essencial, Plus, Premium e personalizado continuam funcionais; nenhuma feature é perdida.
6. Valor final, horas, dependências e preços devem permanecer idênticos antes/depois da troca visual, para uma mesma seleção.
7. Confirmar que e-books, eventos e promoções do mural permanecem opcionais, enquanto cursos em destaque são obrigatórios.
8. Não representar links de Google Drive como alternativa de produção automaticamente aprovada; continuar respeitando notas técnicas de vídeo.
9. Não declarar “identidade oficial homologada” ou “logo incluído” sem confirmação de sua existência local.

## 8. Fonte e autorização

- Identidade institucional: https://www.atsibrasil.com.br/capa#institucional
- URLs oficiais de imagem: seção 2.
- Trabalho de aplicação/integração: YvyLab, no contexto do configurador ATSI Brasil.
- Este pacote é para preparar uma proposta ou protótipo; confirmar autorização da ATSI antes de distribuição pública com seus sinais distintivos.
