# O relatório — achado, severidade e escopo

O relatório serve a quem vai corrigir e a quem vai decidir se a entrega sai. Os dois precisam da
mesma coisa: onde está, como se explora, como se fecha e quanto custa não fechar.

## Severidade pelo impacto

A severidade sai de três perguntas, respondidas no próprio achado:

1. **Quem explora?** Anônimo na internet, qualquer usuário autenticado, usuário com papel
   específico, alguém com acesso à rede interna ou ao servidor.
2. **O que precisa ter?** Nada além de uma requisição, um identificador que vaza, uma condição de
   corrida, interação de outra pessoa.
3. **O que obtém?** Dado de terceiro, dado regulado, credencial, escrita ou movimentação de valor,
   indisponibilidade, execução de código.

| Severidade | Impacto típico |
|---|---|
| crítica | dado de terceiro ou de outro tenant, credencial, dado regulado ou movimentação de valor, ao alcance de qualquer usuário autenticado ou anônimo; execução remota de código |
| alta | o mesmo impacto exigindo condição difícil, como papel específico ou janela de corrida; ou escalada de privilégio dentro do próprio tenant |
| média | vazamento de informação que facilita outro ataque, como enumeração, versão ou estrutura interna; negação de serviço com custo baixo para o atacante |
| baixa | falha de defesa em profundidade, sem exploração direta conhecida |

A justificativa é uma frase com as três respostas: "crítica — qualquer cliente autenticado lê
endereço e CPF de qualquer outro cliente, bastando o identificador do pedido". Adjetivo sem
impacto ("muito grave", "perigoso") não justifica nada e não convence quem prioriza.

Crítica bloqueia a entrega. Quem decide aceitar o risco de uma alta registra a decisão em ADR, com
o prazo de correção.

## O achado

```
{arquivo}:{linha}
Problema: {uma frase, o que o código faz de errado}
Exploração: {requisição, entrada ou sequência concreta} → {efeito observável}
Correção: {a menor mudança que fecha a falha}
Severidade: {nível} — {quem, com o quê, obtém o quê}
Referência: {CWE-nnn; OWASP quando ajudar}
```

Quando a correção cabe em poucas linhas, mostre o código. Quando muda contrato, por exemplo um
`403` que vira `404`, diga quem é afetado.

Achado sem exploração descrita é **hipótese**. Registre em seção própria, com o que falta para
confirmar: "não vi o middleware que preenche o tenant; se ele aceitar o cabeçalho `X-Tenant-Id` do
cliente, a consulta da linha 88 vaza dado entre tenants".

## Estrutura do relatório

1. **Escopo verificado**: arquivos e commits lidos, superfícies percorridas, o que ficou de fora.
2. **Premissas não verificadas**: proteções citadas e não vistas, como gateway, WAF ou filtro
   global, cada uma com o que acontece se ela não existir.
3. **Achados**, da maior severidade para a menor.
4. **Hipóteses**, com o que confirma cada uma.
5. **Higiene**: pontos sem exploração conhecida que melhoram a postura. Sem severidade, em uma
   linha cada.

Revisão sem achado entrega as seções 1 e 2 completas. É isso que diz quanto a ausência de achado
vale.

## Afirmações de terceiros

"Passou no pentest", "o time revisou" e "o scanner não apontou nada" entram no relatório só como
contexto, nunca como evidência. Quando a afirmação contradiz o achado, o achado prevalece, porque
traz a exploração.

Os motivos são práticos. Pentest de caixa-preta raramente tem dois usuários do mesmo perfil para
testar IDOR. Scanner estático não sabe quem é o dono de um pedido. O código revisado pode ser
posterior ao teste. Diga isso em uma frase quando o usuário trouxer a afirmação, e siga para o
código.

## Correção e teste

Cada achado corrigido ganha teste que reproduz a exploração: falha antes da correção, passa depois.
O teste fica na suíte para impedir que a falha volte. Para autorização, o par "A não acessa o de B"
e "A acessa o próprio" é o mínimo.

A correção é feita por quem implementa, em invocação separada de quem revisou. Quem revisa aponta
o menor caminho; não reescreve o módulo.
