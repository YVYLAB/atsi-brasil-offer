# B02 — Login, logout e recuperação

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 28 h.

## Escopo e funcionamento
Permitir entrada e saída por e-mail/senha, sessão protegida e recuperação. MFA e provedores sociais são opcionais separados.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B02-T01 | Configurar login e validação de credenciais no provedor | 6 | Revisão técnica preliminar |
| B02-T02 | Implementar sessão, renovação, expiração e logout | 8 | Revisão técnica preliminar |
| B02-T03 | Implementar recuperação e deep link de redefinição | 8 | Revisão técnica preliminar |
| B02-T04 | Construir telas, erros e proteção contra enumeração | 8 | Revisão técnica preliminar |
| B02-T05 | Testar sessão expirada, recuperação e isolamento de usuários | 10 | Revisão técnica preliminar |
| **Total** | | **40 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Depende da fundação e de B03 para e-mail transacional. Auth e envio consomem planos compartilhados; limites e segurança dependem da configuração.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **40 h**. Estimativa anterior: 28 h.
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
Sessão expirada não permite operação protegida; link de recuperação inválido ou expirado é rejeitado, sem revelar se um e-mail existe.
