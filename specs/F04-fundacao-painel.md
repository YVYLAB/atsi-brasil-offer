# F04 — Fundação do painel e RBAC

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 20 h.

## Escopo e premissas
Preparar estrutura Next.js, navegação e base de permissões administrativas. Não inclui as telas de gestão de B08.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| F04-T01 | Inicializar Next.js, configuração e layout administrativo | 8 | Revisão técnica preliminar |
| F04-T02 | Integrar sessão administrativa e papéis | 8 | Revisão técnica preliminar |
| F04-T03 | Proteger rotas e centralizar autorização no servidor | 8 | Revisão técnica preliminar |
| F04-T04 | Testar matriz de acesso e navegação administrativa | 8 | Revisão técnica preliminar |
| **Total** | | **32 h** | **Aprovação pendente** |

## Dependências e riscos
Depende de F02 e da definição dos papéis administrativos; regras específicas pertencem às respectivas features.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **32 h**. Estimativa anterior: 20 h.
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
Uma conta sem papel administrativo é recusada tanto pela rota quanto pela operação de servidor.
