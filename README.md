# bks-sdd-kit

🇧🇷 [Leia em português](README.pt-BR.md)

Skills, commands and the artifacts they generate are written in Brazilian Portuguese; code and
identifiers are in English.

A Claude Code plugin with the BKS (Backside) kit for **Spec-Driven Development** (SDD). SDD is
the process that takes a product idea all the way to implemented code, by way of the PRD (product
requirements document), plans, feature specifications, test scenarios and executable tasks.

It is not a code framework. It is the working process: skills that drive the cycle, commands that
operate the workbench, and agents with separate roles.

**Why it exists.** The pattern was born from real projects — a banking transaction engine, a
security SDK, product platforms and proofs of concept. It also came from a recurring problem:
the coding agent writes fast, but without a contract, without proof and without memory between
sessions. The kit enforces all three. The spec comes before the code, the guard refuses an
off-pattern write instead of warning about it, and every skill has an eval case that measures
whether it changes the agent's decision.

## Installation

```
/plugin marketplace add fabiobackside-code/bks-sdd-kit
/plugin install bks@bks-sdd-kit
```

## What's in the kit

### Skills

| Skill | What it is for |
|---|---|
| `bks-sdd` | Full SDD cycle: workspace, PRD, projects, macro plan, feature specs, test scenarios, tasks and execution |
| `bks-dotnet-solutions` | Generates .NET solutions with Hexagonal Architecture and the TXC (Transaction Context) pattern |
| `bks-typescript-solutions` | Node.js + TypeScript backends: REST API, LangGraph agent, worker and consumer, also under TXC |
| `bks-go-solutions` | Go solutions: REST API, worker, consumer, CLI and SDK — TXC in the shape Go allows, idiomatic errors instead of `Result[T]` |
| `bks-create-plan-tasks` | Breaks any piece of work into atomic tasks optimized for token consumption |
| `bks-tests` | Test coverage in a .NET solution: a single xUnit project under `src/`, 90%+ line, branch and method coverage, SonarQube compliance |
| `bks-standards` | BKS engineering standards: coding premises, .NET and Go dependencies, calisthenics, comment policy, SEDA (staged event-driven architecture) and TCP |
| `bks-arch` | BKS diagram notation: brand palette, color semantics by node type, line convention — emits Mermaid, archify, C4 (Context, Containers, Components, Code) or TOGAF (The Open Group Architecture Framework) |
| `api-design` | Endpoint contract: HTTP semantics, versioning, errors, pagination, idempotency |
| `frontend-design` | Interfaces with their own identity — component structure, visual hierarchy, consistency |
| `security-audit` | Security review: input, authorization, secrets, sensitive data |
| `debug-assistant` | From symptom to cause: reproduce, capture in a test, isolate the layer |
| `refactor-guide` | Change structure without changing behavior, with a test safety net first |
| `doc-writer` | Docstrings, README and comments — under the kit's comment ceiling |
| `bks-writing` | Writing standard for living documentation in PT-BR: the decision synthesized in the text, opening with the information, short sentences, defined terms, a list of crutch phrases |
| `bks-maintainability-review` | Maintainability assessment per application, a 0–100 score from a mid-level developer's standpoint, and the project's theoretical and technical foundations; criteria per stack, currently .NET and SQL |
| `pr-writer` | PR title and description from the actual diff, not from the conversation's memory |
| `bks-daiwl` | *Don't Accept It Without Learning*: measures how well **you** can maintain the code the AI (artificial intelligence) generated, comparing the fundamentals applied against your vault, and teaches the difference. Pinned copy of its [own repository](https://github.com/fabiobackside-code/bks-daiwl) |

### Commands

| Command | What it does |
|---|---|
| `/bks:brain` | Resumes the session: who you are, where you stopped, next step |
| `/bks:new-project` | Creates a new project with the canonical structure — the single entry point |
| `/bks:note` | Writes a living note in the project's `docs/input/notas/` |
| `/bks:ingest` | Ingests knowledge into the cross-project base in the vault's `knowledge/` |
| `/bks:canonize` | Consolidates research and design into a single canonical context |
| `/bks:prd` | Generates the PRD from the canonical context |
| `/bks:spec` | Bounded-context interview that generates `FEAT` + `TEST` |
| `/bks:arch` | Generates `ARCH-[project].md` (C4 in Mermaid) and the repo README |
| `/bks:loop` | LOOP-4: implements a task under verifiable goals, at most 4 attempts |
| `/bks:review` | Triggers an independent, read-only review |
| `/bks:maintainability` | Inventories `app/`, generates a maintainability assessment per application in `outputs/maintainability/` and the project's foundations in `outputs/references/` |
| `/bks:save` | Routes the session's outcome by the two-places rule |

### Agents

| Agent | Role | Model |
|---|---|---|
| `planner` | Turns scope into `FEAT`/`TEST`/`TASK` — never production code | Opus |
| `builder` | Implements under LOOP-4, within the limits of the approved FEAT (feature specification) | Sonnet |
| `reviewer` | Independent, read-only security review | Opus |
| `scribe` | Records only what has been confirmed with evidence | Haiku |

## Project profiles

A project declares **what it produces**, and the profile determines which phases apply. A
documentation project gets no questions about databases; a library does not go through screen
design.

| Profile | For |
|---|---|
| `docs` | documentation deliverable — scope, architecture, presentation |
| `fullstack` | full phased project |
| `frontend` | design, mocks, components |
| `backend` | API, domain, persistence |
| `component` | library, SDK, package |
| `infra` | IaC, pipeline, observability |
| `data` | ETL (extract, transform, load), modeling, BI (business intelligence) |
| `legacy-docs` | understanding a legacy system without changing it |
| `reengineering` | documenting and rewriting a legacy system |

Four axes cut across the profiles: output format (`md`/`html`), architecture renderer, frontend
target (`web`/`mobile`/`both`) and rigor (`producao`/`poc`).

`/bks:new-project` records the choice in `.bks-profile.json`. Details in
[`profiles/`](profiles/README.md).

## Guards

The kit installs five hooks. The first three **refuse the write** when the rule is violated — the
reason comes back in the block itself, so you can fix it and retry. `writing_guard` does not
refuse: the write goes through, and the findings return to the agent to be fixed in the same pass.

| Guard | When it fires | What it refuses |
|---|---|---|
| `no_dispatcher` | write to `.cs` | `MediatR`, `IMediator`, `ISender`, `IRequestHandler<>`, `AddMediatR` and equivalents — BKS orchestration is explicit, via `PipelineOrchestrator` |
| `comment_budget` | write to `.cs` | a comment block over 5 lines, and severity markers in comments |
| `dod_docs` | write to `.cs` that declares a public type | the write, as long as `README.md` and `ARCHITECTURE.md` have not been touched in the same batch |
| `writing_guard` | after a write to a living-documentation `.md` | nothing — returns to the agent any ADR outside the decision note, sentences over 40 words, undefined acronyms, crutch phrases and emoji in the written passage, and reminds the user to run `/bks:review` |
| `session_memory` | session start | nothing — loads the project's `STATUS.md`, or the user profile at the vault root |

The code guards ignore test files, files outside a git repository and anything that is not `.cs`.
`writing_guard` ignores `STATUS.md`, `JOURNAL.md`, `CLAUDE.md`, ADRs, `CONTEXT*.md`,
`docs/prompts/`, `docs/history/`, `docs/input/` and agent instructions (`skills/`, `commands/`,
`agents/`). It also runs as a command line over whole files:
`python hooks/scripts/writing_guard.py <file.md>`, exiting with 1 when there are findings. An
internal failure in a guard lets the write through: a rule that breaks the flow because of its own
bug stops being used within a week.

Running the guard tests:

```
bash hooks/tests/run.sh
```

The guards require `python` on the `PATH`.

## Verification

Two suites, answering different questions.

**Structural** — is the file still intact after someone touched it? Frontmatter, references that
resolve, documented commands that exist, declared guards that compile. Runs without a model:

```
python tests/test_structure.py
bash hooks/tests/run.sh
```

**Behavioral** — does the skill still decide correctly? Refuses MediatR, keeps the test project in
`src/`, asks before assuming. Runs the real agent, with a baseline arm without the plugin to
measure the delta:

```
claude plugin eval .
```

The cases live in `evals/`. The two complement each other: the structural suite catches the
refactor that broke the file, the eval suite catches the refactor that kept the file valid and
lost the rule.

## Configuration

The workbench commands (`/bks:brain`, `/bks:save`, `/bks:new-project`, `/bks:note`, `/bks:canonize`, `/bks:prd`,
`/bks:review`) operate on a project vault. Point to it with environment variables:

| Variable | Points to | Example |
|---|---|---|
| `BKS_VAULT` | Vault root | `D:/path/to/vault` |
| `BKS_KNOWLEDGE` | Cross-project knowledge base | `${BKS_VAULT}/knowledge` |

That's two. Each project keeps its own memory, decisions and domain — there is no central hub to
point to.

The skills (`bks-sdd`, `bks-dotnet-solutions`, `bks-typescript-solutions`, `bks-go-solutions`,
`bks-create-plan-tasks`, `bks-tests`, `bks-standards`, `bks-arch`, `bks-writing`, `bks-maintainability-review`, `bks-daiwl`, and the support skills)
work without any configuration — they operate on the current working directory.

## The cycle, in one pass

```
/bks:new-project   creates the structure
/bks:note          raw material comes in
/bks:canonize      becomes canonical context
/bks:prd           becomes a PRD
/bks:spec          becomes FEAT + TEST
                   (or the bks-sdd skill, for the cycle with workspace and macro plan)
/bks:loop          implements a task under goals
/bks:review        independent review
/bks:maintainability  per-application assessment and foundations
/bks:arch          consolidates the architecture view
/bks:save          records decisions and progress
```

## `/bks:spec` or the `bks-sdd` skill?

Both specify, at different scales.

**`/bks:spec`** goes straight to FEAT and TEST (test scenarios), inside the repository. It is the default path for a
feature you already understand, in a project that already exists.

**The `bks-sdd` skill** is the full cycle, with PRD, macro plan and task breakdown, keeping state
across sessions in a `workspace-*/`. It pays off when the product is new and large, or when the
scope is uncertain and needs formal decomposition.

| Flag | What for |
|---|---|
| `/bks-sdd` | creates the `workspace-[name]/` |
| `--prd` | generates the PRD from what is in `research/` |
| `--project` / `--project-prd` / `--project-plan` | internal project, its PRD and its phase plan |
| `--feature` / `--feature-tests` / `--feature-task` | FEAT, then TEST, then the tasks |
| `--feature-list` / `--task-list` / `--status` | what exists and where it stopped |
| `--impl-init` / `--task-done` | executes and closes a task |
| `--continue` / `--tan` / `--clear` | resumes, or ends while saving state |
| `--cost` / `--cost-report` | session and cycle consumption |

Steps cannot be skipped: `--feature-tests` only runs with an approved FEAT, `--feature-task` only
with an approved TEST. It is the same rule as `/bks:spec`, applied to a larger cycle.

## Agent architecture

The four agents are not the same worker under different names. Each one has **the tools of its
role, and only those** — the restriction is the design, not a cost saving.

| Agent | Model | Tools | What the restriction prevents |
|---|---|---|---|
| `planner` | Opus | read + write, no `Bash` | executes nothing; scope becomes FEAT, TEST and TASK (executable task), never code |
| `builder` | Sonnet | read + write + `Bash` | implements under LOOP-4, within the limits of an approved FEAT |
| `reviewer` | Opus | **read only** | does not fix what it judges — a finding becomes a report, not a commit |
| `scribe` | Haiku | read + write | records what has been confirmed; does not decide what was done |

Three consequences of this arrangement:

**The review is independent because it cannot act.** A `reviewer` without `Write` has no way to
turn a finding into a silent fix. Whoever reviews does not fix; whoever fixes does not approve
their own fix.

**The model matches the judgment required.** Opus where judgment happens — security in the
`reviewer`, architecture in the `planner`, because a wrong spec contaminates every task below it.
Sonnet where an approved spec is executed. Haiku where evidence is transcribed. Paying for Opus to
record what has already been decided is waste; paying for Haiku to judge risk is recklessness.

**The role is invoked, not assumed.** The `reviewer` runs in a separate invocation from whoever
implemented, without the state of the session that produced the code. An agent that reviews its
own work in the same session carries the assumptions that led it to the defect.

Invoke by name: `bks:reviewer`, `bks:planner`, `bks:builder`, `bks:scribe`. `/bks:review` triggers
the `reviewer` with the right context.

## Kit and vault, together

The kit works on its own — skills, commands and guards read nothing from outside. What the
[vault](https://github.com/fabiobackside-code/bks-2brains) adds is **memory across projects**, and
that is where the bigger gain comes from.

| | Without vault | With vault |
|---|---|---|
| Coding standard | whatever the model remembers from training | `workbench/` says how *you* work |
| Technical decision | starts over in every project | `knowledge/wiki/` keeps what you have already concluded |
| Known mistake | repeats until it hurts again | recorded, with the signal that would have warned you |
| Session context | whatever fits in the prompt | the project's `STATUS.md`, read by `/bks:brain` |

### Why it consumes less

It is not a promise, it is mechanics — and it can be measured in the kit itself:

**Progressive disclosure.** The skills add up to 4,584 lines of entry point and 12,455 in
`references/` — a 2.7× ratio. A reference only enters the context when the task requires it.
`bks-tests` loads 93 lines and keeps 1,847 available.

**State outside the session.** `STATUS.md` and `JOURNAL.md` keep track of where the project
stopped. Resuming costs reading one file, not rebuilding the history at every opening.

**Knowledge on demand.** The vault's collection is consulted when the question calls for it. Fifty
curated pages cost less than five hundred lines of instructions loaded every time.

### Why it hallucinates less

**The answer cites a source that exists.** When the agent consults `knowledge/wiki/`, the claim
has a verifiable origin in `knowledge/raw/`. What it "remembers" from training does not.

**The guards refuse, they don't warn.** A hook that blocks the wrong write does not depend on the
agent having read the rule. A warning is a suggestion; a refusal is a guarantee.

**The spec precedes the code.** FEAT and TEST approved before implementation give verifiable
acceptance criteria. Without that, "done" is an opinion.

What this does **not** solve: if your wiki is wrong, the agent is wrong with confidence and with
a citation. That is why `raw/` is immutable and a curated page has a status — so you can check
where the conclusion came from.

> The kit's 20 eval cases measure whether each skill changes the agent's decision. The baseline
> with the delta between the `with` and `without` arms has not run yet; until then, what is
> written here is mechanism, not a measured number.

## Language

Documentation and generated artifacts in **PT-BR**. Code, type, method and variable names in
**English**.

## Public contract and versioning

The kit follows semantic versioning (SemVer) starting at 1.0.0. The contract below states what a
consuming project can rely on as stable.

**Covered by the contract** — an incompatible change only ships in a major version:

- the names of the `/bks:*` slash commands and their arguments;
- the names of the skills and agents;
- the `.bks-profile.json` schema ([`profiles/bks-profile.schema.json`](profiles/bks-profile.schema.json))
  and the profile names;
- the folder structure of the project skeleton ([`templates/project-skeleton/`](templates/project-skeleton/));
- the names of the guards in `hooks/` and the refusal behavior of each one;
- the commands' output locations, such as `outputs/maintainability/` and `outputs/references/`.

**Outside the contract** — may change in a minor or patch release:

- the internal wording of the skills and of `references/`;
- rubric criteria and weights;
- eval cases;
- template texts.

A minor version brings a new skill, command, profile or stack. A patch version brings fixes and
wording adjustments.

**Known limitation.** The eval baseline, the delta between the `with` and `without` arms, has not
been measured yet.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md); for security
vulnerabilities, [SECURITY.md](SECURITY.md). The version history is in the
[CHANGELOG.md](CHANGELOG.md).

## Credits

What came from third parties, under which license, and what was only inspiration is in
[THIRD_PARTY.md](THIRD_PARTY.md).

## License

MIT — see [LICENSE](LICENSE).
