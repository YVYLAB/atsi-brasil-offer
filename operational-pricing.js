/* Simulação de fornecedores: não é medição de capacidade nem faturamento real. */
(function(root){
  'use strict';
  const version='atsi-operations-v2';
  const defaults=Object.freeze({
    activeUsers:100,exchangeRate:6,peakPercentage:10,
    videoMinutesPerUser:180,libraryHours:100,offlineMinutesPerUser:60
  });
  const plans=Object.freeze({
    essencial:{priceCents:300000,hours:10},
    plus:{priceCents:400000,hours:15},
    premium:{priceCents:500000,hours:20}
  });
  const sources=[
    {title:'Banco e autenticação',url:'https://supabase.com/pricing'},
    {title:'Perfis de processamento',url:'https://supabase.com/docs/guides/platform/compute-and-disk'},
    {title:'Conexões em tempo real',url:'https://supabase.com/docs/guides/platform/manage-your-usage/realtime-peak-connections'},
    {title:'Vídeos',url:'https://developers.cloudflare.com/stream/pricing/'},
    {title:'Hospedagem web',url:'https://vercel.com/docs/plans/pro-plan'},
    {title:'E-mails transacionais',url:'https://resend.com/docs/knowledge-base/what-is-resend-pricing'}
  ];
  const exclusions=[
    'IA, marketing por e-mail, SMS/WhatsApp, conectores pagos e taxas de pagamentos e lojas são contratados separadamente.',
    'Não inclui tributos, variação cambial, domínio, builds pagos, backup de arquivos externo, recuperação contínua do banco ou consumo além das franquias de banco, arquivos, tráfego, funções e mensagens em tempo real.',
    'Valores estimados, sem margem ou reserva adicional. Fornecedores, consumo e condições de cobrança são confirmados no planejamento; crescimento e excedentes exigem acordo prévio.'
  ];
  function calculate(input={}){
    const p={...defaults,...input};
    const bounds={
      activeUsers:[100,10000],exchangeRate:[0.01,100],peakPercentage:[1,100],
      videoMinutesPerUser:[0,6000],libraryHours:[0,10000],offlineMinutesPerUser:[0,6000]
    };
    for(const [key,[min,max]] of Object.entries(bounds)){
      if(typeof p[key]!=='number'||!Number.isFinite(p[key])||p[key]<min||p[key]>max ||
        (key!=='exchangeRate'&&!Number.isInteger(p[key])))
        throw new Error(`Confira a premissa operacional: ${key}.`);
    }
    if(!['C01','C02','C03'].includes(p.videoStrategy))throw new Error('Escolha uma estratégia de vídeo.');
    if(p.realtimeEnabled!==undefined&&typeof p.realtimeEnabled!=='boolean')throw new Error('Confira a opção de tempo real.');
    if(Math.abs(p.exchangeRate*100-Math.round(p.exchangeRate*100))>1e-6)
      throw new Error('Use até duas casas decimais no câmbio.');
    const peakUsers=Math.ceil(p.activeUsers*p.peakPercentage/100);
    // Perfis de orçamento hipotéticos. Não representam benchmarks dos fornecedores.
    const compute=peakUsers<=100?{name:'Micro',usd:10}:peakUsers<=250?{name:'Small',usd:15}:
      peakUsers<=500?{name:'Medium',usd:60}:peakUsers<=1000?{name:'Large',usd:110}:{name:'XL',usd:210};
    const privateVideo=p.videoStrategy!=='C01';
    const exchangeCents=Math.round(p.exchangeRate*100),lines=[];
    function line(id,label,provider,amountUSD,basis){
      const amountCentsUSD=Math.round(amountUSD*100);
      const estimatedCents=Math.round(amountCentsUSD*exchangeCents/100);
      lines.push({id,label,provider,amountCentsUSD,estimatedCents,
        priceCents:privateVideo?estimatedCents:0,coveredByBase:!privateVideo&&estimatedCents>0,basis});
    }
    line('database','Banco e autenticação','Supabase',25+compute.usd+10-10,
      `Pro US$ 25 + produção ${compute.name} US$ ${compute.usd} + homologação Micro US$ 10 − crédito único US$ 10.`);
    line('web','Hospedagem web','Vercel',20,
      'Pro US$ 20/mês, um assento de deploy, consumo dentro do crédito de US$ 20; sem duplicar o crédito como cobrança.');
    const emailCount=p.activeUsers*4;
    const emailUSD=emailCount<=50000?20:35+Math.ceil(Math.max(0,emailCount-100000)/1000)*0.9;
    line('email','E-mails de acesso e avisos','Resend',emailUSD,
      `${emailCount} e-mails/mês (4 por usuário), plano transacional pago, sem marketing.`);
    const realtimeConnections=p.realtimeEnabled?peakUsers:0;
    line('realtime','Conexões em tempo real','Supabase',
      Math.ceil(Math.max(0,realtimeConnections-500)/1000)*10,
      `${realtimeConnections} conexões de pico hipotéticas; 1 por usuário simultâneo com chat, 500 incluídas, US$ 10 por bloco excedente de 1.000. Sem chat: zero.`);
    const storageMinutes=privateVideo?p.libraryHours*60:0;
    const streamingMinutes=privateVideo?p.activeUsers*p.videoMinutesPerUser:0;
    const downloadMinutes=p.videoStrategy==='C03'?p.activeUsers*p.offlineMinutesPerUser:0;
    line('videoStorage','Acervo de vídeos privados','Cloudflare Stream',Math.ceil(storageMinutes/1000)*5,
      `${storageMinutes} minutos; US$ 5 por bloco pré-pago de 1.000 minutos. YouTube: sem cobrança de Stream.`);
    line('videoDelivery','Reprodução online de vídeos privados','Cloudflare Stream',streamingMinutes/1000,
      `${streamingMinutes} minutos entregues/mês; US$ 1 por 1.000 minutos, tráfego incluído.`);
    line('videoDownloads','Downloads offline adicionais','Cloudflare Stream',downloadMinutes/1000,
      `${downloadMinutes} minutos baixados/mês adicionais à reprodução online; sem nova cobrança por assistir ao arquivo local.`);
    const fmt=n=>n.toLocaleString('pt-BR',{maximumFractionDigits:2});
    const videoLabel={C01:'YouTube incorporado',C02:'Streaming privado',C03:'Streaming privado + offline'}[p.videoStrategy];
    const explanation=[
      'A mensalidade reúne o cuidado contínuo com a plataforma e os serviços necessários para seu funcionamento. Esse valor é separado do investimento inicial para desenvolver o projeto.',
      'Manutenção do plano: inclui as horas mensais contratadas para correções, ajustes e melhorias no software. Se precisar de mais horas, um pacote adicional será combinado antes da execução.',
      'Serviços e vídeos: ao escolher vídeos privados ou com opção de baixar para assistir sem internet, há um valor adicional pelos serviços que mantêm a plataforma funcionando e disponibilizam esses conteúdos. Esse custo pode crescer principalmente conforme a quantidade de vídeos armazenados, assistidos e baixados pelos alunos.',
      'Com vídeos pelo YouTube, esse adicional é zero. Nesse caso, permanece apenas a mensalidade base do plano, que já cobre os serviços de funcionamento considerados nesta simulação.',
      'O controle de usuários ajuda a estimar esse valor conforme o público esperado. Ele não gera cobranças automáticas: mudanças de capacidade ou consumo serão combinadas previamente. O consumo de inteligência artificial é contratado separadamente.'
    ].join('\n\n');
    const assumptions=[
      `${fmt(p.activeUsers)} usuários ativos por mês (pessoas distintas que usam a plataforma, não contas cadastradas).`,
      `Pico hipotético de ${fmt(p.peakPercentage)}%: ${fmt(peakUsers)} usuários simultâneos; não é capacidade garantida nem limite contratado.`,
      `Câmbio de simulação: R$ ${p.exchangeRate.toFixed(2).replace('.',',')}/US$, sem cotação automática.`,
      `Vídeo: ${videoLabel}. ${privateVideo?`${fmt(p.videoMinutesPerUser)} minutos online por usuário/mês e ${fmt(p.libraryHours)} horas de acervo privado.`:'Sem custos de armazenamento ou entrega de vídeo privado neste cenário.'}`,
      p.videoStrategy==='C03'?`${fmt(p.offlineMinutesPerUser)} minutos de novos downloads por usuário/mês, além do online; repetições locais não somam tráfego.`:'Downloads offline não cobrados neste cenário.',
      `Infraestrutura compartilhada uma vez; produção ${compute.name} e homologação Micro como hipótese de orçamento, não benchmark. Validar com testes de carga.`,
      '4 e-mails transacionais por usuário/mês; hospedagem web com um assento de deploy. Demais consumos dentro das franquias pesquisadas.'
    ];
    assumptions.push(privateVideo?
      'Política comercial: custos do cenário somados à manutenção base como adicional operacional.':
      'Política comercial YouTube: adicional operacional zerado; custos estimados de infraestrutura compartilhada cobertos pela manutenção base, não custos inexistentes.');
    return {schemaVersion:1,version,rateDate:'2026-11-17',
      inputs:{...Object.fromEntries(Object.keys(defaults).map(key=>[key,p[key]])),
        videoStrategy:p.videoStrategy,realtimeEnabled:!!p.realtimeEnabled},
      videoLabel,explanation,billingPolicy:privateVideo?'estimated_surcharge':'youtube_included_in_base',
      peakUsers,computeProfile:compute.name,emailCount,realtimeConnections,
      storageMinutes,streamingMinutes,downloadMinutes,lines,
      totalCents:lines.reduce((n,item)=>n+item.priceCents,0),
      totalEstimatedCents:lines.reduce((n,item)=>n+item.estimatedCents,0),
      totalCentsUSD:lines.reduce((n,item)=>n+item.amountCentsUSD,0),
      assumptions,exclusions:[...exclusions],sources:sources.map(source=>({...source}))};
  }
  const api={version,defaults,plans,calculate};
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.ATSIOperations=api;
})(typeof globalThis!=='undefined'?globalThis:this);
