# Revisão técnica preliminar — 16/11/2026

> Premissa de equipe atualizada: duas pessoas dedicadas, 22 dias úteis/mês,
> 8 h/dia por pessoa, capacidade equivalente de **352 h/mês**.
> Horas de esforço e valores não mudam. Prazos vigentes: Essencial **2,53 meses**,
> Plus **3,27 meses**, Premium **5,53 meses**. As durações anteriores abaixo
> são históricas para uma pessoa. Paralelismo integral não é garantido:
> dependências e coordenação exigem validação do cronograma.

> Atualização posterior: os números desta revisão inicial são históricos.
> Após explicitar ambientes e pipelines genéricos, F05 passou de 48 para 56 h
> e F06 de 52 para 90 h. Fundação vigente: **522 h**.
> Referências vigentes: Essencial **890 h / R$ 178.000 / 5,06 meses**;
> Plus **1.150 h / R$ 230.000 / 6,53 meses**;
> Premium **1.946 h / R$ 389.200 / 11,06 meses**.
> Fornecedores são decididos em F02; nenhuma infraestrutura real foi criada.

## Resultado e limites

Revisadas 54 features e sete atividades de fundação. As 53 features com horas
numéricas e as sete atividades de fundação receberam decomposição específica.
G02 permanece sob cotação, com tarefas de viabilidade e contratação bloqueada.
Ao todo, o catálogo contém 318 tarefas, incluindo as três de viabilidade G02.
Nenhuma foi executada ou aprovada pelo cliente.

Os rascunhos anteriores de 46 features usavam percentuais uniformes de esforço.
Essa distribuição foi substituída por estimativas por tarefa. As horas
foram ampliadas quando faltavam autorização, estados de erro, integração,
idempotência, revisão ou testes. Não foi aplicada contingência percentual.

As estimativas são avaliação técnica inicial, não dados históricos de velocidade.
Critérios específicos de negócio e cobertura completa de cenários ainda serão
refinados em F01. Valores de fornecedores não foram revalidados nesta revisão.

## Principais alterações

| Item | Antes | Revisado | Motivo |
|---|---:|---:|---|
| F01 | 40 h | 104 h | Requisitos, épicos, specs e tarefas do catálogo completo |
| F02 | 40 h | 120 h | Fluxos, telas, estados, domínio e arquitetura |
| Fundação F01–F07 | 252 h | 476 h | Planejamento e atividades compartilhadas explicitadas |
| Base B01–B08 | 266 h | 340 h | Sessão, validação, publicação, privacidade e testes |
| C01 YouTube | 20 h | 28 h | Política de uso, erros e testes mobile |
| C02 privado | 68 h | 80 h | Ingestão, estados, autorização e testes |
| C03 offline | 166 h | 208 h | Inclui as 80 h de C02, mais downloads e sincronização |
| C07 chat IA | 112 h | 136 h | Isolamento de fontes, qualidade, segurança e operação |

As demais alterações estão nas tabelas e no histórico de cada spec.
As 224 h de F01/F02 são cobradas obrigatoriamente dentro das 476 h da fundação,
uma vez. A estimativa de planejamento considera o catálogo completo; se o
contrato limitar o planejamento somente ao Essencial, deve haver nova revisão,
não uma redução automática ou cobrança implícita pelo restante.

## Referências de implantação após a revisão

Taxa de referência fixa: R$ 200/h. Preço comercial ainda não aprovado.
Prazo equivalente: esforço dividido por 22 dias úteis × 8 h, uma pessoa dedicada.
Não é cronograma contratual; esperas externas e feriados não são modelados.

| Plano | Horas | Referência de implantação | Meses equivalentes |
|---|---:|---:|---:|
| Essencial | 844 | R$ 168.800 | 4,80 |
| Plus | 1.104 | R$ 220.800 | 6,27 |
| Premium | 1.900 | R$ 380.000 | 10,80 |

Planos mantêm as seleções existentes. Fundação é incluída uma vez; C03 substitui
C02. Mensalidades, suporte, tributos e custos externos não integram esses valores.

## Decisões ainda necessárias

- Confirmar escopo de telas e número de ciclos de revisão antes de aprovar F02.
- Confirmar Expo/player/download offline com prova de viabilidade antes de C03.
- Definir política de conclusão, consentimento, retenção e métricas.
- Selecionar estratégia de pagamento por canal. As horas estimam uma integração
  de referência; gateway web não inclui automaticamente Apple/Google IAP.
  Necessidade de implementações adicionais de loja exige nova decomposição.
- Definir provedor e fontes autorizadas para IA. Transcrição automática,
  moderação avançada e DRM não estão implicitamente incluídos.
- Validar a automação WhatsApp oficialmente antes de estimar G02.
- Validar políticas de YouTube para acesso pago e gamificação.

## Fonte de verdade e atualização

As tarefas revisadas em `specs/*.md` são a fonte das horas do HTML.
Execute `python3 specs/gerar_catalogo.py` após revisão. O catálogo original em
`docs/` permanece como histórico. O script `revisar_estimativas.py` registra a
revisão inicial e recusa reaplicação para não sobrescrever trabalho posterior.
