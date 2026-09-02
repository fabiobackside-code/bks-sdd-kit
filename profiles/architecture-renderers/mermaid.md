---
renderer: mermaid
tipo: nativo
padrao: true
fallback: null
---

# Mermaid

Diagrama em texto, dentro do markdown. Renderiza sem dependencia — no GitHub, no Obsidian, em
artefatos.

## Quando e a escolha certa

- o diagrama precisa viver no repositorio e ser revisado em diff
- a saida e markdown
- ninguem vai instalar nada para ver

## O que suporta da notacao BKS

| Elemento | Suporta |
|---|---|
| cor por tipo de no | sim, via `classDef` |
| linha continua e pontilhada | sim |
| agrupamento por fronteira | sim, via `subgraph` |
| logo de empresa | **nao** — usa rotulo textual |
| controle fino de posicao | limitado |

## Como aplicar a notacao

Declare as classes uma vez, no topo do diagrama, com a paleta de `skills/bks-arch/paleta.md`:

```
classDef backend    fill:#336698,stroke:#1F4266,color:#FFFFFF
classDef storage    fill:#4A7C63,stroke:#2E5140,color:#FFFFFF
classDef broker     fill:#B5713C,stroke:#8A5228,color:#FFFFFF
classDef acesso     fill:#9E4B4B,stroke:#733535,color:#FFFFFF
classDef componente fill:#B39038,stroke:#8A6E26,color:#FFFFFF
classDef externo    fill:#6B7280,stroke:#4B5563,color:#FFFFFF
```

Aplique com `class NO1,NO2 backend`.

Linha continua (`-->`) para conexao direta. Linha pontilhada (`-.->`) para fluxo assincrono.

## Limite honesto

Sem logo de empresa e com layout automatico. Para diagrama de infraestrutura com marca visual e
posicionamento controlado, use `archify`.
