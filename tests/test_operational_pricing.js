const assert=require('node:assert/strict');
const ops=require('../operational-pricing.js');
const calculate=(activeUsers,videoStrategy='C01',extra={})=>ops.calculate({activeUsers,videoStrategy,...extra});
const expected=[
  [100,10,0,73800,77400],
  [500,50,0,117000,135000],
  [1000,100,0,171000,207000],
  [2500,250,0,336000,426000],
  [5000,500,0,633000,813000],
  [10000,1000,0,1203000,1563000]
];
for(const [users,peak,...totals] of expected){
  ['C01','C02','C03'].forEach((video,index)=>{
    const result=calculate(users,video);
    assert.equal(result.totalCents,totals[index],`${users} / ${video}`);
    assert.equal(result.peakUsers,peak);
    assert.equal(result.lines.reduce((n,row)=>n+row.priceCents,0),result.totalCents);
    assert.equal(result.lines.reduce((n,row)=>n+row.amountCentsUSD,0),result.totalCentsUSD);
    assert.equal(result.lines.reduce((n,row)=>n+row.estimatedCents,0),result.totalEstimatedCents);
    assert.equal(result.billingPolicy,video==='C01'?'youtube_included_in_base':'estimated_surcharge');
    assert(result.explanation.includes('Manutenção do plano:'));
    assert(result.explanation.includes('Serviços e vídeos:'));
    assert(result.explanation.includes('não gera cobranças automáticas'));
    assert(result.explanation.includes('inteligência artificial é contratado separadamente'));
    assert.equal(result.explanation.split('\n\n').length,5);
    assert(!/adicional operacional|infraestrutura compartilhada|benchmark|câmbio/.test(result.explanation));
    if(video==='C01'){
      assert.equal(result.totalCents,0);
      assert(result.totalEstimatedCents>0);
      assert(result.lines.every(line=>line.priceCents===0));
      assert(result.explanation.includes('Com vídeos pelo YouTube, esse adicional é zero.'));
    }else assert.equal(result.totalEstimatedCents,result.totalCents);
    assert.equal(new Set(result.lines.map(row=>row.id)).size,result.lines.length);
    assert.equal(result.version,ops.version);
    assert.equal(result.inputs.activeUsers,users);
    assert.equal(result.sources.length,6);
  });
}
assert.deepEqual(Object.values(ops.plans).map(plan=>[plan.priceCents,plan.hours]),
  [[300000,10],[400000,15],[500000,20]]);
for(const video of ['C01','C02','C03']){
  let previous=0;
  for(let users=100;users<=10000;users+=100){
    const result=calculate(users,video);
    assert(result.totalCents>=previous);
    previous=result.totalCents;
  }
}
const row=(result,id)=>result.lines.find(line=>line.id===id);
const youtube=calculate(1000,'C01');
assert.equal(youtube.storageMinutes+youtube.streamingMinutes+youtube.downloadMinutes,0);
assert.equal(row(youtube,'videoStorage').priceCents,0);
const privateVideo=calculate(1000,'C02'),offline=calculate(1000,'C03');
assert.equal(privateVideo.totalCentsUSD,28500);
assert.equal(privateVideo.streamingMinutes,180000);
assert.equal(privateVideo.storageMinutes,6000);
assert.equal(row(privateVideo,'videoStorage').amountCentsUSD,3000);
assert.equal(row(privateVideo,'videoDelivery').amountCentsUSD,18000);
assert.equal(offline.totalCents-privateVideo.totalCents,36000);
assert.equal(offline.downloadMinutes,60000);
assert.equal(row(offline,'videoStorage').priceCents,row(privateVideo,'videoStorage').priceCents);
assert.equal(calculate(1000,'C03',{offlineMinutesPerUser:0}).totalCents,privateVideo.totalCents);
assert.equal(calculate(1000,'C02',{videoMinutesPerUser:0,libraryHours:0}).totalCents,youtube.totalEstimatedCents);
assert.equal(row(calculate(100,'C02',{libraryHours:17}),'videoStorage').amountCentsUSD,1000);
assert.equal(row(calculate(1000,'C01'),'database').amountCentsUSD,3500);
assert.equal(row(youtube,'database').estimatedCents,21000);
assert.equal(row(youtube,'database').coveredByBase,true);
assert.equal(row(youtube,'database').priceCents,0);
assert.equal(row(calculate(1001,'C01'),'database').amountCentsUSD,4000);
assert.equal(row(calculate(10000,'C01'),'realtime').amountCentsUSD,0);
assert.equal(row(calculate(5000,'C01',{realtimeEnabled:true}),'realtime').amountCentsUSD,0);
assert.equal(row(calculate(10000,'C01',{realtimeEnabled:true}),'realtime').amountCentsUSD,1000);
assert.equal(row(calculate(10000,'C01',{realtimeEnabled:true,peakPercentage:100}),'realtime').amountCentsUSD,10000);
assert.equal(calculate(10000,'C01',{peakPercentage:100}).computeProfile,'XL');
assert.equal(calculate(10000,'C01',{realtimeEnabled:true,peakPercentage:100,exchangeRate:100}).totalCents,0);
const input={activeUsers:100,videoStrategy:'C03',exchangeRate:5.37,offlineMinutesPerUser:1,videoMinutesPerUser:1};
const before=JSON.stringify(input),rounded=ops.calculate(input);
assert.equal(JSON.stringify(input),before);
rounded.lines.forEach(line=>assert.equal(line.priceCents,Math.round(line.amountCentsUSD*537/100)));
assert.equal(calculate(1000,'C02',{exchangeRate:3}).totalCents,privateVideo.totalCents/2);
for(const invalid of [
  {activeUsers:0},{activeUsers:99},{activeUsers:10001},{activeUsers:100.5},{activeUsers:'100'},
  {activeUsers:NaN},{activeUsers:Infinity},{exchangeRate:0},{exchangeRate:101},{exchangeRate:6.123},
  {exchangeRate:'6'},{exchangeRate:NaN},{peakPercentage:0},{peakPercentage:101},{peakPercentage:2.5},
  {videoMinutesPerUser:-1},{videoMinutesPerUser:6001},{libraryHours:10001},{libraryHours:0.5},
  {offlineMinutesPerUser:-1},{offlineMinutesPerUser:6001},{realtimeEnabled:'true'},
  {videoStrategy:'invalid'},{videoStrategy:null}
])assert.throws(()=>calculate(100,'C01',invalid),JSON.stringify(invalid));
assert.throws(()=>ops.calculate(),/vídeo/);
console.log('Operação: cenários, tarifas, câmbio, arredondamento, exclusividade e entradas inválidas aprovados.');
