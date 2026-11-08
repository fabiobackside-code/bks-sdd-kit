# README e ARCHITECTURE: o que vai em cada um

Os dois ficam na raiz do projeto e respondem a leitores diferentes. O `README.md` atende quem quer
usar ou rodar o projeto hoje. O `ARCHITECTURE.md` atende quem vai mudar o projeto e precisa saber
por que ele é assim.

## README.md

Curto e funcional. Quem termina de ler sabe o que o projeto faz e consegue rodá-lo.

```markdown
# {nome}

{uma ou duas frases: o que faz e para quem}

## Como rodar
{pré-requisitos e os comandos, copiáveis}

## Estrutura
{um nível de pastas, uma linha por pasta}

## Stack
{linguagem, runtime, banco, mensageria}

## Documentação
`ARCHITECTURE.md` · `specs/` · `decisions/`
```

Fica fora do README: decisão de arquitetura, dicionário de classes, histórico de mudança.

## ARCHITECTURE.md

O dicionário técnico vivo. A abertura diz em uma frase para que o arquivo serve, e é por isso que o
comentário de código não precisa apontar para ele.

```markdown
# Arquitetura — {nome}

Por que o projeto é como é, e o que cada peça pública faz.

## Camadas
{o fluxo do adapter de entrada até o resultado, e o que cada camada pode referenciar}

## Decisões
### {título que afirma a decisão}
{contexto, decisão e consequência, em prosa curta}

## Dicionário
### {Tipo ou módulo}
{o que é, quem usa, invariantes, o que não faz}
```

Quando o projeto já tem `decisions/` com ADRs, a seção de decisões resume cada uma e linka o
registro, sem copiar o texto inteiro.

## Quando atualizar

Na mesma task que cria ou altera tipo público, função pública ou decisão estrutural, antes de fechar.
Em C#, a guarda `dod_docs.py` recusa a escrita do tipo público até os dois arquivos estarem entre as
mudanças pendentes. Refactor que não muda contrato nem decisão ganha uma linha no `ARCHITECTURE.md`
dizendo isso, ou o tipo vira `internal`.

## Entrada de decisão a partir de um pedido de comentário

Quando a informação chegou como pedido de comentário longo, ela vira uma entrada na seção de
decisões. O que o usuário não disse fica marcado, nunca preenchido por suposição:

```markdown
### O limite de requisições é contado em memória, por instância

O contador de cada cliente vive na memória do processo e zera quando a instância reinicia. Com três
instâncias, o limite efetivo é até três vezes o configurado.

A alternativa era um contador compartilhado no Redis, que dá limite exato ao custo de uma ida à
rede por requisição.

> [!uncertain]
> Quando a troca foi feita e qual incidente a motivou: confirmar com o autor.
```

## Retrofit em repositório pronto

Faça por módulo, nunca o repositório inteiro numa passada. Leia os comentários antes de apagá-los:
cada decisão que estava num bloco longo vira entrada no `ARCHITECTURE.md`, e o bloco vira a linha
de contrato. Mostre o diff ao usuário antes de aplicar.
