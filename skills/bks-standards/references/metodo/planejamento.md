# Planejamento — o que a feature, os cenários e as tasks garantem

Guia de método do agente `planner`, que escreve três peças: FEAT (a feature), TEST (os cenários
de teste) e TASK (a unidade de trabalho).

O plano é bom quando quem implementa abre uma task e consegue terminá-la sem perguntar nada a
ninguém, e quando quem revisa consegue dizer, por teste, se ela ficou pronta.

## Antes da primeira spec

Quatro respostas precisam existir antes de haver escopo. Se alguma falta, pergunte ao usuário em
vez de supor.

1. **Quem usa.** O ator concreto: o operador do backoffice, o sistema parceiro, o job noturno.
2. **O que muda para ele.** O comportamento observável depois da entrega, não a peça construída.
3. **O que fica de fora.** O limite da FEAT, escrito. Sem ele, o escopo cresce a cada task.
4. **Como se sabe que ficou pronto.** Os critérios de aceite.

## FEAT — a feature

- **Critério de aceite verificável.** Cada critério vira um teste. "Responde rápido" não serve;
  "responde em até 300 ms no p95 com 1.000 registros" serve. "Trata erro" não serve; "devolve 409
  quando o código já existe e não grava nada" serve.
- **Fora de escopo explícito.** Uma lista curta do que alguém poderia esperar e não vem.
- **Vínculo com a decisão.** O frontmatter declara `relacionada: ADR-NNN` quando a FEAT depende de
  uma decisão registrada. O corpo segue a skill `bks-writing`: a decisão entra resumida em nota de
  fim de parágrafo, sem número no meio da frase.
- **Vínculo com o manifesto.** Se a FEAT toca área sensível declarada no manifesto do projeto, ela
  diz qual, para o `reviewer` entrar no fluxo.

## TEST — os cenários

Um cenário por critério de aceite, no mínimo, mais os casos de borda que o critério implica: vazio,
duplicado, limite da faixa, concorrência quando há recurso compartilhado. Cada cenário tem entrada,
ação e resultado esperado concretos.

## TASK — a unidade de trabalho

- **Atômica.** Uma mudança coerente, que compila e passa nos testes sozinha. Se a task tem "e" no
  título, provavelmente são duas.
- **Contexto mínimo e declarado.** A task se implementa com a spec, o código do módulo e os
  arquivos de convenção do kit e do projeto. O que mais ela precisar, ela cita.
- **Caminho dos arquivos.** Lista os arquivos que cria ou altera, com o caminho. Quem implementa
  não deveria procurar onde mexer.
- **Dependência declarada.** "Depende de T-003" quando depende. A entidade vem antes do serviço que
  a usa, o contrato antes do adapter que o implementa.
- **Rollback.** Para mudança de schema, de contrato público ou de configuração compartilhada, a
  task diz como desfazer: a migration de reversão, a flag que desliga, a versão anterior do
  contrato mantida.

## Ordem de construção

Do núcleo para a borda, cada passo testável antes do próximo:

1. tipos de domínio e suas invariantes;
2. portas (as interfaces de entrada e de saída);
3. use case com seus steps de pipeline;
4. adapters de saída (banco, fila, cliente HTTP);
5. adapter de entrada (endpoint, consumer);
6. composição e configuração.

Tasks sem dependência entre si ficam marcadas como paralelizáveis.

## DoD de toda task

A DoD (*Definition of Done*, a lista que fecha a task) tem os mesmos quatro itens em toda task,
escritos nela:

- [ ] build limpo, sem aviso novo;
- [ ] testes do cenário escritos e verdes;
- [ ] `README.md` atualizado se mudou o que o projeto faz ou como roda;
- [ ] `ARCHITECTURE.md` atualizado se a task criou ou alterou tipo público, função pública ou
  decisão estrutural.

## Quando spec e código divergem

O planner corrige a spec e registra a divergência. Não mexe em código.
