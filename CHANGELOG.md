# Changelog

Mudanças relevantes do `bks-sdd-kit`, da mais recente para a mais antiga. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versões seguem
[SemVer](https://semver.org/lang/pt-BR/).

## [1.2.0] — 2026-11-27

### Adicionado
- `bks-maintainability-review/references/repertorio-bks.md` 1.0.0: cem práticas do cânone BKS (o cânone de engenharia do time), cada
  uma com nível (DEVE APLICAR, RECONHECE ou SÊNIOR), sinal no código e eixo. O parecer registra a
  versão do repertório no cabeçalho.

### Alterado
- `bks-maintainability-review`: a persona soma o repertório BKS ao repertório da stack; a aplicação
  avaliada não é fonte de calibração; a lente pessoal é a `bks-daiwl`, em nota separada.
- Rubrica: o eixo A4 (aderência ao repertório) pontua pelo nível de cada item do repertório. A âncora
  5 do A10 (documentação do porquê) pede o porquê no `ARCHITECTURE.md` e, no código, só contrato e
  guarda contra regressão. A âncora 5 do A11 (duplicação e abstração) extrai função privada no
  segundo uso e abstrai a partir do terceiro.
- `stacks/dotnet.md`: `[LoggerMessage]` é repertório; base genérica com vários parâmetros é
  RECONHECE para herdar e SÊNIOR para escrever; concorrência manual e pooling são RECONHECE
  isolados em adapter, com a carga medida, e SÊNIOR em código de negócio.
- `criterios-comuns.md`: o endpoint e o worker chamam o serviço ou a sessão.
- `/bks:maintainability`: carrega o repertório e registra a versão; avisa em uma linha quando a
  `bks-daiwl` não tem configuração.
- `bks-tests`: o projeto de testes fica em `tests/[SolutionName].Tests/`, com `Architecture/`
  dentro; os templates sem `#region` e com nomes `Method_Condition_Result` em inglês.
- `bks-dotnet-solutions/references/stored-procedures.md`: o repositório não abre `Activity` à mão.

## [1.1.1] — 2026-11-17

### Adicionado
- Campo opcional `txc` no `.bks-profile.json`: `none` (padrão direto), `base` ou `motor`. Sem o
  campo, a skill de geração pergunta a forma e grava a resposta.
- `bks-dotnet-solutions` 3.0: entrevista em nove fases, com a forma do projeto (TXC ou padrão
  direto) e as portas de entrada e de saída declaradas uma a uma. Toda lista tem "outro", que vira
  Port. Referências novas: `ports-catalog.md` e `txc-base.md`.
- `bks-go-solutions` 2.0, com `go-txc.md`: TXC opcional por executor tipado.
- Casos de eval `dotnet-portas-worker`, `dotnet-stack-outro` e `go-txc`.

### Alterado
- `txc-guidelines.md` 2.2: sessão que cria o contexto somente leitura, pipeline `[10]` `[20]`
  `[40]` `[50]`, executor transacional e executor de consulta (`BksQueryExecutor`), dado entre
  passos por retorno tipado. Sai o objeto de transação mutável com `Hydrate`.
- `bks-typescript-solutions` 3.0, `bks-sdd`, `bks-standards` e o manifesto multiagente alinhados ao
  mesmo modelo.

### Limitação conhecida
- O delta entre os braços `with` e `without` dos casos `dotnet-txc`, `dotnet-portas-worker`,
  `dotnet-stack-outro` e `go-txc` não foi medido. A suíte estrutural confere a integridade dos
  arquivos; se o agente segue a entrevista nova, só o eval mostra.

## [1.0.1] — 2026-11-16

### Corrigido
- `bks-sdd`: o `test-spec-structure.md` removia o próprio bloqueio do `--feature-task` ao sugerir
  pular a Fase 6. Agora o TEST aprovado é exigido sem exceção, como o `SKILL.md` já dizia.

## [1.0.0] — 2026-11-08

Primeira versão estável. A partir dela, o kit segue SemVer sobre o contrato público descrito no
README: mudança incompatível em comando, skill, agente, schema de perfil, esqueleto de projeto,
guarda ou local de saída só entra em versão major.

### Adicionado
- README em inglês (`README.md`) e em português (`README.pt-BR.md`), com a seção de contrato público
  e versionamento.
- Guardas na suíte estrutural: sem marca de severidade nas instruções, sem marca em comentário de
  exemplo de código e sem nome de projeto interno no repositório.
- `bks-maintainability-review` ganhou as regras que a primeira execução real mostrou faltar:
  decisão registrada no eixo, critério de severidade, achado Média que impede a nota 5, limiar de
  âncora sem quantidade, script de medição guardado, teste de integração só contra recurso local ou
  autorizado, reuso de medição por hash de árvore, numeração de achados, identificação do avaliador
  e casos de fronteira da fundamentação. O cabeçalho do parecer ganhou persona, base de comparação e
  limiares.

### Alterado
- Callouts de severidade saíram das skills; ✅ e ❌ ficaram só como ícone de estado e par didático.

### Limitação conhecida
- A baseline dos casos de eval (delta entre os braços `with` e `without`) ainda não foi medida.

## [0.9.0] — 2026-11-08
### Adicionado
- `/bks:maintainability` oferece a `bks-daiwl` como lente pessoal opcional, quando ela já está
  configurada; a nota pessoal sai ao lado do parecer, sem se fundir a ele.

### Alterado
- `bks-daiwl` atualizada para a `1.0.1`.

## [0.8.0] — 2026-11-08

Versão de abertura para uso externo.

### Adicionado
- Skill `bks-daiwl` (*Don't Accept It Without Learning*), cópia fixada da versão `1.0.0` do
  repositório próprio: manutenibilidade pessoal do código gerado por IA (inteligência artificial).
- `THIRD_PARTY.md`: conteúdo de terceiros, licenças, inspirações e referências conceituais.
- `CONTRIBUTING.md`, `SECURITY.md`, modelos de issue e de pull request em `.github/`.

### Alterado
- `api-design`, `security-audit`, `debug-assistant`, `frontend-design`, `refactor-guide`,
  `pr-writer` e `doc-writer` reescritas do zero no padrão BKS (Backside).
- Os guias de método do `planner` e do `reviewer` foram reescritos e mudaram para
  `skills/bks-standards/references/metodo/`. Dentro de `agents/`, o Claude Code os carregava
  como agentes.
- Exemplos que citavam projetos internos passaram a ser genéricos.
- `JOURNAL.md` e `STATUS.md` do mantenedor saíram do repositório; o histórico público é este
  arquivo.

## [0.7.0] — 2026-10-15
### Adicionado
- Comando `/bks:maintainability` e skill `bks-maintainability-review`: parecer de
  manutenibilidade por aplicação e documento de fundamentação, com critérios por stack (.NET e
  SQL).

## [0.6.0] — 2026-10-14
### Adicionado
- Skill `bks-writing` e a guarda de escrita, com revisão de texto no `/bks:review`.
- O `/bks:canonize` confronta a skill referenciada com o que o projeto concretizou.

## [0.5.0] — 2026-09-15
### Adicionado
- O tier de cada agente fica visível, e o consumo de subagente entra na medição.

## [0.4.0] — 2026-09-15
### Alterado
- O namespace dos comandos passou de `bks-sdd-kit` para `bks`.

## [0.3.0] — 2026-09-15
### Alterado
- Os comandos passam a existir só no plugin; a suíte verifica todo ponteiro para arquivo do kit.

## [0.2.1] — 2026-09-14
### Adicionado
- Ciclo de realimentação: a spec aprovada volta para o contexto canônico.

## [0.2.0] — 2026-09-10
### Adicionado
- Go como terceira stack de backend (`bks-go-solutions`).
- Artefatos de projeto nos templates; casos de eval migrados para o schema do CLI.

## [0.1.0] — 2026-09-02
### Adicionado
- Primeira versão do plugin: skills de SDD, .NET e TypeScript, `bks-tests`, `bks-standards`,
  perfis de projeto, renderers de arquitetura, guardas executáveis e a suíte estrutural.
