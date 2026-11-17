# Correspondência dos mockups com as features

## Escopo da revisão
54 composições específicas em `specificMockContent()` no `home.html`, mantendo
os nomes e IDs do catálogo. São ilustrações com dados fictícios, não telas
funcionais ou promessa de implementação idêntica.
Nenhuma alteração de horas, preços, seleção ou dependências.

## Adequações
| Grupo / IDs | Representação |
|---|---|
| B01 | Cursos, progresso e vitrines M01/M02/M03 condicionadas à seleção |
| B02 | Login, senha, recuperação e indicação de sessão |
| B03 | Exemplo de mensagem transacional, sem inventar caixa de e-mail no app |
| B04 | Perfil privado, foto, e-mail verificado, senha e complementos contratados |
| B05 | Controle de consentimento e revogação, separado de comunicações essenciais |
| B06/B07 | Catálogo, estrutura de módulos/aulas e progresso individual |
| B08 | Gestão administrativa com publicação e rascunho |
| A01/A02/A03 | Segundo fator e acesso por provedor, com fluxos distintos |
| M01/M02/M03 | Cards de vitrine, sem confundir com biblioteca, inscrições ou checkout |
| C01/C02/C03 | YouTube, privado online e offline, com limitações explícitas |
| C04/C05 | PDF/verificação de certificado e quiz com alternativas |
| C06/C07 | Geração com revisão humana e conversa com fonte autorizada |
| C08/C09 | Comentário público por aula e satisfação, distintos de chat privado/quiz |
| E01 | Pesquisa, capa e arquivo da biblioteca |
| N01 | Push do dispositivo, sem adicionar uma caixa persistente não especificada |
| N02/N03 | Segmentação e automação administrativas com etapas e rascunho |
| G01/G02 | Convites oficiais do WhatsApp versus automação sob validação |
| G03/G04 | Feed interno e moderação versus conversa privada com bloqueio/denúncia |
| G05/G06 | Perfil público opt-in e busca somente de perfis publicáveis |
| EV01 | Evento/inscrição com complementos EV02–EV04 apenas se contratados |
| EV02/EV03/EV04 | QR da inscrição, convite de e-mail e câmera/check-in distintos |
| P01–P04 | Pedido, assinatura, compra de curso e ingresso, sem preço fictício |
| P05–P07 | Exemplos de acesso permitido e restrito para cada tipo de conteúdo |
| L01 | Ator, ação, momento e registro da auditoria |
| R01–R05 | Visualização, conclusão, satisfação, ativos e presença com unidades próprias |
| GM01–GM04 | Extrato, presença, ranking e posição no perfil com regras ilustrativas |

As telas administrativas usam identificação e navegação de gestão. São mostradas
no mesmo dispositivo por conveniência da apresentação; isso não muda a definição
arquitetural de painel web. QR é padrão decorativo não utilizável. Números de
relatórios/pontos são demonstrativos e não métricas reais.

## Validação
Testes verificam cobertura dos 54 IDs por composição específica, marcadores de
conteúdo de exemplos, contexto administrativo, seleção versus visualização,
mural e eventos condicionais e preservação do orçamento.
`python3 -m unittest discover -s tests -v`

Não substitui revisão de desenho com ATSI nem validação de acessibilidade de um
aplicativo real. Os critérios das specs serão homologados na implementação
futura; o protótipo não executa autenticação, downloads, envio, pagamentos ou IA.
