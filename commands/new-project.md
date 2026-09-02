---
description: Cria um projeto novo com a estrutura canonica e o perfil escolhido. Unico ponto de entrada para comecar um projeto. Roda na raiz do vault.
---

Crie um projeto novo. Rode com a sessao aberta na **raiz do vault** — o diretorio que contem
`repos/`.

Se `BKS_VAULT` estiver definido e o diretorio atual for outro, diga qual voce vai usar antes de
criar qualquer coisa.

## Passo 1 — o que perguntar

Colete, numa unica rodada de perguntas:

1. **Nome** do projeto — vira o diretorio, em kebab-case
2. **Categoria** — as que existem em `repos/`; se o usuario disser uma que nao existe, confirme
   antes de criar a pasta
3. **Perfil** — o que o projeto gera

Apresente os perfis com uma linha cada, para o usuario poder escolher:

| Perfil | Gera |
|---|---|
| `docs` | escopo, arquitetura, apresentacao — sem codigo |
| `fullstack` | projeto completo faseado: docs, design, front, back, banco, infra |
| `frontend` | design, mocks, componentes, integracao |
| `backend` | API, dominio, persistencia, scripts |
| `component` | biblioteca, SDK, pacote |
| `infra` | IaC, pipeline, observabilidade |
| `data` | ETL, modelagem, BI |
| `legacy-docs` | documentar um legado, sem altera-lo |
| `reengineering` | documentar e reescrever um legado |

A lista canonica esta em `${CLAUDE_PLUGIN_ROOT}/profiles/`. Leia o diretorio — nao confie nesta
tabela se ela divergir dos arquivos.

## Passo 2 — os eixos

Leia `${CLAUDE_PLUGIN_ROOT}/profiles/{perfil}.md`. Ele diz quais eixos se aplicam e o que mais
perguntar.

Pergunte apenas os eixos que o perfil usa:

| Eixo | Valores | Padrao |
|---|---|---|
| `output` | `md`, `html` | `md` |
| `architecture_renderer` | ver `profiles/architecture-renderers/` | `mermaid` |
| `frontend_target` | `web`, `mobile`, `both` | `web` — so em `frontend` e `fullstack` |
| `rigor` | `producao`, `poc` | `producao` |

Mais as perguntas especificas que o arquivo do perfil lista em "O que perguntar na criacao".

**Nao pergunte o que o perfil nao usa.** Um projeto `docs` nao ouve pergunta sobre banco de dados,
e um `component` nao ouve pergunta sobre alvo de frontend.

## Passo 3 — confirmar

Mostre o que vai ser criado — caminho, perfil, eixos — e espere. Nao crie nada antes do aceite.

## Passo 4 — criar

Copie `${CLAUDE_PLUGIN_ROOT}/templates/project-skeleton/` para
`{vault}/repos/{categoria}/{nome}/` e preencha:

**`.bks-profile.json`** — conforme
`${CLAUDE_PLUGIN_ROOT}/profiles/bks-profile.schema.json`:

```json
{
  "profile": "backend",
  "category": "backside",
  "axes": {
    "output": "md",
    "architecture_renderer": "mermaid",
    "frontend_target": null,
    "rigor": "producao"
  }
}
```

Acrescente `stack` e `architecture_template` quando a conversa os tiver definido.

**`STATUS.md`** — o estado inicial. Fase: levantamento. Proximo passo: a primeira acao concreta do
perfil escolhido, que costuma ser `/note` ou reunir o material de entrada. Nao escreva "definir o
projeto" — isso nao e acao.

**`WORKFLOW.md`** — a partir das fases do perfil. Remova as secoes de fases que o perfil nao usa.

**`JOURNAL.md`** — uma entrada: a data de hoje, "Projeto criado", perfil e escopo inicial em duas
linhas.

**`README.md`** — do template `PROJECT-README.md`, resolvido nesta ordem:
`${BKS_VAULT}/workbench/templates/`, senao `${CLAUDE_PLUGIN_ROOT}/templates/`.

**`CLAUDE.md`** — do template `REPO-CLAUDE.md`, mesma precedencia. Declare as skills que o perfil
carrega e aponte `brain/domain/` e `brain/engineering/`.

**`git init`** — todo projeto nasce versionado. Primeiro commit com a estrutura.

## Passo 5 — informar

Em ate cinco linhas: onde foi criado, qual perfil, e o primeiro comando a rodar.

Diga que o trabalho acontece com a sessao aberta **na pasta do projeto**, nao aqui. Os comandos de
projeto escrevem onde a sessao esta; rodar da raiz gravaria no lugar errado.

Nao ofereca continuar o trabalho do projeto a partir do vault.

## Regras

**Um projeto por vez.** Se o usuario pedir varios, crie o primeiro e pergunte se segue.

**Nome que ja existe nao e sobrescrito.** Avise e pergunte se e para usar outro nome ou abrir o
que existe.

**Perfil errado custa caro depois.** Se a descricao do usuario nao casar com o perfil que ele
escolheu, diga em uma linha antes de criar. A escolha e dele; o alerta e seu.

Responda em portugues do Brasil.
