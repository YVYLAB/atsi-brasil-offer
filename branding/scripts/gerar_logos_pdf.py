#!/usr/bin/env python3
"""Empacota as logos institucionais para PDF offline, sem dependências Python.

Rasteriza os originais SVG/PNG com Chrome, sem recorte/recoloração. O JavaScript
gerado permite abrir home.html via file:// sem fetch, CORS ou rede no PDF.
"""
import base64
import hashlib
import json
import shutil
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    "atsi-brasil": "branding/assets/atsi-logo-cabecalho.svg",
    "jan": "assets/companies/jan/logo-institucional.svg",
    "bocchi-agrobios": "assets/companies/bocchi-agrobios/logo-institucional.svg",
    "yvy-lab": "assets/companies/yvy-lab/logo-yvylab.png",
    "grazmec": "assets/companies/grazmec/logo-institucional.svg",
}


def main():
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Chrome/Chromium é necessário apenas para regenerar as logos.")
    logos = {}
    with tempfile.TemporaryDirectory(prefix="pdf-logos-", dir="/tmp/opencode") as directory:
        temp = Path(directory)
        for company, source in SOURCES.items():
            original = ROOT / source
            if original.suffix.lower() == ".png":
                raw = original.read_bytes()
                if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise ValueError(f"PNG inválido: {source}")
                source_width, source_height = struct.unpack(">II", raw[16:24])
            else:
                viewbox = list(map(float, ET.parse(original).getroot().attrib["viewBox"].split()))
                source_width, source_height = viewbox[2:4]
            width = 1024
            height = round(width * source_height / source_width)
            page, image = temp / f"{company}.html", temp / f"{company}.png"
            page.write_text(
                '<!doctype html><style>html,body{margin:0;background:transparent}'
                'img{display:block;width:100vw;height:100vh;object-fit:contain}</style>'
                f'<img src="{original.as_uri()}">',
                encoding="utf-8",
            )
            subprocess.run([
                chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--hide-scrollbars",
                "--force-device-scale-factor=1", "--default-background-color=00000000",
                f"--window-size={width},{height}", "--virtual-time-budget=1000",
                f"--screenshot={image}", page.as_uri(),
            ], check=True, capture_output=True, timeout=30)
            content = image.read_bytes()
            if not content.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("A rasterização não gerou PNG.")
            actual_width, actual_height = struct.unpack(">II", content[16:24])
            if (actual_width, actual_height) != (width, height):
                raise ValueError("Dimensões inesperadas na rasterização.")
            logos[company] = {
                "company": company,
                "source": source,
                "sourceSha256": hashlib.sha256(original.read_bytes()).hexdigest(),
                "width": width,
                "height": height,
                "dataURL": "data:image/png;base64," + base64.b64encode(content).decode("ascii"),
            }
    target = ROOT / "branding/pdf-logos.js"
    target.write_text(
        "/* Gerado por branding/scripts/gerar_logos_pdf.py. Não editar manualmente. */\n"
        "globalThis.CompanyPDFLogos=Object.freeze("
        + json.dumps(logos, ensure_ascii=False, separators=(",", ":"))
        + ");\n",
        encoding="utf-8",
    )
    print(f"{target.relative_to(ROOT)}: {len(logos)} logos institucionais offline.")


if __name__ == "__main__":
    main()
