# F05 — Banco, API, storage e ambientes

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 28 h.

## Escopo e premissas
Preparar fundação de banco, API, armazenamento e ambientes usando os fornecedores
aprovados em F02. Nomes de produtos citados como referência não são obrigatórios.
Não inclui modelos e regras específicos já contabilizados nas features.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| F05-T01 | Configurar ambientes aprovados, contas, acessos e segredos nos fornecedores escolhidos | 12 | Revisão técnica preliminar |
| F05-T02 | Configurar migrações e acesso ao banco/API | 8 | Revisão técnica preliminar |
| F05-T03 | Estabelecer políticas RLS e isolamento inicial | 8 | Revisão técnica preliminar |
| F05-T04 | Configurar storage, permissões e upload comum | 8 | Revisão técnica preliminar |
| F05-T05 | Configurar monitoramento básico, backup e procedimento de restauração com validação | 12 | Revisão técnica preliminar |
| F05-T06 | Validar isolamento dos ambientes e segurança da fundação | 8 | Revisão técnica preliminar |
| **Total** | | **56 h** | **Aprovação pendente** |

## Dependências e riscos
Depende de F02, contas e credenciais. Custos dos fornecedores são compartilhados e dependem de plano e uso.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **48 h**. Estimativa anterior: 28 h.
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
Migrações reproduzem o ambiente e políticas impedem leitura ou alteração de registros de outro usuário.

## Atualização de ambientes — escopo genérico
**Estimativa vigente: 56 h**, substituindo a revisão anterior de 48 h (+8 h).
As horas adicionais explicitam configuração de acessos/ambientes e validação de
recuperação antes tratadas de forma agregada. Não é uma cobrança extra de toda a
fundação. A escolha dos fornecedores é de F02; esta atividade configura e valida.

- Configurar os ambientes aprovados (desenvolvimento, homologação e produção,
  quando previstos), com isolamento e responsáveis documentados.
- Aplicar menor privilégio, separar segredos e definir rotação de credenciais.
- Disponibilizar serviços, endpoints, domínio/TLS e rede conforme arquitetura.
- Preparar migrações reproduzíveis, permissões de dados e armazenamento.
- Configurar alertas básicos e validar restauração em ambiente seguro.
- Entregar inventário de ambientes, acessos, dependências e procedimento operacional.

Aceite: ambientes e isolamento verificados, serviços acessíveis apenas conforme
permissão, segredos fora do código e evidência de recuperação registrada.
A expressão RLS na tabela significa a política de acesso equivalente aprovada
na arquitetura; não obriga a contratação de um produto.

Premissa de esforço: uma arquitetura de referência, um conjunto de ambientes e
uma configuração básica por serviço. Alta disponibilidade, múltiplas regiões,
migração de legado, auditoria externa e operação contínua exigem escopo próprio.
Mensalidades e consumo de serviços são separados das horas de implantação.
