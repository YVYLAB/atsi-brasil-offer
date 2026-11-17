# G02 — Encaminhamento multicanal para redes sociais

**Status:** estimativa preliminar conservadora autorizada pelo vendedor em
17/11/2026: **250 h / R$ 50.000**, a R$ 200/h. Selecionável na simulação.
Não é medição histórica nem garantia de cobertura de qualquer rede ou limite
máximo de esforço. A execução dos conectores depende de viabilidade oficial.

## Descrição e funcionamento
Configurar mensagens e conteúdo para distribuição a múltiplos grupos e canais
de diferentes redes sociais no mesmo agendamento. Escopo ampliado pelo usuário
em 17/11/2026; não limitado ao WhatsApp.

Uma tela administrativa centraliza:
- Origem do conteúdo: mensagem manual ou conteúdo autorizado da plataforma.
- Texto, link e, quando suportado, mídia, com prévia/adaptação por destino.
- Seleção de múltiplas redes, contas e grupos/canais autorizados.
- Um envio imediato ou agendamento comum aos destinos selecionados.
- Acompanhamento separado por destino: aguardando, enviado, falhou ou bloqueado.

WhatsApp, Telegram, Discord e outras redes são exemplos a avaliar, não
integrações já disponíveis. Grupo, canal e página não são destinos equivalentes:
cada conector só pode oferecer os tipos de destino permitidos oficialmente.
Premissa da estimativa: até três conectores oficiais viáveis, uma conta por rede,
mensagens de texto/link e mídia simples quando suportada, um ciclo de homologação
e volume inicial a definir. Não equivale a integrar todas as redes.

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.
Não inclui captura irrestrita de conversas, encaminhamento entre contas de terceiros,
scraping ou automação por navegador para contornar as APIs. Conteúdo e destinos
devem ser autorizados; consentimento, privacidade e política antispam são obrigatórios.

## Tarefas para validação
| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| G02-T01 | Validar até três redes, APIs, destinos permitidos e requisitos de envio | 20 | Revisão técnica preliminar |
| G02-T02 | Modelar campanhas, contas, destinos e permissões administrativas | 24 | Revisão técnica preliminar |
| G02-T03 | Construir tela administrativa de mensagem, destinos e agendamento | 30 | Revisão técnica preliminar |
| G02-T04 | Implementar até três conectores oficiais viáveis e configuração de credenciais | 54 | Revisão técnica preliminar |
| G02-T05 | Implementar fila, agendamento, concorrência e limites por rede | 30 | Revisão técnica preliminar |
| G02-T06 | Tratar idempotência, retentativas e status independente por destino | 24 | Revisão técnica preliminar |
| G02-T07 | Adaptar conteúdo, validar formatos e mostrar prévia por destino | 18 | Revisão técnica preliminar |
| G02-T08 | Proteger segredos, revogar acessos e registrar auditoria dos envios | 16 | Revisão técnica preliminar |
| G02-T09 | Testar integração, falhas parciais, bloqueios e homologar o fluxo multicanal | 34 | Revisão técnica preliminar |
| **Total** | | **250 h** | **Estimativa conservadora preliminar** |

## Dependências e riscos
Validação técnica e elegibilidade oficial de cada rede e destino.
Validar regras de negócio, privacidade, plataformas e limites de cada fornecedor.
Não utilizar automação não oficial nem prometer integração antes da validação.

## Marco de viabilidade obrigatório
Antes de executar cada conector, verificar documentação oficial de cada rede,
elegibilidade da conta e do parceiro, permissões para os tipos de destino,
consentimento, limites de frequência, formatos e tarifas. Registrar matriz de
capacidade e evidências por conector. Destinos sem suporte permanecem bloqueados;
usar alternativa por links G01 quando aplicável ou excluir o conector do escopo.
Sem essas evidências, não executar nem prometer o conector. A estimativa numérica
foi autorizada para a simulação, não substitui a validação técnica das redes.
Se uma rede não for elegível, revisar o destino, o conector e o escopo com a ATSI;
não contornar restrições com automação não oficial. Novas redes, formatos especiais,
alto volume ou múltiplas contas podem exigir revisão de esforço.
Um agendamento comum dispara trabalhos independentes; não garante entrega no
mesmo instante nem transação atômica entre redes. Falha em um destino não deve
reenviar aos destinos concluídos. Prever idempotência, retentativas limitadas,
revogação de credenciais e trilha de auditoria, sem expor segredos.

## Cenário mínimo específico de aceite
A opção pode ser selecionada na simulação por 250 h / R$ 50.000, sem integrar os
presets automaticamente. O configurador sinaliza a validação técnica por rede.
O mockup permite visualizar uma configuração multicanal administrativa, com
mensagem, múltiplos destinos e agendamento, sem conectar contas nem enviar.
Na implementação futura, validar envio autorizado a pelo menos dois destinos
de redes distintas no mesmo agendamento e status independente por destino;
destino indisponível deve ser bloqueado com explicação.

## Custos esperados
Implantação: **R$ 50.000**, com 250 h de esforço conservador preliminar.
Operação: APIs oficiais das redes / parceiros autorizados — SOB COTAÇÃO:
cobrança, limites e elegibilidade devem ser confirmados por integração.
Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.
