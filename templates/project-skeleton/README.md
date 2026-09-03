# {{PROJETO}} — esqueleto de exemplo

Esta pasta existe so para mostrar a **estrutura canonica** de um projeto. Esta vazia de
proposito — sem escopo real, sem stack definida, sem specs preenchidas.

## Estrutura

```
{{projeto}}/
├── STATUS.md              onde parei, o que trava, proximo passo
├── WORKFLOW.md            o fluxo de comandos deste projeto
├── JOURNAL.md             marcos e sessoes, do mais recente ao mais antigo
├── README.md              o que e o projeto
├── CLAUDE.md              contexto que o agente carrega
├── .bks-profile.json      perfil, renderer, eixos
│
├── brain/
│   ├── domain/            o que o produto E — regra de negocio, metodo, normativo
│   └── engineering/       como se constroi AQUI — padrao tecnico, skill local
│
├── docs/
│   ├── input/             material bruto: notas, entrevistas, pesquisa, escopo
│   ├── design/            bancada de trabalho
│   ├── canonical/         contexto consolidado — a fonte apos o /canonize
│   ├── history/           o que foi superado
│   └── prompts/           registro de auditoria do proprio processo
│
├── specs/
│   ├── features/          FEAT-*.md
│   ├── tests/             TEST-*.md
│   └── tasks/             TASK-*.md
│
├── decisions/             ADR-NNN deste projeto
├── outputs/               entregaveis gerados
└── app/                   codigo
```

## Os tres arquivos de estado

| Arquivo | Responde | Escrito por | Reescrito? |
|---|---|---|---|
| `STATUS.md` | onde o projeto esta **agora** | `/save` | sim, por inteiro |
| `JOURNAL.md` | como chegou ate aqui | `/save` | nao, so acrescenta |
| `WORKFLOW.md` | como se trabalha aqui | `/new-project` | so quando o fluxo muda |

`STATUS.md` e o ponto de entrada. O `/brain` le ele.

## Como usar de verdade

Rode `/new-project {{nome}} {{categoria}}` com a sessao aberta na **raiz do vault** para gerar a
sua versao preenchida. Depois traga material para `docs/input/` e siga o ciclo descrito no
`WORKFLOW.md` gerado: `/note` → `/canonize` → `/prd` → `/spec` → `/arch` → `/loop` → `/review` →
`/save`.

Todos os comandos de projeto rodam com a sessao aberta na raiz do repositorio do projeto — nao no
vault.
