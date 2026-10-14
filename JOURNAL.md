# JOURNAL — prj-bks-kit

> Marcos e sessões, do mais recente para o mais antigo. Acrescentado pelo `/save`; nunca
> reescrito. O `STATUS.md` diz onde o projeto está agora; este arquivo diz como chegou até aqui.

---

## 2026-10-14 · A escrita ganha skill, guarda e revisão

O padrão de escrita que o NQuantic aplicou em quatro documentos de arquitetura e nos decks veio
para o kit como `bks-writing`, sem nada do projeto. A decisão entra sintetizada no texto, e o
número do ADR só no fim da nota de decisão. A guarda `writing_guard` roda depois da escrita, devolve
os achados ao agente e lembra o usuário de rodar o `/bks:review`, que passou a conferir a escrita.
Ela conta o mesmo que a guarda em PowerShell do NQuantic: 75 achados antes da reescrita, zero depois.

As skills `writing-anti-ai` e `human-writing` ficaram em `third-party/` como consulta, com licença
MIT e mapeamento do que vale, do que foi adaptado e do que conflita. O comentário de código perdeu
o ponteiro para documento no `doc-writer`, no `bks-dotnet-solutions`, no `bks-sdd` e no
`comment_budget`. Antes da branch, foi para `main` o confronto da skill com o projeto no
`/bks:canonize`. Versão `0.6.0` instalada da branch `feat/skill-escrita`; o eval do caso novo não
rodou.

### Consumo da sessao

| Modelo | Input | Output | Cache write | Cache read | Total | Custo |
|---|---:|---:|---:|---:|---:|---:|
| claude-opus-5-5 | 124 | 52.799 | 195.161 | 10.726.694 | 10.974.778 | US$ 8,6356 |
| **TOTAL** | **124** | **52.799** | **195.161** | **10.726.694** | **10.974.778** | **US$ 8,6356** |

**TOTAL GERAL: 126.542.188 tokens — US$ 83,2238**

---

## 2026-09-15 · O tier deixa de ser invisível, e o subagente entra na conta

Os comandos passaram a responder como `/bks:*`: o namespace de plugin é obrigatório — a
documentação do Claude Code diz que nenhuma chave de frontmatter o remove — então a decisão que
restava era o comprimento dele, e `bks-sdd-kit` virou `bks`. As 330 ocorrências de documentação
nos dois repositórios foram atrás.

O `session_cost.py` media só o thread principal. Nesta sessão, três subagentes consumiram 278.890
tokens que não entravam em relatório nenhum — inclusive nos números que esta própria sessão
reportou mais cedo. O dado estava na notificação de conclusão, e o tipo do agente na chamada da
tool `Agent`; o script passou a correlacionar pelo `tool-use-id`. A tabela não soma ao custo, e
isso é deliberado: a notificação traz tokens, não tier.

O `planner` subiu de Sonnet para Opus. É onde o erro custa mais caro — spec errada contamina toda
task abaixo dela — e fica sob medição por dez FEATs, com o método de comparação escrito no
`ARCHITECTURE.md`.

A documentação do vault foi reescrita na mesma sessão: dois documentos que descreviam um hub
central morto foram apagados depois de extraído o que valia, e o `CONHECIMENTO.md` passou a cobrir
o que nenhum arquivo cobria — como o acervo cresce e o que merece virar página.

O que isto trava: o caminho do alerta do `/bks:save` continua sem prova, e agora espera o
`dash-scheduller` ter árvore limpa.

### Consumo da sessão

| Modelo | Input | Output | Cache write | Cache read | Total | Custo |
|---|---:|---:|---:|---:|---:|---:|
| claude-opus-5 | 718 | 162.676 | 322.005 | 77.996.928 | 78.482.327 | US$ 46,2890 |
| **TOTAL** | **718** | **162.676** | **322.005** | **77.996.928** | **78.482.327** | **US$ 46,2890** |

Acumulado do processo: **115.567.410 tokens — US$ 74,5883**. Estimativa por token contra o
`pricing.json` do kit, não fatura.

### Modelos usados

| Agente | Modelo | Invocações | Tokens |
|---|---|---:|---:|
| `geral` | ? | 2 | 206.282 |
| `claude-code-guide` | ? | 1 | 72.608 |
| **TOTAL** | | **3** | **278.890** |

Os três subagentes levantaram o comportamento do `name:` em comando de plugin, inventariaram a
documentação do vault e analisaram o `bks-multiagent-skill`. Nenhum é agente do kit, por isso o
tier aparece como `?` — o script não infere modelo de agente que não declara. Primeira sessão em
que esses tokens aparecem em relatório: antes desta medição, eram invisíveis.

## 2026-09-15 · O `/save` certo, enfim, sabe calar

O `claude plugin update` subiu o kit para `0.3.0` e a sessão reiniciou com o comando unificado. O
`/save` rodou aqui pelo caminho do silêncio, e desta vez o comando exercitado foi o certo: o prompt
trouxe o passo 4, da verificação do canônico, e o passo 7, da medição — os dois só existem na
`0.3.0`.

Sem `docs/canonical/CONTEXT.md` neste repositório, o passo 4 não disse nada, como previsto. O falso
positivo mais caro, alertar projeto que não tem canônico, está descartado por execução — a prova
que a entrada anterior desta data alegava ter e não tinha.

Falta o caminho do alerta, no `dash-scheduller`. E fica registrado que os comandos hoje respondem
com namespace (`bks-sdd-kit:save`), porque o frontmatter não traz `name:` — devolver o `/save` puro
é decisão que muda o contrato dos onze e não foi tomada.

### Consumo da sessão

| Modelo | Input | Output | Cache write | Cache read | Total | Custo |
|---|---:|---:|---:|---:|---:|---:|
| claude-opus-5 | 282 | 61.941 | 149.830 | 18.520.535 | 18.732.588 | US$ 12,3085 |
| **TOTAL** | **282** | **61.941** | **149.830** | **18.520.535** | **18.732.588** | **US$ 12,3085** |

Acumulado do processo: **55.817.671 tokens — US$ 40,6077**. Estimativa por token contra o
`pricing.json` do kit, não fatura.

## 2026-09-15 · Os comandos passam a existir só no plugin

A entrada abaixo, desta mesma data, está errada no ponto que mais importa: o `/save` exercitado não
foi o do kit. Havia duas cópias de cada comando — `commands/` deste repositório e
`~/.claude/commands/` — e a global vencia na resolução de nome. O comando que rodou não tinha a
verificação do canônico, então o silêncio observado não provava nada: aquela cópia nunca ia falar.

O levantamento mostrou onze comandos duplicados, não dois. Sete diferiam só por acentuação. Quatro
divergiam em conteúdo, e nenhum lado era completo: o `save` do kit tinha o ciclo do canônico, o
global tinha a medição de consumo. O kit ainda carregava seis ponteiros para arquivos inexistentes,
incluindo dois que a cópia global tinha corretos.

A causa de os ponteiros passarem despercebidos era o regex da própria suíte, que só casava ASCII
minúsculo e portanto não enxergava `checklist-revisão-crítica.md`. Com a verificação estendida,
uma das três falhas antigas caiu junto — era o mesmo defeito, sob outro nome.

A instalação global foi removida depois de migrado o que tinha de melhor, e a medição de consumo
virou `commands/references/medicao-consumo.md`. O `session_cost.py` foi validado rodando da cópia
do plugin com a global já apagada.

O que isto trava: o `/save` unificado continua sem teste real. Esta sessão o escreveu, não o
exercitou — e o plugin instalado ainda é o `0.2.1`, anterior a estas mudanças.

## 2026-09-15 · O `/save` novo sabe calar

Primeira execução do `/save` de `0.2.1`, neste repositório, em sessão nova — a condição que faltava
desde ontem, quando o `claude plugin update` pediu reinício e a sessão anterior seguiu com os
comandos de `0.2.0`.

O caminho exercitado foi o do silêncio: não há `docs/canonical/`, `specs/` nem `decisions/` aqui, e
a verificação de defasagem não acrescentou nada ao `STATUS.md`. Era o falso positivo mais caro
previsto no desenho — alertar projeto sem canônico treina o leitor a ignorar o aviso — e está
descartado por execução.

Metade da prova. O caminho do alerta continua sem teste, e o alvo segue sendo o `dash-scheduller`,
que precisa da árvore limpa antes.

### Consumo da sessão

| Modelo | Input | Output | Cache write | Cache read | Total | Custo |
|---|---:|---:|---:|---:|---:|---:|
| claude-opus-5 | 20 | 4.081 | 53.745 | 777.722 | 835.568 | US$ 1,0284 |
| **TOTAL** | **20** | **4.081** | **53.745** | **777.722** | **835.568** | **US$ 1,0284** |

Acumulado do processo: **37.920.651 tokens — US$ 29,3277**. Estimativa por token contra
`~/.claude/scripts/pricing.json`, não fatura.

## 2026-09-14 · O canônico deixou de ser mão única

O fluxo documental ia do `/canonize` ao `/spec` e nunca voltava. Depois da primeira entrega o
sentido se inverte: a FEAT aprovada e o ADR fechado viram a verdade do projeto, e o
`docs/canonical/CONTEXT.md` envelhece sem que nada sinalize — alimentando o `/prd` seguinte com
informação vencida.

A correção ficou em duas metades. O `/canonize` passou a ler `specs/` e `decisions/` como fonte
citável, com precedência sobre `docs/input/` onde os dois se contradizem. O `/save` compara a data
do `CONTEXT.md` com a desses diretórios e registra a defasagem na seção do que trava do
`STATUS.md` — que é o que o `/brain` lê na sessão seguinte, e não some quando a sessão fecha.

Duas alternativas foram descartadas e estão no `ARCHITECTURE.md`. A nota-ponte em `docs/input/`,
porque síntese de segunda mão afasta a afirmação da fonte, e spec aprovada já é fonte com caminho
e data. A detecção no `/review`, porque ele dispensa mudança que não toca área sensível —
documentação, justamente — e o agente `reviewer` é read-only, sem o estado da sessão que aprovou a
FEAT.

A detecção foi validada por fora do comando, com o mesmo `find` que ele executa: sete projetos
consumidores com canônico, quatro limpos e três divergentes, nenhum falso positivo. São doze
decisões reais fora do canônico, e o `dash-scheduller` é o caso que fecha o argumento — o
`CONTEXT.md` v6 não cita ADR-003 nem ADR-004 em lugar nenhum, enquanto o `STATUS.md` do projeto já
lista quatro decisões cuja fonte são esses dois arquivos.

Fica um débito que a regra do próprio kit cobra: guarda sem teste é intenção, e esta não tem
guarda. É o primeiro caso em que a regra vale para o projeto consumidor e o teste não tem onde
morar deste lado.

O plugin subiu para `0.2.1` — sem o bump, a reinstalação sobre `0.2.0` não recopia o cache.
`claude plugin update` confirmou `0.2.0 → 0.2.1` e o cache tem os comandos novos. O `/save` de
`0.2.1`, porém, não rodou nenhuma vez: o próprio CLI avisou `Restart to apply changes`, e a sessão
que fez a mudança seguiu com os comandos antigos.

`python tests/test_structure.py` → `720 verificacoes, 3 falhas` — as mesmas três já conhecidas,
nenhuma nova.

Commits: `61802c6` (comandos e documentação), `5fda0fe` (merge), `74fc59b` (`0.2.1`), `b302e24`
(fechamento).

### Consumo da sessao

| Modelo | Input | Output | Cache write | Cache read | Total | Custo |
|---|---:|---:|---:|---:|---:|---:|
| claude-opus-5 | 110 | 26.608 | 262.623 | 5.349.637 | 5.638.978 | US$ 5,9668 |
| **TOTAL** | **110** | **26.608** | **262.623** | **5.349.637** | **5.638.978** | **US$ 5,9668** |

Acumulado do processo: **37.085.083 tokens — US$ 28,2992** em 3 sessoes.

Estimativa por token contra a tabela local de precos, nao a fatura oficial.

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
