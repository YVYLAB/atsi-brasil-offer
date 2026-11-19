# PROMPT ÚNICO PARA OPENCODE — ATSI BRASIL × YVYLAB

**Missão:** atualizar o configurador comercial interativo existente, e não construir a plataforma real. Implementar a matriz atualizada de 55 features + 7 atividades compartilhadas, comparação dos custos da infraestrutura e das escolhas de vídeo (YouTube/Cloudflare Stream/offline/Google Drive experimental), com precificação coerente, descrições claras, testes e documentação. Não entregar apenas um plano: executar as alterações possíveis no repositório atual, testar e relatar o resultado.

**Data-base dos preços e premissas:** 16/11/2026. **Moeda da implantação:** BRL. **Referência:** R$ 200/h (tarifa comercial da YvyLab). **Fornecedores:** USD, sem conversão automática fictícia. Valores de desenvolvimento são estimativas preliminares, não proposta assinada.

## 0. Instruções de trabalho (não negociar a qualidade)

1. Antes de editar, leia o `AGENTS.md` do repositório e identifique o HTML/aplicação atual do configurador. Verifique stack, estrutura, estado do git, modificações não commitadas e implementações já existentes. Não suponha que a versão local ainda seja a v2 desta conversa: **preserve trabalho posterior do OpenCode**. Se a documentação anterior estiver desatualizada, atualize-a de forma compatível.
2. Não altere outro projeto, não sobrescreva alterações do usuário, não execute comandos destrutivos no git, não crie commits/push/PR sem solicitação. Preserve os IDs existentes e mapeie IDs legados quando houver; evite migrações destrutivas do localStorage.
3. Faça preflight breve, estabeleça plano de alterações, e **implemente nesta execução**. Se faltar credencial/conta externa, não bloqueie o simulador: use dados locais transparentes e marque integrações como propostas, sem simular consumo real nem inventar contratação.
4. Trabalhe como sênior de produto, engenharia e pré-vendas: componentização, modelos tipados quando a stack permitir, fórmulas puras, acessibilidade, estados vazios, limites, testes automatizados, responsividade, tratamento de falhas e proteção contra dupla cobrança.
5. O configurador é um **orçamentador/visualizador**, não o aplicativo ATSI real. Mockups do celular são ilustrativos. Não implementar autenticação real de alunos, pagamentos, Cloudflare Stream real, anúncios ou armazenamento real neste trabalho sem escopo explícito.
6. Toda informação de fornecedor deve ter unidade, data-base, fonte oficial, limitações, hipóteses e status (confirmado como preço público, estimativa de uso, pendente de cotação). Atualize preços se houver mudança oficial documentada, registre a diferença e **não troque silenciosamente** as premissas deste prompt.

## 1. Produto e UI que não podem regredir

YvyLab apresentará à **ATSI Brasil** uma proposta modular de plataforma de cursos voltada a clientes finais, com mural, identidade agro e muitos complementos opcionais. O objetivo é vender o valor de cada entrega — não apenas horas, embora R$ 200/h componha a referência.

- Visual **escuro premium inspirado no agronegócio**: verdes de campo, textura/ilustração agrícola discreta, contraste alto, títulos e agrupamentos destacados por cor. Não usar fundos que prejudiquem legibilidade.
- Em desktop, dividir a tela em duas metades de aproximadamente 50/50: **esquerda** com três presets no topo e sections de features coloridas e expansíveis; **direita** com mockup de smartphone que altera sua tela ao selecionar/clicar em qualquer feature e **abaixo do celular** o investimento total atual, horas, preço, custos mensais e ressalvas. Painel direito sticky quando houver espaço; em telas pequenas, empilhar sem impedir edição.
- Presets **Essencial, Plus, Premium**, de fato configurados e válidos. Após alterar um preset manualmente, apresentar **Personalizado**, preservando as escolhas. Não inventar um quarto preset de Drive como apto à venda.
- Sections com obrigatórias, opcionais, e escolhas exclusivas. Clique no corpo de um card **mostra preview**; checkbox/radio **altera contratação**. Uma ação não deve disparar acidentalmente a outra.
- Cada card mostra: ID, título, descrição do que entrega, classificação e dependências, horas mínima/provável/conservadora, complexidade 1–5, valor percebido, tarifa comercial de referência, **referência de implantação** (h × R$200), **preço de venda editável** (independente da referência), fornecedor(es), modelo de custo operacional, riscos/limites e link da fonte. Caso sem estimativa: **Sob cotação** — nunca 0 fictício.
- Painel direito apresenta valores: **fundação única** + **features obrigatórias** + **opcionais** + **uma estratégia de vídeo**, e em bloco separado operação externa/mês, suporte YvyLab/mês (editável se disponível), custos incertos e totais por provedor. Não chamar R$200/h de custo interno. Caso se queira margem, criar campo separado **custo real interno/hora**; se não preenchido, ocultar margem ou exibir 'indisponível'.
- Preservar funcionamento offline do **configurador HTML** (arquivo local) quando esta for a arquitetura existente. Não importar dependências de CDN externas de forma que o configurador pare de abrir localmente, salvo necessidade comprovada e alternativa local de fallback.
- Conservar ou implementar persistência robusta `localStorage` (ou o mecanismo já adotado), restaurar dados sem perder valores editados, versão e migração, exportar/importar JSON, exportar CSV e proposta imprimível/PDF do navegador quando viável na stack atual. Não declarar entregue funcionalidade não implementada.

## 2. Escopo e decisões comerciais fechadas

- A fundação compartilhada é obrigatória **uma vez**. Oito features `B01..B08` são obrigatórias. **B01 exibe somente cursos em destaque**; e-book/evento/promoção no mural são opcionais independentes (`M01..M03`).
- Login + recuperação, integração de e-mail transacional, perfil privado, registro de preferência de marketing, catálogo + módulos + aulas, progresso e painel administrativo são obrigatórios.
- `A01..A04` (MFA, Google, Microsoft e Facebook) são opcionais independentes.
- Curso requer **exatamente uma** opção apta à implantação: `C01` YouTube incorporado **OU** `C02` Cloudflare Stream privado **OU** `C03` privado com download offline. `C03` **já inclui `C02`**, portanto não somar seus preços ou horas.
- Progresso `B07` é obrigatório; certificados, quizzes, geração de testes por IA, chat de IA sobre vídeo, comentários e avaliação de satisfação são opcionais separados. 'Avaliação de aprendizagem' (`C05`) não é 'avaliação do curso' (`C09`). Chat IA demanda base textual autorizada/transcrição/indexação, limites de uso e análise de privacidade, não depende necessariamente de quizzes.
- Grupos são multisseleção: diretório de WhatsApp, automação WhatsApp **sob validação**, grupos internos/notícias, chat entre usuários, perfis públicos opt-in, busca global por perfis públicos.
- Gestão de eventos opcional com cadastro/vagas/inscrições, QR individual, convite por e-mail, leitor QR + check-in. Cobrança de evento é outro opcional.
- Pagamentos e entitlements opcionais: gateway, assinatura, venda de curso, ingressos, acesso a curso/evento/e-book por perfil/compra/assinatura. Aplicar regras das lojas para **conteúdos digitais comprados dentro de apps**; não assumir gateway web serve irrestritamente em iOS/Android.
- Auditoria administrativa: log de quem fez o quê, quando e qual registro, com retenção e controle de acesso. Relatórios independentes: visualizações, conclusão, satisfação, ativos, simultâneos. Gamificação independente: motor de pontos, presença em eventos, ranking público e pontos no perfil.

## 3. Stack de referência para as estimativas (não pressupor que o app real já exista)

- App: React Native + Expo + TypeScript (Android/iOS); painel administrativo: Next.js.
- Banco relacional: PostgreSQL via Supabase e Supabase Auth/RLS. Não migrar para MongoDB/Cassandra: cursos, matrículas, assinaturas, eventos e entitlements são relacionais; `JSONB` cobre dados flexíveis.
- Arquivos estáticos (capa, PDF, e-book, foto): Cloudflare R2 Standard; verificar se usar apenas Supabase Storage para volumes pequenos simplifica sem piorar o custo. **Não obrigar dois object stores sem motivo** e não cobrar ambos pelos mesmos arquivos.
- Conteúdo de vídeo privado: Cloudflare Stream para armazenamento, processamento e entrega. **Não cobrar armazenamento duplicado do mesmo vídeo no R2**.
- E-mail transacional: Resend (ou equivalente, com fonte). Push: Expo/FCM/APNs. Serviços de IA e pagamento com preço variável/sob cotação.
- Infraestrutura mobile, hospedagem do painel, DNS/domínio, monitoramento e lojas devem ser explicitamente incluídos nas premissas/pendências, não presumidos gratuitos.

## 4. Comparação obrigatória de entrega de vídeo

Criar uma seção/aba **'Comparar vídeo e custos'** com quatro opções visuais e comparação lado a lado; três contratáveis e a quarta como experimental:

1. **C01 — YouTube embedado — 20 h, R$ 4.000 de referência.** Sem tarifa direta à ATSI para hospedagem/distribuição via player padrão; depende de internet, controle de acesso limitado, possível exposição/compartilhamento de URL, integração e experiência dependentes das políticas. **Não vender como streaming privado nem garantir cursos pagos com acesso bloqueado.** As políticas da API YouTube vedam cobrar pelo ato de assistir no player incorporado, downloads/offline fora dos mecanismos autorizados e incentivação/recompensa por visualizações. Verificar caso de uso antes de habilitar pagamento de acesso ao vídeo ou gamificação baseada em assistir vídeos. Não ocultar marca/anúncios nem contornar player.
2. **C02 — Cloudflare Stream privado — 68 h, R$ 13.600 de referência.** Upload/ingestão, player, autorização compatível, URLs/tokens assinados conforme arquitetura, tratamento de erros e testes. Custo operacional específico: armazenamento e minutos entregues, distinto do custo compartilhado do backend. Não prometer DRM forte.
3. **C03 — Cloudflare Stream + offline — 166 h, R$ 33.200 de referência.** Substitui C02; inclui sua capacidade online mais downloads autorizados no app, retomada, armazenamento local, revogação/expiração quando possível, sincronização, falhas e QA Android/iOS. Downloads MP4 entregues são contabilizados pelo Stream. Offline não significa proteção anticópia inviolável nem DRM comercial avançado.
4. **DRIVE-PILOT — Google Drive preview/link — alternativa experimental, FORA das 55 features canônicas.** É tecnicamente possível usar links de visualização conforme permissões, mas Drive não é CDN nem provedor de vídeo privado para muitos assinantes. Sujeito a cotas, permissões, bloqueios, disponibilidade e possível mudança contratual. **Não atribuir preço de produção 'R$ 0' nem mensalidade 'US$ 0 garantido'.** Mostrar preço de implantação e operação como **'a validar / sob cotação'**, permitir explorar mockup e advertências, mas **bloquear exportação como proposta comercial fechada** até validação técnica/documental. Não recorrer a scraping, extração de URL temporária, bypass de quotas ou mecanismos não oficiais. Se orçamento comercial usar YouTube ou Cloudflare, o Drive pode continuar no comparador, mas fora da seleção válida de produção.

A comparação deve ter colunas: descrição, quando faz sentido, quando não faz, dificuldade, horas, implantação de referência, custo mensal por cenário, privacidade/controle, offline, dependências, limitações/políticas e fonte.

## 5. Taxas externas de referência (16/11/2026; validar fonte oficial antes de atualizar)

**Não aplicar custos mensais fixos a cada feature individualmente!** Os planos/cotas são compartilhados por fornecedor, enquanto a feature deve indicar o consumo incremental esperado ou 'coberto por plano até limite'.

| Provedor | Parâmetro inicial auditado | Atenção |
|---|---|---|
| YouTube embed | Sem tarifa direta de hospedagem/streaming cobrada à ATSI pelo embed comum | Políticas impedem certos modelos de cobrança, bloqueio e offline; sem SLA de conteúdo privado |
| Cloudflare Stream armazenagem | **US$ 5 / 1.000 minutos de capacidade armazenada por mês**, blocos pré-pagos | Ingestão/encoding incluídos, outros serviços não; capacidade por blocos |
| Cloudflare Stream entrega | **US$ 1 / 1.000 minutos entregues** | Inclui pré-carregamento, segmentos e downloads MP4; não contar reprodução local sem novo download |
| Cloudflare R2 Standard | **US$ 0,015/GB-mês** acima de 10 GB-mês gratuitos | Classe A: US$4,50/milhão acima de 1 milhão/mês; classe B: US$0,36/milhão acima de 10 milhões/mês; sem tarifa de egress; cobrança considera arredondamento das unidades |
| Supabase Pro | **A partir de US$ 25/mês** | Compute, MAU, egress, armazenamento, Realtime e ambientes extras podem gerar excedentes |
| Resend transacional | **Free US$ 0 até 3.000 e-mails/mês**, com limite de 100/dia; **Pro US$ 20/mês/50.000** | Marketing em massa não está incluído só porque a flag de consentimento existe; observar excedentes |
| Expo EAS | Free / Starter US$19/mês / Production US$199/mês (referência do documento v5) | Conferir condições atuais; usar 'não contratado' por padrão; publicação/contas Apple/Google separadas |
| Google Drive | Custo condicionado ao plano de armazenamento/Workspace e cotas/API | Não assumir gratuito para operação em massa; quotas/mudanças podem ocorrer |
| IA, WhatsApp, gateway e lojas | Sem valor fixo sem provedor, modelo de negócio, volume e elegibilidade | Exibir 'variável / sob cotação' com unidade possível e premissas requeridas |

**Fontes oficiais a linkar no app e no documento de premissas:**
- Stream: https://developers.cloudflare.com/stream/pricing/
- Stream downloads: https://developers.cloudflare.com/stream/viewing-videos/download-videos/
- R2: https://developers.cloudflare.com/r2/pricing/
- Supabase: https://supabase.com/pricing
- Resend: https://resend.com/pricing
- Expo: https://expo.dev/pricing
- YouTube: https://developers.google.com/youtube/terms/developer-policies
- Drive/API: https://developers.google.com/workspace/drive/api/guides/limits
- Drive/quota errors: https://developers.google.com/workspace/drive/api/guides/handle-errors
- App Store: https://developer.apple.com/app-store/review/guidelines/
- Google Play Billing: https://support.google.com/googleplay/android-developer/answer/10281818

**Importante:** não afirmar que os preços externos são cotação contratual da ATSI. Cada fonte no simulador deve ter link clicável e data-base; qualquer política que dependa de interpretação/país ou tipo de compra deve ser 'necessita verificação jurídica/comercial'.

## 6. Modelo de custos operacional editável

Implementar formulário em uma seção de **premissas operacionais** com:

- `activeStudentsMonth` (alunos que assistem vídeos por mês), `watchHoursPerStudentMonth`, `libraryHours`, `offlineDownloadsPerStudentMonth` (métrica separada de reprodução), `avgDownloadedHours` ou minutos equivalentes, `storedFilesGBMonth`, `r2OperationsClassA`, `r2OperationsClassB`, `emailsPerMonth`, `monthlyActiveUsers`, `supportMonthlyBRL` (opcional), `exchangeRateBRLperUSD` opcional editável com origem/data manual, `planSupabase`, `planResend`, `planExpo` e indicadores para serviços não cotados.
- `youtubeVideoCostUSD=0` apenas **para tarifa direta de vídeo do player padrão**; outras despesas da plataforma continuam existindo. O YouTube não dá controle privado equivalente ao Stream.
- **Stream armazenagem USD** `ceil(libraryHours * 60 / 1000) * 5` para `libraryHours>0`, senão `0`.
- **Stream minutos entregues** = `activeStudentsMonth * watchHoursPerStudentMonth * 60` + **minutos adicionais efetivamente entregues** em downloads que não estejam já incluídos no campo de consumo; dar nome/ajuda no formulário para evitar contagem dupla. `deliveredUSD = deliveredMinutes / 1000` com precisão monetária adequada. Preload e tráfego real podem elevar consumo além do modelo simplificado.
- **R2 Standard**: armazenamento e operações **líquidos das franquias**, aplicar arredondamento de unidades cobradas conforme documentação; exibir componentes separados e indicar uso médio em GB-mês. Não somar espaço de vídeo Stream ao R2.
- **Supabase/Resend/Expo**: uma única assinatura/plano por cenário; cotas e excedentes com valor conhecido ou sinalização de 'excedente não estimado'; nunca aplicar os planos por feature.
- **Custos de IA, gateways, lojas, WhatsApp, hospedagem Next.js, domínios e logs premium** devem ser mostrados como pendentes quando não houver dados; não mascarar 'desconhecido' como 'zero'. Exibir `total mensal conhecido (USD) + pendências não cotadas`, e não um falso 'custo total garantido'.
- Operação USD e preço de implantação BRL: mostrar separadamente. Conversão para reais só se câmbio fornecido, com data, e ainda assim manter USD e aviso sobre flutuação e tributos.
- Três cenários prontos e **editáveis**, com premissas transparentes (não confundir com os presets funcionais):
  - Piloto: 100 alunos ativos, 2h assistidas/aluno/mês, 30h acervo => **Stream US$22/mês** (US$10 armazenagem + US$12 entrega), antes de custos compartilhados.
  - Operação: 1.000 alunos, 3h/aluno/mês, 100h acervo => **Stream US$210/mês** (US$30 + US$180).
  - Expansão: 5.000 alunos, 4h/aluno/mês, 300h acervo => **Stream US$1.290/mês** (US$90 + US$1.200).
  - YouTube: custo direto de vídeo por embed padrão US$0 nos três cenários; despesas compartilhadas continuam e política de acesso pode tornar a opção incompatível.
  - Drive: **sem cálculo de produção validado**, com risco explícito. Simular visualmente sem oferecer falso número.
- Exibir diferença mensal `Stream - YouTube` e diferença de implantação conforme seleção, além de um gráfico simples de composição (sem exigir biblioteca externa se arquivo standalone).

## 7. Precificação da implantação e fundação

**Tarifa comercial:** R$ 200/h, editável como cenário de referência com valor inicial 200. *Não confundir com custo real interno.*

Fundação técnica **F01–F07 = 236 h = R$47.200** de referência, **uma única vez**, com detalhamento:
- `F01` — Descoberta, jornadas, UX, critérios de aceite: **32 h / R$ 6,400.00** de referência.
- `F02` — Arquitetura de domínio, dados, segurança e autorização: **32 h / R$ 6,400.00** de referência.
- `F03` — Shell mobile Expo/React Native, navegação e design system: **44 h / R$ 8,800.00** de referência.
- `F04` — Fundação do painel web Next.js e RBAC: **20 h / R$ 4,000.00** de referência.
- `F05` — Banco/API, storage, ambientes e segurança inicial: **28 h / R$ 5,600.00** de referência.
- `F06` — Build, CI/CD, preparação e publicação mobile: **40 h / R$ 8,000.00** de referência.
- `F07` — Homologação integrada, segurança e políticas essenciais: **40 h / R$ 8,000.00** de referência.

Base obrigatória **B01–B08 = 266 h = R$53.200**, adicionada à fundação. Estratégias exclusivas de vídeo:

- `C01`: **20 h / R$4.000** => implantação mínima (fundação+base+YouTube) **522 h / R$104.400**.
- `C02`: **68 h / R$13.600** => implantação mínima com Stream **570 h / R$114.000**.
- `C03`: **166 h / R$33.200** => implantação mínima com offline **668 h / R$133.600**.

**Preço de venda comercial por feature pode diferir da referência.** Modelo sugerido de cada feature: `id`, `section`, `title`, `description`, `type`, `hoursMin`, `hoursLikely`, `hoursHigh`, `complexity`, `perceivedValue`, `hourlyReference`, `referenceImplementationBRL`, `commercialPriceBRL|null`, `monthlyCostModel`, `sharedProviders`, `dependencies`, `exclusions`, `pricingStatus`, `sourceUrls`. O somatório comercial deve usar a coluna comercial quando definida; se não, mostrar referência e marcar que o preço de venda ainda é proposto. Jamais converter ausência (`null`) em zero.

## 8. Catálogo canônico — 55 features e horas revisadas (não excluir, não renomear IDs)

Nesta tabela, **descrição e operação pertencem a cada feature**, mas **os custos compartilhados de fornecedor não são somados uma vez por card**. Números em R$ são **valores de referência de implantação**, não preços finais aprovados.

| ID | Módulo | Feature / descrição funcional | Tipo | Horas provável | Referência R$200/h | Complexidade 1–5 | Custo operacional / fornecedor / observação |
|---|---|---|---|---:|---:|---:|---|
| `B01` | Base obrigatória | **Mural inicial: cursos em destaque**: Mural inicial com cursos em destaque, banners de capa e acesso ao catálogo. | Obrigatória | 26 h | R$ 5.200 | 2 | Supabase (base compartilhada) — Uso de banco/API dentro do plano; excedentes variáveis. |
| `B02` | Base obrigatória | **Login, logout e recuperação de senha**: Entrar, sair e recuperar senha por e-mail, com sessão protegida. | Obrigatória | 28 h | R$ 5.600 | 3 | Supabase Auth + e-mail — Incluído no plano base até franquia; reset conta na cota de e-mails. |
| `B03` | Base obrigatória | **Integração com serviço de e-mail transacional**: Envio de e-mails transacionais, como redefinição de senha, com domínio autenticado. | Obrigatória | 16 h | R$ 3.200 | 2 | Resend ou provedor transacional — Free: 3.000 e-mails/mês (limite diário); Pro: US$ 20/mês até 50.000. |
| `B04` | Base obrigatória | **Perfil privado do cliente**: Perfil privado: foto, nome, e-mail verificado e gestão de senha. | Obrigatória | 32 h | R$ 6.400 | 2 | Supabase + Cloudflare R2 — Banco no plano compartilhado; R2: US$ 0,015/GB-mês além da franquia + operações. |
| `B05` | Base obrigatória | **Preferência de comunicações de marketing**: Aceite e revogação de e-mails promocionais com registro da escolha. | Obrigatória | 12 h | R$ 2.400 | 2 | Supabase + e-mail — Dados incluídos no backend; campanhas não estão incluídas. |
| `B06` | Base obrigatória | **Catálogo, módulos e aulas de cursos**: Catálogo de cursos, módulos, aulas e páginas de detalhes. | Obrigatória | 64 h | R$ 12.800 | 4 | Supabase — Consultas dentro do plano; consumo adicional se exceder cotas. |
| `B07` | Base obrigatória | **Progresso por aula e curso**: Registro e visualização do progresso do aluno em aulas e cursos. | Obrigatória | 32 h | R$ 6.400 | 3 | Supabase — Escritas/leituras e armazenamento de progresso; excedentes por uso. |
| `B08` | Base obrigatória | **Painel administrativo básico**: Painel ATSI para administrar cursos, aulas e destaques com permissões. | Obrigatória | 56 h | R$ 11.200 | 4 | Supabase + hospedagem web — Operação de API e hospedagem; provedor e plano web a definir. |
| `A01` | Autenticação adicional | **Autenticação multifator (MFA)**: Segundo fator de autenticação opcional e recuperação segura de acesso. | Opcional | 24 h | R$ 4.800 | 3 | Supabase Auth MFA — TOTP pode usar recursos do plano; SMS acrescenta tarifa por mensagem. |
| `A02` | Autenticação adicional | **Entrar com Google**: Entrar com uma conta Google e vincular identidades existentes. | Opcional | 16 h | R$ 3.200 | 2 | Supabase Auth + OAuth Google — Geralmente coberto pelo plano de autenticação; verificar cotas e política. |
| `A03` | Autenticação adicional | **Entrar com Microsoft**: Entrar com Microsoft e integrar contas corporativas permitidas. | Opcional | 18 h | R$ 3.600 | 2 | Supabase Auth + Microsoft OAuth — Normalmente dentro de cotas de autenticação; licenças/Entra podem variar. |
| `A04` | Autenticação adicional | **Entrar com Facebook**: Entrar com uma conta Facebook e vincular a identidade à conta ATSI+, com consentimento e permissões necessárias ao acesso. | Opcional | 32 h | R$ 6.400 | 3 | Serviço de identidade compartilhado + integração oficial Meta — Validar permissões, políticas, credenciais e cotas na arquitetura. |
| `M01` | Mural — vitrines opcionais | **E-books em destaque no mural**: Card de e-book em destaque na home com capa, resumo e link. | Opcional | 10 h | R$ 2.000 | 1 | Supabase + R2 (se houver capa) — R2 Standard: US$ 0,015/GB-mês além de 10 GB + operações. |
| `M02` | Mural — vitrines opcionais | **Eventos em destaque no mural**: Card de evento em destaque na home com data e link. | Opcional | 10 h | R$ 2.000 | 1 | Supabase + R2 (capa) — Dados no backend; armazenamento da capa em R2 conforme uso. |
| `M03` | Mural — vitrines opcionais | **Promoções em destaque no mural**: Banners e chamadas promocionais com programação e link de destino. | Opcional | 12 h | R$ 2.400 | 2 | Supabase + R2 (banners) — Dados dentro do backend; armazenamento/leituras em R2 conforme uso. |
| `C01` | Cursos — entrega de vídeos | **Player YouTube incorporado**: Player do YouTube integrado às aulas, sem hospedagem de vídeo própria. | Escolha única | 20 h | R$ 4.000 | 2 | YouTube embed — US$ 0/mês direto de hospedagem/streaming do vídeo no embed padrão. |
| `C02` | Cursos — entrega de vídeos | **Streaming privado na nuvem**: Upload, processamento, player e controle de acesso a vídeos privados online. | Escolha única | 68 h | R$ 13.600 | 4 | Cloudflare Stream — Armazenamento: US$ 5/1.000 min/mês (blocos); entrega: US$ 1/1.000 min vistos. |
| `C03` | Cursos — entrega de vídeos | **Streaming privado + download offline**: Vídeos privados e downloads para reprodução offline controlada no app. | Escolha única | 166 h | R$ 33.200 | 5 | Cloudflare Stream + armazenamento do app — Mesma tabela do Stream: US$ 5/1.000 min armazenados + US$ 1/1.000 min entregues ou baixados. |
| `C04` | Cursos — opcionais | **Emissão de certificados**: Certificado PDF após conclusão, com modelo e código de verificação. | Opcional | 32 h | R$ 6.400 | 3 | Supabase + R2 — PDFs em R2 (US$ 0,015/GB-mês fora franquia) + operações. |
| `C05` | Cursos — opcionais | **Quizzes e avaliações de aprendizagem**: Quizzes com perguntas, alternativas, correção e tentativas do aluno. | Opcional | 48 h | R$ 9.600 | 3 | Supabase — Persistência no backend; custos adicionais só por uso além de cotas. |
| `C06` | Cursos — opcionais | **Geração de testes com inteligência artificial**: IA gera sugestões de testes a partir de texto do curso, com revisão humana. | Opcional | 56 h | R$ 11.200 | 4 | API de IA + transcrição/arquivo — Variável por tokens do modelo; transcrição/ingestão pode ter custo adicional. |
| `C07` | Cursos — opcionais | **Chat com IA sobre o vídeo/aula**: Chat com IA responde dúvidas sobre aulas usando transcrições e fontes autorizadas. | Opcional | 112 h | R$ 22.400 | 5 | API de IA + embeddings/RAG — Variável por tokens, transcrição, indexação e consultas ao banco vetorial. |
| `C08` | Cursos — opcionais | **Comentários em videoaulas**: Comentários e respostas em cada videoaula com moderação básica. | Opcional | 34 h | R$ 6.800 | 3 | Supabase (dados/Realtime se ativado) — Dados e eventual tempo real dentro de franquias; excedentes sob uso. |
| `C09` | Cursos — opcionais | **Avaliação de satisfação do curso**: Aluno atribui nota e opinião ao curso depois da experiência. | Opcional | 20 h | R$ 4.000 | 2 | Supabase — Armazenamento da avaliação no plano base; eventuais excedentes. |
| `E01` | E-books | **Biblioteca de e-books**: Biblioteca de PDFs/e-books com pesquisa, capas e download autorizado. | Opcional | 40 h | R$ 8.000 | 3 | Cloudflare R2 + Supabase — R2 Standard US$ 0,015/GB-mês além da franquia; operações A/B tarifáveis. |
| `N01` | Notificações | **Notificações push básicas**: Enviar avisos push de novos cursos, eventos e comunicações da plataforma. | Opcional | 32 h | R$ 6.400 | 3 | Expo Push + FCM/APNs — O envio básico pode usar Expo sem tarifa por mensagem; custos de apps/build e limites à parte. |
| `N02` | Notificações | **Push segmentado**: Enviar notificações para segmentos como novos alunos ou cursos específicos. | Opcional | 30 h | R$ 6.000 | 3 | Supabase + push — Mesmo serviço push; consultas/filas usam backend e cotas. |
| `N03` | Notificações | **Automações de notificações**: Disparar mensagens automaticamente por regras e agendamento. | Opcional | 52 h | R$ 10.400 | 4 | Supabase + push/cron — Processamento e jobs consumidos; custos por volume/fornecedor. |
| `G01` | Grupos e comunidade | **Diretório/links de grupos de WhatsApp**: Catálogo de grupos com botões que abrem convites oficiais do WhatsApp. | Opcional | 12 h | R$ 2.400 | 2 | Supabase + link WhatsApp — Sem cobrança de API para simples abrir link; backend dentro do plano. |
| `G02` | Grupos e comunidade | **Encaminhamento multicanal para redes sociais**: Configurar mensagens e conteúdo para distribuição a múltiplos grupos e canais de diferentes redes sociais no mesmo agendamento, conforme APIs e permissões disponíveis. | Opcional | 250 h | **R$ 50.000** | 5 | APIs oficiais das redes / parceiros autorizados — validar por rede os destinos permitidos, credenciais, limites, cobrança e elegibilidade. |
| `G03` | Grupos e comunidade | **Grupos internos: conteúdos e notícias**: Grupos internos com membros, notícias, publicações e moderação. | Opcional | 64 h | R$ 12.800 | 4 | Supabase + R2 para mídia — Banco/realtime/arquivos dentro de cotas; R2 conforme tamanho e operações. |
| `G04` | Grupos e comunidade | **Chat direto entre usuários**: Mensagens privadas entre usuários com histórico, bloqueio e denúncias. | Opcional | 96 h | R$ 19.200 | 5 | Supabase Realtime + banco — Picos de conexões e volume de mensagens podem gerar excedentes mensais. |
| `G05` | Grupos e comunidade | **Perfis públicos de usuários**: Perfil público opt-in com nome público, imagem e dados escolhidos pelo usuário. | Opcional | 40 h | R$ 8.000 | 3 | Supabase + R2 — Dentro de cotas de dados/armazenamento; R2 para imagens conforme uso. |
| `G06` | Grupos e comunidade | **Pesquisa global por usuários**: Pesquisa global de perfis publicáveis com paginação e regras de privacidade. | Opcional | 28 h | R$ 5.600 | 3 | PostgreSQL / Supabase — Consultas e índices usam plano de banco; escala pode exigir busca dedicada. |
| `EV01` | Eventos e inscrições | **Gestão de eventos + inscrições + painel admin**: Cadastrar eventos, vagas, inscrições e listas no painel da ATSI. | Opcional | 88 h | R$ 17.600 | 4 | Supabase + R2 — Transações no banco e imagens em R2; custos conforme uso. |
| `EV02` | Eventos e inscrições | **Gerar QR Code individual para inscrição**: Gerar um QR Code identificador exclusivo para cada inscrição. | Opcional | 22 h | R$ 4.400 | 3 | Backend + QR/PDF — Baixo custo incremental; se gerar PDFs/imagens persistidos, R2 por volume. |
| `EV03` | Eventos e inscrições | **Enviar convite do evento por e-mail**: Enviar convites de evento por e-mail com modelos e rastreio de envios. | Opcional | 18 h | R$ 3.600 | 2 | Resend + backend — Compartilha franquia de e-mails: Free 3.000/mês; Pro US$ 20/mês/50.000. |
| `EV04` | Eventos e inscrições | **Leitura de QR Code para check-in do evento**: Ler QR Code na entrada, validar ingresso e registrar check-in. | Opcional | 52 h | R$ 10.400 | 5 | Câmera do app + Supabase — API/banco dentro de cotas; mais uso gera mais tráfego. |
| `P01` | Pagamentos e controle de acesso | **Integração com serviço de pagamento**: Conectar gateway web, criar pedidos, reconciliar pagamentos e webhooks. | Opcional | 72 h | R$ 14.400 | 5 | Gateway de pagamento — Taxas por transação e eventuais mensalidades do gateway; fornecedor a escolher. |
| `P02` | Pagamentos e controle de acesso | **Assinatura da plataforma**: Oferecer planos por assinatura com renovação e cancelamento. | Opcional | 84 h | R$ 16.800 | 5 | Gateway + app stores se aplicável — Comissões/taxas por cobrança recorrente; varia por canal e país. |
| `P03` | Pagamentos e controle de acesso | **Venda avulsa de cursos**: Comprar curso individualmente e liberar acesso após confirmação. | Opcional | 48 h | R$ 9.600 | 4 | Gateway/IAP + controle de acesso — Taxa por compra no gateway ou comissão da loja se aplicável. |
| `P04` | Pagamentos e controle de acesso | **Venda de ingressos/inscrições de eventos**: Vender ingressos de eventos, com pagamento e confirmação. | Opcional | 48 h | R$ 9.600 | 4 | Gateway + inscrições — Taxas por transação de evento; reembolsos/estornos podem ter custos. |
| `P05` | Pagamentos e controle de acesso | **Controle de acesso de cursos por perfil/assinatura/pagamento**: Liberar cursos conforme perfil, assinatura, pagamento ou direito de acesso. | Opcional | 68 h | R$ 13.600 | 5 | Supabase + serviço de vídeo privado — Consultas e assinaturas dentro de cotas; Stream se C02/C03. |
| `P06` | Pagamentos e controle de acesso | **Controle de acesso de eventos**: Restringir eventos a perfis, convidados ou clientes pagantes. | Opcional | 38 h | R$ 7.600 | 4 | Supabase — Operação dentro de banco/API; escalonamento por uso. |
| `P07` | Pagamentos e controle de acesso | **Controle de acesso de e-books**: Restringir acesso e download dos e-books a públicos elegíveis. | Opcional | 32 h | R$ 6.400 | 3 | Supabase + R2 — Backend + R2 (armazenamento/operação) conforme uso. |
| `L01` | Auditoria | **Logs administrativos de auditoria**: Registrar histórico de ações administrativas: usuário, hora e alteração. | Opcional | 48 h | R$ 9.600 | 4 | Supabase / logs — Retenção e armazenamento podem exigir plano/logs maiores. |
| `R01` | Relatórios administrativos | **Relatório de visualizações de cursos/aulas**: Relatório de visualizações de cursos e aulas por período. | Opcional | 36 h | R$ 7.200 | 4 | Supabase / eventos de uso — Mais eventos gravados = mais banco/armazenamento; pode exigir analytics. |
| `R02` | Relatórios administrativos | **Relatório de conclusão dos cursos**: Relatório de alunos e cursos concluídos, com filtros e exportação. | Opcional | 24 h | R$ 4.800 | 2 | Supabase — Consultas agregadas geralmente cobertas no início; escala depende de volume. |
| `R03` | Relatórios administrativos | **Relatório de avaliações/satisfação de cursos**: Painel consolidado de avaliações e satisfação dos cursos. | Opcional | 22 h | R$ 4.400 | 2 | Supabase — Consultas agregadas; consumo de banco conforme uso. |
| `R04` | Relatórios administrativos | **Relatório de usuários ativos**: Métricas de usuários ativos diariamente e mensalmente. | Opcional | 40 h | R$ 8.000 | 4 | Supabase / analytics — Coleta de eventos e agregação; excedentes ou analytics dedicado. |
| `R05` | Relatórios administrativos | **Relatório de usuários simultâneos**: Mostrar quantidade de usuários online simultaneamente. | Opcional | 72 h | R$ 14.400 | 5 | Supabase Realtime / presença — Conexões concorrentes, mensagens e heartbeat podem gerar excedentes. |
| `GM01` | Gamificação | **Motor de pontos por aulas e cursos concluídos**: Ganhar pontos por concluir aulas e cursos, com saldo e regras. | Opcional | 56 h | R$ 11.200 | 4 | Supabase — Gravação de eventos e ranking; banco dentro de cotas inicialmente. |
| `GM02` | Gamificação | **Pontos por presença em eventos**: Creditar pontos após participação comprovada em eventos. | Opcional | 22 h | R$ 4.400 | 3 | Supabase + check-in — Baixo custo incremental no banco, dependendo do volume. |
| `GM03` | Gamificação | **Ranking público**: Mostrar classificação pública por pontos e períodos. | Opcional | 36 h | R$ 7.200 | 4 | Supabase / cache eventual — Consultas e ranking; Redis opcional só se necessário. |
| `GM04` | Gamificação | **Pontos e posição no ranking no perfil**: Mostrar pontos acumulados e posição do usuário em seu perfil. | Opcional | 18 h | R$ 3.600 | 2 | Supabase — Leituras de pontuação dentro das cotas do backend. |
| `GT01` | Gestão de tarefas e conteúdo | **Gestão de tarefas**: Criar e editar tarefas, definir responsáveis, prazos e prioridades. | Opcional | 50 h | R$ 10.000 | 3 | Serviços compartilhados conforme volume. |
| `GT02` | Gestão de tarefas e conteúdo | **Kanban interativo**: Organizar tarefas em quadros e colunas, movendo cards entre etapas. | Opcional | 37.5 h | R$ 7.500 | 3 | Serviços compartilhados conforme volume. |
| `GT03` | Gestão de tarefas e conteúdo | **Calendário de tarefas**: Visualizar tarefas por semana ou mês com seus prazos. | Opcional | 32 h | R$ 6.400 | 2 | Serviços compartilhados conforme volume. |
| `GT04` | Gestão de tarefas e conteúdo | **Planejamento de conteúdo**: Associar tarefas a cursos, e-books, notícias e eventos disponíveis no escopo contratado. | Opcional | 40 h | R$ 8.000 | 3 | Serviços compartilhados conforme volume. |
| `GT05` | Gestão de tarefas e conteúdo | **Comentários e anexos nas tarefas**: Reunir discussões e documentos nas tarefas da equipe. | Opcional | 32 h | R$ 6.400 | 3 | Armazenamento conforme volume. |
| `GT06` | Gestão de tarefas e conteúdo | **Notificações de tarefas**: Avisar responsáveis sobre atribuições, prazos e alterações. | Opcional | 22 h | R$ 4.400 | 3 | Entrega de notificações conforme canais contratados. |
| `GT07` | Gestão de tarefas e conteúdo | **Aprovação de conteúdo**: Revisar e aprovar conteúdo antes da publicação, com retorno para ajustes. | Opcional | 38 h | R$ 7.600 | 4 | Serviços compartilhados conforme volume. |

**Totalização e checagem:** a matriz canônica contém **55 features: 8 obrigatórias + 44 opcionais + 3 de escolha única**, mais 7 linhas de fundação. `G02` recebeu estimativa conservadora de 250 h / R$ 50.000 em 17/11/2026, sem alterar os presets. `A04` acrescenta login com Facebook como opcional independente. **Google Drive experimental não é uma 56ª feature pronta para venda**; mantenha separado do catálogo canônico ou explique claramente a linha experimental sem contaminar contagens/contrato. Preserve também os intervalos de horas mín./prov./conserv. do CSV v5 quando esses documentos estiverem no workspace.

## 9. Dependências e incompatibilidades obrigatórias

- `B01..B08`: sempre ativas, não removíveis. `B07` não pode aparecer como opcional.
- `C01/C02/C03`: **exatamente uma** selecionada; mudanças substituem a anterior e recalculam total; `C03` já inclui `C02`; `DRIVE-PILOT` não constitui escolha de produção aprovada.
- `C04` depende de `B07`. `C06` depende de `C05`. `C07` exige fonte/transcrição autorizada e uso de IA — preço de operação sob variável.
- `C09` é distinto de `C05`; `R03` depende de `C09`.
- `N02`, `N03` dependem de `N01`.
- `G06` depende de `G05`; consentimento e regras de privacidade para perfis públicos, busca e ranking. `G02` ampliada em 17/11/2026 para múltiplas redes, grupos e canais; selecionável na simulação, com execução de cada conector condicionada à documentação oficial e elegibilidade da integração/destino. **Não usar bot não oficial ou automação via WhatsApp Web para contornar restrições.** `G01` só abre diretório/links, sem disparos.
- `EV02`, `EV03`, `EV04` dependem de `EV01`; convite por e-mail reutiliza `B03`, sem contratar Resend duas vezes. `P04` depende de `EV01` e `P01` (ou estratégia de pagamento aprovada).
- `P02/P03/P04` dependem de uma estratégia válida de cobrança/in-app purchase que respeite a política da loja e os direitos de acesso. `P05` é serviço de autorização e deve habilitar os cursos vendidos, liberados por perfil ou assinatura; `P06` eventos; `P07` e-books (quando existirem).
- `R01` depende de telemetria/captura de eventos; `R02` usa progresso `B07`; `R04` exige definição inequívoca de 'usuário ativo'; `R05` exige heartbeat/presença e não equivale a 'usuários ativos'.
- `GM01` motor de pontos; `GM02` depende de check-in confirmado `EV04`; `GM03` de `GM01`; `GM04` de `GM01` + `GM03`. Política YouTube: não prometer recompensas por visualizações de vídeo. Se optado `C01`, marcar alerta/incompatibilidade e exigir alternativa de regra de pontos que não recompense assistir ao player.
- Se desmarcar dependência com complementos habilitados, mostrar escolha clara: cancelar a alteração ou remover dependentes (com confirmação e recálculo). Nunca deixar estado inconsistente silenciosamente.
- O 'conteúdo do mural' não equivale a 'módulo de gestão de e-books/eventos/promoções'; cobrança por destaque `M01..M03` só se selecionado e não cobrar como parte do `B01`.
- Não afirmar que assinatura via gateway web poderá ser vendida no app nativo sem revisar regras Apple/Google por tipo de produto, país e canal.

## 10. Presets funcionais válidos por padrão

- **Essencial:** F01..F07 + B01..B08 + `C01`. Menor custo operacional direto de vídeo. Cursos com YouTube devem ser apresentados como hipótese de conteúdo cujo modelo de acesso seja compatível com as políticas. Demais opcionais desligados por padrão.
- **Plus:** fundação + base + `C02` + (a título de proposta, nunca imposto) `C04`, `C05`, `E01`, `N01`, `M01`; se habilitar M01 e E01, são entregas distintas: card vs biblioteca. Ajustar a proposta na UI sem violar dependências.
- **Premium:** fundação + base + `C03` + (proposta) `A01`,`C04`,`C05`,`C06`,`C07`,`C08`,`C09`,`E01`,`M01`,`M02`,`M03`,`N01`,`N02`,`G03`,`EV01`,`EV02`,`EV03`,`EV04`, com todos os custos de IA/serviços sob aviso. **Não selecionar G02**, nem funcionalidades de pagamentos como se a decisão comercial já estivesse aprovada. Apresentar como pacote ilustrativo configurável, sem compromisso contratual.
- Ao editar manualmente qualquer preset: estado Personalizado. Cada preset deve ter seleção correta de vídeo e totais reproduzíveis.

## 11. Fluxo do mockup e conteúdo das seções

- Ao clicar na seção, exibir/expandir as features; ao clicar em uma feature, smartphone deve mudar para mockup correspondente, inclusive a opção Drive experimental e páginas de 'custos da infraestrutura'. Não basta alterar título: desenhar tela representativa de usuário ou painel admin.
- Telas: mural com curso em destaque e complementos somente se habilitados; autenticação/segurança; perfil; catálogo/curso/progresso; visual de YouTube, Stream e offline com estados distintos; biblioteca; push; grupos/WhatsApp; eventos/convite/QR/check-in; pagamento/assinatura/entitlements; IA/quizzes/chat; logs/relatórios/gamificação.
- Mostrar na visualização da feature **contratada vs apenas visualizada**. Para todos os elementos, usar elementos de UI acessíveis e nenhum ícone que dependa de baixar fontes externas se for standalone.
- Insumos de operação na lateral ou modal secundário claro, sem perder resumo total embaixo do celular. Gráfico comparativo YouTube × Stream e composição mensal por fornecedor.
- Disponibilizar tooltip/accordion 'Como calculamos?' para cada feature e serviço, explicando que horas representam esforço, R$200/h é referência e mensalidades são despesas da ATSI ou repasse conforme contrato.

## 12. QA exigido antes de concluir

Teste com as ferramentas disponíveis na stack atual; crie funções puras para a matemática e use suite de testes automatizados quando viável. **Não declarar PASS sem execução efetiva.** Casos mínimos:

1. 55 IDs canônicos únicos; oito B obrigatórios; exatamente um vídeo; não incluir DRIVE-PILOT no total de produção.
2. F01..F07 = 236 h; B01..B08 = 266 h. Essencial puro: 522 h / R$104.400; privado puro: 570 h / R$114.000; offline puro: 668 h / R$133.600 **na referência, sem opcionais**.
3. C02→C03 recalcula corretamente e não soma Stream duas vezes. Se C01→C02, atualizar mockup, descrição, horas, implantação e operação.
4. Presets todos válidos; personalização, valores editáveis, recarregar/importar, dependências, exclusões, remoção em cascata, G02 selecionável com aviso de viabilidade por rede.
5. Stream cenários: 100/2h/30h => US$22; 1.000/3h/100h => US$210; 5.000/4h/300h => US$1.290; ajustar segundos/minutos e arredondamentos corretos.
6. 15GB R2 e operações abaixo da franquia => somente GB faturável de armazenamento; 0 GB e zero ops => US$0; Stream nunca duplica R2; Supabase/Resend contabilizados uma vez.
7. Preço da feature ausente ou IA sem volume não vira R$0/US$0; exibir 'sob cotação' e avisos, sem falsa totalização completa. G02 usa a estimativa conservadora explícita de implantação; terceiros permanecem a validar.
8. Moedas separadas BRL/USD; câmbio manual apenas se informado; campo de custo interno não se confunde com tarifa comercial.
9. YT + offline proibido; YT + políticas de paywall/recompensa alerta/impede proposta incompatível; Drive não tratado como privado garantido; fontes clicáveis e disclaimer.
10. Telas/preview correspondem à feature clicada, sem seleção acidental. Responsividade em 390, 768 e 1440 px; teclados, foco, contraste, campos inválidos, exportação/impressão. Sem regressão de tema escuro, presets e mockup 50/50.

## 13. Entregáveis e relato final obrigatórios

- Código do configurador atualizado (preservando o padrão do repositório), com testes possíveis e `AGENTS.md`/README ajustados ao **estado real**.
- Matriz/dados precificação internos (55 IDs + fundação) separados do componente de UI quando possível; camada de fórmula isolada.
- Documentação 'Arquitetura e Custos' com **descrição de cada feature**, horas e custo de implantação, custo operacional por serviço, comparação entre YouTube / Cloudflare Stream / offline / Drive experimental, data-base e links oficiais.
- No relatório final ao solicitante: arquivos modificados, implementação concluída, cálculos conferidos, comandos de teste e resultados reais, pendências/limitações/decisões que exigem contrato ou fornecedor. **Não pedir ao solicitante para repetir definições já informadas**; use essas decisões como fonte. Não publicar/contratar serviços ou fazer deploy sem autorização.

**Prioridade para resolver conflitos:** decisões deste prompt > dados numéricos técnicos v5 e auditoria v4 > escopo v3 > protótipo v2/AGENTS.md antigo. Todavia, **não sobrescrever trabalho local posterior sem reconciliação**. Se qualquer documento estiver ausente, este prompt contém os IDs, regras e números necessários para avançar.

**Critério de pronto:** o configurador permite selecionar uma configuração válida, entender o que cada feature entrega, visualizar sua tela no celular, saber horas + referência + preço de venda, comparar alternativas de vídeo incluindo riscos de YouTube/Drive, simular despesas mensais externas sem duplicá-las e exportar uma proposta honesta — incluindo o que ainda está sob cotação.
