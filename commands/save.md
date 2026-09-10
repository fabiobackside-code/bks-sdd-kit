---
description: Fecha a sessão. Roteia decisões para decisions/, specs para specs/, atualiza o STATUS.md e acrescenta o marco no JOURNAL.md.
---

Feche a sessão registrando o que ela produziu. Rode com a sessão aberta na raiz do repositório do
projeto.

Se não houver `STATUS.md` na raiz, pergunte se é para criar a partir do template antes de seguir.

## O que vai para onde

| O que a sessão produziu | Destino |
|---|---|
| Decisão de arquitetura, stack ou contrato | `decisions/ADR-NNN.md` |
| Spec nova ou alterada | `specs/features/`, `specs/tests/`, `specs/tasks/` |
| Onde o projeto parou | `STATUS.md` — reescrito |
| Marco da sessão | `JOURNAL.md` — acrescentado no topo |
| Entregável gerado | `outputs/` |
| Conhecimento de domínio que surgiu | `brain/domain/` |
| Padrão técnico que se firmou | `brain/engineering/` |

Decisão sobre o **processo de trabalho** — não sobre este projeto — vai para
`${BKS_VAULT}/workbench/decisions/`. É raro; na dúvida, é do projeto.

## Regras

**Registre só o que foi verificado.** Se um teste rodou, cole a linha que comprova. Se não rodou,
escreva que não rodou. Nunca escreva que algo funciona porque parecia funcionar.

**O `STATUS.md` é reescrito, não acrescentado.** Ele diz onde o projeto está agora. Estado antigo
não se acumula ali — vai para o `JOURNAL.md`.

**O `JOURNAL.md` é acrescentado, nunca reescrito.** Entrada nova no topo, com a data em ISO.
Sessão que não produziu nada não vira entrada — não invente marco para justificar a sessão.

**ADR só para decisão fechada.** Discussão em aberto fica no `STATUS.md`, na seção do que trava.
Um ADR que registra hesitação polui o log de decisões.

## Passos

1. **Levante o que mudou.** `git status` e `git diff --stat`, mais o que a sessão decidiu sem
   tocar em arquivo. Se não houver repositório git, pergunte ao usuário o que considerar.

2. **Classifique** cada item pela tabela acima. Item que não se encaixa: pergunte, não invente
   destino.

3. **Escreva os arquivos.** ADR numerado em sequência a partir do maior existente. Spec no formato
   do kit. `STATUS.md` reescrito por inteiro.

4. **Acrescente ao `JOURNAL.md`** uma entrada: data, título curto do marco, duas a quatro linhas
   do que mudou e do que isso libera ou trava.

5. **Confirme em até cinco linhas** o que foi gravado e onde. Uma linha por arquivo. Não repita o
   conteúdo que acabou de escrever.

Responda em português do Brasil.
