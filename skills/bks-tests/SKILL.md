---
name: bks-tests
description: >
  Analisa uma solution .NET, cria ou melhora um projeto unico de testes xUnit dentro de src/
  e leva a cobertura a 90%+ em linhas, branches e metodos, com conformidade SonarQube.
  Use sempre que o usuario quiser criar testes para uma solution .NET, subir a cobertura,
  montar projeto de testes, gerar relatorio de cobertura, corrigir issues do SonarQube em
  testes, ou configurar coverlet e ReportGenerator. Trigger: cobertura de testes, xUnit,
  90% de cobertura, projeto de testes .NET, coverlet, ReportGenerator, SonarQube nos testes,
  testes unitarios e de integracao .NET.
---

# BKS-TESTS — Cobertura de testes em solution .NET

**Idioma:** interacao e documentacao gerada em **PT-BR**. Codigo, nomes de classe, metodo e
variavel em **ingles**.

## O que esta skill entrega

1. Analise da estrutura da solution e do que ja existe de teste
2. Um projeto unico de testes xUnit, dentro de `src/`, organizado em `Unit/`, `Integration/` e
   `Shared/`
3. Cobertura de 90%+ em linhas, branches e metodos
4. Relatorio HTML navegavel
5. Scripts de execucao e integracao com CI/CD
6. Guia de testes no repositorio

## Duas regras que nao se negociam

### Localizacao do projeto de testes

O projeto de testes fica em `src/`, junto dos projetos de producao:

```
src/
├── [ProjectName1]/
├── [ProjectName2]/
└── [SolutionName].Tests/     <- aqui
```

Nunca em `tests/`, `test/` ou na raiz. A solution inteira vive em `src/`; separar os testes
quebra a consistencia, alonga os caminhos relativos entre projetos e complica build e deploy.

Um projeto so. Unitario e integracao convivem nele, separados por diretorio — nao por projeto.

### Biblioteca de assercao

Use exclusivamente o `Assert` nativo do xUnit.

Nunca instale FluentAssertions: a v8 passou a licenca comercial paga (Xceed) e a v7.x e a ultima
sob Apache 2.0. Nao substitua por Shouldly nem equivalente.

## Fases

Execute na ordem. Cada fase tem sua referencia — **abra a referencia da fase no momento em que
for executa-la**, nao antes.

| Fase | O que faz | Referencia |
|---|---|---|
| 1 | Mapeia a solution, os projetos e os gaps de teste | `references/solution-analysis.md` |
| 2 | Cria ou melhora o projeto de testes, com pacotes e coverage configurados | `references/test-project-setup.md` |
| 3 | Prioriza o que testar e gera os testes | `references/coverage-strategy.md` + `references/test-templates.md` |
| 4 | Executa com cobertura e gera o relatorio HTML | `references/coverage-execution.md` |
| 5 | Cria os scripts de automacao e a integracao com CI/CD | `references/coverage-execution.md` |
| 6 | Escreve o guia de testes do repositorio | `references/test-docs-template.md` |

**Antes de gerar qualquer arquivo de teste**, leia `references/sonarqube-conformance.md` — sao
cinco regras que evitam issue de SonarQube no codigo gerado (nullable, value type em
`Assert.NotNull`, using duplicado, `SqlException` obsoleto, mock com retorno nullable) e o
checklist de validacao por arquivo.

## Antes de comecar

Confirme com o usuario:

1. **Alvo de cobertura** — 90% e o default desta skill. Solution legada as vezes pede uma escada
   (70% agora, 90% em duas fases). Pergunte se 90% direto e realista aqui.
2. **Projetos de infraestrutura a excluir** — wrapper de transporte, adaptador de socket,
   biblioteca gerada. Cobrir isso nao mede nada util e derruba o percentual da solution. Se
   houver, peca o padrao de nome; a exclusao entra no `sonar-project.properties` e no `.csproj`.
3. **Testes de integracao** — se a solution depende de banco ou broker, confirme se ha
   Testcontainers ou ambiente disponivel. Sem isso, a fase de integracao fica de fora e o alvo
   de cobertura muda.

Nao pergunte o que da para descobrir lendo a solution.

## Conduta

**Mostre progresso por fase**, com o que foi criado e o percentual atingido. Nao encerre sem
validar a cobertura contra o alvo — relatorio que nao foi conferido nao e entrega.

Se o alvo nao for atingido, diga o numero real, aponte as classes que faltam e proponha o proximo
passo. Nunca declare cobertura atingida sem a saida do relatorio.
