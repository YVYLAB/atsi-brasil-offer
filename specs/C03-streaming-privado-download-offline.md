# C03 — Streaming privado + download offline

**Status:** rascunho não validado. Horas de referência do catálogo: 166 h.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
Vídeos privados e downloads para reprodução offline controlada no app.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| C03-T01A | Definir ingestão e autorização de vídeo online | 8 | Revisão técnica preliminar |
| C03-T01B | Implementar upload e associação no painel | 14 | Revisão técnica preliminar |
| C03-T01C | Processar estados e callbacks do vídeo online | 10 | Revisão técnica preliminar |
| C03-T01D | Gerar autorização e verificar direitos de acesso | 12 | Revisão técnica preliminar |
| C03-T01E | Integrar player online e estados de falha | 14 | Revisão técnica preliminar |
| C03-T01F | Testar autorização e rede Android/iOS online | 18 | Revisão técnica preliminar |
| C03-T01G | Documentar limites e consumo do vídeo online | 4 | Revisão técnica preliminar |
| C03-T02 | Validar viabilidade do download no Expo e políticas de uso | 12 | Revisão técnica preliminar |
| C03-T03 | Implementar fila, pausa, retomada e cancelamento de downloads | 24 | Revisão técnica preliminar |
| C03-T04 | Gerenciar arquivos, espaço local e remoção por usuário | 16 | Revisão técnica preliminar |
| C03-T05 | Definir e implementar expiração e revogação possível | 18 | Revisão técnica preliminar |
| C03-T06 | Implementar reprodução local e retomada offline | 16 | Revisão técnica preliminar |
| C03-T07 | Sincronizar progresso com resolução de eventos repetidos | 14 | Revisão técnica preliminar |
| C03-T08 | Testar rede interrompida, pouco espaço, logout e Android/iOS | 28 | Revisão técnica preliminar |
| **Total** | | **208 h** | **Aprovação pendente** |

## Dependências e riscos
Substitui C02, incluindo as mesmas 80 h online, sem somar C02 novamente.
Depende de B02/B06/B07 e da capacidade de reprodução local na arquitetura Expo
escolhida. Revogação imediata não é garantida em dispositivo desconectado;
expiração offline exige política explícita. DRM avançado não está incluído.


## Custos esperados
Referência de implantação do catálogo: R$ 33.200. Não é preço comercial aprovado.
Operação: Cloudflare Stream + armazenamento do app — Mesma tabela do Stream: US$ 5/1.000 min armazenados + US$ 1/1.000 min entregues ou baixados. Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **208 h**. Estimativa anterior: 166 h.
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
Download interrompido pode ser retomado sem arquivo corrompido; logout e expiração obedecem à política possível, e reprodução offline não é prometida como DRM inviolável.
