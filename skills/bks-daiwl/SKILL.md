---
name: bks-daiwl
description: "BKS-DAIWL (Don't Accept It Without Learning). Scores how well AI-generated code (Claude Code, Copilot, Cursor, MCP agents) matches how the developer works — vault, notes, own repos, papers, links — and explains every fundamental the AI used with snippets from the generated code and study paths. Records what the user learned and experiences that challenge the AI, so the score improves. Bilingual (English/Portuguese). Use ALWAYS when the user wants to compare AI-generated or vibecoded code with their own way of programming, check if they can maintain AI-written code, find which patterns the AI applied, index their vault, mark concepts as learned, or record a decision against the AI. Also trigger on bks-daiwl, daiwl, não aceitar sem aprender, score de aderência, manutenibilidade do código da IA, fundamentos usados pela IA, comparar código gerado com meu vault, aprendi."
metadata:
  version: "1.0.0"
  author: "Fabio (BKS)"
  languages: "en, pt-BR"
---

# BKS-DAIWL — Don't Accept It Without Learning

**Version 1.0.0** · see `CHANGELOG.md`.

Principle: **never accept code without understanding the fundamentals it relies on.**
The score does not say whether the code is "good". It says how well *this person* can maintain
*this code*, given what they master, have learned, or decided from experience.

## Language

Detect the user's language from the conversation (or `language` in `config.md`: `en` | `pt-BR`).
Speak, write reports, vault notes and study material in that language. Internal keys, folder names
inside `.daiwl/` and JSON fields are always English, so vaults and reports are portable between users.
Pass `--lang` to the script when rendering.

## Commands (both languages accepted)

| English | Português | What it does | Writes |
|---|---|---|---|
| `daiwl init` | `daiwl init` | First run: create a new vault or register existing knowledge sources | `config.md` |
| `daiwl sources [ls\|add\|rm]` | `daiwl fontes` | Manage sources: vault, notes, repositories, papers, links | `config.md` |
| `daiwl index` | `daiwl indexar` | Build/refresh the Canon Index from all sources | `.daiwl/index.md` |
| `daiwl analyze <code>` | `daiwl analisar` | Compare AI code against the index; score + fundamentals report | `.daiwl/history/` |
| `daiwl learned <concept...>` | `daiwl aprendi` | Mark concepts from the last report as learned | `.daiwl/learnings/` |
| `daiwl experience "<note>"` | `daiwl experiencia` | Record an experience that challenges the AI; ground it; negotiate | `.daiwl/experiences/` |
| `daiwl version` | `daiwl versao` | Show skill version and the score formula version | — |

Map natural language ("compare this with my vault", "aprendi CQRS e Outbox",
"I disagree with the generic repository because...") to the right command.

Configuration lookup: `.daiwl/config.md` in the current repo (overrides) → `~/.daiwl/config.md` (global pointer)
→ `DAIWL_VAULT` env var. **If none exists, run `init` before anything else.** Never invent paths.

---

## 0. `init`

Ask one question: *"Do you already keep your knowledge somewhere (vault, notes folder, repositories, papers)?"*

**A. Yes.** Collect paths and classify each source (see `references/sources.md`):
`vault` · `notes` · `repo` · `papers` (PDF/docx/epub) · `links` (file with URLs or exported bookmarks) · `url`.
For each `repo` ask its **authorship**: `own`, `mixed` (AI or other people involved) or `ai`.
AI-written code in the user's repo does not prove the user masters what is in it.
Default write location: `<first vault>/.daiwl/`, else `~/.daiwl/`.
The skill **only reads** sources — it never modifies repositories, papers or existing notes.

**B. No.** Offer to create an Obsidian-compatible vault (default `~/DAIWL-Vault`, folder names in the user's language):
```bash
python scripts/daiwl.py init --vault ~/DAIWL-Vault --create --lang <en|pt-BR>
```
Then a **short interview** (max 6 questions, one at a time): languages and stack; architectural style;
patterns always used; patterns avoided and why; reference books/authors; 1–3 repositories that represent
how they code. Turn answers into concept notes with level `declared` and register the repos as sources.
Explain that `declared` is worth less than real evidence and rises with `learned`, `experience` or own notes.

Finish with `python scripts/daiwl.py sources ls` and offer to run `index`.

---

## 1. `index` — build the Canon Index

1. `python scripts/daiwl.py inventory > inventory.json` lists files from **all** sources, by type, already filtered.
   Read each type as `references/sources.md` says. For large sources sample by relevance (READMEs, ADRs,
   domain code, most-linked notes) and say what was left out.
   **Never index the code that is going to be analyzed** — that would compare the AI with itself.
2. For each concept record: canonical name, aliases, category, **evidence** (file + short excerpt) and **level**:
   - `masters` — used in `own` code/templates, or the user wrote their own explanation
   - `knows` — cited, linked, reading note, saved paper, or present in a `mixed` repo
   - `declared` — stated in the `init` interview, no evidence yet
   - `learned` — from `learned`; `experience` — from an adopted `experience`
   (an `ai` repo gives no level; it only records presence)
3. Normalize names with `references/fundamentals-catalog.md` (it lists English and Portuguese aliases).
   Concepts missing from the catalog are kept with `source: user`.
4. Record explicit **anti-preferences** ("I don't use AutoMapper"). They count as divergence in analysis.
5. Write `.daiwl/index.md` (`references/vault-format.md`). Merge with any existing index: never lower a level,
   never drop `learned`/`experience`.

Show totals per category and the 5 most obvious evidence gaps. Ask whether the index is faithful.

---

## 2. `analyze`

1. Make sure an index exists.
2. Read the target code. In big projects prioritize entry points, domain, integration layers, tests.
3. **Extract applied fundamentals.** For each: canonical name, category; **occurrences** (`file:line` + up to ~15
   lines that *exemplify* it); **weight** (`references/score.md`); **grounded?** — is there a recognized reference
   (catalog, book, RFC, official docs)? If not, class `unfounded` (AI improvisation — an alarm, not a user gap).
4. Classify against the index: `aligned` · `gap` (valid fundamental the user lacks) ·
   `divergent` (contradicts an anti-preference or adopted experience) · `unfounded`.
5. Write `findings.json` (schema in `references/score.md`) and run:
   ```bash
   python scripts/daiwl.py score findings.json --out <write_to>/history/<date>-<project>
   python scripts/daiwl.py render <write_to>/history/<date>-<project> --lang <en|pt-BR>
   ```
   The LLM classifies; the script scores, deterministically. Without Python, follow `references/score.md`
   by hand and show the math.
6. Outputs (MD + HTML each): `score` (score, class distribution, top divergences and gaps, delta) and
   `fundamentals` (per fundamental: what it is, **where it is in the code**, why the AI likely chose it,
   how to study it, where to go deeper — primary source first).
7. Summarize in chat: score, the 3 decisions the user must make, and the available commands.

Honesty rules: examples always come from **the analyzed code** (no snippet → the fundamental is dropped);
never inflate the score; `unfounded` is the AI's problem, not the user's.

---

## 3. `learned`

1. Read the latest report in `history/`; confirm each concept is in it.
2. Ask **one short check question** per concept. Vague answer → record anyway with `confidence: low`
   and suggest study material. The user decides; the skill does not block.
3. Write `learnings/<slug>.md` and update `index.md` (level `learned`).
4. `python scripts/daiwl.py rescore <history-folder>` + `render`, show the new score.

---

## 4. `experience`

1. Understand the note: which AI decision is challenged, the alternative, the lived evidence.
2. **Ground it**: catalog first, then primary sources if web search exists. Classify `grounded` (recognized
   fundamental, cite it) · `contextual` (no canonical source, but evidence: incident, regulation, metric) ·
   `preference` (taste, no evidence).
3. **Negotiate.** In 3–5 lines: gains, losses, when the AI's choice would be better. Ask: adopt as a rule,
   adopt for this project only, or just record.
4. Write `experiences/<slug>.md` (lightweight ADR) with `contested` and `followed` (canonical names) in frontmatter.
5. Adopted: code that contradicts it becomes `divergent`, code that follows it becomes `aligned`.
   `rescore` + `render`, show the impact. An adopted `preference` weighs half — tell the user.

---

## Versioning

The skill follows SemVer. Every `score.json` stores `skill_version` and `formula_version`.
When comparing with an older analysis whose `formula_version` differs, say so and do not present the delta
as progress — run `rescore` on the old findings first. Changes to weights or factors bump `formula_version`.

## References (read when needed)

- `references/score.md` — formula, weights, `findings.json` schema. **Read before any `analyze`.**
- `references/fundamentals-catalog.md` — fundamentals, EN/PT aliases, primary sources.
- `references/sources.md` — source types, how to read each, the vault created by `init`.
- `references/vault-format.md` — files written in the vault and `config.md`.
