# C02 — Streaming privado na nuvem

**Status:** rascunho não validado. Horas de referência do catálogo: 68 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Upload, processamento, player e controle de acesso a vídeos privados online.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| C02-T01 | Definir ingestão e autorização do vídeo privado | 8 | Revisão técnica preliminar |
| C02-T02 | Implementar upload e associação no painel | 14 | Revisão técnica preliminar |
| C02-T03 | Processar estados e callbacks de preparação do vídeo | 10 | Revisão técnica preliminar |
| C02-T04 | Gerar autorização/token e verificar direito de acesso | 12 | Revisão técnica preliminar |
| C02-T05 | Integrar player, retomada e estados de falha | 14 | Revisão técnica preliminar |
| C02-T06 | Testar expiração, acesso indevido e rede em Android/iOS | 18 | Revisão técnica preliminar |
| C02-T07 | Documentar limites de proteção e consumo operacional | 4 | Revisão técnica preliminar |
| **Total** | | **80 h** | **Aprovação pendente** |

## Dependências e riscos
fundação e base aplicáveis; detalhes a validar. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 13.600. Não é preço comercial aprovado.
Operação: Cloudflare Stream — Armazenamento: US$ 5/1.000 min/mês (blocos); entrega: US$ 1/1.000 min vistos. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **80 h**. Estimativa anterior: 68 h.
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
Vídeo em processamento não é oferecido como pronto; token expirado ou usuário sem direito não obtém autorização válida de reprodução.
