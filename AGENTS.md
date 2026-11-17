# AGENTS.md — Configurador Comercial ATSI Brasil × YvyLab

> **Status:** protótipo HTML interativo, em evolução.  
> **Última contextualização:** 16 de novembro de 2026.  
> **Idioma de produto e comunicação:** português brasileiro (`pt-BR`).  
> **Público deste arquivo:** agentes de IA, designers, desenvolvedores, QA e pessoas que assumirem a continuidade do projeto.

## 1. Missão do projeto

A **YvyLab** está elaborando uma proposta comercial para a **ATSI Brasil** referente à construção de uma **plataforma digital de educação e relacionamento com clientes**, com experiência centrada no aplicativo e conteúdo relacionado ao negócio da ATSI.

Em vez de oferecer apenas um orçamento por horas de desenvolvimento, a YvyLab quer possibilitar que a ATSI **configure a solução escolhendo funcionalidades**. Cada funcionalidade tem:

- **Horas de esforço estimadas** (variável técnica e interna);
- **Preço comercial da feature em reais** (independente da simples multiplicação horas × taxa/hora);
- **Complexidade** (escala de 1 a 5);
- **Valor percebido para o cliente** (classificação comercial);
- **Tipo de contratação:** obrigatória, opcional ou escolha única.

A ferramenta deve servir a dois propósitos: **tomada de decisão sobre o escopo** e **simulação transparente do investimento**, permitindo comparar um produto essencial, intermediário e avançado.

### Princípio comercial inegociável

**Preço da feature não é sinônimo de custo calculado por hora.** O custo interno de referência pode ser estimado por `horas × custo_interno_por_hora`, mas o **preço comercial de venda** é um campo próprio. O agente não deve substituir automaticamente os preços comerciais por cálculos de horas, nem tratar as estimativas iniciais como uma proposta aprovada.

## 2. O que a ATSI quer construir

A plataforma é voltada principalmente para **clientes/alunos da ATSI Brasil**. O produto mínimo discutido inclui:

1. **Mural inicial obrigatório**, com destaque para cursos, e-books, eventos presenciais e eventuais promoções.
2. **Login obrigatório** por e-mail e senha, recuperação de acesso e gerenciamento de sessão.
3. **Perfil obrigatório** com foto, nome, e-mail, redefinição de senha, alteração de e-mail e preferência de recebimento de comunicações de marketing.
4. **Cursos obrigatórios**, contendo catálogo, detalhes, módulos/aulas e reprodução de conteúdos; a forma de disponibilizar os vídeos é uma **decisão técnica/comercial exclusiva**.
5. **Administração mínima de conteúdo** para a ATSI atualizar ofertas, cursos e destaques sem intervenção do desenvolvedor.

**Importante:** a exibição de um card de e-book, evento ou promoção no mural não equivale automaticamente a implementar uma biblioteca de e-books, sistema de inscrições de eventos, checkout ou mecanismo completo de promoções. Evitar dupla cobrança por uma mesma entrega.

### Funcionalidades opcionais já colocadas em discussão

- MFA (autenticação multifator);
- Login com Google;
- Login com Microsoft;
- Biblioteca de e-books e seus recursos associados;
- Notificações push, segmentação e automações;
- Grupos/comunidade, chat e encontros ao vivo;
- Progresso de cursos, certificados, quizzes e comentários em aulas;
- Vídeos privados em nuvem e acesso offline como alternativas de implementação da entrega de vídeos.

**Pontos ainda não fechados:** apps Android/iOS nativos ou cross-platform versus PWA/web; se os cursos serão gratuitos, pagos ou restritos; pagamentos; inscrições em eventos; certificados; propriedade intelectual dos vídeos; escala de alunos; regras de acesso; custos operacionais; e quais opcionais entram no contrato.

## 3. Objetivo da interface de configuração

O usuário solicitou um **HTML visual, interativo e independente** com estas características:

- **Tema escuro** com direção visual ligada ao **agronegócio** (tons de verde, terra, natureza; acabamento tecnológico e comercial).
- **Tela dividida visualmente em duas metades** em desktop.
- **Coluna esquerda:** três presets no topo; abaixo, seções de features destacadas por cor; cards de funcionalidades com seleção e campos de esforço/preço/complexidade.
- **Coluna direita:** um **mockup grande de smartphone**, que muda de tela quando a pessoa **clica em uma feature** para visualizá-la.
- **Abaixo do smartphone:** preço total atualizado automaticamente, horas, custo interno, composição e outras informações comerciais.
- **Responsive:** desktop em duas colunas; tablet e mobile com empilhamento apropriado.
- **Experiência em pt-BR:** moeda `R$` e separação decimal brasileira.
- **Presets no topo da esquerda:** `Essencial`, `Plus`, `Premium`; alterações manuais passam para um estado de configuração personalizada.

O preview do smartphone é **uma representação conceitual** de telas do aplicativo proposto. Não constitui protótipo funcional do aplicativo ATSI nem compromisso de implementação exata.

## 4. Estado real do artefato e arquivos existentes

Na versão que originou este documento há um único HTML autossuficiente, com CSS e JavaScript inline:

- `ATSI_Brasil_Configurador_Interativo_v2.html` — arquivo para distribuição;
- `configurador_atsi_yvylab.html` — cópia/variação de trabalho do mesmo protótipo.

**Ao copiar estes arquivos para um repositório, escolher um arquivo HTML canônico e evitar manter duas versões divergentes.** No momento, não há requisito de framework, servidor ou processo de build; abrir o HTML em um navegador é o uso principal.

### Implementado no HTML atual

- Layout escuro com cores agro;
- Divisão em colunas com features à esquerda e smartphone à direita;
- Presets **Essencial**, **Plus** e **Premium**;
- Seis categorias de funcionalidades;
- Features obrigatórias, opcionais e escolhas únicas;
- Campos editáveis de horas, preço e complexidade;
- Valor percebido exibido como classificação inicial;
- Cálculo em tempo real de total comercial, horas e custo interno;
- Preview visual de telas distintas, conforme a feature clicada;
- Comportamento responsivo básico.

### Lacunas conhecidas / atenção antes de produção

- **Não há persistência em `localStorage` ou banco** no protótipo atual: ao recarregar, volta ao estado padrão.
- **Não há exportação funcional de proposta/JSON/CSV/PDF** nesta versão escura. Não afirmar o contrário.
- **Não há backend, autenticação real, API de cursos ou player de vídeo real.** O smartphone é apenas mockup.
- **Não há validação abrangente de dependências** entre opcionais: por exemplo, certificados deveriam requerer progresso; push segmentado deveria requerer infraestrutura de push; chat/lives deveriam requerer grupos.
- **A seleção da estratégia de vídeo merece reforço:** deve haver exatamente uma alternativa válida, sem permitir deixar o módulo obrigatório de cursos sem método de entrega.
- **O clique que seleciona uma opção e o clique que apenas visualiza o mockup são conceitos distintos.** A implementação precisa deixar esse comportamento inequívoco e garantir atualização imediata do preview após seleção.
- **As alterações de horas e custo/hora devem atualizar também os indicadores nos cards**, além do resumo à direita.
- **Estimativas de despesas mensais externas, impostos, suporte e descontos** ainda não estão adequadamente modeladas nesta versão.
- **O valor percebido não é um input editável** no protótipo v2; é apenas exibido. Pode vir a se tornar editável, caso aprovado.
- **Os preços e as horas são números demonstrativos**, não estimativas contratuais ou preços aprovados pela YvyLab.

**Orientação:** melhorias futuras devem sanar as lacunas sem eliminar a experiência visual escura e a arquitetura de orçamento por features.

## 5. Organização funcional atual

| Seção | Conteúdo atual | Regra principal |
|---|---|---|
| Base obrigatória | Mural, login, perfil, preferência de marketing, catálogo de cursos, painel administrativo básico | Todas incluídas em qualquer configuração |
| Login e segurança | MFA, Google Login, Microsoft Login | Opcionais independentes |
| Cursos | YouTube embutido, vídeos privados, vídeos offline, progresso, certificados, quizzes, comentários | Uma estratégia de vídeo por vez; complementos opcionais |
| E-books | Destaque no mural e biblioteca | Opcionais, sem duplicar o mural obrigatório |
| Notificações | Push básico, push segmentado e automações | Opcionais com dependências a formalizar |
| Grupos | Comunidade básica, chat, lives | Opcionais com dependências a formalizar |

### Identificadores de features existentes no JavaScript

Preservar os IDs para manter a consistência de presets e eventuais persistências/exportações:

```text
obrigatorias:
  mural, login, perfil, marketing_optin, catalogo_cursos, admin_basico

autenticacao:
  mfa, login_google, login_microsoft

cursos:
  curso_youtube, curso_privado, curso_offline,
  progresso, certificados, quizzes, comentarios_aulas

ebooks:
  ebook_vitrine, biblioteca_ebooks

notificacoes:
  push_basico, push_segmentado, automacoes

grupos:
  grupos_basicos, chat_grupos, lives_grupos
```

As três opções `curso_youtube`, `curso_privado` e `curso_offline` pertencem ao grupo exclusivo `curso_entrega`.

## 6. Arquitetura de dados e cálculo

A implementação presente mantém um array JavaScript `features`, um objeto `presets` e um estado em memória com:

- `selected`: `Set` de IDs selecionados;
- `activePreset`: preset ativo ou `custom`;
- `activePreview`: tipo de tela exibida no smartphone;
- `openSections`: seções expandidas;
- `hourRate`: custo interno por hora.

**Regras fundamentais:**

1. Features `required` fazem parte do orçamento sempre e não podem ser desmarcadas.
2. Features `optional` podem ser ativadas/desativadas individualmente, salvo dependências explícitas.
3. Features `unique` pertencentes ao mesmo grupo são mutuamente exclusivas; o grupo obrigatório `curso_entrega` deve possuir **exatamente uma** opção selecionada em uma configuração comercial válida.
4. Um preset seleciona um conjunto predefinido de features; alterações manuais indicam configuração `custom`.
5. Clicar no **corpo do card** mostra o preview; interagir com checkbox/radio ou com campo de preço/horas não deve disparar seleções acidentais.
6. O mockup deve corresponder à feature clicada, independentemente de ela estar ou não contratada. A seleção do escopo é controlada separadamente.

### Fórmulas

```text
features_selecionadas = todas as obrigatórias + opcionais escolhidas + uma escolha por grupo obrigatório

horas_totais = soma(feature.hours das features selecionadas)

preco_bruto_implantacao = soma(feature.price das features selecionadas)

custo_interno_estimado = horas_totais × custo_interno_por_hora

margem_bruta_simplificada = preco_bruto_implantacao − custo_interno_estimado

margem_percentual_simplificada =
  preco_bruto_implantacao > 0
  ? margem_bruta_simplificada / preco_bruto_implantacao × 100
  : indefinida
```

**Não misturar** preço comercial de implantação com custo mensal de terceiros, suporte, tributos, royalties, taxas de gateway ou custos de distribuição de vídeos. Quando esses componentes forem implementados, devem aparecer **separados**.

**Observação sobre complexidade:** usar escala de 1–5 para comunicação/risco; o campo não recalcula automaticamente preço, horas nem margem, a menos que uma política de estimativa seja aprovada explicitamente.

### Premissas e preços

As horas e os valores preenchidos no HTML são **dados de demonstração**. É apropriado usá-los para testar a interface, mas **nunca apresentá-los como orçamento definitivo sem revisão comercial e técnica**.

## 7. Decisão crítica — entrega de vídeos dos cursos

A estratégia de vídeos altera muito o custo e deve ser tratada como uma **decisão de produto**, não como três extras cobrados simultaneamente.

| Alternativa | Exemplo | Perfil comercial | Cuidados |
|---|---|---|---|
| YouTube incorporado | `curso_youtube` | Menor custo inicial | Depende de internet; restrições da plataforma, publicidade/experiência e eventual incompatibilidade com modelo pago/privado devem ser avaliadas |
| Hospedagem privada / streaming | `curso_privado` | Mais controle | Armazenamento, distribuição/CDN, processamento e autorização podem gerar custos variáveis |
| Hospedagem privada + offline | `curso_offline` | Maior investimento e complexidade | Downloads locais, sincronização, expiração/renovação de licença, segurança e limitações de SO; pressupõe entrega privada, sem cobrança duplicada |

**Não supor que S3 sozinho resolve streaming, proteção e offline.** Uma implementação real pode envolver S3, CDN, empacotamento/streaming, URLs/cookies assinados, player apropriado e regras de acesso. A seleção arquitetural deve considerar volume de vídeo, alunos simultâneos, plataformas-alvo, proteção de conteúdo e custos recorrentes.

**Não prometer que embedding do YouTube fornece proteção efetiva de um curso pago nem download offline.** Validar termos e políticas do serviço antes de incluir essas características em contrato.

## 8. UX, design e responsividade

Direção visual desejada:

- Fundo geral escuro com referência discreta a natureza/campo/agro; evitar imagens decorativas que prejudiquem legibilidade.
- Verde como cor primária de destaque; cores complementares distintas para seções.
- Cards e painéis com cantos arredondados, hierarquia clara e contraste suficiente.
- Três presets acima das seções, com estado ativo evidente.
- Smartphone bem visível na metade direita em desktop, com telas específicas por feature.
- Total financeiro legível **abaixo do celular**, sem esconder os dados importantes em abas secundárias.
- Em telas pequenas, empilhar painéis e manter edição e visualização utilizáveis.
- Usar rótulos acessíveis, estados de foco, inputs utilizáveis por teclado e feedback visual.

O layout não deve depender de imagens externas para funcionar. Qualquer futura imagem remota deve ter fallback e não deve ser necessária aos cálculos ou às interações.

## 9. Como trabalhar no código sem regressões

### Antes de editar

1. Ler este `AGENTS.md` e inspecionar o HTML **real que está sendo modificado**.
2. Confirmar a lista atual de features, IDs, presets, totais e comportamentos; **não assumir** que versões anteriores e atuais têm as mesmas capacidades.
3. Separar claramente o que já está implementado do que é uma proposta futura.
4. Planejar qualquer alteração de modelo de preços e dependências antes de mexer na interface.
5. Preservar o pedido explícito do usuário: **HTML interativo, metade esquerda configurável e metade direita com smartphone, tema escuro e três presets**.

### Ao implementar

- Priorizar modificações pequenas, testáveis e reversíveis.
- Manter o **preço comercial editável por feature** separado do custo interno.
- Centralizar regras e dados de features para evitar divergência entre cards, mockups, presets, cálculos e exportações.
- Evitar IDs duplicados e estados impossíveis (como duas estratégias de vídeo ou nenhuma).
- Tratar dependências com clareza: impedir seleção inválida ou incluir requisitos explicitamente, nunca adicionar custos escondidos.
- Se implementar persistência, versionar o schema e proteger contra dados antigos/corrompidos; disponibilizar ação de restaurar padrões.
- Se implementar exportação, garantir que corresponda exatamente ao estado visível da configuração.
- Não introduzir backend, bibliotecas ou infraestrutura sem necessidade: um HTML independente é requisito útil nesta fase.
- Não misturar este projeto comercial ATSI Brasil com sistemas/repositórios não relacionados da YvyLab.

### Verificações mínimas antes de entregar

- O HTML abre diretamente no navegador, sem servidor.
- Sem erros de JavaScript no console.
- Os três presets produzem conjuntos diferentes, válidos, e totalizam corretamente.
- Obrigatórias não podem ser removidas.
- `curso_youtube`, `curso_privado` e `curso_offline` não podem coexistir, nem ficar todos vazios.
- Selecionar/desmarcar opcionais altera preço, horas, custo interno e contagem corretamente.
- Editar preço altera apenas o preço comercial pertinente e seus totais.
- Editar horas/custo-hora altera os cálculos internos adequados, preservando preço comercial.
- Clicar nas features troca o conteúdo e a legenda do smartphone.
- Selecionar feature também deve atualizar imediatamente o preview se essa for a interação esperada na versão implementada.
- Desktop mantém composição em duas metades; mobile mantém legibilidade e controles funcionais.
- Valores em moeda usam `pt-BR`.
- Exportação/persistência, se presentes, devem ser testadas para ida e volta sem perda de escolhas.

## 10. Melhorias prioritárias para próximos ciclos

### P0 — Consistência e confiabilidade

- Corrigir a atualização imediata do preview ao selecionar um rádio/checkbox.
- Garantir **uma, e somente uma**, estratégia obrigatória de vídeo.
- Atualizar custo/margem de cada card quando horas ou taxa/hora mudarem.
- Adicionar regras explícitas de dependências (certificados → progresso; segmentação → push; chat/lives → grupos), sem dupla cobrança.
- Revisar sobreposições de escopo: mural obrigatório vs. e-book em destaque opcional.

### P1 — Continuidade da configuração

- Salvar/reabrir configuração localmente, com versão de dados e botão de restaurar.
- Exportar/importar JSON de configuração.
- Exportar CSV e proposta comercial legível/imprimível em PDF.
- Adicionar observações, premissas, exclusões e identificação da versão do orçamento.

### P2 — Precificação profissional

- Separar implantação, suporte mensal e serviços externos recorrentes.
- Editar custo-hora, descontos, contingência e indicadores de margem.
- Criar comparação lado a lado dos três presets e de um cenário personalizado.
- Manter preços-base revisados e auditáveis, evitando aumentos automáticos sem critério.

### P3 — UX premium

- Melhorar fidelidade visual do smartphone por feature, com transições suaves.
- Tornar a navegação por seções e funcionalidades mais clara.
- Evoluir o painel para experiência de apresentação comercial à ATSI.

**As prioridades acima são recomendações de execução, não escopos automaticamente autorizados.**

## 11. Decisões que precisam de validação com a ATSI / YvyLab

Antes de converter este simulador em proposta contratual, confirmar:

1. **Plataformas:** Android, iOS, web/PWA, ou combinação.
2. **Acesso aos cursos:** gratuitos, por assinatura, compra avulsa, por convite ou vínculo com cliente.
3. **Estratégia de vídeo:** YouTube, streaming privado ou offline; volumes esperados e requisitos de proteção.
4. **Painel administrativo:** quem gerencia conteúdo, usuários, eventos, campanhas e mídia.
5. **E-books:** link externo, biblioteca própria, leitor interno e/ou download.
6. **Eventos:** somente destaque ou fluxo completo de inscrição, lista de presença e check-in.
7. **Notificações:** somente push, e-mail, SMS/WhatsApp ou combinações; consentimentos.
8. **Grupos:** regras de moderação, privacidade, mensagens, permissões e retenção.
9. **Escala e operação:** usuários esperados, vídeos, custos de hospedagem, manutenção e suporte.
10. **Políticas e compliance:** LGPD, consentimento de marketing, segurança de contas, termos de uso e regras das plataformas de vídeo/lojas.
11. **Preços:** confirmar que horas, margem e preços comerciais foram revisados pela YvyLab.

Até essa validação, apresentar números como **simulação preliminar, não oferta firme**.

## 12. Critério de sucesso

O configurador é bem-sucedido quando a YvyLab consegue, durante uma conversa com a ATSI:

1. Mostrar **Essencial / Plus / Premium** imediatamente;
2. Abrir seções por tema e explicar cada feature sem jargão excessivo;
3. Clicar em uma feature e visualizar uma tela representativa no celular;
4. Ativar/desativar opcionais ou trocar a escolha técnica de vídeo;
5. Ajustar horas, complexidade e preço comercial com rastreabilidade;
6. Ver o **investimento total** reagir imediatamente abaixo do mockup;
7. Sair da reunião com um escopo consistente, decisões pendentes explícitas e um orçamento exportável — quando a etapa de exportação estiver implementada.

---

**Regra final para agentes:** preservar a visão do projeto, não inventar funcionalidades como já prontas, não criar números comerciais como se fossem aprovados, e priorizar uma experiência simples, visual e confiável de negociação por funcionalidades.

## Atualização de estado — revisão técnica de 16/11/2026

O artefato canônico é `home.html`. Ele usa o catálogo de 54 features e inclui
fundação obrigatória uma vez. O histórico acima descreve versões anteriores.
As horas vigentes vêm das tarefas revisadas em `specs/`, incorporadas pelo comando
`python3 specs/gerar_catalogo.py`. Não retornar às horas históricas em `docs/`.

A revisão preliminar atual soma 522 h de fundação (F01: 104 h; F02: 120 h;
F05: 56 h; F06: 90 h após detalhar ambientes e pipelines genéricos)
e 340 h de base obrigatória. C03 contém o esforço online de C02 sem somá-lo de novo.
G02 permanece sob cotação e indisponível para contratação.
R$ 200/h é referência comercial fixa, não custo interno real nem preço aprovado.
Critérios e justificativas estão em `specs/REVISAO-TECNICA.md`.

Teste reproduzível: `python3 -m unittest discover -s tests -v`.
Ele verifica somas das specs e, quando Chrome está disponível, catálogo, totais,
dependências, exclusividade do vídeo, bloqueio G02 e renderização dos mockups.
Não equivale à validação funcional do futuro aplicativo nem à aprovação comercial.

Fornecedores são definidos em F02, não presumidos a partir das referências de
preço. F05 prepara os ambientes aprovados; F06 configura versionamento e pipelines.
O módulo mensal do configurador possui spec separada, ainda sem implementação
ou estimativa, em `specs/configurador-custos-operacionais.md`.

Promoções locais: `pricing-promotion.js` concentra os cálculos em centavos;
`ofertas-admin.html` emite JSON de oferta com aprovação explícita e sem percentuais
padrão. Não há autenticação real. `home.html` importa/persiste a oferta, mostra
contador de 24 h e comparação e exporta JSON/CSV/impressão.
Nunca descontar fundação, obrigatórias, mensalidades ou personalizado. A política
atual também exclui vídeo. Não apresentar o relógio local como autoridade comercial.
Consultar `docs/ofertas-24h.md`. Teste adicional: `node tests/test_promotion.js`.

Identidade de produto: ATSI+, com configuração em `branding/product-config.js`
e guia `branding/atsi-plus.md`. ATSI Brasil permanece cliente/instituição e YvyLab
desenvolvedora. Rebranding não altera IDs, snapshots financeiros ou regras de
promoção. Assets ATSI+ são propostas, não logos homologados ou marcas registradas.

Atualização posterior: painel de ofertas simplificado por solicitação do usuário.
Popup azul com início/fim em Brasília, descontos nos três planos e Salvar;
sem importação/exportação na interface. Campanha v2 usa datas explícitas e
desconto sobre o total de implantação do preset (inclusive Essencial).
Mensalidades, horas e Personalizado ficam sem desconto. Isso substitui a política
anterior de opcionais elegíveis v1 no fluxo atual. Persistência em
`atsi-campaign-v2` é somente local; não grava no repositório nem publica para todos.

## Atualização de escopo — 17/11/2026

O usuário confirmou que o Essencial já inclui aplicativos Android e iOS e
versão web para alunos, além do painel administrativo web. Isso vale também
para Plus, Premium e configurações personalizadas. A plataforma de acesso não
é um opcional de plano. A antiga pendência sobre inclusão de plataformas está
substituída por essa decisão; a tecnologia continua sujeita à arquitetura.
Consultar `specs/plataformas-entrega.md`.

Horas, valores e prazos não foram alterados nesta atualização. O impacto da web
dos alunos ainda requer decomposição e revisão técnica/comercial; não afirmar
que as estimativas anteriores já cobrem esse esforço. O configurador sinaliza
essa pendência nos planos, resumo e dados de proposta.

Apresentação comercial — decisão posterior do usuário em 17/11/2026: os preços
exibidos são definidos pelo vendedor. Não mostrar "Preço de venda: Não aprovado"
nem avisos equivalentes de preço/proposta sem aprovação nos cards, resumo ou
popups. Usar "Preço de implantação" / "Investimento de implantação", preservando
os valores e os cálculos existentes. Isso não aprova automaticamente entregáveis
técnicos nem remove as ressalvas de prazo, detalhamento da web ou mockups.

Complexidade dos presets: classificação relativa Essencial Baixa, Plus Média
e Premium Alta. Não confundir com notas técnicas das features (preservadas).
Personalizado continua exibindo a média técnica com rótulo e explicação próprios.
Consultar `docs/complexidade-planos.md`.

G02 ampliada pelo usuário em 17/11/2026: configuração administrativa para
encaminhar mensagens/conteúdo a múltiplos grupos e canais de diferentes redes
sociais no mesmo agendamento, não somente WhatsApp. Preservar ID G02. Por nova
solicitação do vendedor, usa estimativa conservadora de 250 h / R$ 50.000 para até
três conectores oficiais viáveis e é selecionável na simulação, fora dos presets.
Isso substitui o estado anterior sob cotação/bloqueado, sem atestar viabilidade.
Validar APIs oficiais, permissões e elegibilidade por rede/destino antes de
executar conectores. Não prometer suporte universal ou entrega no mesmo
instante. Spec: `specs/G02-encaminhamento-multicanal-redes-sociais.md`.
G01 continua sendo diretório de links do WhatsApp, sem disparos.

Campanha v2 agora tem um sexto input: "Desconto por feature opcional adicional".
`additionalOptionalPercentage` é opcional no schema v2 (ausente = zero), salvo
somente no navegador. `basePreset` preserva o plano de origem; acrescentar extras
mantém o desconto do pacote completo e aplica o percentual adicional apenas aos
opcionais que não estejam em NENHUM dos planos Essencial/Plus/Premium, sem
duplicidade. Um recurso incluído em qualquer plano não recebe desconto adicional
quando comprado separadamente em outro plano. Usar a união dos IDs dos três
presets como exclusão, não somente os itens do plano de origem. Remover itens do pacote ou trocar vídeo
suspende ambos; restaurar a composição recupera as condições na mesma vigência.
Fundação, obrigatórias, vídeo e mensalidade não recebem o percentual adicional.
Horas não mudam. O estado personalizado sem um pacote completo não é elegível.
`pricing-promotion.js` centraliza arredondamento por feature em centavos.
Consultar `docs/ofertas-24h.md` e executar testes Python e Node.

Copy comercial: `product-copy.js` concentra títulos, descrições, benefícios e
escopo comercial das 54 funcionalidades, seções e preparação. A interface
prioriza valor para cliente/aluno e não mostra tarefas técnicas, pendências de
auditoria ou caminhos do repositório. Especificações internas continuam intactas.
Limites importantes permanecem em linguagem de composição da entrega; não
inventar capacidades nem apresentar mockups como produto já implementado.
Snapshots financeiros mantêm os títulos originais das specs, separados dos títulos
comerciais, para não invalidar ofertas por edição de copy. Ver `docs/copy-produto.md`.

Benefício comum: curso de capacitação para administradores, cortesia em todos
os planos e nas configurações personalizadas. `includedBenefits` mantém o item
`admin_training` separado das 54 features e dos snapshots financeiros, com
preço adicional zero e sem inventar carga horária. Mostrar no card e no resumo;
dados de proposta também incluem o benefício. Conteúdo acompanha os recursos
contratados; não prometer formato, duração ou treinamentos ilimitados.
Ver `specs/capacitacao-administradores.md`.

Configurações de oferta agora têm liberação por hash e importação/exportação
de JSON por solicitação do usuário. `campaign-settings.js` valida o hash fixo,
formato, versão e campos. Arquivo exportado inclui o hash; importação preenche
e libera a edição, mas só Salvar aplica e persiste a campanha. Não gravar o hash
no localStorage ou proposta. Edição/download bloqueados inicialmente; fechar ou
alterar o hash bloqueia novamente. Isso é barreira local, não autenticação real.
Não publica no repositório nem sincroniza visitantes. Limite de arquivo 64 KB.
Teste adicional: `node tests/test_campaign_settings.js`.

O atalho de preço alterna para "Voltar ao início" ao se aproximar do investimento,
mantém essa ação até chegar ao topo e então volta a "Ver preço". Preservar
animação interrompível, preferência por movimento reduzido e layout sticky.

Catálogo atual: 55 features e sete atividades de fundação. A04 — Entrar com
Facebook é opcional independente, com estimativa inicial de 32 h / R$ 6.400
para Android/iOS/web. Não está nos presets e não mostra tag de plano; segue as
regras de desconto de opcionais fora de todos os planos. IDs anteriores, preços
e horas dos presets não mudam. O mockup não executa autenticação. A integração
real dependerá das credenciais, permissões e políticas oficiais da Meta.

PDF: botão "Gerar PDF Oferta" ao final da página. `offer-pdf.js` gera o documento
com jsPDF local em `vendor/jspdf/`, usando o estado escolhido e preços congelados
no instante da geração. Os nomes técnicos vêm de `technicalTitle` e as tarefas
tipadas de `taskDetails`, gerados a partir das specs. Incluir preparação uma vez,
cortesia e manutenção separada. Rateio proporcional do desconto de pacote com
centavos compensados; desconto adicional separado, sem duplicidade. Somar cada
entrega deve fechar com o total. Nunca incluir hash ou senha no PDF.
Ver `docs/oferta-pdf.md`; teste adicional `node tests/test_offer_pdf.js`.

Dependências agora são incluídas automaticamente, com popup explicativo e OK.
M01 exige E01 por decisão explícita do usuário, substituindo a política anterior
de vitrine independente para esse recurso. Requisito em uso fica bloqueado para
remoção; `autoSelected` permite retirar somente inclusões automáticas sem uso,
preservando escolhas manuais e itens do preset. Requisitos já presentes não
geram custos duplicados nem novo popup. Ver `docs/dependencias.md`.

Adicional operacional — decisão posterior de 17/11/2026: operação passa a ser
somada à base de manutenção (R$ 3/4/5 mil; 10/15/20 h preservadas), substituindo
a política anterior de operação incluída. `operational-pricing.js` centraliza
o modelo versionado, com slider de 100–10.000 usuários ativos/mês. Câmbio e
consumo são hipóteses explícitas/editáveis; pico simultâneo não é benchmark nem
capacidade garantida. Fornecedores são referências, não decisões de F02.
Não duplicar infraestrutura, vídeo/acervo ou tráfego já incluído no Stream.
Base e adicional nunca recebem descontos de implantação. IA, tributos,
serviços/consumos fora do cenário e excedentes seguem separados e exigem acordo.
`monthlyMaintenanceBRL` continua sendo só base; `monthlyOperationalBRL`,
`monthlyTotalBRL` e `operations` compõem exports e PDF. Não há persistência local
de premissas operacionais. Ver `docs/custos-operacionais.md` e
`docs/condicoes-manutencao.md`. Teste adicional:
`node tests/test_operational_pricing.js`, além dos testes anteriores.

Regra comercial posterior: com YouTube (C01), **todo o adicional operacional
é zerado**, mantendo a manutenção base de origem. Não apenas a parcela de vídeo.
`atsi-operations-v2` separa custo de referência (`estimatedCents`,
`totalEstimatedCents`) do adicional cobrado (`priceCents`, `totalCents`).
Infraestrutura compartilhada do cenário fica coberta pela base com YouTube;
não afirmar que os serviços deixam de ter custo. Streaming privado/offline
mantém os adicionais anteriores. A explicação logo abaixo da mensalidade,
PDF e exports destaca o impacto de transmissão, armazenamento e downloads
no crescimento do adicional. Preservar coerência entre esses canais.

White label: `company` na URL seleciona identidade via `branding/product-config.js`.
Assets e cores ficam em `assets/companies/<slug>/`; camada compartilhada em
`branding/company-theme.css`. `company` válido é obrigatório: ausente, vazio ou
desconhecido redireciona para `404.html`, sem fallback visual para a ATSI. Trata-se
de página de erro no navegador, não de status HTTP 404 sem regra no hosting.
`jan` tem identidade
textual/paleta provisórias, não homologadas. Catálogo, IDs, valores, horas,
presets e cálculos são únicos para todas as empresas. Não duplicar ofertas por
branding. Campanhas locais de outras empresas usam sufixo `:company:<slug>`,
preservando a chave histórica da ATSI. A entrada mantém o parâmetro ao navegar;
PDF e dados de proposta identificam a empresa. Não há envio de e-mail nem
autenticação/multitenancy real nesta entrega. Ver `docs/white-label.md` e
`tests/test_white_label.py`.

Defaults white label: imagem de fundo `branding/assets/parallax.jpg`, fonte
Montserrat, textos e comportamento são compartilhados. `branding/company-theme.css`
define tokens padrão com baixa especificidade; `theme.css` de cada empresa
sobrescreve apenas o necessário. Tipografia é configurável por
`--brand-font-family`, com controles herdando a fonte. Imagens próprias são
opcionais: declarar `background-image` diretamente no CSS da empresa, não URL
relativa em variável consumida por outro stylesheet. Não remover o fundo padrão
de uma empresa só por alterar sua paleta. Testar herança parcial e carregamento
real da imagem nas páginas de entrada, configurador e emissor interno.

Logos white label têm papéis separados: `logoInstitutional` (opcional, caminho
relativo à raiz) identifica a instituição no cabeçalho de `home.html`, com
`data-company-logo="institutional"`. ATSI reutiliza o SVG original
`branding/assets/atsi-logo-cabecalho.svg`, sem edição. `logoDark` continua sendo
ATSI+ na entrada e nos mockups. Sem logo institucional própria, usar a logo da
plataforma da empresa selecionada, sem vazar a marca ATSI para outras empresas.
