---
name: doc-writer
description: >
  Escreve e atualiza documentação de código: resumo de contrato em membro público (XML doc
  comment em C#, JSDoc em TypeScript, godoc em Go, docstring em Python), README.md e
  ARCHITECTURE.md, e comentário só para o que não é óbvio. Lê o código antes de escrever e
  documenta o contrato e o porquê, nunca a paráfrase do como. Use SEMPRE que o usuário pedir para
  documentar um método, classe, módulo ou repositório; escrever docstring, summary, JSDoc ou
  godoc; comentar o código; explicar uma decisão "no comentário"; criar ou atualizar README ou
  ARCHITECTURE; ou fazer retrofit de documentação num repositório pronto. Trigger: documenta
  isto, comenta este método, escreve o summary, XML doc, JSDoc, godoc, docstring, README,
  ARCHITECTURE.md, dicionário técnico, documentação de API pública, comentário de código.
---

# doc-writer — contrato no código, decisão no ARCHITECTURE

A documentação de código responde a duas perguntas de quem chega: o que este membro promete a quem
o chama, e por que o sistema foi montado assim. A primeira resposta mora no código, em uma linha. A
segunda mora no `ARCHITECTURE.md`, onde cabe o argumento inteiro e onde alguém vai procurá-lo.

## As regras que a guarda confere

Duas guardas rodam a cada escrita de arquivo `.cs` e recusam a escrita que as viola.

**Teto de comentário** (`hooks/scripts/comment_budget.py`):

- nenhum bloco de comentário passa de cinco linhas — `//`, `///` ou `/* */` contíguos contam juntos;
- no código ficam só duas coisas: o **contrato**, uma linha em membro público, e a **guarda contra
  regressão**, até duas linhas dizendo o que quebra se alguém mudar aquele trecho;
- decisão, trade-off e histórico vão para o `ARCHITECTURE.md`, e o comentário não aponta para lá —
  nada de "ver ARCHITECTURE.md", nem número de ADR, nem código de task;
- nenhuma marca de severidade: círculo colorido, triângulo de alerta, check, alfinete.

**Dívida de documentação** (`hooks/scripts/dod_docs.py`): arquivo `.cs` que declara tipo público é
recusado enquanto `README.md` e `ARCHITECTURE.md` não estiverem entre as mudanças pendentes do
working tree. Tipo público novo é decisão de contrato, e o contrato se documenta na mesma leva.

Essas regras valem igual em TypeScript, Go e Python, mesmo onde não há guarda executável. A política
completa está na skill `bks-standards`, na referência de documentação.

## Como trabalhar

1. **Leia o código antes de escrever.** O contrato sai do comportamento real: o que o método
   devolve, o que lança, o que aceita como nulo, o que altera fora dele. Um indexador de dicionário
   lança exceção quando a chave falta — isso é contrato e vai na linha de resumo.
2. **Separe o pedido em três destinos.** Contrato vai para o membro. Guarda contra regressão vai
   para a linha que ela protege. Decisão, trade-off e histórico vão para o `ARCHITECTURE.md`.
3. **Escreva a linha de contrato para quem chama.** Verbo no presente, o que faz e o que devolve.
   Membro trivial (propriedade auto, construtor que só atribui) não ganha comentário.
4. **Atualize `README.md` e `ARCHITECTURE.md`** quando a mudança cria ou altera tipo público,
   função pública ou decisão estrutural. É item de DoD (*Definition of Done*, a lista que fecha a
   task), junto com build e testes.
5. **Marque o que não dá para confirmar.** Decisão que o código não revela entra como
   `> [!uncertain]` no `ARCHITECTURE.md`, com a pergunta para o autor. Não invente a justificativa.

A forma da linha de contrato em cada linguagem está em `references/contrato-por-linguagem.md`. O
que vai no README e o que vai no ARCHITECTURE, com o esqueleto de cada um, está em
`references/readme-e-architecture.md`.

## Quando o pedido contraria a regra

É comum o usuário pedir o bloco longo com a história da decisão, ou um alerta em vermelho no topo
para ninguém mexer. A resposta tem três partes, sempre:

1. entrega o código com o contrato em uma linha e, se houver risco real, a guarda contra regressão
   em até duas linhas, sem marca;
2. diz por que não escreveu o bloco: o teto de cinco linhas e a marca de severidade são recusados
   pela guarda, e decisão no comentário envelhece sem ninguém ver;
3. entrega o conteúdo pedido no lugar certo — a entrada do `ARCHITECTURE.md` com contexto,
   decisão, trade-off e histórico, preenchida com o que se sabe e marcada onde falta informação.

Obedecer em silêncio não basta: quem pediu precisa saber onde a informação foi parar. Exemplos de
resposta em `references/pedido-fora-da-regra.md`.

## O tom

Prosa de README, ARCHITECTURE, spec e treinamento, e o tom da linha de contrato, seguem a skill
`bks-writing`: o parágrafo se lê sozinho, a decisão entra resumida no texto e o número do ADR fica
fora do meio da frase.

## Checklist antes de entregar

- [ ] Li o código e a linha de contrato descreve o comportamento real, inclusive exceção e nulo.
- [ ] Nenhum bloco de comentário passa de cinco linhas.
- [ ] Nenhum comentário aponta para documento, ADR ou task.
- [ ] Nenhuma marca de severidade.
- [ ] Decisão, trade-off e histórico estão no `ARCHITECTURE.md`, não no código.
- [ ] Tipo público novo ou alterado veio com `README.md` e `ARCHITECTURE.md` atualizados.
- [ ] O que não pude confirmar está marcado como `[!uncertain]`, não inventado.
