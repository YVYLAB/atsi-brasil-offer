const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const settings=require('../campaign-settings.js');
const source=fs.readFileSync(path.join(__dirname,'../campaign-settings.js'),'utf8');
const hash=source.match(/const releaseHash='([a-f0-9]{64})'/)[1];
const campaign={schemaVersion:2,startsAt:'2026-11-17T12:34:56.123Z',endsAt:'2026-11-19T20:12:34.456Z',
  percentages:{essencial:10,plus:15,premium:20},additionalOptionalPercentage:25};
assert(settings.isAuthorized(hash));
assert(settings.isAuthorized(' '+hash.toUpperCase()+' '));
assert(!settings.isAuthorized('wrong'));
assert(!settings.isAuthorized(null));
const before=JSON.stringify(campaign);
const file=settings.createFile(campaign,hash);
assert.equal(file.releaseHash,hash);
assert.equal(file.schemaVersion,1);
assert.equal(file.kind,'atsi-discount-settings');
assert.deepEqual(file.campaign,campaign);
assert.equal(JSON.stringify(campaign),before);
assert.deepEqual(settings.parseFile(JSON.stringify(file)),{releaseHash:hash,campaign});
assert.deepEqual(settings.parseFile('\uFEFF'+JSON.stringify(file)),{releaseHash:hash,campaign});
assert.throws(()=>settings.createFile(campaign,'wrong'),/hash/);
assert.throws(()=>settings.parseFile(JSON.stringify({...file,releaseHash:'wrong',expectedHash:'wrong'})),/hash/);
assert(settings.isAuthorized(hash)); // O arquivo não muda a chave esperada.
for(const data of [null,[],{},campaign,{...file,kind:'other'},{...file,schemaVersion:99}]){
  assert.throws(()=>settings.parseFile(JSON.stringify(data)));
}
assert.throws(()=>settings.parseFile('{'));
assert.throws(()=>settings.parseFile(' '.repeat(settings.maxFileBytes+1)));
assert.throws(()=>settings.parseFile('"'+ 'é'.repeat(settings.maxFileBytes/2) +'"'));
for(const invalid of [-1,101,'10',null,NaN]){
  assert.throws(()=>settings.createFile({...campaign,percentages:{...campaign.percentages,plus:invalid}},hash));
}
assert.throws(()=>settings.createFile({...campaign,additionalOptionalPercentage:101},hash));
assert.throws(()=>settings.createFile({...campaign,endsAt:campaign.startsAt},hash));
assert.throws(()=>settings.createFile({...campaign,startsAt:'2026-02-30T12:00:00.000Z'},hash));
assert.throws(()=>settings.createFile({...campaign,startsAt:'2026-11-17'},hash));
const legacy={...campaign};delete legacy.additionalOptionalPercentage;
assert.equal(settings.createFile(legacy,hash).campaign.additionalOptionalPercentage,0);
const cleaned=settings.parseFile(JSON.stringify({...file,evil:'ignored',
  campaign:{...campaign,releaseHash:'wrong',arbitraryValue:1}}));
assert.deepEqual(cleaned,{releaseHash:hash,campaign});
const edge={...campaign,percentages:{essencial:0,plus:100,premium:12.5},additionalOptionalPercentage:0};
assert.deepEqual(settings.parseFile(JSON.stringify(settings.createFile(edge,hash))).campaign,edge);
console.log('Configurações: liberação, JSON, validação e ida e volta aprovados.');
