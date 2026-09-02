---
description: Roteia o resultado da sessao pela regra dos dois lugares: ADR e specs no repo do projeto, progresso e nota de sessao no workbench.
---

Roteie as informações da sessão pela regra dos dois lugares:
- Decisão SOBRE ESTE PROJETO (stack, arquitetura) -> decisions/ADR-NNN.md
  (no repo do projeto).
- Decisão SOBRE O WORKBENCH EM SI (raro) -> ${BKS_BRAIN}/decisions/ADR-NNN.md.
- Specs novas/alteradas -> specs/{features,tests,tasks}/ (no repo do projeto).
- Progresso e próximo passo -> ${BKS_BRAIN}/memory/hot.md.
- Entregáveis -> outputs/ (no repo do projeto).
- Nota de sessão -> ${BKS_BRAIN}/sessions/sessao-YYYY-MM-DD.md.
Mostre o que gravou, e em qual lugar, antes de finalizar.

## Medição de consumo (obrigatória, sempre ao final do /save)

Depois de gravar tudo acima, meça o consumo desta sessão e mostre ao usuário.

**Passo 1 — localizar o ledger.** Procure, a partir do diretório de trabalho atual
subindo até 4 níveis, um folder `workspace-*`.

- Se encontrar: o ledger é `<workspace-*>/.logs/cost-ledger.jsonl`.
- Se não encontrar: o ledger é
  `${BKS_BRAIN}/memory/cost-ledger.jsonl` (ledger geral do workbench).

**Passo 2 — determinar a fase.** Use o rótulo da fase BKS-SDD em que a sessão trabalhou
(ex.: `Fase 5.1 — Feature Spec`, `Fase 6 — Implementação`). Se a sessão não faz parte de um
fluxo bks-sdd, use um rótulo curto do trabalho feito (ex.: `manutenção`, `spike`).

**Passo 3 — executar** (Bash, uma linha):

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/session_cost.py" append \
  --ledger "<caminho do passo 1>" \
  --phase "<rótulo do passo 2>" \
  --label "<resumo de 3-6 palavras do que a sessão fez>"
```

**Passo 4 — exibir.** Reproduza a saída do script na íntegra (a tabela markdown já vem pronta).
Acrescente uma linha final com o acumulado do processo:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/session_cost.py" report --ledger "<mesmo caminho>"
```

Do relatório acumulado, mostre apenas a linha **TOTAL GERAL** — o detalhamento completo
fica para o fechamento do bks-sdd (`--cost-report`).

**Passo 5 — painel Dataview do Home.md (`custo-tokens.md`).** Além do ledger JSONL (que é o
registro fino, por checkpoint), atualize também um arquivo que o Dataview do `Home.md` lê
direto — o painel já existe e só precisa de arquivos com este `tipo` em qualquer lugar do
vault (`FROM "" WHERE tipo = "custo-tokens"`, sem caminho fixo).

- **Onde:** `{repo do projeto}/.logs/custo-tokens.md` — **por projeto**, não em
  `brain/_bks-ai/`, pra não colidir quando dois projetos diferentes rodam `/save` no mesmo dia
  (um arquivo só em `brain/_bks-ai/memory/` seria compartilhado e sobrescrito entre eles).
- **Se o arquivo não existir:** crie com frontmatter e uma tabela de checkpoints:
  ```
  ---
  tipo: custo-tokens
  workspace: {nome do projeto/repo}
  acumulado_usd: {custo deste checkpoint, número puro}
  checkpoints: 1
  ultima_atualizacao: YYYY-MM-DD
  ---

  | Data/hora | Fase | Custo do checkpoint | Acumulado |
  |---|---|---|---|
  | {timestamp} | {rótulo do passo 2} | {custo} | {acumulado_usd} |
  ```
- **Se já existir:** acrescente uma linha na tabela e atualize o frontmatter
  (`acumulado_usd` soma o novo checkpoint, `checkpoints` incrementa, `ultima_atualizacao` vira
  hoje). Nunca recrie do zero — isso apagaria o histórico do projeto.
- Extraia o custo do checkpoint e o acumulado do que o `session_cost.py` já reportou nos
  Passos 3 e 4 — não recalcule por fora do script.

**Passo 6 — registrar no Obsidian.** Acrescentar a tabela do passo 4 à nota de sessão
`${BKS_BRAIN}/sessions/sessao-YYYY-MM-DD.md`, sob o cabeçalho
`## Consumo da sessão`, junto com o acumulado do processo. Assim o custo fica no mesmo
lugar onde a sessão já está documentada, e o Obsidian indexa junto.

Se a nota do dia já tiver essa seção (segundo `/save` no mesmo dia), **substituir** a
tabela em vez de acrescentar outra — o snapshot é cumulativo, duas tabelas confundiriam.

**Se o script ou o passo 5 falharem** (Python ausente, transcript não encontrado, arquivo
`custo-tokens.md` ilegível): informe o erro em uma linha e siga — a falha da medição nunca
deve bloquear o `/save`.

**Nunca** afirme que o valor é a fatura real. É estimativa por token contra a tabela local
`~/.claude/scripts/pricing.json`.
