# WORKFLOW — {{PROJETO}}

> O fluxo de comandos deste projeto. Para saber **onde o projeto esta**, leia `STATUS.md`.
>
> Todos os comandos rodam com a sessao aberta na **raiz deste repositorio**. Nao ha comando que
> precise do vault: o projeto e autossuficiente.

---

## Perfil

**{{perfil}}** — {{docs · fullstack · frontend · backend · component · infra · data ·
legacy-docs · reengineering}}

O perfil esta em `.bks-profile.json` e determina quais fases se aplicam. As fases que o perfil
nao usa nao aparecem abaixo.

---

## Ciclo

### 1 · Entrada de material

`/note <assunto>` — material bruto vai para `docs/input/notas/`. Nota viva: cresce ao longo dos
dias, com secao `## Estado em AAAA-MM-DD`. Nunca decisao fechada.

Material de terceiros (artigo, entrevista, norma) vai para `docs/input/research/` a mao.

### 2 · Consolidacao

`/canonize` — le `docs/input/` e `docs/design/` e escreve `docs/canonical/CONTEXT.md`. E a fonte
unica a partir daqui; o material bruto deixa de ser lido pelos comandos seguintes.

Rode quando as notas pararem de mudar, nao antes.

### 3 · Produto

`/prd` — do `CONTEXT.md` sai o PRD. O que o produto e, para quem, e o que conta como pronto.

### 4 · Especificacao

`/spec` — entrevista por bounded context e gera `specs/features/FEAT-*.md`. Depois de aprovado,
`specs/tests/TEST-*.md`. Depois de aprovado, `specs/tasks/TASK-*.md`.

Nao pule a aprovacao entre os tres. Spec aprovada sem teste vira codigo sem criterio.

### 5 · Arquitetura

`/arch` — gera `outputs/ARCH-{{projeto}}.md` e atualiza o `README.md`. Diagramas seguem a notacao
BKS; o renderer esta no `.bks-profile.json`.

### 6 · Implementacao

`/loop` — implementa uma task sob LOOP-4: no maximo quatro tentativas contra goals verificaveis
(build limpo, testes verdes, cenarios da `TEST` cobertos).

### 7 · Revisao

`/review` — revisao independente, read-only, em invocacao separada. Quem escreveu nao revisa a
propria seguranca.

### 8 · Fechamento

`/save` — roteia o resultado da sessao:

| O que | Para onde |
|---|---|
| Decisao de arquitetura ou stack | `decisions/ADR-NNN.md` |
| Spec nova ou alterada | `specs/` |
| Onde o projeto parou | `STATUS.md` |
| Marco da sessao | `JOURNAL.md` |
| Entregavel | `outputs/` |

---

## Onde o conhecimento vive

| Pasta | O que entra |
|---|---|
| `brain/domain/` | o que o produto **e** — regra de negocio, metodo, normativo |
| `brain/engineering/` | como se constroi **aqui** — padrao tecnico, skill local |

Skill em `brain/engineering/` sobrescreve a equivalente do kit para este projeto.

---

## Retomando

Abra a sessao na raiz deste repositorio e rode `/brain`. Ele le o `STATUS.md` e diz onde voce
parou, o que trava e qual o proximo passo.
