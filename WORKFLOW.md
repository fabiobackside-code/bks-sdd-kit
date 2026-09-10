# WORKFLOW — prj-bks-kit

> O fluxo de trabalho deste projeto. Para saber **onde ele está**, leia `STATUS.md`.
>
> Todos os comandos rodam com a sessão aberta na **raiz deste repositório**.

---

## Perfil

**`component`** — biblioteca reusável. O kit é consumido por outros projetos como plugin do Claude
Code; não roda sozinho.

O perfil está em `.bks-profile.json`.

---

## O que este projeto tem de particular

Um projeto `component` comum atravessa entrada → consolidação → contrato → specs →
implementação. Este não: nasceu extraído de um vault em uso, com o conteúdo já escrito e
validado em produção. As fases iniciais não se aplicam — não há escopo a levantar, há um artefato
em uso a manter.

O ciclo real é outro: **mudar → provar → medir**.

---

## Ciclo

### 1 · Mudar

Skill, comando, agente, hook ou template. A mudança vive no diretório da sua natureza:

| O que | Onde |
|---|---|
| Skill | `skills/<nome>/SKILL.md` + `references/` |
| Slash command | `commands/<nome>.md` |
| Subagente | `agents/<nome>.md` |
| Guarda executável | `hooks/` |
| Perfil de projeto | `profiles/<perfil>.md` |
| Esqueleto de projeto novo | `templates/project-skeleton/` |

### 2 · Provar

Duas redes, que respondem perguntas diferentes.

**`python tests/test_structure.py`** — o arquivo continua íntegro depois que mexi nele:
frontmatter válido, referência citada que existe, comando documentado que está no repositório,
schema dos casos de eval. Roda em segundos, sem custo.

**`claude plugin eval .`** — a skill ainda decide certo. Roda o agente de verdade contra os 18
casos em `evals/`, com braço `without` para medir o delta que o plugin causa. Custa crédito.

Guarda que muda comportamento precisa de teste em `hooks/tests/` — guarda sem teste é intenção.

### 3 · Medir

O número que importa é o **delta** entre o braço `with` e o `without`. Score alto sem delta
significa que o modelo já acertava sozinho, e a skill não está pagando o próprio contexto.

```
claude plugin eval . --output-dir evals/results
```

### 4 · Fechar

`/save` — roteia o resultado da sessão:

| O que | Para onde |
|---|---|
| Decisão de arquitetura ou contrato | `decisions/ADR-NNN.md` |
| Onde o projeto parou | `STATUS.md` — reescrito |
| Marco da sessão | `JOURNAL.md` — acrescentado no topo |
| Padrão técnico que se firmou | `brain/engineering/` |

---

## Instalação e consumo

O kit está registrado como marketplace de diretório apontando para este repositório
(`~/.claude/settings.json`, `extraKnownMarketplaces`). O que executa, porém, é a cópia em
`~/.claude/plugins/cache/bks-sdd-kit/bks-sdd-kit/<versão>/` — `${CLAUDE_PLUGIN_ROOT}` aponta para
lá, não para cá.

Consequência prática: **editar aqui não muda o que roda**. É preciso reinstalar ou atualizar o
plugin para a mudança valer. E mover este repositório exige reapontar o caminho nos dois registros
(`settings.json` e `plugins/known_marketplaces.json`).

---

## Onde o conhecimento vive

| Pasta | O que entra |
|---|---|
| `brain/domain/` | o que o kit **é** — o método SDD, o que cada perfil significa |
| `brain/engineering/` | como se constrói **aqui** — padrão de skill, de guarda, de eval |
| `docs/ARCHITECTURE.md` | as decisões estruturais, com o porquê |

---

## Retomando

Abra a sessão na raiz deste repositório e rode `/brain`. Ele lê o `STATUS.md` e diz onde você
parou, o que trava e qual o próximo passo.
