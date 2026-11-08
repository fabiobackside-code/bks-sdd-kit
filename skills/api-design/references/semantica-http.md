# Semântica HTTP — método, status e repetição

O protocolo já resolve boa parte do desenho. Cada propriedade abaixo é uma promessa que clientes,
proxies e bibliotecas assumem sem perguntar; quebrar a promessa quebra quem confia nela.

## Propriedades de cada método

| Método | Seguro | Idempotente | Uso |
|---|---|---|---|
| `GET` | sim | sim | ler recurso ou coleção |
| `HEAD` | sim | sim | o mesmo que GET, sem corpo |
| `OPTIONS` | sim | sim | capacidades do recurso, CORS |
| `POST` | não | não | criar em coleção, executar ação de domínio como sub-recurso |
| `PUT` | não | sim | substituir o recurso inteiro, ou criar em URI que o cliente escolhe |
| `PATCH` | não | não por definição | alterar parte do recurso |
| `DELETE` | não | sim | remover o recurso |

**Seguro** significa que o cliente não pede efeito. Log e métrica não contam; mudar estado de
negócio conta. **Idempotente** significa que N chamadas deixam o mesmo estado que uma. A resposta
pode variar: o segundo `DELETE` pode devolver `404`, e o estado continua o mesmo.

`PATCH` pode ser idempotente quando o corpo descreve o estado final (`{"status":"cancelled"}`) e
deixa de ser quando descreve operação (`{"increment": 1}`). Prefira a primeira forma.

## Status por situação

### Sucesso

| Status | Quando |
|---|---|
| `200 OK` | leitura, ou ação com corpo de resposta |
| `201 Created` | recurso criado; `Location` aponta para ele e o corpo traz a representação |
| `202 Accepted` | aceito para processar depois; corpo aponta onde acompanhar |
| `204 No Content` | sucesso sem corpo, típico de `DELETE` e `PUT` |

### Erro do cliente

| Status | Quando | Não confundir com |
|---|---|---|
| `400 Bad Request` | corpo malformado, tipo errado, campo obrigatório ausente | regra de negócio violada |
| `401 Unauthorized` | sem credencial, ou credencial inválida ou expirada | falta de permissão |
| `403 Forbidden` | autenticado, sem permissão para a operação em si | recurso de outro dono, que é 404 |
| `404 Not Found` | recurso não existe, ou existe e não pertence a quem chama | — |
| `405 Method Not Allowed` | método não suportado no recurso; mande `Allow` | — |
| `409 Conflict` | transição de estado inválida, duplicidade, chave de idempotência em uso | validação de formato |
| `412 Precondition Failed` | `If-Match` não confere com o `ETag` atual | — |
| `415 Unsupported Media Type` | `Content-Type` que o endpoint não aceita | — |
| `422 Unprocessable Content` | corpo bem formado, mas semanticamente inválido | — |
| `428 Precondition Required` | o endpoint exige `If-Match` e ele não veio | — |
| `429 Too Many Requests` | limite de taxa; mande `Retry-After` | — |

A fronteira entre `400` e `422` varia de casa para casa. Escolha uma regra e aplique em todo
endpoint; a convenção existente vence a preferência pessoal.

### Erro do servidor

`500` é defeito do servidor, nunca resultado de regra de negócio. `502`, `503` e `504` dizem que
uma dependência falhou ou não respondeu; `503` com `Retry-After` diz ao cliente quando voltar.

## Por que "sempre 200" quebra

O argumento comum é que o front só olha o corpo. O front não é o único cliente do protocolo:

- o APM e o dashboard contam taxa de erro por status; com 200 em tudo, a taxa de erro é zero;
- o cache de proxy e de CDN guarda resposta 200 de GET, inclusive a de erro;
- a política de retry (Polly, `fetch` com retry, SDK gerado) decide por status; com 200, não
  repete o que deveria e não para no que não deveria;
- o cliente gerado a partir de OpenAPI lança exceção tipada por status; com 200, tudo é sucesso e
  o desserializador quebra no corpo de erro.

O front continua lendo o corpo, e o corpo passa a ser Problem Details em todo erro.

## Repetição e idempotência de POST

Timeout de rede não diz se o servidor processou. O cliente repete, e o servidor precisa
reconhecer a repetição.

### Ação de domínio sobre recurso existente

O estado do recurso já resolve. Exemplo do cancelamento:

| Estado atual | `POST /orders/123/cancellation` |
|---|---|
| `open` | cancela, `200` com o pedido cancelado |
| `cancelled` | não faz nada de novo, `200` com o mesmo pedido |
| `shipped` | `409`, `type` = `.../order-not-cancellable` |
| não existe ou é de outro cliente | `404` |

O segundo caso é o que torna a ação idempotente: nenhum novo estorno, nenhuma nova notificação. O
use case decide pela transição, e o teste cobre a chamada dupla.

### Criação e movimentação de valor

Sem estado prévio para comparar, use `Idempotency-Key`:

1. O cliente gera um identificador único por intenção (UUID) e manda no header.
2. O servidor grava chave, hash do corpo e resposta numa tabela com constraint única na chave,
   escopada por cliente ou tenant.
3. Repetição com a mesma chave e o mesmo corpo devolve a resposta gravada.
4. Mesma chave com corpo diferente devolve `422`; chave ainda em processamento devolve `409`.
5. A chave expira depois de uma janela definida no contrato, por exemplo 24 horas.

A constraint no banco é o que garante. Checar "já existe?" em código deixa passar duas requisições
concorrentes que leem ao mesmo tempo.

## Concorrência otimista

Edição concorrente de recurso perde atualização sem aviso. O `GET` devolve `ETag`; o `PUT` ou
`PATCH` manda `If-Match`; o servidor responde `412` se o recurso mudou. A versão vem de uma coluna
de versão ou `rowversion`, não de hash do corpo calculado a cada leitura.

## Cabeçalhos que fazem parte do contrato

| Header | Direção | Uso |
|---|---|---|
| `Location` | resposta | URI do recurso criado (`201`) ou do status do processamento (`202`) |
| `ETag` / `If-Match` | ambos | concorrência otimista |
| `Idempotency-Key` | requisição | repetição segura de POST |
| `Retry-After` | resposta | quando tentar de novo (`429`, `503`) |
| `Allow` | resposta | métodos aceitos (`405`) |
| `Deprecation` / `Sunset` | resposta | versão em retirada e data de desligamento |
| `traceparent` | ambos | correlação W3C com a telemetria |
