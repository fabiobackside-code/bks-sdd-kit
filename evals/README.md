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
