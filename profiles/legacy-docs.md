# Perfil `legacy-docs`

Entender um legado. Inventario, arquitetura reconstruida, regras de negocio extraidas — sem
alterar uma linha do codigo existente.

## Gera

- inventario: o que existe, em que linguagem, quanto, em que estado
- arquitetura reconstruida a partir do codigo, nao da documentacao antiga
- regras de negocio extraidas, com o ponto do codigo que as sustenta
- mapa de dependencias: interno, externo, banco, integracao
- modelo de dados como esta, nao como deveria ser
- pontos de risco: codigo morto, dependencia sem suporte, regra duplicada, acoplamento critico
- questoes abertas — o que o codigo nao responde e precisa de alguem

## Nao gera

Codigo. Nao refatora, nao corrige, nao "melhora enquanto documenta". Se o alvo e reescrever, o
perfil e `reengineering`.

## Fases

| Fase | Produz |
|---|---|
| inventario | `outputs/INVENTARIO-{projeto}.md` |
| leitura | `docs/input/` — anotacoes brutas da leitura do codigo |
| dominio | `brain/domain/` — as regras de negocio encontradas |
| arquitetura | `outputs/ARCH-{projeto}-ATUAL.md` — como o sistema e hoje |
| dados | `outputs/DADOS-{projeto}.md` — modelo como esta |
| riscos | `outputs/RISCOS-{projeto}.md` |
| consolidacao | `docs/canonical/CONTEXT.md` |
| fechamento | `STATUS.md`, `JOURNAL.md` |

## Regras

**Documente o que o codigo faz, nao o que deveria fazer.** Onde houver divergencia entre
comentario, documentacao antiga e comportamento, o comportamento vence — e a divergencia vira
questao aberta.

**Toda regra extraida aponta para o codigo.** Arquivo e linha. Regra sem referencia e suposicao, e
suposicao sobre legado custa caro.

**O que o codigo nao explica fica em aberto.** Nao invente a intencao por tras de um `if` que
ninguem entende. Liste, e siga.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | nao | — |
| `rigor` | nao | — |

## Skills

`bks-sdd` · `bks-arch` · `doc-writer` · `debug-assistant` (para entender comportamento obscuro)

## O que perguntar na criacao

1. Onde esta o codigo, e ha acesso a um ambiente que rode?
2. Qual a linguagem e a versao?
3. Ha alguem que conheca o sistema e possa responder duvidas?
4. O objetivo e entender, ou preparar uma reescrita?
5. Ha documentacao anterior? Ela e confiavel?
