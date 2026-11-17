# F07 — Homologação integrada e segurança essencial

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 40 h.

## Escopo e premissas
Homologar fluxos integrados da base, segurança essencial e políticas. Testes específicos de cada feature permanecem nas respectivas estimativas; auditoria externa e pentest não estão incluídos.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| F07-T01 | Preparar plano integrado, massa de dados e ambientes de homologação | 10 | Revisão técnica preliminar |
| F07-T02 | Executar jornadas ponta a ponta da base e vídeo escolhido | 16 | Revisão técnica preliminar |
| F07-T03 | Revisar autorização e exposição de dados entre usuários | 10 | Revisão técnica preliminar |
| F07-T04 | Revisar acessibilidade e dispositivos representativos | 10 | Revisão técnica preliminar |
| F07-T05 | Executar ciclo de regressão após correções integradas | 12 | Revisão técnica preliminar |
| F07-T06 | Consolidar aceite, pendências e transferência operacional | 6 | Revisão técnica preliminar |
| **Total** | | **64 h** | **Aprovação pendente** |

## Dependências e riscos
Depende da disponibilidade da base integrada e de responsáveis pela homologação. Correções extensas podem exigir revisão.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **64 h**. Estimativa anterior: 40 h.
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
Os fluxos integrados contratados têm evidência de execução, problemas classificados e aceite ou pendência explícita dos responsáveis.
