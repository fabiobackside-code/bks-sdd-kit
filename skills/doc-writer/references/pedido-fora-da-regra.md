# Pedido fora da regra: como responder

O usuário pede o que a guarda recusa: o bloco longo com a decisão, o histórico no topo da classe, o
alerta colorido para ninguém mexer. A resposta não discute a regra nem a ignora em silêncio. Ela
entrega o código conforme, diz por que ficou assim e põe o conteúdo pedido onde ele sobrevive.

## As três partes da resposta

1. **O código.** Contrato em uma linha no membro público. Se existe um risco concreto de regressão,
   uma guarda de até duas linhas dizendo o que quebra. Sem marca de severidade.
2. **O motivo, em duas ou três frases.** O teto de cinco linhas e a marca de severidade são
   recusados pela guarda do kit a cada escrita de `.cs`. Decisão escrita no comentário envelhece
   sem ninguém ver, porque ninguém revisa comentário quando muda o desenho.
3. **O conteúdo no lugar certo.** A entrada do `ARCHITECTURE.md`, com o que o usuário contou e com
   `[!uncertain]` no que ele não contou. A informação muda de lugar, não some.

## Exemplo

Pedido: "Comenta esta classe explicando por que a fila é em memória e não no RabbitMQ, conta quando
mudou, e põe um aviso vermelho para ninguém mexer."

```csharp
public sealed class OutboxBuffer
{
    private readonly ConcurrentQueue<OutboxMessage> _pending = new();

    /// <summary>Enfileira a mensagem para o próximo ciclo de envio; não bloqueia.</summary>
    // Mensagens pendentes se perdem se o processo cair antes do ciclo de envio.
    public void Enqueue(OutboxMessage message) => _pending.Enqueue(message);
}
```

Texto que acompanha o código:

> Deixei no código só o contrato e a guarda que diz o que se perde se o processo cair. O bloco com
> a decisão e o aviso em vermelho seriam recusados pela guarda de comentário do kit: o teto é de
> cinco linhas por bloco, e marca de severidade não entra. A decisão foi para o `ARCHITECTURE.md`,
> que é onde quem for mexer na fila vai procurar:

```markdown
### O buffer de saída fica em memória, sem broker

As mensagens esperam numa fila do próprio processo até o ciclo de envio. Se a instância cair antes,
as pendentes se perdem.

A alternativa era publicar direto no RabbitMQ, que sobrevive à queda ao custo de uma dependência
de infraestrutura a mais no serviço.

> [!uncertain]
> Quando a fila saiu do broker e o que motivou a troca: confirmar com quem decidiu.
```

> A classe é pública, então o `README.md` também precisa entrar nesta mudança; sem ele a guarda de
> documentação recusa a escrita do `.cs`.

## O que não fazer

- Escrever o bloco longo e avisar que ele viola a regra. A guarda recusa e o trabalho se perde.
- Cortar o pedido sem dizer nada. O usuário volta perguntando onde foi parar a explicação.
- Inventar a justificativa que o usuário não deu. Marque e pergunte.
- Trocar o alerta colorido por "IMPORTANTE:" em maiúsculas. É a mesma marca de severidade escrita
  com letras.
