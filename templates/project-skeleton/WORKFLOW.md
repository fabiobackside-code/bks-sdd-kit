# WORKFLOW — {{PROJETO}}

> O fluxo de comandos deste projeto. Para saber **onde o projeto está**, leia `STATUS.md`.
>
> Todos os comandos rodam com a sessão aberta na **raiz deste repositório**. Não há comando que
> precise do vault: o projeto é autossuficiente.

---

## Perfil

**{{perfil}}** — {{docs · fullstack · frontend · backend · component · infra · data ·
legacy-docs · reengineering}}

O perfil está em `.bks-profile.json` e determina quais fases se aplicam. As fases que o perfil
não usa não aparecem abaixo.

---

## Ciclo

### 1 · Entrada de material

`/note <assunto>` — material bruto vai para `docs/input/notas/`. Nota viva: cresce ao longo dos
dias, com seção `## Estado em AAAA-MM-DD`. Nunca decisão fechada.

Material de terceiros (artigo, entrevista, norma) vai para `docs/input/research/` à mão.

### 2 · Consolidação

`/canonize` — lê `docs/input/` e `docs/design/` e escreve `docs/canonical/CONTEXT.md`. É a fonte
única a partir daqui; o material bruto deixa de ser lido pelos comandos seguintes.

Rode quando as notas pararem de mudar, não antes.

### 3 · Produto

`/prd` — do `CONTEXT.md` sai o PRD. O que o produto é, para quem, e o que conta como pronto.

### 4 · Especificação

`/spec` — entrevista por bounded context e gera `specs/features/FEAT-*.md`. Depois de aprovado,
`specs/tests/TEST-*.md`. Depois de aprovado, `specs/tasks/TASK-*.md`.

Não pule a aprovação entre os três. Spec aprovada sem teste vira código sem critério.

### 5 · Arquitetura

`/arch` — gera `outputs/ARCH-{{projeto}}.md` e atualiza o `README.md`. Diagramas seguem a notação
BKS; o renderer está no `.bks-profile.json`.

### 6 · Implementação

`/loop` — implementa uma task sob LOOP-4: no máximo quatro tentativas contra goals verificáveis
(build limpo, testes verdes, cenários da `TEST` cobertos).

### 7 · Revisão

`/review` — revisão independente, read-only, em invocação separada. Quem escreveu não revisa a
própria segurança.

### 8 · Fechamento

`/save` — roteia o resultado da sessão:

| O que | Para onde |
|---|---|
| Decisão de arquitetura ou stack | `decisions/ADR-NNN.md` |
| Spec nova ou alterada | `specs/` |
| Onde o projeto parou | `STATUS.md` |
| Marco da sessão | `JOURNAL.md` |
| Entregável | `outputs/` |

---

## Onde o conhecimento vive

| Pasta | O que entra |
|---|---|
| `brain/domain/` | o que o produto **é** — regra de negócio, método, normativo |
| `brain/engineering/` | como se constrói **aqui** — padrão técnico, skill local |

Skill em `brain/engineering/` sobrescreve a equivalente do kit para este projeto.

---

## Retomando

Abra a sessão na raiz deste repositório e rode `/brain`. Ele lê o `STATUS.md` e diz onde você
parou, o que trava e qual o próximo passo.
