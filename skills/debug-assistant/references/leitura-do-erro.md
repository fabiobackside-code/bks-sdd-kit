# Leitura do erro — o que a stack diz e onde ela engana

A maior parte do diagnóstico cabe na mensagem e na stack que já existem. Esta referência mostra
como ler cada formato e quais armadilhas fazem a leitura apontar para o lugar errado.

## A ordem de leitura

1. **Tipo e mensagem** da exceção mais externa.
2. **Exceção interna**, até a última. É ela que diz o que aconteceu; as de fora dizem por onde o
   erro passou.
3. **Primeiro quadro do código do projeto**, procurando de cima para baixo na stack da exceção
   mais interna. Quadros de framework acima dele mostram onde explodiu; ele mostra quem chamou com
   o valor errado.
4. **Contexto da requisição**: o traceId, o log anterior ao erro e o span. O erro raramente é o
   primeiro sinal; o log de dois segundos antes costuma ter o valor estranho.

## .NET

### NullReferenceException

A mensagem não diz qual variável era nula. A linha diz, desde que a linha esteja na stack:

- **Sem número de linha** significa build sem PDB ou com PDB não implantado. Publique o PDB
  (`<DebugType>portable</DebugType>`) ou embuta (`embedded`); sem ele, cada NRE vira caça.
- **Uma linha com várias desreferências** (`order.Customer.Address.ZipCode`) não diz qual parte
  era nula. Separe em variáveis no teste de reprodução, ou confira cada uma no depurador.
- **Com nullable reference types ligado**, procure o aviso que alguém silenciou: `!` (operador
  de supressão), `#nullable disable`, `= null!` em propriedade. O defeito costuma morar ao lado do
  `!` que prometeu que o valor nunca seria nulo.
- **Desserialização** é origem frequente: o JSON não trouxe o campo, o `System.Text.Json` deixou o
  padrão, e a propriedade declarada como não nula está nula. `required` na propriedade, ou
  `JsonRequired`, transforma isso em erro na borda.

`ArgumentNullException` já nomeia o parâmetro na mensagem. É o formato que a validação de borda
deveria produzir, e por isso indica que o valor nulo veio de fora daquele método.

### Stack de código assíncrono

Desde o .NET Core 2.1 a stack de `async` sai legível, sem os quadros de máquina de estado. Ainda
assim:

- `--- End of stack trace from previous location ---` separa o trecho antes e depois de um
  `await`. Leia os dois.
- `AggregateException` vem de `.Result`, `.Wait()` ou `Task.WhenAll` observado por `.Exception`.
  Abra `InnerExceptions` e leia todas, não só a primeira. A presença de `.Result` em código
  assíncrono é em si suspeita de deadlock em contexto com sincronização.
- `TaskCanceledException` e `OperationCanceledException` dizem que alguém cancelou ou que um
  timeout venceu. Em `HttpClient`, o timeout aparece como `TaskCanceledException` com
  `TimeoutException` interna.

### Exceções que enganam

| Exceção | O que costuma ser |
|---|---|
| `TypeInitializationException` | exceção no construtor estático; a interna é a real |
| `TargetInvocationException` | exceção dentro de código chamado por reflexão; a interna é a real |
| `InvalidOperationException` em coleção | coleção alterada durante enumeração, frequentemente por outra thread |
| `ObjectDisposedException` | uso depois do fim do escopo de DI, ou `DbContext` capturado num `Task` solto |
| `DbUpdateConcurrencyException` | duas escritas no mesmo registro; é concorrência, não falha de banco |
| `SqlException` com número 1205 | deadlock no banco; o número diz mais que a mensagem |

### Release e otimização

Em Release, o JIT pode embutir métodos pequenos, e o quadro do método embutido some da stack. Se a
stack aponta para um método que parece incapaz de lançar aquela exceção, confira os métodos que ele
chama diretamente.

## Go

Um panic imprime a mensagem, a goroutine que entrou em pânico e a stack dela. Os pontos de leitura:

- `invalid memory address or nil pointer dereference` com `[signal SIGSEGV ...]`: ponteiro nulo.
  A linha do primeiro quadro do pacote do projeto é a desreferência.
- Interface com valor nulo dentro não é nula: `var p *T = nil; var i I = p; i != nil` é verdadeiro.
  Função que devolve `error` concreto nulo como interface produz `err != nil` sem erro algum.
- `concurrent map writes` é condição de corrida em mapa; confirme com `go test -race`.
- `all goroutines are asleep - deadlock!` traz a stack de todas as goroutines: procure as que
  esperam no mesmo canal ou mutex.
- Erro embrulhado com `%w` guarda a cadeia; `errors.Is` e `errors.As` a percorrem. Log com `%v` no
  meio da cadeia, sem `%w`, corta a causa.

`GOTRACEBACK=all` mostra todas as goroutines no panic, útil quando a causa está em outra.

## TypeScript e Node.js

- **Stack minificada** em produção só se lê com source map. Gere o mapa no build e resolva a stack
  com ele (o Node com `--enable-source-maps` faz isso em tempo de execução).
- `Cannot read properties of undefined (reading 'zipCode')` diz a propriedade lida, não o objeto
  que era `undefined`; o objeto é o que vem antes do ponto.
- **Promise rejeitada sem tratamento** (`unhandledRejection`) perde a stack de quem a criou. Ligue
  o tratador global para registrar a origem, e procure `async` chamado sem `await`.
- `error.cause` guarda a causa encadeada desde o ES2022; o log que só imprime `message` a perde.
- Tipo do TypeScript não existe em tempo de execução: dado vindo de fora tipado com `as` não foi
  validado. Esse é o equivalente do `!` do C#.

## Quando a stack não existe

Erro engolido, processo que morre sem log ou resposta errada sem exceção pedem que se crie a
evidência antes de investigar:

- procure `catch` vazio ou que só registra a mensagem, sem a exceção, no caminho do fluxo;
- ligue a captura de exceção de primeira chance no depurador para ver a que foi engolida;
- em contêiner que reinicia, leia o log do contêiner anterior (`kubectl logs --previous`) e o
  motivo do término (`OOMKilled` é falta de memória, não defeito de código).
