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
console.log('Promoções: 23 asserções aprovadas.');
