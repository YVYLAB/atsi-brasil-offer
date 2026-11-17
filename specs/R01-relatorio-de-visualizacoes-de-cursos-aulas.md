# R01 — Relatório de visualizações de cursos/aulas

**Status:** rascunho não validado. Horas de referência do catálogo: 36 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Relatório de visualizações de cursos e aulas por período.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| R01-T01 | Definir o que conta como visualização e fonte do evento | 6 | Revisão técnica preliminar |
| R01-T02 | Instrumentar captura sem duplicar eventos de navegação | 10 | Revisão técnica preliminar |
| R01-T03 | Agregar dados por curso, aula e período | 8 | Revisão técnica preliminar |
| R01-T04 | Construir filtros e visualização administrativa | 8 | Revisão técnica preliminar |
| R01-T05 | Testar contagem, privacidade e desempenho inicial | 12 | Revisão técnica preliminar |
| **Total** | | **44 h** | **Aprovação pendente** |

## Dependências e riscos
telemetria de visualizações a definir. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 7.200. Não é preço comercial aprovado.
Operação: Supabase / eventos de uso — Mais eventos gravados = mais banco/armazenamento; pode exigir analytics. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **44 h**. Estimativa anterior: 36 h.
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
Contagem segue definição de visualização e não soma navegação repetida como eventos distintos sem critério.
