# Pacotes e ofertas de 24 horas — protótipo local

## Atualização — painel simplificado
O fluxo atual substitui os controles de importação/exportação por um popup azul
acessível pelo menu ☰. Contém somente início e término (data/hora de Brasília),
percentuais de Essencial/Plus/Premium e Salvar.
O período é explícito, não obrigatoriamente 24 h. Os percentuais aplicam-se ao
total de implantação de cada preset; mensalidades, horas e Personalizado não mudam.
A chave `atsi-campaign-v2` salva os dados somente no navegador atual. Nenhuma
configuração é pré-preenchida como promoção real. A oferta anterior v1 não é
apagada, mas não é restaurada automaticamente por esse novo painel.
O GitHub Pages não grava um JSON no repositório; o botão Salvar não publica dados
para outros visitantes. Horário e permissões continuam sem validação de servidor.
O fluxo detalhado abaixo é histórico; não é mais a interface atual do configurador.

## Estado
O configurador continua usando as referências de implantação das specs, a
R$ 200/h, e preserva as mensalidades Essencial/Plus/Premium de R$ 3.000/4.000/5.000
com 10/15/20 horas. Nenhum desconto é pré-preenchido ou ativado automaticamente.
Não foram implementados os simuladores de infraestrutura/e-mail/GitHub descritos
em documentos anteriores: permanecem em especificação separada.

## Fluxo de configuração
1. Em `home.html`, exportar o catálogo da cotação.
2. Abrir `ofertas-admin.html` localmente e importar esse JSON.
3. Informar identificação da cotação e responsável.
4. Revisar e confirmar os valores como preços de tabela reais e aprovados.
   Eles não são preços aprovados só por terem sido gerados a partir de horas.
5. Habilitar Plus e/ou Premium, informar percentuais e marcar opcionais elegíveis.
   Fundação, obrigatórias, vídeo e mensalidades não são elegíveis nesta política.
   Não há regra aprovada para desconto de vídeo ou de configuração personalizada.
6. Definir o piso total por pacote a partir de custo direto efetivo + reserva
   de risco + contribuição mínima, sem usar R$ 200/h como custo interno.
7. Confirmar a análise de margem. Desconto que excede o limite é bloqueado,
   não reduzido silenciosamente.
8. Emitir explicitamente uma nova simulação e importar o JSON em `home.html`.

O percentual do Premium é independente; um desconto maior não comprova por si
só melhor custo-benefício. A comparação mostra recursos incluídos, valor regular,
economia efetiva e diferença de investimento. Não há selo de superioridade financeira.

## Cálculos
Valores em centavos inteiros; desconto arredondado uma vez ao centavo.
Base elegível = soma de opcionais explicitamente selecionados na política e no
pacote. Desconto = base elegível × percentual / 100, limitado por bloqueio ao
máximo comercial aprovado. Implantação final = regular − desconto.
Mensalidade não é descontada nem somada ao investimento único.

## Tempo, histórico e persistência
Cada emissão gera identificadores, `issuedAt` e `expiresAt = issuedAt + 24 h`.
Snapshot integral da tabela e configurações públicas acompanha a oferta.
Oferta importada é salva com schema v1 em `localStorage`, chave `atsi-offer-v1`.
O carregamento não renova datas. Alterar pacote não renova oferta.
Após expirar, retornam valores regulares. Catálogo diferente suspende aplicação
sem reescrever o snapshot histórico. Cancelamento local registra o identificador
e impede sua reimportação naquele armazenamento.

Se armazenamento falhar, a importação/cancelamento é recusada com mensagem.
Limpar dados do navegador ou mudar de dispositivo não transporta a oferta:
é necessário importar o mesmo JSON, com a data original. Não é criada outra oferta.
A emissão registra responsável, IDs, versões e datas em histórico local separado;
isso não é auditoria inviolável nem autenticação.

## Exportação
JSON inclui snapshot, seleção, composição, oferta, status, manutenção e franquia.
CSV e impressão/PDF do navegador registram composição e validade no momento da
geração. A validade é recalculada antes de exportar, sem alterar o arquivo histórico
de oferta. Impressão e arquivos exportados são documentos estáticos; uma cópia
antiga não se atualiza sozinha após expirar.

## Limites de segurança
**Simulação — sem validação de servidor.** Relógio, arquivos e localStorage são
manipuláveis. A tela administrativa é outro arquivo, não um controle de acesso.
Não compartilhar `ofertas-admin.html` nem os pisos e custos confidenciais.
O JSON público não contém o piso ou custos efetivos, apenas a política aprovada.
Os arquivos locais `pricing-promotion.js`, logos e fontes precisam acompanhar o HTML.

Para uso comercial vinculante é necessário backend com:
- autenticação e autorização administrativa para emissão/cancelamento;
- validação de custos/piso, versão publicada e cálculo no servidor;
- persistência imutável de emissão, autoria, snapshot e histórico;
- consulta de validade por ID usando relógio do servidor;
- nova validação ao exportar/aceitar proposta, inclusive revogação e expiração.

Nenhuma infraestrutura, contrato ou backend foi criado nesta entrega.

## Testes
`node tests/test_promotion.js`: funções puras de validade, elegibilidade, margem,
expiração, snapshot e serialização, com percentuais exclusivamente de teste.
`python3 -m unittest discover -s tests -v`: somas das specs e verificações no Chrome
de planos, manutenção, prazo, ofertas, personalizado, expiração e exportação em memória.
Download real dos arquivos, impressão e revisão visual responsiva ainda exigem
homologação manual; não são comprovados pelos testes de cálculo.
