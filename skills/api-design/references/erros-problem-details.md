# Erro em Problem Details e a tradução do PipelineResult

A RFC 9457 define um formato único de erro para HTTP, servido como `application/problem+json`. Ela
substitui a RFC 7807 com o mesmo formato e acrescenta o registro de tipos comuns. Adotar o formato
poupa cada cliente de aprender um envelope próprio, e o ASP.NET Core já o produz nativamente.

## Os campos

| Campo | Conteúdo | Quem decide por ele |
|---|---|---|
| `type` | URI que identifica o tipo do problema; `about:blank` quando o status basta | o código do cliente |
| `title` | resumo curto do tipo, igual para toda ocorrência | quem lê o log |
| `status` | o mesmo código da resposta HTTP | ferramenta que só vê o corpo |
| `detail` | explicação desta ocorrência, legível por pessoa | quem lê a tela ou o log |
| `instance` | URI desta ocorrência, em geral o caminho da requisição | suporte |

Extensões entram como membros extras no mesmo objeto. As duas que todo projeto BKS manda são
`code`, igual ao último segmento do `type`, e `traceId`, para achar a requisição na telemetria.

O cliente decide pelo `type` ou pelo `code`, nunca pelo `title` ou pelo `detail`. Texto muda com
tradução e com revisão de redação; o `type` é contrato e só muda com versão nova.

## Exemplos

Transição inválida:

```json
{
  "type": "https://errors.exemplo.com.br/order-not-cancellable",
  "title": "Pedido não pode ser cancelado",
  "status": 409,
  "detail": "O pedido 123 já foi despachado.",
  "instance": "/orders/123/cancellation",
  "code": "order-not-cancellable",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

Validação de entrada, com a lista de campos como extensão:

```json
{
  "type": "https://errors.exemplo.com.br/validation",
  "title": "Entrada inválida",
  "status": 422,
  "instance": "/orders",
  "code": "validation",
  "errors": {
    "items": ["A lista de itens não pode ser vazia."],
    "shippingAddress.zipCode": ["CEP com formato inválido."]
  },
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

## O que nunca entra no erro

Stack trace, mensagem de exceção, nome de tabela ou coluna, SQL, caminho de arquivo do servidor,
versão de biblioteca e qualquer dado do titular que a requisição não trouxe. Tudo isso fica no log
estruturado, correlacionado pelo `traceId`, e o log segue a regra de não carregar senha, token nem
documento pessoal.

## O erro precisa de tipo para virar status

O adapter só escolhe o status certo se o erro disser o que aconteceu. Um `PipelineResult` com erro
em string obriga o adapter a adivinhar pelo texto, e o resultado é tudo virar `422` ou `400`.

O erro tipado vive no domínio e usa só `System.*`:

```csharp
namespace Orders.Domain.Core.Common;

public enum ErrorKind { Validation, NotFound, Conflict, Forbidden, Unexpected }

/// <summary>Falha de negócio devolvida pelo pipeline, com o código estável do contrato.</summary>
public sealed record PipelineError(
    ErrorKind Kind,
    string Code,
    string Message,
    IReadOnlyDictionary<string, string[]>? Fields = null);
```

## A tradução no adapter inbound

Uma extensão só, chamada por todo endpoint. Nenhum endpoint escolhe status de erro por conta
própria.

```csharp
namespace Orders.Adapters.Inbound.Api;

internal static class PipelineResultHttp
{
    private const string TypeBase = "https://errors.exemplo.com.br/";

    /// <summary>Converte o resultado do pipeline em resposta HTTP.</summary>
    public static IResult ToHttp<T>(
        this PipelineResult<T> result, HttpContext http, Func<T, IResult> onSuccess)
        => result.IsSuccess ? onSuccess(result.Value!) : ToProblem(result.Error!, http);

    private static IResult ToProblem(PipelineError error, HttpContext http)
    {
        var status = error.Kind switch
        {
            ErrorKind.Validation => StatusCodes.Status422UnprocessableEntity,
            ErrorKind.NotFound => StatusCodes.Status404NotFound,
            ErrorKind.Conflict => StatusCodes.Status409Conflict,
            ErrorKind.Forbidden => StatusCodes.Status403Forbidden,
            _ => StatusCodes.Status500InternalServerError
        };

        var extensions = new Dictionary<string, object?>
        {
            ["code"] = error.Code,
            ["traceId"] = Activity.Current?.TraceId.ToString() ?? http.TraceIdentifier
        };
        if (error.Fields is not null)
            extensions["errors"] = error.Fields;

        // Falha inesperada não expõe a mensagem interna ao cliente.
        var detail = status == StatusCodes.Status500InternalServerError ? null : error.Message;

        return TypedResults.Problem(
            detail: detail,
            instance: http.Request.Path,
            statusCode: status,
            type: TypeBase + error.Code,
            extensions: extensions);
    }
}
```

O dicionário de extensões é `object?` porque é a assinatura do `TypedResults.Problem`; o valor que
entra nele é sempre `string` ou o mapa de campos.

`ErrorKind.Forbidden` serve para permissão sobre a operação, como um papel que não pode aprovar.
Recurso que existe e pertence a outro titular é `NotFound`: responder `403` confirma que o
identificador existe e permite enumerar recursos alheios.

O endpoint fica com uma linha de tradução:

```csharp
group.MapPost("/{orderId:guid}/cancellation", async (
    Guid orderId, ICancelOrderUseCase useCase, HttpContext http, CancellationToken ct) =>
{
    var transaction = CancelOrderTransaction.Create(http, orderId);
    var result = await useCase.ExecuteAsync(transaction, ct);
    return result.ToHttp(http, order => TypedResults.Ok(order));
});
```

## Exceção não prevista

O que escapa do pipeline é defeito, e sai como `500` em Problem Details sem detalhe interno:

```csharp
builder.Services.AddProblemDetails();

var app = builder.Build();
app.UseExceptionHandler();
app.UseStatusCodePages();
```

Com `AddProblemDetails`, o `UseExceptionHandler` sem argumento e o `UseStatusCodePages` passam a
responder em `application/problem+json`, inclusive para `404` de rota inexistente e `405`. A página
de exceção de desenvolvimento nunca fica ligada fora do ambiente local.

## Teste do contrato de erro

O teste confere status e `type`, que são o contrato. Texto de `detail` não entra na asserção.

```csharp
public sealed class PipelineResultHttpTests
{
    [Fact]
    public void Conflict_maps_to_409_with_stable_type()
    {
        var error = new PipelineError(ErrorKind.Conflict, "order-not-cancellable", "Já despachado.");
        var result = PipelineResult<OrderResponse>.Failure(error);

        var http = result.ToHttp(new DefaultHttpContext(), order => TypedResults.Ok(order));

        var problem = Assert.IsType<ProblemHttpResult>(http);
        Assert.Equal(StatusCodes.Status409Conflict, problem.StatusCode);
        Assert.EndsWith("/order-not-cancellable", problem.ProblemDetails.Type);
    }

    [Fact]
    public void Unexpected_hides_internal_message()
    {
        var error = new PipelineError(ErrorKind.Unexpected, "unexpected", "Timeout no banco X");
        var result = PipelineResult<OrderResponse>.Failure(error);

        var http = result.ToHttp(new DefaultHttpContext(), order => TypedResults.Ok(order));

        var problem = Assert.IsType<ProblemHttpResult>(http);
        Assert.Equal(StatusCodes.Status500InternalServerError, problem.StatusCode);
        Assert.Null(problem.ProblemDetails.Detail);
    }
}
```

Um teste por `ErrorKind` fecha a tabela. O teste de integração do endpoint confere também o
`Content-Type` `application/problem+json`.

## Catálogo de tipos

Cada `type` que a API pode devolver fica listado no contrato, com status e o que o cliente deve
fazer. A tabela é parte da documentação da API, junto do OpenAPI:

| `code` | Status | O que o cliente faz |
|---|---|---|
| `validation` | 422 | corrige os campos listados em `errors` |
| `order-not-found` | 404 | trata como inexistente |
| `order-not-cancellable` | 409 | recarrega o pedido e mostra o estado atual |
| `idempotency-key-reused` | 422 | gera chave nova para a nova intenção |
| `unexpected` | 500 | repete depois, ou abre chamado com o `traceId` |

Código novo no catálogo é mudança compatível quando o cliente tem tratamento padrão para `type`
desconhecido. Mudar o status ou o significado de um código existente é incompatível.
