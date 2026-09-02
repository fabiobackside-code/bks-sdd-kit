# bks-sdd-kit

Plugin do Claude Code com o kit BKS de **Spec-Driven Development** — o processo que leva uma ideia
de produto ate codigo implementado, passando por PRD, planos, especificacoes de feature, cenarios
de teste e tasks executaveis.

Nao e um framework de codigo. E o processo de trabalho: skills que conduzem o ciclo, comandos que
operam o workbench e agentes com papeis separados.

## Instalacao

```
/plugin marketplace add fabiobackside-code/bks-sdd-kit
/plugin install bks-sdd-kit@bks-sdd-kit
```

## O que vem no kit

### Skills

| Skill | Para que serve |
|---|---|
| `bks-sdd` | Ciclo SDD completo: workspace, PRD, projetos, plano macro, feature specs, cenarios de teste, tasks e execucao |
| `bks-dotnet-solutions` | Geracao de solucoes .NET com Arquitetura Hexagonal e o padrao TXC (Transaction Context) |
| `bks-typescript-solutions` | Backends Node.js + TypeScript: API REST, agente LangGraph, worker e consumer, tambem sob TXC |
| `bks-create-plan-tasks` | Decomposicao de qualquer trabalho em tasks atomicas otimizadas para consumo de tokens |
| `bks-tests` | Cobertura de testes em solution .NET: projeto xUnit unico em `src/`, 90%+ em linhas, branches e metodos, conformidade SonarQube |
| `bks-standards` | Padroes de engenharia BKS: premissas de codificacao, dependencias .NET, calisthenics, politica de comentario, SEDA e TCP |
| `bks-arch` | Notacao BKS de diagramas: paleta da marca, semantica de cor por tipo de no, convencao de linha — emite para Mermaid, archify, C4 ou TOGAF |
| `api-design` | Contrato de endpoint: semantica HTTP, versionamento, erro, paginacao, idempotencia |
| `frontend-design` | Interface com identidade propria — estrutura de componente, hierarquia visual, consistencia |
| `security-audit` | Revisao de seguranca: entrada, autorizacao, segredo, dado sensivel |
| `debug-assistant` | Do sintoma a causa: reproduzir, capturar em teste, isolar a camada |
| `refactor-guide` | Mudar estrutura sem mudar comportamento, com rede de teste antes |
| `doc-writer` | Docstring, README e comentario — sob o teto de comentario do kit |
| `pr-writer` | Titulo e descricao de PR a partir do diff real, nao da memoria da conversa |

### Comandos

| Comando | O que faz |
|---|---|
| `/brain` | Retoma a sessao: quem voce e, onde parou, proximo passo |
| `/new-project` | Cria projeto novo com a estrutura canonica — unico ponto de entrada |
| `/note` | Escreve nota viva em `docs/input/notas/` do projeto |
| `/canonize` | Consolida pesquisa e design num contexto canonico unico |
| `/prd` | Gera o PRD a partir do contexto canonico |
| `/spec` | Entrevista de bounded context e gera `FEAT` + `TEST` |
| `/arch` | Gera `ARCH-[projeto].md` (C4 em Mermaid) e o README do repo |
| `/loop` | LOOP-4: implementa task sob goals verificaveis, maximo 4 tentativas |
| `/review` | Dispara revisao independente read-only |
| `/save` | Roteia o resultado da sessao pela regra dos dois lugares |

### Agentes

| Agente | Papel | Modelo |
|---|---|---|
| `planner` | Escopo vira `FEAT`/`TEST`/`TASK` — nunca codigo de producao | Sonnet |
| `builder` | Implementa sob LOOP-4, dentro dos limites da FEAT aprovada | Sonnet |
| `reviewer` | Revisao de seguranca independente, read-only | Opus |
| `scribe` | Registra apenas o que foi confirmado com evidencia | Haiku |

## Perfis de projeto

Um projeto declara **o que gera**, e o perfil determina quais fases se aplicam. Um projeto de
documentacao nao recebe pergunta sobre banco de dados; uma biblioteca nao passa por design de tela.

| Perfil | Para |
|---|---|
| `docs` | entrega documental — escopo, arquitetura, apresentacao |
| `fullstack` | projeto completo faseado |
| `frontend` | design, mocks, componentes |
| `backend` | API, dominio, persistencia |
| `component` | biblioteca, SDK, pacote |
| `infra` | IaC, pipeline, observabilidade |
| `data` | ETL, modelagem, BI |
| `legacy-docs` | entender um legado sem altera-lo |
| `reengineering` | documentar e reescrever um legado |

Quatro eixos atravessam os perfis: formato de saida (`md`/`html`), renderer de arquitetura,
alvo de frontend (`web`/`mobile`/`both`) e rigor (`producao`/`poc`).

O `/new-project` grava a escolha em `.bks-profile.json`. Detalhes em
[`profiles/`](profiles/README.md).

## Guardas

O kit instala quatro hooks. Os tres primeiros **recusam a escrita** quando a regra e violada — a
razao volta no proprio bloqueio, para corrigir e repetir.

| Guarda | Quando dispara | O que recusa |
|---|---|---|
| `no_dispatcher` | escrita em `.cs` | `MediatR`, `IMediator`, `ISender`, `IRequestHandler<>`, `AddMediatR` e equivalentes — a orquestracao BKS e explicita, via `PipelineOrchestrator` |
| `comment_budget` | escrita em `.cs` | bloco de comentario acima de 5 linhas, e marca de severidade em comentario |
| `dod_docs` | escrita em `.cs` que declara tipo publico | a escrita, enquanto `README.md` e `ARCHITECTURE.md` nao tiverem sido tocados na mesma leva |
| `session_memory` | inicio de sessao | nada — carrega o `STATUS.md` do projeto, ou o perfil do usuario na raiz do vault |

Os guardas ignoram arquivo de teste, arquivo fora de repositorio git e qualquer coisa que nao
seja `.cs`. Falha interna de um guarda libera a escrita: regra que quebra o fluxo por bug proprio
deixa de ser usada em uma semana.

Rodar os testes dos guardas:

```
bash hooks/tests/run.sh
```

Os guardas exigem `python` no PATH.

## Verificacao

Duas suites, que respondem a perguntas diferentes.

**Estrutural** — o arquivo continua integro depois que mexeram nele? Frontmatter, referencia que
resolve, comando documentado que existe, guarda declarado que compila. Roda sem modelo:

```
python tests/test_structure.py
bash hooks/tests/run.sh
```

**Comportamental** — a skill ainda decide certo? Recusa MediatR, mantem o projeto de testes em
`src/`, pergunta antes de assumir. Roda o agente de verdade, com braco baseline sem o plugin para
medir o delta:

```
claude plugin eval .
```

Os casos estao em `evals/`. As duas se complementam: a estrutural pega o refactor que quebrou o
arquivo, a de eval pega o refactor que manteve o arquivo valido e perdeu a regra.

## Configuracao

Os comandos de workbench (`/brain`, `/save`, `/new-project`, `/note`, `/canonize`, `/prd`,
`/review`) operam sobre um vault de projetos. Aponte-o por variavel de ambiente:

| Variavel | Aponta para | Exemplo |
|---|---|---|
| `BKS_VAULT` | Raiz do vault | `X:/2brains` |
| `BKS_KNOWLEDGE` | Base de conhecimento transversal | `${BKS_VAULT}/knowledge` |

Sao duas. Cada projeto guarda sua propria memoria, decisao e dominio — nao ha hub central a
apontar.

As skills (`bks-sdd`, `bks-dotnet-solutions`, `bks-typescript-solutions`,
`bks-create-plan-tasks`, `bks-tests`, `bks-standards`, `bks-arch`, e as sete importadas)
funcionam sem nenhuma configuracao — operam sobre o diretorio de
trabalho atual.

## O ciclo, em uma passada

```
/new-project      cria a estrutura
/note             material bruto entra
/canonize         vira contexto canonico
/prd              vira PRD
/spec             vira FEAT + TEST
                  (ou /bks-sdd para o ciclo completo com workspace e plano macro)
/loop             implementa task sob goals
/review           revisao independente
/save             registra decisoes e progresso
/arch             consolida a visao de arquitetura
```

## Idioma

Documentacao e artefatos gerados em **PT-BR**. Codigo, nomes de tipo, metodo e variavel em
**ingles**.

## Licenca

MIT — veja [LICENSE](LICENSE).
