/* Núcleo local: valores em centavos. Não é autoridade comercial nem autenticação. */
(function(root){
  'use strict';
  function money(n){ return Number.isSafeInteger(n) && n >= 0; }
  function regular(pack){
    return pack.foundationCents + pack.items.reduce((sum,item)=>sum+item.priceCents,0);
  }
  function validSnapshot(snapshot){
    if (!snapshot || snapshot.schemaVersion !== 1 || !snapshot.priceListVersion || !snapshot.packages) return false;
    return ['essencial','plus','premium'].every(key=>{
      const p=snapshot.packages[key];
      return p && money(p.foundationCents) && Array.isArray(p.items) &&
        p.items.every(i=>i && typeof i.id==='string' && money(i.priceCents) &&
          ['required','optional','unique'].includes(i.type)) &&
        new Set(p.items.map(i=>i.id)).size===p.items.length &&
        money(regular(p));
    });
  }
  function validOffer(offer){
    if (!offer || offer.schemaVersion!==1 || typeof offer.id!=='string' ||
        typeof offer.quoteId!=='string' || !offer.quoteId.trim() ||
        typeof offer.author!=='string' || !offer.author.trim() || !offer.configVersion ||
        !['active','cancelled'].includes(offer.status) || !offer.config || !validSnapshot(offer.snapshot)) return false;
    const start=Date.parse(offer.issuedAt), end=Date.parse(offer.expiresAt);
    if (!Number.isFinite(start) || end-start!==86400000) return false;
    return ['plus','premium'].some(key=>offer.config[key]?.enabled) && ['plus','premium'].every(key=>{
      const c=offer.config[key], pack=offer.snapshot.packages[key];
      return c && typeof c.enabled==='boolean' &&
        (c.percentage===null || (Number.isFinite(c.percentage)&&c.percentage>=0&&c.percentage<=100)) &&
        money(c.maxDiscountCents) && Array.isArray(c.eligibleFeatureIds) &&
        new Set(c.eligibleFeatureIds).size===c.eligibleFeatureIds.length &&
        c.eligibleFeatureIds.every(id=>pack.items.some(i=>i.id===id && i.type==='optional')) &&
        (!c.enabled || (c.percentage>0 && c.priceApproval===true && c.marginApproval===true));
    });
  }
  function status(offer, snapshot, now=Date.now()){
    if (!offer) return 'unavailable';
    if (!validOffer(offer)) return 'invalid';
    if (offer.status==='cancelled') return 'cancelled';
    if (JSON.stringify(offer.snapshot)!==JSON.stringify(snapshot)) return 'catalog_changed';
    if (now < Date.parse(offer.issuedAt)) return 'scheduled';
    return now>=Date.parse(offer.expiresAt) ? 'expired' : 'active';
  }
  function calculate(snapshot,key,offer,now=Date.now()){
    const pack=snapshot.packages[key];
    const total=regular(pack);
    const result={regularCents:total,eligibleCents:0,discountCents:0,finalCents:total,effectivePct:0};
    if (!['plus','premium'].includes(key) || status(offer,snapshot,now)!=='active') return result;
    const config=offer.config[key];
    if (!config.enabled) return result;
    result.eligibleCents=pack.items.filter(i=>i.type==='optional' && config.eligibleFeatureIds.includes(i.id))
      .reduce((sum,i)=>sum+i.priceCents,0);
    const requested=Math.round(result.eligibleCents*config.percentage/100);
    // Bloqueio, não redução silenciosa.
    if (requested<=0 || requested>config.maxDiscountCents) return {...result,blocked:true};
    result.discountCents=requested;
    result.finalCents=total-requested;
    result.effectivePct=100*requested/total;
    return result;
  }
  function validCampaign(c){
    return !!c && c.schemaVersion===2 && Number.isFinite(Date.parse(c.startsAt)) &&
      Number.isFinite(Date.parse(c.endsAt)) && Date.parse(c.endsAt)>Date.parse(c.startsAt) &&
      !!c.percentages && ['essencial','plus','premium'].every(key=>
        Number.isFinite(c.percentages[key]) && c.percentages[key]>=0 && c.percentages[key]<=100);
  }
  function campaignStatus(c,now=Date.now()){
    if(!c)return 'unavailable';
    if(!validCampaign(c))return 'invalid';
    if(now<Date.parse(c.startsAt))return 'scheduled';
    return now>=Date.parse(c.endsAt)?'expired':'active';
  }
  function calculateCampaign(snapshot,key,c,now=Date.now()){
    const total=regular(snapshot.packages[key]);
    const pct=campaignStatus(c,now)==='active'?c.percentages[key]:0;
    const discount=Math.round(total*pct/100);
    return {regularCents:total,eligibleCents:pct>0?total:0,discountCents:discount,
      finalCents:total-discount,effectivePct:pct};
  }
  const api={regular,validSnapshot,validOffer,status,calculate,validCampaign,campaignStatus,calculateCampaign};
  root.ATSIPromotion=api;
  if (typeof module!=='undefined') module.exports=api;
})(globalThis);
