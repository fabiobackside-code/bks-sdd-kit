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
eval/               suites de teste das skills
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

## Consumidores

O kit foi extraido de um vault em uso. Os projetos que o consomem continuam sendo a fonte de
validação — mudança de contrato aqui precisa ser verificada contra eles antes de virar versão.
