---
name: api-design
description: >
  Projeta e revisa contrato de API HTTP antes da implementação: recurso e verbo, semântica HTTP
  (método seguro, idempotência, código de status que reflete o resultado), erro em Problem Details
  (RFC 9457), versionamento, paginação, filtro e evolução compatível. Lê as rotas que o projeto já
  tem antes de propor, para o endpoint novo seguir a convenção da casa. No padrão BKS, o adapter
  inbound traduz o PipelineResult para HTTP e erro de negócio nunca vira 500. Use SEMPRE que o
  usuário for criar endpoint, desenhar ou revisar API, discutir rota, status code, payload de erro,
  versão ou paginação; também quando trouxer um desenho pronto para validar ou for consumir um
  contrato no front. Trigger: novo endpoint, desenhar API, revisar contrato, REST, rota, status code,
  HTTP verb, idempotência, Idempotency-Key, Problem Details, RFC 9457, versionamento de API,
  paginação, cursor, OpenAPI, breaking change.
---

# api-design — o contrato vem antes do código

Contrato de API é a parte do sistema mais cara de mudar: o código muda num commit, o contrato muda
quando o último cliente migra. Por isso esta skill desenha o contrato primeiro, revisa contra a
semântica do HTTP e só então deixa implementar.

Quem consome a API conhece HTTP. Um endpoint que contradiz o protocolo obriga cada cliente a ler
documentação para descobrir o que um proxy, um cache ou uma biblioteca de retry já saberia sozinho.

## 1. Antes de propor: ler o que já existe

Abra as rotas do projeto antes de escrever a primeira linha do contrato. Procure:

- o prefixo e o estilo do caminho (`/api/v1/orders`, `/orders`, plural ou singular, kebab-case);
- como o erro sai hoje: Problem Details, envelope próprio ou corpo livre;
- como a versão aparece: no caminho, em header ou em lugar nenhum;
- como a lista pagina: cursor, `page`/`pageSize`, `offset`/`limit`;
- o arquivo OpenAPI, se houver, e os testes de contrato.

Se a convenção existe, o endpoint novo a segue, mesmo que outra fosse melhor no vazio. Um endpoint
correto e diferente do resto quebra o cliente que generalizou a regra. Quando a convenção existente
for defeito de verdade, aponte em uma linha e proponha a migração como mudança separada.

Sem acesso ao código, pergunte pela convenção antes de impor uma. Uma pergunta só, com as opções
nomeadas.

## 2. Recurso, verbo e identificador

O caminho nomeia **recurso**, substantivo no plural. O verbo é o método HTTP. O identificador vai
no caminho; a query fica para filtro, ordenação e paginação.

| Errado | Certo | Por quê |
|---|---|---|
| `GET /api/cancelarPedido?id=123` | `POST /orders/123/cancellation` | ação com efeito não é GET; identificador na rota |
| `POST /getOrders` | `GET /orders?status=open` | leitura é GET, filtro na query |
| `POST /orders/123/delete` | `DELETE /orders/123` | o método já diz a ação |

Ação de domínio que não cabe em CRUD vira **sub-recurso** com nome de substantivo (`cancellation`,
`approval`, `refund`) e POST. Quem preferir `PATCH /orders/123` com `{"status":"cancelled"}` pode,
desde que a transição tenha regra; mas transição com efeito colateral (estorno, notificação) fica
mais clara como sub-recurso. `DELETE` remove o recurso; cancelar pedido não remove nada, o pedido
continua existindo com outro estado.

## 3. Método seguro, idempotente e o status que reflete o resultado

**GET, HEAD e OPTIONS são seguros**: não mudam estado. Crawler, prefetch do navegador, cache e
retry automático disparam GET sem pedir licença. Um GET que cancela pedido cancela pedido sozinho.

**PUT e DELETE são idempotentes**: repetir produz o mesmo estado. **POST não é**, e precisa de
regra explícita quando o cliente vai repetir — e o cliente sempre repete, porque timeout de rede
não diz se o servidor processou. Defina o que acontece na segunda chamada:

- cancelar pedido já cancelado devolve o mesmo resultado da primeira vez, sem novo efeito;
- cancelar pedido já despachado é transição inválida: `409 Conflict` com Problem Details;
- POST que cria recurso ou movimenta valor aceita `Idempotency-Key` e guarda a resposta pela chave,
  com constraint única no banco, não checagem em código.

**O status reflete o resultado.** `200` com `{"ok": false}` faz o monitoramento contar falha como
sucesso, o retry não saber quando parar e o cache guardar o erro. O front que "só olha o corpo"
continua podendo olhar o corpo; os outros clientes do protocolo param de ser enganados.

A tabela de status por situação, as regras de cada método e o desenho do `Idempotency-Key` estão
em `references/semantica-http.md`.

## 4. Erro em Problem Details

Toda resposta de erro sai em `application/problem+json`, no formato da RFC 9457: `type`, `title`,
`status`, `detail`, `instance`, e extensões tipadas quando o cliente precisa agir (lista de campos
inválidos, por exemplo). O `type` é o contrato: o cliente decide por ele, não pelo texto do
`title`.

Erro não carrega stack trace, nome de tabela, SQL nem mensagem de exceção. O `traceId` vai como
extensão para correlacionar com a telemetria.

## 5. Ligação com o padrão BKS

O use case devolve `PipelineResult<TResponse>`; quem fala HTTP é o adapter inbound. Ele faz uma
tradução só, num lugar só:

| Resultado do pipeline | HTTP |
|---|---|
| sucesso com recurso criado | `201` + `Location` |
| sucesso com corpo | `200` |
| sucesso sem corpo | `204` |
| falha de validação de entrada | `400` ou `422`, conforme a convenção da casa |
| recurso não encontrado, ou não pertence a quem chama | `404` |
| transição de estado inválida, conflito de versão | `409` |
| exceção não prevista | `500`, sem detalhe interno |

Erro de negócio nunca chega como exceção ao adapter, e por isso nunca vira 500. Se o erro do
projeto é uma string, o adapter não tem como distinguir 404 de 409: o erro precisa de um tipo.
O mapeamento completo em C#, com o catálogo de `type` e o teste do adapter, está em
`references/erros-problem-details.md`.

## 6. Versão, paginação e evolução

- **Mudança compatível** (campo novo opcional, endpoint novo, valor novo de enum documentado como
  aberto) não muda a versão.
- **Mudança incompatível** (remover ou renomear campo, mudar tipo, tornar obrigatório, mudar status
  de um caso existente) exige versão nova e período de convivência com `Deprecation` e `Sunset`.
- Lista sem paginação é bug com data marcada. Cursor opaco para coleção grande ou que muda durante
  a leitura; `offset`/`limit` só para coleção pequena e estável. Toda lista tem limite máximo do
  lado do servidor.

Regras de versionamento, formato de página, filtro e ordenação em
`references/evolucao-e-colecoes.md`.

## 7. Conduta

**Quando o usuário traz um desenho pronto**, revise contra as seções 2 a 4 antes de implementar.
Corrija cada ponto com o motivo em uma frase, mostre o contrato corrigido e confirme a convenção
existente. Não implemente o desenho errado para corrigir depois: o cliente que nascer contra ele
vira o motivo de nunca mais corrigir.

**Entregue o contrato antes do código**: método e caminho, corpo de entrada, respostas de sucesso
e de erro com status e `type`, comportamento na repetição. Em projeto com OpenAPI, o contrato entra
no arquivo; sem OpenAPI, entra na spec da feature.

**Teste o contrato, não só o use case.** O teste do adapter confere status, `Content-Type` e o
`type` do Problem Details de cada caminho de erro, com `Assert` nativo do xUnit.

## Checklist

- [ ] Rotas existentes lidas, ou convenção perguntada, antes de propor.
- [ ] Caminho nomeia recurso; identificador no caminho; verbo é o método HTTP.
- [ ] Nenhum GET altera estado.
- [ ] Repetição de cada POST e PATCH tem comportamento definido.
- [ ] Status reflete o resultado; nenhum erro sai com 2xx.
- [ ] Erro em Problem Details, com `type` estável e sem detalhe interno.
- [ ] Recurso de outro dono responde 404, não 403.
- [ ] Lista com paginação e limite máximo.
- [ ] Mudança classificada como compatível ou incompatível.
- [ ] Teste do adapter cobre os status de erro.
