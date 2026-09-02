# STATUS — {{PROJETO}}

> Ponto de entrada do projeto. Leia so este arquivo para saber onde as coisas estao e o que fazer
> a seguir. Atualizado pelo `/save` ao fim de cada sessao; lido pelo `/brain`.
>
> Ultima atualizacao: {{DATA}}

---

## Em uma frase

{{Uma frase que diz onde o projeto esta. Nao o que ele e — onde ele esta.}}

---

## Fase atual

**{{Fase}}** — {{o que caracteriza esta fase e o que a encerra}}

---

## O que trava

{{O que impede o proximo passo. Se nada trava, escreva "Nada trava." e siga.}}

| Bloqueio | Espera | Quem destrava |
|---|---|---|
| {{o que esta parado}} | {{decisao, pessoa, evento}} | {{quem}} |

Bloqueio resolvido sai daqui e vira entrada no `JOURNAL.md`. Este quadro mostra o que trava
**agora**, nao o que ja travou.

---

## Proximo passo

{{Uma acao concreta, executavel agora. Nao um tema, nao uma area — uma acao.}}

{{Se ha varios caminhos possiveis, diga por onde comecar e por que. Ordem de construcao vale mais
que lista de tarefas.}}

---

## Decisoes que valem

{{O que ja foi decidido e nao se reabre sem motivo novo. Existe para que a proxima sessao nao
gaste tempo rediscutindo o que ja esta fechado.}}

| # | Decisao | Onde |
|---|---|---|
| 1 | {{a decisao, em uma linha}} | {{ADR-NNN ou documento}} |

Toda linha aponta para onde a decisao esta registrada com contexto. Decisao sem referencia e
memoria — e memoria nao sobrevive a duas semanas.

---

## Aberto

{{O que ficou pendente e nao trava o proximo passo. Lista curta; o que envelhece sem virar
trabalho sai daqui.}}

---

## Mapa dos documentos

{{Onde cada coisa esta, para que a proxima sessao encontre sem procurar.}}

| Documento | Para que |
|---|---|
| este arquivo | onde parei, o que trava, proximo passo |
| `WORKFLOW.md` | o fluxo de comandos deste projeto |
| `JOURNAL.md` | marcos e sessoes, do mais recente ao mais antigo |
| `decisions/` | as decisoes, com contexto e alternativas descartadas |
| `specs/` | features, cenarios de teste, tasks |
| `docs/canonical/` | contexto consolidado — a fonte apos o `/canonize` |
| `docs/input/` | material bruto ainda nao consolidado |
| `brain/domain/` | o que o produto e — regra de negocio, metodo, normativo |
| `brain/engineering/` | como se constroi aqui — padrao tecnico deste projeto |

{{Acrescente os documentos proprios do projeto que a proxima sessao precisa achar.}}
