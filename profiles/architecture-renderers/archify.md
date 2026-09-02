---
renderer: archify
tipo: skill-externa
skill: archify
licenca: MIT
padrao: false
fallback: mermaid
---

# Archify

Skill externa que gera HTML interativo — pan, zoom, foco, navegacao por camadas, export para PNG,
SVG e WebM.

## Dependencia

Nao vem no kit. E skill de terceiro, com motor de renderizacao proprio, e evolui por conta
propria. Copia-la aqui criaria um fork que precisaria de manutencao.

**Se nao estiver instalada**, avise e caia no `mermaid`. Nao falhe.

## Quando e a escolha certa

- diagrama de infraestrutura com logo e posicionamento controlado
- entrega para apresentacao ou consulta, nao para diff
- sistema grande, onde navegar por camadas ajuda mais que ver tudo de uma vez
- reconstrucao de arquitetura de legado, onde explorar importa

## O que suporta da notacao BKS

| Elemento | Suporta |
|---|---|
| cor por tipo de no | sim |
| linha continua e pontilhada | sim |
| agrupamento por fronteira | sim |
| logo de empresa | sim |
| controle fino de posicao | sim |
| tema claro e escuro | sim |

## Como aplicar a notacao

O `archify` aceita cor por no. Use os tokens de `skills/bks-arch/paleta.md` no lugar do padrao
dele — sem isso, o diagrama sai no estilo da skill, nao no seu.

Icones de infraestrutura: use os SVG genericos de `skills/bks-arch/icons/`. O kit nao distribui
marca de terceiro.

## Limite honesto

Saida em HTML, nao em texto. Um diagrama `archify` nao se revisa em diff — versione o arquivo de
entrada, nao so o HTML gerado.
