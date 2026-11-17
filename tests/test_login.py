import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LoginTest(unittest.TestCase):
    def test_visual_entry(self):
        chrome = shutil.which("google-chrome")
        if not chrome:
            self.skipTest("Chrome não disponível")
        page = (ROOT / "index.html").read_text()
        script = """
        (async()=>{
          const results={};
          const email=document.getElementById('loginEmail');
          const pass=document.getElementById('loginPassword');
          document.getElementById('showPassword').click();
          results.show=pass.type==='text';
          document.getElementById('showPassword').click();
          results.hide=pass.type==='password';
          email.value='contato@yvyagro.com';pass.value='incorrect-test';
          document.getElementById('loginForm').requestSubmit();
          await new Promise(resolve=>setTimeout(resolve,50));
          results.error=document.getElementById('loginStatus').textContent.includes('incorretos');
          // Testar a transição de sucesso sem armazenar a senha nos testes.
          crypto.subtle.digest=async()=>Uint8Array.from(demoPasswordHash.match(/../g),v=>parseInt(v,16)).buffer;
          const originalTimeout=window.setTimeout;
          let navigationDelay=null;
          window.setTimeout=(callback,delay)=>{
            if(delay===900){navigationDelay=delay;return 1;}
            return originalTimeout(callback,delay);
          };
          pass.value='success-fixture';
          document.getElementById('loginForm').requestSubmit();
          await new Promise(resolve=>originalTimeout(resolve,50));
          results.animation=document.body.classList.contains('is-opening');
          results.delay=navigationDelay===900;
          results.cleared=pass.value==='';
          document.body.insertAdjacentHTML('beforeend','<pre id="login-result">'+JSON.stringify(results)+'</pre>');
        })();
        """
        page = page.replace("<head>", f'<head><base href="{ROOT.as_uri()}/">', 1)
        page = page.replace("</body>", f"<script>{script}</script></body>")
        with tempfile.TemporaryDirectory(prefix="atsi-login-", dir="/tmp/opencode") as directory:
            file = Path(directory) / "login.html"
            file.write_text(page)
            run = subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--virtual-time-budget=1000",
                "--dump-dom", file.as_uri() + "?company=atsi-brasil"
            ], capture_output=True, text=True, timeout=30)
        match = re.search(r'<pre id="login-result">(\{.*?\})</pre>', run.stdout)
        self.assertIsNotNone(match, "Teste de login não completou")
        for name, ok in json.loads(match.group(1)).items():
            self.assertTrue(ok, name)


if __name__ == "__main__":
    unittest.main()
