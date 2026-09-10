# Arquitetura do bks-sdd-kit

## O que este repositório é

Um plugin do Claude Code. Não contém código de aplicação — contém **processo**: instruções que o
agente carrega para conduzir um ciclo de Spec-Driven Development.

A unidade de entrega é o pacote instalável. Antes deste repo, skills, comandos e agentes viviam
soltos em pastas de usuário, sem versão e duplicados entre a instalação global e o vault. O
empacotamento existe para dar a essas peças uma única fonte da verdade, versionada.

## Estrutura

```
.claude-plugin/     manifestos (plugin.json, marketplace.json)
skills/             skills, cada uma com SKILL.md + references/
commands/           slash commands
agents/             subagentes com papel e modelo declarados
scripts/            utilitarios chamados pelas skills (medição de custo)
hooks/              guardas executáveis de regra
evals/              suites de eval das skills, um diretório por caso
docs/               está documentação
```

## Decisões

### Progressive disclosure nas skills

Cada skill tem um `SKILL.md` de entrada e um diretório `references/` carregado sob demanda. O
`SKILL.md` decide qual referência abrir; o conteúdo pesado não entra no contexto até ser
necessário.

O motivo e custo: uma skill que carrega todas as suas fases a cada invocação paga por instrução
que não vai usar. `bks-sdd` tem sete fases; um comando de status não precisa das outras seis.

`bks-tests` nasceu já neste formato: era um slash command de 2043 linhas que entrava inteiro no
contexto a cada invocação. Virou um `SKILL.md` de 93 linhas — regras inegociaveis, tabela de fases
e ponteiros — com sete referências abertas sob demanda.

Estado atual: `bks-sdd`, `bks-dotnet-solutions` e `bks-typescript-solutions` tem `references/`,
mas o `SKILL.md` ainda concentra as fases. O adelgacamento está planejado para depois das suites
de eval — refactor de skill validada em uso sem rede de teste e aposta, não engenharia.

`bks-go-solutions` nasceu no formato alvo: 222 linhas de entrada — registro de tipos, variáveis,
fluxo, base de aprendizado e checklist — contra 856 do .NET e 716 do TypeScript, com os cinco
prompts especializados em `references/`, abertos um por vez. É a referência de como as outras três
devem ficar.

### O delta de linguagem mora em `bks-standards`, não na skill geradora

As premissas (TXC, pipeline explícito, Result, calisthenics, pragmatismo token-aware) são método,
não linguagem, e vivem em `bks-standards/references/bks-premises.md`. As skills geradoras
produzem estrutura e apontam para lá.

Go forçou a distinção a ficar explícita, porque é a primeira linguagem do kit que **contradiz** o
padrão-base em pontos concretos: `error` idiomático no lugar de `Result[T]`, imutabilidade por
disciplina sem `record`, interface declarada no consumidor e não no provedor, wiring manual sem
container, e metade do Object Calisthenics chegando por early return em vez de polimorfismo.

Esse delta ficou em `bks-standards/references/go-standards.md`, simétrico ao `dotnet-standards.md`
que já existia — não dentro de `bks-go-solutions`. A alternativa (skill autossuficiente) duplicaria
premissa em duas casas, e premissa duplicada diverge na primeira mudança. `bks-premises.md` ganhou
um aviso no ponto onde o padrão-base é descrito em termos de C#, porque quem lê aquele parágrafo e
gera Go direto produz código que compila e que nenhum programador Go mantém.

### A skill de Go alimenta e consome uma base de aprendizado

`bks-go-solutions` é a primeira skill do kit que **escreve fora do projeto**: a cada geração,
consulta `${BKS_KNOWLEDGE}/wiki/go/` antes e registra depois. As demais só leem referência
estática.

A razão é que Go entrou como stack nova, sem os anos de prática que .NET e TypeScript já têm. O que
se aprende nos primeiros projetos é justamente o que não está em nenhuma referência — e sem
registro, se perde entre uma sessão e outra.

O registro é em duas casas, com papéis distintos, e é o que resolve a confidencialidade: o caso
completo com nomes reais fica em `brain/engineering/` do projeto (repositório fechado, contexto
ligado ao código); a wiki recebe a lição destilada e **anonimizada**. Os projetos de origem são de
domínio bancário — a lição é transversal, o caso não é. A regra de anonimização está no `index.md`
da base e repetida na skill, porque regra que vive num lugar só não sobrevive à pressa.

Quatro classes: padrão, armadilha, trecho e decisão Go vs .NET. A quarta existe para que a escolha
de stack seja revisitável com evidência, e não por impressão.

O risco conhecido é a base encher de trivialidade — página que repete o Effective Go. A contenção
é instrução explícita de só registrar o que custou tempo, e `status: draft` até a lição se repetir
em outro projeto. Se não bastar, o passo seguinte é uma guarda executável, não mais texto.

### Caminhos por variavel de ambiente

Os comandos de workbench referenciavam caminhos absolutos de uma maquina. Num pacote público isso
não funciona e vaza estrutura pessoal.

As referências passaram a `${BKS_VAULT}` e `${BKS_KNOWLEDGE}`. São duas, não mais: cada projeto
guarda sua própria memória, decisão e domínio, e não há hub central a apontar.

As skills não dependem de nenhuma das duas — operam sobre o diretório de trabalho atual, e por
isso servem a qualquer projeto sem configuração. Só dois comandos precisam do vault: `/brain` no
modo panorama, que percorre `repos/`, e `/new-project`, que cria dentro dele.

### Separação de papéis entre agentes

Quatro agentes com ferramentas e modelos distintos, não um agente genérico:

- `reviewer` e read-only e roda em invocação separada. Quem escreveu o código não revisa a própria
  segurança — o vies de quem implementou e saber que o filtro está la porque o pos nos outros
  três.
- `scribe` roda em Haiku e só registra o que foi confirmado com evidência. Documentação que
  infere resultado e pior que documentação ausente.
- `planner` não tem Bash nem Edit de código de produção. Separar quem específica de quem
  implementa evita spec escrita para caber no que já foi codado.
- `builder` opera sob LOOP-4 — no máximo quatro tentativas contra goals verificáveis (build
  limpo, testes verdes, cenários da `TEST` cobertos).

### Regra precisa de guarda executável

Regra que vive só em texto de instrução não sobrevive a pressa. Um SDK deste kit foi construido
inteiro — quatro fases, vinte e uma tasks — sem `README.md` nem `ARCHITECTURE.md`, e com quase um
terco do código em comentario. A regra existia havia uma semana. Vivia no lugar errado: era lida
na abertura da sessão, e não no ponto onde o trabalho e conferido.

Os guardas em `hooks/` são a resposta. Três deles recusam a escrita, não avisam:

- `no_dispatcher` recusa `MediatR` e equivalentes em `.cs`. Dispatcher esconde a ordem dos passos
  atras de uma convenção de tipo; não da para ler o fluxo sem procurar o handler.
- `comment_budget` recusa bloco acima de cinco linhas e marca de severidade. O que denúncia ensaio
  não e a proporção de comentario no arquivo, e o bloco longo — decisão e trade-off pertencem a
  este documento.
- `dod_docs` recusa a declaração de tipo público enquanto `README.md` e `ARCHITECTURE.md` não
  tiverem sido tocados na mesma leva. Le o working tree do git, não o conteúdo dos documentos:
  o guarda cobra que a documentação entre na mesma passada, não julga se ela ficou boa.

Três escolhas os mantém usaveis. Ignoram arquivo de teste, arquivo fora de repositório git e o
que não e `.cs`. Falha interna libera a escrita — guarda que quebra o fluxo por bug próprio e
desligado em uma semana, e a regra volta a ser intenção. E cada um tem teste em `hooks/tests/`,
pela mesma razão que existe: guarda sem teste também e só intenção.

### Schema dos casos de eval

Os casos vivem em `evals/<caso>/case.yaml` e o `plugin.json` os declara em
`experimental.evals`. O schema é do `claude plugin eval`, não nosso: fora dele o caso não carrega
e não roda.

O schema `1.1` difere do `1.0` em quatro pontos: `prompt` e `max_turns` vivem dentro de
`execution`; todo grader tem `name`; `with_only` não existe mais — `tool_used: Skill` já é tratado
como indicador de disparo, fora da pontuação; e `runs` fica no topo.

Os 18 casos passaram semanas escritos em `1.0` sem carregar. `test_evals` checava se o YAML
parseava e se o `name` batia com o diretório — nada disso falha quando o schema muda. A suíte
passava verde enquanto a suíte de eval estava inteira fora do ar.

Por isso `test_evals` valida contra o schema, e não contra o parser. A regra que só o CLI conhece
precisa de guarda deste lado; senão a próxima mudança de schema volta a passar despercebida até
alguém gastar crédito para descobrir.

Os nomes dos graders são derivados do critério — `sem-mediatr`, `verifica-propriedade` — e não
posicionais. O relatório do CLI os imprime a cada run, e `g1 falhou` não diz o que quebrou.

## Consumidores

O kit foi extraido de um vault em uso. Os projetos que o consomem continuam sendo a fonte de
validação — mudança de contrato aqui precisa ser verificada contra eles antes de virar versão.
