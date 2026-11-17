/* Documento estático da configuração: valores em centavos, esforço em horas. */
(function(root){
  'use strict';
  const money=n=>Number.isSafeInteger(n)&&n>=0;
  const sum=(items,key)=>items.reduce((total,item)=>total+item[key],0);
  const brl=n=>new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(n/100);
  const number=n=>new Intl.NumberFormat('pt-BR',{maximumFractionDigits:2}).format(n);
  const date=value=>Number.isFinite(Date.parse(value))?
    new Intl.DateTimeFormat('pt-BR',{dateStyle:'short',timeStyle:'medium',timeZone:'America/Sao_Paulo'}).format(new Date(value)):'A combinar';
  function allocateDiscount(items,discountCents){
    const total=sum(items,'regularCents');
    if(!money(discountCents)||!money(total)||discountCents>total)
      throw new Error('O desconto não corresponde à composição da oferta.');
    const allocation=new Map(items.map(item=>[item.id,0]));
    if(discountCents===0)return allocation;
    const shares=items.map((item,index)=>{
      const weighted=BigInt(item.regularCents)*BigInt(discountCents);
      return {id:item.id,index,value:Number(weighted/BigInt(total)),remainder:weighted%BigInt(total)};
    });
    let remaining=discountCents-shares.reduce((n,item)=>n+item.value,0);
    shares.sort((a,b)=>a.remainder===b.remainder?a.index-b.index:a.remainder>b.remainder?-1:1);
    for(const item of shares){
      allocation.set(item.id,item.value+(remaining>0?1:0));
      if(remaining>0)remaining--;
    }
    return allocation;
  }
  function buildModel(input){
    const data=JSON.parse(JSON.stringify(input));
    const rows=[...data.foundation,...data.features];
    if(new Set(rows.map(row=>row.id)).size!==rows.length)throw new Error('Há entregas repetidas na oferta.');
    for(const row of rows){
      if(!row.id || !row.technicalTitle || !money(row.regularCents) ||
        !Number.isFinite(row.hours) || row.hours<0 || !Array.isArray(row.tasks) || row.tasks.length===0 ||
        row.tasks.some(task=>!task.id || !task.title || !Number.isFinite(task.hours)||task.hours<0) ||
        sum(row.tasks,'hours')!==row.hours)
        throw new Error(`Confira as tarefas e as horas da entrega ${row.id || ''}.`);
      if(new Set(row.tasks.map(task=>task.id)).size!==row.tasks.length)
        throw new Error(`Há tarefas repetidas na entrega ${row.id}.`);
    }
    if(!Number.isFinite(Date.parse(data.generatedAt)) || !money(data.pricing.regularCents) ||
      sum(rows,'regularCents')!==data.pricing.regularCents)
      throw new Error('A composição não corresponde ao investimento da oferta.');
    const targets=new Set(data.promotion.planTargetIds);
    if([...targets].some(id=>!rows.some(row=>row.id===id)))throw new Error('A promoção contém uma entrega ausente.');
    const planAllocation=allocateDiscount(rows.filter(row=>targets.has(row.id)),data.promotion.planDiscountCents);
    const extras=new Map();
    for(const item of data.promotion.additionalItems){
      const row=data.features.find(feature=>feature.id===item.id);
      if(!row || row.type!=='optional' || extras.has(item.id) || !money(item.discountCents) ||
        item.discountCents>row.regularCents || (targets.has(item.id)&&item.discountCents>0))
        throw new Error('O desconto adicional não corresponde às funcionalidades escolhidas.');
      extras.set(item.id,item.discountCents);
    }
    for(const row of rows){
      row.planDiscountCents=planAllocation.get(row.id)||0;
      row.additionalDiscountCents=extras.get(row.id)||0;
      row.discountCents=row.planDiscountCents+row.additionalDiscountCents;
      row.finalCents=row.regularCents-row.discountCents;
      if(!money(row.finalCents))throw new Error('O desconto excede o valor de uma entrega.');
    }
    if(sum(rows,'discountCents')!==data.pricing.discountCents ||
      sum(rows,'finalCents')!==data.pricing.finalCents ||
      data.pricing.regularCents-data.pricing.discountCents!==data.pricing.finalCents)
      throw new Error('A soma das entregas não fecha com o total da oferta.');
    if(!money(data.support.priceCents)||!Number.isFinite(data.support.hours)||data.support.hours<0)
      throw new Error('Confira a manutenção mensal da oferta.');
    const operations=data.support.operations;
    if(operations){
      if(operations.schemaVersion!==1||!operations.inputs ||
        !Number.isSafeInteger(operations.inputs.activeUsers)||operations.inputs.activeUsers<100||
        operations.inputs.activeUsers>10000 ||
        !money(operations.totalCents)||!Array.isArray(operations.lines)||!operations.lines.length ||
        operations.lines.some(line=>!line.label||!line.basis||!money(line.priceCents)||!money(line.amountCentsUSD)||
          !money(line.estimatedCents)) ||
        new Set(operations.lines.map(line=>line.id)).size!==operations.lines.length ||
        sum(operations.lines,'priceCents')!==operations.totalCents ||
        sum(operations.lines,'amountCentsUSD')!==operations.totalCentsUSD ||
        sum(operations.lines,'estimatedCents')!==operations.totalEstimatedCents ||
        !operations.explanation ||
        !Array.isArray(operations.assumptions)||!operations.assumptions.length ||
        !Array.isArray(operations.exclusions)||!Array.isArray(operations.sources) ||
        data.support.totalCents!==data.support.priceCents+operations.totalCents)
        throw new Error('Confira a composição operacional mensal da oferta.');
    }else{
      data.support.totalCents=data.support.priceCents;
    }
    if(data.benefits.some(benefit=>benefit.priceCents!==0))throw new Error('Confira os benefícios de cortesia.');
    data.foundation=rows.slice(0,data.foundation.length);
    data.features=rows.slice(data.foundation.length);
    data.totalHours=sum(rows,'hours');
    data.estimatedMonths=data.totalHours/352;
    data.foundationTotals={
      hours:sum(data.foundation,'hours'),regularCents:sum(data.foundation,'regularCents'),
      discountCents:sum(data.foundation,'discountCents'),finalCents:sum(data.foundation,'finalCents')
    };
    return data;
  }
  function clean(value){
    return String(value||'').replace(/\*\*/g,'').replace(/`/g,'')
      .replace(/[—–]/g,'-').replace(/[“”]/g,'"').replace(/[‘’]/g,"'")
      .replace(/→/g,' -> ').replace(/≥/g,'>=').replace(/≤/g,'<=').replace(/\t/g,' ');
  }
  function fileName(model){
    return `ATSI-Oferta-${model.generatedAt.replace(/[-:]/g,'').slice(0,15)}.pdf`;
  }
  function createDocument(model,JsPDF=root.jspdf?.jsPDF){
    if(!JsPDF)throw new Error('O gerador de PDF não está disponível. Reabra a página e tente novamente.');
    const doc=new JsPDF({unit:'mm',format:'a4',compress:true,putOnlyUsedFonts:true});
    doc.setProperties({title:`Oferta ${model.project.product} - ${model.project.client}`,
      author:model.project.developer,subject:'Escopo, tarefas e investimento da configuração escolhida',
      creator:`${model.project.developer} - Configurador ${model.project.product}`});
    doc.setCreationDate(new Date(model.generatedAt));
    const left=16,right=194,width=178,bottom=276;
    let y=29;
    function header(){
      doc.setFillColor(23,56,80);doc.rect(0,0,210,20,'F');
      doc.setFont('helvetica','bold');doc.setFontSize(11);doc.setTextColor(255,255,255);
      doc.text(clean(`${model.project.product} | ${model.project.client}`),left,12);
      doc.setFontSize(9);doc.text(clean(model.project.developer),right,12,{align:'right'});
      doc.setDrawColor(44,157,84);doc.setLineWidth(1);doc.line(0,20,210,20);
    }
    function page(){doc.addPage();header();y=29;}
    function ensure(height,repeat){
      if(y+height>bottom){page();if(repeat)repeat();}
    }
    function paragraph(text,{size=9.5,bold=false,color=[40,54,62],indent=0,gap=3}={}){
      doc.setFont('helvetica',bold?'bold':'normal');doc.setFontSize(size);doc.setTextColor(...color);
      const lineHeight=size*.43;
      const lines=doc.splitTextToSize(clean(text),width-indent);
      for(const line of lines){
        ensure(lineHeight);
        doc.setFont('helvetica',bold?'bold':'normal');doc.setFontSize(size);doc.setTextColor(...color);
        doc.text(line,left+indent,y);y+=lineHeight;
      }
      y+=gap;
    }
    function heading(text,major=false){
      ensure(18);y+=3;
      paragraph(text,{size:major?17:12,bold:true,color:[23,56,80],gap:4});
    }
    function keyValue(label,value,bold=false){
      paragraph(`${label}: ${value}`,{bold,gap:2});
    }
    function financialHeader(){
      ensure(10);
      doc.setFillColor(232,241,237);doc.rect(left,y-4,width,8,'F');
      doc.setFont('helvetica','bold');doc.setFontSize(8);doc.setTextColor(23,56,80);
      doc.text('Entrega',left+2,y+1);
      doc.text('Horas',106,y+1,{align:'right'});
      doc.text('Tabela',135,y+1,{align:'right'});
      doc.text('Desconto',164,y+1,{align:'right'});
      doc.text('Oferta',right-1,y+1,{align:'right'});
      y+=8;
    }
    function financialRow(title,hours,regularCents,discountCents,finalCents){
      doc.setFont('helvetica','normal');doc.setFontSize(8);
      const lines=doc.splitTextToSize(clean(title),73);
      const height=Math.max(9,lines.length*3.6+3);
      ensure(height+2,financialHeader);
      doc.setFont('helvetica','normal');doc.setFontSize(8);doc.setTextColor(40,54,62);
      doc.text(lines,left+2,y);
      doc.text(hours===null?'-':number(hours),106,y,{align:'right'});
      doc.text(brl(regularCents),135,y,{align:'right'});
      doc.text(brl(discountCents),164,y,{align:'right'});
      doc.setFont('helvetica','bold');doc.text(brl(finalCents),right-1,y,{align:'right'});
      y+=height;doc.setDrawColor(222,229,232);doc.setLineWidth(.2);doc.line(left,y-3,right,y-3);
    }
    function taskHeader(){
      ensure(10);
      doc.setFillColor(232,241,237);doc.rect(left,y-4,width,8,'F');
      doc.setFont('helvetica','bold');doc.setFontSize(8);doc.setTextColor(23,56,80);
      doc.text('Tarefa / entrega verificável',left+2,y+1);
      doc.text('Esforço',right-2,y+1,{align:'right'});y+=9;
    }
    function taskRow(task,item){
      doc.setFont('helvetica','normal');doc.setFontSize(8.5);
      const lines=doc.splitTextToSize(clean(`${task.id} - ${task.title}`),145);
      const height=Math.max(9,lines.length*3.8+3);
      ensure(height+2,()=>{
        paragraph(`${item.id} - ${item.technicalTitle} (continuação)`,{bold:true,size:10});
        taskHeader();
      });
      doc.setFont('helvetica','normal');doc.setFontSize(8.5);doc.setTextColor(40,54,62);
      doc.text(lines,left+2,y);
      doc.setFont('helvetica','bold');doc.text(`${number(task.hours)} h`,right-2,y,{align:'right'});
      y+=height;doc.setDrawColor(222,229,232);doc.setLineWidth(.2);doc.line(left,y-3,right,y-3);
    }
    function detail(item){
      ensure(48);
      heading(`${item.id} - ${item.technicalTitle}`);
      keyValue('Esforço estimado',`${number(item.hours)} h`);
      keyValue('Valor de tabela',brl(item.regularCents));
      if(item.planDiscountCents>0)keyValue('Desconto do plano, rateado nesta entrega',brl(item.planDiscountCents));
      if(item.additionalDiscountCents>0)keyValue('Desconto de opcional adicional',brl(item.additionalDiscountCents));
      keyValue('Valor desta entrega na oferta',brl(item.finalCents),true);
      if(item.description)paragraph(item.description);
      taskHeader();
      for(const task of item.tasks)taskRow(task,item);
      keyValue('Total das tarefas',`${number(sum(item.tasks,'hours'))} h`,true);
      if(item.scope){ensure(20);paragraph('Escopo e limites',{bold:true});paragraph(item.scope);}
      if(item.risks){ensure(20);paragraph('Integrações e condições da entrega',{bold:true});paragraph(item.risks);}
      if(item.acceptance){ensure(20);paragraph('Critério de entrega',{bold:true});paragraph(item.acceptance);}
      y+=6;
    }
    header();
    heading('Oferta técnica e comercial',true);
    paragraph('Configuração escolhida para a construção da plataforma ATSI+.');
    keyValue('Cliente',model.project.client);keyValue('Desenvolvimento',model.project.developer);
    keyValue('Gerada em Brasília',date(model.generatedAt));
    keyValue('Configuração',model.packageName);keyValue('Plano de origem',model.basePackageName);
    keyValue('Plataformas',model.delivery.studentLabel);keyValue('Gestão',model.delivery.administration);
    heading('Investimento e prazo',true);
    keyValue('Implantação - valor de tabela',brl(model.pricing.regularCents));
    keyValue('Desconto do plano',brl(model.promotion.planDiscountCents));
    keyValue('Desconto dos opcionais adicionais',brl(sum(model.promotion.additionalItems,'discountCents')));
    keyValue('Investimento de implantação da oferta',brl(model.pricing.finalCents),true);
    keyValue('Esforço total',`${number(model.totalHours)} h`);
    keyValue('Prazo equivalente estimado',`${number(model.estimatedMonths)} meses`);
    paragraph('As horas de cada tarefa representam esforço de uma pessoa, não duração corrida. O prazo equivalente considera duas pessoas dedicadas, com 352 h mensais de capacidade. Sequência das entregas, paralelismo e disponibilidade são detalhados no planejamento.');
    if(model.promotion.startsAt&&model.promotion.endsAt){
      heading('Condição da oferta');
      keyValue('Situação no momento da geração',model.promotion.statusLabel);
      keyValue('Período em Brasília',`${date(model.promotion.startsAt)} até ${date(model.promotion.endsAt)}`);
      paragraph('Este documento registra os valores no momento da geração. As datas da campanha permanecem as mesmas; gerar o PDF não renova sua vigência.');
    }
    heading('Composição financeira',true);
    paragraph('Os nomes abaixo seguem as especificações técnicas de cada entrega. A preparação é cobrada uma única vez. A manutenção mensal é apresentada separadamente.');
    financialHeader();
    const f=model.foundationTotals;
    financialRow('Preparação técnica - detalhada nas próximas páginas',f.hours,f.regularCents,f.discountCents,f.finalCents);
    for(const item of model.features)financialRow(`${item.id} - ${item.technicalTitle}`,item.hours,item.regularCents,item.discountCents,item.finalCents);
    for(const benefit of model.benefits)financialRow(`${benefit.title} - cortesia`,null,0,0,0);
    financialRow('TOTAL DA IMPLANTAÇÃO',model.totalHours,model.pricing.regularCents,model.pricing.discountCents,model.pricing.finalCents);
    paragraph('O desconto do pacote é distribuído proporcionalmente entre as entregas que o compõem, com compensação dos centavos de arredondamento. O desconto de opcionais adicionais é separado, sem desconto duplicado. A soma dos valores por entrega fecha com o investimento total. As tarefas têm estimativas de esforço; o preço comercial corresponde à entrega completa.');
    page();heading('Preparação técnica incluída',true);
    for(const item of model.foundation)detail(item);
    page();heading('Funcionalidades adquiridas',true);
    for(const item of model.features)detail(item);
    heading('Capacitação e benefícios incluídos',true);
    for(const benefit of model.benefits){
      heading(benefit.title);
      paragraph(benefit.description);
      for(const topic of benefit.topics)paragraph(`- ${topic}`,{indent:2});
      paragraph(benefit.scope);keyValue('Investimento adicional',benefit.commercialLabel,true);
    }
    heading('Manutenção e operação mensal',true);
    keyValue('Plano de manutenção',model.support.planName);
    if(model.support.operations){
      heading('O que compõe sua mensalidade?');
      for(const text of model.support.operations.explanation.split('\n\n'))paragraph(text);
    }
    keyValue('Manutenção do plano',`${brl(model.support.priceCents)} / mês`);
    if(model.support.operations){
      keyValue('Serviços e vídeos - valor estimado',`${brl(model.support.operations.totalCents)} / mês`);
      keyValue('Total mensal estimado',`${brl(model.support.totalCents)} / mês`,true);
    }
    keyValue('Horas mensais incluídas',`${number(model.support.hours)} h`);
    paragraph('As horas do plano são compartilhadas entre correções, ajustes e melhorias no software. Os descontos do desenvolvimento inicial não se aplicam à mensalidade. Esse valor mensal não integra o pagamento único para desenvolver o projeto.');
    if(model.support.operations){
      const ops=model.support.operations;
      heading('Cenário de operação mensal');
      keyValue('Modelo e data das tarifas',`${ops.version} | ${ops.rateDate}`);
      for(const text of ops.assumptions)paragraph(`- ${text}`);
      for(const line of ops.lines){
        keyValue(`${line.label} (${line.provider})`,`${brl(line.priceCents)} / mês`,true);
        paragraph(`${line.basis} Custo de referência: US$ ${number(line.amountCentsUSD/100)} / mês.${line.coveredByBase?' Incluído na base de manutenção, sem cobrança adicional.':''}`);
      }
      keyValue('Total dos fornecedores em USD',`US$ ${number(ops.totalCentsUSD/100)} / mês`);
      keyValue('Custo estimado convertido (não somar novamente)',brl(ops.totalEstimatedCents));
      paragraph('Conversão e soma por serviço em centavos, congeladas no momento de gerar este documento.');
      for(const text of ops.exclusions)paragraph(`- ${text}`);
      heading('Fontes das tarifas de referência');
      for(const source of ops.sources)paragraph(`${source.title}: ${source.url}`,{size:8.5});
    }
    heading('Planejamento da contratação');
    paragraph('Forma de pagamento, início das entregas, cronograma e condições de manutenção são combinados na contratação. Plataformas, integrações e permissões seguem o escopo de cada funcionalidade detalhada neste documento.');
    paragraph(model.delivery.estimateNote);
    const pages=doc.getNumberOfPages();
    for(let i=1;i<=pages;i++){
      doc.setPage(i);doc.setDrawColor(200,212,218);doc.setLineWidth(.2);doc.line(left,282,right,282);
      doc.setFont('helvetica','normal');doc.setFontSize(8);doc.setTextColor(83,102,111);
      doc.text(clean(`${model.project.product} - ${date(model.generatedAt)} (Brasília)`),left,288);
      doc.text(`Página ${i} de ${pages}`,right,288,{align:'right'});
    }
    return doc;
  }
  const api={allocateDiscount,buildModel,createDocument,fileName};
  root.ATSIOfferPDF=api;
  if(typeof module!=='undefined')module.exports=api;
})(globalThis);
