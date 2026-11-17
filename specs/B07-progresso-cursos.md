# B07 — Progresso por aula e curso

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 32 h.

## Escopo e funcionamento
Registrar e apresentar progresso por aula e curso. Não inclui certificados nem recompensas.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B07-T01 | Definir regras de conclusão e retomada por estratégia de vídeo | 6 | Revisão técnica preliminar |
| B07-T02 | Implementar progresso idempotente por usuário e aula | 10 | Revisão técnica preliminar |
| B07-T03 | Calcular conclusão do curso e atualizar visualização | 8 | Revisão técnica preliminar |
| B07-T04 | Tratar reconexão e alterações no catálogo | 6 | Revisão técnica preliminar |
| B07-T05 | Testar isolamento, repetição de eventos e retomada | 10 | Revisão técnica preliminar |
| **Total** | | **40 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Depende de B02 e B06. Backend compartilhado; volume de leituras e escritas varia com o uso. No configurador legado, progresso ainda aparece como opcional e tem outra estimativa.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **40 h**. Estimativa anterior: 32 h.
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
Repetir um evento de conclusão não duplica progresso e a conclusão pertence exclusivamente ao usuário autenticado.
