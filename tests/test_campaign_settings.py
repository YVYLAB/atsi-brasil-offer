import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CampaignSettingsTest(unittest.TestCase):
    def test_browser_settings(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        key = re.search(r"const releaseHash='([a-f0-9]{64})'", (ROOT / "campaign-settings.js").read_text()).group(1)
        script = """
        (async()=>{
          const checks=[];
          const check=(name,ok)=>checks.push({name,ok});
          const hash=document.getElementById('discountReleaseHash');
          const fields=document.getElementById('discountFields');
          const form=document.getElementById('promotionSettings');
          const access=document.getElementById('discountAccessForm');
          const fileInput=document.getElementById('discountSettingsFile');
          const feedback=document.getElementById('settingsStatus');
          const exportButton=document.getElementById('exportDiscountSettings');
          let downloaded=null;
          window.downloadJSON=(data,name)=>{downloaded={data,name};};
          function populate(){
            const local=ms=>new Date(ms-3*3600000).toISOString().slice(0,16);
            document.getElementById('promotionStart').value=local(Date.now()-3600000);
            document.getElementById('promotionEnd').value=local(Date.now()+3600000);
            document.getElementById('discountEssencial').value=10;
            document.getElementById('discountPlus').value=15;
            document.getElementById('discountPremium').value=20;
            document.getElementById('discountAdditionalOptional').value=25;
          }
          async function loadFile(text){
            const transfer=new DataTransfer();
            transfer.items.add(new File([text],'oferta.json',{type:'application/json'}));
            const done=new Promise(resolve=>{
              const observer=new MutationObserver(()=>{
                if(!feedback.textContent.startsWith('Carregando')){
                  observer.disconnect();resolve();
                }
              });
              observer.observe(feedback,{childList:true,subtree:true,characterData:true});
            });
            fileInput.files=transfer.files;
            fileInput.dispatchEvent(new Event('change',{bubbles:true}));
            await done;
          }
          async function save(){
            const closed=new Promise(resolve=>settingsDialog.addEventListener('close',resolve,{once:true}));
            form.requestSubmit();await closed;
          }
          const values=()=>[hash.value,...form.querySelectorAll('input')].map(v=>typeof v==='string'?v:v.value).join('|');
          document.getElementById('openSettings').click();
          check('bloqueado inicialmente',fields.disabled && exportButton.disabled && !campaignConfig);
          check('carregar disponível sem hash',!document.getElementById('importDiscountSettings').disabled);
          populate();form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));
          check('submit bloqueado sem hash',campaignConfig===null && localStorage.getItem(campaignStorageKey)===null);
          hash.value='incorreto';access.requestSubmit();
          check('hash incorreto não libera',fields.disabled && exportButton.disabled);
          hash.value='TEST_RELEASE_HASH';access.requestSubmit();
          check('hash correto libera campos e download',!fields.disabled && !exportButton.disabled);
          exportButton.click();
          check('exporta campos atuais e hash',downloaded && downloaded.name==='atsi-configuracao-descontos.json' &&
            downloaded.data.releaseHash===hash.value && downloaded.data.campaign.percentages.plus===15 &&
            downloaded.data.campaign.additionalOptionalPercentage===25);
          check('download não aplica ou persiste',campaignConfig===null && targetTotal===178000 &&
            localStorage.getItem(campaignStorageKey)===null);
          const payload=JSON.parse(JSON.stringify(downloaded.data));
          hash.value='alterado';hash.dispatchEvent(new Event('input',{bubbles:true}));
          check('editar hash bloqueia novamente',fields.disabled && exportButton.disabled);
          hash.value='TEST_RELEASE_HASH';access.requestSubmit();
          await save();
          check('salva somente após confirmação',targetTotal===160200 && campaignConfig.percentages.essencial===10);
          check('fechar limpa hash e bloqueia',hash.value==='' && fields.disabled && exportButton.disabled);
          check('hash fora da persistência e proposta',!localStorage.getItem(campaignStorageKey).includes(payload.releaseHash) &&
            !JSON.stringify(quoteData()).includes(payload.releaseHash));
          document.getElementById('openSettings').click();
          const beforeInvalid=values(),stored=localStorage.getItem(campaignStorageKey);
          await loadFile(JSON.stringify({...payload,releaseHash:'outra-chave'}));
          check('arquivo com outro hash rejeitado sem alterações',values()===beforeInvalid && fields.disabled &&
            localStorage.getItem(campaignStorageKey)===stored && targetTotal===160200);
          await loadFile('{');
          check('JSON corrompido não altera campos',values()===beforeInvalid && fields.disabled);
          await loadFile(' '.repeat(ATSICampaignSettings.maxFileBytes+1));
          check('arquivo grande recusado',feedback.textContent.includes('64 KB') && values()===beforeInvalid);
          payload.campaign.percentages.essencial=30;
          payload.campaign.startsAt=new Date(Date.now()-3600000).toISOString();
          payload.campaign.endsAt=new Date(Date.now()+3600000).toISOString();
          await loadFile(JSON.stringify(payload));
          check('importação preenche hash e percentuais',hash.value===payload.releaseHash && !fields.disabled &&
            document.getElementById('discountEssencial').value==='30' &&
            document.getElementById('discountAdditionalOptional').value==='25');
          check('importação preserva datas com segundos',new Date(document.getElementById('promotionStart').value+'-03:00').toISOString()===payload.campaign.startsAt &&
            new Date(document.getElementById('promotionEnd').value+'-03:00').toISOString()===payload.campaign.endsAt);
          check('importação não aplica automaticamente',campaignConfig.percentages.essencial===10 &&
            localStorage.getItem(campaignStorageKey)===stored && targetTotal===160200);
          downloaded=null;exportButton.click();
          check('ida e volta sem perda',JSON.stringify(downloaded.data.campaign)===JSON.stringify(payload.campaign) &&
            downloaded.data.releaseHash===payload.releaseHash);
          await save();
          check('salvar importado aplica desconto',targetTotal===124600 &&
            campaignConfig.startsAt===payload.campaign.startsAt && campaignConfig.endsAt===payload.campaign.endsAt);
          document.getElementById('openSettings').click();
          delete payload.campaign.additionalOptionalPercentage;
          await loadFile(JSON.stringify(payload));
          check('campo adicional ausente vira zero',document.getElementById('discountAdditionalOptional').value==='0');
          check('importação permite selecionar o mesmo arquivo novamente',fileInput.value==='');
          document.body.insertAdjacentHTML('beforeend','<pre id="qa-settings">'+JSON.stringify(checks)+'</pre>');
        })();
        """.replace("TEST_RELEASE_HASH", key)
        page = (ROOT / "home.html").read_text()
        page = page.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
        page = page.replace("    initOffers();", "    localStorage.removeItem(campaignStorageKey);\n    initOffers();", 1)
        page = page.replace("</body>", f"<script>{script}</script></body>")
        with tempfile.TemporaryDirectory(prefix="atsi-settings-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "test.html"
            file.write_text(page)
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--virtual-time-budget=5000",
                "--dump-dom", file.as_uri()
            ], capture_output=True, text=True, timeout=30)
        match = re.search(r'<pre id="qa-settings">(\[.*?\])</pre>', run.stdout)
        self.assertIsNotNone(match, "Fluxo de configuração não completou")
        results = json.loads(match.group(1))
        for check in results:
            self.assertTrue(check["ok"], check["name"])
        print(f"Chrome: {len(results)} verificações de hash/importação/exportação aprovadas")
