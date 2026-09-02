---
name: bks-arch
description: >
  Notacao BKS para diagramas de arquitetura: paleta derivada da marca, semantica de cor por
  tipo de no (backend, storage, broker, canal de acesso, componente), convencao de linha
  para fluxo sincrono e assincrono, e escolha do tipo de diagrama. Emite para Mermaid,
  archify, C4 ou TOGAF — a notacao e a mesma, o motor e plugavel. Use ao desenhar
  arquitetura, topologia, fluxo de dados, sequencia, ciclo de vida ou diagrama de
  infraestrutura. Trigger: diagrama de arquitetura, topologia, C4, TOGAF, mermaid, archify,
  desenhar o sistema, notacao de diagrama, paleta de diagrama.
---

# BKS-ARCH — notacao de arquitetura

Esta skill e a **notacao**, nao o motor. Ela decide o que cada cor e cada linha significam; o
renderer decide como desenhar.

Por isso um diagrama BKS parece um diagrama BKS em qualquer motor — e trocar de motor nao muda o
que o leitor entende.

## Primeiro: qual diagrama

| Se a pergunta e | O diagrama e |
|---|---|
| do que o sistema e feito e como as pecas se falam | **arquitetura** |
| em que ordem as coisas acontecem entre atores | **sequencia** |
| por onde o dado passa e onde repousa | **fluxo de dados** |
| que estados uma entidade atravessa | **ciclo de vida** |
| quem faz o que, e onde decide | **workflow** |

Escolher errado custa mais que desenhar mal. Um diagrama de arquitetura respondendo pergunta de
sequencia vira caixa com seta demais.

Detalhes em `references/topologias.md`.

## Depois: qual motor

Le `.bks-profile.json` do projeto, campo `axes.architecture_renderer`. Sem o arquivo, pergunte.

| Motor | Quando |
|---|---|
| `mermaid` | padrao — vive no repositorio, revisa em diff, sem dependencia |
| `archify` | infraestrutura com logo, entrega para apresentacao, sistema grande de navegar |
| `c4` | publicos diferentes precisam de niveis de zoom diferentes |
| `togaf` | exigencia formal de arquitetura corporativa |

O registro esta em `profiles/architecture-renderers/`. Cada motor tem seu arquivo com o que
suporta e o que nao suporta.

Se o motor escolhido for skill externa e ela nao estiver instalada, **avise e caia no mermaid**.
Nao falhe.

## A notacao

Cor por papel, nunca por estetica:

| Papel | Cor | Para |
|---|---|---|
| backend | azul `#336698` | servico, API, worker, use case |
| storage | verde `#4A7C63` | banco, blob, filesystem, cache |
| broker | laranja `#B5713C` | Kafka, RabbitMQ, fila, topico |
| acesso | vermelho `#9E4B4B` | gateway, ingress, canal externo, usuario |
| componente | amarelo `#B39038` | biblioteca, SDK, DLL |
| externo | cinza `#6B7280` | terceiro, fora da fronteira |

Linha continua = sincrono, quem chama espera. Linha pontilhada = assincrono.

Tokens completos, contraste e tema escuro em `references/paleta.md`.

## Referencias

| Arquivo | Quando abrir |
|---|---|
| `references/paleta.md` | ao atribuir cor — tokens, contraste, tema |
| `references/topologias.md` | ao escolher o tipo de diagrama |
| `references/notacao-bks.md` | ao decidir o que vira no, e o que fica de fora |
| `references/emit-mermaid.md` | ao gerar em Mermaid |
| `references/emit-archify.md` | ao gerar em archify |

## Regras

**Um diagrama responde uma pergunta.** Se precisa de duas, sao dois diagramas.

**Cor nunca e a unica informacao.** Todo no tem rotulo. O diagrama sobrevive a impressao em preto
e branco.

**Sem cor viva.** A paleta e dessaturada de proposito. Trinta nos em cor saturada cansam antes de
serem lidos.

**O que nao ajuda a responder a pergunta sai.** Diagrama completo nao e diagrama util.
