# bks-sdd-kit

Plugin do Claude Code com o kit BKS de **Spec-Driven Development** — o processo que leva uma ideia
de produto até código implementado, passando por PRD, planos, especificações de feature, cenários
de teste e tasks executáveis.

Não e um framework de código. É o processo de trabalho: skills que conduzem o ciclo, comandos que
operam o workbench e agentes com papéis separados.

## Instalação

```
/plugin marketplace add fabiobackside-code/bks-sdd-kit
/plugin install bks@bks-sdd-kit
```

## O que vem no kit

### Skills

| Skill | Para que serve |
|---|---|
| `bks-sdd` | Ciclo SDD completo: workspace, PRD, projetos, plano macro, feature specs, cenários de teste, tasks e execução |
| `bks-dotnet-solutions` | Geração de soluções .NET com Arquitetura Hexagonal e o padrão TXC (Transaction Context) |
| `bks-typescript-solutions` | Backends Node.js + TypeScript: API REST, agente LangGraph, worker e consumer, também sob TXC |
| `bks-go-solutions` | Soluções Go: API REST, worker, consumer, CLI e SDK — TXC na forma que Go admite, erro idiomático no lugar de `Result[T]` |
| `bks-create-plan-tasks` | Decomposição de qualquer trabalho em tasks atomicas otimizadas para consumo de tokens |
| `bks-tests` | Cobertura de testes em solution .NET: projeto xUnit único em `src/`, 90%+ em linhas, branches e métodos, conformidade SonarQube |
| `bks-standards` | Padrões de engenharia BKS: premissas de codificação, dependências .NET e Go, calisthenics, politica de comentario, SEDA e TCP |
| `bks-arch` | Notação BKS de diagramas: paleta da marca, semantica de cor por tipo de no, convenção de linha — emite para Mermaid, archify, C4 ou TOGAF |
| `api-design` | Contrato de endpoint: semantica HTTP, versionamento, erro, paginação, idempotência |
| `frontend-design` | Interface com identidade própria — estrutura de componente, hierarquia visual, consistência |
| `security-audit` | Revisão de segurança: entrada, autorização, segredo, dado sensivel |
| `debug-assistant` | Do sintoma a causa: reproduzir, capturar em teste, isolar a camada |
| `refactor-guide` | Mudar estrutura sem mudar comportamento, com rede de teste antes |
| `doc-writer` | Docstring, README e comentario — sob o teto de comentario do kit |
| `pr-writer` | Titulo e descrição de PR a partir do diff real, não da memória da conversa |

### Comandos

| Comando | O que faz |
|---|---|
| `/bks:brain` | Retoma a sessão: quem você e, onde parou, próximo passo |
| `/bks:new-project` | Cria projeto novo com a estrutura canônica — único ponto de entrada |
| `/bks:note` | Escreve nota viva em `docs/input/notas/` do projeto |
| `/bks:ingest` | Ingere conhecimento para a base transversal em `knowledge/` do vault |
| `/bks:canonize` | Consolida pesquisa e design num contexto canônico único |
| `/bks:prd` | Gera o PRD a partir do contexto canônico |
| `/bks:spec` | Entrevista de bounded context e gera `FEAT` + `TEST` |
| `/bks:arch` | Gera `ARCH-[projeto].md` (C4 em Mermaid) e o README do repo |
| `/bks:loop` | LOOP-4: implementa task sob goals verificáveis, máximo 4 tentativas |
| `/bks:review` | Dispara revisão independente read-only |
| `/bks:save` | Roteia o resultado da sessão pela regra dos dois lugares |

### Agentes

| Agente | Papel | Modelo |
|---|---|---|
| `planner` | Escopo vira `FEAT`/`TEST`/`TASK` — nunca código de produção | Sonnet |
| `builder` | Implementa sob LOOP-4, dentro dos limites da FEAT aprovada | Sonnet |
| `reviewer` | Revisão de segurança independente, read-only | Opus |
| `scribe` | Registra apenas o que foi confirmado com evidência | Haiku |

## Perfis de projeto

Um projeto declara **o que gera**, e o perfil determina quais fases se aplicam. Um projeto de
documentação não recebe pergunta sobre banco de dados; uma biblioteca não passa por design de tela.

| Perfil | Para |
|---|---|
| `docs` | entrega documental — escopo, arquitetura, apresentação |
| `fullstack` | projeto completo faseado |
| `frontend` | design, mocks, componentes |
| `backend` | API, domínio, persistência |
| `component` | biblioteca, SDK, pacote |
| `infra` | IaC, pipeline, observabilidade |
| `data` | ETL, modelagem, BI |
| `legacy-docs` | entender um legado sem altera-lo |
| `reengineering` | documentar e reescrever um legado |

Quatro eixos atravessam os perfis: formato de saída (`md`/`html`), renderer de arquitetura,
alvo de frontend (`web`/`mobile`/`both`) e rigor (`produção`/`poc`).

O `/bks:new-project` grava a escolha em `.bks-profile.json`. Detalhes em
[`profiles/`](profiles/README.md).

## Guardas

O kit instala quatro hooks. Os três primeiros **recusam a escrita** quando a regra e violada — a
razão volta no próprio bloqueio, para corrigir e repetir.

| Guarda | Quando dispara | O que recusa |
|---|---|---|
| `no_dispatcher` | escrita em `.cs` | `MediatR`, `IMediator`, `ISender`, `IRequestHandler<>`, `AddMediatR` e equivalentes — a orquestração BKS e explicita, via `PipelineOrchestrator` |
| `comment_budget` | escrita em `.cs` | bloco de comentario acima de 5 linhas, e marca de severidade em comentario |
| `dod_docs` | escrita em `.cs` que declara tipo público | a escrita, enquanto `README.md` e `ARCHITECTURE.md` não tiverem sido tocados na mesma leva |
| `session_memory` | inicio de sessão | nada — carrega o `STATUS.md` do projeto, ou o perfil do usuário na raiz do vault |

Os guardas ignoram arquivo de teste, arquivo fora de repositório git e qualquer coisa que não
seja `.cs`. Falha interna de um guarda libera a escrita: regra que quebra o fluxo por bug próprio
deixa de ser usada em uma semana.

Rodar os testes dos guardas:

```
bash hooks/tests/run.sh
```

Os guardas exigem `python` no PATH.

## Verificação

Duas suites, que respondem a perguntas diferentes.

**Estrutural** — o arquivo continua integro depois que mexeram nele? Frontmatter, referência que
resolve, comando documentado que existe, guarda declarado que compila. Roda sem modelo:

```
python tests/test_structure.py
bash hooks/tests/run.sh
```

**Comportamental** — a skill ainda decide certo? Recusa MediatR, mantém o projeto de testes em
`src/`, pergunta antes de assumir. Roda o agente de verdade, com braco baseline sem o plugin para
medir o delta:

```
claude plugin eval .
```

Os casos estão em `evals/`. As duas se complementam: a estrutural pega o refactor que quebrou o
arquivo, a de eval pega o refactor que manteve o arquivo valido e perdeu a regra.

## Configuração

Os comandos de workbench (`/bks:brain`, `/bks:save`, `/bks:new-project`, `/bks:note`, `/bks:canonize`, `/bks:prd`,
`/bks:review`) operam sobre um vault de projetos. Aponte-o por variavel de ambiente:

| Variavel | Aponta para | Exemplo |
|---|---|---|
| `BKS_VAULT` | Raiz do vault | `X:/2brains` |
| `BKS_KNOWLEDGE` | Base de conhecimento transversal | `${BKS_VAULT}/knowledge` |

São duas. Cada projeto guarda sua própria memória, decisão e domínio — não há hub central a
apontar.

As skills (`bks-sdd`, `bks-dotnet-solutions`, `bks-typescript-solutions`, `bks-go-solutions`,
`bks-create-plan-tasks`, `bks-tests`, `bks-standards`, `bks-arch`, e as sete importadas)
funcionam sem nenhuma configuração — operam sobre o diretório de
trabalho atual.

## O ciclo, em uma passada

```
/new-project      cria a estrutura
/note             material bruto entra
/canonize         vira contexto canônico
/prd              vira PRD
/spec             vira FEAT + TEST
                  (ou /bks-sdd para o ciclo completo com workspace e plano macro)
/loop             implementa task sob goals
/review           revisão independente
/save             registra decisões e progresso
/arch             consolida a visão de arquitetura
```

## Idioma

Documentação e artefatos gerados em **PT-BR**. Código, nomes de tipo, método e variavel em
**inglês**.

## Licenca

MIT — veja [LICENSE](LICENSE).
