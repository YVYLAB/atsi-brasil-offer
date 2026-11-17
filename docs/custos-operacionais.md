# Adicional operacional por volume

Implementação local em `operational-pricing.js`, usada por `home.html`, exports
e PDF. Modelo `atsi-operations-v2`, tarifas de referência consultadas em
17/11/2026. Não provisiona serviços, não mede acessos e não determina capacidade.

## Política comercial

Decisão do vendedor: acrescer operação à base mensal. Substitui a apresentação
anterior de operação incluída. Bases e franquias preservadas:

| Plano | Base mensal | Trabalho incluído |
|---|---:|---:|
| Essencial | R$ 3.000 | 10 h |
| Plus | R$ 4.000 | 15 h |
| Premium | R$ 5.000 | 20 h |

`total mensal = base do plano + soma dos serviços convertidos em centavos`.
**Exceção comercial posterior: com YouTube (C01), todo o adicional operacional
fica zerado**, independentemente do volume do slider. A base de manutenção
permanece, inclusive em Personalizado originado de Plus/Premium. A infraestrutura
compartilhada continua tendo custo estimado, mas é coberta pela base nesse
cenário, não repassada novamente. Privado/offline mantêm o cálculo anterior.
Há explicação imediatamente abaixo da mensalidade, também no PDF e exports.
Nem a base nem o adicional recebem descontos de implantação.
Usuários/consumo não alteram features, horas, complexidade, prazo ou implantação.
Personalizado preserva a base mensal de origem e considera a estratégia de vídeo
efetivamente selecionada, não o vídeo original do preset.

## Premissas iniciais, não dados observados

- Slider: **100–10.000 usuários ativos no mês**, em passos de 100, inicial 100.
- Pico hipotético: **10%** dos ativos mensais, arredondado para cima.
- Câmbio: **R$ 6/US$**, hipótese editável, sem consulta a cotação em tempo real.
- Vídeo privado: **180 minutos online por usuário/mês**.
- Acervo privado: **100 horas**.
- Offline: **60 minutos de novos downloads adicionais por usuário/mês**,
  somados aos 180 online. Reassistir localmente não é nova entrega. Ajustar
  para zero ou redistribuir online/downloads quando o offline substituir online.
- **4 e-mails transacionais por ativo/mês**, sem campanhas de marketing.
- Um projeto de produção e um de homologação; um assento de deploy web.
- Outros consumos dentro das franquias, sem excedentes presumidos.

Câmbio, proporção simultânea, minutos online, acervo e downloads são editáveis
em “Ajustar premissas”. YouTube desabilita os campos privados; streaming online
desabilita downloads, preservando os valores para eventual retorno ao offline.
Inputs inválidos não entram nos cálculos; há aviso do último valor válido e
restauração ao sair do campo. Somente o cenário válido integra os exports.
Trocar plano preserva usuários e premissas. Recarregar restaura padrões:
**não há persistência ou importação de cenário operacional nesta entrega**.

**10% não é um benchmark de outra plataforma.** Não há uma relação universal
entre usuários ativos mensais, usuários logados, requisições simultâneas,
conexões Postgres e WebSockets. O indicador é apenas hipótese ajustável.
Testes de carga e telemetria devem validar o dimensionamento real.

## Referências de fornecedores e fórmulas

### Banco e autenticação — Supabase

- Pro: US$ 25/mês por organização.
- Crédito único de compute: US$ 10/mês.
- Homologação Micro: aproximadamente US$ 10/mês.
- Produção: preço mensal aproximado do perfil de compute:

| Pico hipotético do cenário | Perfil orçamentário | Compute de produção |
|---|---|---:|
| até 100 | Micro | US$ 10 |
| 101–250 | Small | US$ 15 |
| 251–500 | Medium | US$ 60 |
| 501–1.000 | Large | US$ 110 |
| acima de 1.000 | XL | US$ 210 |

Essa associação de faixas é **uma escolha de orçamento, não capacidade publicada,
benchmark, recomendação do fornecedor ou garantia de desempenho**. A tarifa
mensal real varia também com horas faturáveis. A fórmula não duplica plano nem
crédito: `25 + compute de produção + 10 de homologação − 10 de crédito`.
Não há upgrade automático de banco implementado.

Franquias de referência Pro compartilhadas: 100 mil MAU, 8 GB de banco,
100 GB de arquivos, 250 GB de saída, 5 milhões de mensagens Realtime e
500 conexões Realtime de pico. Quotas não equivalem à capacidade do aplicativo.

Com G04 (chat) selecionado, pressupõe-se um WebSocket por usuário simultâneo:
`US$ 10 × ceil(max(0, pico − 500) / 1.000)`. Sem G04, nenhuma conexão
Realtime é presumida. Sessões autenticadas não são automaticamente sockets,
e múltiplas abas/dispositivos ou workers podem gerar mais conexões.
Mensagens Realtime excedentes não estão modeladas.

Fontes:
- https://supabase.com/pricing
- https://supabase.com/docs/guides/platform/compute-and-disk
- https://supabase.com/docs/guides/platform/manage-your-usage/realtime-peak-connections

### Web — Vercel

US$ 20/mês para Pro com um assento de deploy e US$ 20 de crédito de uso.
O crédito não é nova cobrança. Pressupõe uso dentro do crédito; outros assentos,
processamento, tráfego e demais excedentes não estão projetados.

Fonte: https://vercel.com/docs/plans/pro-plan

### E-mails — Resend

Plano transacional pago de US$ 20/50 mil envios, mesmo nos menores cenários,
para não depender do teto gratuito de 100/dia. O catálogo de referência também
registra US$ 35/100 mil e US$ 0,90 por bloco adicional de mil (arredondamento
conservador por bloco no modelo). Na faixa atual, `10.000 × 4 = 40.000` envios,
portanto o plano de US$ 20 cobre todos os cenários.
Não modela contatos/marketing nem presume campanhas incluídas.

Fonte: https://resend.com/docs/knowledge-base/what-is-resend-pricing

### Vídeo privado — Cloudflare Stream

- Acervo: `ceil(horas × 60 / 1.000) × US$ 5/mês`.
- Online: `ativos × minutos online / 1.000 × US$ 1`.
- Offline: `ativos × minutos de novos downloads / 1.000 × US$ 1`.
- C01: nenhuma das três cobranças de vídeo privado.
- C02: acervo e online; C03: acervo, online e downloads adicionais.

Tráfego de vídeo já está incluído; **não adicionar R2, saída de vídeo ou uma
segunda assinatura por C03**. Minutos são entregues, não apenas assistidos:
buffering, repetições online e downloads completos podem mudar o consumo.
Stream é referência de custos, não compromisso de DRM ou offline protegido.

Fonte: https://developers.cloudflare.com/stream/pricing/

## Arredondamento e cenários reproduzíveis

Cada serviço é arredondado em centavos USD, convertido pelo câmbio com duas
casas e arredondado em centavos BRL. O adicional soma as parcelas cobradas BRL
(zero em todas as parcelas para YouTube); o total mensal acrescenta a base.
O custo de referência continua registrado separadamente. PDF congela essas
parcelas, sem recalcular ao abrir.

Premissas padrão, sem chat, câmbio hipotético R$ 6/US$:

| Ativos/mês | Pico hipotético | Adicional YouTube | Adicional privado | Adicional offline |
|---:|---:|---:|---:|---:|
| 100 | 10 | R$ 0 | R$ 738 | R$ 774 |
| 500 | 50 | R$ 0 | R$ 1.170 | R$ 1.350 |
| 1.000 | 100 | R$ 0 | R$ 1.710 | R$ 2.070 |
| 2.500 | 250 | R$ 0 | R$ 3.360 | R$ 4.260 |
| 5.000 | 500 | R$ 0 | R$ 6.330 | R$ 8.130 |
| 10.000 | 1.000 | R$ 0 | R$ 12.030 | R$ 15.630 |

Exemplo de **total com 1.000 ativos**: Essencial/YouTube R$ 3.000;
Plus/privado R$ 5.710; Premium/offline R$ 7.070. Não são custos medidos,
garantias de capacidade ou cobrança automática.

## Limites e exclusões

Não se calcula tudo a partir do número de usuários. Este é um cenário para
serviços compartilhados e consumo típico, não um simulador completo de todos
os opcionais. Não inclui IA, marketing por e-mail, SMS/WhatsApp, conectores
pagos, taxas de gateway/lojas, domínio, builds pagos, backup externo de arquivos,
PITR, tributos, variação cambial nem excedentes das demais franquias de banco,
Storage, saída, funções e mensagens Realtime.

Não acrescenta markup, margem, reserva, SLA ou preço por usuário arbitrário.
Há degraus de compute e base mínima de serviços, mas com YouTube o adicional
permanece zerado por política comercial. Crescimento e excedentes são combinados antes
da cobrança, sem alteração silenciosa da mensalidade contratada.
F02 continua responsável por aprovar fornecedores/arquitetura. A spec mais ampla
`specs/configurador-custos-operacionais.md` não está integralmente implementada.

## Dados e validação

- `quoteData().monthlyMaintenanceBRL` continua sendo **apenas a base**, por
  compatibilidade. Novos campos: `monthlyOperationalBRL`, `monthlyTotalBRL`,
  `operations` (entradas, fontes, tarifas por serviço, totais e condições).
- CSV/impressão incluem composição, premissas, fontes e exclusões.
- PDF: `support.priceCents` é a base; `support.operations.totalCents` é o adicional;
  `support.totalCents` é a soma validada em centavos.
- Em `operations.lines`, `estimatedCents` é custo de referência convertido;
  `priceCents` é parcela efetivamente acrescida (zero com YouTube).
  `coveredByBase` sinaliza custos absorvidos pela manutenção. `totalEstimatedCents`
  e `totalCentsUSD` são custos estimados, não cobranças adicionais.
  `billingPolicy` distingue `youtube_included_in_base` de `estimated_surcharge`.
- Usuários e fontes não integram os snapshots de implantação/campanha.

Testes:
```
node tests/test_operational_pricing.js
node tests/test_offer_pdf.js
node tests/test_promotion.js
node tests/test_campaign_settings.js
python3 -m unittest discover -s tests -v
```

Cobrem cenários/limites, arredondamento, infraestrutura única, vídeo exclusivo,
ausência de descontos mensais, slider real no navegador, campos inválidos,
exports, snapshot PDF, composição mensal e layout de 320 a 1.440 px.
