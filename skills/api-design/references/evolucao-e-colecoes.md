# Evolução do contrato e coleções

A API muda; o cliente que já está em produção, não. Esta referência separa a mudança que o cliente
absorve sem saber da que o quebra, e define como listar coleção sem que a lista cresça até derrubar
o servidor.

## Compatível ou incompatível

Classifique toda mudança antes de implementar. A classificação decide se a versão muda.

| Mudança | Classe | Condição |
|---|---|---|
| campo novo na resposta | compatível | o cliente ignora campo desconhecido |
| campo novo opcional na requisição | compatível | ausência mantém o comportamento anterior |
| endpoint novo | compatível | — |
| valor novo de enum na resposta | compatível só se o enum foi documentado como aberto | senão, incompatível |
| código novo de erro | compatível | o cliente tem tratamento para `type` desconhecido |
| remover ou renomear campo | incompatível | — |
| mudar tipo ou formato de campo | incompatível | `"10.50"` para `10.5` é mudança de tipo |
| campo opcional passa a obrigatório | incompatível | — |
| mudar o status de um caso existente | incompatível | `200` para `204` quebra quem lê o corpo |
| mudar o significado de um campo sem mudar o nome | incompatível, e a pior | ninguém percebe até o dado sair errado |

O desserializador do cliente precisa ignorar campo desconhecido. Em .NET, o `System.Text.Json` já
ignora por padrão; não ligue `UnmappedMemberHandling.Disallow` em cliente de API externa.

## Versionamento

Siga o que o projeto já usa. Sem convenção, a versão vai no caminho (`/v1/orders`): aparece no
log, no proxy e na documentação sem configuração extra. Versão em header ou em media type é
válida, e cobra disciplina de todo cliente e de toda ferramenta no caminho.

- A versão é **maior** e muda só por mudança incompatível. Mudança compatível não gera `v1.1`.
- Versão nova convive com a anterior por um período escrito no contrato.
- A versão em retirada responde com `Deprecation` e `Sunset` (RFC 9745 e RFC 8594), e com `Link`
  apontando para a documentação de migração.
- A métrica de chamadas por versão diz quando é seguro desligar. Desligar sem olhar a métrica é
  descobrir o cliente esquecido pelo chamado dele.

No padrão BKS, a versão nova é outro adapter inbound sobre o mesmo use case sempre que a diferença
for de formato. Quando a regra de negócio muda, o use case também muda, e a versão antiga passa a
traduzir para o comportamento novo ou fica congelada até o desligamento.

## Paginação

Toda coleção pagina, e o servidor impõe o tamanho máximo. Lista sem limite funciona com 200
registros no ambiente de teste e derruba o processo com 2 milhões em produção.

### Cursor ou offset

| | Cursor | Offset |
|---|---|---|
| Requisição | `?limit=50&cursor=eyJpZCI6...` | `?limit=50&offset=100` |
| Custo no banco | constante, usa índice (`WHERE id > @last`) | cresce com o offset, o banco lê e descarta |
| Inserção durante a leitura | não repete nem pula item | repete ou pula item |
| Ir para a página 37 | não | sim |
| Total de itens | caro, opcional | caro, opcional |

Use cursor como padrão. Offset serve para coleção pequena e estável, ou para tela que precisa
saltar para página arbitrária. O total exige `COUNT` sobre o filtro inteiro: devolva só quando o
cliente pedir e o custo for conhecido.

### Formato

```json
{
  "items": [ { "id": "8f1c...", "status": "open" } ],
  "nextCursor": "eyJjcmVhdGVkQXQiOiIyMDI2LTExLTA4VDEyOjAwOjAwWiIsImlkIjoiOGYxYy4uLiJ9",
  "limit": 50
}
```

`nextCursor` nulo encerra a lista. O cursor é **opaco**: o cliente devolve sem interpretar, e o
servidor pode mudar o conteúdo sem quebrar ninguém. Codifique a chave de ordenação completa,
incluindo o desempate por identificador, e valide o cursor recebido como qualquer entrada externa.

Em TypeScript, a codificação e a validação ficam no adapter:

```typescript
type CursorKey = { createdAt: string; id: string };

export const encodeCursor = (key: CursorKey): string =>
  Buffer.from(JSON.stringify(key)).toString("base64url");

export function decodeCursor(raw: string): CursorKey | null {
  try {
    const parsed = JSON.parse(Buffer.from(raw, "base64url").toString("utf8"));
    const valid = typeof parsed?.createdAt === "string" && typeof parsed?.id === "string";
    return valid ? parsed : null;
  } catch {
    return null;
  }
}
```

Cursor inválido responde `400` em Problem Details, não `500`.

Em PostgreSQL, a consulta usa comparação de tupla sobre a mesma ordenação do índice. SQL Server não
tem comparação de tupla: escreva `created_at < @c OR (created_at = @c AND id < @id)` e `TOP`.

```sql
SELECT id, status, created_at
FROM orders
WHERE customer_id = @customerId
  AND (created_at, id) < (@cursorCreatedAt, @cursorId)
ORDER BY created_at DESC, id DESC
LIMIT @limit;
```

## Filtro e ordenação

- Filtro vai na query, com nome do campo do contrato: `?status=open&createdFrom=2026-11-01`.
- Só os campos indexados ou de custo conhecido são filtráveis; a lista fica no contrato.
- Ordenação aceita uma lista fechada de campos (`?sort=-createdAt`). Campo fora da lista é `400`;
  nunca concatene o valor recebido no `ORDER BY`.
- Data e hora em ISO 8601 com fuso (`2026-11-08T12:00:00Z`). Valor monetário como string decimal
  ou inteiro na menor unidade, nunca número de ponto flutuante.

## Busca que não cabe na query

Filtro com estrutura complexa, ou que levaria dado sensível para a URL e daí para o log de acesso,
vira `POST /orders/search` com o critério no corpo. A rota é exceção documentada: o POST continua
seguro na prática, e o contrato diz isso.
