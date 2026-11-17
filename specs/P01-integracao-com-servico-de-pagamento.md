# P01 — Integração com serviço de pagamento

**Status:** rascunho não validado. Horas de referência do catálogo: 72 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Conectar gateway web, criar pedidos, reconciliar pagamentos e webhooks.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| P01-T01 | Selecionar estratégia web e revisar fronteira com regras de lojas | 10 | Revisão técnica preliminar |
| P01-T02 | Modelar pedidos, estados e referências de pagamento | 12 | Revisão técnica preliminar |
| P01-T03 | Integrar criação de cobrança e checkout do provedor | 16 | Revisão técnica preliminar |
| P01-T04 | Validar assinatura de webhooks e tratar idempotência | 16 | Revisão técnica preliminar |
| P01-T05 | Implementar conciliação e fluxo básico de estorno | 12 | Revisão técnica preliminar |
| P01-T06 | Testar sandbox, eventos fora de ordem e falhas | 20 | Revisão técnica preliminar |
| **Total** | | **86 h** | **Aprovação pendente** |

## Dependências e riscos
fundação e base aplicáveis; detalhes a validar. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 14.400. Não é preço comercial aprovado.
Operação: Gateway de pagamento — Taxas por transação e eventuais mensalidades do gateway; fornecedor a escolher. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **86 h**. Estimativa anterior: 72 h.
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
Webhook sem assinatura válida não altera pedido; repetição e evento fora de ordem não geram efeitos duplicados.
