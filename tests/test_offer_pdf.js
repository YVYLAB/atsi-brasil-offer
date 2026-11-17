const assert=require('node:assert/strict');
const pdf=require('../offer-pdf.js');
const {jsPDF}=require('../vendor/jspdf/jspdf.umd.min.js');
const row=(id,hours,regularCents,type='optional')=>({
  id,technicalTitle:`Entrega ${id}`,hours,regularCents,type,
  tasks:[{id:`${id}-T01`,title:'Implementar e conferir a experiência',hours}]
});
const fixture=()=>({
  generatedAt:'2026-11-17T13:00:00.000Z',
  project:{product:'ATSI+',client:'ATSI Brasil',developer:'YvyLab'},
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
assert.equal(pdf.fileName(model),'ATSI-Oferta-20261117T130000.pdf');
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
const document=pdf.createDocument(model,jsPDF);
const bytes=Buffer.from(document.output('arraybuffer'));
assert(bytes.subarray(0,5).equals(Buffer.from('%PDF-')));
assert(document.getNumberOfPages()>=3);
console.log('PDF: rateio, tarefas, composição e geração binária aprovados.');
