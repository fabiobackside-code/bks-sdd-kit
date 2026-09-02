---
description: Retoma o trabalho. Na raiz do vault, monta o panorama de todos os projetos a partir dos STATUS.md. Dentro de um repositorio de projeto, le o STATUS.md dele.
---

Retome o trabalho. O que fazer depende de onde a sessao esta aberta — decida primeiro.

## Passo 1 — descobrir o modo

Verifique o diretorio de trabalho atual:

- Existe `STATUS.md` na raiz? → **modo projeto**
- Existe `repos/` com subpastas de categoria? → **modo panorama**
- Nenhum dos dois → pergunte ao usuario onde ele quer trabalhar e pare

Nao adivinhe. Se `BKS_VAULT` estiver definido e o diretorio atual for outro, diga qual dos dois
voce esta usando antes de continuar.

---

## Modo projeto

Leia, nesta ordem:

1. `STATUS.md` — onde o projeto esta
2. `JOURNAL.md` — apenas a entrada mais recente, para saber o que mudou por ultimo
3. `.bks-profile.json`, se existir — perfil e renderer

Responda em ate seis linhas:

- **Onde parou** — a frase do `STATUS.md`, nao um resumo dela
- **O que trava**, se algo trava
- **Proximo passo** — a acao concreta que o `STATUS.md` nomeia

Se o `STATUS.md` estiver desatualizado em relacao ao `JOURNAL.md` ou ao git log, diga isso em uma
linha e ofereca atualiza-lo. Nao atualize sozinho.

Se nao houver `STATUS.md`, ofereca cria-lo a partir do template do kit.

---

## Modo panorama

Percorra `repos/*/*/` e, para cada projeto, leia:

- `STATUS.md` — a frase de estado, a fase, e o que trava
- `JOURNAL.md` — a data da entrada mais recente

**Pule `repos/old/`.** E arquivo morto: projeto encerrado ou substituido, guardado porque apagar
seria irreversivel, nao porque ainda valha. Nao entra no panorama, nao entra na contagem, nao
aparece como sugestao.

Nao leia mais nada. Nao abra `specs/`, `decisions/` nem codigo — o panorama e calculado desses
dois arquivos, e ler alem disso custa tokens sem mudar a resposta.

Monte a visao, agrupada por estado e ordenada pela data mais recente primeiro:

```
{{vault}} · {{n}} projetos · {{n}} ativos

ATIVO
  {{projeto}}   {{categoria}}   {{frase de estado, truncada}}   {{data}}

PAUSADO
  {{projeto}}   {{categoria}}   {{frase de estado, truncada}}   {{data}}
```

Classifique como **ativo** o projeto cuja entrada mais recente do `JOURNAL.md` tem menos de 30
dias; **pausado** acima disso. Projeto sem `STATUS.md` entra numa terceira secao, `SEM STATUS`,
com a data do ultimo commit.

Feche com uma linha de sugestao: qual projeto tem trabalho pronto para seguir, e qual esta travado
esperando algo. Baseie-se no que trava — projeto bloqueado por decisao externa nao e candidato.

Termine dizendo que, para trabalhar num projeto, o usuario abre uma sessao nova na pasta dele.
Nao ofereca continuar o trabalho do projeto a partir da raiz: os comandos de projeto precisam da
sessao aberta no repositorio.

---

## Em ambos os modos

Responda em portugues do Brasil. Nao narre o que voce leu, nao liste os arquivos abertos, nao
recapitule a estrutura do vault. A resposta e o estado, nao o relatorio de como voce o obteve.
