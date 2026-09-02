# Perfil `data`

Dados e analytics. Pipeline, modelagem, contratos de dados, BI.

## Gera

- pipeline de ingestao e transformacao (ETL ou ELT)
- modelagem analitica
- contratos de dados entre produtor e consumidor
- qualidade: validacao, deteccao de anomalia, linhagem
- painel ou camada semantica de BI
- testes de pipeline e de qualidade

## Nao gera

Aplicacao transacional, interface de usuario. O consumo dos dados e de outro perfil.

## Fases

| Fase | Produz |
|---|---|
| entrada | `docs/input/` — fontes, volumes, frequencia, donos |
| consolidacao | `docs/canonical/CONTEXT.md` |
| inventario de fontes | `outputs/FONTES-{projeto}.md` — o que existe e em que estado |
| modelagem | modelo analitico e contratos de dados |
| arquitetura | `outputs/ARCH-{projeto}.md` — linhagem e fronteiras de dado sensivel |
| especificacao | `specs/features/`, `specs/tests/` |
| implementacao | `app/` — pipeline e transformacoes |
| qualidade | validacao, anomalia, reconciliacao |
| fechamento | `STATUS.md`, `JOURNAL.md` |

O inventario de fontes vem cedo. Pipeline construido sobre fonte que ninguem inspecionou quebra na
primeira carga real.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | nao | — |
| `rigor` | sim | `producao` |

## Skills

`bks-sdd` · `bks-arch` · `bks-standards` · `security-audit` (dado pessoal e regulado)

## O que perguntar na criacao

1. Quais as fontes, e quem e dono de cada uma?
2. Batch, streaming, ou os dois?
3. Onde os dados repousam — data lake, warehouse, banco relacional?
4. Ha dado pessoal ou regulado no caminho?
5. Quem consome no fim — painel, API, modelo?
