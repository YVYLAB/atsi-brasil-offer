# C06 — Geração de testes com inteligência artificial

**Status:** rascunho não validado. Horas de referência do catálogo: 56 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
IA gera sugestões de testes a partir de texto do curso, com revisão humana.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| C06-T01 | Definir fontes autorizadas, formato e política de geração | 8 | Revisão técnica preliminar |
| C06-T02 | Preparar ingestão textual e limites de conteúdo | 10 | Revisão técnica preliminar |
| C06-T03 | Integrar provedor com saída estruturada validada | 12 | Revisão técnica preliminar |
| C06-T04 | Construir revisão, edição e publicação humana no quiz | 12 | Revisão técnica preliminar |
| C06-T05 | Implementar limites de uso, erros e registro de consumo operacional | 8 | Revisão técnica preliminar |
| C06-T06 | Testar respostas inválidas, segurança e qualidade amostral | 14 | Revisão técnica preliminar |
| **Total** | | **64 h** | **Aprovação pendente** |

## Dependências e riscos
C05 (quizzes) e fonte autorizada. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 11.200. Não é preço comercial aprovado.
Operação: API de IA + transcrição/arquivo — Variável por tokens do modelo; transcrição/ingestão pode ter custo adicional. Custos compartilhados não devem ser cobrados por feature;
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
Saída inválida do modelo não vira quiz publicado; toda sugestão exige revisão humana antes de entrar em C05.
