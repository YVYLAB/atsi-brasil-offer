"""Uma única oferta/catálogo, com identidade escolhida por URL."""
import hashlib
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
    def test_shared_link_metadata_is_generic_without_javascript(self):
        for page in ("index.html", "home.html"):
            with self.subTest(page=page):
                source = (ROOT / page).read_text().split("</head>", 1)[0]
                self.assertIn("<title>YvyLab Community Platform</title>", source)
                self.assertIn('<meta property="og:title" content="YvyLab Community Platform">', source)
                self.assertIn('<meta name="twitter:title" content="YvyLab Community Platform">', source)
                for name in ("description", "og:description", "twitter:description"):
                    pattern = rf'<meta (?:name|property)="{name}" content="([^"]+)">'
                    content = re.search(pattern, source)
                    self.assertIsNotNone(content)
                    self.assertNotIn("ATSI", content.group(1))

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
        bocchi = self.browser("home.html", "?company=bocchi-agrobios", script)
        yvy = self.browser("home.html", "?company=yvy-lab", script)
        grazmec = self.browser("home.html", "?company=grazmec", script)
        kuhn = self.browser("home.html", "?company=kuhn", script)
        cotrijal = self.browser("home.html", "?company=cotrijal", script)
        tentos = self.browser("home.html", "?company=3tentos", script)
        self.assertEqual(atsi["plans"], tentos["plans"])
        self.assertEqual(atsi["commonCopy"], tentos["commonCopy"])
        self.assertEqual(tentos["heading"], "3tentos+")
        self.assertEqual(tentos["logoAlt"], "3tentos")
        self.assertEqual(tentos["logo"], "assets/companies/3tentos/logo-institucional.svg")
        self.assertEqual(tentos["primary"].lower(), "#ed7278")
        self.assertEqual(tentos["project"]["product"], "3tentos+")
        self.assertEqual(tentos["pdfProject"]["institutionalLogo"]["company"], "3tentos")
        self.assertEqual(tentos["storageKey"], "atsi-campaign-v2:company:3tentos")
        self.assertTrue(tentos["pdfIsValid"])
        self.assertTrue(tentos["mockups"])
        self.assertTrue(tentos["popups"])
        self.assertEqual(atsi["plans"], cotrijal["plans"])
        self.assertEqual(atsi["commonCopy"], cotrijal["commonCopy"])
        self.assertEqual(cotrijal["heading"], "Cotrijal+")
        self.assertEqual(cotrijal["logoAlt"], "Cotrijal")
        self.assertEqual(cotrijal["logo"], "assets/companies/cotrijal/logo-institucional.svg")
        self.assertEqual(cotrijal["primary"].lower(), "#f16a7b")
        self.assertEqual(cotrijal["project"]["product"], "Cotrijal+")
        self.assertEqual(cotrijal["pdfProject"]["institutionalLogo"]["company"], "cotrijal")
        self.assertEqual(cotrijal["storageKey"], "atsi-campaign-v2:company:cotrijal")
        self.assertTrue(cotrijal["pdfIsValid"])
        self.assertTrue(cotrijal["mockups"])
        self.assertTrue(cotrijal["popups"])
        self.assertEqual(atsi["plans"], kuhn["plans"])
        self.assertEqual(atsi["commonCopy"], kuhn["commonCopy"])
        self.assertEqual(kuhn["heading"], "KUHN+")
        self.assertEqual(kuhn["logoAlt"], "KUHN Brasil")
        self.assertEqual(kuhn["logo"], "assets/companies/kuhn/logo-institucional.svg")
        self.assertEqual(kuhn["primary"].lower(), "#ee5148")
        self.assertEqual(kuhn["project"]["product"], "KUHN+")
        self.assertEqual(kuhn["pdfProject"]["institutionalLogo"]["company"], "kuhn")
        self.assertEqual(kuhn["storageKey"], "atsi-campaign-v2:company:kuhn")
        self.assertTrue(kuhn["pdfIsValid"])
        self.assertTrue(kuhn["mockups"])
        self.assertTrue(kuhn["popups"])
        self.assertEqual(atsi["plans"], grazmec["plans"])
        self.assertEqual(atsi["commonCopy"], grazmec["commonCopy"])
        self.assertEqual(grazmec["heading"], "Grazmec+")
        self.assertEqual(grazmec["logoAlt"], "Grazmec")
        self.assertEqual(grazmec["logo"], "assets/companies/grazmec/logo-institucional.svg")
        self.assertEqual(grazmec["primary"].lower(), "#f04a51")
        self.assertEqual(grazmec["project"]["product"], "Grazmec+")
        self.assertEqual(grazmec["pdfProject"]["institutionalLogo"]["company"], "grazmec")
        self.assertEqual(grazmec["storageKey"], "atsi-campaign-v2:company:grazmec")
        self.assertTrue(grazmec["pdfIsValid"])
        self.assertTrue(grazmec["mockups"])
        self.assertTrue(grazmec["popups"])
        self.assertEqual(atsi["plans"], yvy["plans"])
        self.assertEqual(yvy["heading"], "YVY+")
        self.assertEqual(yvy["logoAlt"], "YvyLab")
        self.assertEqual(yvy["logo"], "assets/companies/yvy-lab/logo-yvylab.png")
        self.assertEqual(yvy["primary"].lower(), "#c152fb")
        self.assertEqual(yvy["project"]["product"], "YVY+")
        self.assertEqual(yvy["pdfProject"]["institutionalLogo"]["company"], "yvy-lab")
        self.assertEqual(yvy["storageKey"], "atsi-campaign-v2:company:yvy-lab")
        self.assertTrue(yvy["pdfIsValid"])
        self.assertTrue(yvy["mockups"])
        self.assertTrue(yvy["popups"])
        self.assertEqual(atsi["plans"], bocchi["plans"])
        self.assertEqual(atsi["commonCopy"], bocchi["commonCopy"])
        self.assertEqual(bocchi["heading"], "Bocchi+")
        self.assertEqual(bocchi["logoAlt"], "Bocchi Agrobios")
        self.assertEqual(bocchi["logo"], "assets/companies/bocchi-agrobios/logo-institucional.svg")
        self.assertEqual(bocchi["primary"].lower(), "#d3a449")
        self.assertEqual(bocchi["project"]["product"], "Bocchi+")
        self.assertEqual(bocchi["pdfProject"]["institutionalLogo"]["company"], "bocchi-agrobios")
        self.assertEqual(bocchi["storageKey"], "atsi-campaign-v2:company:bocchi-agrobios")
        self.assertTrue(bocchi["pdfIsValid"])
        self.assertTrue(bocchi["mockups"])
        self.assertTrue(bocchi["popups"])
        self.assertEqual(atsi["plans"], jan["plans"], "Catálogo e cálculos devem ser idênticos")
        self.assertEqual(atsi["commonCopy"], jan["commonCopy"],
                         "Textos devem ser os mesmos, alterando apenas os nomes da identidade")
        self.assertEqual([p["pricing"]["finalCents"] for p in jan["plans"].values()],
                         [17800000, 23000000, 38920000])
        self.assertEqual(jan["company"], "jan")
        self.assertEqual(jan["heading"], "JAN+")
        self.assertEqual(atsi["heading"], "ATSI+")
        self.assertNotIn("ATSI", jan["title"])
        self.assertNotIn("ATSI", jan["metadata"])
        self.assertEqual(jan["primary"].lower(), "#ff8031")
        self.assertNotEqual(atsi["headerBackground"], jan["headerBackground"])
        self.assertEqual(jan["logo"], "assets/companies/jan/logo-institucional.svg")
        self.assertEqual(jan["logoAlt"], "JAN")
        self.assertEqual(atsi["logo"], "branding/assets/atsi-logo-cabecalho.svg")
        self.assertEqual(atsi["logoAlt"], "ATSI Brasil")
        self.assertEqual(jan["favicon"], "assets/companies/jan/icon.png")
        self.assertEqual(jan["project"]["company"], "jan")
        self.assertEqual(jan["project"]["product"], "JAN+")
        self.assertEqual(atsi["project"]["product"], "ATSI+")
        pdf_project = dict(jan["pdfProject"])
        logo = pdf_project.pop("institutionalLogo")
        self.assertEqual(logo["company"], "jan")
        self.assertEqual(logo["source"], "assets/companies/jan/logo-institucional.svg")
        self.assertTrue(logo["dataURL"].startswith("data:image/png;base64,"))
        self.assertEqual(pdf_project, jan["project"])
        self.assertEqual(jan["pdfProject"]["branding"]["header"], [36, 54, 63])
        self.assertEqual(jan["pdfProject"]["branding"]["accent"], [255, 128, 49])
        self.assertNotIn("brandingNotice", jan["pdfProject"])
        self.assertNotIn("brandingNotice", atsi["project"])
        self.assertTrue(jan["pdfName"].startswith("jan-Oferta-"))
        self.assertTrue(jan["pdfIsValid"])
        self.assertFalse(jan["pdfHasATSI"])
        self.assertTrue(jan["mockups"])
        self.assertTrue(jan["popups"])
        self.assertEqual(atsi["storageKey"], "atsi-campaign-v2")
        self.assertEqual(jan["storageKey"], "atsi-campaign-v2:company:jan")
        self.assertEqual(atsi["isolationTotal"], 160200)
        self.assertEqual(jan["isolationTotal"], 178000)
        for result in (atsi, jan, bocchi, yvy, grazmec, kuhn, cotrijal, tentos):
            self.assertTrue(result["logoLoaded"])
            self.assertFalse(result["overflow"])
            self.assertEqual(result["errors"], [])
            self.assertEqual(result["link"], result["company"])

    def test_institutional_entry_logo_and_product_mockups(self):
        entry_script = """
        const image=document.querySelector('[data-company-logo]');
        const result={src:image.getAttribute('src'),alt:image.alt};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        entry = self.browser("index.html", "?company=atsi-brasil", entry_script)
        self.assertEqual(entry["src"], "branding/assets/atsi-logo-cabecalho.svg")
        self.assertEqual(entry["alt"], "ATSI Brasil")
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

    def test_bocchi_entry_and_mobile(self):
        script = """
        (async()=>{
          const image=document.querySelector('[data-company-logo]');
          await image.decode();
          const result={name:ATSIProduct.name,src:image.getAttribute('src'),
            alt:image.alt,loaded:image.naturalWidth>0,
            intro:document.querySelector('.intro').textContent,
            link:CompanyBranding.pageURL('home.html').searchParams.get('company'),
            overflow:document.documentElement.scrollWidth>window.innerWidth,
            errors:brandErrors};
          document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        })();
        """
        for width in (390, 1440):
            with self.subTest(width=width):
                result = self.browser("index.html", "?company=bocchi-agrobios", script, width)
                self.assertEqual(result["name"], "Bocchi+")
                self.assertEqual(result["alt"], "Bocchi Agrobios")
                self.assertEqual(result["src"], "assets/companies/bocchi-agrobios/logo-institucional.svg")
                self.assertIn("Bocchi+", result["intro"])
                self.assertEqual(result["link"], "bocchi-agrobios")
                self.assertTrue(result["loaded"])
                self.assertFalse(result["overflow"])
                self.assertEqual(result["errors"], [])

    def test_yvy_entry_responsive(self):
        script = """
          const image=document.querySelector('[data-company-logo]');
          const result={name:ATSIProduct.name,src:image.getAttribute('src'),
            alt:image.alt,
            intro:document.querySelector('.intro').textContent,
            link:CompanyBranding.pageURL('home.html').searchParams.get('company'),
            overflow:document.documentElement.scrollWidth>window.innerWidth,errors:brandErrors};
          document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        for width in (390, 768, 1440):
            with self.subTest(width=width):
                result = self.browser("index.html", "?company=yvy-lab", script, width)
                self.assertEqual(result["name"], "YVY+")
                self.assertEqual(result["alt"], "YvyLab")
                self.assertEqual(result["src"], "assets/companies/yvy-lab/logo-yvylab.png")
                self.assertIn("YVY+", result["intro"])
                self.assertEqual(result["link"], "yvy-lab")
                self.assertFalse(result["overflow"])
                self.assertEqual(result["errors"], [])

    def test_3tentos_entry_responsive(self):
        script = """
        const image=document.querySelector('[data-company-logo]');
        const result={name:ATSIProduct.name,src:image.getAttribute('src'),alt:image.alt,
          intro:document.querySelector('.intro').textContent,
          link:CompanyBranding.pageURL('home.html').searchParams.get('company'),
          overflow:document.documentElement.scrollWidth>window.innerWidth,errors:brandErrors};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        for width in (390, 768, 1440):
            with self.subTest(width=width):
                result = self.browser("index.html", "?company=3tentos", script, width)
                self.assertEqual(result["name"], "3tentos+")
                self.assertEqual(result["alt"], "3tentos")
                self.assertEqual(result["src"], "assets/companies/3tentos/logo-institucional.svg")
                self.assertIn("3tentos+", result["intro"])
                self.assertEqual(result["link"], "3tentos")
                self.assertFalse(result["overflow"])
                self.assertEqual(result["errors"], [])

    def test_cotrijal_entry_responsive(self):
        script = """
        const image=document.querySelector('[data-company-logo]');
        const result={name:ATSIProduct.name,src:image.getAttribute('src'),alt:image.alt,
          intro:document.querySelector('.intro').textContent,
          link:CompanyBranding.pageURL('home.html').searchParams.get('company'),
          overflow:document.documentElement.scrollWidth>window.innerWidth,errors:brandErrors};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        for width in (390, 768, 1440):
            with self.subTest(width=width):
                result = self.browser("index.html", "?company=cotrijal", script, width)
                self.assertEqual(result["name"], "Cotrijal+")
                self.assertEqual(result["alt"], "Cotrijal")
                self.assertEqual(result["src"], "assets/companies/cotrijal/logo-institucional.svg")
                self.assertIn("Cotrijal+", result["intro"])
                self.assertEqual(result["link"], "cotrijal")
                self.assertFalse(result["overflow"])
                self.assertEqual(result["errors"], [])

    def test_kuhn_entry_responsive(self):
        script = """
        const image=document.querySelector('[data-company-logo]');
        const result={name:ATSIProduct.name,src:image.getAttribute('src'),alt:image.alt,
          intro:document.querySelector('.intro').textContent,
          copy:document.querySelector('.login').textContent,
          link:CompanyBranding.pageURL('home.html').searchParams.get('company'),
          overflow:document.documentElement.scrollWidth>window.innerWidth,errors:brandErrors};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        for width in (390, 768, 1440):
            with self.subTest(width=width):
                result = self.browser("index.html", "?company=kuhn", script, width)
                self.assertEqual(result["name"], "KUHN+")
                self.assertEqual(result["alt"], "KUHN Brasil")
                self.assertEqual(result["src"], "assets/companies/kuhn/logo-institucional.svg")
                self.assertIn("KUHN+", result["intro"])
                self.assertNotIn("não oficial", result["copy"].lower())
                self.assertEqual(result["link"], "kuhn")
                self.assertFalse(result["overflow"])
                self.assertEqual(result["errors"], [])

    def test_grazmec_entry_responsive(self):
        script = """
        const image=document.querySelector('[data-company-logo]');
        const result={name:ATSIProduct.name,src:image.getAttribute('src'),alt:image.alt,
          intro:document.querySelector('.intro').textContent,
          link:CompanyBranding.pageURL('home.html').searchParams.get('company'),
          overflow:document.documentElement.scrollWidth>window.innerWidth,errors:brandErrors};
        document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        """
        for width in (390, 768, 1440):
            with self.subTest(width=width):
                result = self.browser("index.html", "?company=grazmec", script, width)
                self.assertEqual(result["name"], "Grazmec+")
                self.assertEqual(result["alt"], "Grazmec")
                self.assertEqual(result["src"], "assets/companies/grazmec/logo-institucional.svg")
                self.assertIn("Grazmec+", result["intro"])
                self.assertEqual(result["link"], "grazmec")
                self.assertFalse(result["overflow"])
                self.assertEqual(result["errors"], [])

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
          heading:document.querySelector('h1').textContent,product:ATSIProduct.name,
          headingSize:parseFloat(getComputedStyle(document.querySelector('h1')).fontSize),
          hasEyebrow:!!document.querySelector('.eyebrow'),
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
            product_name = "ATSI+" if company == "atsi-brasil" else "JAN+"
            self.assertEqual(result["heading"], f"Vamos apresentar a plataforma {product_name}.")
            self.assertLessEqual(result["headingSize"], 16)
            self.assertFalse(result["hasEyebrow"])
            self.assertEqual(result["product"], product_name)
            self.assertEqual(result["title"], "YvyLab Community Platform")
            expected_logo = ("branding/assets/atsi-logo-cabecalho.svg" if company == "atsi-brasil"
                             else "assets/companies/jan/logo-institucional.svg")
            self.assertEqual(result["logo"], expected_logo)
            self.assertEqual(result["errors"], [])
            self.assertFalse(result["overflow"])
            if expected == "jan":
                self.assertNotIn("ATSI", result["intro"])

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
        self.assertEqual(result["title"], "JAN+")
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

    def test_jan_original_assets_integrity(self):
        folder = ROOT / "assets/companies/jan"
        manifest = json.loads((folder / "sources.json").read_text())
        for asset in manifest["officialAssets"]:
            with self.subTest(asset=asset["file"]):
                content = (folder / asset["file"]).read_bytes()
                self.assertEqual(len(content), asset["bytes"])
                self.assertEqual(hashlib.sha256(content).hexdigest(), asset["sha256"])
                self.assertTrue(asset["source"].startswith("https://www.jan.com.br/source/"))
        self.assertTrue((folder / "icon.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
        for asset in manifest["decorativeAssets"]:
            self.assertTrue((folder / asset["file"]).is_file())

    def test_jan_kit_visual_identity_and_responsive_layout(self):
        script = """
        (async()=>{
          if(document.readyState!=='complete'){
            await new Promise(resolve=>window.addEventListener('load',resolve,{once:true}));
          }
          const content=document.querySelector('.page') || document.querySelector('.login');
          const images=[...document.querySelectorAll('[data-company-logo],.app-brand img')];
          const loaded=await Promise.all(images.map(image=>image.decode().then(()=>image.naturalWidth>0,()=>false)));
          const primary=getComputedStyle(document.documentElement).getPropertyValue('--brand-primary').trim();
          const model=typeof buildOfferPDFModel==='function'?buildOfferPDFModel():null;
          const doc=model?ATSIOfferPDF.createDocument(model).output():null;
          const result={heading:document.querySelector('h1').textContent,
            noPublicNotice:!document.querySelector('[data-company-disclaimer]') &&
              !/não aprovad[ao]/i.test(content.textContent),
            overflow:document.documentElement.scrollWidth>innerWidth,
            primary,imagesLoaded:loaded.every(Boolean),errors:brandErrors,
            iconType:document.querySelector('link[rel=icon]').type,
            pdfCommercial:doc===null || (doc.startsWith('%PDF') && !('brandingNotice' in model.project))};
          document.body.insertAdjacentHTML('beforeend','<pre id="brand-result">'+JSON.stringify(result)+'</pre>');
        })();
        """
        for page in ("index.html", "home.html"):
            for width in (390, 768, 1440):
                with self.subTest(page=page, width=width):
                    result = self.browser(page, "?company=jan", script, width=width)
                    expected_heading = "Vamos apresentar a plataforma JAN+." if page == "index.html" else "JAN+"
                    self.assertEqual(result["heading"], expected_heading)
                    self.assertTrue(result["noPublicNotice"])
                    self.assertEqual(result["primary"].lower(), "#ff8031")
                    self.assertEqual(result["iconType"], "image/png")
                    self.assertTrue(result["imagesLoaded"])
                    self.assertTrue(result["pdfCommercial"])
                    self.assertFalse(result["overflow"])
                    self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()
