# Knowledge sources

The skill reads from many sources and writes to one place (`<vault>/.daiwl/`). Sources live in `config.md`.

## Types

| Type | What | How to read | Evidence |
|---|---|---|---|
| `vault` | Obsidian or Logseq vault | Markdown, frontmatter, `[[links]]`, tags; most-linked notes first | masters (own explanation) / knows (citation) |
| `notes` | Plain md/txt folder | Same as vault, no graph | same |
| `repo` | Source code | README, ADRs, folder structure, manifests (`*.csproj`, `package.json`, `pom.xml`, `go.mod`), domain, tests | depends on **authorship** |
| `papers` | PDF, docx, epub, articles | `pdftotext -layout` or a PDF-reading skill; title, abstract, sections, highlights | knows |
| `links` | File with URLs (md, txt, exported HTML bookmarks) | With web fetch: page title + summary. Without: link text and surrounding note | knows |
| `url` | A single page | Same as links | knows |

Portuguese aliases accepted by the script: `notas`, `repositorio`, `artigos`.

### Repository authorship

| Authorship | Level | Why |
|---|---|---|
| `own` (`propria`) | masters | you wrote and maintain it |
| `mixed` (`mista`) | knows | partly AI or other people; not proof of mastery |
| `ai` | none | records presence only, so the index is not contaminated |

Manifest hints are clues, not proof: `MediatR` → Mediator, `Polly` → Retry/Circuit Breaker,
`Dapper` → explicit SQL without a full ORM. Confirm in code before recording.

## Ignored by default

`.git/ .obsidian/ .trash/ node_modules/ bin/ obj/ dist/ build/ target/ .venv/ __pycache__/ .daiwl/ *.lock`,
binaries and files over 2 MB (except PDFs). Extra patterns per source in the `Ignore` column.

## Vault created by `init --create`

| English | Português |
|---|---|
| `00-Inbox/` | `00-Inbox/` |
| `Concepts/` | `Conceitos/` |
| `Projects/` | `Projetos/` |
| `References/Papers/` | `Referencias/Artigos/` |
| `References/links.md` | `Referencias/links.md` |
| `Templates/concept.md`, `Templates/experience.md` | `Templates/conceito.md`, `Templates/experiencia.md` |

Plus `.daiwl/` (always English inside). Opens straight in Obsidian; otherwise it is just a Markdown folder.
