# F01 — Análise de requisitos e jornadas

**Status:** proposta inicial; tarefas e horas pendentes de validação. Mínimo: **40 h**, considerando uma semana de 5 dias úteis com 8 h por dia. A referência anterior era de 32 h.

## Escopo e premissas
Levantar e analisar requisitos, jornadas, prioridades e critérios de aceite do produto. Pressupõe acesso aos responsáveis da ATSI. O design de interface e a arquitetura estão em F02; implementação visual e pesquisas extensivas não estão incluídas.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| F01-T01 | Workshops com responsáveis, objetivos, públicos e plataformas | 12 | Revisão técnica preliminar |
| F01-T02 | Mapear jornadas e requisitos funcionais por módulo do catálogo | 20 | Revisão técnica preliminar |
| F01-T03 | Definir requisitos não funcionais, privacidade e restrições | 12 | Revisão técnica preliminar |
| F01-T04 | Organizar épicos, prioridades, dependências e exclusões | 12 | Revisão técnica preliminar |
| F01-T05 | Revisar specs e critérios de aceite das features contratáveis | 24 | Revisão técnica preliminar |
| F01-T06 | Decompor tarefas, revisar estimativas e registrar premissas | 16 | Revisão técnica preliminar |
| F01-T07 | Consolidar pendências e conduzir revisão de aprovação | 8 | Revisão técnica preliminar |
| **Total** | | **104 h** | **Aprovação pendente** |

## Dependências e riscos
Disponibilidade dos envolvidos e decisões sobre plataformas e acesso. Mudanças de escopo podem exigir nova estimativa.

## Entregáveis obrigatórios e marco de aprovação
- Análise de requisitos funcionais e não funcionais, jornadas, regras, premissas e pendências.
- Épicos com objetivos, escopo e prioridades.
- Especificações por feature com dependências, exclusões e critérios de aceite.
- Tarefas de implementação, testes e homologação, com estimativas revisadas.

Todos devem ser revisados e aprovados pela ATSI e pela YvyLab antes do início
do desenvolvimento. Status atual: **aprovação pendente**. As tarefas existentes
devem produzir esses artefatos; não há cobrança separada adicional. As 40 h são
um mínimo e sua suficiência precisa ser validada, não uma garantia para qualquer escopo.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **104 h**. Estimativa anterior: 40 h.
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
Cada feature planejada está ligada a um épico, a critérios de aceite e a tarefas; decisões não resolvidas têm responsável e não são tratadas como aprovadas.
