# Autorização por objeto — IDOR, BOLA e isolamento de tenant

Autenticar diz quem chama. Autorizar diz se quem chama pode fazer isto com este recurso. A falha
desta referência é a segunda pergunta não ser feita: o endpoint exige login e entrega o recurso de
qualquer um a qualquer logado.

O nome muda conforme a fonte: IDOR (Insecure Direct Object Reference), BOLA no OWASP API Security
Top 10 (API1:2023), Broken Access Control no OWASP Top 10 (A01:2021), CWE-639 e CWE-862. O defeito
é o mesmo.

## Como reconhecer

O sinal é um identificador vindo da requisição chegar à consulta sem nenhuma condição que envolva
quem chama:

```csharp
var order = await _repo.GetByIdAsync(orderId);
```

```sql
SELECT * FROM orders WHERE id = @id
```

Procure também as variações menos óbvias:

- **identidade vinda do cliente**: `?customerId=`, `{userId}` na rota ou `ownerId` no corpo usados
  como filtro, em vez da claim do token;
- **sub-recurso**: `/orders/{orderId}/items/{itemId}` confere o pedido e busca o item só pelo
  `itemId`, que pode ser de outro pedido;
- **escrita**: `PUT` e `DELETE` com o mesmo defeito do `GET`, de impacto maior;
- **listagem e relatório**: agregado que esquece o filtro de tenant porque "é só contagem";
- **operação em lote**: lista de identificadores no corpo em que só o primeiro é conferido;
- **arquivo e exportação**: URL de download com identificador sequencial ou previsível.

Guid no lugar de inteiro não corrige nada. Dificulta adivinhar, e o identificador continua vazando
por URL compartilhada, log de acesso, e-mail, histórico do navegador e resposta de outro endpoint.

## A correção no padrão BKS

A identidade entra no adapter inbound, a partir da credencial já validada, e viaja na transaction.
A consulta exige o dono. O use case trata "não encontrado" e "não é seu" como o mesmo resultado.

```csharp
group.MapGet("/{orderId:guid}", async (
    Guid orderId, ClaimsPrincipal user, IGetOrderUseCase useCase,
    HttpContext http, CancellationToken ct) =>
{
    var transaction = new GetOrderTransaction(orderId, user.GetCustomerId(), http.TraceIdentifier);
    var result = await useCase.ExecuteAsync(transaction, ct);
    return result.ToHttp(http, order => TypedResults.Ok(order));
}).RequireAuthorization();
```

A porta de saída não oferece busca sem dono. Quem implementa o próximo endpoint não tem como
esquecer o filtro, porque o método sem ele não existe:

```csharp
public interface IOrderReader
{
    /// <summary>Pedido do cliente informado, ou nulo se não existir ou pertencer a outro.</summary>
    Task<Order?> GetForCustomerAsync(Guid orderId, Guid customerId, CancellationToken ct);
}
```

```sql
SELECT id, customer_id, status, total_amount
FROM orders
WHERE id = @OrderId AND customer_id = @CustomerId
```

No passo de processamento, a ausência vira falha tipada, nunca exceção:

```csharp
var order = await _reader.GetForCustomerAsync(tx.OrderId, tx.CustomerId, ct);
return order is null
    ? PipelineResult<OrderResponse>.Failure(
        new PipelineError(ErrorKind.NotFound, "order-not-found", "Pedido não encontrado."))
    : PipelineResult<OrderResponse>.Success(OrderResponse.From(order));
```

Filtrar na consulta é melhor do que buscar e comparar depois: a linha de outro titular nunca sai do
banco, e não há janela para um `if` esquecido no meio do caminho.

## Por que 404 e não 403

`403` responde "existe, e não é seu". Com isso, o atacante enumera identificadores válidos e depois
ataca cada um por outra via. `404` responde igual para inexistente e para alheio, com o mesmo corpo
e o mesmo `type`.

`403` continua certo para permissão sobre a operação em si, quando a existência do recurso não é
segredo: um operador sem papel de aprovador tentando aprovar um pedido que ele consegue ler.

Mantenha também o tempo de resposta parecido nos dois caminhos. Filtrar na consulta já resolve; o
padrão "busca, depois compara, depois carrega o resto" deixa o caminho alheio mais lento ou mais
rápido que o inexistente.

## Multi-tenant

O mesmo princípio, um nível acima. O `TenantId` vem da credencial, entra na transaction e é
parâmetro obrigatório de toda porta de leitura e escrita, inclusive agregado e relatório.

- Com Dapper, o tenant é argumento do método da porta; nenhuma consulta é escrita sem ele.
- Com EF Core, filtro global de consulta por tenant, e revisão de todo `IgnoreQueryFilters`.
- Com PostgreSQL, row-level security é a defesa em profundidade que pega a consulta esquecida.
- Cache e chave de idempotência são escopados por tenant; senão um tenant lê a resposta do outro.

## Acesso administrativo

Suporte e administração precisam ler recurso de terceiros, e esse é o caminho que mais vaza. A
regra é tornar o acesso explícito:

- rota ou política própria, exigindo permissão nomeada, e não um papel genérico que entra no fluxo
  do cliente com o filtro desligado;
- registro de auditoria imutável de cada leitura: quem, qual recurso, quando, com que motivo;
- nunca um parâmetro de query que desliga o filtro de dono.

## Teste que prova a correção

O teste usa dois titulares reais. Um titular só não exercita o defeito.

```csharp
public sealed class OrderAccessTests(OrdersApiFactory factory) : IClassFixture<OrdersApiFactory>
{
    [Fact]
    public async Task Customer_cannot_read_order_of_another_customer()
    {
        var orderOfB = await factory.SeedOrderAsync(customerId: CustomerIds.B);
        var clientA = factory.CreateClientFor(CustomerIds.A);

        var response = await clientA.GetAsync($"/orders/{orderOfB.Id}");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task Customer_reads_own_order()
    {
        var orderOfA = await factory.SeedOrderAsync(customerId: CustomerIds.A);
        var clientA = factory.CreateClientFor(CustomerIds.A);

        var response = await clientA.GetAsync($"/orders/{orderOfA.Id}");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

A fábrica sobe a API com banco em Testcontainers e emite token de teste por titular. O par de
testes vem junto: só o primeiro passaria também com um endpoint que nega tudo.

Repita o par para cada verbo que recebe identificador, e um teste a mais para cada sub-recurso,
com o item de um pedido de B pedido pela rota do pedido de A.
