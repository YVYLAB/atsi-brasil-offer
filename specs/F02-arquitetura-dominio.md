# F02 — Design e arquitetura

**Status:** proposta inicial; tarefas e horas pendentes de validação. Mínimo: **40 h**, considerando uma semana de 5 dias úteis com 8 h por dia. A referência anterior era de 32 h.

## Escopo e premissas
Desenhar fluxos e interfaces essenciais, domínio relacional e autorização para a base. Pressupõe React Native/Expo, Next.js e Supabase como hipóteses, não decisões definitivas. Não inclui implementação visual nem desenvolvimento completo.

**Atualização de escopo — 17/11/2026:** considerar aplicativos Android/iOS,
versão web para alunos e painel administrativo web desde o Essencial.
Detalhar jornadas e diferenças por plataforma, inclusive navegadores e
tecnologia da web dos alunos, sem confundi-la com o painel administrativo.
O impacto nas tarefas/horas atuais está pendente; consulte `plataformas-entrega.md`.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| F02-T01 | Definir arquitetura da informação e fluxos essenciais | 16 | Revisão técnica preliminar |
| F02-T02 | Desenhar wireframes mobile e painel administrativo | 24 | Revisão técnica preliminar |
| F02-T03 | Produzir telas de referência e estados de erro/vazio | 24 | Revisão técnica preliminar |
| F02-T04 | Modelar domínio, diagrama de classes e relacionamentos | 16 | Revisão técnica preliminar |
| F02-T05 | Definir arquitetura, contratos e fronteiras dos serviços | 16 | Revisão técnica preliminar |
| F02-T06 | Desenhar autorização, segurança e fluxo de dados pessoais | 12 | Revisão técnica preliminar |
| F02-T07 | Revisar acessibilidade e decisões com ATSI/YvyLab | 12 | Revisão técnica preliminar |
| **Total** | | **120 h** | **Aprovação pendente** |

## Dependências e riscos
Depende das jornadas de F01; regras de acesso e LGPD ainda exigem validação.

## Entregáveis obrigatórios e marco de aprovação
- Telas e mockups dos fluxos essenciais, incluindo estados relevantes para validação.
- Diagrama de classes e domínio: entidades, relacionamentos e responsabilidades.
- Decisões de arquitetura, autenticação e autorização que sustentam o desenho.

Todos devem ser revisados e aprovados pela ATSI e pela YvyLab antes do início
do desenvolvimento. Status atual: **aprovação pendente**. Mockups comerciais do
configurador não substituem o design de produto aprovado. Os entregáveis integram
as tarefas acima, sem cobrança adicional. As 40 h são um mínimo cuja suficiência
será revisada com o escopo.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **120 h**. Estimativa anterior: 40 h.
As horas da tabela acima substituem a distribuição inicial e são esforço de uma
pessoa, não prazo contratual. A ampliação cobre fluxos, autorização, falhas e
testes específicos que não estavam explicitados no rascunho.
As referências históricas no texto e no catálogo de origem não são o total vigente.
As tarefas estão sujeitas a revisão e aprovação; não foram executadas.

### Critérios de aceite transversais
- Entrega específica descrita em cada tarefa demonstrada em ambiente de homologação.
- Caminho principal e estados de vazio, erro e ausência de permissão verificados
  quando aplicáveis à interface e à integração.
- Regras de acesso aplicadas no servidor, não apenas ocultadas na interface.
- Testes da tarefa documentados e verificáveis; critérios funcionais específicos
  de negócio devem ser aprovados durante F01.
- Dependências, credenciais e decisões pendentes registradas antes de implementar.

### Limites da estimativa
Premissa: React Native/Expo Android e iOS, painel Next.js e backend Supabase;
uma implementação de referência e um ciclo de revisão por entrega. Recursos
do provedor e viabilidade técnica devem ser confirmados antes de compromisso.
Mudanças de escopo, integrações extras, migração de legado, tradução, DRM avançado,
funcionamento offline além do descrito e múltiplos gateways não estão implícitos.
Testes locais pertencem às features; F07 cobre integração, não repetição integral
dos mesmos testes. F01/F02 cobrem planejamento geral; tarefas de detalhamento
das features tratam decisões técnicas específicas e não repetem a descoberta.
Sem contingência percentual automática e sem custos de fornecedores incluídos.

## Cenário mínimo específico de aceite
Fluxos essenciais têm telas e estados associados; o diagrama explicita entidades e relações, e decisões de autorização correspondem às jornadas.

## Decisões de fornecedores — deliberadas na arquitetura
As tecnologias citadas anteriormente são hipóteses de estimativa, não contratações.
Escolher e registrar em decisões de arquitetura os serviços de versionamento,
CI/CD, hospedagem, banco, armazenamento, vídeo, e-mail e distribuição mobile.
Comparar compatibilidade, custo, segurança, portabilidade, limites e operação.
Definir responsáveis pelas contas, ambientes necessários e estratégia de deploy,
segredos, migrações e recuperação.

Esse trabalho integra a definição de arquitetura e a revisão já estimadas, sem
acréscimo de horas nesta atualização. F05/F06/B03 dependem dessas decisões.
O aceite exige decisões aprovadas ou pendências explícitas que impeçam iniciar
a configuração afetada; nenhum fornecedor é presumido aprovado.
