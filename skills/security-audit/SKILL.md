---
name: security-audit
description: >
  Revisão de segurança de código por superfície de ataque: autenticação, autorização (dono do
  recurso, IDOR/BOLA, isolamento de tenant — não só login), entrada não confiável (injeção SQL e de
  comando, desserialização, SSRF, path traversal), segredos, dado sensível e PII em log,
  dependências e configuração. Todo achado sai com arquivo:linha, cenário de exploração concreto,
  correção mínima e severidade justificada pelo impacto. Use SEMPRE que o usuário pedir revisão de
  segurança, auditoria, pentest de código, threat model ou "isso está seguro?"; e ative por conta
  própria quando o código tocar autenticação, autorização, pagamento, dado pessoal (CPF, e-mail,
  cartão), upload, webhook ou entrada externa. Trigger: security review, auditoria de segurança,
  vulnerabilidade, OWASP, ASVS, CWE, IDOR, BOLA, broken access control, SQL injection, XSS, SSRF,
  segredo no código, vazamento de dado, LGPD, token, JWT.
---

# security-audit — o que o código permite, não o que dizem dele

A revisão responde a uma pergunta: **o que um atacante consegue fazer com este código?** Lista de
verificação ajuda a não esquecer superfície, mas a falha que importa costuma estar na regra de
negócio que ninguém pensou em atacar, e não no item óbvio do checklist.

## 1. Afirmação não é evidência

"O time revisou", "passou no pentest", "o gateway valida" e "só o front chama este endpoint" são
hipóteses, não fatos sobre o código à frente. Pentest cobre o que o testador alcançou na janela
dele; o código pode ter mudado desde então, e a falha de autorização exige conhecer dois usuários
para aparecer.

Revise o que está escrito. Se uma proteção vive fora do trecho analisado (middleware, gateway,
filtro global), peça para ver ou registre como premissa não verificada no relatório. Nunca dê o
ponto como seguro porque alguém disse.

## 2. Comece pela autorização

A falha mais comum em API é a que o checklist de entrada não pega: **o endpoint autentica e não
autoriza**. `[Authorize]` prova que existe um usuário logado; não prova que o recurso pedido é
dele.

```csharp
[HttpGet("orders/{orderId}")]
[Authorize]
public async Task<IActionResult> GetOrder(Guid orderId)
{
    var order = await _repo.GetByIdAsync(orderId);
    ...
```

Qualquer cliente autenticado lê o pedido de qualquer outro, bastando ter o identificador. É IDOR
(referência direta insegura a objeto, CWE-639), a BOLA do OWASP API Security Top 10 (API1). Guid
não protege: identificador vaza em URL, log, e-mail, tela compartilhada e resposta de outro
endpoint.

Para cada operação que recebe identificador, faça três perguntas:

1. **De onde vem a identidade de quem chama?** Tem de vir da credencial validada (claim do token),
   nunca da rota, da query ou do corpo.
2. **Onde se verifica que o recurso pertence a essa identidade?** Na consulta (`WHERE id = @id AND
   customer_id = @callerId`) ou numa regra explícita do use case. Papel genérico ("é cliente") não
   substitui verificação de propriedade.
3. **O que responde quando não pertence?** `404`, igual a inexistente. `403` confirma que o
   identificador existe e permite enumerar.

O padrão de correção em .NET, a variação multi-tenant, o caso do administrador e o teste que prova
"A não lê o recurso de B" estão em `references/autorizacao-por-objeto.md`.

## 3. As outras superfícies

Percorra cada uma que o código toca. Para cada superfície, o que procurar, onde costuma estar e o
CWE de referência estão em `references/superficies.md`.

| Superfície | Pergunta central |
|---|---|
| Autenticação | o token é validado inteiro (assinatura, emissor, audiência, expiração)? |
| Autorização | a operação confere dono, tenant e permissão, nessa ordem de importância? |
| Entrada não confiável | algum dado externo chega a SQL, shell, caminho de arquivo, URL de saída ou desserializador sem parâmetro ou validação? |
| Atribuição em massa | o corpo da requisição consegue escrever campo que o cliente não deveria (`role`, `price`, `ownerId`)? |
| Segredos | há credencial no código, no `appsettings`, no histórico do git ou no log? |
| Dado sensível em log | senha, token, CPF, cartão ou PII chegam ao log, ao trace ou à mensagem de erro? |
| Dependências | há pacote com vulnerabilidade conhecida, ou fonte de pacote não confiável? |
| Configuração | CORS, HTTPS, cabeçalhos, página de erro de desenvolvimento, limite de tamanho e de taxa |

A regra BKS de log não tem exceção: **nunca logar senha, token, CPF nem PII em claro**, nem em nível
debug. Mascare ou omita no ponto onde o dado entra no log, não num filtro global que alguém desliga.

## 4. O achado

Achado sem localização é opinião. Cada um tem cinco partes:

```
src/Orders/Adapters/Inbound/Api/OrdersController.cs:42
Problema: o endpoint busca o pedido só pelo id, sem conferir o dono.
Exploração: cliente A, autenticado, chama GET /orders/{id-do-pedido-de-B} e recebe
  endereço, itens e valor do pedido de B.
Correção: filtrar por customer_id da claim na consulta e responder 404 quando não houver linha.
Severidade: crítica — leitura de dado pessoal de terceiro por qualquer usuário autenticado.
```

A **severidade se justifica pelo impacto**, numa frase: quem explora, o que precisa ter, o que
obtém. "Grave" e "perigoso" não são justificativa. A régua, o formato do relatório e a declaração
de escopo estão em `references/relatorio.md`.

A **exploração é concreta**: requisição, entrada ou sequência de passos, e o efeito observável. Se
não dá para descrever a exploração, o achado ainda é hipótese; registre como tal, com o que falta
para confirmar.

A **correção é a menor que fecha a falha**. Refatoração ampla vai como sugestão separada.

## 5. Conduta

- **Leia o código antes de concluir.** Siga o identificador da rota até a consulta, e a entrada
  externa até onde ela é usada. A falha mora na ligação entre camadas.
- **Ative por conta própria** quando a tarefa em andamento tocar autenticação, pagamento, dado
  pessoal, upload, webhook ou entrada externa. Uma linha avisando que revisou, e o achado se houver.
- **Revisão sem achado declara o escopo verificado**: arquivos, superfícies e premissas. "Nada
  encontrado" sem escopo não dá garantia nenhuma.
- **Não invente achado para ter o que entregar.** Ponto de higiene sem exploração vai em seção
  própria, abaixo dos achados, sem severidade.
- **A correção pede teste**: o caso de exploração vira teste que falha antes da correção e passa
  depois, com `Assert` nativo do xUnit.
- Em entrega que toca área sensível, a revisão independente é do agente `reviewer`, em invocação
  separada de quem implementou.

## Referências externas

Cite pela identificação quando ajudar a correção a ser aceita: OWASP Top 10 (A01 a A10), OWASP API
Security Top 10, OWASP ASVS (o nível e o requisito), OWASP Cheat Sheet Series (o tema) e CWE
(o número). A citação acompanha o achado; não substitui a exploração.

## Checklist

- [ ] Nenhuma afirmação externa usada como evidência de segurança.
- [ ] Toda operação com identificador verifica o dono do recurso a partir da credencial.
- [ ] Recurso de outro dono responde 404.
- [ ] Toda superfície tocada pelo código foi percorrida.
- [ ] Nenhuma senha, token, CPF ou PII em log, trace ou erro.
- [ ] Cada achado com `arquivo:linha`, exploração, correção e impacto.
- [ ] Escopo verificado declarado, com as premissas não verificadas.
