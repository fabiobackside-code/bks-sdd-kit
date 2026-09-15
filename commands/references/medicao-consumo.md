# Medicao de consumo

> Chamado pelo `/bks:save` no passo final. Depende de `scripts/session_cost.py`, que o kit versiona.
> Se o Python ou o script nao estiverem disponiveis, informe em uma linha e siga - a falha da
> medicao nunca bloqueia o `/bks:save`.

## Onde esta o script

O script vive em `${CLAUDE_PLUGIN_ROOT}/scripts/session_cost.py` e le o `pricing.json` ao lado
dele. Nao ha copia fora do plugin: a instalacao em `~/.claude/scripts/` foi removida em 2026-09-15.

Se o script nao existir, ou o Python nao estiver disponivel, escreva "medicao pulada:
session_cost.py nao encontrado" e encerre o `/bks:save` normalmente. Nao instale nada, nao peca para
instalar.

Depois de gravar tudo acima, meca o consumo desta sessao e mostre ao usuario.

**Passo 1 — localizar o ledger.** O ledger e `{repo do projeto}/.logs/cost-ledger.jsonl`. Se a
sessao nao estiver dentro de um repositorio de projeto, use
`${BKS_VAULT}/workbench/.logs/cost-ledger.jsonl`.

**Passo 2 — determinar a fase.** Use o rotulo da fase bks-sdd em que a sessao trabalhou (ex.:
`Fase 5.1 — Feature Spec`, `Fase 6 — Implementacao`). Fora de um fluxo bks-sdd, use um rotulo
curto do trabalho feito (ex.: `manutencao`, `spike`).

**Passo 3 — executar** (Bash, uma linha):

```bash
python "<script localizado acima>" append \
  --ledger "<caminho do passo 1>" \
  --phase "<rotulo do passo 2>" \
  --label "<resumo de 3-6 palavras do que a sessao fez>"
```

**Passo 4 — exibir.** Reproduza a saida do script na integra (a tabela markdown ja vem pronta).
Acrescente uma linha final com o acumulado do processo:

```bash
python "<script localizado acima>" report --ledger "<mesmo caminho>"
```

Do relatorio acumulado, mostre apenas a linha **TOTAL GERAL** — o detalhamento completo fica para
o fechamento do bks-sdd (`--cost-report`).

**Passo 5 — painel `custo-tokens.md`.** Alem do ledger JSONL (o registro fino, por checkpoint),
atualize o arquivo que o Dataview le direto (`FROM "" WHERE tipo = "custo-tokens"`, sem caminho
fixo).

- **Onde:** `{repo do projeto}/.logs/custo-tokens.md` — por projeto. Cada projeto tem o seu; um
  arquivo unico e compartilhado seria sobrescrito quando dois projetos rodassem `/bks:save` no mesmo
  dia.
- **Se nao existir:** crie com frontmatter e uma tabela de checkpoints:
  ```
  ---
  tipo: custo-tokens
  workspace: {nome do projeto/repo}
  acumulado_usd: {custo deste checkpoint, numero puro}
  checkpoints: 1
  ultima_atualizacao: YYYY-MM-DD
  ---

  | Data/hora | Fase | Custo do checkpoint | Acumulado |
  |---|---|---|---|
  | {timestamp} | {rotulo do passo 2} | {custo} | {acumulado_usd} |
  ```
- **Se ja existir:** acrescente uma linha na tabela e atualize o frontmatter (`acumulado_usd` soma
  o novo checkpoint, `checkpoints` incrementa, `ultima_atualizacao` vira hoje). Nunca recrie do
  zero — isso apagaria o historico do projeto.
- Extraia o custo do checkpoint e o acumulado do que o `session_cost.py` ja reportou nos passos 3
  e 4 — nao recalcule por fora do script.

**Passo 6 — registrar no `JOURNAL.md`.** Acrescente a tabela do passo 4 a entrada da sessao, sob o
subtitulo `### Consumo da sessao`, junto com o acumulado do processo. Se a entrada do dia ja tiver
essa secao (segundo `/bks:save` no mesmo dia), **substitua** a tabela em vez de acrescentar outra — o
snapshot e cumulativo, duas tabelas confundiriam.

**Passo 7 — sintese de modelos.** Se o relatorio trouxe a tabela de subagentes, reproduza-a na
entrada do `JOURNAL.md`, sob o subtitulo `### Modelos usados`, junto com uma linha do que os
agentes fizeram nesta sessao. Sem subagente na sessao, pule sem comentar.

A tabela responde onde cada tier foi gasto. Ela existe para calibrar a escolha do modelo com dado,
nao com opiniao: agente que consome muito e entrega pouco e candidato a baixar de tier; agente
barato que gera retrabalho e candidato a subir. Ver `docs/ARCHITECTURE.md`.

Dois limites a respeitar ao ler:

- O tier vem do que o agente **declara**, nao do que a plataforma reportou — a notificacao de
  conclusao traz tokens, nao modelo.
- Os tokens do subagente **nao entram no custo** da tabela principal, que so ve o thread da
  sessao. Somar os dois por fora seria inventar preco para token cujo tier e inferido.

**Se o script ou o passo 5 falharem** (Python ausente, transcript nao encontrado, `custo-tokens.md`
ilegivel): informe o erro em uma linha e siga — a falha da medicao nunca bloqueia o `/bks:save`.

**Nunca** afirme que o valor e a fatura real. E estimativa por token contra a tabela local
`pricing.json`, ao lado do script.
