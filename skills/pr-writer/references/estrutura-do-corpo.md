# Estrutura do corpo — cinco seções, nenhuma de enfeite

Esta estrutura vale quando o projeto não tem template de PR. Cada seção responde uma pergunta do
revisor. Seção sem conteúdo real sai, em vez de ganhar "N/A".

## As seções

### O que muda e por quê

Duas a quatro frases: o problema, a decisão e o efeito para quem usa. É o parágrafo que alguém lê
no `git blame` daqui a um ano.

- Bom: "O desconto progressivo truncava a terceira casa decimal e cobrava um centavo a menos em
  pedidos com taxa fracionária. O cálculo passa a arredondar meio para cima, como a regra
  comercial define."
- Ruim: "Ajustes no cálculo de desconto e melhorias gerais."

### Mudanças

Agrupadas por área, na ordem em que o revisor deve ler. Listar arquivo por arquivo repete o que a
aba de arquivos já mostra.

### Como verificar

Passos executáveis, com o resultado esperado. O revisor copia e roda.

### Risco e rollback

Quem é afetado se der errado, e como desfazer. Reverter o commit basta? Há migration que precisa
de reversão? Há flag para desligar? PR sem risco relevante diz isso em uma frase, com o motivo.

### Fora do escopo

O que o revisor poderia esperar e não está aqui, com o motivo ou o link da issue. Evita o
comentário "e o caso X?" e registra a dívida.

## Exemplo completo

Diff de uma branch com 3 commits, 7 arquivos e 214 linhas alteradas:

```markdown
fix(checkout): arredonda desconto progressivo para duas casas

## O que muda e por quê

O desconto progressivo truncava o valor na segunda casa, e pedidos com taxa
fracionária saíam um centavo mais baratos. O cálculo passa a usar
arredondamento meio para cima, como a regra comercial define. A tabela
`order_discount` ganha a coluna `rounding_mode` para registrar o critério
usado em cada pedido.

## Mudanças

- **Domínio:** `DiscountPolicy` aplica `MidpointRounding.AwayFromZero` no
  valor final.
- **Banco:** migration `20261105_AddRoundingModeToOrderDiscount`, com
  default `away_from_zero` para registros novos e `truncate` para os antigos.
- **API:** `GET /orders/{id}` passa a devolver `discount.roundingMode`. Campo
  novo, sem remoção.
- **Testes:** caracterização do cálculo antigo atualizada para o valor
  corrigido; três casos novos de borda (0,005, 0,015 e taxa de 1/3).

## Como verificar

1. `dotnet test src/Checkout.Tests --filter DiscountPolicy` — 14 testes verdes.
2. Pedido de R$ 10,00 com desconto de 1/3: total de R$ 6,67 (antes, R$ 6,66).
3. Aplicar a migration num banco local e conferir que pedidos antigos ficam
   com `rounding_mode = 'truncate'`.

## Risco e rollback

Pedidos criados após o deploy podem diferir em um centavo dos anteriores, o
que o time financeiro já aprovou. Rollback: reverter o merge e rodar a
migration de reversão; a coluna nova não é lida por outro serviço.

## Fora do escopo

- Recalcular pedidos antigos com o critério novo (#482).
- O mesmo truncamento existe no cálculo de frete; fica para outro PR.
```

Repare no que a descrição faz:

- O título diz o efeito. "Ajuste pequeno" virou migration, campo novo na API e mudança de valor
  cobrado. Tudo isso saiu do diff.
- Os números são do diff e da execução: 14 testes, R$ 6,67, nome da migration.
- O risco tem quem é afetado e como desfazer.

## Descrição curta para PR pequeno de verdade

Um PR que muda uma linha de documentação não precisa de cinco seções:

```markdown
docs(readme): corrige o comando de execução dos testes

O README indicava `dotnet test tests/`, mas o projeto de testes fica em
`src/`. Sem impacto em código.
```

O diff confirma que é pequeno. A palavra do autor, sozinha, não confirma.

## O que não escrever

<!-- bks-escrita: ignorar -->

- Lista de commits copiada do `git log`. O GitHub já mostra.
- Adjetivo sem fato: "robusto", "otimizado", "muito mais limpo".
- Afirmação que o diff não sustenta: "melhora a performance" sem número, "adiciona testes" sem
  teste.
- Narrativa do processo: "primeiro tentei X, depois percebi Y". Isso vai para a conversa ou para
  o ADR, se for decisão.
- Linha de atribuição de ferramenta ou rodapé gerado.
- Segredo, connection string ou dado pessoal, mesmo que estejam no diff.

<!-- /bks-escrita -->

## Revisar uma descrição existente

Quando o usuário pede para melhorar uma descrição já escrita, compare com o diff antes de mexer no
texto:

1. O que está no diff e não está na descrição? Contrato, migration, configuração.
2. O que está na descrição e não está no diff? Teste prometido, arquivo que saiu.
3. Só depois disso, a forma.
