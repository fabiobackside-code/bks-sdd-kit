# prj-bks-kit (categoria: backside)

O `bks-sdd-kit`: skills, comandos, agentes, perfis, guardas e templates do método SDD, empacotados
como plugin do Claude Code.

## O projeto é autossuficiente

Tudo que uma sessão precisa está neste repositório. Nenhum comando lê o vault para funcionar.

## Boot da sessão — carregar nesta ordem

| # | Arquivo | Para que |
|---|---|---|
| 1 | `./STATUS.md` | onde o projeto parou, o que trava, próximo passo |
| 2 | `./WORKFLOW.md` | o ciclo mudar → provar → medir |
| 3 | `./docs/ARCHITECTURE.md` | as decisões estruturais e o porquê de cada uma |

O perfil do usuário vive no vault (`workbench/profile.md`) e é carregado pelo ambiente, não por
este arquivo.

## Este repositório é a origem, não o que executa

As skills rodam da cópia em `~/.claude/plugins/cache/bks-sdd-kit/bks/<versão>/`;
`${CLAUDE_PLUGIN_ROOT}` aponta para lá. Editar aqui não muda o comportamento da sessão até o
plugin ser reinstalado ou atualizado.

## Onde cada coisa está

| O que | Onde |
|---|---|
| Skills | `./skills/<nome>/SKILL.md` + `references/` |
| Slash commands | `./commands/` |
| Subagentes | `./agents/` |
| Guardas executáveis | `./hooks/` — cada um com teste em `hooks/tests/` |
| Perfis de projeto | `./profiles/` |
| Esqueleto de projeto novo | `./templates/project-skeleton/` |
| Casos de eval | `./evals/<caso>/case.yaml` |
| Decisões estruturais | `./docs/ARCHITECTURE.md` |
| Decisões pontuais | `./decisions/ADR-NNN.md` |

## Antes de fechar qualquer mudança

`python tests/test_structure.py` — o arquivo continua íntegro. Roda em segundos, sem custo.

Mudança de comportamento de skill pede também `claude plugin eval .`, que custa crédito. O número
que importa não é o score: é o **delta** entre o braço `with` e o `without`.

## Regras que este kit impõe a si mesmo

As mesmas que ele impõe aos projetos que o consomem — um kit que não segue o próprio padrão não
tem autoridade para exigi-lo:

- Guarda sem teste é intenção. Todo hook tem teste em `hooks/tests/`.
- Decisão, trade-off e histórico vão para `docs/ARCHITECTURE.md`, nunca para comentário de código.
- Teto de cinco linhas por bloco de comentário; sem marca de severidade.
- Regra que só uma ferramenta externa conhece precisa de guarda deste lado — senão a próxima
  mudança dela passa despercebida.

## Idioma

Documentação e artefatos em português do Brasil. Código, nomes de tipo, método e variável em
inglês.
