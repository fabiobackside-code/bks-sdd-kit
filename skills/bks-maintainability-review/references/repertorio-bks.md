# Repertório BKS (o cânone de engenharia do time)

Versão **1.0.0**. O parecer registra no cabeçalho a versão usada; trocar a versão é mudar a régua.

## A régua

O repertório responde a uma pergunta: um desenvolvedor pleno, formado no cânone de engenharia BKS,
mantém este código sem apoio? O cânone é o conjunto de padrões que o kit gera e que o time pratica
nos seus projetos.

Cada item tem um de três níveis:

| Nível | Quem é | Como pontua |
| --- | --- | --- |
| `DEVE APLICAR` | o pleno aplica sem ajuda | presente onde cabia conta a favor; ausente onde cabia conta contra |
| `RECONHECE` | o pleno entende se estiver documentado | neutro quando o porquê está no `ARCHITECTURE.md` ou num ADR; sem documentação, conta como construção fora do repertório |
| `SÊNIOR` | fora do alcance do pleno | conta contra em código de negócio; neutro quando isolado em componente nomeado, com o porquê documentado |

Item com dois níveis separa consumir de construir. Exemplo: "RECONHECE (herdar e preencher); SÊNIOR
(escrever a base)". O avaliador usa o nível do papel que o código exerce.

Item marcado com uma condição ("em projeto TXC (com contexto de transação)", "PostgreSQL", "domínio rico") só vale onde a
condição existe. Fora dela, o item não se aplica e não pontua.

## Como se usa

O repertório se soma ao `stacks/<linguagem>.md`. A stack diz o que o pleno domina na linguagem; o
repertório diz o que o cânone BKS espera dele. Onde os dois tratam o mesmo assunto, vale o
repertório, que é o mais específico.

Os itens alimentam os eixos da coluna **Eixos**, com mais peso no A4 (aderência ao repertório).
Achado que cita um item traz o id dele: "K-21 ausente: `throw new NotFoundException` no serviço".

A aplicação avaliada nunca é fonte do repertório. Um item que só existisse nela mediria o código
contra ele mesmo.

A coluna **Origem** diz onde o cânone traz a prática. Os rótulos são `kit` (as skills do kit),
`wiki` (a base de conhecimento do time) e `art` (o artigo de referência do contexto de transação).
O número que segue é o de projetos do time que a praticam.

## Siglas

- BKS (o cânone de engenharia do time e o prefixo dos seus tipos).
- DEVE (de `DEVE APLICAR`, o primeiro nível da régua).
- TXC (Transaction Context): o contexto somente leitura que atravessa a transação.
- VO (Value Object) · DTO (objeto de transferência de dados) · DDD (design orientado ao domínio).
- CRUD (cadastro de criar, ler, alterar e excluir) · CQRS (separação entre comando e consulta).
- ACID (atomicidade, consistência, isolamento e durabilidade) · TS (TypeScript).
- SOAP (protocolo de serviço por XML) · WSDL (contrato de serviço SOAP).
- WCF (framework de serviços do .NET Framework) · MVC (Model-View-Controller).
- POST (método HTTP de envio) · TTL (tempo de vida de entrada em cache).
- DLQ (fila de mensagens mortas) · SEDA (arquitetura por estágios conduzidos por eventos).
- HMAC (código de autenticação de mensagem por hash) · SSRF (requisição forjada pelo servidor).
- ECB (modo de cifra por bloco sem vetor de inicialização) · JWT (token assinado JSON Web Token).
- Os eixos de `rubrica.md`: A1 (nomes), A2 (tamanho e complexidade), A3 (indireção), A4 (aderência
  ao repertório), A5 (fronteiras), A6 (localidade de mudança), A7 (testabilidade), A8 (consistência
  e erros), A9 (operabilidade), A10 (documentação do porquê), A11 (duplicação e abstração) e
  A12 (superfície pública).

## 1. Arquitetura e fronteiras

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-01 | Domínio sem infraestrutura nem framework; nenhuma camada que só repassa a chamada | comum | DEVE APLICAR | a favor: `Domain/` só com `System.*`. Contra: `using Npgsql`/`Dapper`/`Microsoft.AspNetCore` no domínio; camada de cerimônia | A5, A3 | kit, wiki · 4 proj. |
| K-02 | Port na fronteira com infraestrutura externa (banco, fila, HTTP, cofre); interface interna só com segunda implementação ou dublê de teste; sem `I{Operacao}UseCase` nem `IRepository<T>` genérico | comum | DEVE APLICAR | a favor: Port por aggregate ou recurso externo. Contra: interface com uma implementação e nenhum dublê | A3, A11 | kit, wiki · 1 proj. |
| K-03 | Adapter de entrada fino: endpoint, consumer, ator ou tela só traduz e chama o serviço ou a sessão; o host não decide | comum | DEVE APLICAR | a favor: endpoint de poucas linhas; núcleo `Core` testado sem plataforma. Contra: regra ou consulta no endpoint, no consumer ou no code-behind | A5, A3, A7 | kit, wiki · 3 proj. |
| K-04 | Uma forma de fluxo por projeto (TXC ou direto), declarada e aplicada no projeto inteiro | comum | DEVE APLICAR | a favor: forma no `.bks-profile.json` ou em ADR, seguida em todo o código. Contra: parte das operações pela sessão, parte por serviço com regra | A4, A6, A11 | kit, wiki, art · 3 proj. |
| K-05 | Composition root curto: `Program.cs` encadeia um `Add{Nome}` por adapter; dependência pelo construtor; tempo de vida respeitado | .NET, Go | DEVE APLICAR | a favor: grafo legível num arquivo. Contra: `IServiceProvider` em serviço (service locator), registro espalhado, `Scoped` capturado em singleton | A6, A3, A5 | kit · 3 proj. |
| K-06 | Organização por contexto de domínio, sem import cruzado entre contextos | comum, Go | DEVE APLICAR em Go; RECONHECE em .NET | a favor: `internal/order/` com tipo, regra e porta. Contra: um contexto espalhado por `domain/`, `ports/` e `adapters/` sem critério | A6, A5 | kit, wiki |
| K-07 | Regra de arquitetura vira teste executável em `tests/{ServiceName}.Tests/Architecture/`: pureza do domínio, fronteira de transporte, superfície pública, baseline de pacotes | .NET, comum | DEVE APLICAR (manter e rodar); RECONHECE (escrever a primeira) | a favor: suíte `Architecture/` que quebra o build com a mensagem da regra. Contra: regra só no documento, fronteira só por convenção num assembly único | A5, A7 | wiki, kit, art · 3 proj. |
| K-08 | Thin client, fat server: regra, validação autoritativa, autorização e segredo só no servidor | comum, TS | DEVE APLICAR | a favor: servidor revalida tudo. Contra: cálculo de saldo, chave de API ou validação só no front | A5 | wiki |
| K-09 | Abstrair só por dor: troca real, uso repetido ou contrato externo que poluiria o domínio; função privada no segundo uso, tipo, interface ou base genérica a partir do terceiro; projeto ou pacote novo só quando paga o preço | comum | DEVE APLICAR | a favor: abstração com uso múltiplo verificável. Contra: abstração para um uso, mapper entre DTOs idênticos, projeto criado para um uso | A11, A3 | wiki, kit · 2 proj. |
| K-10 | Tipo externo não atravessa a porta: contrato WSDL, `.proto`, DTO de fornecedor e erro de driver ficam no adapter | comum | DEVE APLICAR | a favor: adapter converte para modelo e erro do domínio. Contra: tipo gerado em assinatura de Port, `SqlException` no domínio | A5, A8, A6 | kit · 3 proj. |
| K-11 | Componente de execução não decide negócio nem assume controle extra: não repete, não aquece cache, não publica, não purga, não adivinha o ambiente | comum | RECONHECE | a favor: decisão na aplicação, recusa por ambiente na composição. Contra: `ConfirmOnTimeout` em opção, retry dentro de quem só encaminha, SDK lendo `ASPNETCORE_ENVIRONMENT` | A5, A12 | wiki · 3 proj. |
| K-12 | Sem acoplamento de disponibilidade; serviços sobre o mesmo banco são monólito distribuído; decompor só com driver medido | comum | RECONHECE | a favor: o processo sobe com a dependência fora do ar; driver registrado. Contra: health que depende de outro serviço, chamada síncrona obrigatória na subida | A5, A9 | wiki · 2 proj. |

## 2. Orquestração e pipeline

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-13 | Orquestração explícita: sem MediatR nem dispatcher, inclusive para evento de domínio; evento entre domínios sai por broker | comum | DEVE APLICAR | a favor: o fluxo se segue por chamada direta. Contra: `IMediator`, `ISender`, handler resolvido por tipo | A3, A4 | kit, wiki · 3 proj. |
| K-14 | Escrever uma transação TXC: código `{CONTEXTO}.{OPERACAO}`, envelope por fábrica pura, executor por operação; TXC somente leitura e dado entre passos como retorno tipado | .NET, TS, Go | DEVE APLICAR em projeto TXC | a favor: `sealed record` sem setter; `ValidateAsync` devolve o que `ApplyRule` recebe. Contra: `Hydrate`, `With*`, `private set`, `AsyncLocal`, handler ao lado da sessão | A1, A3, A6 | kit, wiki, art |
| K-15 | Base do pipeline: etapas de ordem fixa tipadas, número da etapa como nome do span, hierarquia selada e base genérica com vários parâmetros de tipo | .NET, TS, Go | RECONHECE (herdar e preencher); SÊNIOR (escrever a base) | a favor: base no motor ou em `Application/Pipeline/`, documentada. Contra: base reescrita em cada projeto; genérico aninhado em código de negócio | A3, A4, A9, A12 | wiki, kit · 1 proj. |
| K-16 | Regra num lugar só: `ApplyRule` ou serviço com aggregate; `[10]` sem I/O; executor é o único ponto de escrita e não chama outro; etapa duplicada sai | comum | DEVE APLICAR | a favor: regra localizável pelo nome. Contra: consulta ao banco na `[10]`, regra repetida em dois passos, dois pontos de extensão com o mesmo papel | A6, A11 | kit, wiki · 1 proj. |

## 3. Domínio

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-17 | Linguagem ubíqua: o termo do negócio em classe, método, teste e tabela; um nome por coisa | comum | DEVE APLICAR | a favor: o termo do requisito no código e no teste. Contra: "pedido", "ordem" e "solicitação" para o mesmo conceito | A1 | wiki, kit |
| K-18 | DDD por julgamento: aggregate, VO e evento em domínio rico; entidade simples em cadastro; bounded context só com complexidade essencial | comum | DEVE APLICAR (julgamento tático); RECONHECE (bounded context) | a favor: complexidade do domínio declarada no `ARCHITECTURE.md`. Contra: aggregate root para CRUD, contexto criado para um cadastro | A11, A4, A5 | kit, wiki |
| K-19 | Value Object só para invariante real; não embrulhar todo primitivo | comum | DEVE APLICAR | a favor: VO com validação no construtor. Contra: tipo de um campo para cada `string` sem regra | A11 | kit |
| K-20 | Modelo rico: entidade e aggregate como `class` com factory, setter privado e ID imutável, referência externa só por ID; evento nomeado no passado, publicado depois de persistir | .NET, comum | DEVE APLICAR (domínio rico) | a favor: `Pedido.Criar(...)`, `PedidoConfirmado` após gravar. Contra: `record` de entidade, setter público, aggregate recebendo envelope, publicação antes do commit | A5, A1, A8 | kit, wiki |

## 4. Erros e resultado

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-21 | Erro de negócio é valor tipado; `throw` só para dependência nula, configuração inválida, estado irrecuperável e composição | comum | DEVE APLICAR | a favor: `Fail(...)` para não encontrado e regra violada. Contra: `throw new NotFoundException`, `bool` + `out` | A8, A12 | kit, wiki, art · 4 proj. |
| K-22 | Um tipo de resultado e um estilo de erro por solução, com o nome do componente, nunca anulável | .NET, comum | DEVE APLICAR | a favor: um só tipo de resultado nos adapters. Contra: `bool`, exceção, `BaseReturn` e `Result<T>` convivendo; `Result<T>?`; JSON em `Exception.Data` | A8, A11 | kit · 1 proj. |
| K-23 | Erro de composição falha na subida: configuração validada no startup, registro preguiçoso recusado | .NET | DEVE APLICAR | a favor: `ValidateOnStart`, `InvalidOperationException` no `AddXyz`. Contra: Result no `Program.cs` que ninguém confere, erro adiado para a primeira chamada | A8, A9 | wiki, kit · 2 proj. |
| K-24 | Exceção nunca chega crua ao cliente: vira falha tipada na fronteira; cancelamento propaga; timeout do `HttpClient` separado do cancelamento pelo token | .NET, comum | DEVE APLICAR | a favor: `catch (OperationCanceledException) when (!ct.IsCancellationRequested)`. Contra: stack trace na resposta, `catch (Exception)` que engole cancelamento | A8 | wiki, kit · 3 proj. |
| K-25 | Código de erro por motivo, com descrição, nunca reaproveitado; classificado por natureza e origem; `EventId` do log igual ao código; a aplicação decide o que mostrar | comum | DEVE APLICAR (código por motivo); RECONHECE (eixos natureza × origem, `EventId`) | a favor: catálogo de códigos documentado. Contra: mensagem livre sem código, código reaproveitado, decisão de exibição dentro da biblioteca | A8, A9, A1 | art, wiki · 2 proj. |
| K-26 | Falha em efeito posterior ou de terceiro não altera nem desfaz o resultado confirmado; fica no span e deixa rastro reprocessável | comum | DEVE APLICAR | a favor: estado e motivo persistidos, efeito separado da ação. Contra: timeout de notificação devolvendo falha de transação gravada | A8, A6 | kit, wiki · 1 proj. |
| K-27 | TypeScript: serviço devolve resultado tipado e a rota traduz por `statusFor`; o handler global trata só o técnico | TS | DEVE APLICAR | a favor: rota sem `try/catch` de negócio. Contra: `throw` de negócio capturado pelo handler | A8 | wiki, kit |
| K-28 | Go: `error` idiomático com sentinela ou tipo, `%w`, `errors.Is`/`errors.As`; `panic` só para invariante; `recover` só na fronteira da etapa ou do runner, documentado | Go | DEVE APLICAR | a favor: `fmt.Errorf("ctx: %w", err)`. Contra: comparação de mensagem, `err` descartado, `recover` espalhado | A8 | kit, wiki · 1 proj. |

## 5. Dados e banco

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-29 | Port de dados com métodos do negócio, uma por aggregate ou recurso; nunca `IQueryable<T>` | .NET | DEVE APLICAR | a favor: `IPedidoRepository.ObterPorNumeroAsync`. Contra: `IQueryable` na Port | A5, A1 | kit |
| K-30 | Repositório Dapper: conexão aberta e descartada por operação via `IDbConnectionFactory`; procedure por parâmetros tipados ou contrato JSON, com nomes `{NomeSP}Input`/`{NomeSP}Result` | .NET, SQL | DEVE APLICAR (conexão, parâmetros tipados); RECONHECE (contrato JSON) | a favor: `await using var conn = factory.CreateConnection()`; um sub-padrão por procedure. Contra: conexão em campo, pool próprio, mistura sem critério | A8, A1, A6 | kit |
| K-31 | A procedure transacional é dona da gravação e do ACID; a aplicação não abre transação distribuída nem escreve SQL de gravação; cada esquema tem um dono | SQL, .NET | RECONHECE | a favor: `BEGIN TRAN`/`COMMIT` na procedure, permissão só nas próprias procedures. Contra: `INSERT` em C#, transação atravessando duas bases, serviço lendo tabela de outro esquema | A5, A6, A8 | art, wiki · 2 proj. |
| K-32 | Texto da procedure legível no banco: cabeçalho colado ao `CREATE`, régua em volta de cada bloco numerado, reformatação provada sem mudança de lógica | SQL | DEVE APLICAR | a favor: cabeçalho no `sp_helptext`. Contra: cabeçalho antes do `DROP`, que fica só no arquivo | A10, A2 | kit |
| K-33 | Idempotência por constraint, gravada na mesma transação do negócio; violação de unicidade é sucesso; webhook gravado como chegou; cache, se houver, só de estado terminal | SQL, comum | DEVE APLICAR | a favor: `UNIQUE` na chave natural, `ON CONFLICT DO NOTHING`. Contra: "se não existe, insere" sem constraint; chave só em cache; cache respondendo estado pendente | A8, A6 | kit, wiki · 2 proj. |
| K-34 | Transição de estado atômica no `UPDATE` com guarda de status; idempotência e trava de concorrência são proteções distintas | SQL | RECONHECE | a favor: `UPDATE ... WHERE status = @esperado` com conferência de linhas afetadas. Contra: `SELECT` + `IF` + `UPDATE` | A8 | art, wiki · 1 proj. |
| K-35 | Migration só acrescentada: script publicado não muda, correção é script novo, versão aplicada registrada; o formato do nome é do projeto, declarado no README | .NET, SQL | DEVE APLICAR | a favor: histórico de migrations só cresce. Contra: diff em migration já aplicada | A6, A9 | kit · 2 proj. |
| K-36 | Valor monetário sem `float`/`double`; `decimal` no domínio, menor unidade no banco; sobra de arredondamento com destino único | comum | DEVE APLICAR | a favor: busca por `double` em campo monetário volta vazia. Contra: `double` em saldo | A8, A1 | kit |
| K-37 | Multi-tenant: `tenant_id` em toda tabela de negócio e filtro em toda consulta; tenant do token, nunca do payload | comum | DEVE APLICAR (projeto multi-tenant) | a favor: teste "tenant A não enxerga B". Contra: consulta sem filtro, tenant lido do corpo | A5, A8 | kit, wiki |
| K-38 | O esquema declara a regra: chave natural imutável e nunca reutilizada; coluna de decisão sem `DEFAULT`, com `CHECK` de coerência | SQL | DEVE APLICAR (sem `DEFAULT` com `CHECK`); RECONHECE (chave natural) | a favor: `boolean NOT NULL` sem default; regra de imutabilidade registrada. Contra: default que escolhe comportamento por omissão | A8, A1 | 2 proj. |
| K-39 | PostgreSQL: `now()` é fixo na transação; chave com timestamp usa `clock_timestamp()` ou chave própria | SQL | DEVE APLICAR (PostgreSQL) | a favor: teste de duas gravações na mesma transação. Contra: chave primária com `DEFAULT now()` em auditoria | A8, A7 | 1 proj. |
| K-40 | Integridade sem FK física: índice em toda coluna de junção e rotina de consistência testada | SQL | SÊNIOR | a favor: `check_*()` testada, ADR com o motivo. Contra: ausência de FK sem rotina substituta | A5, A8 | 1 proj. |
| K-41 | Cifra determinística (AES-SIV) só em coluna de busca ou junção, chave fora do banco, custo declarado; nunca ECB, nunca em baixa cardinalidade | comum | SÊNIOR (escolher e implementar); RECONHECE (consumir pela porta) | a favor: cifra atrás de porta, decisão em ADR. Contra: algoritmo de cifra no código de negócio | A4, A5, A10 | wiki · 2 proj. |
| K-42 | Compensação é ação nova com referência cruzada, não desfazimento; estorno marca, não apaga; estado desconhecido é dito como tal e resolvido lendo a fonte | comum | RECONHECE; SÊNIOR (montar a compensação à mão) | a favor: estados `Executed`/`Confirmed`/`Reversed`, `ExecutionUnknown`. Contra: `DELETE` revertendo dado confirmado; timeout tratado como falha certa | A8, A6 | wiki, art · 1 proj. |

## 6. Concorrência e assíncrono

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-43 | Async correto: sem `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`, `async void` ou `async` sem `await`; `CancellationToken` até o driver; `ConfigureAwait(false)` em biblioteca; `ValueTask` só com medição | .NET | DEVE APLICAR | a favor: token propagado; `await` do SDK com `ConfigureAwait(false)`. Contra: bloqueio síncrono, `ValueTask` sem benchmark | A8, A4, A12 | kit · 1 proj. |
| K-44 | Sem fire-and-forget; sem `lock` global nem estado estático mutável | .NET | DEVE APLICAR | a favor: trabalho em paralelo com dono e término. Contra: `Task.Run` solto, `_ = MetodoAsync()`, `static` mutável | A8 | kit · 1 proj. |
| K-45 | Concorrência manual e alocação (`Channel` com capacidade, `SemaphoreSlim`, `ArrayPool<byte>`, `Span`, estágios SEDA) isoladas em adapter nomeado, com capacidade em `IOptions<T>` e carga medida documentada | .NET, comum | RECONHECE isolado; SÊNIOR em código de negócio | a favor: concorrência confinada ao adapter TCP, carga no `ARCHITECTURE.md`. Contra: `Channel.CreateUnbounded`, semáforo sem uso, `Span` ou pool sem medição em código de negócio | A4, A8, A9, A2 | kit · 1 proj. |
| K-46 | Go: toda goroutine com término; `context.Context` primeiro parâmetro e nunca em campo; `errgroup` com `SetLimit`; `defer` fora de laço; `go test -race` | Go | DEVE APLICAR | a favor: `-race` no CI. Contra: goroutine sem cancelamento, `select` sem `ctx.Done()` | A8, A9 | kit |
| K-47 | Objeto caro de obter (`Encoding` 1252, provider) obtido uma vez; sem `GC.Collect` forçado | .NET | DEVE APLICAR | a favor: campo estático somente leitura. Contra: `GetEncoding` por chamada, `GC.Collect()` em `src/` | A2, A4 | 1 proj. |

## 7. Integração e mensageria

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-48 | Socket TCP como adapter: frame com prefixo de tamanho, parser tolerante a fragmentação, heartbeat com timeout, reconexão com jitter | .NET, Go | RECONHECE (manter com documentação); SÊNIOR (escrever o framing) | a favor: framing só no adapter, com teste de fragmentação. Contra: "uma leitura = uma mensagem", `TcpClient.Connected` como detector de queda | A4, A5 | wiki, kit |
| K-49 | Mensageria confiável: outbox para o dual-write banco + broker; consumidor at-least-once que confirma depois de processar ou gravar na DLQ; nunca auto-ack | comum, TS, Go | DEVE APLICAR (consumidor); RECONHECE (outbox) | a favor: ordem processa → DLQ → commit; outbox na mesma transação. Contra: auto-ack, retry de mensagem malformada, publicar dentro da transação | A8, A9 | kit, wiki |
| K-50 | Webhook: entrada com HMAC sobre o corpo bruto antes de qualquer efeito e 2xx rápido; saída assinada, com retry, DLQ e proteção contra SSRF | comum | DEVE APLICAR | a favor: fila ou outbox depois do `INSERT`. Contra: processamento pesado no handler | A8, A5 | wiki, kit |
| K-51 | Cliente HTTP por `IHttpClientFactory` (typed client) com uma política de resiliência e timeout explícito; repetição só onde decidida (sem 307 reenviando POST) | .NET, Go | DEVE APLICAR (factory, timeout); RECONHECE (redirect e retry único) | a favor: `AddStandardResilienceHandler` por cliente, `AllowAutoRedirect = false` onde repetir é perigoso. Contra: `new HttpClient()`, retry em dois níveis | A8, A9 | kit · 2 proj. |
| K-52 | Cache com contrato do negócio, expiração declarada e queda para a fonte quando falha | comum | DEVE APLICAR | a favor: `I{Recurso}Cache.ObterSaldoAsync`. Contra: `ICache` genérico, entrada sem TTL, falha de cache derrubando a operação | A8, A11 | kit |

## 8. Segurança

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-53 | O identificador do titular vem da credencial, nunca da URL ou do corpo; posse do recurso conferida | comum | DEVE APLICAR | a favor: filtro por `UserId` do token. Contra: `ownerId` lido do request | A5 | kit |
| K-54 | Autenticação declarada por porta: `RequireAuthorization()` em todo grupo, validação de `aud`; porta aberta tem a rede que a protege no README | .NET, Go | DEVE APLICAR | a favor: grupos protegidos por padrão. Contra: endpoint esquecido sem autorização | A5, A10 | kit, wiki |
| K-55 | Nada sensível em log, erro, telemetria ou notificação; mensagem de erro não repete entrada externa nem `ex.Message` de terceiro; chave e URL que serve de credencial fora de log e trace | comum | DEVE APLICAR | a favor: notificação com categoria e ponteiro; causa em `InnerException`. Contra: CPF ou token em tag, `$"... {valorRecebido}"` em recusa | A9, A8, A5 | kit · 3 proj. |
| K-56 | Configuração e segredo são categorias distintas: seção por adapter com `IOptions<T>`, segredo por Secret ou cofre, nada no código; ambiente não declarado é o mais restrito; biblioteca não cacheia segredo | comum | DEVE APLICAR; RECONHECE (cache de segredo dentro do SDK) | a favor: tabela config × segredo por ambiente no README; seed fictício que se recusa sem marca. Contra: IP, chave ou connection string em `src/`; `process.env` espalhado; `_ => default` que engole configuração inválida | A9, A10, A8 | kit, wiki · 5 proj. |
| K-57 | Token, assinatura e hash comparados em tempo constante; erro de cifra sem oráculo (causas distintas, mesmo código e mensagem) | comum | DEVE APLICAR (tempo constante); RECONHECE (manter anti-oráculo); SÊNIOR (desenhar) | a favor: `timingSafeEqual`/`ConstantTimeCompare`; teste que compara os dois casos. Contra: `==` em segredo, código de erro que distingue a causa | A8 | wiki, kit · 1 proj. |
| K-58 | A mesma imagem em todos os ambientes, só a configuração muda; nenhum adapter preso a serviço proprietário de nuvem | comum | DEVE APLICAR | a favor: um Dockerfile, variáveis por ambiente. Contra: build por ambiente | A9 | wiki |
| K-59 | Validação de JWT que não confia no header (`alg` de lista fixa, `kid` obrigatório) nem no discovery (issuer igual à authority, `jwks_uri` na mesma origem) | .NET | SÊNIOR | a favor: validador sem opção de desligar verificação. Contra: `ValidateIssuer = false`, algoritmo escolhido pelo token | A5, A8 | 1 proj. |
| K-60 | Autorização num lugar só, por tipo de transação, antes da validação | comum | RECONHECE | a favor: matriz perfil × tipo consultada num ponto. Contra: checagem de perfil espalhada por endpoint | A5, A6 | 2 proj. |

## 9. Observabilidade

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-61 | Telemetria embutida na base: span por etapa sem código do desenvolvedor; sem `Activity` à mão nem `try/catch` só para span | comum | DEVE APLICAR | a favor: `step.{ordem}` com o código como tag. Contra: `StartActivity` espalhado em regra e repositório | A9, A3 | kit, wiki, art |
| K-62 | Span não é logger: tag de negócio, nunca payload, objeto serializado ou stack trace; log por `ILogger`, nunca `Console` | .NET | DEVE APLICAR | a favor: tags curtas de negócio. Contra: `JsonSerializer.Serialize(obj)` em tag, span por linha de log, `Console.WriteLine` | A9 | kit · 1 proj. |
| K-63 | Métrica com atributo de conjunto fechado (identificador vai no span); histograma de duração lido em percentil | comum | DEVE APLICAR | a favor: p95/p99 em painel. Contra: `userId` ou chave de idempotência em tag de contador; só média | A9 | kit, wiki · 1 proj. |
| K-64 | Log de alto volume por `[LoggerMessage]`, sem interpolação | .NET | RECONHECE | a favor: `[LoggerMessage]` em classe parcial. Contra: `$"..."` em `LogInformation` | A9, A4 | kit · 1 proj. |
| K-65 | Correlação ponta a ponta: `traceparent` em cada salto; identificador de mensagem como chave de idempotência | comum | DEVE APLICAR | a favor: o mesmo trace atravessa API, fila e banco. Contra: correlação perdida no consumidor | A9 | wiki |

## 10. Testes

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-66 | Teste por camada: domínio sem mock (só `new()`); serviço com as Ports substituídas; no TXC, cada passo do executor e o replay da `[20]` | .NET | DEVE APLICAR | a favor: um teste por método do serviço ou passo do executor. Contra: domínio testado só por integração | A7 | kit |
| K-67 | Dublê honesto: recusa o que o real recusa, escrito a partir de resposta real observada; suíte de conformidade, vetores compartilhados e teste de paridade quando a regra existe em dois caminhos | comum | DEVE APLICAR (dublê honesto); RECONHECE (conformidade, vetores, paridade) | a favor: fake com envelope capturado do servidor; base abstrata de testes para quem implementa a porta. Contra: `Verify(... It.IsAny ...)` como única asserção; fake por suposição | A7, A12 | wiki, kit · 3 proj. |
| K-68 | Integração de adapter contra a tecnologia real (Testcontainers), separada por `Trait`; o `dotnet test` de um clone limpo passa sem Docker | .NET, comum | DEVE APLICAR | a favor: `[Trait("Category","Integration")]` com filtro documentado. Contra: `UseInMemoryDatabase` como teste de adapter; suíte padrão que exige container; integração nunca rodada | A7 | wiki, kit · 2 proj. |
| K-69 | Asserção nativa: `Assert` do xUnit, um framework de mock só; em Go, `if got != want`, table-driven | .NET, Go | DEVE APLICAR | a favor: `Assert.Equal`. Contra: `.Should()`, dois frameworks de mock | A7, A4 | kit · 1 proj. |
| K-70 | Projeto de testes em `tests/{ServiceName}.Tests/`, espelhando a produção (`Unit/`, `Integration/`, `Shared/`), nome `Método_Condição_Resultado` em inglês e Arrange/Act/Assert | .NET | DEVE APLICAR | a favor: o teste se acha pelo caminho do código. Contra: projetos de teste espalhados, nome sem condição, `#region` | A7, A1 | kit, wiki · 1 proj. |
| K-71 | Teste prova a decisão: falha de composição, registro de DI (cada adapter resolve), mensagem repetida com um efeito só; defeito corrigido vem com o teste que o reproduz; teste instável se prova com várias execuções | comum | DEVE APLICAR | a favor: teste que falharia com a implementação vazia; teste que monta o contêiner. Contra: só caminho feliz; correção sem teste; "passou uma vez" | A7 | wiki, kit · 2 proj. |
| K-72 | Relógio injetado (`TimeProvider`/`FakeTimeProvider`); timer só pelo relógio injetado | .NET | DEVE APLICAR | a favor: `TimeProvider` no construtor. Contra: `DateTime.Now` ou `Task.Delay` em código com prazo | A7 | 1 proj. |
| K-73 | Cobertura com exclusão explícita de DTO, migration, código gerado e wrapper de transporte | .NET | RECONHECE | a favor: exclusões no `.csproj` ou no `sonar-project.properties`. Contra: percentual inflado por DTO | A7 | kit |
| K-74 | Teste e exemplo dentro da solution; o exemplo usa só a superfície pública e cresce com cada recurso | .NET | DEVE APLICAR | a favor: projeto de exemplo sem `InternalsVisibleTo`, com `.http`. Contra: guarda que só roda quando executada à parte; exemplo que usa interno | A7, A12, A10 | 2 proj. |

## 11. Documentação e comentário

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-75 | No código, só contrato (resumo de uma linha em membro público) e guarda contra regressão (até duas linhas, o quê); decisão, trade-off e histórico no `ARCHITECTURE.md` | comum | DEVE APLICAR | a favor: "Não é record: ToString() exporia a ApiKey." Contra: bloco de trade-off ou histórico, comentário que repete o nome | A10 | kit, wiki · 5 proj. |
| K-76 | Teto de cinco linhas por bloco; sem marca de severidade, sem ponteiro ("Ver ARCHITECTURE.md"), sem código de spec; regra guardada por `CommentBudgetTests` | comum, Go | DEVE APLICAR (cumprir e manter a guarda verde); RECONHECE (escrever a guarda) | a favor: `CommentBudgetTests` verde. Contra: emoji de alerta, `[ADR-012]`, `TASK-021` em comentário | A10, A7 | kit, wiki · 5 proj. |
| K-77 | `README.md` e `ARCHITECTURE.md` na mesma entrega que muda tipo público ou decisão estrutural; o README diz uso e configuração, sem ADR nem spec no corpo; o `ARCHITECTURE.md` abre dizendo que guarda o porquê | comum | DEVE APLICAR | a favor: commit que cria tipo público toca os dois. Contra: tipo público novo sem documentação; README com `ADR-0xx`; `ARCHITECTURE.md` que repete o README | A10, A12 | kit · 5 proj. |
| K-78 | Documentação viva no presente: sem "passa a", "antes era" nem nota de migração; histórico em ADR e JOURNAL | comum | DEVE APLICAR | contra: "agora", "deixou de", tabela antes/depois em README, ARCHITECTURE ou comentário | A10 | 2 proj. |
| K-79 | ADR curto e local para decisão cara de reverter, com alternativas, ganho, custo e dívida deliberada com gatilho; exceção ao padrão vive no ADR do projeto que a sofre | comum | RECONHECE (o pleno lê e segue; escreve com revisão) | a favor: `decisions/` com alternativas descartadas; seção de dívida deliberada. Contra: desvio de padrão ou atalho sem registro | A10, A4 | wiki · 3 proj. |

## 12. Nomes, idioma e tipos

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-80 | Sem abreviação; sufixo `Async`; prefixo `I`; namespace igual à pasta, com prefixo do produto | .NET | DEVE APLICAR | a favor: `customerId`. Contra: `custId`, namespace divergente do caminho | A1, A6 | kit · 1 proj. |
| K-81 | Código em inglês; texto para quem lê (comentário, mensagem, documentação) em português com acentuação; sem mistura de idioma no mesmo projeto; nome de negócio em português só por ADR do projeto | comum | DEVE APLICAR | a favor: uma regra de idioma declarada e seguida. Contra: comentário sem acento; `Cifrar` e `Encrypt` convivendo | A1 | 8 proj. |
| K-82 | Convenção de enum única por projeto: PascalCase por padrão, outra só por ADR do projeto | .NET | RECONHECE | a favor: convenção declarada. Contra: `EnumXxx` maiúsculo e PascalCase no mesmo projeto | A1, A4 | 2 proj. |
| K-83 | Tipo pela semântica: `sealed record` para TXC, envelope, DTO e settings; `readonly record struct` para VO pequeno e resultado; `class` para entidade; `sealed` em classe concreta; tipo que guarda segredo não é `record` | .NET | DEVE APLICAR | a favor: tabela de tipos seguida. Contra: entidade `record`, DTO mutável, `record` com `ApiKey` | A1, A8, A9 | kit · 2 proj. |
| K-84 | Tipagem forte: `dynamic`, `object` e `any` só com justificativa; `any` só na borda de serialização | comum | DEVE APLICAR | a favor: tipos de Zod por `z.infer`. Contra: `object` em contrato de domínio | A4 | kit |
| K-85 | `StringComparison.Ordinal` em comparação que não é linguística | .NET | DEVE APLICAR | contra: comparação cultural em chave ou token | A8 | kit |
| K-86 | Minimal API devolve `IResult` (`Results`, `TypedResults`), não `IActionResult` | .NET | DEVE APLICAR | contra: `IActionResult` em rota Minimal API | A4 | 1 proj. |

## 13. Simplicidade e trade-off

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-87 | Solução mais simples que resolve; nenhum mecanismo que nem o requisito nem o sistema de origem pedem | comum | DEVE APLICAR | a favor: feature em poucos arquivos com papel claro. Contra: Event Sourcing, CQRS ou hierarquia sem driver; chave, retry ou estado que o legado não tem | A11, A3 | kit, wiki · 1 proj. |
| K-88 | Legibilidade de método: guard clause e retorno antecipado no lugar de `else`; método público curto que delega a privados com nome de regra; despacho por `switch`; as regras de classe do Object Calisthenics são guia, não regra | comum | DEVE APLICAR | a favor: caminho feliz à esquerda; método público lido como roteiro. Contra: toda a regra inline no método público; classe criada só para obedecer regra | A2, A1, A11 | kit · 1 proj. |
| K-89 | Régua de previsibilidade: toda operação com a mesma forma; a regra tem endereço fixo; o que não deve variar fica no componente | comum | DEVE APLICAR | a favor: o pleno deduz onde cada coisa está. Contra: cada serviço organizado do jeito do autor | A3, A6, A4 | art, wiki |
| K-90 | Higiene: sem código morto, registro duplicado, pacote sem uso, `#region`, adapter não declarado ou opção pública que não funciona | comum | DEVE APLICAR | a favor: build sem aviso de import não usado. Contra: `XxxOld.cs`, `AddXxx2`, `Configure<T>` repetido, valor de enum sem implementação | A11, A2, A12 | kit · 2 proj. |

## 14. Superfície pública, pacotes e legado

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-91 | Pacote novo só com aprovação registrada e baseline guardada por teste; dependência usada é referenciada diretamente; pré-release com versão exata e critério de troca | .NET, comum | DEVE APLICAR | a favor: `PACOTES.md` ou allowlist com teste. Contra: `PackageReference` sem registro; tipo de pacote transitivo usado sem referência própria; faixa flutuante de beta | A4, A12, A9 | kit, wiki · 4 proj. |
| K-92 | Mudança de contrato público sobe a major; valor de enum novo sobe a minor | .NET | DEVE APLICAR | a favor: CHANGELOG e versão coerentes. Contra: quebra de contrato em patch | A12 | 2 proj. |
| K-93 | Namespace pelo papel de quem consome (`Hosting`, `Extensibility`); interface pública com prefixo do produto; ponto de extensão pequeno, com implementação padrão; implementação `internal sealed` | .NET | RECONHECE | a favor: raiz do pacote enxuta; `IBksIdempotencyCache.FindAsync` só. Contra: `Helpers`, `Utils`; interface larga de extensão | A12, A1 | wiki, kit · 1 proj. |
| K-94 | Biblioteca agnóstica de hospedagem: entrega o serviço ou validador, não o middleware; sem `FrameworkReference` de ASP.NET Core | .NET | RECONHECE | a favor: SDK usável em Worker e Console. Contra: SDK que referencia `Microsoft.AspNetCore.App` | A5, A12 | 2 proj. |
| K-95 | SDK em Go: obrigatório posicional, opcional por functional option; SemVer sério, `// Deprecated:` sem quebrar | Go | DEVE APLICAR | a favor: `New(required, opts ...Option)`. Contra: struct de config pública que quebra a cada campo | A12 | kit |
| K-96 | Legado 4.7: WCF é adapter inbound sem regra; TopShelf só hospeda; Akka.NET é infraestrutura, com a regra testável sem `ActorSystem`; DI no composition root | .NET legado | RECONHECE | a favor: `Start`/`Stop` só acionam a sessão. Contra: regra dentro do `.svc` ou do ator | A4, A5, A7 | kit |

## 15. Específicos de Go e TypeScript

| K | Prática | Stack | Nível | Sinal no código (a favor / contra) | Eixos | Origem |
|---|---|---|---|---|---|---|
| K-97 | Interface declarada no consumidor, pequena; aceite interface, retorne struct; wiring manual em `main.go`; `init()` sem trabalho que falha | Go | DEVE APLICAR | a favor: interface ao lado de quem a usa. Contra: pacote `ports/` com todas as interfaces, interface de quinze métodos | A5, A3, A12 | kit |
| K-98 | Getter só no TXC e em VO com invariante; struct de dados com campo exportado | Go | DEVE APLICAR | a favor: getter só onde impede mutação. Contra: getter e setter em struct de dados | A11, A8 | kit |
| K-99 | Go sem tradução de .NET linha a linha: sem `Result[T]`, sem mapeamento automático, sem `chan` em pipeline síncrona; `gofmt`, `go vet`, `golangci-lint` e `gosec` no CI | Go | DEVE APLICAR | a favor: código que um programador Go reconhece. Contra: construção .NET transplantada | A4, A9 | kit |
| K-100 | API TypeScript: módulo por domínio, rota sem controller MVC, Zod em toda rota com body ou query, `server.ts` só faz bootstrap e `app.ts` só registra | TS | DEVE APLICAR | a favor: `{módulo}.routes.ts` com schema Zod. Contra: `process.env` no módulo, regra no `app.ts` | A3, A4 | kit |
