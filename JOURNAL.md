# JOURNAL — prj-bks-kit

> Marcos e sessões, do mais recente para o mais antigo. Acrescentado pelo `/save`; nunca
> reescrito. O `STATUS.md` diz onde o projeto está agora; este arquivo diz como chegou até aqui.

---

## 2026-09-10 · Go entrou como terceira stack de backend

O kit gerava .NET e TypeScript. Go entrou com a skill `bks-go-solutions` — cinco tipos (API com
chi, worker, consumer, CLI, SDK), 224 linhas de entrada contra 856 do .NET e 716 do TypeScript,
já no formato de progressive disclosure que as outras três ainda devem alcançar.

Go é a primeira linguagem do kit que **contradiz** o padrão-base, e isso forçou uma distinção que
estava implícita: premissa é método e vive em `bks-standards`; a skill geradora produz estrutura e
aponta para lá. O delta ficou em dois arquivos novos — `go-standards.md`, com tabela de tradução
.NET → Go e as nove seções onde a tradução literal falha, e `go-review-checklist.md`, que faltava
(o checklist existente é escrito em termos de .NET).

Três fontes externas foram lidas; uma foi descartada por ser trilha de iniciante. Das outras duas
saiu uma contradição real: a prática comum manda campo exportado sem getter, mas no TXC o getter é
o mecanismo de imutabilidade. A exceção é do TXC, não da linguagem, e ficou registrada nos dois
lados para não ser redescoberta.

A skill também lê e alimenta uma base de aprendizado em `${BKS_KNOWLEDGE}/wiki/go/` — a primeira
do kit que escreve fora do projeto. O caso com nomes reais fica em `brain/engineering/` do
projeto; a wiki recebe a lição anonimizada, porque os projetos de origem são de domínio bancário.

Uma das quatro falhas conhecidas do `test_structure.py` caiu no caminho: era acento —
`documentação.md` citado na tabela, `documentacao.md` em disco. Restam três.

O plugin foi para `0.2.0` e o cache atualizado: a `bks-go-solutions` já aparece na sessão. Sem o
bump a skill não chegaria, porque o plugin instalado é cópia congelada por versão.

**Verificado:** `python tests/test_structure.py` → 720 verificações, 3 falhas (as conhecidas).
`ls ~/.claude/plugins/cache/bks-sdd-kit/bks-sdd-kit/0.2.0/skills/` → 15 skills, com
`bks-go-solutions`. A skill **não** foi exercitada numa geração real — é o próximo passo.

Commits: `550fb72` (Go), `607d5e1` (acento), `c7cc7aa` (0.2.0); `2bc217e` no vault.

### Consumo da sessão

| Modelo | Input | Output | Cache write | Cache read | Total | Custo |
|---|---:|---:|---:|---:|---:|---:|
| claude-opus-5 | 216 | 74.219 | 217.696 | 17.159.714 | 17.451.845 | US$ 12,6134 |
| **TOTAL** | **216** | **74.219** | **217.696** | **17.159.714** | **17.451.845** | **US$ 12,6134** |

Acumulado do processo: **31.446.105 tokens — US$ 22,3324** (2 checkpoints, fase `manutencao`).

Estimativa por token contra `~/.claude/scripts/pricing.json`, não a fatura real.

---

## 2026-09-10 · O kit ganhou os artefatos de projeto

Estava em `repos/` sem `STATUS.md`, `WORKFLOW.md`, `JOURNAL.md`, `CLAUDE.md` nem
`.bks-profile.json` — os artefatos que o `/new-project` cria e que o `/brain` e o `/save` leem.
Criados os cinco, perfil `component`, categoria `backside`, rigor `producao`.

O `WORKFLOW.md` não copiou o ciclo do perfil. Um `component` comum vai de entrada a implementação;
este nasceu extraído de um vault em uso, com o conteúdo já validado. O ciclo real é **mudar →
provar → medir**, e é esse que está escrito.

Fecha a lacuna aberta pela mudança de lugar: o kit agora é um projeto igual aos demais em
`repos/`, legível pelos comandos do próprio kit.

---

### Consumo da sessão

| Modelo | Input | Output | Cache write | Cache read | Total | Custo |
|---|---:|---:|---:|---:|---:|---:|
| claude-opus-5 | 214 | 52.831 | 150.171 | 13.791.044 | 13.994.260 | US$ 9,7191 |
| **TOTAL** | **214** | **52.831** | **150.171** | **13.791.044** | **13.994.260** | **US$ 9,7191** |

Acumulado do processo: **13.994.260 tokens — US$ 9,7191**.

Estimativa por token contra `~/.claude/scripts/pricing.json`, não a fatura real.

---

## 2026-09-10 · O kit saiu da raiz do vault

`bks-sdd-kit` morava em `X:/2brains/kit`, fora de `repos/`. Passou a
`repos/backside/prj-bks-kit`: é um projeto como os outros, e a raiz do vault não é lugar de
repositório.

O que a mudança exigiu, além de mover: cinco referências ao caminho antigo. Duas em `~/.claude` —
`extraKnownMarketplaces` no `settings.json` e `installLocation` no `known_marketplaces.json`, sem
as quais o próximo `plugin update` falharia por diretório inexistente. Uma permissão de leitura de
templates no `settings.local.json` do `nquantic`. Uma menção na wiki. E o `STATUS.md`.

Nada quebrou no uso: as skills rodam da cópia em
`~/.claude/plugins/cache/bks-sdd-kit/bks-sdd-kit/0.1.0`, e `${CLAUDE_PLUGIN_ROOT}` aponta para lá.
O diretório do repositório é origem, não o que executa.

**Um ponto a lembrar.** O `Move-Item` do PowerShell falhou no meio: migrou os arquivos soltos e
parou em `.git` por lock, deixando conteúdo dos dois lados. O `.git` completo — 225 objetos — já
tinha ido para o destino; a origem ficou com um esvaziado. Completar na direção do destino e
verificar com `git status` e `git fsck` resolveu, com os 14 commits intactos. Move interrompido no
Windows pede conferência de qual lado tem o repositório íntegro antes de qualquer nova ação.

## 2026-09-10 · Os casos de eval não carregavam — schema, não crédito

O `STATUS.md` registrava um bloqueio para a baseline dos evals: saldo de crédito. Eram dois, em
série, e o de cima escondia o de baixo.

**O que estava quebrado.** Os 18 casos foram escritos em `schema_version: "1.0"`. O
`claude plugin eval` recusa a carga fora do schema atual, com três divergências: `execution`
virou bloco obrigatório (leva `prompt` e `max_turns`), todo grader precisa de `name`, e
`with_only` saiu — `tool_used: Skill` já é tratado como indicador fora da pontuação. Nenhum dos
18 carregava. O run de 02/09 nunca chegou a exercitar skill alguma; o erro de crédito veio
depois, e foi o único que ficou registrado.

**Como o schema foi descoberto.** Não por documentação — não há pública. `claude plugin eval init
--bare` gera um caso no formato canônico (`prompt.md` + `graders/*.md`, um arquivo por grader,
nome vindo do arquivo), e o validador, sondado com casos mínimos sucessivos, devolveu o resto.

**O que se corrigiu** (`b836be1`, no kit): os 18 migrados para `1.1`, texto dos critérios
verbatim, 85 graders nomeados a partir do que cada um verifica — `sem-mediatr`,
`verifica-propriedade` — e não `g1`, `g2`; o relatório do CLI imprime esses nomes a cada run.

**O ponto cego.** `test_evals` checava se o YAML parseava e se o `name` batia com o diretório.
Nada disso falha quando o schema muda: a suíte passou verde por semanas com a suíte de eval
inteira fora do ar. Agora valida contra o schema do CLI — 319 verificações viraram 713. É o mesmo
padrão que o perfil já nomeia: regra sem guarda executável é intenção.

**Também.** O alvo por caminho resolve o plugin e liga o braço `without` (`Ablation: 2 arms × 18
cases`) — a hipótese do STATUS, de que seria preciso usar `bks-sdd-kit@bks-sdd-kit`, estava
errada; o `"plugins": []` vinha dos casos não carregarem. E a pasta `eval/` vazia foi removida: o
`ARCHITECTURE.md` a citava no lugar de `evals/`.

**O que resta.** Crédito, agora isolado e confirmado com casos válidos. Quando houver, a suíte
roda sem outro conserto.

---

## Antes de 2026-09-10

O kit foi extraído de um vault em uso e empacotado como plugin em 07/09, com 12 commits. Esse
histórico está nos commits do repositório e no `JOURNAL.md` do vault, que registra a
reestruturação de onde ele saiu.
