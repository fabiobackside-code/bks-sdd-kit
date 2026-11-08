# Componentes e layout — uma responsabilidade, qualquer largura

Um componente que busca dado, guarda filtro, formata moeda e desenha a linha da tabela muda por
quatro motivos diferentes. Cada motivo vira um componente, ou uma função, com nome próprio.

## A divisão de uma tela

Para a listagem de pedidos:

```
OrdersPage              rota: lê a URL, monta a consulta, deriva o estado
├── OrderFilters        apresentação: período e status, emite mudança
├── OrderListBody       escolhe o que mostrar pelo estado
│   ├── OrderTable      apresentação: linhas e cabeçalho
│   │   └── OrderStatusBadge
│   ├── OrderTableSkeleton
│   ├── EmptyOrders
│   ├── NoMatch
│   └── ErrorPanel
└── Pagination          apresentação: página atual, total, emite mudança
```

Só a `OrdersPage` conhece a fonte de dados e a URL. Os demais recebem props e emitem eventos, o
que os deixa testáveis sem rede e reaproveitáveis em outra tela.

## Estado que mora na URL

Filtro, página e ordenação são estado de navegação. Ficam na query string:

```tsx
export function useOrderFilters(): [OrderFilters, (next: Partial<OrderFilters>) => void] {
  const [params, setParams] = useSearchParams();
  const filters = parseOrderFilters(params);

  const update = (next: Partial<OrderFilters>) => {
    const merged = { ...filters, ...next, page: next.page ?? 1 };
    setParams(serializeOrderFilters(merged), { replace: true });
  };

  return [filters, update];
}
```

Trocar um filtro volta para a página 1. Sem isso, o usuário filtra estando na página 7 e cai numa
página que não existe mais.

## Formatação fora do componente

```tsx
const currency = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

export const formatAmount = (cents: number): string => currency.format(cents / 100);
```

O formatador é criado uma vez, fora da renderização. O componente chama `formatAmount` e não sabe
de localidade.

## Props que contam a intenção

- Prefira `variant="danger"` a `color="red"`. A prop descreve o papel, e o token decide a cor.
- Evite booleanos que se excluem: `isPrimary` e `isGhost` juntos geram um estado impossível. Uma
  prop `variant` com união de literais não deixa.
- Componente com mais de oito props está fazendo coisa demais. Divida, ou passe filhos por
  composição.

## Responsividade pelo conteúdo

O ponto de quebra fica onde o conteúdo deixa de caber, não na largura de um aparelho específico.
Para uma tabela de seis colunas, a pergunta é: em que largura a terceira coluna começa a quebrar
linha?

Duas saídas honestas para a tabela em tela estreita:

1. **Lista de cartões** — cada linha vira um cartão com o identificador em destaque e dois ou três
   campos. Boa quando o usuário olha um item por vez.
2. **Rolagem horizontal com a primeira coluna fixa** — boa quando o usuário compara linhas. A área
   rolável recebe `tabindex="0"` e um rótulo, para quem usa teclado conseguir rolar.

```css
.order-table-wrapper {
  overflow-x: auto;
}

.order-table th:first-child,
.order-table td:first-child {
  position: sticky;
  left: 0;
  background: var(--color-surface);
}

@media (max-width: 40rem) {
  .order-filters {
    flex-direction: column;
    align-items: stretch;
    gap: var(--space-2);
  }
}
```

Use `rem` nos pontos de quebra: o layout acompanha o tamanho de fonte que o usuário escolheu no
navegador.

## Layout com poucas regras

- `display: grid` para a estrutura da página, `flex` para alinhar itens numa linha.
- `gap` em vez de margem em cada filho.
- Largura máxima de conteúdo em token, como `--content-max: 80rem`, e não repetida em cada tela.
- `min-width: 0` em filho de flex que contém texto longo, para que ele quebre em vez de estourar.

## Testes de componente

Teste o que o usuário percebe, não a estrutura interna. Com Testing Library:

- cada estado renderiza a mensagem certa;
- "Limpar filtros" aparece no estado sem correspondência e chama o callback;
- a tabela expõe cabeçalhos com `scope` e a contagem chega à região `aria-live`.

Busque elementos por papel e nome acessível, como `getByRole("button", { name: "Tentar de novo" })`.
Se o teste não encontra o elemento por papel, o leitor de tela também não encontra.
