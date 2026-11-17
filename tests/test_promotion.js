const assert=require('node:assert/strict');
const p=require('../pricing-promotion.js');
const item=(id,type,priceCents)=>({id,type,priceCents,title:id});
const snapshot={schemaVersion:1,priceListVersion:'test-only',packages:{
  essencial:{foundationCents:10000,items:[item('B','required',5000),item('V','unique',2000)]},
  plus:{foundationCents:10000,items:[item('B','required',5000),item('V2','unique',4000),item('O','optional',10000)]},
  premium:{foundationCents:10000,items:[item('B','required',5000),item('V3','unique',6000),item('O','optional',10000),item('P','optional',20000)]}
}};
const now=Date.parse('2026-11-16T12:00:00Z');
// Percentuais e preços exclusivamente de teste, nunca carregados pela interface.
const config=(pct,ids)=>({enabled:true,percentage:pct,eligibleFeatureIds:ids,
  maxDiscountCents:10000,priceApproval:true,marginApproval:true});
const offer={schemaVersion:1,id:'test-offer',quoteId:'test-quote',author:'Test',
 configVersion:'test',status:'active',issuedAt:new Date(now).toISOString(),
 expiresAt:new Date(now+86400000).toISOString(),snapshot,
 config:{plus:config(10,['O']),premium:config(20,['O','P'])}};
assert(p.validOffer(offer));
assert.equal(p.calculate(snapshot,'essencial',offer,now).discountCents,0);
assert.equal(p.calculate(snapshot,'plus',null,now).discountCents,0);
assert.equal(p.calculate(snapshot,'plus',offer,now).discountCents,1000);
assert.equal(p.calculate(snapshot,'premium',offer,now).discountCents,6000);
assert.equal(p.calculate(snapshot,'premium',offer,now).finalCents,45000);
assert.equal(p.calculate(snapshot,'plus',offer,now+86400000).discountCents,0);
assert.equal(p.status(offer,snapshot,now+86400000),'expired');
assert.equal(p.status(offer,snapshot,now-1),'scheduled');
const copy=()=>JSON.parse(JSON.stringify(offer));
let invalid=copy();invalid.config.plus.eligibleFeatureIds=['B'];assert(!p.validOffer(invalid));
invalid=copy();invalid.config.plus.eligibleFeatureIds=['V2'];assert(!p.validOffer(invalid));
invalid=copy();invalid.config.plus.percentage=101;assert(!p.validOffer(invalid));
invalid=copy();invalid.config.plus.priceApproval=false;assert(!p.validOffer(invalid));
invalid=copy();invalid.config.plus.maxDiscountCents=500;
assert(p.calculate(snapshot,'plus',invalid,now).blocked);
assert.equal(p.calculate(snapshot,'plus',invalid,now).discountCents,0);
invalid=copy();invalid.config.plus.percentage=0;assert(!p.validOffer(invalid));
invalid=copy();invalid.status='cancelled';assert.equal(p.status(invalid,snapshot,now),'cancelled');
invalid=copy();invalid.expiresAt=new Date(now+86400001).toISOString();assert(!p.validOffer(invalid));
const changed=JSON.parse(JSON.stringify(snapshot));changed.packages.plus.items[0].priceCents++;
assert.equal(p.status(offer,changed,now),'catalog_changed');
const restored=JSON.parse(JSON.stringify(offer));
assert.equal(restored.issuedAt,offer.issuedAt);
assert.equal(restored.expiresAt,offer.expiresAt);
assert.equal(p.status(restored,snapshot,now+1000),'active');
assert(!p.validOffer({}));

const campaign={schemaVersion:2,startsAt:new Date(now).toISOString(),
  endsAt:new Date(now+86400000).toISOString(),percentages:{essencial:10,plus:10,premium:20},
  additionalOptionalPercentage:25};
const selection=[...snapshot.packages.plus.items,item('X','optional',5000),item('Y','optional',333)];
const original=JSON.stringify({snapshot,selection,campaign});
assert(p.validCampaign(campaign));
let priced=p.calculateSelection(snapshot,'plus',selection,campaign,now);
assert.equal(priced.regularCents,34333);
assert.equal(priced.planDiscountCents,2900);
assert.equal(priced.additionalDiscountCents,1333);
assert.equal(priced.discountCents,4233);
assert.equal(priced.finalCents,30100);
assert.equal(priced.eligibleCents,34333);
assert.equal(priced.baseIntact,true);
assert.deepEqual(priced.additionalItems.map(i=>i.id),['X','Y']);
assert(priced.planItemIds.includes('P')); // Incluído no Premium, mesmo ao escolher Plus.
const premiumOnly=snapshot.packages.premium.items.find(i=>i.id==='P');
const mixed=p.calculateSelection(snapshot,'plus',[...selection,premiumOnly],campaign,now);
assert.equal(mixed.regularCents,54333);
assert.equal(mixed.additionalDiscountCents,1333);
assert.equal(mixed.additionalRegularCents,5333);
assert.equal(mixed.eligibleCents,34333);
assert.equal(mixed.finalCents,50100); // P a preço de tabela, X/Y com desconto.
assert(!mixed.additionalItems.some(i=>i.id==='P'));
const crossPlan=[...snapshot.packages.essencial.items,
  snapshot.packages.plus.items.find(i=>i.id==='O'),premiumOnly];
const crossPriced=p.calculateSelection(snapshot,'essencial',crossPlan,campaign,now);
assert.equal(crossPriced.additionalDiscountCents,0);
assert.equal(crossPriced.additionalRegularCents,0);
assert.equal(crossPriced.finalCents,45300);
const changedMembership=JSON.parse(JSON.stringify(snapshot));
changedMembership.packages.premium.items.push(item('X','optional',5000));
assert.equal(p.calculateSelection(changedMembership,'plus',selection,campaign,now).additionalDiscountCents,83);
assert.equal(JSON.stringify({snapshot,selection,campaign}),original);
assert.deepEqual(JSON.parse(JSON.stringify(priced)),priced);
assert.equal(p.calculateSelection(snapshot,'plus',selection,campaign,now-1).discountCents,0);
assert.equal(p.calculateSelection(snapshot,'plus',selection,campaign,now+86400000).discountCents,0);
assert.equal(p.calculateSelection(snapshot,'plus',selection,null,now).discountCents,0);
const legacyCampaign={...campaign};delete legacyCampaign.additionalOptionalPercentage;
assert(p.validCampaign(legacyCampaign));
priced=p.calculateSelection(snapshot,'plus',selection,legacyCampaign,now);
assert.equal(priced.planDiscountCents,2900);
assert.equal(priced.additionalDiscountCents,0);
assert.equal(priced.additionalPercentage,0);
assert.equal(p.calculateCampaign(snapshot,'plus',campaign,now).finalCents,26100);
for(const bad of [-1,101,NaN,Infinity,null,'25']){
  const invalidCampaign={...campaign,additionalOptionalPercentage:bad};
  assert(!p.validCampaign(invalidCampaign));
  assert.equal(p.calculateSelection(snapshot,'plus',selection,invalidCampaign,now).discountCents,0);
}
const removed=selection.filter(i=>i.id!=='O');
priced=p.calculateSelection(snapshot,'plus',removed,campaign,now);
assert.equal(priced.baseIntact,false);
assert.equal(priced.discountCents,0);
assert.equal(priced.additionalPercentage,0);
const swapped=[...selection.filter(i=>i.id!=='V2'),item('V3','unique',6000)];
assert.equal(p.calculateSelection(snapshot,'plus',swapped,campaign,now).discountCents,0);
priced=p.calculateSelection(snapshot,'plus',[...selection,item('required-extra','required',1000)],campaign,now);
assert.equal(priced.additionalDiscountCents,1333);
assert.equal(priced.finalCents,31100);
const zero={...campaign,percentages:{essencial:0,plus:0,premium:0},additionalOptionalPercentage:0};
assert.equal(p.calculateSelection(snapshot,'plus',selection,zero,now).discountCents,0);
const maximum={...campaign,percentages:{essencial:100,plus:100,premium:100},additionalOptionalPercentage:100};
assert.equal(p.calculateSelection(snapshot,'plus',selection,maximum,now).finalCents,0);
assert.equal(p.discountedItem(item('B','required',100),50).discountCents,0);
assert.equal(p.discountedItem(item('V','unique',100),50).discountCents,0);
assert.equal(p.discountedItem(item('X','optional',101),12.5).discountCents,13);
const rounding={...campaign,additionalOptionalPercentage:50};
priced=p.calculateSelection(snapshot,'plus',[...snapshot.packages.plus.items,
  item('cent1','optional',1),item('cent2','optional',1)],rounding,now);
assert.equal(priced.additionalDiscountCents,2); // Arredondar cada feature, não a soma.
assert.throws(()=>p.calculateSelection(snapshot,'plus',[...selection,selection[0]],campaign,now),TypeError);
assert.throws(()=>p.calculateSelection(snapshot,'unknown',selection,campaign,now),TypeError);
assert.throws(()=>p.calculateSelection(snapshot,'plus',[item('bad','optional',-1)],campaign,now),TypeError);
assert.throws(()=>p.discountedItem(item('bad','optional',100),101),TypeError);
console.log('Promoções e opcionais adicionais: testes aprovados.');
