# PDF da oferta

O botão **Gerar PDF Oferta**, no final de `home.html`, baixa um PDF binário.
Não depende de impressão pelo navegador, servidor ou acesso à rede. A biblioteca
jsPDF 4.2.1 (MIT) acompanha o projeto em `vendor/jspdf/`.

## Conteúdo

- Cliente, produto, desenvolvedora, data/hora em Brasília e configuração escolhida.
- Plataformas incluídas, total comercial, descontos e esforço total.
- Período da campanha e situação no momento da geração, sem renovar a validade.
- Composição financeira com preparação, funcionalidades selecionadas e cortesia.
- As sete entregas de preparação, cobradas uma vez, com suas tarefas e horas.
- Cada funcionalidade selecionada com ID e **título técnico do arquivo de
  especificação**, descrição, tarefas, IDs das tarefas, horas, escopo, condições
  e critério de entrega.
- Valor de tabela, desconto atribuído e valor final de cada entrega.
- Curso administrativo de cortesia, sem inventar carga horária.
- Manutenção mensal e franquia, separadas da implantação; consumo de IA e horas
  excedentes seguem as condições já apresentadas na página.
- Base do plano, adicional operacional e total mensal, sem desconto promocional.
  Snapshot dos usuários ativos, pico hipotético, consumo de vídeo/downloads,
  câmbio de simulação, tarifas por serviço, fontes e exclusões. Ver
  [custos operacionais](custos-operacionais.md).
- Explicação do impacto dos serviços de streaming abaixo da mensalidade.
  Com YouTube, adicional zerado e infraestrutura compartilhada coberta pela
  base; custos de referência identificados separadamente, sem dupla cobrança.
  A explicação introdutória usa os mesmos cinco parágrafos em linguagem simples
  da página, com manutenção, serviços/vídeos, regra YouTube, simulação sem cobrança
  automática e IA separada. A composição técnica permanece na seção de detalhes.

Horas são esforço de uma pessoa por tarefa, não prazos corridos individuais.
O prazo equivalente mantém a capacidade vigente de 352 h/mês para duas pessoas.
Não são criados preços por tarefa: o valor comercial pertence à entrega completa.

## Dados e consistência

`specs/gerar_catalogo.py` incorpora `technicalTitle`, `taskDetails` (ID, nome e
horas), escopo e condições das especificações. Os títulos comerciais da página
e os títulos originais dos snapshots financeiros permanecem separados.

`buildOfferPDFModel()` captura a configuração e a validade da promoção em um
mesmo instante. Inclui também os requisitos acrescentados automaticamente.
Antes da geração, verifica a estratégia única de vídeo, dependências, somas
das tarefas, preços e descontos. A interface é atualizada com esse mesmo instante.
Não muda seleção, estimativas, manutenção, preços ou validade da campanha.
O adicional operacional é calculado com os mesmos parâmetros válidos do resumo;
`support.priceCents` mantém a base, `support.operations` congela o cenário e
`support.totalCents` deve fechar com base + parcelas operacionais. O documento
não promove hipóteses de dimensionamento a garantias de capacidade.

O desconto de pacote é rateado proporcionalmente entre as entregas do plano,
inclusive a preparação quando participante da campanha v2. O arredondamento
usa o método dos maiores restos, em centavos, com desempate pela ordem dos itens.
A soma das parcelas corresponde exatamente ao desconto do pacote.

Opcionais adicionais mantêm o desconto calculado pelo núcleo de promoções,
separado do rateio do plano. Recursos incluídos em qualquer preset continuam
fora do desconto adicional. Ofertas legadas v1 só rateiam entre os opcionais
explicitamente elegíveis; não descontam a preparação.

O PDF não contém hash de liberação, senha, segredos de provedores ou caminhos
de arquivos internos. É um registro estático da oferta configurada, não uma
assinatura eletrônica nem um serviço de autorização comercial.

## Validação

- `python3 -m unittest discover -s tests -v`
- `node tests/test_offer_pdf.js`

São gerados PDFs reais para Essencial, Premium com adicionais, oferta expirada,
e-books com biblioteca, configuração ampla e oferta legada. Quando disponíveis,
`pdfinfo` e `pdftotext` verificam estrutura, paginação, nomes, todas as tarefas,
horas e limites da página. O teste do botão confirma a chamada de download.
O comportamento de salvamento do sistema operacional ainda depende do navegador.
