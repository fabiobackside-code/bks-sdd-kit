# Perfis de projeto

Um projeto declara **o que gera**. O perfil determina quais fases se aplicam, quais artefatos
saem, e quais skills o agente carrega.

Isso existe para que um projeto de documentacao nao receba pergunta sobre banco de dados, e um
projeto de biblioteca nao passe por design de tela.

## Como se declara

O `/new-project` grava `.bks-profile.json` na raiz do projeto:

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

As skills leem esse arquivo. Sem ele, perguntam.

## Os perfis

| Perfil | Para | Nao gera |
|---|---|---|
| [`docs`](docs.md) | entrega documental | codigo |
| [`fullstack`](fullstack.md) | projeto completo faseado | — |
| [`frontend`](frontend.md) | camada visual | backend, banco |
| [`backend`](backend.md) | servidor e dados | interface |
| [`component`](component.md) | biblioteca reusavel | aplicacao |
| [`infra`](infra.md) | plataforma e entrega | aplicacao |
| [`data`](data.md) | dados e analytics | interface |
| [`legacy-docs`](legacy-docs.md) | entender um legado | codigo — nao altera nada |
| [`reengineering`](reengineering.md) | reescrever um legado | — |

`reengineering` consome `legacy-docs` como primeira fase. Quem so quer entender o legado para no
primeiro; quem vai reescrever passa pelos dois.

## Os eixos

Valem para varios perfis e sao escolhidos junto com ele.

### `output` — formato de saida

| Valor | Gera |
|---|---|
| `md` | markdown apenas |
| `html` | HTML navegavel, exportavel para PDF |

### `architecture_renderer` — como o diagrama e desenhado

Registro extensivel em [`architecture-renderers/`](architecture-renderers/). Cada renderer e um
arquivo; adicionar um novo e criar um arquivo, substituir e trocar o conteudo.

| Valor | E |
|---|---|
| `mermaid` | nativo, versionavel em texto — **padrao** |
| `archify` | skill externa, HTML interativo com export |
| `togaf` | template documental TOGAF |
| `c4` | C4 model — Context, Container, Component |

Todos aplicam a notacao BKS: paleta, semantica de cor e convencao de linha definidas em
`skills/bks-arch/`.

### `frontend_target` — o que a interface e

Vale para `frontend` e `fullstack`.

| Valor | Gera |
|---|---|
| `web` | aplicacao web |
| `mobile` | aplicativo movel |
| `both` | os dois, com design compartilhado |

### `rigor` — quanto de disciplina

| Valor | Exige |
|---|---|
| `producao` | testes, documentacao, ADRs — **padrao** |
| `poc` | prototipo descartavel: teste so no caminho critico, documentacao minima |

`rigor: poc` afrouxa a exigencia; nao a elimina. Um POC sem nenhum teste e um POC que ninguem
consegue avaliar.

## Fases

Cada perfil declara sua sequencia. As comuns:

| Fase | O que faz | Comando |
|---|---|---|
| entrada | material bruto entra | `/note` |
| consolidacao | vira contexto canonico | `/canonize` |
| produto | vira PRD | `/prd` |
| especificacao | vira FEAT, TEST, TASK | `/spec` |
| arquitetura | vira ARCH e README | `/arch` |
| implementacao | vira codigo | `/loop` |
| revisao | revisao independente | `/review` |
| fechamento | STATUS e JOURNAL | `/save` |

Um perfil pode pular fases, acrescentar as suas, ou mudar o que uma fase produz. O que cada um faz
esta no seu arquivo.

## Acrescentar um perfil

Crie o arquivo seguindo o formato dos existentes: o que gera, o que nao gera, as fases, os eixos
que se aplicam, as skills que carrega, e o que o `/new-project` deve perguntar.

Nenhuma skill tem a lista de perfis embutida — todas leem este diretorio.
