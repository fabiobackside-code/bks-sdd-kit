# Revisão de código — as armadilhas de quem revisa

Guia de método do agente `reviewer`. Passe por esta lista antes de fechar o relatório. Cada item é
um jeito de a revisão parecer feita sem ter achado o que importa, ou de bloquear a entrega pelo
motivo errado.

## Achado sem evidência

"Pode haver problema de concorrência aqui" não é achado. Achado tem `arquivo:linha`, a entrada que
provoca o defeito e o efeito que ela produz. Se não dá para escrever a entrada, a suspeita vai para
a seção de dúvidas do relatório, não para a lista de achados.

## Opinião de estilo como bloqueio

Preferir `switch` a `if`, `var` a tipo explícito ou outro nome de variável é gosto. Pode entrar como
sugestão de severidade baixa. Bloqueio fica para defeito: comportamento errado, dado exposto,
contrato quebrado, premissa do kit violada.

O mesmo vale para o que o linter ou o formatador já pegam. Repetir o aviso da ferramenta ocupa o
relatório sem acrescentar nada.

## Revisar o que não mudou

O diff tem dez linhas e o relatório aponta quinze problemas em arquivos que ninguém tocou. Defeito
antigo encontrado no caminho pode ser registrado à parte, como dívida, mas não entra na decisão de
aprovar esta entrega.

A exceção é o código que a mudança passa a exercitar de um jeito novo. Se o diff chama uma função
antiga com um argumento que ela nunca recebeu, a função entra no escopo.

## Aprovar sem ler nem rodar o teste

"Os testes passaram" no texto do autor não é evidência. Leia o teste e confira se ele falharia com
o defeito que diz cobrir. Rode a suíte quando a ferramenta permitir. Teste verde que verifica só a
chamada ao mock aprova qualquer implementação.

## Severidade inflada

Marcar tudo como alta transforma a severidade em ruído, e o crítico de verdade se perde na lista.
Crítica é acesso a dado de terceiro, vazamento entre tenants, credencial ou dado regulado exposto.
Um nome ruim é baixa, por mais que incomode.

O contrário também acontece: rebaixar um vazamento para média porque "o endpoint é interno".
Interno hoje não é garantia de interno amanhã, e o dado já está na resposta.

## Sugerir reescrita em vez de correção

"Este módulo deveria usar outro padrão" não ajuda quem precisa entregar hoje. Aponte o menor passo
que resolve o defeito. Se o desenho inteiro é o problema, isso é assunto para uma decisão de
arquitetura, registrada à parte, e não para o relatório de revisão.

## Revisar o próprio código

Quem implementou não revisa a própria entrega: sabe o que quis escrever e lê isso no lugar do que
escreveu. A revisão roda em invocação separada, e a correção volta para o `builder`.

## Relatório vazio sem escopo

"Nenhum problema encontrado" sem dizer o que foi lido equivale a não ter revisado. Liste os
arquivos e os testes verificados, e o que ficou de fora.
