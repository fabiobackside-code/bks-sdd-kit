# Superfícies de ataque — o que procurar e onde

Cada seção diz o que perguntar ao código, onde a falha costuma morar e como fica o certo. Os termos
de busca são ponto de partida para achar o trecho; a conclusão vem de ler o fluxo até o fim.

Autorização por objeto tem referência própria, `autorizacao-por-objeto.md`, e não se repete aqui.

## Autenticação

**Pergunta:** o sistema confere a credencial inteira, em todo caminho de entrada?

- Token JWT validado por assinatura, emissor, audiência e expiração. `ValidateIssuer = false`,
  `ValidateAudience = false`, `ValidateLifetime = false` ou `RequireSignedTokens = false` são
  achados até prova em contrário (CWE-347).
- Algoritmo fixado pelo servidor; nunca aceitar `alg: none` nem o algoritmo que o token declara.
- Chave de assinatura simétrica curta ou presente no repositório (CWE-321).
- Endpoint sem `RequireAuthorization` num grupo que deveria ter, ou `AllowAnonymous` esquecido
  depois de um teste.
- Senha guardada com hash rápido (`SHA256`, `MD5`) em vez de algoritmo de derivação lento (CWE-916);
  comparação de segredo com `==` em vez de comparação em tempo constante (CWE-208).
- Login, recuperação de senha e verificação de código sem limite de tentativas (CWE-307).
- Mensagem de erro de login que distingue "usuário não existe" de "senha errada" (CWE-204).

Busca: `TokenValidationParameters`, `AllowAnonymous`, `ValidateLifetime`, `SymmetricSecurityKey`,
`PasswordHasher`, `SHA256.HashData`.

## Atribuição em massa

**Pergunta:** o cliente consegue escrever campo que só o servidor deveria definir?

O sinal é a entidade de domínio, ou o modelo de persistência, recebida direto como corpo da
requisição. Campos como `Role`, `IsAdmin`, `Price`, `Discount`, `OwnerId`, `TenantId` e `Status`
passam a ser escritos por quem chama (CWE-915, API3:2023 no OWASP API Top 10).

A correção é o DTO de entrada com só os campos que o cliente pode enviar, convertido na transaction
pelo adapter. O mesmo vale na saída: DTO de resposta, nunca a entidade serializada inteira, que
vaza hash de senha, campo interno e dado de outro contexto (API3:2023, exposição excessiva).

## Entrada não confiável

Todo dado que vem de fora (requisição, mensagem de fila, arquivo, resposta de terceiro, cabeçalho)
é não confiável até ser validado. Siga cada um até onde ele é usado.

### SQL (CWE-89)

Interpolação ou concatenação em texto de consulta: `$"... WHERE id = {id}"`, `"..." + filtro`,
`FromSqlRaw` com string interpolada, `ORDER BY` montado com o valor da query. Com Dapper, todo
valor vai como parâmetro; nome de coluna e direção de ordenação saem de uma lista fechada no código.

```csharp
private static readonly Dictionary<string, string> SortColumns = new()
{
    ["createdAt"] = "created_at",
    ["total"] = "total_amount"
};
```

Em EF Core, `FromSql` e `FromSqlInterpolated` parametrizam; `FromSqlRaw` com interpolação, não.

### Comando de sistema (CWE-78)

`Process.Start` com argumento montado de entrada externa, `cmd /c`, `bash -c`. Use
`ProcessStartInfo.ArgumentList`, que passa cada argumento separado, e lista fechada de valores
aceitos.

### Caminho de arquivo (CWE-22)

`Path.Combine(baseDir, nomeRecebido)` aceita `../../` e caminho absoluto, que descarta a base.
Normalize com `Path.GetFullPath` e confira que o resultado começa com o diretório base. Em upload,
o nome de arquivo do servidor é gerado, nunca o enviado.

### Requisição de saída (SSRF, CWE-918)

URL vinda do cliente usada em `HttpClient` (webhook cadastrado, importação por link, preview). O
atacante aponta para `169.254.169.254`, `localhost` ou a rede interna. Lista de hosts permitidos,
resolução de DNS conferida contra faixas privadas, sem seguir redirecionamento.

### Desserialização (CWE-502)

`BinaryFormatter`, `NetDataContractSerializer`, `Newtonsoft.Json` com `TypeNameHandling` diferente
de `None`, ou qualquer serializador que leia o tipo do próprio payload. O atacante escolhe a classe
instanciada. `System.Text.Json` sem polimorfismo aberto não tem esse vetor; polimorfismo, só com
`JsonDerivedType` em lista fechada.

### XML (CWE-611)

`XmlDocument` ou `XmlReader` com `DtdProcessing.Parse` e resolvedor ativo lê arquivo local por
entidade externa. Em .NET moderno o padrão é seguro; procure quem o alterou e o código legado em
.NET Framework.

### Saída para HTML (CWE-79)

Interesse menor em API pura, maior quando a API devolve HTML, monta e-mail ou o front usa
`dangerouslySetInnerHTML`, `v-html` ou `innerHTML` com dado do usuário.

### Expressão regular (CWE-1333)

Regex com quantificador aninhado aplicada a entrada externa trava a thread. Em .NET, sempre com
`matchTimeout`, ou `RegexOptions.NonBacktracking`.

## Segredos

**Pergunta:** alguma credencial está onde não deveria?

- Senha, connection string com senha, chave de API ou chave privada em código, `appsettings.json`,
  `docker-compose.yml`, manifesto Kubernetes sem `Secret`, pipeline de CI (CWE-798).
- Segredo no histórico do git, mesmo removido do arquivo atual: removido do arquivo não é removido
  do repositório. O segredo é revogado e trocado; reescrever histórico é complemento.
- Segredo em variável de ambiente impressa no log de inicialização ou no endpoint de diagnóstico.

Busca: `Password=`, `pwd=`, `ApiKey`, `Secret`, `BEGIN PRIVATE KEY`, `AKIA`, `ghp_`, `xox`.
Ferramenta: `gitleaks` ou `trufflehog` sobre o histórico inteiro.

## Dado sensível em log, trace e erro

**Pergunta:** o que acontece com o dado sensível depois que ele entra no sistema?

A regra BKS é absoluta: senha, token, chave, CPF, cartão e PII não vão para log, trace nem mensagem
de erro, em nenhum nível, nem em debug (CWE-532, CWE-209). Procure:

- objeto de requisição ou entidade logado inteiro (`_logger.LogInformation("{@Request}", request)`);
- cabeçalho `Authorization` registrado por middleware de log de requisição;
- atributo de span com corpo da requisição ou identificador pessoal;
- exceção com dado na mensagem (`throw new X($"CPF {cpf} inválido")`) que acaba no log e no erro;
- query string com dado pessoal, que vai para o log de acesso do proxy.

A correção mascara no ponto de entrada no log, com tipo próprio para o dado sensível cujo
`ToString()` já sai mascarado, ou omite o campo. Filtro global de log ajuda como segunda camada e
não substitui o primeiro: alguém o desliga para depurar e esquece.

## Dependências

- Pacote com vulnerabilidade conhecida: `dotnet list package --vulnerable --include-transitive`,
  `npm audit`, `govulncheck ./...`. Severidade da base é ponto de partida; o achado diz se o código
  usa a parte vulnerável.
- Pacote abandonado, ou com nome parecido com o legítimo (typosquatting).
- Fonte de pacote sem mapeamento: `nuget.config` com feed interno e público misturados permite
  confusão de dependência. Use `packageSourceMapping`.
- Versão flutuante (`*`, `^` sem lockfile) em artefato de produção.

## Configuração

- CORS com `AllowAnyOrigin` junto de credenciais, ou origem refletida do cabeçalho (CWE-942).
- HTTPS desligado, HSTS ausente em aplicação exposta.
- Página de exceção de desenvolvimento ou Swagger aberto em produção.
- Sem limite de tamanho de corpo, de upload ou de página; sem limite de taxa em endpoint caro.
- Cookie de sessão sem `Secure`, `HttpOnly` e `SameSite`.
- Contêiner rodando como root, com sistema de arquivos gravável e segredo em camada de imagem.
- Endpoint de health ou métricas expondo versão, connection string ou variável de ambiente.

## Webhook e integração

- Assinatura do webhook validada antes de qualquer efeito, sobre o corpo bruto recebido, com
  comparação em tempo constante e janela de tempo contra repetição.
- Mensagem repetida é idempotente.
- Resposta de terceiro tratada como entrada não confiável, com timeout explícito.
