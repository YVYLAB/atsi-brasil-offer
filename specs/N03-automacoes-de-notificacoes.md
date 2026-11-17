# N03 — Automações de notificações

**Status:** rascunho não validado. Horas de referência do catálogo: 52 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Disparar mensagens automaticamente por regras e agendamento.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| N03-T01 | Definir gatilhos, agenda, fuso e regras dos fluxos | 8 | Revisão técnica preliminar |
| N03-T02 | Implementar processamento agendado e estado do fluxo | 14 | Revisão técnica preliminar |
| N03-T03 | Adicionar idempotência, retentativa e cancelamento | 12 | Revisão técnica preliminar |
| N03-T04 | Construir configuração administrativa e histórico | 12 | Revisão técnica preliminar |
| N03-T05 | Testar reprocessamento, falhas e limites do serviço | 14 | Revisão técnica preliminar |
| **Total** | | **60 h** | **Aprovação pendente** |

## Dependências e riscos
N01 (push básico). Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 10.400. Não é preço comercial aprovado.
Operação: Supabase + push/cron — Processamento e jobs consumidos; custos por volume/fornecedor. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **60 h**. Estimativa anterior: 52 h.
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
Reexecutar job não repete ação já concluída; cancelar fluxo impede novos disparos pendentes conforme estado.
