import base64
import json
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalized(text):
    return " ".join(text.replace("—", "-").replace("–", "-").replace("**", "").replace("`", "").split())


class OfferPDFTest(unittest.TestCase):
    def test_generated_offer_documents(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        script = """
        (async()=>{
          const documents=[];
          function capture(name,now=Date.now()){
            const model=buildOfferPDFModel(now);
            const doc=ATSIOfferPDF.createDocument(model);
            documents.push({name,model,pdf:doc.output('datauristring').split(',')[1],pages:doc.getNumberOfPages()});
          }
          currentOffer=null;campaignConfig=null;applyPreset('essencial');capture('essencial');
          campaignConfig={schemaVersion:2,startsAt:new Date(Date.now()-3600000).toISOString(),
            endsAt:new Date(Date.now()+3600000).toISOString(),
            percentages:{essencial:10,plus:15,premium:20},additionalOptionalPercentage:25};
          applyPreset('premium');toggleFeature('G02',true);toggleFeature('A04',true);
          capture('premium-adicionais');
          capture('expirada',Date.parse(campaignConfig.endsAt)+1);
          applyPreset('essencial');toggleFeature('M01',true);
          document.getElementById('confirmDependencies').click();
          capture('ebooks-dependentes');
          applyPreset('premium');
          for(const feature of features.filter(f=>f.type==='optional'&&!isSelected(f)))toggleFeature(feature.id,true);
          if(dependencyDialog.open)document.getElementById('confirmDependencies').click();
          capture('escopo-completo');
          campaignConfig=null;applyPreset('plus');
          document.getElementById('monthlyActiveUsers').value='10000';
          document.getElementById('monthlyActiveUsers').dispatchEvent(new Event('input'));
          const issued=Date.now();
          const rule=(ids,pct)=>({enabled:true,percentage:pct,eligibleFeatureIds:ids,
            maxDiscountCents:10000000,priceApproval:true,marginApproval:true});
          currentOffer={schemaVersion:1,id:'legacy',quoteId:'legacy',author:'Test',configVersion:'test',
            status:'active',issuedAt:new Date(issued).toISOString(),expiresAt:new Date(issued+86400000).toISOString(),
            snapshot:pricingSnapshot(),config:{plus:rule(['C04'],10),premium:rule(['C04'],20)}};
          capture('legada');
          currentOffer=null;applyPreset('essencial');
          const original=ATSIOfferPDF.createDocument;let saved=null;
          ATSIOfferPDF.createDocument=model=>{
            const doc=original(model);
            doc.save=async name=>{saved={name,header:doc.output().slice(0,5),total:model.pricing.finalCents};};
            return doc;
          };
          const status=document.getElementById('pdfOfferStatus'),button=document.getElementById('generateOfferPDF');
          const done=new Promise(resolve=>{
            const observer=new MutationObserver(()=>{
              if(!button.disabled){observer.disconnect();resolve();}
            });
            observer.observe(button,{attributes:true,attributeFilter:['disabled']});
          });
          const selectedBefore=[...state.selected].join(',');
          button.click();await done;
          const buttonChecks={saved:!!saved&&saved.header==='%PDF-'&&saved.name.endsWith('.pdf'),
            amount:!!saved&&saved.total===17800000,
            message:status.textContent.includes('PDF pronto'),
            state:selectedBefore===[...state.selected].join(',')&&!button.disabled};
          document.body.insertAdjacentHTML('beforeend','<pre id="qa-pdf">'+JSON.stringify({documents,buttonChecks})+'</pre>');
        })();
        """
        page = (ROOT / "home.html").read_text()
        page = page.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
        page = page.replace("</body>", f"<script>{script}</script></body>")
        with tempfile.TemporaryDirectory(prefix="atsi-pdf-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "test.html"
            file.write_text(page)
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--virtual-time-budget=10000",
                "--dump-dom", file.as_uri() + "?company=atsi-brasil"
            ], capture_output=True, text=True, timeout=45)
            match = re.search(r'<pre id="qa-pdf">(\{.*?\})</pre>', run.stdout)
            self.assertIsNotNone(match, "Geração do PDF não completou")
            results = json.loads(match.group(1))
            for name, ok in results["buttonChecks"].items():
                self.assertTrue(ok, f"botão PDF: {name}")
            documents = {item["name"]: item for item in results["documents"]}
            self.assertEqual(documents["essencial"]["model"]["pricing"]["finalCents"], 17800000)
            self.assertEqual(documents["premium-adicionais"]["model"]["pricing"]["finalCents"], 35366000)
            self.assertEqual(documents["expirada"]["model"]["pricing"]["finalCents"], 44560000)
            self.assertEqual(documents["legada"]["model"]["pricing"]["finalCents"], 22916000)
            self.assertEqual(documents["legada"]["model"]["foundationTotals"]["discountCents"], 0)
            ebook_ids = {item["id"] for item in documents["ebooks-dependentes"]["model"]["features"]}
            self.assertTrue({"M01", "E01"}.issubset(ebook_ids))
            self.assertEqual(len(documents["escopo-completo"]["model"]["features"]), 53)
            hash_value = re.search(r"const releaseHash='([a-f0-9]{64})'", (ROOT / "campaign-settings.js").read_text()).group(1)
            for name, item in documents.items():
                with self.subTest(document=name):
                    model = item["model"]
                    self.assertNotIn(hash_value, json.dumps(model))
                    rows = model["foundation"] + model["features"]
                    self.assertEqual(sum(row["finalCents"] for row in rows), model["pricing"]["finalCents"])
                    self.assertEqual(sum(row["hours"] for row in rows), model["totalHours"])
                    self.assertEqual(len(model["foundation"]), 7)
                    support = model["support"]
                    operations = support["operations"]
                    self.assertEqual(sum(line["priceCents"] for line in operations["lines"]), operations["totalCents"])
                    self.assertEqual(support["priceCents"] + operations["totalCents"], support["totalCents"])
                    self.assertEqual(sum(line["estimatedCents"] for line in operations["lines"]), operations["totalEstimatedCents"])
                    if operations["inputs"]["videoStrategy"] == "C01":
                        self.assertEqual(operations["totalCents"], 0)
                        self.assertGreater(operations["totalEstimatedCents"], 0)
                        self.assertEqual(support["totalCents"], support["priceCents"])
                    self.assertEqual(model["benefits"][0]["priceCents"], 0)
                    self.assertGreater(item["pages"], 1)
                    pdf = base64.b64decode(item["pdf"])
                    self.assertTrue(pdf.startswith(b"%PDF-"))
                    pdf_file = Path(directory) / f"{name}.pdf"
                    pdf_file.write_bytes(pdf)
                    if shutil.which("pdfinfo"):
                        info = subprocess.run(["pdfinfo", str(pdf_file)], capture_output=True, text=True, check=True).stdout
                        self.assertRegex(info, rf"Pages:\s+{item['pages']}\b")
                    if not shutil.which("pdftotext"):
                        continue
                    text = subprocess.run(["pdftotext", "-layout", str(pdf_file), "-"], capture_output=True, text=True, check=True).stdout
                    flat = normalized(text)
                    self.assertIn("Oferta técnica e comercial", flat)
                    self.assertIn("Curso de capacitação para administradores", flat)
                    self.assertIn("Manutenção e operação mensal", flat)
                    self.assertIn("Serviços e vídeos - valor estimado", flat)
                    self.assertIn("Total mensal estimado", flat)
                    self.assertIn("Cenário de operação mensal", flat)
                    self.assertIn("não é capacidade garantida", flat)
                    self.assertIn("Câmbio de simulação", flat)
                    self.assertIn("O que compõe sua mensalidade?", flat)
                    self.assertIn("Manutenção do plano:", flat)
                    self.assertIn("Com vídeos pelo YouTube, esse adicional é zero.", flat)
                    self.assertIn("não gera cobranças automáticas", flat)
                    self.assertNotIn("Inclui os custos operacionais da plataforma", flat)
                    self.assertNotIn(hash_value, text)
                    for row in rows:
                        self.assertIn(normalized(row["technicalTitle"]), flat)
                        for task in row["tasks"]:
                            self.assertIn(normalized(task["title"]), flat)
                            task_line = next(line for line in text.splitlines() if re.search(re.escape(task["id"]) + r"(?![A-Za-z0-9])", line))
                            self.assertRegex(task_line, rf"\s{task['hours']}\s*h\s*$")
                    bbox = subprocess.run(["pdftotext", "-bbox", str(pdf_file), "-"], capture_output=True, text=True, check=True).stdout
                    xml = ET.fromstring(bbox)
                    for word in xml.iter():
                        if word.tag.endswith("}word"):
                            self.assertGreaterEqual(float(word.attrib["xMin"]), 0, word.text)
                            self.assertLessEqual(float(word.attrib["xMax"]), 595.5, word.text)
                            self.assertGreaterEqual(float(word.attrib["yMin"]), 0, word.text)
                            self.assertLessEqual(float(word.attrib["yMax"]), 842.5, word.text)
            print(f"PDF: {len(documents)} documentos gerados e composição verificada")
