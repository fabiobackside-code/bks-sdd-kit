# Planejamento — as armadilhas do plano

Guia de método do agente `planner`, que escreve FEAT (a feature), TEST (os cenários de teste) e
TASK (a unidade de trabalho). Passe por esta lista antes de entregar o plano. Cada item é um
plano que parece completo e trava na hora de implementar ou de revisar.

## Tema em vez de ação

"T-004: Autenticação" é um tema. Quem abre a task não sabe se vai escrever o middleware, configurar
o provedor ou testar o token expirado. A task começa por um verbo e nomeia o resultado: "Validar o
token no adapter de entrada e devolver 401 quando expirado".

## Contexto que ninguém declarou

A task diz "seguir o padrão combinado" ou "usar a mesma abordagem do outro serviço", e o combinado
está na cabeça de quem planejou. Toda referência vira caminho de arquivo, decisão registrada ou
trecho da spec. Se a task só se entende com a conversa de planejamento aberta, ela não está pronta.

## Critério que não se testa

"Deve ser seguro", "interface amigável", "boa performance". Ninguém escreve o teste, então ninguém
consegue dizer se passou. Troque o adjetivo pela observação: o status devolvido, o tempo medido com
a carga definida, o campo que não aparece na resposta.

## Escopo que vaza

A task de "adicionar o filtro por data" também renomeia a tabela, atualiza a biblioteca de log e
reorganiza as pastas. Cada uma dessas pode ser boa ideia, e nenhuma está na FEAT. O que não está no
escopo vira item de backlog ou FEAT nova, nunca carona numa task.

## Ordem que não fecha

O serviço aparece antes da entidade que ele usa, ou o adapter antes da porta que implementa. A
task não compila sozinha e duas tasks precisam ser feitas juntas, o que desfaz a atomicidade.
Ordene do núcleo para a borda e declare a dependência.

## Sem caminho de volta

Migration que apaga coluna, contrato público que muda de forma, configuração compartilhada
alterada, e nenhuma linha sobre como desfazer. Quando o deploy falha, o rollback é improvisado sob
pressão. Mudança que não se desfaz com um revert simples declara o caminho de volta na própria task.

## DoD genérica

"Concluir a implementação" não é DoD. Sem build, teste, `README.md` e `ARCHITECTURE.md` escritos na
task, a documentação fica para depois, e depois não chega.

## Repropor o que já foi rejeitado

O plano traz de volta uma alternativa que o log de decisões do projeto já descartou, sem dizer o
que mudou desde então. Leia `decisions/` antes de propor.
