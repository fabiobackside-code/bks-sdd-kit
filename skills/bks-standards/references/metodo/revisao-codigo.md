# Revisão de código — o que olhar e em que ordem

Guia de método do agente `reviewer`. A revisão existe para achar o defeito que vai chegar à
produção, e a ordem abaixo põe primeiro o que custa mais caro se passar. Estilo vem por último
porque o linter já pega quase tudo dele.

## Antes de abrir o código

1. **Delimite o escopo.** Liste os arquivos do diff e marque os que tocam área sensível do
   manifesto do projeto. A revisão cobre o que mudou e o que a mudança afeta, não o repositório.
2. **Leia a spec da entrega.** FEAT (a feature), TEST (os cenários) e TASK (a unidade de
   trabalho) dizem o que o código deveria fazer. Sem isso, a revisão só confere se o código faz o que ele mesmo diz.
3. **Leia o log de decisões do projeto.** Decisão já aceita não volta como achado.

## A ordem

### 1. Correção

O código faz o que a spec pede, inclusive no caso de borda? Procure:

- entrada vazia, nula, duplicada ou fora de faixa sem tratamento;
- condição invertida, limite com `<` onde devia ser `<=`, comparação de tipos diferentes;
- estado alterado antes de uma validação que pode falhar;
- concorrência: duas requisições iguais ao mesmo tempo, recurso compartilhado sem proteção;
- recurso aberto sem fechamento no caminho de erro.

### 2. Conformidade com as premissas do kit

As premissas BKS (o padrão-base do kit: hexagonal, pipeline, transaction e Result) têm cada uma
um sinal concreto no diff:

| Premissa | Sinal de violação |
|---|---|
| Domain agnóstico | `using` de ORM (mapeador objeto-relacional), driver, ASP.NET ou cliente de mensageria em `Domain/` |
| Sem dispatcher | MediatR, `ISender`, `IMediator` ou um despachante caseiro por tipo de mensagem |
| Result Pattern | `throw` de regra de negócio no use case, ou exceção de negócio chegando ao adapter |
| Transaction como parameter object | contexto (correlação, usuário, tenant) passado solto em vários parâmetros, ou a transaction mutada no meio do fluxo |
| Telemetria via BaseStep | `Activity` montada à mão, `try/catch` só para registrar span |

Padrão do projeto em `brain/engineering/` sobrepõe o do kit; confira antes de apontar.

### 3. Segurança e dado sensível

Para mudança em área sensível, o checklist obrigatório é `checklist-revisao-critica.md`, na mesma
pasta de referências. Em qualquer mudança, confira ao menos:

- identificador do titular vindo da credencial, nunca do corpo ou da URL;
- query com parâmetro vinculado, sem concatenação;
- senha, token, CPF e dado pessoal fora de log, mensagem de erro e telemetria;
- segredo fora do código e do arquivo de configuração versionado.

### 4. Testes que provam o cenário

Leia os testes do diff. Para cada critério de aceite da spec, existe um teste que falharia se o
critério fosse quebrado? Teste que só exercita o caminho feliz, que verifica a chamada ao mock em
vez do resultado, ou que passaria com a implementação vazia não prova nada.

Rode a suíte quando a ferramenta permitir. Quando não permitir, diga isso no relatório.

### 5. Legibilidade e estilo

Nome que engana, método que faz duas coisas, comentário que viola o teto do kit. Entra como achado
de severidade baixa, nunca bloqueia sozinho.

## O achado

Todo achado tem localização, impacto e correção. Sem os três, é opinião.

```
src/Orders/Application/CancelOrderUseCase.cs:42
Problema: o cancelamento não confere se o pedido pertence ao usuário da credencial.
Impacto: qualquer usuário autenticado cancela pedido de outro passando o ID na URL.
Correção: filtrar por OwnerId = transaction.UserId na consulta da linha 38.
Severidade: crítica
```

A correção é o menor passo que resolve. Reescrita do módulo não é correção.

## Fechando a revisão

- Liste os achados por severidade, críticos primeiro.
- Declare o escopo verificado: arquivos lidos, testes lidos ou rodados, o que ficou fora.
- Revisão sem achado também declara o escopo. "Nada encontrado" sem escopo não garante nada.
