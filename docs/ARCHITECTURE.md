# Arquitetura do bks-sdd-kit

## O que este repositorio e

Um plugin do Claude Code. Nao contem codigo de aplicacao — contem **processo**: instrucoes que o
agente carrega para conduzir um ciclo de Spec-Driven Development.

A unidade de entrega e o pacote instalavel. Antes deste repo, skills, comandos e agentes viviam
soltos em pastas de usuario, sem versao e duplicados entre a instalacao global e o vault. O
empacotamento existe para dar a essas pecas uma unica fonte da verdade, versionada.

## Estrutura

```
.claude-plugin/     manifestos (plugin.json, marketplace.json)
skills/             skills, cada uma com SKILL.md + references/
commands/           slash commands
agents/             subagentes com papel e modelo declarados
scripts/            utilitarios chamados pelas skills (medicao de custo)
hooks/              guardas executaveis de regra
eval/               suites de teste das skills
docs/               esta documentacao
```

## Decisoes

### Progressive disclosure nas skills

Cada skill tem um `SKILL.md` de entrada e um diretorio `references/` carregado sob demanda. O
`SKILL.md` decide qual referencia abrir; o conteudo pesado nao entra no contexto ate ser
necessario.

O motivo e custo: uma skill que carrega todas as suas fases a cada invocacao paga por instrucao
que nao vai usar. `bks-sdd` tem sete fases; um comando de status nao precisa das outras seis.

`bks-tests` nasceu ja neste formato: era um slash command de 2043 linhas que entrava inteiro no
contexto a cada invocacao. Virou um `SKILL.md` de 93 linhas — regras inegociaveis, tabela de fases
e ponteiros — com sete referencias abertas sob demanda.

Estado atual: `bks-sdd`, `bks-dotnet-solutions` e `bks-typescript-solutions` tem `references/`,
mas o `SKILL.md` ainda concentra as fases. O adelgacamento esta planejado para depois das suites
de eval — refactor de skill validada em uso sem rede de teste e aposta, nao engenharia.

### Caminhos por variavel de ambiente

Os comandos de workbench referenciavam caminhos absolutos de uma maquina. Num pacote publico isso
nao funciona e vaza estrutura pessoal.

As referencias passaram a `${BKS_VAULT}`, `${BKS_BRAIN}` e `${BKS_REPOS}`. As skills nao dependem
de nenhuma delas — operam sobre o diretorio de trabalho atual, e por isso servem a qualquer
projeto sem configuracao.

### Separacao de papeis entre agentes

Quatro agentes com ferramentas e modelos distintos, nao um agente generico:

- `reviewer` e read-only e roda em invocacao separada. Quem escreveu o codigo nao revisa a propria
  seguranca — o vies de quem implementou e saber que o filtro esta la porque o pos nos outros
  tres.
- `scribe` roda em Haiku e so registra o que foi confirmado com evidencia. Documentacao que
  infere resultado e pior que documentacao ausente.
- `planner` nao tem Bash nem Edit de codigo de producao. Separar quem especifica de quem
  implementa evita spec escrita para caber no que ja foi codado.
- `builder` opera sob LOOP-4 — no maximo quatro tentativas contra goals verificaveis (build
  limpo, testes verdes, cenarios da `TEST` cobertos).

### Regra precisa de guarda executavel

Regra que vive so em texto de instrucao nao sobrevive a pressa. O diretorio `hooks/` existe para
converter as regras de entrega em verificacao automatica no momento em que o trabalho e conferido,
e nao em recomendacao lida no inicio da sessao.

## Consumidores

O kit foi extraido de um vault em uso. Os projetos que o consomem continuam sendo a fonte de
validacao — mudanca de contrato aqui precisa ser verificada contra eles antes de virar versao.
