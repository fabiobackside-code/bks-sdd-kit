# Perfil `reengineering`

Reescrever um legado. Entende primeiro, decide o alvo, migra com paridade comprovada.

## Gera

Tudo o que `legacy-docs` gera, e mais:

- decisao do alvo: stack, arquitetura, fronteiras
- estrategia de migracao: de uma vez, por fatia, ou lado a lado
- mapa de paridade: cada regra do legado apontando para onde ela vive no novo
- testes de caracterizacao — o comportamento antigo capturado antes de qualquer reescrita
- codigo novo
- plano de corte e de retorno

## Fases

| Fase | Produz |
|---|---|
| **entendimento** | tudo do perfil `legacy-docs` |
| alvo | `decisions/ADR-*.md` — stack, arquitetura, o que sai de escopo |
| estrategia | `outputs/MIGRACAO-{projeto}.md` — como se atravessa |
| caracterizacao | testes que capturam o comportamento atual |
| paridade | `outputs/PARIDADE-{projeto}.md` — regra do legado por destino no novo |
| especificacao | `specs/features/`, `specs/tests/`, `specs/tasks/` |
| arquitetura | `outputs/ARCH-{projeto}.md` — o sistema novo |
| implementacao | `app/` |
| corte | plano de virada e de retorno |
| revisao | independente |
| fechamento | `STATUS.md`, `JOURNAL.md` |

A fase de entendimento nao se pula. Reescrever o que nao se entendeu produz um sistema novo com os
bugs antigos e sem as correcoes que ninguem sabia que existiam.

## Regras

**Teste de caracterizacao antes do codigo novo.** O comportamento atual — inclusive o errado —
precisa estar capturado antes de a reescrita comecar. Sem isso nao ha como provar paridade.

**Comportamento errado que alguem depende continua sendo comportamento.** Ao encontrar um bug no
legado, registre e pergunte: corrigir na migracao muda o contrato de quem consome.

**O mapa de paridade e a evidencia de conclusao.** Regra sem destino no novo e escopo perdido, nao
escopo cortado.

## Eixos

| Eixo | Vale | Padrao |
|---|---|---|
| `output` | sim | `md` |
| `architecture_renderer` | sim | `mermaid` |
| `frontend_target` | sim, se houver interface | `web` |
| `rigor` | sim | `producao` |

## Skills

`bks-sdd` · `bks-standards` · `bks-arch` · `bks-tests` · `refactor-guide` ·
`bks-dotnet-solutions` ou `bks-typescript-solutions` · `security-audit`

## O que perguntar na criacao

1. Onde esta o legado, e ha ambiente que rode?
2. Qual a stack alvo?
3. Migracao de uma vez, por fatia, ou os dois sistemas lado a lado por um periodo?
4. Ha consumidores externos cujo contrato precisa ser preservado?
5. Ha janela de corte, ou a virada e gradual?
6. O que explicitamente **nao** vai ser migrado?
