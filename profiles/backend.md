# Perfil `backend`

Servidor e dados. API, dominio, persistencia — sem interface.

## Gera

- API e contratos
- dominio, sob arquitetura hexagonal e padrao TXC
- modelo de dados e scripts SQL
- testes unitarios e de integracao
- README e ARCHITECTURE

## Nao gera

Interface, design, mock de tela. Consumidor da API e outro projeto ou outro perfil.

## Fases

| Fase | Produz |
|---|---|
| entrada | `docs/input/` |
| consolidacao | `docs/canonical/CONTEXT.md` |
| produto | `outputs/PRD-{projeto}.md` |
| modelagem | modelo de dominio e de dados; DDL em `app/db/` |
| especificacao | `specs/features/`, `specs/tests/`, `specs/tasks/` |
| arquitetura | `outputs/ARCH-{projeto}.md` |
| implementacao | `app/` — dominio, portas, adapters |
| revisao | independente |
| fechamento | `STATUS.md`, `JOURNAL.md` |

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | nao | — |
| `rigor` | sim | `producao` |

## Skills

`bks-sdd` · `bks-standards` · `bks-dotnet-solutions` ou `bks-typescript-solutions` · `bks-tests`
· `bks-arch` · `api-design` · `security-audit`

## O que perguntar na criacao

1. Qual a stack — .NET, TypeScript, outra?
2. Qual o banco — SQL Server, PostgreSQL, outro?
3. Ha mensageria — Kafka, RabbitMQ, nenhuma?
4. Como se autentica — JWT proprio, provedor externo, nenhuma?
