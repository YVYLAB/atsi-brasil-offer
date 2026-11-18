const assert=require('node:assert/strict');
const pdf=require('../offer-pdf.js');
const operations=require('../operational-pricing.js');
const {jsPDF}=require('../vendor/jspdf/jspdf.umd.min.js');
require('../branding/pdf-logos.js');
const row=(id,hours,regularCents,type='optional')=>({
  id,technicalTitle:`Entrega ${id}`,hours,regularCents,type,
  tasks:[{id:`${id}-T01`,title:'Implementar e conferir a experiência',hours}]
});
const fixture=()=>({
  generatedAt:'2026-11-17T13:00:00.000Z',
  project:{product:'ATSI+',client:'ATSI Brasil',developer:'YvyLab',company:'atsi-brasil',
    institutionalLogo:globalThis.CompanyPDFLogos['atsi-brasil']},
  packageName:'Personalizado',basePackageName:'Essencial',
  delivery:{studentLabel:'Android, iOS e web',administration:'Painel web',estimateNote:'Cronograma detalhado no planejamento.'},
  pricing:{regularCents:1700,discountCents:320,finalCents:1380},
  foundation:[row('F01',2,400)],
  features:[row('B01',1,200,'required'),row('C01',1,100,'unique'),row('X01',5,1000)],
  benefits:[{id:'admin_training',title:'Curso para administradores',priceCents:0,
    description:'Capacitação da equipe.',topics:['Uso do painel'],scope:'Recursos contratados.',commercialLabel:'Cortesia'}],
  support:{planName:'Essencial',priceCents:300000,hours:10},
  promotion:{planDiscountCents:70,planTargetIds:['F01','B01','C01'],
    additionalItems:[{id:'X01',discountCents:250}],status:'active',statusLabel:'Condição vigente',
    startsAt:'2026-11-17T12:00:00.000Z',endsAt:'2026-11-18T12:00:00.000Z'}
});
const input=fixture(),before=JSON.stringify(input);
const model=pdf.buildModel(input);
assert.equal(JSON.stringify(input),before);
assert.equal(model.totalHours,9);
assert.equal(model.foundation[0].discountCents,40);
assert.equal(model.features[0].discountCents,20);
assert.equal(model.features[1].discountCents,10);
assert.equal(model.features[2].additionalDiscountCents,250);
assert.equal(model.foundationTotals.finalCents,360);
assert.equal([...model.foundation,...model.features].reduce((n,item)=>n+item.finalCents,0),1380);
assert.equal(model.support.priceCents,300000);
const monthly=fixture();
monthly.support.operations=operations.calculate({videoStrategy:'C03',activeUsers:1000});
monthly.support.totalCents=monthly.support.priceCents+monthly.support.operations.totalCents;
const monthlyModel=pdf.buildModel(monthly);
assert.equal(monthlyModel.support.totalCents,507000);
assert.equal(monthlyModel.pricing.finalCents,model.pricing.finalCents);
const youtube=fixture();
youtube.support.operations=operations.calculate({videoStrategy:'C01',activeUsers:10000,realtimeEnabled:true});
youtube.support.totalCents=youtube.support.priceCents;
const youtubeModel=pdf.buildModel(youtube);
assert.equal(youtubeModel.support.operations.totalCents,0);
assert(youtubeModel.support.operations.totalEstimatedCents>0);
assert.equal(youtubeModel.support.totalCents,youtubeModel.support.priceCents);
for(const mutate of [
  data=>data.support.totalCents++,
  data=>data.support.operations.totalCents++,
  data=>data.support.operations.totalCentsUSD++,
  data=>data.support.operations.totalEstimatedCents++,
  data=>data.support.operations.lines[0].priceCents++,
  data=>data.support.operations.lines[0].priceCents=-1,
  data=>data.support.operations.lines[0].id=data.support.operations.lines[1].id,
  data=>data.support.operations.inputs.activeUsers=10001
]){
  const broken=JSON.parse(JSON.stringify(monthly));mutate(broken);
  assert.throws(()=>pdf.buildModel(broken),/operacional/);
}
assert.equal(pdf.fileName(model),'atsi-brasil-Oferta-20261117T130000.pdf');
const tied=[row('A',1,1),row('B',1,1),row('C',1,1)];
assert.deepEqual([...pdf.allocateDiscount(tied,1).values()],[1,0,0]);
assert.deepEqual([...pdf.allocateDiscount(tied,2).values()],[1,1,0]);
assert.deepEqual([...pdf.allocateDiscount(tied,3).values()],[1,1,1]);
assert.deepEqual([...pdf.allocateDiscount([],0).values()],[]);
assert.throws(()=>pdf.allocateDiscount(tied,4));
const large=[row('large1',1,4000000000),row('large2',1,4000000000)];
assert.deepEqual([...pdf.allocateDiscount(large,4000000000).values()],[2000000000,2000000000]);
let invalid=fixture();invalid.features[0].tasks[0].hours=99;
assert.throws(()=>pdf.buildModel(invalid),/tarefas/);
invalid=fixture();invalid.pricing.finalCents++;
assert.throws(()=>pdf.buildModel(invalid),/total/);
invalid=fixture();invalid.features[0].id='F01';
assert.throws(()=>pdf.buildModel(invalid),/repetidas/);
invalid=fixture();invalid.promotion.additionalItems[0].id='B01';
assert.throws(()=>pdf.buildModel(invalid),/adicional/);
invalid=fixture();invalid.benefits[0].priceCents=1;
assert.throws(()=>pdf.buildModel(invalid),/cortesia/);
const legacy=fixture();
legacy.pricing={regularCents:1700,discountCents:20,finalCents:1680};
legacy.promotion={...legacy.promotion,planDiscountCents:20,planTargetIds:['B01'],additionalItems:[]};
const legacyModel=pdf.buildModel(legacy);
assert.equal(legacyModel.foundation[0].discountCents,0);
assert.equal(legacyModel.features[0].discountCents,20);
const imageCalls=[],textCalls=[];
function RecordingPDF(options){
  const doc=new jsPDF(options);
  const addImage=doc.addImage,text=doc.text;
  doc.addImage=function(...args){imageCalls.push(args);return addImage.apply(this,args);};
  doc.text=function(...args){textCalls.push(args[0]);return text.apply(this,args);};
  return doc;
}
const document=pdf.createDocument(model,RecordingPDF);
const bytes=Buffer.from(document.output('arraybuffer'));
assert(bytes.subarray(0,5).equals(Buffer.from('%PDF-')));
assert(document.getNumberOfPages()>=3);
assert.equal(imageCalls.length,document.getNumberOfPages());
for(const args of imageCalls){
  assert.equal(args[0],model.project.institutionalLogo.dataURL);
  assert(args[4]<=48 && args[5]<=12);
  assert(Math.abs(args[4]/args[5]-model.project.institutionalLogo.width/model.project.institutionalLogo.height)<1e-9);
}
assert(!textCalls.includes('ATSI+ | ATSI Brasil'));
assert.equal(textCalls.filter(text=>typeof text==='string'&&text.includes('ATSI+')).length,1);
assert.throws(()=>pdf.createDocument({...model,project:{...model.project,institutionalLogo:null}},jsPDF),/logo institucional/);
assert.throws(()=>pdf.createDocument({...model,project:{...model.project,company:'jan'}},jsPDF),/logo institucional/);
assert(Buffer.from(pdf.createDocument(monthlyModel,jsPDF).output('arraybuffer')).subarray(0,5).equals(Buffer.from('%PDF-')));
console.log('PDF: rateio, tarefas, composição e geração binária aprovados.');
