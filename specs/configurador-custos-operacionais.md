# Evolução do configurador — custos operacionais

**Status:** especificação ampla preliminar, parcialmente implementada pelo
recorte de usuários ativos e adicional mensal de 17/11/2026.
Ver `../docs/custos-operacionais.md` para o que realmente funciona e seus limites.
Comparação de fornecedores, importação/persistência e demais entregas desta
spec continuam fora desse recorte. **Horas: a estimar** após
detalhamento da interface e da base de dimensionamento. Não pertence às 54 features
da plataforma ATSI nem deve ser somada automaticamente ao orçamento do aplicativo.

## Objetivo
Comparar custos mensais de serviços de e-mail, versionamento e CI/CD, sem decidir
fornecedores da plataforma. F02 decide a arquitetura; o simulador exibe alternativas
com fonte, data, unidade, condições e incertezas.

## Tarefas e entregáveis a estimar
| ID | Tarefa | Estimativa |
|---|---|---|
| CFG-OPS-01 | Mapear o HTML atual e definir entradas próprias de MAU, volume e câmbio, pois ainda não há módulo completo de dimensionamento | A estimar |
| CFG-OPS-02 | Criar catálogo local versionado de planos, tarifas, franquias e fontes oficiais verificadas | A estimar |
| CFG-OPS-03 | Calcular transacionais por destinatário, franquia mensal, pico diário e excedentes por provedor | A estimar |
| CFG-OPS-04 | Separar marketing por contatos/envios, consentimento, habilitação e faixas sob cotação | A estimar |
| CFG-OPS-05 | Calcular versionamento por assentos, CI por workloads/runners e crédito compartilhado por conta | A estimar |
| CFG-OPS-06 | Tratar arredondamento por job, público/privado, self-hosted, artefatos e cache sem tarifa inventada | A estimar |
| CFG-OPS-07 | Exibir parcelas do fornecedor e da ATSI, rateio, subtotal conhecido e pendências | A estimar |
| CFG-OPS-08 | Construir interface acessível e responsiva, sem afetar seleção ou implantação das features | A estimar |
| CFG-OPS-09 | Definir persistência versionada, restauração, importação e exportação coerentes com o estado real do HTML | A estimar |
| CFG-OPS-10 | Executar cenários determinísticos, testes de limites, ida e volta de dados e regressão dos planos | A estimar |
| CFG-OPS-11 | Documentar fórmulas, limitações, preços e checklist de validação comercial | A estimar |

## Critérios de aceite
- Desconhecido é `sob cotação`, não zero; marketing desabilitado é `não contratado`.
- Crédito de CI pertence à conta, não ao aluno, assento ou repositório.
- Custos mensais não alteram horas ou referência de implantação.
- E-mail e CI são cobrados uma vez no agregado, sem duplicar assinaturas.
- Preços são locais no runtime; câmbio é premissa explícita e editável.
- Infraestrutura ainda não simulada aparece pendente, nunca como já implementada.
- Build mobile externo não gera cobrança fictícia de runner macOS.
- Importação e exportação, quando implementadas, reproduzem o estado mostrado.

## Fora de escopo
Contratar serviços, criar contas reais, provisionar ambientes, executar pipelines
ou mudar a stack. Essas entregas da plataforma pertencem a F05/F06 após F02.
Campanhas reais de marketing não pertencem ao configurador nem à base transacional.

## Referência de requisitos
Documento v8 de custos de e-mail/GitHub apresentado pelo usuário. Os preços e
exemplos precisam de conferência oficial antes de implementação. Não reutilizar
horas antigas desse documento para substituir as specs vigentes da plataforma.
