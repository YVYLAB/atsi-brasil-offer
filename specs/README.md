# Especificações e validação

O catálogo contém 54 features B/A/M/C/E/N/G/EV/P/L/R/GM e sete atividades
compartilhadas F. As atividades F01 e F02 têm mínimo de 40 h cada; as demais
horas são apenas propostas pendentes de avaliação.

As distribuições mecânicas iniciais foram substituídas por uma revisão técnica
por tarefa nas 53 features estimáveis e nas sete atividades de fundação.
As estimativas permanecem preliminares e precisam de aprovação; G02 continua
sob cotação. Consulte `REVISAO-TECNICA.md` para resultados e limitações.

O HTML usa as 54 features do catálogo como opções de orçamento. A fundação
é incluída uma vez, com 522 h após o detalhamento genérico de ambientes e pipelines. O valor exibido
é uma referência de implantação de R$ 200/h, não um preço de venda aprovado
nem custo interno. Custos operacionais permanecem separados e não cotados.
G02 está indisponível para contratação; as estimativas continuam pendentes
de revisão técnica e comercial. Os cards legados não são migrados automaticamente
para equivalentes que tenham escopo diferente.

Para atualizar o catálogo incorporado ao HTML após editar especificações,
execute `python3 specs/gerar_catalogo.py`. O script não sobrescreve
especificações existentes. Revise manualmente os dados de dependências e
operação usados pelo script quando esses campos mudarem.

A escolha de fornecedores acontece em F02. F05 prepara ambientes e F06 configura
versionamento e pipelines nos serviços aprovados. A evolução do simulador mensal
tem spec separada em `configurador-custos-operacionais.md`, sem horas adicionadas
automaticamente ao orçamento da plataforma.
