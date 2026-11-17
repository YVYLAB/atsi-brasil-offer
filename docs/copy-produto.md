# Copy de produto da apresentação ATSI+

`product-copy.js` concentra a apresentação das 54 funcionalidades, das seções
e das sete atividades de preparação. É carregado localmente pelo `home.html`,
sem servidor ou dependências adicionais.

Cada funcionalidade tem título comercial, descrição, benefícios e escopo em
linguagem de produto. Cards e legendas usam a mesma descrição; o popup apresenta
os benefícios, a composição da entrega e o investimento vigente.

## Direção editorial

- Mostrar o que o recurso oferece ao aluno, à equipe ou ao negócio da ATSI.
- Usar frases claras, verbos de ação e benefícios específicos.
- Evitar tom de relatório técnico, reprovação comercial ou auditoria.
- Não exibir caminhos de arquivos, documentos internos ou nomes de fornecedores
  como se a arquitetura já tivesse sido contratada.
- Explicar limites relevantes como composição da entrega: vídeo online/offline,
  vitrines versus bibliotecas, inscrições versus QR/check-in, fontes autorizadas
  de IA, consumo separado, permissões das redes e regras por canal de pagamento.
- Manter a identificação de prévia conceitual e dados de exemplo. Os mockups
  apresentam o produto proposto, não operações já implementadas.

## Dados preservados

Especificações técnicas permanecem em `specs/`, com seus critérios, tarefas e
pendências internas. `specs/gerar_catalogo.py` continua sendo a fonte das
estimativas; a geração não sobrescreve a copy comercial.

IDs, horas, preços, presets e regras de promoção não mudam com a copy.
Os snapshots financeiros mantêm os títulos técnicos originais para não invalidar
ofertas históricas por uma alteração apenas editorial. A interface apresenta
os títulos comerciais.

Os testes verificam cobertura dos 54 recursos, conteúdo comercial dos popups,
ausência de referências internas na apresentação, cálculos e responsividade.
Painéis de desconto se sobrepõem ao topo dos cards elegíveis sem cobrir os
controles, com preço de tabela, preço final, percentual e economia em reais.
