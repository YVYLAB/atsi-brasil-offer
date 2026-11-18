"""Slider mensal: estado, exports/PDF, promoções e layout em file://."""
import html
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OperationalPricingTest(unittest.TestCase):
    def run_browser(self, script, width=1440):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        page = (ROOT / "home.html").read_text()
        page = page.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
        script = """
        window.qaOperationsPromise=(async()=>{
        const checks=[];
        function check(name,ok){checks.push({name,ok});}
        window.addEventListener('error',event=>check('sem erros JS: '+event.message,false));
        await document.fonts.ready;
        try {
        """ + script + """
        }catch(error){check('exceção: '+error.message,false);}
        return checks;
        })();
        """
        page = page.replace("</body>", f"<script>{script}</script></body>")
        with tempfile.TemporaryDirectory(prefix="atsi-operations-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "test.html"
            file.write_text(page)
            wrapper = Path(directory) / "layout.html"
            wrapper.write_text("""<!doctype html><body><script>
            (async()=>{
              const frame=document.createElement('iframe');frame.style.width='WIDTHpx';frame.style.height='1000px';
               frame.src='test.html?company=atsi-brasil';const loaded=new Promise(resolve=>frame.onload=resolve);
              document.body.append(frame);await loaded;
              const checks=await frame.contentWindow.qaOperationsPromise;
              checks.push({name:'viewport real',ok:frame.contentWindow.innerWidth===WIDTH});
              const output=document.createElement('pre');output.id='qa-operations';
              output.textContent=JSON.stringify(checks);document.body.append(output);
            })();
            </script></body>""".replace("WIDTH", str(width)))
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--allow-file-access-from-files",
                "--virtual-time-budget=5000", "--dump-dom", wrapper.as_uri()
            ], capture_output=True, text=True, timeout=45)
            match = re.search(r'<pre id="qa-operations">(.*?)</pre>', run.stdout, re.S)
            self.assertIsNotNone(match, "O teste não completou")
            results = json.loads(html.unescape(match.group(1)))
            self.assertTrue(results)
            for item in results:
                self.assertTrue(item["ok"], item["name"])

    def test_slider_exports_and_promotions(self):
        self.run_browser("""
        const slider=document.getElementById('monthlyActiveUsers');
        function users(value){slider.value=value;slider.dispatchEvent(new Event('input',{bubbles:true}));}
        function input(id,value){const node=document.getElementById(id);node.value=value;
          node.dispatchEvent(new Event('input',{bubbles:true}));return node;}
        const start=quoteData();
        check('faixa e semântica do slider',slider.min==='100'&&slider.max==='10000'&&slider.step==='100'&&
          !!document.querySelector('label[for="monthlyActiveUsers"]'));
        check('cenário inicial',start.monthlyMaintenanceBRL===3000&&start.monthlyOperationalBRL===0&&
          start.monthlyTotalBRL===3000&&start.operations.peakUsers===10);
        const explanation=document.getElementById('maintenanceExplanation');
        check('explicação logo abaixo da mensalidade',explanation.previousElementSibling.querySelector('#maintenancePrice')&&
          explanation.textContent.includes('Com vídeos pelo YouTube, esse adicional é zero.')&&
          explanation.textContent.includes('vídeos privados'));
        check('explicação organizada sem jargão',explanation.querySelector('h4').textContent==='O que compõe sua mensalidade?'&&
          explanation.querySelectorAll('p').length===5&&explanation.querySelectorAll('strong').length===3&&
          !/adicional operacional|infraestrutura compartilhada|benchmark|câmbio/.test(explanation.textContent));
        check('regras de manutenção claras',explanation.textContent.includes('horas mensais contratadas')&&
          explanation.textContent.includes('antes da execução')&&
          explanation.textContent.includes('não gera cobranças automáticas')&&
          explanation.textContent.includes('inteligência artificial é contratado separadamente'));
        check('rótulos comerciais simples',document.getElementById('maintenanceBasePrice').previousElementSibling.textContent==='Manutenção do plano'&&
          document.getElementById('operationalPrice').previousElementSibling.textContent==='Serviços e vídeos — valor estimado');
        const advanced=document.getElementById('operationalPeak').closest('details');
        check('pico e câmbio recolhidos',advanced&&!advanced.open&&advanced.contains(document.getElementById('operationalExchange')));
        check('franquia sem repetição',document.querySelectorAll('#maintenanceHours').length===1&&
          document.getElementById('maintenanceHours').textContent==='10 horas por mês');
        const selected=[...state.selected].join(','),snapshot=JSON.stringify(pricingSnapshot());
        users(1000);
        check('slider não muda implantação nem preset',state.activePreset==='essencial'&&
          selected===[...state.selected].join(',')&&snapshot===JSON.stringify(pricingSnapshot())&&
          quoteData().pricing.finalCents===17800000);
        check('texto acessível atualizado',slider.getAttribute('aria-valuetext').includes('1.000')&&
          document.getElementById('monthlyActiveUsersValue').textContent==='1.000 usuários ativos/mês');
        applyPreset('plus');
        let q=quoteData(),pdf=buildOfferPDFModel();
        check('trocar preset preserva usuários e ajusta operação',q.operations.inputs.activeUsers===1000&&
          q.operations.inputs.videoStrategy==='C02'&&q.monthlyMaintenanceBRL===4000&&
          q.monthlyOperationalBRL===1710&&q.monthlyTotalBRL===5710&&q.monthlyHours===15);
        check('resumo fecha com dados',document.getElementById('maintenancePrice').textContent===brl(q.monthlyTotalBRL)&&
          document.getElementById('maintenanceBasePrice').textContent===brl(4000)&&
          document.getElementById('operationalPrice').textContent===brl(1710));
        check('explicação de vídeos acompanha escolha',explanation.textContent.includes('pode crescer principalmente')&&
          explanation.textContent.includes('YouTube'));
        check('PDF congela cenário e separa base',pdf.support.priceCents===400000&&pdf.support.totalCents===571000&&
          JSON.stringify(pdf.support.operations)===JSON.stringify(q.operations));
        users(10000);
        check('snapshot PDF imutável',pdf.support.totalCents===571000&&pdf.support.operations.inputs.activeUsers===1000);
        applyPreset('premium');
        check('máximo premium offline',quoteData().monthlyTotalBRL===20630&&quoteData().operations.downloadMinutes===600000);
        users(1000);toggleFeature('C02',true);
        check('vídeo é escolha única no custo mensal',quoteData().operations.inputs.videoStrategy==='C02'&&
          quoteData().monthlyMaintenanceBRL===5000&&quoteData().monthlyOperationalBRL===1710&&
          quoteData().operations.downloadMinutes===0&&document.getElementById('operationalOfflineMinutes').disabled);
        toggleFeature('C01',true);
        check('YouTube zera todo adicional, preserva base de origem',quoteData().monthlyOperationalBRL===0&&
          quoteData().monthlyTotalBRL===5000&&quoteData().operations.totalEstimatedCents===45000&&
          document.getElementById('operationalVideoMinutes').disabled&&
          document.getElementById('operationalLibraryHours').disabled);
        const youtubePDF=buildOfferPDFModel();
        check('YouTube zerado também no PDF e exports',youtubePDF.support.operations.totalCents===0&&
          youtubePDF.support.totalCents===500000&&youtubePDF.support.operations.totalEstimatedCents===45000&&
          quoteRows().some(row=>row[0]==='Serviços e vídeos — valor estimado'&&row[1]===brl(0)));
        users(10000);
        check('YouTube segue zerado no maior volume',quoteData().monthlyOperationalBRL===0&&
          quoteData().monthlyTotalBRL===5000&&document.getElementById('operationalPrice').textContent===brl(0));
        users(1000);
        input('operationalExchange','3');
        check('câmbio muda custo de referência, não cobra adicional YouTube',quoteData().monthlyOperationalBRL===0&&
          quoteData().operations.totalEstimatedCents===22500&&quoteData().monthlyMaintenanceBRL===5000);
        const invalid=input('operationalExchange','');
        check('inválido mantém cálculo e avisa',quoteData().operations.inputs.exchangeRate===3&&!invalid.validity.valid&&
          document.getElementById('operationalInputStatus').textContent.includes('último valor válido'));
        invalid.dispatchEvent(new Event('change'));
        check('campo restaurado ao sair',invalid.value==='3'&&invalid.validity.valid);
        input('operationalExchange','6');
        input('operationalPeakPercentage','20');
        check('pico é premissa independente',quoteData().operations.peakUsers===200&&
          document.getElementById('operationalPeak').textContent.includes('não capacidade garantida'));
        input('operationalPeakPercentage','10');
        applyPreset('plus');
        input('operationalVideoMinutes','0');input('operationalLibraryHours','0');
        check('consumo pode ser ajustado',quoteData().monthlyOperationalBRL===450);
        input('operationalVideoMinutes','180');input('operationalLibraryHours','100');
        const withoutPromotion=quoteData().monthlyTotalBRL;
        campaignConfig={schemaVersion:2,startsAt:new Date(Date.now()-3600000).toISOString(),
          endsAt:new Date(Date.now()+3600000).toISOString(),
          percentages:{essencial:10,plus:15,premium:20},additionalOptionalPercentage:25};
        render();
        check('promoção não desconta mensalidade',quoteData().pricing.discountCents>0&&
          quoteData().monthlyTotalBRL===withoutPromotion);
        toggleFeature('A04',true);
        check('opcional sem consumo não duplica infraestrutura',quoteData().monthlyTotalBRL===withoutPromotion);
        users(10000);toggleFeature('G04',true);
        check('chat ativa somente seu excedente compartilhado',quoteData().operations.realtimeConnections===1000&&
          quoteData().operations.lines.find(line=>line.id==='realtime').priceCents===6000&&
          quoteData().monthlyOperationalBRL===12090);
        q=quoteData();pdf=buildOfferPDFModel();
        check('CSV e impressão recebem totais e premissas',quoteRows().some(row=>row[0]==='Total mensal estimado'&&row[1]===brl(q.monthlyTotalBRL))&&
          quoteRows().some(row=>row[0]==='Premissa operacional'&&row[1].includes('Câmbio'))&&
          quoteRows().some(row=>row[0]==='Fonte de tarifa'));
        check('modelo PDF reconcilia mensalidade',pdf.support.totalCents===pdf.support.priceCents+
          pdf.support.operations.lines.reduce((n,row)=>n+row.priceCents,0));
        check('sem texto antigo de operação incluída',!document.querySelector('.page').textContent.includes('Inclui os custos operacionais da plataforma.'));
        check('sem persistência escondida',!localStorage.getItem('atsi-operations-v1'));
        """)

    def test_video_controls_surcharge_independently_of_plan(self):
        self.run_browser("""
        for(const plan of ['essencial','plus','premium']){
          for(const activeUsers of [100,1000,10000]){
            applyPreset(plan);
            const slider=document.getElementById('monthlyActiveUsers');
            slider.value=activeUsers;slider.dispatchEvent(new Event('input',{bubbles:true}));
            for(const strategy of ['C01','C02','C03','C01']){
              const radio=document.querySelector(`[data-feature="${strategy}"] .feature-toggle`);
              radio.click();
              const q=quoteData(),pdf=buildOfferPDFModel();
              const base=ATSIOperations.plans[plan].priceCents;
              const expected=ATSIOperations.calculate({...state.operations,
                videoStrategy:strategy,realtimeEnabled:state.selected.has('G04')});
              const label=plan+' / '+activeUsers+' usuários / '+strategy;
              check(label+' usa seleção de vídeo, não preset',
                q.operations.inputs.videoStrategy===strategy &&
                q.monthlyOperationalBRL*100===expected.totalCents &&
                selectedFeatures().filter(f=>f.group==='curso_entrega').length===1);
              check(label+' preserva manutenção base',
                q.monthlyMaintenanceBRL*100===base && state.maintenancePlan===plan &&
                q.monthlyTotalBRL*100===base+expected.totalCents);
              check(label+' política por estratégia',
                strategy==='C01'?
                  q.operations.billingPolicy==='youtube_included_in_base' &&
                  q.monthlyOperationalBRL===0 && q.operations.totalEstimatedCents>0:
                  q.operations.billingPolicy==='estimated_surcharge' && q.monthlyOperationalBRL>0);
              check(label+' tela atualiza imediatamente',
                document.getElementById('operationalPrice').textContent===brl(expected.totalCents/100) &&
                document.getElementById('maintenancePrice').textContent===brl((base+expected.totalCents)/100) &&
                document.getElementById('operationalBillingRule').textContent===q.operations.billingSummary &&
                q.operations.billingSummary.includes('em qualquer plano'));
              check(label+' PDF e exportações coerentes',
                pdf.support.operations.totalCents===expected.totalCents &&
                pdf.support.totalCents===base+expected.totalCents &&
                quoteRows().some(row=>row[0]==='Regra do adicional por usuários'&&row[1]===q.operations.billingSummary));
            }
          }
        }
        """)

    def test_essential_custom_video_selection_and_slider_by_click(self):
        self.run_browser("""
        applyPreset('essencial');
        const startingPrice=quoteData().monthlyTotalBRL;
        document.querySelector('[data-feature="C02"] .feature-copy').click();
        check('prévia não contrata vídeo nem altera mensalidade',
          state.activePreview==='C02' && state.selected.has('C01') &&
          !state.selected.has('C02') && quoteData().monthlyTotalBRL===startingPrice);
        document.querySelector('[data-feature="C02"] .video-selection-action').click();
        check('ação visível seleciona vídeo privado e personaliza',
          document.getElementById('select-C02').checked && state.selected.has('C02') &&
          !state.selected.has('C01') && state.activePreset==='custom' &&
          !document.getElementById('customConfigurationStatus').hidden &&
          document.getElementById('customConfigurationStatus').textContent.includes('baseada no Essencial'));
        const slider=document.getElementById('monthlyActiveUsers');
        const totals=[];
        for(const count of [100,1000,10000]){
          slider.value=count;slider.dispatchEvent(new Event('input',{bubbles:true}));
          const q=quoteData(),pdf=buildOfferPDFModel();
          totals.push(q.monthlyTotalBRL);
          check(count+' usuários atualizam tela, proposta e PDF sem trocar plano',
            state.maintenancePlan==='essencial' && state.activePreset==='custom' &&
            q.monthlyMaintenanceBRL===3000 && q.operations.inputs.videoStrategy==='C02' &&
            document.getElementById('maintenancePrice').textContent===brl(q.monthlyTotalBRL) &&
            pdf.support.totalCents===Math.round(q.monthlyTotalBRL*100));
        }
        check('mensalidade personalizada aumenta com usuários',
          totals[0]===3738 && totals[1]===4710 && totals[2]===15030);
        document.querySelector('[data-feature="C03"] .video-selection-action').click();
        check('offline mantém base Essencial e recalcula imediatamente',
          quoteData().monthlyMaintenanceBRL===3000 && quoteData().monthlyTotalBRL===18630 &&
          document.getElementById('maintenancePrice').textContent===brl(18630));
        document.querySelector('[data-feature="C01"] .video-selection-action').click();
        check('voltar ao YouTube zera adicional sem reaplicar Essencial',
          state.activePreset==='custom' && quoteData().monthlyOperationalBRL===0 &&
          document.getElementById('maintenancePrice').textContent===brl(3000));
        applyPreset('essencial');
        check('reaplicar plano retira indicação personalizada',
          document.getElementById('customConfigurationStatus').hidden);
        """)

    def test_responsive_controls(self):
        for width in [320, 375, 768, 1121, 1440]:
            with self.subTest(width=width):
                self.run_browser("""
                const inputs=[document.getElementById('monthlyActiveUsers'),...document.querySelectorAll('[data-operational]')];
                document.querySelector('.operation-controls details').open=true;
                const panel=document.getElementById('operationalLines').closest('details');panel.open=true;
                const explanation=document.getElementById('maintenanceExplanation');
                check('texto cabe no painel',explanation.scrollWidth<=explanation.clientWidth&&
                  explanation.querySelectorAll('p').length===5);
                check('sem overflow horizontal',document.documentElement.scrollWidth<=window.innerWidth+1);
                check('inputs dentro do viewport',inputs.every(input=>{
                  const box=input.getBoundingClientRect();return box.width>80&&box.left>=0&&box.right<=window.innerWidth+1;
                }));
                check('slider tem foco de teclado',!inputs[0].disabled&&inputs[0].tabIndex===0);
                check('mantém duas colunas no desktop',window.innerWidth<1100||
                  document.querySelector('.split').getBoundingClientRect().width>
                  document.querySelector('.operation-controls').getBoundingClientRect().width*1.5);
                """, width)
