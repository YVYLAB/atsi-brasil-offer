# B04 — Perfil privado do cliente

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 32 h.

## Escopo e funcionamento
Permitir ao usuário gerenciar foto, nome, e-mail verificado e senha. Perfis públicos e pesquisa de usuários são opcionais separados.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B04-T01 | Modelar perfil privado e políticas de leitura/alteração | 6 | Revisão técnica preliminar |
| B04-T02 | Implementar foto com tipo, tamanho e autorização | 8 | Revisão técnica preliminar |
| B04-T03 | Implementar alteração de nome e e-mail com verificação | 8 | Revisão técnica preliminar |
| B04-T04 | Integrar gestão de senha e reautenticação necessária | 6 | Revisão técnica preliminar |
| B04-T05 | Construir telas e testar privacidade, falhas e validações | 12 | Revisão técnica preliminar |
| **Total** | | **40 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Depende de B02, B03 e fundação. Banco e armazenamento são compartilhados; serviços e custos dependem do volume e arquitetura escolhida.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **40 h**. Estimativa anterior: 32 h.
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
Usuário altera somente o próprio perfil; e-mail novo exige verificação e arquivo inválido não é aceito como foto.
