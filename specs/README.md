# Especificações e validação

O catálogo contém 55 features B/A/M/C/E/N/G/EV/P/L/R/GM e sete atividades
compartilhadas F. As atividades F01 e F02 têm mínimo de 40 h cada; as demais
horas são apenas propostas pendentes de avaliação.

As distribuições mecânicas iniciais foram substituídas por uma revisão técnica
por tarefa nas 53 features estimáveis e nas sete atividades de fundação.
As estimativas permanecem preliminares e precisam de revisão técnica.
G02 recebeu estimativa conservadora de 250 h / R$ 50.000 em 17/11/2026
por solicitação do vendedor, para até três conectores oficiais viáveis.
Consulte `REVISAO-TECNICA.md` para resultados e limitações.

A04 acrescenta login com Facebook como opcional independente de 32 h / R$ 6.400,
com jornadas Android/iOS/web. Não foi incluído nos presets; os valores dos planos
permanecem iguais. Consultar `A04-entrar-com-facebook.md`.

Escopo confirmado em 17/11/2026: Android, iOS e web para alunos desde o Essencial,
além do painel administrativo web. Consulte `plataformas-entrega.md`.
O impacto da web dos alunos em esforço, valores e prazo ainda requer revisão;
as estimativas existentes foram mantidas, não revalidadas para esse escopo.

O HTML usa as 55 features do catálogo como opções de orçamento. A fundação
é incluída uma vez, com 522 h após o detalhamento genérico de ambientes e pipelines. O valor exibido
é uma referência de implantação de R$ 200/h, não um preço de venda aprovado
nem custo interno. Custos operacionais permanecem separados e não cotados.
G02 é selecionável na simulação, sem mudar os presets; a execução das integrações
depende de validação por rede. Os cards legados não são migrados automaticamente
para equivalentes que tenham escopo diferente.

Para atualizar o catálogo incorporado ao HTML após editar especificações,
execute `python3 specs/gerar_catalogo.py`. O script não sobrescreve
especificações existentes. Revise manualmente os dados de dependências e
operação usados pelo script quando esses campos mudarem.

A escolha de fornecedores acontece em F02. F05 prepara ambientes e F06 configura
versionamento e pipelines nos serviços aprovados. A evolução do simulador mensal
tem spec separada em `configurador-custos-operacionais.md`, sem horas adicionadas
automaticamente ao orçamento da plataforma.
