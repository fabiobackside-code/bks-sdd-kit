# {{PROJETO}} (categoria: {{backside | w3 | private}})

> **Esqueleto de exemplo.** Esta pasta mostra a estrutura canonica de um projeto real, mas esta
> vazia de proposito — sem escopo, sem stack, sem specs preenchidas. Use `/new-project` na raiz do
> vault para gerar a sua versao com conteudo real.

## O projeto e autossuficiente

Tudo que uma sessao precisa esta neste repositorio. Nenhum comando le o vault para funcionar.

## Boot da sessao — carregar nesta ordem

| # | Arquivo | Para que |
|---|---|---|
| 1 | `./STATUS.md` | onde o projeto parou, o que trava, proximo passo |
| 2 | `./WORKFLOW.md` | o fluxo de comandos deste projeto |
| 3 | `./brain/engineering/` | como se constroi aqui — padrao tecnico local |
| 4 | `./brain/domain/` | o que o produto e — regra de negocio, metodo, normativo |

Skill em `brain/engineering/` sobrescreve a equivalente do kit para este projeto.

O perfil do usuario vive no vault (`workbench/profile.md`) e e carregado pelo ambiente, nao por
este arquivo.

## Onde cada coisa esta

| O que | Onde |
|---|---|
| Specs — fonte de verdade para implementar | `./specs/{features,tests,tasks}/` |
| Decisoes deste projeto | `./decisions/ADR-NNN.md` |
| Contexto consolidado (apos `/canonize`) | `./docs/canonical/` |
| Material bruto ainda nao consolidado | `./docs/input/` |
| Entregaveis gerados | `./outputs/` |
| Codigo | `./app/` |

## Idioma

Documentacao e artefatos em portugues do Brasil. Codigo, nomes de tipo, metodo e variavel em
ingles.
