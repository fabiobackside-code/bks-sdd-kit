---
description: Fecha a sessao. Roteia decisoes para decisions/, specs para specs/, atualiza o STATUS.md e acrescenta o marco no JOURNAL.md.
---

Feche a sessao registrando o que ela produziu. Rode com a sessao aberta na raiz do repositorio do
projeto.

Se nao houver `STATUS.md` na raiz, pergunte se e para criar a partir do template antes de seguir.

## O que vai para onde

| O que a sessao produziu | Destino |
|---|---|
| Decisao de arquitetura, stack ou contrato | `decisions/ADR-NNN.md` |
| Spec nova ou alterada | `specs/features/`, `specs/tests/`, `specs/tasks/` |
| Onde o projeto parou | `STATUS.md` — reescrito |
| Marco da sessao | `JOURNAL.md` — acrescentado no topo |
| Entregavel gerado | `outputs/` |
| Conhecimento de dominio que surgiu | `brain/domain/` |
| Padrao tecnico que se firmou | `brain/engineering/` |

Decisao sobre o **processo de trabalho** — nao sobre este projeto — vai para
`${BKS_VAULT}/workbench/decisions/`. E raro; na duvida, e do projeto.

## Regras

**Registre so o que foi verificado.** Se um teste rodou, cole a linha que comprova. Se nao rodou,
escreva que nao rodou. Nunca escreva que algo funciona porque parecia funcionar.

**O `STATUS.md` e reescrito, nao acrescentado.** Ele diz onde o projeto esta agora. Estado antigo
nao se acumula ali — vai para o `JOURNAL.md`.

**O `JOURNAL.md` e acrescentado, nunca reescrito.** Entrada nova no topo, com a data em ISO.
Sessao que nao produziu nada nao vira entrada — nao invente marco para justificar a sessao.

**ADR so para decisao fechada.** Discussao em aberto fica no `STATUS.md`, na secao do que trava.
Um ADR que registra hesitacao polui o log de decisoes.

## Passos

1. **Levante o que mudou.** `git status` e `git diff --stat`, mais o que a sessao decidiu sem
   tocar em arquivo. Se nao houver repositorio git, pergunte ao usuario o que considerar.

2. **Classifique** cada item pela tabela acima. Item que nao se encaixa: pergunte, nao invente
   destino.

3. **Escreva os arquivos.** ADR numerado em sequencia a partir do maior existente. Spec no formato
   do kit. `STATUS.md` reescrito por inteiro.

4. **Acrescente ao `JOURNAL.md`** uma entrada: data, titulo curto do marco, duas a quatro linhas
   do que mudou e do que isso libera ou trava.

5. **Confirme em ate cinco linhas** o que foi gravado e onde. Uma linha por arquivo. Nao repita o
   conteudo que acabou de escrever.

Responda em portugues do Brasil.
