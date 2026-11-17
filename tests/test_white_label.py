"""Uma única oferta/catálogo, com identidade escolhida por URL."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]


class WhiteLabelTest(unittest.TestCase):
    def browser(self, page, query="", script="", width=1440, expect_not_found=False):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        html = (ROOT / page).read_text()
        setup = """
        window.brandErrors=[];
        window.addEventListener('error',e=>brandErrors.push(e.message));
        localStorage.clear();
        """
        html = html.replace("<head>", f'<head><base href="{ROOT.as_uri()}/"><script>{setup}</script>', 1)
        html = html.replace("</body>", f"<script>{script}</script></body>")
        with tempfile.TemporaryDirectory(prefix="white-label-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "page.html"
            file.write_text(html)
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", f"--window-size={width},960",
                "--virtual-time-budget=2000", "--dump-dom", file.as_uri() + query
            ], capture_output=True, text=True, timeout=30)
        if expect_not_found:
            self.assertIn('<title>404 — Página não encontrada</title>', run.stdout)
            self.assertIn('<h1 id="notFoundTitle">Página não encontrada</h1>', run.stdout)
            self.assertNotIn('id="loginForm"', run.stdout)
            self.assertNotIn('id="investmentSummary"', run.stdout)
            self.assertNotIn('id="catalog"', run.stdout)
            return
        match = re.search(r'<pre id="brand-result">(\{.*?\})</pre>', run.stdout)
        self.assertIsNotNone(match, run.stderr[-2000:])
        return json.loads(match.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))

    def test_company_catalog_and_presentation(self):
        script = """
        (async()=>{
          const plans={};
          for(const key of ['essencial','plus','premium']){
            applyPreset(key);
            const q=quoteData(),pdf=buildOfferPDFModel();
            plans[key]={selected:q.selectedIds,pricing:q.pricing,
              hours:pdf.totalHours,maintenance:q.monthlyMaintenanceBRL,
              operations:q.operations.totalCents,snapshot:q.priceListSnapshot};
          }
          const mockups=features.every(f=>{
            state.activePreview=f.id;renderPreview();
            return !/\\bATSI\\b/.test(el.phoneScreen.textContent) &&
              el.phoneScreen.querySelector('img').alt===ATSIProduct.name;
          });
          const popups=features.every(f=>{
            openFeatureDetails(f,null);
            const valid=!/\\bATSI\\b/.test(dialogContent.textContent);
            featureDialog.close();return valid;
          });
          applyPreset('essencial');
          // Uma campanha ATSI gravada não deve afetar JAN.
          localStorage.setItem('atsi-campaign-v2',JSON.stringify({
            schemaVersion:2,startsAt:new Date(Date.now()-3600000).toISOString(),
            endsAt:new Date(Date.now()+3600000).toISOString(),
            percentages:{essencial:10,plus:15,premium:20}
          }));
          initOffers();applyPreset('essencial');
          const image=document.querySelector('[data-company-logo]');
          await image.decode();
          const q=quoteData(),pdf=buildOfferPDFModel();
          const commonCopy=JSON.stringify(ATSIProductCopy)
            .split(ATSIProduct.name).join('MARCA')
            .split(ATSIProduct.client).join('MARCA')
            .split(ATSIProduct.shortName).join('MARCA');
          const result={company:ATSIProduct.company,name:ATSIProduct.name,plans,mockups,popups,
            commonCopy,
            title:document.title,heading:document.querySelector('h1').textContent,
            primary:getComputedStyle(document.documentElement).getPropertyValue('--brand-primary').trim(),
            headerBackground:getComputedStyle(document.querySelector('.hero')).backgroundImage,
            logo:image.getAttribute('src'),logoAlt:image.alt,logoLoaded:image.naturalWidth>0,
            favicon:document.querySelector('link[rel=icon]').getAttribute('href'),
            metadata:document.querySelector('meta[name=description]').content,
            project:q.project,pdfProject:pdf.project,pdfName:ATSIOfferPDF.fileName(pdf),
            pdfIsValid:ATSIOfferPDF.createDocument(pdf).output().startsWith('%PDF'),
            pdfHasATSI:/\\bATSI\\b/.test(JSON.stringify([pdf.foundation,pdf.features,pdf.benefits])),
            storageKey:campaignStorageKey,isolationTotal:targetTotal,
            link:CompanyBranding.pageURL('home.html').searchParams.get('company'),
            errors:brandErrors,
            overflow:document.documentElement.scrollWidth>window.innerWidth};
          document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        })();
        """
        atsi = self.browser("home.html", "?company=atsi-brasil", script)
        jan = self.browser("home.html", "?company=jan", script)
        self.assertEqual(atsi["plans"], jan["plans"], "Catálogo e cálculos devem ser idênticos")
        self.assertEqual(atsi["commonCopy"], jan["commonCopy"],
                         "Textos devem ser os mesmos, alterando apenas os nomes da identidade")
        self.assertEqual([p["pricing"]["finalCents"] for p in jan["plans"].values()],
                         [17800000, 23000000, 38920000])
        self.assertEqual(jan["company"], "jan")
        self.assertEqual(jan["heading"], "Plataforma JAN")
        self.assertNotIn("ATSI", jan["title"])
        self.assertNotIn("ATSI", jan["metadata"])
        self.assertEqual(jan["primary"], "#ff8897")
        self.assertNotEqual(atsi["headerBackground"], jan["headerBackground"])
        self.assertEqual(jan["logo"], "assets/companies/jan/logo-dark.svg")
        self.assertEqual(jan["logoAlt"], "JAN")
        self.assertEqual(atsi["logo"], "branding/assets/atsi-logo-cabecalho.svg")
        self.assertEqual(atsi["logoAlt"], "ATSI Brasil")
        self.assertEqual(jan["favicon"], "assets/companies/jan/icon.svg")
        self.assertEqual(jan["project"]["company"], "jan")
        self.assertEqual(jan["pdfProject"], jan["project"])
        self.assertEqual(jan["pdfProject"]["branding"]["header"], [66, 35, 44])
        self.assertTrue(jan["pdfName"].startswith("jan-Oferta-"))
        self.assertTrue(jan["pdfIsValid"])
        self.assertFalse(jan["pdfHasATSI"])
        self.assertTrue(jan["mockups"])
        self.assertTrue(jan["popups"])
        self.assertEqual(atsi["storageKey"], "atsi-campaign-v2")
        self.assertEqual(jan["storageKey"], "atsi-campaign-v2:company:jan")
        self.assertEqual(atsi["isolationTotal"], 160200)
        self.assertEqual(jan["isolationTotal"], 178000)
        for result in (atsi, jan):
            self.assertTrue(result["logoLoaded"])
            self.assertFalse(result["overflow"])
            self.assertEqual(result["errors"], [])
            self.assertEqual(result["link"], result["company"])

    def test_atsi_product_logo_preserved_in_entry_and_mockups(self):
        entry_script = """
        const image=document.querySelector('[data-company-logo]');
        const result={src:image.getAttribute('src'),alt:image.alt};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        entry = self.browser("index.html", "?company=atsi-brasil", entry_script)
        self.assertEqual(entry["src"], "assets/companies/atsi-brasil/logo-dark.svg")
        self.assertEqual(entry["alt"], "ATSI+")
        mock_script = """
        const result={correct:features.every(feature=>{
          state.activePreview=feature.id;renderPreview();
          const image=el.phoneScreen.querySelector('.app-brand img');
          return image.alt==='ATSI+' &&
            image.getAttribute('src')==='assets/companies/atsi-brasil/logo-dark.svg';
        })};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        mockups = self.browser("home.html", "?company=atsi-brasil", mock_script)
        self.assertTrue(mockups["correct"])

    def test_missing_empty_and_unknown_company_not_found(self):
        for page in ("index.html", "home.html", "ofertas-admin.html"):
            for query in ("", "?company=", "?origem=email", "?company=%20",
                          "?company=../../jan", "?company=__proto__",
                          "?company=empresa-inexistente"):
                with self.subTest(page=page, query=query):
                    self.browser(page, query, width=390, expect_not_found=True)

    def test_valid_mobile_entry(self):
        script = """
        const result={company:ATSIProduct.company,title:document.title,
          logo:document.querySelector('[data-company-logo]').getAttribute('src'),
          intro:document.querySelector('.intro').textContent,
          destination:CompanyBranding.pageURL('home.html').searchParams.get('company'),
          overflow:document.documentElement.scrollWidth>innerWidth,errors:brandErrors};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        for company in ("atsi-brasil", "jan"):
            query = "?" + urlencode({"company": company})
            result = self.browser("index.html", query, script, width=390)
            expected = company
            self.assertEqual(result["company"], expected)
            self.assertEqual(result["destination"], expected)
            self.assertIn(f"/{expected}/", result["logo"])
            self.assertEqual(result["errors"], [])
            self.assertFalse(result["overflow"])
            if expected == "jan":
                self.assertNotIn("ATSI", result["intro"])
                self.assertIn("JAN", result["title"])

    def test_shared_background_and_font_load_for_all_companies(self):
        script = """
        (async()=>{
          if(document.readyState!=='complete'){
            await new Promise(resolve=>window.addEventListener('load',resolve,{once:true}));
          }
          const background=getComputedStyle(document.body).backgroundImage;
          const expected=new URL('branding/assets/parallax.jpg',document.baseURI).href;
          const urls=[...background.matchAll(/url\\(["']?([^"')]+)["']?\\)/g)].map(match=>match[1]);
          const image=new Image();
          const loaded=await new Promise(resolve=>{
            image.onload=()=>resolve(image.naturalWidth>0);
            image.onerror=()=>resolve(false);
            image.src=expected;
          });
          const result={correctURL:urls.includes(expected),loaded,errors:brandErrors,
            font:getComputedStyle(document.body).fontFamily,
            inputFont:getComputedStyle(document.querySelector('input')).fontFamily};
          document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        })();
        """
        for company in ("atsi-brasil", "jan"):
            for page in ("index.html", "home.html", "ofertas-admin.html"):
                with self.subTest(page=page, company=company):
                    result = self.browser(page, f"?company={company}", script)
                    self.assertTrue(result["correctURL"], "O fundo deve usar o caminho real da imagem")
                    self.assertTrue(result["loaded"], "A imagem deve carregar sem erro")
                    self.assertIn("Montserrat", result["font"])
                    self.assertEqual(result["font"], result["inputFont"])
                    self.assertEqual(result["errors"], [])

    def test_partial_theme_inherits_defaults_and_allows_overrides(self):
        script = """
        (async()=>{
          if(document.readyState!=='complete'){
            await new Promise(resolve=>window.addEventListener('load',resolve,{once:true}));
          }
          const originalCopy=JSON.stringify(ATSIProductCopy);
          const originalPricing=JSON.stringify(pricingSnapshot());
          // Simula um tema que não informou as cores nem a tipografia comuns.
          document.querySelector('link[href="assets/companies/jan/theme.css"]').remove();
          const base=getComputedStyle(document.body);
          const inherited={color:base.color,font:base.fontFamily,background:base.backgroundImage};
          const custom=document.createElement('style');
          custom.textContent=':root[data-company="jan"]{--brand-font-family:Georgia,serif;--brand-primary:#ffaa00}';
          document.head.append(custom);
          const result={inherited,customFont:getComputedStyle(document.body).fontFamily,
            buttonFont:getComputedStyle(document.querySelector('button')).fontFamily,
            primary:getComputedStyle(document.documentElement).getPropertyValue('--brand-primary').trim(),
            copyUnchanged:JSON.stringify(ATSIProductCopy)===originalCopy,
            pricingUnchanged:JSON.stringify(pricingSnapshot())===originalPricing,
            title:document.querySelector('h1').textContent,errors:brandErrors};
          document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        })();
        """
        result = self.browser("home.html", "?company=jan", script)
        self.assertEqual(result["inherited"]["color"], "rgb(239, 248, 247)")
        self.assertIn("Montserrat", result["inherited"]["font"])
        self.assertIn("parallax.jpg", result["inherited"]["background"])
        self.assertIn("Georgia", result["customFont"])
        self.assertEqual(result["buttonFont"], result["customFont"])
        self.assertEqual(result["primary"], "#ffaa00")
        self.assertEqual(result["title"], "Plataforma JAN")
        self.assertTrue(result["copyUnchanged"])
        self.assertTrue(result["pricingUnchanged"])
        self.assertEqual(result["errors"], [])

    def test_mobile_configurator(self):
        script = """
        const result={overflow:document.documentElement.scrollWidth>innerWidth,
          errors:brandErrors,total:targetTotal,company:ATSIProduct.company};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        result = self.browser("home.html", "?company=jan", script, width=390)
        self.assertFalse(result["overflow"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["total"], 178000)


if __name__ == "__main__":
    unittest.main()
