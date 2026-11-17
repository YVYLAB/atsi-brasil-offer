"""Gera especificações iniciais ausentes e atualiza os dados locais do popup.

Os arquivos existentes nunca são sobrescritos. As horas distribuídas são hipóteses,
não validações; detalhes e tarefas exigem revisão humana.
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "specs"
SOURCE = ROOT / "docs/features-iniciais-custo.md"
HTML = ROOT / "home.html"
pattern = re.compile(
    r"^\| `(\w+)` \| ([^|]+) \| \*\*(.*?)\*\*: (.*?) \| ([^|]+) \| "
    r"([^|]+) \| ([^|]+) \| ([^|]+) \| (.*?) \|$", re.M
)
dependencies = {
    "C04": "B07 (progresso)", "C06": "C05 (quizzes) e fonte autorizada",
    "C07": "fonte textual ou transcrição autorizada e serviço de IA",
    "N02": "N01 (push básico)", "N03": "N01 (push básico)",
    "G02": "validação técnica, APIs oficiais, permissões e elegibilidade de cada rede e destino",
    "G06": "G05 (perfis públicos)", "EV02": "EV01 (eventos e inscrições)",
    "EV03": "EV01 e B03 (e-mail transacional)", "EV04": "EV01 e EV02",
    "P02": "estratégia de pagamento e regras das lojas a validar",
    "P03": "P05 e estratégia de pagamento compatível com as lojas",
    "P04": "EV01 e P01 ou estratégia de pagamento aprovada",
    "P05": "B06 e regras de direitos de acesso a definir",
    "P06": "EV01 e regras de elegibilidade a definir",
    "P07": "E01 e regras de elegibilidade a definir",
    "R01": "telemetria de visualizações a definir", "R02": "B07",
    "R03": "C09", "R04": "definição e coleta de usuários ativos",
    "R05": "mecanismo de presença e heartbeat",
    "GM01": "B07 e regras de pontuação compatíveis com o provedor de vídeo",
    "GM02": "GM01 e check-in confirmado EV04", "GM03": "GM01",
    "GM04": "GM01 e GM03",
}
legacy = {
    "mfa": "A01", "login_google": "A02", "login_microsoft": "A03",
    "ebook_vitrine": "M01", "curso_youtube": "C01", "curso_privado": "C02",
    "curso_offline": "C03", "certificados": "C04", "quizzes": "C05",
    "comentarios_aulas": "C08", "biblioteca_ebooks": "E01",
    "push_basico": "N01", "push_segmentado": "N02", "automacoes": "N03",
}


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


rows = pattern.findall(SOURCE.read_text(encoding="utf-8"))
if len(rows) != 54 or len({row[0] for row in rows}) != 54:
    raise SystemExit("Catálogo inválido: esperados 54 IDs únicos.")
catalog = {}
created = 0
for code, module, title, description, kind, hours, price, complexity, operation in rows:
    files = list(SPECS.glob(f"{code}-*.md"))
    if len(files) > 1:
        raise SystemExit(f"Mais de uma especificação para {code}.")
    dep = dependencies.get(code, "fundação e base aplicáveis; detalhes a validar")
    hours_match = re.search(r"\d+", hours)
    n = int(hours_match.group()) if hours_match else None
    if not files:
        path = SPECS / f"{code}-{slug(title)}.md"
        if n is None:
            task_rows = [
                ("Validar documentação oficial, elegibilidade e viabilidade", "A estimar"),
                ("Definir escopo e alternativa autorizada com a ATSI", "A estimar"),
                ("Detalhar implementação e testes somente após viabilidade", "A estimar"),
            ]
            total = "Sob cotação"
        else:
            # Distribuição inicial, não uma medição ou aprovação da equipe.
            a, b, c = round(n * .15), round(n * .35), round(n * .30)
            task_rows = [
                (f"Detalhar regras, estados e critérios de aceite — {title}", str(a)),
                (f"Implementar dados, integrações e permissões — {title}", str(b)),
                (f"Implementar interface e fluxos — {title}", str(c)),
                (f"Testar, revisar erros e homologar — {title}", str(n - a - b - c)),
            ]
            total = f"{n} h"
        tasks = "\n".join(f"| {task} | {estimate} | Pendente |" for task, estimate in task_rows)
        text = f"""# {code} — {title}

**Status:** rascunho não validado. Horas de referência do catálogo: {total}.
As tarefas e sua distribuição são hipóteses iniciais para revisão com a equipe;
não representam medições nem aprovação de escopo.

## Descrição e funcionamento
{description}

## Escopo e exclusões
Implementar somente a entrega descrita acima, sem contabilizar novamente a fundação
ou assinaturas compartilhadas. Escopo detalhado e integrações adicionais: a validar.

## Tarefas para validação
| Tarefa | Horas propostas | Status |
|---|---:|---|
{tasks}
| **Total** | **{total}** | **Pendente** |

## Dependências e riscos
{dep}. Validar regras de negócio, privacidade, plataformas e limites do fornecedor.
{"Não utilizar automação não oficial nem prometer integração antes da validação." if code == "G02" else ""}

## Custos esperados
Referência de implantação do catálogo: {price.strip()}. Não é preço comercial aprovado.
Operação: {operation.strip()} Custos compartilhados não devem ser cobrados por feature;
condições, volume e preços atuais precisam de confirmação.

Fonte: `docs/features-iniciais-custo.md`, data-base 16/11/2026.
"""
        path.write_text(text, encoding="utf-8")
        created += 1
        files = [path]
    spec_text = files[0].read_text(encoding="utf-8")
    tasks = re.findall(r"^\| (?!\*\*Total)([^|\n]+) \| ([^|\n]+) \| Pendente \|$", spec_text, re.M)
    reviewed = re.findall(r"^\| [A-Z]+\d+-T\d+[A-Z]? \| ([^|\n]+) \| (\d+) \| Revisão técnica preliminar \|$", spec_text, re.M)
    if reviewed:
        n = sum(int(estimate) for _, estimate in reviewed)
        tasks = reviewed
        declared = re.search(r"\| \*\*Total\*\* \| \| \*\*(\d+) h\*\*", spec_text)
        if not declared or int(declared.group(1)) != n:
            raise SystemExit(f"Soma de tarefas divergente em {code}")
    criterion = re.search(r"## Cenário mínimo específico de aceite\n(.*?)(?=\n## |\Z)", spec_text, re.S)
    catalog[code] = {"title": title, "module": module.strip(), "description": description, "hours": n,
                     "kind": kind.strip(), "complexity": int(complexity.strip()),
                     "dependencies": dep, "operation": operation.strip(),
                     "tasks": [f"{task.strip()} — {estimate.strip()}" for task, estimate in tasks],
                     "acceptance": criterion.group(1).strip() if criterion else "A definir",
                     "file": files[0].name}

foundation = []
for path in sorted(SPECS.glob("F[0-9][0-9]-*.md")):
    text = path.read_text()
    tasks = re.findall(r"^\| F\d+-T\d+ \| ([^|\n]+) \| (\d+) \| Revisão técnica preliminar \|$", text, re.M)
    if not tasks:
        raise SystemExit(f"Fundação sem revisão de tarefas: {path.name}")
    foundation.append({
        "id": path.name.split("-")[0],
        "title": text.splitlines()[0].removeprefix("# "),
        "hours": sum(int(hours) for _, hours in tasks),
        "tasks": [f"{task} — {hours} h" for task, hours in tasks],
    })

html = HTML.read_text(encoding="utf-8")
start = "    // BEGIN GENERATED SPEC CATALOG"
end = "    // END GENERATED SPEC CATALOG"
payload = (f"{start}\n    const specCatalog = {json.dumps(catalog, ensure_ascii=False)};\n"
           f"    const foundationCatalog = {json.dumps(foundation, ensure_ascii=False)};\n"
           f"    const legacySpecIds = {json.dumps(legacy, ensure_ascii=False)};\n{end}")
if html.count(start) != 1 or html.count(end) != 1:
    raise SystemExit("Marcadores do catálogo ausentes ou duplicados no HTML.")
html = html[:html.index(start)] + payload + html[html.index(end) + len(end):]
HTML.write_text(html, encoding="utf-8")
print(f"{created} especificações criadas; {len(rows)} itens incluídos no catálogo local.")
