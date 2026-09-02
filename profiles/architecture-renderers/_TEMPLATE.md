---
renderer: {{nome}}
tipo: {{nativo | skill-externa | template | template-documental}}
skill: {{nome da skill, se externa}}
licenca: {{se externa}}
padrao: false
fallback: mermaid
---

# {{Nome}}

{{O que este renderer produz, em duas linhas.}}

## Dependencia

{{Se for skill externa: o que precisa estar instalado, e o que fazer quando nao esta. Se for
nativo ou template: diga que nao ha dependencia.}}

## Quando e a escolha certa

{{Tres a cinco situacoes concretas. Nao "quando voce quer um diagrama bonito" — quando o formato
resolve um problema que os outros nao resolvem.}}

## O que suporta da notacao BKS

| Elemento | Suporta |
|---|---|
| cor por tipo de no | |
| linha continua e pontilhada | |
| agrupamento por fronteira | |
| logo de empresa | |
| controle fino de posicao | |

## Como aplicar a notacao

{{Como os tokens de skills/bks-arch/paleta.md entram neste renderer. Codigo, nao descricao.}}

## Limite honesto

{{O que este renderer nao faz bem. Sem isso, quem escolhe descobre tarde.}}
