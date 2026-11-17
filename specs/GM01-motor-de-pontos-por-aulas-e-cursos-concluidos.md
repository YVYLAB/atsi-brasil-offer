# GM01 — Motor de pontos por aulas e cursos concluídos

**Status:** rascunho não validado. Horas de referência do catálogo: 56 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Ganhar pontos por concluir aulas e cursos, com saldo e regras.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| GM01-T01 | Definir eventos elegíveis e restrições das plataformas de vídeo | 8 | Revisão técnica preliminar |
| GM01-T02 | Modelar extrato e regras de pontuação | 10 | Revisão técnica preliminar |
| GM01-T03 | Implementar concessão idempotente e reversão definida | 14 | Revisão técnica preliminar |
| GM01-T04 | Construir configuração administrativa básica | 10 | Revisão técnica preliminar |
| GM01-T05 | Integrar consulta de saldo e atividades | 8 | Revisão técnica preliminar |
| GM01-T06 | Testar repetição, exploração básica e alterações de conteúdo | 14 | Revisão técnica preliminar |
| **Total** | | **64 h** | **Aprovação pendente** |

## Dependências e riscos
B07 e regras de pontuação compatíveis com o provedor de vídeo. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 11.200. Não é preço comercial aprovado.
Operação: Supabase — Gravação de eventos e ranking; banco dentro de cotas inicialmente. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **64 h**. Estimativa anterior: 56 h.
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
Evento repetido concede pontos uma vez; regras não recompensam assistir ao player YouTube em desacordo com políticas.
