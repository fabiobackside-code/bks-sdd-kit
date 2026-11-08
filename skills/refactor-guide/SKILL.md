---
name: refactor-guide
description: >
  Conduz refatoração que muda a estrutura sem mudar o comportamento: estabelece rede de testes
  antes de mexer (testes de caracterização quando não há teste), avança em passos pequenos e
  verificáveis, faz um tipo de mudança por commit, separa refatoração de correção de bug e de
  otimização, escolhe o alvo por cheiro concreto (duplicação, método longo, classe que faz
  demais, acoplamento) e confere o padrão BKS — dependência apontando para dentro, Domain sem
  infraestrutura, Object Calisthenics. Use SEMPRE que o pedido for refatorar, limpar, quebrar
  método ou classe grande, extrair, desacoplar, reorganizar ou modernizar código, ou mexer em
  legado sem teste. Trigger: refatorar, refactor, refatoração, código legado, legacy code,
  método longo, classe grande, god class, code smell, cheiro de código, extrair método,
  desacoplar, characterization test, teste de caracterização, "aproveita e corrige".
---

# refactor-guide — mudar a forma sem mudar o que o código faz

**Refatoração** é mudar a estrutura interna do código sem mudar o comportamento observável. Essa
definição, de Martin Fowler, é o que separa refatorar de reescrever. Se o comportamento mudou,
não foi refatoração, e a rede de testes precisa dizer isso.

Esta skill segue duas fontes: *Refactoring*, 2ª edição, de Fowler, para os movimentos e os
cheiros; e *Working Effectively with Legacy Code*, de Michael Feathers, para mexer em código sem
teste.

## 1. Separe o pedido antes de tocar no código

Pedidos de refatoração costumam vir misturados. Desmonte em mudanças de natureza diferente e diga
ao usuário a ordem proposta:

| Natureza | O que é | Como se prova |
|---|---|---|
| **estrutura** | extrair, renomear, mover, dividir; comportamento idêntico | a rede de caracterização continua verde sem ajuste |
| **comportamento** | corrigir bug, mudar regra, novo caso | um teste que falhava passa a passar; o teste que fixava o erro muda junto, de propósito |
| **desempenho** | trocar estrutura de dados ou algoritmo por velocidade | uma medição antes e depois, no cenário real |

Cada natureza vai num commit próprio, de preferência num PR próprio. Misturar as três faz o
revisor não saber se uma diferença de saída é o bug corrigido ou uma regressão nova.

A ordem que costuma funcionar: rede de caracterização, depois estrutura, depois comportamento.
Desempenho entra só com medição, como na seção 5. Às vezes a correção de bug vem antes, por ser
urgente: tudo bem, desde que seja uma mudança isolada com o próprio teste.

## 2. Rede antes da primeira mudança

Sem teste, não se refatora: se edita e torce. Antes do primeiro movimento:

1. **Há teste cobrindo o trecho?** Rode e confirme que está verde. Confira se cobre os caminhos
   que você vai mexer, não só o caminho feliz.
2. **Não há?** Escreva **testes de caracterização** — testes que registram o que o código faz
   hoje, não o que deveria fazer. Inclusive o comportamento errado: o bug de arredondamento fica
   fixado no teste como está. Ele só muda no commit de correção, onde a mudança fica visível.
3. **O código não deixa testar** — dependência estática, `DateTime.Now`, banco aberto no meio do
   método? Use um ponto de separação mínimo, como extrair uma interface ou injetar um relógio.
   Essa primeira mudança é feita com o máximo de cuidado e o mínimo de alcance.

Como escrever caracterização em C# com xUnit, como achar os casos e como quebrar dependência sem
rede estão em `references/rede-de-caracterizacao.md`.

**Não comece a quebrar o método enquanto a rede não estiver verde e acordada com o usuário.**

## 3. Alvo guiado por cheiro concreto

"Está feio" não é alvo. Nomeie o cheiro, aponte onde ele está e diga o movimento que o resolve:

| Cheiro | Sinal no código | Movimento típico |
|---|---|---|
| método longo | mais de uma tela; comentário separando "etapas" | extrair função por etapa |
| duplicação | o mesmo bloco em dois lugares, com variação pequena | extrair e parametrizar |
| classe que faz demais | campos usados só por metade dos métodos | extrair classe |
| acoplamento | regra de negócio chamando banco, HTTP ou fila direto | introduzir porta e inverter a dependência |
| obsessão por primitivo | `decimal` de dinheiro e `string` de CPF circulando soltos | value object, onde há invariante |
| condicional em cascata | `switch` por tipo repetido em vários métodos | polimorfismo ou tabela de estratégia |

O catálogo completo, com antes e depois em C#, está em `references/cheiros-e-movimentos.md`.

## 4. Passos pequenos, sempre verdes

- **Um movimento por vez.** Extrair, rodar os testes, commitar. Depois o próximo.
- **Testes verdes entre todo passo.** Ficou vermelho? Desfaça o último passo em vez de depurar
  em cima de dois passos misturados.
- **Um tipo de mudança por commit.** Renomear num, mover noutro, extrair noutro. O commit diz o
  movimento: `refactor: extrai cálculo de frete de CheckoutService`.
- **Ferramenta antes de mão.** Renomear e extrair pela IDE ou pelo LSP é mais seguro que editar
  texto.

Como montar a sequência de commits e o PR está em `references/sequencia-e-commits.md`.

## 5. Desempenho pede número

"Fica mais rápido" é hipótese, não premissa. Antes de trocar lista por dicionário, ou qualquer
estrutura por outra:

1. Existe problema medido? Qual operação, com que volume, em que tempo?
2. O trecho está no caminho quente? Um profiler ou um benchmark diz; intuição não.
3. Meça antes, com BenchmarkDotNet ou o perfil de produção, e meça depois, no mesmo cenário.

Sem medição, a troca não entra junto com a refatoração. Fica registrada como hipótese a medir.
Num laço de cinco itens, `List<T>` costuma ganhar de `Dictionary<TKey, TValue>`.

## 6. Confira o padrão BKS no destino

A refatoração é a chance de aproximar o código do padrão da casa, um passo por vez:

- **Dependência aponta para dentro:** Adapters → Application → Domain, nunca o contrário.
- **Domain só com `System.*`.** ORM, driver ou cliente de fila no domínio sai por uma porta em
  `Ports/Outbound/`.
- **Erro de negócio vira resultado tipado**, não exceção que escapa da pipeline.
- **Calisthenics por julgamento:** um nível de indentação, sem `else` onde a guarda resolve,
  Tell, Don't Ask. Não crie classe artificial para cumprir regra.
- **Sem MediatR nem dispatcher**, mesmo que a refatoração pareça pedir.

Como cada regra aparece num refactor real, com exemplo, em `references/destino-bks.md`. As regras
completas estão na skill `bks-standards`.

## 7. Entrega

Antes de declarar pronto:

- [ ] A rede de caracterização ou de teste roda verde, e a contagem de testes está na resposta.
- [ ] Cada commit tem um tipo só de mudança, e a mensagem diz qual.
- [ ] Correção de bug e otimização estão fora dos commits de estrutura, ou explicitamente adiadas.
- [ ] Toda troca por desempenho tem a medição antes e depois.
- [ ] Nenhuma dependência nova aponta para fora, e o Domain continua sem infraestrutura.
- [ ] `README.md` e `ARCHITECTURE.md` refletem tipo público movido, renomeado ou criado.

## Referências

| Arquivo | Quando abrir |
|---|---|
| `references/rede-de-caracterizacao.md` | não há teste, ou o código resiste a ser testado |
| `references/cheiros-e-movimentos.md` | ao escolher o alvo e o movimento |
| `references/destino-bks.md` | ao mover código entre camadas ou extrair porta |
| `references/sequencia-e-commits.md` | ao planejar a ordem dos passos, os commits e o PR |
