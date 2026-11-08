---
name: debug-assistant
description: >
  Depuração disciplinada, do sintoma à causa: reproduz antes de corrigir, captura o defeito num
  teste que falha, lê a mensagem e a stack inteiras, isola a variável (git bisect, diferença entre
  ambientes, dado de entrada, concorrência) e segue hipótese, experimento e conclusão. Corrige a
  causa, não o sintoma, e deixa o teste de regressão. Use SEMPRE que o usuário relatar bug, erro,
  exceção, stack trace, teste falhando, comportamento inesperado ou regressão; quando pedir um
  remendo direto ("põe um null check", "coloca um try/catch", "aumenta o timeout"); e para entender
  comportamento obscuro de código legado. Trigger: bug, debug, depurar, NullReferenceException,
  exception, stack trace, erro em produção, funcionava antes, regressão, intermitente, flaky,
  funciona na minha máquina, só em produção, teste quebrando, race condition, deadlock, timeout.
---

# debug-assistant — reproduzir, isolar, depois corrigir

Correção sem reprodução é palpite com commit. O defeito some do sintoma observado e reaparece em
outro lugar, e ninguém sabe se a mudança corrigiu algo ou só mudou o caminho.

Esta skill segue uma ordem fixa: **reproduzir, ler, isolar, explicar, corrigir, travar**. Pular
etapa é permitido só quando a etapa anterior já deu a resposta, e isso se diz em voz alta.

## 1. Remendo pedido não é diagnóstico

O pedido costuma chegar com a solução pronta: "põe um null check", "envolve num try/catch",
"aumenta o timeout", "adiciona um retry". Cada um desses esconde o sintoma e deixa a causa:

- o **null check às cegas** troca uma exceção visível por um valor ausente que segue fluxo adiante.
  O frete passa a sair zero, ou o pedido sai sem frete, e o erro reaparece longe da origem, sem
  stack trace, às vezes como dado errado gravado no banco;
- o **try/catch** que engole a exceção apaga a única evidência que existia;
- o **timeout maior** e o **retry** escondem lentidão ou corrida até a carga crescer.

Não aplique o remendo como correção. Diga por que em duas frases, peça o mínimo que falta para
reproduzir e diga o que vai fazer com isso. Se a produção está parada e o remendo é a contenção
possível agora, ele entra como contenção declarada, com log do caso, e a investigação da causa
continua.

## 2. Reproduzir

O primeiro objetivo é fazer o defeito acontecer sob controle, de preferência num **teste que
falha** antes de qualquer mudança no código de produção. O teste prova que o defeito existe,
prova depois que a correção funciona e fica na suíte como regressão.

Para reproduzir, peça só o que o código não diz:

- a **stack trace completa**, com exceções internas, e não só a primeira linha;
- a **entrada** que provoca: requisição, mensagem, registro, ou o identificador para buscá-lo;
- a **versão** em execução e desde quando acontece;
- a **frequência**: sempre, às vezes, só sob carga, só num ambiente.

Enquanto a resposta não chega, trabalhe com o que há: leia o método citado, liste de onde cada
valor pode vir nulo ou errado, e prepare o esqueleto do teste. Não devolva o problema inteiro ao
usuário com uma lista de perguntas.

Reprodução mínima, teste de caracterização para código sem teste e o caso do defeito que só
aparece em produção estão em `references/reproducao.md`.

## 3. Ler o erro inteiro

A mensagem e a stack dizem mais do que parece, e quase sempre são lidas pela metade.

- Leia **de baixo para cima até o primeiro quadro do seu código**: é ali que a decisão errada foi
  tomada, não no quadro da biblioteca onde ela explodiu.
- Leia a **exceção interna** (`InnerException`, `AggregateException.InnerExceptions`,
  `errors.Unwrap` em Go, `cause` em TypeScript). A externa costuma ser só o embrulho.
- Leia o **tipo exato**: `NullReferenceException` e `ArgumentNullException` contam histórias
  diferentes; a segunda diz qual argumento.
- Correlacione pelo **traceId** com o log e o span do mesmo pedido.

Como ler a stack em .NET (async, linha ausente em Release, NRE com nullable), panic em Go e stack
minificada em TypeScript está em `references/leitura-do-erro.md`.

## 4. Isolar

Quando a stack não basta, reduza o espaço de busca pela metade a cada passo. Uma variável por vez.

| Sintoma | Técnica |
|---|---|
| funcionava antes | `git bisect run` com o teste que reproduz |
| funciona num ambiente e não em outro | diferença de configuração, versão, dado, fuso, cultura, permissão |
| falha com um dado e não com outro | reduzir a entrada até o menor caso que ainda falha |
| intermitente, flaky | ordem dos testes, estado compartilhado, tempo, concorrência, recurso externo |
| lento ou travando | medir antes de supor: trace, profiler, dump |

O passo a passo de cada técnica, com os comandos, está em `references/isolamento.md`.

## 5. Hipótese, experimento, conclusão

Escreva a hipótese numa frase que possa ser falsa: "o `ShippingAddress` chega nulo quando o pedido
é de retirada na loja". Desenhe o experimento que a confirma ou derruba: o teste com um pedido de
retirada. Rode. Registre o resultado.

Hipótese derrubada é progresso: elimina um ramo. Mudar código "para ver se resolve" sem hipótese é
o contrário: muda duas coisas, e o resultado não ensina nada.

Depois de duas hipóteses derrubadas, volte à etapa 3 e releia o erro. A informação que falta
costuma estar lá.

## 6. Corrigir a causa e travar

A causa é o ponto onde o sistema tomou a primeira decisão errada. A correção vai ali.

- Valor nulo que não deveria existir: a correção está em quem o produziu ou no contrato que o
  permitiu. No padrão BKS, entrada inválida vira falha tipada na validação do pipeline
  (`PipelineResult`), e não `null` atravessando passos.
- Valor nulo que é legítimo (pedido de retirada não tem endereço): o domínio modela o caso, e o
  cálculo de frete tem regra explícita para ele.
- O teste da etapa 2 passa a passar. Rode a suíte inteira, não só ele.
- Procure o mesmo padrão em outros pontos do código: o defeito raramente está sozinho.

A entrega diz a causa em uma frase, a evidência que a provou e o teste que agora a impede de
voltar.

## Checklist

- [ ] Remendo pedido avaliado contra a causa, e não aplicado às cegas.
- [ ] Defeito reproduzido, de preferência num teste que falhava antes da correção.
- [ ] Stack inteira lida, com exceção interna, até o primeiro quadro do código do projeto.
- [ ] Hipótese escrita e testada; experimentos registrados.
- [ ] Correção no ponto de origem, não no ponto da explosão.
- [ ] Teste de regressão na suíte, com `Assert` nativo do xUnit; suíte inteira verde.
- [ ] Mesmo padrão procurado em outros pontos.
