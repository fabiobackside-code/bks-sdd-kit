# Perfil `infra`

Plataforma e entrega. Infraestrutura como codigo, pipeline, observabilidade.

## Gera

- infraestrutura como codigo (Terraform, Bicep, manifests)
- pipeline de build e deploy
- observabilidade: metricas, logs, tracing, alertas
- politica de acesso e segredo
- runbook de operacao
- testes de infraestrutura, onde a ferramenta permitir

## Nao gera

Aplicacao. Este perfil entrega a plataforma onde outra coisa roda.

## Fases

| Fase | Produz |
|---|---|
| entrada | `docs/input/` — requisitos de plataforma, restricoes, custo |
| consolidacao | `docs/canonical/CONTEXT.md` |
| topologia | `outputs/ARCH-{projeto}.md` — ambientes, rede, fronteiras |
| especificacao | `specs/features/`, `specs/tests/` |
| implementacao | `app/` — IaC e pipeline |
| observabilidade | dashboards, alertas, SLO |
| runbook | `outputs/RUNBOOK-{projeto}.md` |
| revisao | independente, com foco em acesso e exposicao |
| fechamento | `STATUS.md`, `JOURNAL.md` |

A topologia vem antes do codigo. IaC escrito sem topologia decidida vira recurso orfao.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | nao | — |
| `rigor` | sim | `producao` |

## Skills

`bks-sdd` · `bks-arch` · `security-audit` · `bks-standards`

## O que perguntar na criacao

1. Onde roda — qual nuvem, ou on-premise?
2. Quais ambientes — desenvolvimento, homologacao, producao?
3. Kubernetes, serverless, maquina virtual?
4. Ha politica de seguranca ou conformidade a atender?
5. Quem opera depois de entregue?
