# F03 — Shell mobile e design system

**Status:** proposta inicial; tarefas e horas pendentes de validação. Referência: 44 h.

## Escopo e premissas
Criar fundação do app Expo/React Native, navegação e componentes reutilizáveis. Não inclui telas completas de features nem publicação.

**Atualização de escopo — 17/11/2026:** a entrega inclui Android, iOS e versão
web para alunos desde o Essencial, além do painel administrativo web separado.
Esta spec deve contemplar também a fundação da experiência web dos alunos;
a tecnologia e o impacto nas tarefas/horas abaixo ainda exigem revisão.
Consulte `plataformas-entrega.md`. As 56 h atuais não são uma validação de
cobertura da versão web.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| F03-T01 | Inicializar Expo/TypeScript e configuração por ambiente | 8 | Revisão técnica preliminar |
| F03-T02 | Estruturar navegação, deep links e rotas protegidas | 12 | Revisão técnica preliminar |
| F03-T03 | Implementar tokens, componentes e layouts reutilizáveis | 16 | Revisão técnica preliminar |
| F03-T04 | Preparar cliente de API, erros globais e estado de sessão | 8 | Revisão técnica preliminar |
| F03-T05 | Validar shell em Android/iOS e acessibilidade básica | 12 | Revisão técnica preliminar |
| **Total** | | **56 h** | **Aprovação pendente** |

## Dependências e riscos
Depende de F01 e F02. Acesso a dispositivos e requisitos de acessibilidade podem alterar o esforço.


## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **56 h**. Estimativa anterior: 44 h.
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
O shell abre em Android/iOS, preserva navegação e mostra estados globais de erro sem acesso a rotas protegidas por sessão inválida.

O mesmo aceite deve ser detalhado para o navegador, com layout responsivo e
sessão protegida, conforme `plataformas-entrega.md`; esforço ainda não revisado.
