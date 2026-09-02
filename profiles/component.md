# Perfil `component`

Biblioteca reusavel. SDK, DLL, pacote — codigo consumido por outros projetos, nao executado
sozinho.

## Gera

- contrato publico da biblioteca
- implementacao
- testes — o consumidor depende do contrato, entao o contrato precisa de prova
- empacotamento e versionamento
- README e ARCHITECTURE

## Nao gera

Aplicacao, interface, infraestrutura de execucao. Uma biblioteca nao tem `Program.cs` de producao.

## Fases

| Fase | Produz |
|---|---|
| entrada | `docs/input/` |
| consolidacao | `docs/canonical/CONTEXT.md` |
| contrato | `specs/features/FEAT-*.md` — a API publica antes da implementacao |
| especificacao | `specs/tests/TEST-*.md`, `specs/tasks/TASK-*.md` |
| arquitetura | `outputs/ARCH-{projeto}.md` |
| implementacao | `app/` |
| empacotamento | versionamento, publicacao, changelog |
| revisao | independente |
| fechamento | `STATUS.md`, `JOURNAL.md` |

O contrato vem antes de tudo. Uma biblioteca cujo contrato muda depois de publicada quebra quem a
usa.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | nao | — |
| `rigor` | sim | `producao` |

## Skills

`bks-sdd` · `bks-standards` · `bks-dotnet-solutions` ou `bks-typescript-solutions` · `bks-tests`
· `bks-arch` · `api-design`

## O que perguntar na criacao

1. Qual a stack — .NET, TypeScript, outra?
2. Onde a biblioteca sera publicada — NuGet, npm, registro interno?
3. Ha compatibilidade a manter com uma versao anterior?
