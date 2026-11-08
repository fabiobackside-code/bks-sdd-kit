# Sequência e commits — o plano antes do primeiro movimento

Uma refatoração boa se lê no histórico. Cada commit tem um movimento, o build passa em todos, e o
revisor entende o PR lendo as mensagens em ordem.

## O plano que se mostra ao usuário

Para um pedido como "quebra esse método de 200 linhas, corrige o bug do arredondamento e troca a
lista por dicionário", o plano tem esta forma:

| # | Natureza | Mudança | Prova |
|---|---|---|---|
| 1 | teste | caracterização do método atual, com o arredondamento errado fixado | testes verdes contra o código intocado |
| 2 | estrutura | extrai as etapas em funções nomeadas, uma por commit | os mesmos testes, sem ajuste |
| 3 | estrutura | renomeia variáveis e introduz constantes nomeadas | os mesmos testes |
| 4 | comportamento | corrige o arredondamento para meio para cima | o teste do caso muda de 6,66 para 6,67 no mesmo commit |
| 5 | desempenho | troca lista por dicionário, se a medição justificar | benchmark antes e depois no PR |

Antes de começar, pergunte duas coisas:

- **Qual é a regra certa do arredondamento?** Meio para cima, meio para par (o padrão do
  `Math.Round` no .NET) ou truncamento? A correção depende disso, e o teste também.
- **Há medição mostrando que a lista é gargalo?** Qual o volume típico? Sem resposta, o passo 5
  vira tarefa separada: medir primeiro.

## A mensagem do commit diz o movimento

```
test: caracteriza OrderCalculator.CalculateTotal antes da refatoração
refactor: extrai SumItems de CalculateTotal
refactor: extrai ShippingFor de CalculateTotal
refactor: nomeia limites de quantidade e frete
fix: arredonda total para duas casas, meio para cima
perf: indexa itens por SKU para busca em O(1)
```

O prefixo segue Conventional Commits. `refactor:` promete que o comportamento não mudou. Um
`refactor:` que altera saída quebra essa promessa, e quem faz `git bisect` depois paga o preço.

## Tamanho do passo

Pequeno o bastante para que, se os testes ficarem vermelhos, a causa seja óbvia. Na prática:

- uma extração por commit em código sem teste;
- algumas extrações relacionadas por commit quando a rede é boa e a ferramenta fez o trabalho;
- nunca uma extração e uma correção juntas.

Ficou vermelho? `git restore` do arquivo e refaça em passo menor. Depurar em cima de uma mudança
grande custa mais que refazê-la.

## Um PR ou vários

| Situação | Divisão |
|---|---|
| caracterização e estrutura, diff até umas 400 linhas | um PR, commits separados |
| estrutura e correção de bug | dois PRs; a correção revisada isolada, com o teste que mudou |
| otimização | PR próprio, com o benchmark na descrição |
| refatoração que atravessa vários módulos | um PR por módulo, na ordem das dependências |

A correção de bug num PR próprio tem uma vantagem extra: dá para reverter sem desfazer a
refatoração.

## Medir desempenho

Com BenchmarkDotNet, num projeto de benchmark fora da solution de produção:

```csharp
[MemoryDiagnoser]
public class ItemLookupBenchmark
{
    [Params(5, 50, 5_000)]
    public int ItemCount { get; set; }

    private List<OrderItem> _list = [];
    private Dictionary<string, OrderItem> _bySku = [];
    private string _target = string.Empty;

    [GlobalSetup]
    public void Setup()
    {
        _list = OrderItemFactory.Create(ItemCount);
        _bySku = _list.ToDictionary(item => item.Sku);
        _target = _list[^1].Sku;
    }

    [Benchmark(Baseline = true)]
    public OrderItem? FromList() => _list.Find(item => item.Sku == _target);

    [Benchmark]
    public OrderItem? FromDictionary() => _bySku.GetValueOrDefault(_target);
}
```

Os parâmetros cobrem o volume real e os extremos. Se o volume típico é de cinco itens, a diferença
costuma ser de nanossegundos, e o custo de montar o dicionário pode superá-la. O resultado entra no
PR como tabela, com a máquina e a versão do runtime.

Adicionar o pacote BenchmarkDotNet é dependência nova: confirme com o usuário antes.

## Quando parar

A refatoração termina quando a mudança que motivou o trabalho fica fácil de fazer. Seguir
limpando além disso é outro trabalho, com outro pedido.
