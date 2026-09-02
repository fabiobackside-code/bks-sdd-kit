---
name: bks-standards
description: >
  Padroes de engenharia BKS: premissas de codificacao, regras de dependencia .NET,
  Object Calisthenics, politica de documentacao e comentario, SEDA e TCP sockets,
  e o checklist de revisao critica. Use quando precisar decidir COMO construir —
  camadas, dependencias, imutabilidade, tratamento de erro, comentario, ou quando
  revisar codigo contra os padroes da casa. Trigger: padrao BKS, premissa de
  codificacao, regra de dependencia, calisthenics, comentario no codigo, SEDA,
  socket TCP, checklist de revisao.
---

# BKS-STANDARDS — padroes de engenharia

Estes padroes governam **como** o codigo e gerado, em qualquer projeto. Sao metodo, nao decisao de
um produto — por isso vivem no kit e nao no vault.

Um projeto pode sobrescrever qualquer um deles em `brain/engineering/`. Onde houver conflito, o
projeto vence.

## Referencias

Abra a que a tarefa exige, nao todas.

| Referencia | Quando abrir |
|---|---|
| `references/bks-premises.md` | antes de gerar codigo novo — e a fonte de verdade do metodo |
| `references/dotnet-standards.md` | projeto .NET: camadas, dependencias, composition root |
| `references/calisthenics.md` | ao decidir forma de classe e metodo |
| `references/documentacao.md` | ao escrever comentario, README ou ARCHITECTURE |
| `references/seda-tcp.md` | pipeline por estagios, socket, backpressure |
| `references/checklist-revisao-critica.md` | ao revisar codigo de area sensivel |

## As tres que nao se negociam

**Dominio agnostico.** `Domain/Core/Common` usa apenas `System.*`. Sem ORM, sem driver, sem
cliente de mensageria. Precisa de infraestrutura no dominio? A dependencia entra invertida, por uma
porta.

**Orquestracao explicita.** Sem MediatR, sem dispatcher. O use case e chamado direto pela porta, e
os passos ficam ordenados no pipeline. Ha um guarda que recusa a escrita — ver `hooks/`.

**Erro de negocio nao e excecao.** Use case devolve resultado tipado. Excecao fica para o que e
excepcional de verdade.
