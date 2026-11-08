# Reprodução — fazer o defeito acontecer sob controle

Um defeito reproduzível está meio resolvido: cada hipótese vira um experimento de segundos. Um
defeito que só se vê no log de produção obriga a adivinhar, e adivinhação não converge.

## O teste que falha primeiro

O formato preferido de reprodução é um teste automatizado que falha pelo mesmo motivo do defeito.
"Pelo mesmo motivo" importa: um teste que falha por erro de montagem não reproduz nada.

Exemplo: `NullReferenceException` no cálculo de frete, e a stack aponta
`ShippingCalculator.Calculate`, linha que lê `order.ShippingAddress.ZipCode`. A hipótese inicial é
que pedido sem endereço chega ao cálculo. O teste escreve a hipótese:

```csharp
public sealed class ShippingCalculatorTests
{
    [Fact]
    public void Store_pickup_order_has_no_shipping_cost()
    {
        var order = OrderBuilder.Default().WithStorePickup().Build();
        var calculator = new ShippingCalculator(new FixedRateTable());

        var result = calculator.Calculate(order);

        Assert.True(result.IsSuccess);
        Assert.Equal(0m, result.Value!.Amount);
    }
}
```

Antes da correção, ele falha com a mesma exceção e o mesmo quadro de stack que a produção mostrou.
Se falhar em outro ponto, a hipótese está errada ou o teste não monta o caso real; ajuste antes de
seguir.

Repare no que o teste afirma: o comportamento esperado, e não "não lança exceção". A correção que
faz o teste passar é a que implementa a regra de retirada na loja; um null check que devolve zero
para qualquer pedido sem endereço também passaria, e por isso o par de testes inclui o pedido de
entrega com endereço ausente, que deve falhar na validação:

```csharp
[Fact]
public void Delivery_order_without_address_is_rejected()
{
    var order = OrderBuilder.Default().WithDelivery().WithoutAddress().Build();
    var calculator = new ShippingCalculator(new FixedRateTable());

    var result = calculator.Calculate(order);

    Assert.False(result.IsSuccess);
    Assert.Equal("shipping-address-required", result.Error!.Code);
}
```

O teste nasce no projeto de testes da solution, em `src/`, junto dos outros.

## Reprodução mínima

Quando a entrada real é grande (um pedido com 80 itens, um arquivo de 40 MB, uma mensagem com
dezenas de campos), reduza até o menor caso que ainda falha:

1. Comece pela entrada real que falha, com dado pessoal substituído.
2. Remova metade do conteúdo. Ainda falha? Fique com a metade menor. Não falha? Volte e remova a
   outra metade.
3. Repita até nada mais poder sair sem o defeito sumir.

O que sobra aponta a causa. Se só falha com um item de quantidade zero, a hipótese já está escrita.

## Código sem teste

Em código legado sem teste, escreva primeiro um **teste de caracterização**: ele registra o que o
código faz hoje, certo ou errado, para a correção não mudar mais do que deveria.

1. Chame o método com entradas representativas e afirme a saída atual, mesmo que pareça estranha.
2. Escreva o teste que reproduz o defeito, falhando.
3. Corrija. Só o teste do defeito muda de resultado; uma caracterização que quebrou indica efeito
   colateral, ou um segundo defeito que alguém dependia.

A mesma técnica serve para entender comportamento obscuro sem bug declarado: o teste vira a
documentação executável do que o código faz.

## Quando só acontece em produção

Não dá para depurar produção passo a passo. Dá para trazer o caso de lá:

- **Busque a entrada pelo traceId**: o log estruturado e o span do pedido que falhou dizem qual
  recurso, qual operação e qual versão. O log não carrega dado pessoal; o identificador permite
  buscar o registro no banco com o acesso apropriado.
- **Monte o caso localmente** com o registro anonimizado, e reproduza no teste.
- **Compare o que difere** do ambiente local, com a tabela de `isolamento.md`.
- **Quando faltar informação**, acrescente log no ponto da dúvida, com o identificador e o estado
  relevante, nunca o dado pessoal, e espere a próxima ocorrência. É uma etapa do diagnóstico, com
  data para sair.
- **Dump de memória** (`dotnet-dump collect`) para travamento, vazamento e deadlock; ele mostra
  as threads e o heap no momento do problema.

## Em Go

O mesmo princípio, no formato da linguagem: teste de tabela com o caso que falha.

```go
func TestCalculateShipping(t *testing.T) {
	cases := []struct {
		name    string
		order   Order
		want    Money
		wantErr error
	}{
		{name: "store pickup", order: pickupOrder(), want: Zero},
		{name: "delivery without address", order: deliveryWithoutAddress(), wantErr: ErrAddressRequired},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := CalculateShipping(tc.order)
			if !errors.Is(err, tc.wantErr) {
				t.Fatalf("err = %v, want %v", err, tc.wantErr)
			}
			if got != tc.want {
				t.Fatalf("got %v, want %v", got, tc.want)
			}
		})
	}
}
```

Panic de ponteiro nulo em Go aparece como `invalid memory address or nil pointer dereference`, e a
stack do panic diz a goroutine e a linha. `go test -run TestCalculateShipping -count=1` evita o
cache de resultado durante a investigação.
