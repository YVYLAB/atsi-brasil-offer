#!/usr/bin/env python3
"""Baixa SVGs originais do site institucional ATSI para uso local (requer internet).
Não cria logos alternativos nem embute assets remotos."""
from pathlib import Path
from urllib.request import urlopen, Request
import hashlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets"
DEST.mkdir(parents=True, exist_ok=True)
ASSETS = {
    "atsi-logo-institucional.svg": "https://www.atsibrasil.com.br/assets/logo-dif-c56ad7a9c36c4768a56ea416da4f0d9b.svg",
    "atsi-logo-cabecalho.svg": "https://www.atsibrasil.com.br/assets/logo-6dbdce245eead0fed844a9778975f7f2.svg",
}

def validate_svg(data: bytes):
    if len(data) < 64 or len(data) > 5_000_000:
        raise ValueError("Tamanho do SVG inesperado")
    root = ET.fromstring(data)
    if root.tag.split('}')[-1].lower() != 'svg':
        raise ValueError("Resposta não é SVG")
    # Fail closed on scripts / embedded remote references until reviewed by developer.
    for item in root.iter():
        tag = item.tag.split('}')[-1].lower()
        if tag in {'script', 'foreignobject'}:
            raise ValueError(f"Elemento potencialmente ativo encontrado: {tag}")
        for k, v in item.attrib.items():
            key = k.split('}')[-1].lower()
            if key.startswith('on') or (key == 'href' and v.strip().lower().startswith(('http:', 'https:', 'javascript:'))):
                raise ValueError('Referência externa ou manipulador ativo detectado')

for name, url in ASSETS.items():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (ATSI brand asset fetch)'} )
    try:
        with urlopen(req, timeout=25) as res:
            body = res.read(5_000_001)
            content_type = res.headers.get('Content-Type', '')
        validate_svg(body)
        output = DEST / name
        output.write_bytes(body)
        print(f"OK: {output.relative_to(ROOT)} | {len(body)} bytes | sha256={hashlib.sha256(body).hexdigest()} | tipo={content_type}")
    except Exception as exc:
        print(f"ERRO em {name}: {exc}. Sem arquivo original; não use placeholder como logo oficial.")
        raise SystemExit(1)
