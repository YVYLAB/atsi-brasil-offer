# B01 — Mural inicial: cursos em destaque

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 26 h.

## Escopo e funcionamento
Exibir cursos em destaque, banners de capa e acesso ao catálogo. O painel fornece os destaques. E-books, eventos e promoções no mural são opcionais separados (M01–M03).

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| B01-T01 | Definir contrato de destaques e disponibilidade dos cursos | 4 | Revisão técnica preliminar |
| B01-T02 | Consultar e paginar destaques publicados com autorização | 6 | Revisão técnica preliminar |
| B01-T03 | Construir mural, capas e navegação ao catálogo | 10 | Revisão técnica preliminar |
| B01-T04 | Tratar carregamento, vazio, imagem ausente e falha de rede | 4 | Revisão técnica preliminar |
| B01-T05 | Testar publicação, acesso e navegação Android/iOS | 8 | Revisão técnica preliminar |
| **Total** | | **32 h** | **Aprovação pendente** |

## Dependências, custos e riscos
Depende da fundação, catálogo B06 e administração B08. Backend compartilhado; consumo e eventual armazenamento de capas dependem do uso. O mural legado do configurador tem escopo e horas diferentes e não equivale exatamente a B01.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **32 h**. Estimativa anterior: 26 h.
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
Somente cursos publicados e elegíveis aparecem; destaque navega ao curso correto, e vitrines M01–M03 não são embutidas como entrega gratuita de B01.
