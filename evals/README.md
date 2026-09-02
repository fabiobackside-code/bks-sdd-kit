# Suites de eval do bks-sdd-kit

Casos para `claude plugin eval`. Cada diretorio tem um `case.yaml` com o prompt, os graders e as
tags.

```
claude plugin eval .
claude plugin eval . --case 'dotnet-*'
claude plugin eval . --tag guarda
claude plugin eval . --threshold 0.8
```

## O que estas suites verificam

Comportamento, nao estrutura. A pergunta e se a skill ainda **decide certo** depois de mexerem
nela — se recusa MediatR, se mantem o projeto de testes em `src/`, se pergunta antes de assumir.

A verificacao de que o arquivo continua integro (frontmatter, referencia que resolve, comando
documentado que existe) e da suite estrutural, em `tests/test_structure.py`, que roda sem
depender de modelo.

As duas se complementam: a estrutural pega o refactor que quebrou o arquivo, e estas pegam o
refactor que manteve o arquivo valido e perdeu a regra.

## Os casos

Cada caso testa a regra **sob pressao**: o prompt pede explicitamente o que a skill deve recusar,
ou descreve o atalho que ela nao deve tomar. Um caso que so pergunta o que a skill ja quer
responder nao mede nada.

| Caso | Pressao aplicada |
|---|---|
| `dotnet-sem-dispatcher` | pede MediatR pelo nome |
| `dotnet-txc` | pede propagacao de contexto sem dizer como |
| `tests-assert-nativo` | pede FluentAssertions pelo nome |
| `tests-local-projeto` | pede o projeto de testes em `tests/` na raiz |
| `doc-writer-teto-comentario` | pede comentario longo com alerta em vermelho |
| `security-audit-autorizacao` | afirma que o time e um pentest ja aprovaram |
| `debug-reproduz-antes` | pede o null check direto, sem diagnostico |
| `refactor-rede-antes` | mistura refatoracao, correcao de bug e otimizacao |
| `api-design-contrato` | traz um desenho pronto com GET que altera estado |
| `frontend-design-identidade` | pede "algo simples e padrao" |
| `pr-writer-le-diff` | descreve a mudanca como "nada demais" |
| `arch-notacao-bks` | nao menciona cor nem convencao — a notacao tem que sair sozinha |
| `arch-fallback-renderer` | pede renderer externo e logo de marca |
| `new-project-perfil` | descreve um projeto sem nomear o perfil |
| `bks-sdd-fase-0` | invoca a fase sem dar o nome do workspace |
| `bks-sdd-fase-1` | pede PRD com escopo curto demais |
| `plan-tasks-atomicas` | pede plano onde caberia comecar a implementar |
| `ts-selecao-tipo` | descreve backend sem dizer de que tipo |

## Ablacao

O default e `--ablation with-without`: cada caso roda tambem sem o plugin, e o relatorio mostra o
delta. E o numero que importa — um caso que passa nos dois bracos nao esta medindo a skill, esta
medindo o modelo.

Grader marcado `with-only` (o `tool_used: Skill`, por exemplo) indica que a skill disparou, e nao
entra na pontuacao.

## Estado

Escritas contra o formato documentado em `claude plugin eval --help`, **ainda nao executadas** —
o comando esta em early access. Ao rodar pela primeira vez, espere ajustar campo e limiar antes
de tratar o resultado como linha de base.
