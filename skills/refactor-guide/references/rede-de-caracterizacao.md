# Rede de caracterização — fixar o que o código faz hoje

Um **teste de caracterização** registra o comportamento atual do código, certo ou errado. Ele não
pergunta o que o código deveria fazer. Feathers propõe o termo para o momento em que ninguém sabe
mais qual é a regra, só o que o sistema faz em produção.

## Como achar os casos

1. **Leia o método procurando ramos.** Cada `if`, `switch`, `catch` e retorno antecipado é pelo
   menos um caso.
2. **Procure as bordas.** Zero, um, muitos; nulo e vazio; valor negativo; limite de faixa, como
   o valor exato onde o desconto muda.
3. **Use dados de produção, anonimizados**, quando existirem. Eles exercitam combinações que
   ninguém pensaria em escrever.
4. **Escreva o teste com uma expectativa qualquer, rode, e copie o valor real.** O teste falha,
   mostra o que o código devolve, e esse valor vira a expectativa. É o mecanismo central da
   caracterização.

A cobertura de linhas e branches do trecho, medida com coverlet, mostra que ramo ficou sem caso.
O alvo aqui é cobrir o trecho que será mexido, não o projeto inteiro.

## Exemplo em C# com xUnit

Um método de 200 linhas que calcula o total de um pedido, sem teste nenhum:

```csharp
public sealed class OrderTotalCharacterizationTests
{
    private readonly LegacyOrderCalculator _calculator = new(new FixedClock(new DateTime(2026, 3, 10)));

    [Fact]
    public void Total_WithSingleItemAndNoDiscount_ReturnsCurrentValue()
    {
        var order = OrderBuilder.Default().WithItem(price: 100.00m, quantity: 1).Build();

        var total = _calculator.CalculateTotal(order);

        Assert.Equal(100.00m, total);
    }

    [Fact]
    public void Total_WithThirdOfDiscount_KeepsCurrentRounding()
    {
        var order = OrderBuilder.Default().WithItem(price: 10.00m, quantity: 1).WithDiscountRate(1m / 3m).Build();

        var total = _calculator.CalculateTotal(order);

        // Valor atual, com o arredondamento por truncamento; muda no commit da correção.
        Assert.Equal(6.66m, total);
    }

    [Theory]
    [InlineData(0, 0.00)]
    [InlineData(10, 1000.00)]
    [InlineData(11, 1045.00)]
    public void Total_AcrossQuantityBands_ReturnsCurrentValue(int quantity, decimal expected)
    {
        var order = OrderBuilder.Default().WithItem(price: 100.00m, quantity: quantity).Build();

        Assert.Equal(expected, _calculator.CalculateTotal(order));
    }
}
```

O segundo teste fixa o bug de propósito. Quando a correção entrar, o mesmo commit muda a
expectativa para `6.67m`, e o diff do teste mostra ao revisor exatamente o que mudou de
comportamento.

O nome do teste diz o que é fixado. "ReturnsCurrentValue" deixa claro que o valor não foi
validado contra regra nenhuma.

## Saída grande demais para afirmar campo a campo

Quando o método devolve um objeto grande, ou gera um arquivo, compare com uma saída aprovada.
Serialize o resultado com `System.Text.Json`, grave a primeira execução num arquivo de referência
versionado e compare as execuções seguintes com ele:

```csharp
[Fact]
public void Invoice_ForReferenceOrder_MatchesApprovedOutput()
{
    var invoice = _generator.Generate(ReferenceOrders.Mixed());

    var actual = JsonSerializer.Serialize(invoice, ApprovedJson.Options);
    var approved = File.ReadAllText(Path.Combine("Approved", "invoice-mixed.json"));

    Assert.Equal(approved, actual);
}
```

Campos que mudam a cada execução, como data de geração e GUID, são fixados por relógio e gerador
injetados. Removê-los da comparação esconde regressão.

## Quando o código não deixa testar

Feathers chama de **ponto de separação** o lugar onde se troca um comportamento sem editar o
código naquele ponto. Os mais úteis em C#:

| Obstáculo | Separação mínima |
|---|---|
| `DateTime.Now` no meio da regra | injetar `TimeProvider`, nativo desde o .NET 8 |
| `new SqlConnection` dentro do método | extrair o acesso para um método virtual ou uma interface |
| classe estática de terceiro | envolver numa interface fina, com uma implementação que só delega |
| construtor que faz I/O | mover o I/O para um método de fábrica, e o construtor só recebe dados |
| método privado gigante | testar pelo método público que o chama; não abra visibilidade só para o teste |

Essas primeiras mudanças acontecem sem rede. Por isso são as menores possíveis, feitas pela
ferramenta de refatoração da IDE e revisadas linha a linha. Nada de lógica muda nelas.

## Integração, quando a regra mora no banco

Se o comportamento depende de stored procedure ou de consulta, o teste de caracterização sobe o
banco real com Testcontainers, aplica o schema e uma massa conhecida, e afirma o resultado. Mock
de banco caracteriza o mock, não o sistema.

## Quando a rede está pronta

- Todos os testes de caracterização passam contra o código atual, sem alteração nele.
- Cada ramo do trecho que será mexido tem ao menos um caso.
- Os comportamentos suspeitos estão nomeados nos testes e listados para o usuário decidir se são
  bug ou regra.

Só depois disso começa o primeiro movimento de estrutura.
