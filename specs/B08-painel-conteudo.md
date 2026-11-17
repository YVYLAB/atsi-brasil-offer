# B08 — Painel administrativo básico

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 56 h.

## Escopo e funcionamento
Gerenciar cursos, módulos, aulas e destaques com permissões. Fundação de interface e papéis está em F04; gestão de eventos e auditoria detalhada são opcionais separados.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B08-T01 | Definir permissões e estados de publicação | 8 | Revisão técnica preliminar |
| B08-T02 | Implementar CRUD de cursos, módulos e aulas | 18 | Revisão técnica preliminar |
| B08-T03 | Construir listagens, formulários e ordenação | 20 | Revisão técnica preliminar |
| B08-T04 | Integrar capas e destaques do mural | 8 | Revisão técnica preliminar |
| B08-T05 | Tratar validações, exclusão e referências em uso | 8 | Revisão técnica preliminar |
| B08-T06 | Testar autorização e ciclo completo de publicação | 14 | Revisão técnica preliminar |
| **Total** | | **76 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Depende de F04/F05 e B06. Hospedagem web e backend compartilhado ainda dependem de contratação e volume.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **76 h**. Estimativa anterior: 56 h.
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
Publicar uma aula válida a disponibiliza na ordem correta; usuário sem permissão não consegue publicar por chamada direta.
