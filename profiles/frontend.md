# Perfil `frontend`

Camada visual. Design, mocks, componentes, integracao com uma API que ja existe.

## Gera

- design de telas e fluxos
- mocks navegaveis
- componentes
- integracao com a API
- testes de componente e de fluxo

## Nao gera

API, dominio, banco. Se a API ainda nao existe, o projeto precisa de `fullstack` ou de um projeto
`backend` ao lado.

## Fases

| Fase | Produz |
|---|---|
| entrada | `docs/input/` |
| consolidacao | `docs/canonical/CONTEXT.md` |
| produto | `outputs/PRD-{projeto}.md` |
| design | telas, fluxos, sistema visual em `docs/design/` |
| mocks | prototipo navegavel em `outputs/mocks/` |
| especificacao | `specs/features/`, `specs/tests/` |
| implementacao | `app/` — componentes e integracao |
| revisao | independente |
| fechamento | `STATUS.md`, `JOURNAL.md` |

O design vem antes do componente. Componente escrito antes do sistema visual vira refactor.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | **sim** | `web` |
| `rigor` | sim | `producao` |

`frontend_target` decide o que se constroi: `web`, `mobile`, ou `both` com design compartilhado.

## Skills

`bks-sdd` · `frontend-design` · `bks-arch` · `bks-tests` · `api-design` (para consumir o contrato)

## O que perguntar na criacao

1. Web, mobile, ou ambos?
2. Qual o framework — React, Vue, React Native, outro?
3. A API ja existe? Onde esta o contrato?
4. Ha sistema de design a seguir, ou vamos criar um?
