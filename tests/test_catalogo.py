"""Valida specs, dados incorporados e comportamento no Chrome headless."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "home.html").read_text()


class CatalogoTest(unittest.TestCase):
    def test_specs_e_somas(self):
        specs = [p for p in (ROOT / "specs").glob("*.md") if re.match(r"^[A-Z]+\d+-", p.name)]
        self.assertEqual(len(specs), 61)
        reviewed = 0
        for path in specs:
            text = path.read_text()
            if path.name.startswith("G02-"):
                self.assertIn("Sob cotação", text)
                continue
            rows = re.findall(r"^\| [A-Z]+\d+-T\d+[A-Z]? \| [^|\n]+ \| (\d+) \| Revisão técnica preliminar \|$", text, re.M)
            declared = re.search(r"\| \*\*Total\*\* \| \| \*\*(\d+) h\*\*", text)
            self.assertTrue(rows, path.name)
            self.assertEqual(sum(map(int, rows)), int(declared.group(1)), path.name)
            self.assertIn("## Cenário mínimo específico de aceite", text)
            reviewed += 1
        self.assertEqual(reviewed, 60)

    def test_browser(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        script = """
        window.confirm = () => true;
        const results = [];
        function check(name, ok) { results.push({name, ok}); }
        check('54 features', features.length === 54);
        check('fundação', foundationHours === 522);
        check('base', features.filter(f=>f.type==='required').reduce((s,f)=>s+f.hours,0) === 340);
        for (const [name, value] of [['essencial',178000],['plus',230000],['premium',389200]]) {
          applyPreset(name);
          check(name, targetTotal === value);
          const supportHours = {essencial:10,plus:15,premium:20}[name];
          check(name+' manutenção', document.getElementById('maintenanceHours').textContent === supportHours+' horas por mês');
          const expectedMonths = new Intl.NumberFormat('pt-BR', {maximumFractionDigits:2}).format((value / 200) / 352) + ' meses';
          check(name+' prazo para duas pessoas',el.estimatedMonths.textContent === expectedMonths && el.floatingDuration.textContent.includes(expectedMonths));
          check(name+' vídeo único',selectedFeatures().filter(f=>f.group==='curso_entrega').length===1);
          check(name+' dependências', selectedFeatures().every(f=>(prerequisites[f.id]||[]).every(id=>isSelected(getFeature(id)))));
        }
        applyPreset('essencial');
        toggleFeature('C02',true);
        check('privado puro',targetTotal===188400);
        toggleFeature('C03',true);
        check('offline sem duplicar',targetTotal===214000 && !state.selected.has('C02'));
        toggleFeature('C03',false);
        check('não esvaziar vídeo',state.selected.has('C03'));
        toggleFeature('G02',true);
        check('G02 bloqueada',!state.selected.has('G02'));
        toggleFeature('N02',true);
        check('incluir dependência',state.selected.has('N01'));
        toggleFeature('N01',false);
        check('remover dependentes',!state.selected.has('N02'));
        check('mockups',features.every(f=>{state.activePreview=f.id;renderPreview();return !!el.phoneScreen.querySelector('.app-screen');}));
        check('54 composições específicas',features.every(f=>specificMockContent(f)!==null));
        const semanticExamples={
          B05:'Receber promoções',A02:'Continuar com Google',A03:'Continuar com Microsoft',
          C01:'Player YouTube',C02:'Streaming privado',C03:'Download da aula',
          C06:'Revisão humana',C07:'Fonte ilustrativa',C08:'Comentários da aula',
          C09:'satisfação',G01:'Abrir convite do WhatsApp',G05:'Publicar meu perfil',
          EV02:'QR ilustrativo',EV04:'Enquadre o QR',P01:'Aguardando pagamento',
          P02:'Renovação',P03:'Comprar curso',P04:'Reserva temporária',
          P05:'Acesso restrito',P06:'Acesso restrito',P07:'Acesso restrito',
          L01:'Responsável',R01:'Visualizações de aulas',R02:'Exportar conclusões',
          R03:'18 avaliações',R04:'Deduplicação',R05:'Heartbeat',GM02:'Check-in'
        };
        check('conteúdo condiz com feature',Object.entries(semanticExamples).every(([id,text])=>{
          state.activePreview=id;renderPreview();return el.phoneScreen.textContent.includes(text);
        }));
        state.activePreview='B08';renderPreview();
        check('contexto administrativo',el.phoneScreen.querySelector('.app-screen').dataset.mockContext==='admin');
        applyPreset('essencial');
        const selectionBefore=[...state.selected].join(',');
        const priceBefore=targetTotal;
        check('opcionais apenas visualizadas',features.filter(f=>f.type==='optional'&&!f.unavailable).every(f=>{
          state.activePreview=f.id;renderPreview();return document.getElementById('liveMode').textContent==='Apenas visualização';
        }));
        check('preview não muda orçamento',selectionBefore===[...state.selected].join(',') && targetTotal===priceBefore);
        state.activePreview='B01';renderPreview();
        check('mural sem opcionais não contratados',!el.phoneScreen.textContent.includes('E-book em destaque')&&!el.phoneScreen.textContent.includes('Próximo evento'));
        applyPreset('premium');state.activePreview='B01';renderPreview();
        check('mural com opcionais contratados',el.phoneScreen.textContent.includes('E-book em destaque')&&el.phoneScreen.textContent.includes('Próximo evento'));
        state.activePreview='EV01';renderPreview();
        check('evento mostra complementos contratados',el.phoneScreen.textContent.includes('QR individual')&&el.phoneScreen.textContent.includes('Convite por e-mail'));
        check('marca nos 54 mockups',features.every(f=>{
          state.activePreview=f.id;renderPreview();
          return el.phoneScreen.querySelector('.app-brand img')?.alt==='ATSI+';
        }));
        check('título do produto',document.querySelector('h1').textContent==='Plataforma ATSI+');
        check('menu simplificado',document.getElementById('promotionSettings').querySelectorAll('input').length===5 &&
          !document.getElementById('settingsDialog').querySelector('input[type=file]'));
        check('menu abre e fecha',(()=>{
          document.getElementById('openSettings').click();
          const open=document.getElementById('settingsDialog').open;
          document.getElementById('closeSettings').click();
          return open&&!document.getElementById('settingsDialog').open;
        })());
        check('exportação com hierarquia de marca',quoteData().project.product==='ATSI+' && quoteData().project.client==='ATSI Brasil' && quoteData().project.developer==='YvyLab');
        applyPreset('essencial');state.activePreview='B04';renderPreview();
        check('certificados não contratados ausentes',!el.phoneScreen.textContent.includes('Meus certificados'));
        applyPreset('plus');state.activePreview='B04';renderPreview();
        check('certificados contratados presentes',el.phoneScreen.textContent.includes('Meus certificados'));
        openFeatureDetails(getFeature('C03'),document.querySelector('.feature-info'));
        check('popup revisado',document.getElementById('dialogContent').textContent.includes('208 h'));
        check('sem oferta automática',currentOffer===null && document.getElementById('offerClock').hidden);
        const offerStart=Date.now();
        const config=(ids,pct)=>({enabled:true,percentage:pct,eligibleFeatureIds:ids,
          maxDiscountCents:10000000,priceApproval:true,marginApproval:true});
        // Apenas cenário automatizado: percentuais nunca são pré-carregados no produto.
        currentOffer={schemaVersion:1,id:'test',quoteId:'test',author:'Test',configVersion:'test',
          status:'active',issuedAt:new Date(offerStart).toISOString(),
          expiresAt:new Date(offerStart+86400000).toISOString(),snapshot:pricingSnapshot(),
          config:{plus:config(['C04'],10),premium:config(['C04'],20)}};
        applyPreset('plus');
        check('oferta plus',targetTotal===229160 && !document.getElementById('offerClock').hidden);
        check('mensalidade preservada',quoteData().monthlyMaintenanceBRL===4000);
        check('exportação identifica oferta',quoteRows().some(row=>row[0]==='Cotação'&&row[1]==='test'));
        toggleFeature('A02',true);
        check('custom sem promoção',quoteData().pricing.discountCents===0);
        applyPreset('essencial');
        check('essencial sem promoção',targetTotal===178000);
        const clock=Date.now;
        Date.now=()=>offerStart+86400001;
        applyPreset('plus');
        check('expiração restaura preço',targetTotal===230000 && quoteData().offerStatus==='expired');
        check('vencimento não renovado',currentOffer.expiresAt===new Date(offerStart+86400000).toISOString());
        Date.now=clock;
        currentOffer=null;
        const asLocal=ms=>new Date(ms-3*3600000).toISOString().slice(0,16);
        document.getElementById('promotionStart').value=asLocal(Date.now()-3600000);
        document.getElementById('promotionEnd').value=asLocal(Date.now()+3600000);
        document.getElementById('discountEssencial').value=10;
        document.getElementById('discountPlus').value=15;
        document.getElementById('discountPremium').value=20;
        document.getElementById('promotionSettings').requestSubmit();
        applyPreset('essencial');
        check('salvar campanha e descontar essencial',targetTotal===160200 && campaignConfig.percentages.essencial===10);
        applyPreset('plus');
        check('campanha plus',targetTotal===195500);
        check('faixas promocionais nos três planos',document.querySelectorAll('.plan-offer del').length===3);
        check('timer compacto',document.getElementById('offerTitle').textContent==='Oferta' && !document.querySelector('.offer-box').hidden);
        check('campanha persistida',JSON.parse(localStorage.getItem(campaignStorageKey)).endsAt===campaignConfig.endsAt);
        check('horas e mensalidades preservadas',quoteData().monthlyMaintenanceBRL===4000 && el.totalHours.textContent==='1150 h');
        Date.now=()=>Date.parse(campaignConfig.endsAt)+1;
        render();
        check('faixas e timer somem ao expirar',document.querySelectorAll('.plan-offer').length===0 && document.querySelector('.offer-box').hidden);
        Date.now=clock;
        window.scrollTo({top:0,behavior:'instant'});
        const nativeRAF=window.requestAnimationFrame;
        let scrollFrame=null;
        window.requestAnimationFrame=callback=>{scrollFrame=callback;return 999999;};
        document.getElementById('viewPrice').click();
        if(scrollFrame)scrollFrame(performance.now()+1000);
        window.requestAnimationFrame=nativeRAF;
        const priceRect=el.totalPrice.getBoundingClientRect();
        check('um clique exibe valor',priceRect.top>=0 && priceRect.bottom<=innerHeight);
        document.body.insertAdjacentHTML('beforeend','<pre id="qa-results">'+JSON.stringify(results)+'</pre>');
        """
        page = HTML.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
        page = page.replace("</body>", f"<script>{script}</script></body>")
        with tempfile.TemporaryDirectory(prefix="atsi-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "test.html"
            file.write_text(page)
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--window-size=1440,1000", "--dump-dom", file.as_uri()
            ], capture_output=True, text=True, timeout=30)
        match = re.search(r'<pre id="qa-results">(\[.*?\])</pre>', run.stdout)
        self.assertIsNotNone(match, "Teste interrompido antes de gerar resultados")
        results = json.loads(match.group(1))
        for result in results:
            self.assertTrue(result["ok"], result["name"])
        print(f"Chrome: {len(results)} verificações de catálogo/seleção/preview aprovadas")


if __name__ == "__main__":
    unittest.main()
