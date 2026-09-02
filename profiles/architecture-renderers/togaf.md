---
renderer: togaf
tipo: template-documental
base: mermaid
padrao: false
fallback: mermaid
---

# TOGAF

Template de arquitetura corporativa. Documento estruturado nas quatro camadas do TOGAF, com
diagramas de apoio.

## Quando e a escolha certa

- a entrega e documento de arquitetura corporativa, nao diagrama de sistema
- ha exigencia formal de metodo — cliente, orgao regulador, area de arquitetura
- o escopo atravessa varios sistemas e envolve processo de negocio

Para um sistema so, `c4` entrega mais com menos cerimonia.

## Camadas

| Camada | Cobre |
|---|---|
| Negocio | processos, atores, capacidades, servicos de negocio |
| Dados | entidades, fluxos, propriedade, ciclo de vida |
| Aplicacao | sistemas, integracoes, contratos |
| Tecnologia | plataforma, rede, ambientes |

Cada camada gera uma secao e ao menos um diagrama.

## Como aplicar a notacao

Os diagramas de apoio saem em Mermaid, com a paleta BKS. A camada de Tecnologia se beneficia de
`archify` quando ha logo de infraestrutura.

## Limite honesto

TOGAF e pesado. Aplicado a um projeto pequeno, produz documento que ninguem le. Confirme que ha
exigencia real de metodo antes de escolher — nao escolha por parecer mais completo.
