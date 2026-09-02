# Topologias — qual diagrama para qual pergunta

## Arquitetura

**Responde:** do que o sistema e feito, e como as pecas se falam.

Nos sao pecas executaveis ou armazenamento: servico, banco, fila, gateway, biblioteca. Arestas sao
dependencias — quem chama quem.

**Nao mostra** ordem temporal. Se a pergunta e "o que acontece primeiro", o diagrama e outro.

Agrupe por fronteira real: processo, container, rede, dominio. Agrupamento por semelhanca visual
engana.

## Sequencia

**Responde:** em que ordem as coisas acontecem, entre quais atores.

Participantes na horizontal, tempo descendo. Mensagem sincrona com linha continua e retorno
explicito; assincrona com pontilhada e sem espera.

**Marque o que pode falhar.** Uma sequencia que so mostra o caminho feliz esconde justamente o que
precisa ser projetado.

Limite: cerca de sete participantes. Acima disso, fatie por cenario.

## Fluxo de dados

**Responde:** por onde o dado passa, o que o transforma, onde repousa.

Nos sao transformacoes e repositorios. Arestas sao o dado em movimento — rotule com **o que**
trafega, nao com o verbo.

**Marque a fronteira de dado sensivel.** Onde dado pessoal ou regulado atravessa um limite, o
diagrama mostra. E o que torna o diagrama util numa revisao de conformidade.

## Ciclo de vida

**Responde:** que estados uma entidade atravessa, e o que dispara cada transicao.

Nos sao estados; arestas sao eventos. Todo estado precisa de saida, menos o final. Estado sem
saida que nao e final e bug de modelagem — mostre.

**Inclua o caminho de erro.** Estado de falha, retentativa, expiracao. Sao os que causam incidente.

## Workflow

**Responde:** quem faz o que, e onde se decide.

Raias por ator ou sistema. Losango para decisao, com as saidas rotuladas.

**Marque onde espera.** Aprovacao humana, lote noturno, timeout — o tempo de espera e o que
explica por que o processo demora.

---

## Erros que aparecem sempre

**Um diagrama para duas perguntas.** Arquitetura com numeracao de ordem tenta ser sequencia
tambem, e falha nas duas.

**Tudo no mesmo diagrama.** Completo nao e util. O que nao ajuda a responder a pergunta sai.

**Fronteira ausente.** Sem mostrar onde termina o que voce controla, ninguem sabe onde estao os
riscos.

**Aresta sem rotulo.** Uma seta sem rotulo diz que existe relacao, nao qual. Rotule com protocolo,
dado ou evento.
