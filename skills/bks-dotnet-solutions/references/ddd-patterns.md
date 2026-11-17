# Padrões DDD Tático

Use estes padrões quando a complexidade do domínio for **Rica**.

## Aggregate Root

```csharp
// Entities são classes, nunca records
public class Pedido : AggregateRoot
{
    public PedidoId Id { get; private set; }
    public ClienteId ClienteId { get; private set; }
    public PedidoStatus Status { get; private set; }
    private readonly List<ItemPedido> _itens = [];

    private Pedido() { } // para ORM

    // Factory method — construção controlada
    public static Pedido Criar(ClienteId clienteId) => new()
    {
        Id = PedidoId.Novo(),
        ClienteId = clienteId,
        Status = PedidoStatus.Rascunho
    };

    public void AdicionarItem(ItemPedido item)
    {
        if (Status != PedidoStatus.Rascunho)
            throw new DomainException("Pedido não pode ser alterado após confirmação");
        _itens.Add(item);
    }

    public void Confirmar()
    {
        if (!_itens.Any())
            throw new DomainException("Pedido sem itens não pode ser confirmado");
        Status = PedidoStatus.Confirmado;
        AddDomainEvent(new PedidoConfirmado(Id, ClienteId));
    }
}
```

**Regras:**
- Setters sempre `private`
- Constructor privado para ORM
- Factory method estático para criação controlada
- Métodos de comportamento encapsulam regras
- Domain Events nomeados no passado, disparados via `AddDomainEvent` após mudança de estado

## Value Objects

```csharp
// ≤ 16 bytes → readonly record struct
public readonly record struct PedidoId(Guid Value)
{
    public static PedidoId Novo() => new(Guid.NewGuid());
}

// > 16 bytes → record class
public sealed record Endereco(
    string Logradouro,
    string Numero,
    string CEP,
    string Cidade,
    string UF);
```

## Domain Events

```csharp
// Nomeados no passado, imutáveis
public sealed record PedidoConfirmado(PedidoId PedidoId, ClienteId ClienteId)
    : IDomainEvent
{
    public DateTime OcorridoEm { get; } = DateTime.UtcNow;
}
```

## Quem chama a regra do aggregate

O aggregate guarda a regra (`Pedido.Criar`, `pedido.Cancelar`); quem o chama depende da forma do
projeto, declarada na fase 2 da entrevista:

| Forma | Quem chama | Onde |
|---|---|---|
| Padrão direto | `{Entidade}Service`, implementação de `I{Entidade}Service` | `Domain/Services/` |
| TXC (Transaction Context) | `ApplyRule` do executor transacional | `Application/{Contexto}/{Operacao}/` |

Nos dois, quem chama não repete a regra: lê o que ela precisa, entrega ao aggregate e grava o
resultado pela Port. Não há `I{Entidade}Handler` nem orquestrador.

## Repositório (Port no Domain)

```csharp
// Interface definida no Domain/Core — sem nenhuma dependência de framework
public interface IPedidoRepository
{
    ValueTask<Pedido?> GetByIdAsync(PedidoId id, CancellationToken ct);
    ValueTask<IReadOnlyList<Pedido>> GetAllAsync(CancellationToken ct);
    ValueTask AddAsync(Pedido pedido, CancellationToken ct);
    ValueTask UpdateAsync(Pedido pedido, CancellationToken ct);
    ValueTask DeleteAsync(PedidoId id, CancellationToken ct);
}
```
