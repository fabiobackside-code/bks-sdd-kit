# Estados e hierarquia — como cada tipo de tela organiza o peso

A hierarquia nasce de uma pergunta: o que o usuário veio fazer aqui? A resposta ganha destaque, e
cada elemento a mais tem que justificar o espaço que ocupa.

## Padrões por tipo de tela

| Tela | O que tem mais peso | O que recua |
|---|---|---|
| listagem | o dado que identifica a linha e o que muda a decisão (status, valor) | ID técnico, datas de auditoria |
| detalhe | o estado atual do objeto e a próxima ação possível | histórico, metadado |
| formulário | o campo atual e o erro dele | ajuda, campo opcional |
| dashboard | o número que pede ação hoje | tendência longa, comparativos |

## Uma listagem, do topo para baixo

Exemplo: listagem de pedidos com filtro por período e status, tabela e paginação.

1. **Título e contagem** — "Pedidos · 1.284". A contagem responde a primeira pergunta.
2. **Filtros** numa faixa só, compactos, com o estado ativo visível. Um "Limpar filtros" aparece
   só quando há filtro aplicado.
3. **Tabela** — a primeira coluna identifica o pedido e tem o maior peso tipográfico. Status é um
   selo com texto e cor. Valor alinha à direita com algarismos tabulares. Data de criação fica em
   texto secundário.
4. **Paginação** discreta, abaixo, com "1–50 de 1.284" e os controles de página.

A ação primária da tela, como "Novo pedido", é o único botão preenchido. Ações por linha ficam
num menu ou aparecem no foco e no hover. Uma coluna inteira de botões compete com o dado.

## Os estados, modelados no tipo

Uma união discriminada obriga o componente a tratar cada estado. Esquecer um vira erro de
compilação, e não um bug descoberto em produção.

```tsx
type OrderListState =
  | { kind: "loading" }
  | { kind: "error"; message: string }
  | { kind: "empty" }
  | { kind: "no-match"; activeFilters: OrderFilters }
  | { kind: "ready"; page: Page<OrderRow> };

export function OrderListBody({ state, onRetry, onClearFilters }: OrderListBodyProps) {
  switch (state.kind) {
    case "loading":
      return <OrderTableSkeleton rows={8} />;
    case "error":
      return <ErrorPanel message={state.message} onRetry={onRetry} />;
    case "empty":
      return <EmptyOrders />;
    case "no-match":
      return <NoMatch filters={state.activeFilters} onClear={onClearFilters} />;
    case "ready":
      return <OrderTable page={state.page} />;
  }
}
```

A derivação do estado fica fora da apresentação:

```tsx
export function toOrderListState(query: OrderQueryResult, filters: OrderFilters): OrderListState {
  if (query.isPending) return { kind: "loading" };
  if (query.error) return { kind: "error", message: describeError(query.error) };
  if (query.data.total > 0) return { kind: "ready", page: query.data };
  if (hasActiveFilters(filters)) return { kind: "no-match", activeFilters: filters };
  return { kind: "empty" };
}
```

## O que cada estado diz

**Carregando.** Esqueleto com o mesmo número de colunas e altura de linha da tabela real. O
cabeçalho e os filtros continuam visíveis e utilizáveis. Spinner centralizado numa área vazia faz
a página pular quando o dado chega.

**Vazio de verdade.** "Nenhum pedido ainda. Os pedidos aparecem aqui quando um cliente finaliza a
compra." Se o usuário pode criar, o botão está ali.

**Sem correspondência.** "Nenhum pedido entre 01/10 e 15/10 com status Cancelado." Os filtros
continuam aplicados e há um botão "Limpar filtros". Mostrar o texto do vazio de verdade aqui
induz o usuário a achar que não há pedido nenhum.

**Erro.** "Não foi possível carregar os pedidos. Tente de novo." O botão refaz a mesma consulta,
com os mesmos filtros. Código técnico, se ajudar o suporte, vai em texto secundário. Stack trace
nunca aparece.

**Atualizando com dado já na tela.** Ao trocar de página ou de filtro, a tabela antiga continua
visível com opacidade reduzida e um indicador discreto. Voltar ao esqueleto a cada clique cansa.

## CSS da tabela, consumindo tokens

```css
.order-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
  color: var(--color-text);
}

.order-table th {
  text-align: left;
  font-weight: 500;
  color: var(--color-text-muted);
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.order-table td {
  padding: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.order-table .order-id {
  font-weight: 600;
}

.order-table .amount {
  text-align: right;
  font-variant-numeric: var(--font-numeric);
}

.order-table .created-at {
  color: var(--color-text-subtle);
}
```

Nenhum valor literal de cor ou espaço. Se a tela precisa de um valor que não existe, o token é
criado antes, no arquivo de tokens.
