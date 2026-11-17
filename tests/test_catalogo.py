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
SETTINGS_HASH = re.search(r"const releaseHash='([a-f0-9]{64})'", (ROOT / "campaign-settings.js").read_text()).group(1)


class CatalogoTest(unittest.TestCase):
    def test_specs_e_somas(self):
        catalog = json.loads(re.search(r"const specCatalog = (.*?);\n", HTML).group(1))
        foundation = {item["id"]: item for item in json.loads(re.search(r"const foundationCatalog = (.*?);\n", HTML).group(1))}
        specs = [p for p in (ROOT / "specs").glob("*.md") if re.match(r"^[A-Z]+\d+-", p.name)]
        self.assertEqual(len(specs), 62)
        reviewed = 0
        for path in specs:
            text = path.read_text()
            rows = re.findall(r"^\| [A-Z]+\d+-T\d+[A-Z]? \| [^|\n]+ \| (\d+) \| Revisão técnica preliminar \|$", text, re.M)
            declared = re.search(r"\| \*\*Total\*\* \| \| \*\*(\d+) h\*\*", text)
            self.assertTrue(rows, path.name)
            self.assertEqual(sum(map(int, rows)), int(declared.group(1)), path.name)
            code = path.name.split("-")[0]
            generated = foundation[code] if code.startswith("F") else catalog[code]
            tasks = re.findall(r"^\| ([A-Z]+\d+-T\d+[A-Z]?) \| ([^|\n]+) \| (\d+) \| Revisão técnica preliminar \|$", text, re.M)
            self.assertEqual(generated["taskDetails"], [
                {"id": task_id, "title": title, "hours": int(hours)} for task_id, title, hours in tasks
            ], path.name)
            self.assertTrue(generated["scope"], path.name)
            self.assertTrue(generated["risks"], path.name)
            self.assertTrue(generated["acceptance"], path.name)
            if not code.startswith("F"):
                title = re.sub(r"^#\s+[A-Z]+\d+\s+[—–-]\s*", "", text.splitlines()[0])
                self.assertEqual(generated["technicalTitle"], title, path.name)
            self.assertIn("## Cenário mínimo específico de aceite", text)
            reviewed += 1
        self.assertEqual(reviewed, 62)

    def test_browser(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        script = """
        window.confirm = () => true;
        const results = [];
        function check(name, ok) { results.push({name, ok}); }
        check('55 features', features.length === 55);
        check('fundação', foundationHours === 522);
        check('preparação sem detalhamento repetido',!document.getElementById('foundationBreakdown') &&
          !document.querySelector('[aria-labelledby="predevelopmentTitle"] details') &&
          document.getElementById('requirementsEstimate').textContent.includes('104 h') &&
          document.getElementById('designEstimate').textContent.includes('120 h'));
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
          const quote=quoteData();
          check(name+' curso administrativo de cortesia',quote.includedBenefits.length===1 &&
            quote.includedBenefits[0].id==='admin_training' && quote.includedBenefits[0].priceCents===0 &&
            quote.includedBenefits[0].includedIn.includes(name) &&
            quoteRows().some(row=>row[0]==='Curso de capacitação para administradores'&&row[1]==='Cortesia · sem custo adicional'));
          check(name+' plataformas incluídas',quote.delivery.studentPlatforms.join(',')==='Android,iOS,Web (navegador)' &&
            quote.delivery.administration==='Painel administrativo web');
          check(name+' revisão web pendente',quote.delivery.estimateStatus==='pending_web_review' &&
            quoteRows().some(row=>row[0]==='Revisão das estimativas'&&row[1].includes('revisa as estimativas')));
          const expectedComplexity={essencial:'Baixa',plus:'Média',premium:'Alta'}[name];
          check(name+' complexidade relativa',el.avgComplexity.textContent===expectedComplexity &&
            document.getElementById('complexityMetricLabel').textContent==='Complexidade do plano' &&
            document.getElementById('complexityExplanation').textContent.includes('Classificação relativa'));
          check(name+' complexidade na proposta',quote.complexity.label===expectedComplexity &&
            quote.complexity.basis==='relative_plan' &&
            quoteRows().some(row=>row[0]==='Complexidade do plano'&&row[1]===expectedComplexity));
        }
        check('complexidade visível nos três presets',[...document.querySelectorAll('.preset-complexity')].map(node=>node.textContent).join('|')===
          'Complexidade baixa|Complexidade média|Complexidade alta');
        check('escala técnica preservada',complexityLabel(3)==='Média-alta' && complexityLabel(5)==='Muito alta' &&
          features.every(f=>f.complexity===specCatalog[f.id].complexity));
        check('copy comercial cobre as 55 features',Object.keys(ATSIProductCopy.features).length===55 &&
          features.every(f=>{
            const copy=ATSIProductCopy.features[f.id];
            return copy && f.title===copy.title && f.desc===copy.description &&
              copy.benefits.length>=2 && copy.scope.length>30;
          }));
        check('tags mostram os planos de cada recurso',features.every(f=>{
          const expected=Object.keys(presets).filter(key=>f.type==='required'||presets[key].features.includes(f.id));
          const actual=[...document.querySelectorAll(`[data-feature="${f.id}"] .badge[data-plan]`)];
          return actual.map(node=>node.dataset.plan).join(',')===expected.join(',') &&
            actual.every(node=>node.textContent===presets[node.dataset.plan].name);
        }));
        check('opcionais fora dos planos ficam sem tags',features.filter(f=>f.type==='optional'&&
          !Object.values(presets).some(preset=>preset.features.includes(f.id))).every(f=>
            !document.querySelector(`[data-feature="${f.id}"] .badges`)));
        check('vídeos identificam o plano correto',featurePlanKeys(getFeature('C01')).join(',')==='essencial' &&
          featurePlanKeys(getFeature('C02')).join(',')==='plus' &&
          featurePlanKeys(getFeature('C03')).join(',')==='premium');
        check('certificados pertencem ao plus e premium',featurePlanKeys(getFeature('C04')).join(',')==='plus,premium');
        check('base essencial presente nos três planos',featurePlanKeys(getFeature('B01')).join(',')==='essencial,plus,premium');
        check('tag genérica removida',!el.sections.textContent.includes('Amplie seu plano'));
        applyPreset('essencial');
        check('Facebook opcional fora dos planos',getFeature('A04').type==='optional' &&
          getFeature('A04').hours===32 && getFeature('A04').price===6400 &&
          featurePlanKeys(getFeature('A04')).length===0 && !document.querySelector('[data-feature="A04"] .badges'));
        toggleFeature('A04',true);
        check('Facebook soma preço e esforço sem mudar manutenção',targetTotal===184400 &&
          el.totalHours.textContent==='922 h' && quoteData().monthlyMaintenanceBRL===3000 &&
          quoteData().selectedIds.includes('A04'));
        state.activePreview='A04';renderPreview();
        check('Facebook tem preview específico',el.phoneScreen.textContent.includes('Continuar com Facebook') &&
          !!el.phoneScreen.querySelector('[data-mock-feature="A04"]'));
        toggleFeature('A04',false);
        check('remover Facebook restaura essencial',targetTotal===178000 && !quoteData().selectedIds.includes('A04'));
        check('curso de cortesia visível e sem seleção',document.getElementById('adminTrainingCard').textContent.includes('Cortesia · sem custo adicional') &&
          !document.getElementById('adminTrainingCard').querySelector('input') &&
          document.getElementById('adminTrainingPlans').querySelectorAll('.badge').length===3 &&
          document.querySelector('#investmentSummary [data-admin-training-courtesy]').textContent==='Cortesia · sem custo adicional');
        check('snapshots financeiros preservam títulos originais',Object.values(pricingSnapshot().packages).every(pack=>
          pack.items.every(item=>item.title===specCatalog[item.id].title)));
        const internalCopy=/specs\\/|docs\\/|\\.md\\b|repositório|pendente de validação|aprovação pendente|cenário mínimo|revisão técnica preliminar|Supabase|Next.js|RBAC|auditoria/i;
        check('página com linguagem de produto',!internalCopy.test(document.querySelector('.page').textContent));
        check('popups vendem benefícios sem expor documentos',features.every(f=>{
          openFeatureDetails(f,null);
          const text=document.getElementById('dialogContent').textContent;
          const valid=!internalCopy.test(text) && text.includes('Mais valor para a sua plataforma') &&
            text.includes(ATSIProductCopy.features[f.id].scope);
          featureDialog.close();
          return valid;
        }));
        const invalidPriceNotice=/Preço de venda:\\s*Não aprovado|não é preço aprovado|não proposta aprovada|não preços comerciais aprovados|Valores não validados/i;
        check('tela sem aviso de preço não aprovado',!invalidPriceNotice.test(document.querySelector('.split').textContent) &&
          !invalidPriceNotice.test(document.getElementById('floatingTotal').textContent));
        check('cards mostram preço de implantação',features.every(f=>renderFeatureCard(f).includes('Preço de implantação') &&
          !invalidPriceNotice.test(renderFeatureCard(f))));
        check('popups sem aviso de preço não aprovado',features.every(f=>{
          openFeatureDetails(f,null);
          const valid=!invalidPriceNotice.test(document.getElementById('dialogContent').textContent);
          featureDialog.close();
          return valid;
        }));
        check('investimento sem ressalva comercial',document.querySelector('#investmentSummary > small').textContent==='Investimento de implantação');
        check('plataformas sem repetição nos cards dos planos',!document.querySelector('.preset-platforms') &&
          !el.presetButtons.textContent.includes('Web para alunos') &&
          document.querySelector('.delivery-scope [data-delivery-students]').textContent===deliveryScope.studentLabel);
        check('destaque desde o essencial',document.getElementById('deliveryScopeTitle').textContent==='Android, iOS e web desde o Essencial');
        check('resumo distingue aluno e gestão',document.querySelector('#investmentSummary [data-delivery-students]').textContent===deliveryScope.studentLabel &&
          document.querySelector('#investmentSummary [data-delivery-administration]').textContent===deliveryScope.administration);
        check('painel de plataformas sem nota de estimativas',!document.querySelector('.delivery-scope [data-delivery-estimate]') &&
          !document.querySelector('.delivery-scope').textContent.includes(deliveryScope.estimateNote));
        check('nota de estimativas preservada no resumo',document.querySelector('#investmentSummary [data-delivery-estimate]').textContent===deliveryScope.estimateNote);
        check('proposta descreve web para alunos',quoteRows().some(row=>row[0]==='Entrega para alunos'&&row[1].includes('versão web para alunos')));
        applyPreset('essencial');
        toggleFeature('C02',true);
        check('privado puro',targetTotal===188400);
        toggleFeature('C03',true);
        check('offline sem duplicar',targetTotal===214000 && !state.selected.has('C02'));
        toggleFeature('C03',false);
        check('não esvaziar vídeo',state.selected.has('C03'));
        toggleFeature('G02',true);
        check('G02 selecionável com estimativa',state.selected.has('G02') && targetTotal===264000);
        check('G02 catálogo multicanal',getFeature('G02').title==='Encaminhamento multicanal para redes sociais' &&
          getFeature('G02').hours===250 && getFeature('G02').price===50000 &&
          getFeature('G02').desc.includes('grupos e canais de diferentes redes'));
        check('G02 ressalva técnica',document.getElementById('scopeWarnings').textContent.includes('até três conectores oficiais viáveis') &&
          ATSIProductCopy.features.G02.scope.includes('APIs e permissões disponíveis') &&
          !document.querySelector('[data-feature="G02"] .badges'));
        const beforeG02Preview=targetTotal;
        state.activePreview='G02';renderPreview();
        check('G02 configuração administrativa',el.phoneScreen.querySelector('.app-screen').dataset.mockContext==='admin');
        check('G02 múltiplas redes e mensagem',['Preparar mensagem','WhatsApp','Telegram','Discord','Mesmo agendamento','status por destino'].every(text=>
          el.phoneScreen.textContent.includes(text)));
        check('G02 limites explícitos',el.phoneScreen.textContent.includes('Prévia da central') &&
          el.phoneScreen.textContent.includes('três conectores oficiais viáveis') &&
          el.phoneScreen.textContent.includes('envios independentes') && targetTotal===beforeG02Preview);
        toggleFeature('N02',true);
        check('incluir dependência',state.selected.has('N01'));
        toggleFeature('N01',false);
        check('requisito em uso não pode ser removido',state.selected.has('N02') && state.selected.has('N01') &&
          document.querySelector('[data-feature="N01"] .feature-toggle').disabled);
        toggleFeature('N02',false);
        check('requisito automático sem uso é retirado',!state.selected.has('N02') && !state.selected.has('N01'));
        check('mockups',features.every(f=>{state.activePreview=f.id;renderPreview();return !!el.phoneScreen.querySelector('.app-screen');}));
        check('55 composições específicas',features.every(f=>specificMockContent(f)!==null));
        const semanticExamples={
          B05:'Receber promoções',A02:'Continuar com Google',A03:'Continuar com Microsoft',A04:'Continuar com Facebook',
          C01:'Player YouTube',C02:'Streaming privado',C03:'Download da aula',
          C06:'Revisão humana',C07:'Fonte ilustrativa',C08:'Comentários da aula',
          C09:'satisfação',G01:'Abrir convite do WhatsApp',G02:'Redes e destinos',G05:'Publicar meu perfil',
          EV02:'Prévia do QR',EV04:'Enquadre o QR',P01:'Aguardando pagamento',
          P02:'Renovação',P03:'Comprar curso',P04:'Reserva temporária',
          P05:'Acesso restrito',P06:'Acesso restrito',P07:'Acesso restrito',
          L01:'Responsável',R01:'Visualizações de aulas',R02:'Exportar conclusões',
          R03:'18 avaliações',R04:'Cada usuário é contado uma vez',R05:'Atualização periódica',GM02:'Check-in'
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
        check('marca nos 55 mockups',features.every(f=>{
          state.activePreview=f.id;renderPreview();
          return el.phoneScreen.querySelector('.app-brand img')?.alt==='ATSI+';
        }));
        check('título do produto',document.querySelector('h1').textContent==='Plataforma ATSI+');
        check('menu simplificado',document.getElementById('promotionSettings').querySelectorAll('input').length===6 &&
          !!document.getElementById('settingsDialog').querySelector('input[type=file]') &&
          document.getElementById('discountFields').disabled);
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
        check('personalizado mantém cortesia fora das features',quoteData().includedBenefits[0].priceCents===0 &&
          !quoteData().selectedIds.includes('admin_training') && !getFeature('admin_training'));
        check('custom mantém plataformas',quoteData().delivery.studentPlatforms.includes('Web (navegador)') &&
          quoteData().delivery.estimateStatus==='pending_web_review');
        const customAverage=selectedFeatures().reduce((sum,f)=>sum+f.complexity,0)/selectedFeatures().length;
        check('custom usa média técnica explícita',document.getElementById('complexityMetricLabel').textContent==='Complexidade média' &&
          el.avgComplexity.textContent===complexityLabel(customAverage) &&
          quoteData().complexity.basis==='feature_average' && quoteData().complexity.average===customAverage &&
          document.getElementById('complexityExplanation').textContent.includes('Personalizado: média técnica'));
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
        document.getElementById('discountAdditionalOptional').value=25;
        document.getElementById('discountReleaseHash').value='TEST_RELEASE_HASH';
        document.getElementById('discountAccessForm').requestSubmit();
        document.getElementById('promotionSettings').requestSubmit();
        applyPreset('essencial');
        check('salvar campanha e descontar essencial',targetTotal===160200 && campaignConfig.percentages.essencial===10);
        applyPreset('plus');
        check('campanha plus',targetTotal===195500);
        check('faixas promocionais nos três planos',document.querySelectorAll('.plan-offer del').length===3);
        check('timer compacto',document.getElementById('offerTitle').textContent==='Oferta' && !document.querySelector('.offer-box').hidden);
        check('campanha persistida',JSON.parse(localStorage.getItem(campaignStorageKey)).endsAt===campaignConfig.endsAt);
        check('horas e mensalidades preservadas',quoteData().monthlyMaintenanceBRL===4000 && el.totalHours.textContent==='1150 h');
        check('desconto adicional persistido',JSON.parse(localStorage.getItem(campaignStorageKey)).additionalOptionalPercentage===25);
        const beforeBannerClick=targetTotal;
        document.querySelector('[data-feature="G02"] .feature-discount-banner').click();
        check('painel de desconto visualiza sem contratar',state.activePreview==='G02' && !state.selected.has('G02') && targetTotal===beforeBannerClick);
        toggleFeature('G02',true);
        check('plus com G02 descontada',targetTotal===233000 && state.basePreset==='plus' && state.activePreset==='custom' &&
          quoteData().pricing.planDiscountCents===3450000 && quoteData().pricing.additionalDiscountCents===1250000);
        check('preço adicional riscado no card',document.querySelector('[data-feature="G02"] .feature-price-offer del').textContent===brl(50000) &&
          document.querySelector('[data-feature="G02"] .feature-price-offer strong').textContent===brl(37500));
        check('painel grande informa percentual e economia',document.querySelector('[data-feature="G02"] .feature-discount-rate b').textContent==='−25%' &&
          document.querySelector('[data-feature="G02"] .feature-discount-saving').textContent==='Economize '+brl(12500) &&
          document.querySelector('[data-feature="G02"]').classList.contains('has-feature-discount'));
        check('painel apenas nas features com desconto',features.every(f=>
          !!document.querySelector(`[data-feature="${f.id}"] .feature-discount-banner`) === (featureAdditionalPricing(f).discountCents>0)));
        check('item incluído no plano não recebe desconto adicional',!document.querySelector('[data-feature="C04"] .feature-price-offer'));
        check('resumo e dados concordam',document.getElementById('additionalDiscount').textContent===brl(12500) &&
          quoteRows().some(row=>row[0].startsWith('G02 ·')&&row[1]===brl(37500)) &&
          quoteData().campaign.additionalOptionalPercentage===25 && quoteData().offerStatus==='active');
        check('horas e manutenção sem desconto adicional',el.totalHours.textContent==='1400 h' && quoteData().monthlyMaintenanceBRL===4000);
        toggleFeature('C04',false);
        check('remover item do plano suspende os descontos',quoteData().pricing.discountCents===0 &&
          !document.querySelector('[data-feature="G02"] .feature-price-offer') &&
          document.getElementById('pricingContext').textContent.includes('Sua configuração está personalizada'));
        toggleFeature('C04',true);
        check('restaurar plano recupera descontos',targetTotal===233000);
        toggleFeature('C03',true);
        check('trocar vídeo não aplica campanha do plano anterior',quoteData().pricing.discountCents===0 && !quoteData().pricing.baseIntact);
        toggleFeature('C02',true);
        check('restaurar vídeo recupera campanha',targetTotal===233000 && quoteData().pricing.baseIntact);
        toggleFeature('G02',false);
        check('remover adicional restaura valor do plano',targetTotal===195500 && quoteData().pricing.additionalDiscountCents===0);
        toggleFeature('G02',true);
        Date.now=()=>Date.parse(campaignConfig.endsAt)+1;
        render();
        check('faixas e timer somem ao expirar',document.querySelectorAll('.plan-offer').length===0 && document.querySelector('.offer-box').hidden);
        check('expiração remove ambos os descontos',targetTotal===280000 && quoteData().pricing.discountCents===0 &&
          !document.querySelector('[data-feature="G02"] .feature-price-offer') && quoteData().offerStatus==='expired');
        Date.now=clock;
        render();
        check('vigência não renovada nas edições',JSON.parse(localStorage.getItem(campaignStorageKey)).endsAt===campaignConfig.endsAt);
        for(const [key,base] of [['essencial',160200],['plus',195500],['premium',311360]]){
          applyPreset(key);toggleFeature('G02',true);
          check(key+' com adicional sem desconto duplicado',targetTotal===base+37500 &&
            quoteData().pricing.additionalDiscountCents===1250000);
          const includedAnywhere=new Set(Object.values(presets).flatMap(preset=>preset.features));
          check(key+' exclui opcionais de todos os planos',features.filter(f=>f.type==='optional'&&includedAnywhere.has(f.id))
            .every(f=>featureAdditionalPricing(f).discountCents===0 &&
              !document.querySelector(`[data-feature="${f.id}"] .feature-price-offer`)));
        }
        check('configurações explicam exclusão dos três planos',document.getElementById('promotionSettings').textContent.includes('nenhum dos planos Essencial, Plus ou Premium'));
        applyPreset('essencial');toggleFeature('C04',true);toggleFeature('E01',true);
        const crossPlanPrice=getFeature('C04').price+getFeature('E01').price;
        check('certificados e biblioteca no essencial ficam a preço de tabela',targetTotal===160200+crossPlanPrice &&
          quoteData().pricing.additionalDiscountCents===0 &&
          !document.querySelector('[data-feature="C04"] .feature-price-offer') &&
          !document.querySelector('[data-feature="E01"] .feature-price-offer'));
        toggleFeature('G02',true);
        check('mistura itens de planos sem desconto e G02 com desconto',targetTotal===160200+crossPlanPrice+37500 &&
          quoteData().pricing.additionalRegularCents===5000000 &&
          quoteData().pricing.additionalItems.length===1 && quoteData().pricing.additionalItems[0].id==='G02' &&
          quoteRows().some(row=>row[0].startsWith('C04 ·')&&row[1]===brl(getFeature('C04').price)) &&
          quoteRows().some(row=>row[0].startsWith('E01 ·')&&row[1]===brl(getFeature('E01').price)));
        applyPreset('plus');toggleFeature('N03',true);
        const n03Price=getFeature('N03').price;
        check('dependência já incluída não duplica desconto',quoteData().pricing.additionalItems.length===1 &&
          quoteData().pricing.additionalItems[0].id==='N03' && targetTotal===195500+n03Price*.75);
        toggleFeature('G06',true);
        check('dependências adicionais recebem desconto uma vez',quoteData().pricing.additionalItems.filter(i=>['G05','G06'].includes(i.id)).length===2 &&
          new Set(quoteData().pricing.additionalItems.map(i=>i.id)).size===quoteData().pricing.additionalItems.length);
        applyPreset('essencial');toggleFeature('A04',true);
        check('Facebook recebe desconto de opcional adicional',targetTotal===165000 &&
          quoteData().pricing.additionalDiscountCents===160000 &&
          document.querySelector('[data-feature="A04"] .feature-discount-banner strong').textContent===brl(4800) &&
          quoteRows().some(row=>row[0].startsWith('A04 ·')&&row[1]===brl(4800)));
        applyPreset('plus');toggleFeature('G02',true);
        window.scrollTo({top:0,behavior:'instant'});
        const nativeRAF=window.requestAnimationFrame;
        let scrollFrame=null;
        window.requestAnimationFrame=callback=>{scrollFrame=callback;return 999999;};
        document.getElementById('viewPrice').click();
        if(scrollFrame)scrollFrame(performance.now()+1000);
        window.requestAnimationFrame=nativeRAF;
        const priceRect=el.totalPrice.getBoundingClientRect();
        check('um clique exibe valor',priceRect.top>=0 && priceRect.bottom<=innerHeight);
        check('perto do investimento oferece voltar ao início',document.getElementById('viewPrice').textContent==='Voltar ao início ↑' &&
          document.getElementById('viewPrice').getAttribute('aria-controls')==='pageTop');
        window.requestAnimationFrame=callback=>{scrollFrame=callback;return 999999;};
        document.getElementById('viewPrice').click();
        if(scrollFrame)scrollFrame(performance.now()+1000);
        window.requestAnimationFrame=nativeRAF;
        check('segundo clique retorna ao topo',window.scrollY===0 && document.getElementById('viewPrice').textContent==='Ver preço ↓' &&
          document.getElementById('viewPrice').getAttribute('aria-controls')==='investmentSummary');
        document.body.insertAdjacentHTML('beforeend','<pre id="qa-results">'+JSON.stringify(results)+'</pre>');
        """
        script = script.replace("TEST_RELEASE_HASH", SETTINGS_HASH)
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

    def test_discount_panel_layout(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        script = """
        (async()=>{
          await document.fonts.ready;
          campaignConfig={schemaVersion:2,startsAt:new Date(Date.now()-3600000).toISOString(),
            endsAt:new Date(Date.now()+3600000).toISOString(),
            percentages:{essencial:10,plus:15,premium:20},additionalOptionalPercentage:25};
          applyPreset('plus');toggleFeature('G02',true);
          const results=[];
          for(const card of document.querySelectorAll('.has-feature-discount')){
            const banner=card.querySelector('.feature-discount-banner');
            const rect=banner.getBoundingClientRect(),parent=card.getBoundingClientRect();
            const header=card.querySelector('.feature-head').getBoundingClientRect();
            results.push({id:card.dataset.feature,
              overlapsTop:rect.top<parent.top,
              controlsClear:rect.bottom<=header.top,
              fits:banner.scrollWidth<=banner.clientWidth && card.scrollWidth<=card.clientWidth &&
                rect.left>=parent.left && rect.right<=parent.right,
              clicksPassThrough:getComputedStyle(banner).pointerEvents==='none'});
          }
          results.push({id:'page',fits:document.documentElement.scrollWidth<=innerWidth});
          results.push({id:'mockups',fits:features.every(f=>{
            state.activePreview=f.id;renderPreview();
            const screen=el.phoneScreen.querySelector('.app-screen');
            return screen.scrollWidth<=screen.clientWidth;
          })});
          results.push({id:'dialogs',fits:features.every(f=>{
            openFeatureDetails(f,null);
            const rect=featureDialog.getBoundingClientRect();
            const fits=rect.left>=0 && rect.right<=innerWidth && featureDialog.scrollWidth<=featureDialog.clientWidth;
            featureDialog.close();
            return fits;
          })});
          document.getElementById('openSettings').click();
          document.getElementById('discountReleaseHash').value='TEST_RELEASE_HASH';
          document.getElementById('discountAccessForm').requestSubmit();
          const settings=document.getElementById('settingsDialog');
          const settingsRect=settings.getBoundingClientRect();
          results.push({id:'settings',fits:settingsRect.left>=0 && settingsRect.right<=innerWidth &&
            settings.scrollWidth<=settings.clientWidth && !document.getElementById('discountFields').disabled});
          settings.close();
          window.scrollTo({top:0,behavior:'instant'});updatePriceShortcut();
          function clickShortcut(){
            const native=requestAnimationFrame;let frame=null;
            window.requestAnimationFrame=callback=>{frame=callback;return 999999;};
            document.getElementById('viewPrice').click();
            if(frame)frame(performance.now()+1000);
            window.requestAnimationFrame=native;
          }
          clickShortcut();
          const priceRect=el.totalPrice.getBoundingClientRect();
          results.push({id:'shortcut-to-price',fits:priceRect.top>=0 && priceRect.bottom<=innerHeight &&
            document.getElementById('viewPrice').textContent==='Voltar ao início ↑'});
          window.scrollBy({top:-30,behavior:'instant'});updatePriceShortcut();
          results.push({id:'shortcut-latched',fits:document.getElementById('viewPrice').textContent==='Voltar ao início ↑'});
          clickShortcut();
          results.push({id:'shortcut-to-top',fits:scrollY===0 && document.getElementById('viewPrice').textContent==='Ver preço ↓'});
          return {width:innerWidth,checks:results};
        })();
        """.replace("TEST_RELEASE_HASH", SETTINGS_HASH)
        page = HTML.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
        wrapper = """<!doctype html><body><script>
        (async()=>{
          const results=[];
          for(const width of [320,390,768,1121,1440]){
            const frame=document.createElement('iframe');
            frame.style.width=width+'px';frame.style.height='1000px';
            frame.src='test.html';
            const loaded=new Promise(resolve=>frame.onload=resolve);
            document.body.appendChild(frame);await loaded;
            results.push(await frame.contentWindow.eval(CHECK_SCRIPT));
            frame.remove();
          }
          document.body.insertAdjacentHTML('beforeend','<pre id="panel-layout">'+JSON.stringify(results)+'</pre>');
        })();
        </script></body>""".replace("CHECK_SCRIPT", json.dumps(script))
        with tempfile.TemporaryDirectory(prefix="atsi-discount-layout-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "test.html"
            file.write_text(page)
            layout = Path(directory) / "layout.html"
            layout.write_text(wrapper)
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--allow-file-access-from-files",
                "--virtual-time-budget=5000", "--dump-dom", layout.as_uri()
            ], capture_output=True, text=True, timeout=30)
        match = re.search(r'<pre id="panel-layout">(\[.*?\])</pre>', run.stdout)
        self.assertIsNotNone(match, "Layout dos descontos não completou")
        layouts = json.loads(match.group(1))
        self.assertEqual([layout["width"] for layout in layouts], [320, 390, 768, 1121, 1440])
        for layout in layouts:
            with self.subTest(width=layout["width"]):
                results = layout["checks"]
                self.assertTrue(any(row["id"] == "G02" for row in results))
                for row in results:
                    for name, ok in row.items():
                        if name != "id":
                            self.assertTrue(ok, f'{row["id"]}: {name}')

    def test_campaign_restore(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        for name, additional, expected, input_value in [
            ("legacy", None, 245500, "0"),
            ("additional", 25, 233000, "25"),
            ("invalid", 101, 280000, "0"),
        ]:
            with self.subTest(name=name):
                field = "" if additional is None else f",additionalOptionalPercentage:{additional}"
                seed = """
                const restoreCampaign={schemaVersion:2,
                  startsAt:new Date(Date.now()-3600000).toISOString(),
                  endsAt:new Date(Date.now()+3600000).toISOString(),
                  percentages:{essencial:10,plus:15,premium:20}FIELD};
                localStorage.setItem(campaignStorageKey,JSON.stringify(restoreCampaign));
                initOffers();
                """.replace("FIELD", field)
                script = """
                applyPreset('plus');toggleFeature('G02',true);
                const result={total:targetTotal,input:document.getElementById('discountAdditionalOptional').value,
                  restored:campaignConfig!==null,
                  sameDates:!campaignConfig || (campaignConfig.startsAt===restoreCampaign.startsAt &&
                    campaignConfig.endsAt===restoreCampaign.endsAt)};
                document.body.insertAdjacentHTML('beforeend','<pre id="restore-result">'+JSON.stringify(result)+'</pre>');
                """
                page = HTML.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
                page = page.replace("    initOffers();", seed, 1)
                page = page.replace("</body>", f"<script>{script}</script></body>")
                with tempfile.TemporaryDirectory(prefix="atsi-restore-", dir="/tmp/opencode") as directory:
                    file = Path(directory) / "test.html"
                    file.write_text(page)
                    run = subprocess.run([
                        chrome, "--headless", "--no-sandbox", "--disable-gpu",
                        "--disable-dev-shm-usage", "--dump-dom", file.as_uri()
                    ], capture_output=True, text=True, timeout=30)
                match = re.search(r'<pre id="restore-result">(\{.*?\})</pre>', run.stdout)
                self.assertIsNotNone(match, "Restauração não completou")
                result = json.loads(match.group(1))
                self.assertEqual(result["total"], expected)
                self.assertEqual(result["input"], input_value)
                self.assertEqual(result["restored"], name != "invalid")
                self.assertTrue(result["sameDates"])


if __name__ == "__main__":
    unittest.main()
