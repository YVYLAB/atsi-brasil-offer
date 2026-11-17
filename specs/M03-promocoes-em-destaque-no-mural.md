# M03 — Promoções em destaque no mural

**Status:** rascunho não validado. Horas de referência do catálogo: 12 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Banners e chamadas promocionais com programação e link de destino.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| M03-T01 | Definir vigência, destino e regras de exibição do banner | 4 | Revisão técnica preliminar |
| M03-T02 | Implementar cadastro e programação no painel | 6 | Revisão técnica preliminar |
| M03-T03 | Exibir banner conforme vigência e tratar links | 4 | Revisão técnica preliminar |
| M03-T04 | Testar limites de data e fallback de imagem | 4 | Revisão técnica preliminar |
| **Total** | | **18 h** | **Aprovação pendente** |

## Dependências e riscos
fundação e base aplicáveis; detalhes a validar. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.


## Custos esperados
Referência de implantação do catálogo: R$ 2.400. Não é preço comercial aprovado.
Operação: Supabase + R2 (banners) — Dados dentro do backend; armazenamento/leituras em R2 conforme uso. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **18 h**. Estimativa anterior: 12 h.
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
Banner só aparece durante sua vigência no fuso definido e não implementa checkout ou motor de cupons.
