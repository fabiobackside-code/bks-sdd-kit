# Notacao BKS — o que vira no, e o que fica de fora

A paleta diz que cor usar. Este documento diz **o que desenhar**.

## O que vira no

Vira no o que tem existencia propria e pode falhar sozinho:

- processo que roda: servico, worker, funcao
- coisa que guarda estado: banco, cache, filesystem, blob
- coisa que transporta: fila, topico, barramento
- fronteira de entrada: gateway, ingress, canal
- artefato consumido por outro: biblioteca, SDK

**Nao vira no:** classe, metodo, tabela, arquivo de configuracao, framework. Sao detalhes de
implementacao — vivem no codigo, nao no diagrama de arquitetura.

Regra pratica: se voce nao consegue reiniciar sozinho, provavelmente nao e um no.

## Fronteiras

Toda arquitetura tem ao menos uma fronteira: onde termina o que voce controla.

| Fronteira | Mostra |
|---|---|
| confianca | onde a entrada deixa de ser confiavel |
| processo | o que roda junto e cai junto |
| rede | o que atravessa a rede — e paga a latencia |
| dominio | onde a linguagem do negocio muda |

Um diagrama sem fronteira nao permite avaliar risco: tudo parece igualmente seguro.

## Rotulos

**No:** o nome real, como aparece no repositorio ou na infraestrutura. Nao "Servico de Pedidos"
quando o servico se chama `orders-api`. Quem le o diagrama vai procurar o nome que voce escreveu.

**Aresta:** o que trafega ou o protocolo. `POST /orders`, `pedido.criado`, `SELECT`. Nao "envia
dados" — toda aresta envia dados.

**Agrupamento:** o nome da fronteira. `Cluster producao`, `Rede interna`, `Contexto de cobranca`.

## Direcao

A seta aponta para quem **recebe a chamada**, nao para onde o dado vai.

Um servico que le do banco aponta para o banco, ainda que o dado venha na direcao contraria. O que
o diagrama mostra e a dependencia: quem precisa de quem para funcionar.

Em fluxo de dados a convencao se inverte — ali a seta segue o dado. Por isso os dois nao se
misturam no mesmo desenho.

## Densidade

| Nos | O que fazer |
|---|---|
| ate 12 | um diagrama |
| 13 a 25 | agrupe por fronteira, considere dois niveis |
| acima de 25 | fatie por contexto, ou use C4 |

Diagrama que precisa de zoom para ser lido ja falhou como diagrama.

## O que fica de fora

- o que nao ajuda a responder a pergunta do diagrama
- infraestrutura de suporte que existe em todo lugar — log, metrica, DNS — a menos que a pergunta
  seja sobre observabilidade
- variantes de ambiente, quando a topologia e a mesma: desenhe uma e diga que vale para todas
- o que ainda nao existe, misturado ao que existe. Se precisa mostrar o futuro, faca dois
  diagramas — atual e alvo
