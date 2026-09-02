# Perfil `fullstack`

Projeto completo, faseado. Documentacao, design, front, back, banco, infraestrutura e componentes
— tudo com testes.

## Gera

Tudo o que os perfis `frontend`, `backend`, `infra` e `component` geram, sob um plano unico e
faseado.

## Nao gera

Nada fica de fora. O que muda e a ordem: este perfil existe para faseamento, nao para ampliacao de
escopo. Fase que nao esta no plano nao entra sozinha.

## Fases

| Fase | Produz |
|---|---|
| entrada | `docs/input/` |
| consolidacao | `docs/canonical/CONTEXT.md` |
| produto | `outputs/PRD-{projeto}.md` |
| plano macro | `outputs/PLAN-{projeto}.md` — o faseamento |
| arquitetura | `outputs/ARCH-{projeto}.md` |
| modelagem | dominio, dados, DDL |
| design | telas, fluxos, sistema visual |
| especificacao | `specs/features/`, `specs/tests/`, `specs/tasks/` — por fase |
| implementacao | `app/` — backend, frontend, componentes |
| infraestrutura | IaC, pipeline, observabilidade |
| revisao | independente, por fase |
| fechamento | `STATUS.md`, `JOURNAL.md` |

O plano macro e obrigatorio aqui. Sem ele, um projeto deste tamanho vira lista de tarefas sem
ordem, e a primeira fase nunca fecha.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | **sim** | `web` |
| `rigor` | sim | `producao` |

## Skills

Todas. `bks-sdd` conduz; as demais entram conforme a fase.

## O que perguntar na criacao

1. Web, mobile, ou ambos?
2. Qual a stack de backend, e qual a de frontend?
3. Qual o banco? Ha mensageria?
4. Onde roda — nuvem, on-premise, container?
5. Ha prazo ou marco que force o faseamento?
