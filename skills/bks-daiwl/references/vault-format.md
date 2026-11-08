# Vault format

Everything the skill writes lives in `<vault>/.daiwl/`, Markdown with frontmatter, readable in Obsidian,
git-friendly. Keys and folder names are English; note bodies are in the user's language.

```
.daiwl/
├── config.md
├── index.md
├── learnings/<slug>.md
├── experiences/<slug>.md
└── history/<YYYY-MM-DD>-<project>/
    ├── findings.json
    ├── score.json  score.md  score.html
    └── fundamentals.md  fundamentals.html
```

## config.md

`~/.daiwl/config.md` is a pointer to the default config; a `.daiwl/config.md` at a repo root overrides it.

```markdown
---
type: daiwl-config
skill_version: 1.0.0
write_to: ~/Obsidian/Dev/.daiwl
created_by_skill: false
language: pt-BR
---
## Sources
| Type | Path or URL | Authorship | Ignore |
|---|---|---|---|
| vault | ~/Obsidian/Dev | | Journal/** |
| repo | ~/src/wallet-apis | own | |
| repo | ~/src/copilot-poc | ai | |
| papers | ~/Documents/papers | | |
| links | ~/Obsidian/Dev/References/links.md | | |
```

## index.md

```markdown
---
type: daiwl-index
updated: 2026-11-07
total: 42
---
## Concepts
| Concept | Aliases | Category | Level | Evidence | Source |
|---|---|---|---|---|---|
| Hexagonal Architecture | Ports & Adapters, Arquitetura Hexagonal | Architecture | masters | [[templates/api-hexagonal]] | catalog |

## Anti-preferences
| Avoid | Reason | Origin |
|---|---|---|
| AutoMapper | implicit mapping hides errors | [[notes/explicit-mapping]] |
```

## learnings/<slug>.md

```markdown
---
type: daiwl-learning
concept: Outbox Pattern
date: 2026-11-07
origin_project: payments-api
confidence: high
---
## What I understood
## Where I saw it applied
## Sources studied
```

## experiences/<slug>.md (lightweight ADR)

```markdown
---
type: daiwl-experience
status: adopted            # adopted | adopted-project | recorded
scope: global              # global | <project>
experience_type: contextual   # grounded | contextual | preference
contested: Generic Repository  # what the AI did (becomes divergent)
followed: Repository per Aggregate  # what the user adopts (becomes aligned)
date: 2026-11-07
---
## Context
## Decision
## Lived evidence
## Grounding
## Trade-offs
```

Section headings may be written in the user's language; only frontmatter keys are fixed.
