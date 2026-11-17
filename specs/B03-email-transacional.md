# B03 — E-mail transacional

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 16 h.

## Escopo e funcionamento
Integrar serviço para mensagens transacionais, inclusive recuperação, e configurar domínio autenticado. Campanhas promocionais e convites de evento não estão incluídos.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B03-T01 | Configurar domínio, DNS e autenticação do remetente | 4 | Revisão técnica preliminar |
| B03-T02 | Integrar envio transacional com credenciais protegidas | 6 | Revisão técnica preliminar |
| B03-T03 | Preparar modelos e links seguros de recuperação | 4 | Revisão técnica preliminar |
| B03-T04 | Tratar falha, limites e rastreabilidade sem expor dados | 4 | Revisão técnica preliminar |
| B03-T05 | Validar entrega e documentar configuração operacional | 6 | Revisão técnica preliminar |
| **Total** | | **24 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Exige acesso a DNS e provedor aprovado em F02. Serviços citados como referência
não são escolhas fechadas. O custo é compartilhado por plano/uso e não por feature.
O catálogo do configurador já contém o card B03.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **24 h**. Estimativa anterior: 16 h.
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
Mensagem transacional usa remetente autenticado e link correto; falha de envio é observável sem registrar segredos.

## Configuração genérica do serviço escolhido
As 24 h já previstas cobrem uma integração transacional de referência:
configurar conta e acesso, credenciais por ambiente, domínio remetente e
SPF/DKIM/DMARC conforme provedor; integrar envio, limites, falhas e supressões
básicas disponíveis no serviço. Entregar instruções operacionais e validar
mensagem de teste sem usar destinatários reais sem autorização.

Opt-in promocional não é requisito para toda comunicação essencial; a base legal
e o conteúdo precisam ser validados. Campanhas e segmentação de marketing não
fazem parte de B03 nem são habilitadas pela simples escolha de plano do fornecedor.
Implementações próprias de listas, campanhas, automações ou múltiplos provedores
exigem escopo adicional, sem reutilizar franquias transacionais como marketing.
Sem aumento de horas nesta atualização; revisar esforço se a arquitetura escolher
serviços sem recursos nativos equivalentes.
