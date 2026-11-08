#!/usr/bin/env python3
"""BKS-DAIWL — Don't Accept It Without Learning.

Deterministic scoring, report rendering, configuration and source inventory.
Standard library only (Python 3.9+).

  daiwl.py version
  daiwl.py init --vault <dir> [--create] [--lang en|pt-BR] [--source type:path[:authorship]] [--local]
  daiwl.py sources [ls | add type:path[:authorship] | rm <path>]
  daiwl.py inventory
  daiwl.py score findings.json --out <dir>
  daiwl.py rescore <dir> [--vault <dir>]
  daiwl.py render <dir> [--lang en|pt-BR]

Portuguese aliases: fontes, inventario, versao; --criar, --fonte; repositorio, notas, artigos; propria, mista.
"""
import argparse, fnmatch, html, json, math, os, re, sys
from pathlib import Path

SKILL_VERSION = "1.0.0"
FORMULA_VERSION = "1.0"

# ------------------------------------------------------------------ normalization (0.x pt-BR -> 1.x en)
PT_KEYS = {"fundamentos": "fundamentals", "projeto": "project", "data": "date", "codigo_analisado": "analyzed_path",
           "ferramenta_origem": "source_tool", "nome": "name", "categoria": "category", "peso": "weight",
           "classe": "class", "nivel": "level", "confianca": "confidence", "tipo_experiencia": "experience_type",
           "fundamentado": "grounded", "fonte": "source", "explicacao": "explanation", "porque_ia_usou": "why_ai_used",
           "estudo": "study", "ocorrencias": "occurrences", "arquivo": "file", "linha": "line", "trecho": "snippet"}
PT_VALUES = {"alinhado": "aligned", "lacuna": "gap", "divergente": "divergent", "sem-fundamento": "unfounded",
             "domina": "masters", "conhece": "knows", "declarado": "declared", "aprendido": "learned",
             "experiencia": "experience", "alta": "high", "baixa": "low", "fundamentada": "grounded",
             "contextual": "contextual", "preferencia": "preference"}
TYPE_ALIASES = {"notas": "notes", "repositorio": "repo", "artigos": "papers"}
AUTH_ALIASES = {"propria": "own", "mista": "mixed"}


def normalize(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            k2 = PT_KEYS.get(k, k)
            if k2 in ("class", "level", "confidence", "experience_type") and isinstance(v, str):
                v = PT_VALUES.get(v, v)
            out[k2] = normalize(v)
        return out
    if isinstance(obj, list):
        return [normalize(x) for x in obj]
    return obj


# ------------------------------------------------------------------ scoring
FACTORS = {
    ("aligned", "masters"): 1.00, ("aligned", "knows"): 0.80, ("aligned", "declared"): 0.70,
    ("aligned", "learned", "high"): 0.85, ("aligned", "learned", "low"): 0.60,
    ("aligned", "experience", "grounded"): 1.00, ("aligned", "experience", "contextual"): 1.00,
    ("aligned", "experience", "preference"): 0.50,
    ("gap",): 0.00, ("divergent",): -0.50, ("unfounded",): -0.25,
}
BANDS = [(80, "band_80"), (60, "band_60"), (40, "band_40"), (0, "band_0")]


def factor(f):
    c = f.get("class")
    if c != "aligned":
        return FACTORS.get((c,), 0.0)
    lvl = f.get("level") or "knows"
    if lvl == "learned":
        return FACTORS[("aligned", "learned", f.get("confidence") or "low")]
    if lvl == "experience":
        return FACTORS[("aligned", "experience", f.get("experience_type") or "preference")]
    return FACTORS.get(("aligned", lvl), 0.8)


def impact(f):
    return int(f.get("weight", 1)) * (1 + math.log(max(1, len(f.get("occurrences") or []))))


def compute(data):
    total = acc = 0.0
    by_class, contrib = {}, []
    for f in data["fundamentals"]:
        i, fa = impact(f), factor(f)
        total += i
        acc += i * fa
        by_class[f["class"]] = by_class.get(f["class"], 0) + i
        contrib.append([f["name"], f["class"], round(i * fa, 2), round(i, 2)])
    pms = round(max(0.0, acc / total) * 100, 1) if total else 0.0
    contrib.sort(key=lambda x: x[2])
    return {
        "skill_version": SKILL_VERSION, "formula_version": FORMULA_VERSION,
        "project": data.get("project"), "date": data.get("date"), "language": data.get("language"),
        "pms": pms, "band": next(b for lim, b in BANDS if pms >= lim),
        "total_impact": round(total, 2), "impact_by_class": {k: round(v, 2) for k, v in by_class.items()},
        "worst_contributions": contrib[:3],
        "top_gaps": [c for c in sorted(contrib, key=lambda x: -x[3]) if c[1] == "gap"][:5],
    }


def load_findings(path):
    return normalize(json.loads(Path(path).read_text(encoding="utf-8")))


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_score(a):
    data = load_findings(a.findings)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    dump(out / "findings.json", data)
    res = compute(data)
    previous = sorted(p for p in out.parent.glob("*/score.json") if p.parent != out)
    if previous:
        prev = json.loads(previous[-1].read_text(encoding="utf-8"))
        prev_pms = prev.get("pms", prev.get("smp"))
        if prev.get("formula_version") == FORMULA_VERSION and prev_pms is not None:
            res["delta_previous"] = round(res["pms"] - prev_pms, 1)
        else:
            res["delta_previous"] = None
            res["delta_note"] = "formula_changed"
    dump(out / "score.json", res)
    print(json.dumps(res, ensure_ascii=False, indent=2))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fm(text, *keys):
    for k in keys:
        m = re.search(rf"^{k}:\s*(.+?)\s*(#.*)?$", text, re.M)
        if m:
            return m.group(1).strip()
    return None


def cmd_rescore(a):
    out = Path(a.folder)
    data = load_findings(out / "findings.json")
    base = Path(exp(a.vault)) / ".daiwl" if a.vault else out.parent.parent
    before = compute(data)["pms"]
    for f in data["fundamentals"]:
        for folder in ("learnings", "aprendizados"):
            lp = base / folder / f"{slug(f['name'])}.md"
            if f["class"] == "gap" and lp.exists():
                raw = fm(lp.read_text(encoding="utf-8"), "confidence", "confianca") or "low"
                conf = PT_VALUES.get(raw, raw)
                f.update({"class": "aligned", "level": "learned", "confidence": conf})
    for folder in ("experiences", "experiencias"):
        d = base / folder
        for ex in (d.glob("*.md") if d.exists() else []):
            t = ex.read_text(encoding="utf-8")
            if (fm(t, "status") or "") not in ("adopted", "adotada", "adopted-project", "adotada-projeto"):
                continue
            raw = fm(t, "experience_type", "tipo_experiencia") or "preference"
            etype = PT_VALUES.get(raw, raw)
            contested = (fm(t, "contested", "fundamento_contestado") or "").lower()
            followed = (fm(t, "followed", "fundamento_seguido") or "").lower()
            for f in data["fundamentals"]:
                if contested and f["name"].lower() == contested:
                    f.update({"class": "divergent"})
                if followed and f["name"].lower() == followed:
                    f.update({"class": "aligned", "level": "experience", "experience_type": etype})
    dump(out / "findings.json", data)
    res = compute(data)
    res["delta_rescore"] = round(res["pms"] - before, 1)
    dump(out / "score.json", res)
    print(f"PMS {before} -> {res['pms']} ({res['delta_rescore']:+})")


# ------------------------------------------------------------------ rendering (i18n)
I18N = {
    "en": {"score_title": "Personal Maintainability Score", "abbr": "PMS", "fund_title": "Fundamentals used by the AI",
           "delta": "Change vs previous analysis", "delta_formula": "Previous analysis used another formula version — run rescore before comparing.",
           "class": "Class", "impact": "Impact", "worst": "Largest negative contributions", "gaps": "Gaps that weigh the most",
           "why": "Why the AI used it", "study": "How to study", "deeper": "Where to go deeper", "weight": "weight",
           "generated": "Generated by BKS-DAIWL", "formula": "formula",
           "aligned": "aligned", "gap": "gap", "divergent": "divergent", "unfounded": "unfounded",
           "band_80": "Maintains comfortably", "band_60": "Maintains while studying the gaps",
           "band_40": "Risk: will depend on the AI to maintain", "band_0": "Code is foreign to its owner"},
    "pt-BR": {"score_title": "Score de Manutenibilidade Pessoal", "abbr": "SMP", "fund_title": "Fundamentos usados pela IA",
              "delta": "Variação vs análise anterior", "delta_formula": "A análise anterior usou outra versão da fórmula — rode rescore antes de comparar.",
              "class": "Classe", "impact": "Impacto", "worst": "Maiores contribuições negativas", "gaps": "Lacunas que mais pesam",
              "why": "Por que a IA usou", "study": "Como estudar", "deeper": "Onde aprofundar", "weight": "peso",
              "generated": "Gerado por BKS-DAIWL", "formula": "fórmula",
              "aligned": "alinhado", "gap": "lacuna", "divergent": "divergente", "unfounded": "sem fundamento",
              "band_80": "Mantém com tranquilidade", "band_60": "Mantém estudando as lacunas",
              "band_40": "Risco: vai depender da IA para manter", "band_0": "Código estranho ao dono"},
}


def lang_of(a, data):
    l = (getattr(a, "lang", None) or data.get("language") or "en")
    return "pt-BR" if l.lower().startswith("pt") else "en"


def md_score(s, T):
    L = [f"# {T['score_title']} — {s['project']}", "",
         f"**{T['abbr']}: {s['pms']} / 100** — {T[s['band']]}"]
    if s.get("delta_note") == "formula_changed":
        L.append(T["delta_formula"])
    elif s.get("delta_previous") is not None:
        L.append(f"{T['delta']}: {s['delta_previous']:+}")
    L += ["", f"| {T['class']} | {T['impact']} |", "|---|---|"]
    L += [f"| {T.get(k, k)} | {v} |" for k, v in s["impact_by_class"].items()]
    L += ["", f"## {T['worst']}"]
    L += [f"- {n} ({T.get(c, c)}): {v}" for n, c, v, _ in s["worst_contributions"] if v <= 0]
    L += ["", f"## {T['gaps']}"]
    L += [f"- {n} ({T['impact'].lower()} {i})" for n, _, _, i in s["top_gaps"]]
    L += ["", f"*{T['generated']} {s['skill_version']} · {T['formula']} {s['formula_version']}*"]
    return "\n".join(L) + "\n"


def md_fund(d, T):
    L = [f"# {T['fund_title']} — {d.get('project')}", ""]
    for f in sorted(d["fundamentals"], key=lambda x: -impact(x)):
        L += [f"## {f['name']}  `{T.get(f['class'], f['class'])}`",
              f"*{f.get('category', '')} · {T['weight']} {f.get('weight')}*", "", f.get("explanation", ""), ""]
        if f.get("why_ai_used"):
            L += [f"**{T['why']}:** {f['why_ai_used']}", ""]
        for o in (f.get("occurrences") or [])[:3]:
            L += [f"`{o['file']}:{o.get('line', '')}`", "```", o.get("snippet", ""), "```", ""]
        if f.get("study"):
            L += [f"**{T['study']}:**"] + [f"{i}. {e}" for i, e in enumerate(f["study"], 1)] + [""]
        if f.get("source"):
            L += [f"**{T['deeper']}:** {f['source']}", ""]
    return "\n".join(L)


def to_html(md, title, tpl, lang):
    body, in_code = [], False
    for ln in md.splitlines():
        if ln.startswith("```"):
            body.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            body.append(html.escape(ln))
            continue
        e = html.escape(ln)
        e = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e)
        e = re.sub(r"`(.+?)`", r"<code>\1</code>", e)
        e = re.sub(r"\*(.+?)\*", r"<em>\1</em>", e)
        if ln.startswith("## "):
            body.append(f"<h2>{e[3:]}</h2>")
        elif ln.startswith("# "):
            body.append(f"<h1>{e[2:]}</h1>")
        elif ln.startswith("|"):
            if set(ln.replace("|", "").strip()) <= set("-: "):
                continue
            body.append("<table><tr>" + "".join(f"<td>{c.strip()}</td>" for c in e.strip("|").split("|")) + "</tr></table>")
        elif re.match(r"^(- |\d+\. )", ln):
            body.append(f"<p class='li'>{e}</p>")
        elif ln.strip():
            body.append(f"<p>{e}</p>")
    return (tpl.replace("{{LANG}}", lang).replace("{{TITLE}}", html.escape(title))
               .replace("{{BODY}}", "\n".join(body)))


def cmd_render(a):
    out = Path(a.folder)
    tpl = (Path(__file__).parent.parent / "assets" / "report.html").read_text(encoding="utf-8")
    s = json.loads((out / "score.json").read_text(encoding="utf-8"))
    d = load_findings(out / "findings.json")
    lang = lang_of(a, d)
    T = I18N[lang]
    for name, md, title in (("score", md_score(s, T), T["score_title"]),
                            ("fundamentals", md_fund(d, T), T["fund_title"])):
        (out / f"{name}.md").write_text(md, encoding="utf-8")
        (out / f"{name}.html").write_text(to_html(md, title, tpl, lang), encoding="utf-8")
    print(f"Reports ({lang}) -> {out}")


# ------------------------------------------------------------------ configuration and sources
TYPES = {"vault", "notes", "repo", "papers", "links", "url"}
AUTHORSHIPS = {"own", "mixed", "ai"}
IGNORE_DIRS = {".git", ".obsidian", ".trash", "node_modules", "bin", "obj", "dist", "build",
               "target", ".venv", "__pycache__", ".daiwl"}
EXT = {
    "vault": {".md", ".txt", ".canvas"}, "notes": {".md", ".txt"},
    "papers": {".pdf", ".docx", ".epub", ".md", ".txt", ".html"},
    "repo": {".cs", ".csproj", ".sln", ".java", ".kt", ".xml", ".ts", ".tsx", ".js", ".json", ".go", ".mod",
             ".php", ".py", ".sql", ".md", ".yaml", ".yml", ".tf", ".toml"},
}
GLOBAL = Path.home() / ".daiwl" / "config.md"

SCAFFOLD = {
    "en": {
        "Templates/concept.md": "---\ntype: concept\nlevel: declared   # masters | knows | declared\naliases: []\n---\n## What it is (in my words)\n\n## Where I use it\n\n## Sources\n",
        "Templates/experience.md": "---\ntype: daiwl-experience\nstatus: recorded\nscope: global\nexperience_type: contextual\ncontested:\nfollowed:\n---\n## Context\n\n## Decision\n\n## Lived evidence\n\n## Grounding\n\n## Trade-offs\n",
        "References/links.md": "# Links\n<!-- one URL per line; text after ' — ' becomes a note -->\n",
        "00-Inbox/.gitkeep": "", "Concepts/.gitkeep": "", "Projects/.gitkeep": "", "References/Papers/.gitkeep": "",
    },
    "pt-BR": {
        "Templates/conceito.md": "---\ntype: concept\nlevel: declared   # masters | knows | declared\naliases: []\n---\n## O que é (nas minhas palavras)\n\n## Onde uso\n\n## Fontes\n",
        "Templates/experiencia.md": "---\ntype: daiwl-experience\nstatus: recorded\nscope: global\nexperience_type: contextual\ncontested:\nfollowed:\n---\n## Contexto\n\n## Decisão\n\n## Vivência\n\n## Fundamento\n\n## Trade-offs\n",
        "Referencias/links.md": "# Links\n<!-- uma URL por linha; texto depois de ' — ' vira nota -->\n",
        "00-Inbox/.gitkeep": "", "Conceitos/.gitkeep": "", "Projetos/.gitkeep": "", "Referencias/Artigos/.gitkeep": "",
    },
}


def exp(p):
    return str(Path(os.path.expandvars(str(p))).expanduser())


def find_config():
    local = Path.cwd() / ".daiwl" / "config.md"
    if local.exists():
        return local
    if GLOBAL.exists():
        target = fm(GLOBAL.read_text(encoding="utf-8"), "config")
        if target and Path(exp(target)).exists():
            return Path(exp(target))
    if os.environ.get("DAIWL_VAULT"):
        c = Path(exp(os.environ["DAIWL_VAULT"])) / ".daiwl" / "config.md"
        if c.exists():
            return c
    sys.exit("No configuration found / Nenhuma configuração encontrada. Run: daiwl.py init --vault <dir> [--create]")


def read_config(path):
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"^## (Sources|Fontes)\s*$", txt, re.M)
    head, rest = (txt[:m.start()], txt[m.end():]) if m else (txt, "")
    sources = []
    for ln in rest.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 2:
            t = TYPE_ALIASES.get(cells[0], cells[0])
            if t in TYPES:
                cells += [""] * (4 - len(cells))
                sources.append({"type": t, "path": cells[1], "authorship": AUTH_ALIASES.get(cells[2], cells[2]),
                                "ignore": cells[3]})
    return head, sources


def write_config(path, head, sources):
    lines = ["## Sources", "| Type | Path or URL | Authorship | Ignore |", "|---|---|---|---|"]
    lines += [f"| {s['type']} | {s['path']} | {s['authorship']} | {s['ignore']} |" for s in sources]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(head.rstrip() + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def parse_source(s):
    parts = s.split(":")
    t = TYPE_ALIASES.get(parts[0], parts[0])
    last = AUTH_ALIASES.get(parts[-1], parts[-1])
    auth = last if len(parts) > 2 and last in AUTHORSHIPS else ""
    path = ":".join(parts[1:-1] if auth else parts[1:])
    if t not in TYPES:
        sys.exit(f"Invalid type '{parts[0]}'. Use: {', '.join(sorted(TYPES))}")
    if t == "repo" and not auth:
        sys.exit("Repo needs authorship / Repositório precisa de autoria: repo:<path>:own|mixed|ai")
    return {"type": t, "path": path, "authorship": auth, "ignore": ""}


def cmd_init(a):
    lang = "pt-BR" if (a.lang or "en").lower().startswith("pt") else "en"
    vault = Path(exp(a.vault))
    if a.create:
        for rel, content in SCAFFOLD[lang].items():
            f = vault / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            if not f.exists():
                f.write_text(content, encoding="utf-8")
    elif not vault.exists():
        sys.exit(f"{vault} does not exist. Use --create to scaffold a new vault.")
    base = vault / ".daiwl"
    for d in ("learnings", "experiences", "history"):
        (base / d).mkdir(parents=True, exist_ok=True)
    head = (f"---\ntype: daiwl-config\nskill_version: {SKILL_VERSION}\nwrite_to: {base}\n"
            f"created_by_skill: {str(bool(a.create)).lower()}\nlanguage: {lang}\n---\n")
    sources = [{"type": "vault", "path": str(vault), "authorship": "", "ignore": ""}]
    sources += [parse_source(s) for s in (a.source or [])]
    cfg = base / "config.md"
    if cfg.exists():
        _, old = read_config(cfg)
        seen = {s["path"] for s in sources}
        sources += [s for s in old if s["path"] not in seen]
    write_config(cfg, head, sources)
    if not a.local:
        GLOBAL.parent.mkdir(parents=True, exist_ok=True)
        GLOBAL.write_text(f"---\ntype: daiwl-pointer\nconfig: {cfg}\n---\n", encoding="utf-8")
    print(f"{'Vault created, c' if a.create else 'C'}onfig: {cfg}")
    list_sources(sources)


def files_of(s):
    root = Path(exp(s["path"]))
    extra = [x.strip() for x in s.get("ignore", "").split(",") if x.strip()]
    exts = EXT.get(s["type"])
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in IGNORE_DIRS]
        for fn in fns:
            full = Path(dp) / fn
            rel = str(full.relative_to(root))
            if (exts and full.suffix.lower() not in exts) or fn.endswith(".lock"):
                continue
            if any(fnmatch.fnmatch(rel, g) for g in extra):
                continue
            try:
                if full.stat().st_size > 2_000_000 and full.suffix.lower() != ".pdf":
                    continue
            except OSError:
                continue
            out.append(rel)
    return sorted(out)


def status(s):
    if s["type"] == "url" or s["path"].startswith("http"):
        return "url", 1
    p = Path(exp(s["path"]))
    if not p.exists():
        return "NOT FOUND", 0
    return "ok", 1 if p.is_file() else len(files_of(s))


def list_sources(sources):
    for s in sources:
        st, n = status(s)
        auth = f"[{s['authorship']}]" if s["authorship"] else ""
        print(f"  {s['type']:<7} {auth:<8} {s['path']}  -> {st}, {n} file(s)")


def cmd_sources(a):
    cfg = find_config()
    head, sources = read_config(cfg)
    if a.action in ("add", "rm") and not a.value:
        sys.exit(f"sources {a.action} needs a value")
    if a.action == "add":
        new = parse_source(a.value)
        sources = [s for s in sources if s["path"] != new["path"]] + [new]
        write_config(cfg, head, sources)
    elif a.action == "rm":
        sources = [s for s in sources if s["path"] != a.value]
        write_config(cfg, head, sources)
    print(f"Config: {cfg}")
    list_sources(sources)


def cmd_inventory(a):
    cfg = find_config()
    _, sources = read_config(cfg)
    inv = []
    for s in sources:
        item = dict(s)
        p = Path(exp(s["path"]))
        if s["type"] == "url" or s["path"].startswith("http"):
            item["files"] = []
        elif s["type"] == "links" and p.is_file():
            item["urls"] = sorted(set(re.findall(r"https?://[^\s)\]>\"']+",
                                                 p.read_text(encoding="utf-8", errors="ignore"))))
        elif p.is_dir():
            item["files"] = files_of(s)
        elif p.is_file():
            item["files"] = [p.name]
        else:
            item["error"] = "path not found"
        inv.append(item)
    print(json.dumps({"skill_version": SKILL_VERSION, "config": str(cfg), "sources": inv},
                     ensure_ascii=False, indent=2))


def cmd_version(a):
    print(f"bks-daiwl {SKILL_VERSION} (score formula {FORMULA_VERSION})")


# ------------------------------------------------------------------ CLI
ALIASES = {"versao": "version", "fontes": "sources", "inventario": "inventory"}
FLAG_ALIASES = {"--criar": "--create", "--fonte": "--source", "--idioma": "--lang"}


def main():
    argv = [ALIASES.get(x, FLAG_ALIASES.get(x, x)) for x in sys.argv[1:]]
    p = argparse.ArgumentParser(prog="daiwl")
    p.add_argument("--version", action="version", version=f"bks-daiwl {SKILL_VERSION}")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("version")
    s = sp.add_parser("score"); s.add_argument("findings"); s.add_argument("--out", required=True)
    r = sp.add_parser("render"); r.add_argument("folder"); r.add_argument("--lang")
    rs = sp.add_parser("rescore"); rs.add_argument("folder"); rs.add_argument("--vault")
    i = sp.add_parser("init"); i.add_argument("--vault", required=True); i.add_argument("--create", action="store_true")
    i.add_argument("--source", action="append"); i.add_argument("--lang"); i.add_argument("--local", action="store_true")
    so = sp.add_parser("sources"); so.add_argument("action", nargs="?", default="ls", choices=["ls", "add", "rm"])
    so.add_argument("value", nargs="?")
    sp.add_parser("inventory")
    a = p.parse_args(argv)
    {"version": cmd_version, "score": cmd_score, "render": cmd_render, "rescore": cmd_rescore,
     "init": cmd_init, "sources": cmd_sources, "inventory": cmd_inventory}[a.cmd](a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
