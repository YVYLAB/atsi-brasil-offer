import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DependenciesTest(unittest.TestCase):
    def test_automatic_dependencies(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        script = """
        const checks=[];
        const check=(name,ok)=>checks.push({name,ok});
        window.confirm=()=>{throw new Error('Inclusão não deve pedir confirmação.');};
        campaignConfig=null;currentOffer=null;
        const cases={
          M01:['E01'],N02:['N01'],N03:['N01'],C06:['C05'],G06:['G05'],
          EV02:['EV01'],EV03:['EV01'],EV04:['EV01','EV02'],
          P02:['P01','P05'],P03:['P01','P05'],P04:['EV01','P01'],
          P07:['E01'],R03:['C09'],GM02:['GM01','EV04','EV01','EV02'],GM04:['GM01','GM03']
        };
        for(const [id,required] of Object.entries(cases)){
          applyPreset('essencial');
          toggleFeature(id,true);
          const expected=178000+getFeature(id).price+required.reduce((n,dep)=>n+getFeature(dep).price,0);
          check(id+' inclui requisitos e preço uma vez',state.selected.has(id) &&
            required.every(dep=>state.selected.has(dep)&&state.autoSelected.has(dep)) && targetTotal===expected);
          check(id+' popup explicativo com OK',dependencyDialog.open &&
            document.getElementById('dependencyDialogDescription').textContent.includes(getFeature(id).title) &&
            document.getElementById('confirmDependencies').textContent==='OK' &&
            document.getElementById('dependencyDialogItems').children.length===required.length);
          check(id+' requisitos bloqueados',required.every(dep=>
            document.querySelector(`[data-feature="${dep}"] .feature-toggle`).disabled));
          const chosenBefore=[...state.selected].join(',');
          toggleFeature(required[0],false);
          check(id+' protege requisito no estado',[...state.selected].join(',')===chosenBefore && targetTotal===expected);
          document.getElementById('confirmDependencies').click();
          check(id+' OK fecha popup',!dependencyDialog.open);
          toggleFeature(id,false);
          check(id+' remove somente requisitos automáticos sem uso',!state.selected.has(id) &&
            required.every(dep=>!state.selected.has(dep)) && state.autoSelected.size===0 && targetTotal===178000);
        }
        applyPreset('essencial');toggleFeature('E01',true);toggleFeature('M01',true);
        check('biblioteca escolhida manualmente não duplica nem abre popup',!dependencyDialog.open &&
          !state.autoSelected.has('E01') && targetTotal===178000+getFeature('E01').price+getFeature('M01').price);
        toggleFeature('M01',false);
        check('biblioteca manual permanece após remover destaque',state.selected.has('E01') &&
          !document.querySelector('[data-feature="E01"] .feature-toggle').disabled &&
          targetTotal===178000+getFeature('E01').price);
        applyPreset('essencial');toggleFeature('N02',true);
        document.getElementById('confirmDependencies').click();toggleFeature('N03',true);
        toggleFeature('N02',false);
        check('requisito compartilhado permanece',state.selected.has('N01')&&state.selected.has('N03'));
        toggleFeature('N03',false);
        check('último uso libera requisito automático',!state.selected.has('N01') && targetTotal===178000);
        for(const key of ['plus','premium']){
          applyPreset(key);toggleFeature('M01',true);
          check(key+' já inclui biblioteca sem duplicidade',!dependencyDialog.open && !state.autoSelected.has('E01') &&
            selectedFeatures().filter(f=>f.id==='E01').length===1);
        }
        document.body.insertAdjacentHTML('beforeend','<pre id="qa-dependencies">'+JSON.stringify(checks)+'</pre>');
        """
        page = (ROOT / "home.html").read_text()
        page = page.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
        page = page.replace("</body>", f"<script>{script}</script></body>")
        with tempfile.TemporaryDirectory(prefix="atsi-dependencies-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "test.html"
            file.write_text(page)
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--dump-dom", file.as_uri()
            ], capture_output=True, text=True, timeout=30)
        match = re.search(r'<pre id="qa-dependencies">(\[.*?\])</pre>', run.stdout)
        self.assertIsNotNone(match, "Teste de dependências não completou")
        checks = json.loads(match.group(1))
        for check in checks:
            self.assertTrue(check["ok"], check["name"])
        print(f"Chrome: {len(checks)} verificações de dependências automáticas aprovadas")
