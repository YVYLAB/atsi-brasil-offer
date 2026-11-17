/* Liberação visual e transporte local. Não autentica nem publica configurações. */
(function(root){
  'use strict';
  const promotion=root.ATSIPromotion || (typeof module!=='undefined'?require('./pricing-promotion.js'):null);
  const releaseHash='10ef47ecf8ba5aaee293a3e54d5618f81da4e5f27b073f43268fac8675c54b90';
  const maxFileBytes=64*1024;
  function isAuthorized(value){
    return typeof value==='string' && value.trim().toLowerCase()===releaseHash;
  }
  function normalizeCampaign(value){
    const iso=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;
    if(!promotion.validCampaign(value) ||
      typeof value.startsAt!=='string' || typeof value.endsAt!=='string' ||
      !iso.test(value.startsAt) || !iso.test(value.endsAt))
      throw new Error('Confira as datas e os percentuais da configuração.');
    const result={schemaVersion:2,
      startsAt:new Date(value.startsAt).toISOString(),endsAt:new Date(value.endsAt).toISOString(),
      percentages:{essencial:value.percentages.essencial,plus:value.percentages.plus,premium:value.percentages.premium},
      additionalOptionalPercentage:value.additionalOptionalPercentage===undefined?0:value.additionalOptionalPercentage};
    // Impedir que datas inexistentes sejam corrigidas silenciosamente pelo navegador.
    if(result.startsAt.slice(0,19)!==value.startsAt.slice(0,19) ||
      result.endsAt.slice(0,19)!==value.endsAt.slice(0,19))
      throw new Error('Use datas válidas para o início e o fim da oferta.');
    return result;
  }
  function createFile(campaign,hash){
    if(!isAuthorized(hash))throw new Error('Informe um hash de liberação válido para continuar.');
    return {kind:'atsi-discount-settings',schemaVersion:1,releaseHash,
      exportedAt:new Date().toISOString(),campaign:normalizeCampaign(campaign)};
  }
  function parseFile(text){
    if(typeof text!=='string' || new TextEncoder().encode(text).length>maxFileBytes)
      throw new Error('Escolha um arquivo JSON de até 64 KB.');
    let data;
    try{data=JSON.parse(text.replace(/^\uFEFF/,''));}
    catch(error){throw new Error('Não foi possível ler o arquivo. Escolha uma configuração JSON válida.');}
    if(!data || Array.isArray(data) || data.kind!=='atsi-discount-settings' || data.schemaVersion!==1)
      throw new Error('Escolha um arquivo exportado pelas configurações da ATSI+.');
    if(!isAuthorized(data.releaseHash))throw new Error('O hash deste arquivo não corresponde à liberação da ATSI+.');
    return {releaseHash,campaign:normalizeCampaign(data.campaign)};
  }
  const api={isAuthorized,normalizeCampaign,createFile,parseFile,maxFileBytes};
  root.ATSICampaignSettings=api;
  if(typeof module!=='undefined')module.exports=api;
})(globalThis);
