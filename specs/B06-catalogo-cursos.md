# B06 — Catálogo, módulos e aulas

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 64 h.

## Escopo e funcionamento
Exibir catálogo, detalhes, módulos e aulas; dados gerenciados pelo painel. A estratégia de vídeo é escolha separada e obrigatória.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B06-T01 | Modelar cursos, módulos, aulas e ordem de publicação | 12 | Revisão técnica preliminar |
| B06-T02 | Implementar consultas, paginação e acesso básico autorizado | 14 | Revisão técnica preliminar |
| B06-T03 | Construir catálogo e página de detalhes | 16 | Revisão técnica preliminar |
| B06-T04 | Construir navegação módulo/aula e integração do player escolhido | 12 | Revisão técnica preliminar |
| B06-T05 | Tratar conteúdo indisponível e falhas de carregamento | 6 | Revisão técnica preliminar |
| B06-T06 | Testar ordenação, publicação e fluxos mobile | 12 | Revisão técnica preliminar |
| **Total** | | **72 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Depende da fundação, B08 e uma estratégia C01/C02/C03. Backend compartilhado; vídeo e suas despesas são contabilizados separadamente.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **72 h**. Estimativa anterior: 64 h.
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
A ordem curso/módulo/aula é consistente com o painel; conteúdo não publicado não é exposto por consulta direta.
