# B05 — Preferência de marketing

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 12 h.

## Escopo e funcionamento
Registrar escolha e revogação de comunicações promocionais. Não inclui ferramenta de campanhas ou disparos em massa.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B05-T01 | Definir versão do texto, registro e revogação do consentimento | 4 | Revisão técnica preliminar |
| B05-T02 | Persistir escolha com identificação e data | 4 | Revisão técnica preliminar |
| B05-T03 | Implementar controle no perfil e feedback de atualização | 4 | Revisão técnica preliminar |
| B05-T04 | Testar revogação, acesso e evidência da escolha | 4 | Revisão técnica preliminar |
| **Total** | | **16 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Depende de B04 e fundação. Dados usam backend compartilhado; texto, base legal e retenção exigem validação com a ATSI.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **16 h**. Estimativa anterior: 12 h.
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
Aceite e revogação persistem com versão e data; a escolha pode ser consultada sem implicar disparos de campanha.
