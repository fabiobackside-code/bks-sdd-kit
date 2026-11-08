# A linha de contrato em cada linguagem

A linha de contrato diz a quem chama o que o membro faz, o que devolve e em que condição falha. Ela
não descreve o algoritmo, não conta a história do código e não repete o nome do método com outras
palavras.

## O que entra na linha

| Entra | Fica fora |
|---|---|
| o efeito visível para quem chama | o passo a passo da implementação |
| o valor devolvido e o que significa vazio ou nulo | a estrutura de dados usada por dentro |
| a exceção ou o erro que o chamador precisa tratar | por que foi feito assim (vai para o `ARCHITECTURE.md`) |
| a unidade, quando o tipo não a carrega | quem pediu e quando mudou |

O teste é perguntar se a linha continua verdadeira depois de um refactor interno que mantém o
comportamento. Se deixa de ser, ela descrevia o como.

## C# — XML doc comment

Uma linha de `<summary>`. As tags `<param>`, `<returns>` e `<exception>` entram só quando dizem algo
que o nome e o tipo não dizem, e o bloco inteiro continua dentro de cinco linhas.

```csharp
/// <summary>Reserva o assento para o passageiro; devolve falha se o voo já partiu.</summary>
public Result<Reservation> Reserve(SeatNumber seat, PassengerId passenger)

/// <summary>Converte centavos em valor monetário com duas casas.</summary>
/// <exception cref="OverflowException">Quando o valor passa do limite de decimal.</exception>
public static decimal FromCents(long cents)
```

Errado, porque parafraseia o nome e explica o como:

```csharp
/// <summary>Método Reserve que reserva. Usa um lock e depois grava no repositório.</summary>
```

## TypeScript — JSDoc

```typescript
/** Devolve o usuário pelo e-mail, ou `undefined` quando não existe. */
export async function findByEmail(email: string): Promise<User | undefined>
```

`@param` e `@returns` repetem o que a assinatura tipada já diz; use só quando acrescentam unidade,
formato ou restrição.

## Go — godoc

Godoc começa pelo nome do identificador e é uma frase completa. A convenção da linguagem manda, e
linters como o `revive` conferem.

```go
// ParseAmount converte "12,34" em centavos; devolve erro se houver mais de duas casas.
func ParseAmount(s string) (int64, error)
```

## Python — docstring

```python
def slugify(title: str) -> str:
    """Devolve o título em minúsculas, sem acento, com hífen no lugar de espaço."""
```

## A guarda contra regressão

É a segunda e última categoria de comentário permitida. Fica na linha que protege, tem até duas
linhas e diz o que quebra se alguém mudar.

```csharp
// Não trocar por record: o ToString() gerado imprimiria o token no log.
public sealed class ApiCredential
```

```go
// A ordem importa: o driver exige SET antes de BEGIN na mesma conexão.
```

Sem marca de severidade e sem ponteiro. Se a razão completa importa, ela vai para o
`ARCHITECTURE.md`, e a guarda continua dizendo só o que quebra.
