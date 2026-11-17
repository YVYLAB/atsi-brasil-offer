# F06 — Versionamento, pipelines, deploy e publicação

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 40 h.

## Escopo e premissas
Configurar versionamento e entrega automatizada da plataforma nos fornecedores
aprovados em F02, incluindo painel, backend quando aplicável e app mobile.
Aprovação das lojas não é garantida; taxas e mensalidades não estão incluídas.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| F06-T01 | Configurar assinatura e credenciais Android/iOS | 10 | Revisão técnica preliminar |
| F06-T02 | Configurar pipelines de validação, testes, builds e artefatos | 12 | Revisão técnica preliminar |
| F06-T03 | Distribuir builds internos e validar instalação | 10 | Revisão técnica preliminar |
| F06-T04 | Preparar metadados, privacidade e submissões | 12 | Revisão técnica preliminar |
| F06-T05 | Executar submissão inicial e documentar publicação | 10 | Revisão técnica preliminar |
| F06-T06 | Configurar organização, repositórios, papéis, revisão e proteção de branches | 8 | Revisão técnica preliminar |
| F06-T07 | Configurar deploy de homologação do painel e serviços nos fornecedores aprovados | 10 | Revisão técnica preliminar |
| F06-T08 | Configurar entrega de produção com aprovação, segredos e migrações controladas | 10 | Revisão técnica preliminar |
| F06-T09 | Validar falha de pipeline, rollback e documentar procedimento de release | 8 | Revisão técnica preliminar |
| **Total** | | **90 h** | **Aprovação pendente** |

## Dependências e riscos
Depende de F03, credenciais e contas Apple/Google. Prazos de revisão das lojas são externos.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **52 h**. Estimativa anterior: 40 h.
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
Builds assinados são instalados nos ambientes de teste; submissões e pendências das lojas são registradas sem garantir aprovação.

## Atualização de entrega — escopo genérico
**Estimativa vigente: 90 h**, substituindo as 52 h anteriores (+38 h).
Os 38 h adicionais cobrem versionamento, deploy web/backend, aprovação e rollback
antes não explicitados, mais 2 h de ajuste no pipeline de validação. As tarefas
anteriores de build e publicação não são cobradas novamente.

F02 escolhe fornecedores e fluxos; F05 prepara os ambientes; F06 conecta o código
aos ambientes por pipelines. Configurar permissões por papel, revisão de mudanças
e proteção de branches conforme capacidade do plano aprovado.
Usar credenciais de menor privilégio por ambiente, sem segredos no repositório.
Migrar banco por mecanismo controlado, sem presumir rollback destrutivo de dados:
definir quando restaurar, corrigir por nova migração ou reverter somente aplicação.

### Aceite adicional
- Repositórios e responsáveis registrados; alteração protegida exige o fluxo aprovado.
- Mudança de teste executa verificações e bloqueia deploy quando houver falha.
- Pipeline entrega versão identificável em homologação e executa verificação básica.
- Produção exige autorização definida e não usa credenciais de homologação.
- Procedimento de rollback é ensaiado em ambiente seguro e possui evidência.
- Logs e artefatos têm retenção definida; custos de CI são separados da hospedagem.

Premissa: um fluxo de entrega de referência por componente (painel, backend
quando existir e mobile), sem migração de legado ou estratégias avançadas de
deploy. Serviço gerenciado pode substituir etapa customizada, sem duplicação.
Build iOS não implica runner macOS no serviço de CI; serviço de build mobile pode
ser separado. Escolha de fornecedor não altera automaticamente horas ou preços.
