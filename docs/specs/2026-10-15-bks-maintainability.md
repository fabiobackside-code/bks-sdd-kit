# `/bks:maintainability` e a skill `bks-maintainability-review`

Desenho aprovado em 2026-10-15. Entra na versão 0.7.0.

## Objetivo

Um comando que, aberto no repositório de um projeto, encontra em `app/` as aplicações concretas
(APIs, Workers, Web Services, componentes, SDKs, scripts SQL) e gera:

- um parecer de manutenibilidade por aplicação, com nota de 0 a 100 para um desenvolvedor pleno;
- um único documento de fundamentação do projeto: literatura, conceitos, padrões e decisões que
  sustentaram a construção.

Na dúvida, o comando pergunta. O conteúdo começa por .NET e SQL e cresce por stack.

## Peças

| Peça | Onde |
| --- | --- |
| Skill | `skills/bks-maintainability-review/` |
| Critérios por stack | `skills/bks-maintainability-review/stacks/` (`dotnet.md`, `sql.md`) |
| Critérios de qualquer stack | `references/criterios-comuns.md` |
| Cofre e OpenShift, só quando detectados | `references/criterios-condicionais.md` |
| Comando | `commands/maintainability.md` |
| Sugestão após o canônico | passo 8 de `commands/canonize.md` |
| Caso de eval | `evals/maintainability-inventario-pergunta/` |

## Decisões

| Tema | Decisão |
| --- | --- |
| Nome | `/bks:maintainability`. Juntar com o `/bks:review` foi descartado: o `reviewer` só lê, revisa diff e bloqueia entrega |
| Saída | `outputs/maintainability/<app>_<tipo>_<AAAA-MM-DD>.html` e `outputs/references/<projeto>_fundamentacao_v<N>_<AAAA-MM-DD>.html`, na raiz do projeto |
| Persona | Pleno, 3 a 5 anos. Calibrada pelo perfil e pela wiki do vault quando `BKS_VAULT` existe; sem vault, roda e declara |
| Stack sem critérios | Lista no inventário e pergunta: pular, ou avaliar só com a rubrica e confiança baixa |
| Tipos | API, Worker, Web Service, Componente, Scripts SQL, cada um com pesos próprios na rubrica |
| Comparação | O parecer anterior da mesma aplicação em `outputs/maintainability/` vira base de comparação sem o usuário enviar |
| Registro | `docs/prompts/prompt-maintainability-<data>.md` com o critério da execução |

## Fluxo do comando

1. Confere que está num projeto (`STATUS.md`) e que `app/` tem código.
2. Inventaria `app/` pela seção Detecção de cada stack.
3. Pergunta quando há tipo indeterminado, stack sem critérios ou aplicação ambígua; acima de três
   aplicações, confirma a lista.
4. Lê o contexto do projeto e, se houver, o vault.
5. Gera um parecer por aplicação, sem sobrescrever.
6. Gera a fundamentação, só com versão nova se algo mudou.
7. Grava o registro e reporta uma linha por aplicação.

## Verificação

- `python tests/test_structure.py`: `skills/` só com pastas; stack com Detecção, Repertório e
  Critérios; núcleo sem CyberArk; comando gravando em `outputs/`; `/bks:canonize` sugerindo o
  comando.
- `claude plugin eval . --case maintainability-inventario-pergunta`: pendente de crédito.

## Fora do escopo

Critérios de Java, Node, Go, PHP e Python. Cada um entra como `stacks/<linguagem>.md`, sem mudar o
núcleo.
