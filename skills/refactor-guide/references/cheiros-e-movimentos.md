# Cheiros e movimentos — do sintoma ao passo que o resolve

Um **cheiro** é um sinal no código de que a estrutura atrapalha a mudança. Não é erro, e nem
todo cheiro precisa de tratamento. A pergunta é sempre: este cheiro está atrapalhando a mudança
que preciso fazer agora?

Os nomes dos movimentos seguem o catálogo de *Refactoring*, 2ª edição, para que o commit e a
conversa usem o mesmo vocabulário.

## Método longo → Extract Function

O sinal mais claro é o comentário que separa etapas dentro do método. Cada etapa vira uma função
com o nome que o comentário tentava dar.

Antes:

```csharp
public decimal CalculateTotal(Order order)
{
    // soma itens
    var subtotal = 0m;
    foreach (var item in order.Items)
    {
        if (item.Quantity > 10)
            subtotal += item.Price * item.Quantity * 0.95m;
        else
            subtotal += item.Price * item.Quantity;
    }

    // frete
    var shipping = subtotal > 500m ? 0m : 25m;

    return subtotal + shipping;
}
```

Depois:

```csharp
public decimal CalculateTotal(Order order)
{
    var subtotal = SumItems(order.Items);
    return subtotal + ShippingFor(subtotal);
}

private static decimal SumItems(IEnumerable<OrderItem> items) => items.Sum(LineTotal);

private static decimal LineTotal(OrderItem item)
{
    var gross = item.Price * item.Quantity;
    return item.Quantity > BulkThreshold ? gross * BulkFactor : gross;
}

private static decimal ShippingFor(decimal subtotal) => subtotal > FreeShippingFloor ? 0m : FlatShipping;
```

O comportamento é o mesmo, inclusive o `> 10`. Se a regra deveria ser `>= 10`, isso é mudança de
comportamento e vai noutro commit. As constantes nomeadas entram num passo próprio,
`Replace Magic Literal`, antes ou depois da extração, mas não junto.

## Duplicação → Extract Function e Parameterize Function

Dois blocos quase iguais. Primeiro, torne-os idênticos com movimentos pequenos, como renomear
variável e reordenar linha sem efeito. Depois extraia. A diferença que sobra vira parâmetro.

Cuidado com duplicação acidental: dois trechos iguais hoje que mudam por motivos diferentes.
Juntá-los cria acoplamento que vai doer na próxima mudança de um dos dois.

## Classe que faz demais → Extract Class

Agrupe métodos pelos campos que eles usam. Um grupo que usa só três dos dez campos é uma classe
esperando para sair.

1. Crie a classe nova vazia e faça a antiga ter uma instância dela.
2. Mova um campo por vez com **Move Field**, rodando os testes.
3. Mova os métodos que usam esse campo com **Move Function**.
4. Ajuste os chamadores para falarem com a classe nova diretamente, se fizer sentido.

## Acoplamento à infraestrutura → introduzir porta

A regra de negócio chama banco, HTTP ou fila no meio do cálculo. No padrão BKS a saída é uma porta
em `Ports/Outbound/`, implementada por um adapter. O passo a passo está em `destino-bks.md`,
nesta mesma pasta.

## Obsessão por primitivo → Replace Primitive with Object

`decimal amount` e `string currency` andando juntos por dez métodos pedem um `Money`. Mas só se
houver invariante: moeda obrigatória, soma só entre a mesma moeda, arredondamento de duas casas.
Embrulhar todo primitivo sem invariante é cerimônia.

```csharp
public readonly record struct Money(decimal Amount, string Currency)
{
    public Money Add(Money other) =>
        other.Currency == Currency
            ? this with { Amount = Amount + other.Amount }
            : throw new InvalidOperationException("Moedas diferentes.");
}
```

A exceção aqui protege invariante de programação, não regra de negócio. Erro que o usuário pode
causar continua voltando como resultado tipado.

## Condicional em cascata → Replace Conditional with Polymorphism

O mesmo `switch` por tipo aparece em três métodos. Cada caso vira uma implementação de uma
interface, ou uma entrada num dicionário de estratégias. Um `switch` único, num lugar só, não é
cheiro: pode ficar.

## Lista longa de parâmetros → Introduce Parameter Object

Cinco parâmetros que viajam juntos viram um `record`. No padrão BKS, o contexto da execução já
viaja na transação; não crie um segundo objeto para carregar `CorrelationId` e `UserId`.

## Inveja de funcionalidade → Move Function

Um método que usa mais dados de outra classe do que da própria mora no lugar errado. Mova-o para
perto dos dados. É o Tell, Don't Ask do Calisthenics visto pelo outro lado.

## Ordem de ataque quando há muitos cheiros

1. O cheiro que bloqueia a mudança que você precisa fazer agora.
2. Os que tornam o código difícil de testar, porque destravam os outros.
3. Os que só incomodam. Esses podem esperar a próxima vez que alguém passar por ali.

Refatorar o arquivo inteiro de uma vez gera um diff que ninguém revisa direito.
