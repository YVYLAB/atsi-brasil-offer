# P05 — Controle de acesso de cursos por perfil/assinatura/pagamento

**Status:** rascunho não validado. Horas de referência do catálogo: 68 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Liberar cursos conforme perfil, assinatura, pagamento ou direito de acesso.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| P05-T01 | Definir regras de perfil, compra e assinatura | 10 | Revisão técnica preliminar |
| P05-T02 | Modelar direitos e precedência das regras | 12 | Revisão técnica preliminar |
| P05-T03 | Aplicar autorização no backend de catálogo e aulas | 14 | Revisão técnica preliminar |
| P05-T04 | Integrar autorização de vídeo privado quando aplicável | 10 | Revisão técnica preliminar |
| P05-T05 | Exibir bloqueios e instruções de acesso no app | 10 | Revisão técnica preliminar |
| P05-T06 | Testar expiração, revogação e acesso por URL direta | 20 | Revisão técnica preliminar |
| **Total** | | **76 h** | **Aprovação pendente** |

## Dependências e riscos
B06 e regras de direitos de acesso a definir. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 13.600. Não é preço comercial aprovado.
Operação: Supabase + serviço de vídeo privado — Consultas e assinaturas dentro de cotas; Stream se C02/C03. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **76 h**. Estimativa anterior: 68 h.
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
Acesso direto à aula e ao vídeo verifica direito no servidor; revogação e expiração não dependem apenas da interface.
