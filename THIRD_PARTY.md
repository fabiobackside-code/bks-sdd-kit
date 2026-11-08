# Créditos, referências e conteúdo de terceiros

O `bks-sdd-kit` é o padrão BKS (Backside) de Spec-Driven Development, desenhado a partir da experiência do autor
em projetos reais: um motor de transações bancárias, um SDK de segurança, plataformas de produto e
provas de conceito. A maior parte do kit é original. Este arquivo diz exatamente o que não é, de
onde veio e sob que licença, e o que foi apenas inspiração.

## 1. Conteúdo de terceiros incluído no repositório

Cada item abaixo está no repositório sob a licença original, que é compatível com a MIT do kit.

| Item | Autor | Origem | Licença | Onde está | O que mudou |
|---|---|---|---|---|---|
| `writing-anti-ai` | Gaorui Zhang | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar), commit `903787345d6a` | MIT | `skills/bks-writing/third-party/writing-anti-ai/` | `SKILL.md` renomeado para `SKILL.original.md`; catálogo e exemplos em chinês ficaram de fora |
| `human-writing` | PRPM (Prompt Package Manager) | [pr-pm/prpm](https://github.com/pr-pm/prpm), commit `d6b1b17b4818` | MIT | `skills/bks-writing/third-party/human-writing/` | `SKILL.md` renomeado para `SKILL.original.md` |
| Checklist de revisão crítica | Diego Amorim | [DiegoAmorimDev/bks-multiagent-skill](https://github.com/DiegoAmorimDev/bks-multiagent-skill) | MIT | `skills/bks-standards/references/checklist-revisao-critica.md` | adaptado ao vocabulário BKS |
| `bks-daiwl` | Fabio Magalhaes | [fabiobackside-code/bks-daiwl](https://github.com/fabiobackside-code/bks-daiwl), versão `1.0.0` | MIT | `skills/bks-daiwl/` | cópia fixada; a fonte da verdade é o repositório próprio |

As duas skills de escrita partem do guia da Wikipedia sobre sinais de texto escrito por
inteligência artificial (AI, na sigla em inglês),
[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). O mapeamento
regra a regra do que foi adaptado e descartado está em
`skills/bks-writing/references/fontes-externas.md`.

### Aviso de licença — Diego Amorim

```
MIT License

Copyright (c) 2026 Diego Amorim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

As licenças das duas skills de escrita estão nas próprias pastas, em `LICENSE`.

## 2. Ferramentas usadas, não incluídas

| Ferramenta | Autor | Licença | Como o kit usa |
|---|---|---|---|
| [archify](https://github.com/tt-a1i/archify) | tt-a1i, derivado do *architecture-diagram-generator* da Cocoon AI | MIT | renderer de arquitetura opcional; fica externo, ver `profiles/architecture-renderers/archify.md` |
| [Mermaid](https://mermaid.js.org) | Knut Sveidqvist e colaboradores | MIT | renderer padrão dos diagramas |
| [agent-skills](https://github.com/tech-leads-club/agent-skills) | Tech Leads Club | ver o repositório | o guia hexagonal descreve quando acionar algumas dessas skills; nenhum texto delas foi copiado |

C4 (Simon Brown) e TOGAF (marca registrada do The Open Group) aparecem só como formato de saída.

## 3. Inspiração, sem texto copiado

As skills genéricas de apoio (`api-design`, `security-audit`, `debug-assistant`,
`frontend-design`, `refactor-guide`, `pr-writer`, `doc-writer`) e os guias de método do `planner` e
do `reviewer` cobrem temas comuns a muitos kits de skills para agentes de código. A ideia de ter uma
skill por tema veio do uso de vários desses kits. O texto deste repositório foi escrito do zero,
sem consulta a nenhum deles, e o que o diferencia é o padrão BKS aplicado a cada tema:

- **Contrato e Result Pattern.** `api-design` traduz `PipelineResult` para HTTP no adapter inbound;
  exceção de negócio não vira 500.
- **Guarda executável.** `doc-writer` obedece às guardas `comment_budget.py` e `dod_docs.py`, que
  recusam a escrita em vez de avisar.
- **Prova antes da mudança.** `debug-assistant` e `refactor-guide` exigem teste que falha, ou teste
  de caracterização, antes de qualquer correção.
- **Achado com evidência.** `security-audit` e o `reviewer` não aceitam achado sem `arquivo:linha`
  e cenário concreto.
- **Medido.** Cada uma tem um caso de eval em `evals/`, e o que conta é o delta entre o braço
  `with` e o `without`.

## 4. Referências conceituais

Os conceitos que sustentam o padrão vêm da literatura, citada onde é usada:

- Arquitetura hexagonal: Alistair Cockburn; Juan Manuel Garrido de Paz
  (`skills/bks-sdd/references/hexagonal-arch-guidelines.md`)
- Domain-Driven Design: Eric Evans, Vaughn Vernon, Alberto Brandolini
  (`skills/bks-sdd/references/ddd-*.md`)
- Spec-Driven Development e harness engineering: Martin Fowler; Waldemar Neto (Dev Lab)
  (`skills/bks-sdd/references/prd-structure.md`)
- Manutenibilidade, qualidade e padrões: a norma ISO/IEC 25010 (International Organization for
  Standardization / International Electrotechnical Commission), Robert C. Martin, Martin Fowler, Jeff Bay,
  John Ousterhout e outros, com a lista completa em
  `skills/bks-maintainability-review/references/referencias.md` e
  `skills/bks-maintainability-review/references/catalogo-conceitos.md`

## 5. Como acrescentar conteúdo de terceiros

Só entra conteúdo com licença compatível com a MIT. O original vai para uma pasta `third-party/`
dentro da skill, com `LICENSE` e commit de origem, e ganha uma linha na seção 1 deste arquivo.
