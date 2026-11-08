# Isolamento — reduzir o espaço de busca pela metade

Quando a stack não aponta a causa, a busca é sistemática: cada experimento elimina metade das
possibilidades. Mudar várias coisas de uma vez e ver se melhora não elimina nada.

## Funcionava antes: git bisect

Se existe um commit bom e um ruim, o `git bisect` acha o commit que introduziu o defeito em
log₂(n) passos: 1000 commits, dez testes.

Com o teste que reproduz, o processo inteiro é automático:

```
git bisect start
git bisect bad HEAD
git bisect good v2.3.0
git bisect run dotnet test --filter "FullyQualifiedName~ShippingCalculatorTests"
git bisect reset
```

O comando passado ao `run` sai com 0 quando o commit é bom e com outro código quando é ruim; 125
diz para pular o commit (não compila, por exemplo). O teste de reprodução precisa existir fora da
árvore versionada durante o bisect, ou ser aplicado em cada passo, porque os commits antigos não o
têm.

O commit encontrado diz **onde** o comportamento mudou. Ainda é preciso entender **por quê**: a
mudança pode ter exposto um defeito antigo, e não criado um novo.

Sem histórico útil (commit gigante, defeito em dependência), aplique a mesma ideia à mudança:
reverta metade do diff, teste, repita. Para dependência, fixe a versão anterior do pacote e
confirme.

## Funciona num ambiente e não em outro

A diferença entre os dois ambientes contém a causa. Liste e elimine uma por vez:

| Dimensão | O que comparar |
|---|---|
| código | commit e imagem realmente implantados, não o que se acredita que está |
| dependência | versão resolvida dos pacotes (lockfile), runtime, imagem base |
| configuração | variáveis de ambiente, `appsettings.{Environment}.json`, feature flag, segredo |
| dado | volume, registros antigos com formato anterior, nulos que a base de teste não tem |
| cultura e fuso | `CultureInfo.CurrentCulture` (separador decimal, formato de data), `TimeZoneInfo.Local`, horário de verão |
| sistema | sistema de arquivos sensível a maiúsculas, separador de caminho, fim de linha, permissão |
| rede | proxy, DNS, certificado, timeout de balanceador, MTU |
| recurso | memória e CPU limitadas no contêiner, número de núcleos, pool de conexões |
| carga | concorrência real versus uma requisição por vez |

Cultura e fuso respondem por boa parte do "só no servidor": `decimal.Parse("10.50")` com cultura
pt-BR lê mil e cinquenta, e `DateTime.Now` no servidor em UTC muda o dia do pedido. O código de
domínio usa `CultureInfo.InvariantCulture` para formato de máquina e recebe o tempo por uma porta
(`TimeProvider` no .NET), o que também torna o teste determinístico.

## Falha com um dado e não com outro

Reduza a entrada pela metade até o menor caso que falha, como em `reproducao.md`. Depois procure o
que esse caso tem de diferente: campo vazio, lista vazia, valor nos limites (zero, negativo,
máximo), texto com acento ou emoji, data de 29 de fevereiro, fim de mês, registro criado antes de
uma migration.

## Intermitente e flaky

Defeito que aparece às vezes tem causa determinística que depende de algo que varia. As fontes, da
mais comum para a menos:

1. **Ordem dos testes e estado compartilhado**: campo estático, singleton, banco não limpo entre
   testes, variável de ambiente alterada. Rode o teste isolado e depois a suíte; se só falha na
   suíte, rode em ordem fixa e divida a suíte ao meio até achar o vizinho que contamina.
2. **Tempo**: `DateTime.Now`, `Task.Delay` como sincronização, expiração calculada perto da
   meia-noite, teste que espera "tempo suficiente". Troque por `TimeProvider` falso e espera por
   condição.
3. **Concorrência**: dois fluxos lendo e escrevendo o mesmo estado sem coordenação. Aumente a
   pressão para tornar frequente o que é raro: rode o teste em laço, com paralelismo, até falhar.
4. **Recurso externo**: rede, banco compartilhado, serviço de terceiro. No teste, Testcontainers
   isola; em produção, timeout explícito e o log da dependência no mesmo traceId.
5. **Ordem de coleção não garantida**: `Dictionary`, `HashSet`, mapa em Go, resultado de `SELECT`
   sem `ORDER BY`.

Para tornar frequente o que é raro:

```
for i in $(seq 1 200); do dotnet test --filter "FullyQualifiedName~OrderAccessTests" || break; done
```

```
go test -run TestReserveStock -race -count=200 ./...
```

O `-race` do Go instrumenta acesso concorrente e aponta as duas goroutines que disputam a mesma
memória. Em .NET não há equivalente embutido; a evidência vem do teste em laço com paralelismo e do
dump das threads quando trava.

Teste flaky não se resolve com retry automático na pipeline. O retry esconde um defeito que, em
metade dos casos, existe também no código de produção.

## Lento ou travando

Meça antes de supor. A hipótese de desempenho mais óbvia costuma estar errada.

- **Trace distribuído** mostra onde o tempo foi: banco, chamada externa ou código.
- **`dotnet-counters`** mostra pool de threads, GC e exceções por segundo em tempo real; fila do
  pool de threads crescendo indica bloqueio síncrono em código assíncrono.
- **`dotnet-trace`** e **`pprof`** em Go mostram o perfil de CPU.
- **Dump** (`dotnet-dump collect`, depois `analyze` com `clrstack -all`) mostra onde cada thread
  está parada num travamento.
- No banco, o **plano de execução** da consulta lenta, com os parâmetros reais.

## Registro dos experimentos

Durante a investigação, mantenha uma lista curta: hipótese, experimento, resultado. Ela evita
repetir o mesmo teste, mostra quando é hora de voltar ao erro original, e vira o resumo da causa
na entrega.

```
H1: endereço nulo em pedido de retirada → teste com pedido de retirada → falha igual à produção. Confirmada.
H2: tabela de frete sem a faixa do CEP → teste com CEP fora da faixa → resultado de falha tipada. Derrubada.
```
