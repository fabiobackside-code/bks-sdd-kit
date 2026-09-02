# Perfil `docs`

Entrega documental. Escopo, arquitetura, apresentacao — sem codigo de aplicacao.

## Gera

- documento de escopo
- arquitetura no template escolhido (TOGAF, C4 ou proprio)
- apresentacao, quando pedida
- ADRs das decisoes tomadas no caminho

## Nao gera

Codigo, banco de dados, infraestrutura. Se a conversa derivar para implementacao, registre como
questao aberta e siga — mudar de perfil e decisao do usuario, nao do agente.

## Fases

| Fase | Produz |
|---|---|
| entrada | `docs/input/` — notas, entrevistas, pesquisa |
| consolidacao | `docs/canonical/CONTEXT.md` |
| escopo | `outputs/ESCOPO-{projeto}.md` |
| arquitetura | `outputs/ARCH-{projeto}.md` no template escolhido |
| apresentacao | `outputs/APRESENTACAO-{projeto}.{md,html}` — se pedida |
| fechamento | `STATUS.md`, `JOURNAL.md` |

Sem `/spec`, sem `/loop`. Nao ha FEAT nem TASK: o artefato e o documento.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | nao | — |
| `rigor` | nao | — |

## Skills

`bks-sdd` (fases de entrada, consolidacao e produto) · `bks-arch` · `doc-writer`

## O que perguntar na criacao

1. Qual o template de arquitetura — TOGAF, C4 ou proprio?
2. A entrega inclui apresentacao?
3. Saida em markdown ou HTML para PDF?
