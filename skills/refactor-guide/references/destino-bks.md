# Destino BKS — para onde o código vai quando sai do lugar

Refatorar num projeto BKS tem um destino conhecido: a arquitetura hexagonal com pipeline explícito,
transação como objeto de parâmetro e resultado tipado. A refatoração aproxima o código desse
destino um passo por vez, sem tentar chegar lá num commit só.

## A direção da dependência

```
Adapters (Inbound, Outbound)  →  Application (Use Cases, Steps)  →  Domain
```

Nenhuma seta volta. Para conferir depois de cada movimento:

- o projeto ou a pasta `Domain` não referencia `Microsoft.AspNetCore.*`, `EntityFrameworkCore`,
  `Dapper`, `Npgsql`, `Confluent.Kafka` nem `RabbitMQ.Client`;
- `Application` conhece as portas, não as implementações;
- só o composition root, em `Program.cs` ou na extensão de DI, conhece as duas pontas.

Se o projeto tem teste de arquitetura, ele roda a cada passo junto com os outros.

## Extrair uma porta de uma regra acoplada

Antes, a regra abre conexão no meio do cálculo:

```csharp
public sealed class CreditLimitService
{
    public decimal AvailableLimit(Guid customerId)
    {
        using var connection = new NpgsqlConnection(Settings.ConnectionString);
        var used = connection.ExecuteScalar<decimal>(
            "select coalesce(sum(amount), 0) from open_invoice where customer_id = @customerId",
            new { customerId });
        return CustomerLimit - used;
    }
}
```

Passo 1, com a rede verde: extraia o acesso para um método, sem mudar nada mais.

Passo 2: declare a porta com o que a regra precisa, na linguagem do domínio.

```csharp
public interface IOpenInvoiceReader
{
    Task<decimal> SumOpenAmountAsync(Guid customerId, CancellationToken cancellationToken);
}
```

Passo 3: mova o SQL para um adapter em `Adapters/Outbound/` que implementa a porta.

Passo 4: a regra recebe a porta pelo construtor e o composition root liga a implementação.

```csharp
public sealed class CreditLimitService(IOpenInvoiceReader openInvoices)
{
    public async Task<decimal> AvailableLimitAsync(Guid customerId, CancellationToken cancellationToken)
    {
        var used = await openInvoices.SumOpenAmountAsync(customerId, cancellationToken);
        return CustomerLimit - used;
    }
}
```

São quatro commits. O passo 4 muda a assinatura para assíncrona, o que mexe nos chamadores: é um
movimento próprio, não um detalhe do passo 3.

## Exceção de negócio vira resultado tipado

Código legado costuma lançar exceção para regra de negócio. A troca muda o contrato com quem
chama, então é feita com cuidado:

1. Caracterize o comportamento atual, inclusive a exceção lançada.
2. Introduza o método novo devolvendo `PipelineResult<T>`, ou o resultado que o projeto usa.
3. Faça o método antigo chamar o novo e relançar, para os chamadores não mudarem ainda.
4. Migre os chamadores um por um.
5. Remova o método antigo.

Cada passo é verde. Nenhum chamador quebra no meio do caminho.

## Do serviço gordo ao use case com pipeline

Um serviço de aplicação com validação, cálculo e persistência num método só vira um use case cujo
pipeline tem os passos separados. Os passos de validação, pré-processamento, processamento e
pós-processamento recebem os trechos correspondentes, um por commit. O orquestrador chama os
passos em ordem explícita. Sem MediatR e sem dispatcher, mesmo que o código antigo use um: tirar
o dispatcher é, por si só, uma refatoração com rede própria.

## Calisthenics no refactor

As regras de Object Calisthenics guiam o movimento, mas não justificam classe artificial:

| Regra | Aplicação útil num refactor |
|---|---|
| um nível de indentação | extrair o corpo do laço ou do `if` interno para uma função |
| sem `else` | cláusula de guarda com retorno antecipado |
| Tell, Don't Ask | mover a decisão para o objeto que tem os dados |
| coleção de primeira classe | uma lista com regra própria, como total ou elegibilidade, vira tipo |
| sem abreviação | renomear `calc`, `tmp`, `obj` num commit só de renomeação |

Se aplicar uma regra deixa o código mais difícil de ler, ela não se aplica ali.

## Documentação acompanha

Tipo público movido, renomeado ou criado entra no `ARCHITECTURE.md` na mesma entrega. Comentário
de bloco que explicava a regra antiga não é apagado em silêncio: o que ele dizia de decisão vai
para o `ARCHITECTURE.md`, e no código fica no máximo o resumo de uma linha.
