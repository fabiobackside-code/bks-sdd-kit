---
name: frontend-design
description: >
  Constrói interface com identidade intencional em vez do default genérico do framework: lê o
  design system e os tokens que o projeto já tem antes de codar, decide uma direção visual
  explícita quando não há (tipografia, escala, cor, espaçamento) e a registra como tokens, monta
  hierarquia visual deliberada, trata os estados vazio, carregando, erro e filtro sem resultado,
  cumpre WCAG 2.2 (contraste, foco visível, semântica, teclado), responde a qualquer largura e
  mantém cada componente com uma responsabilidade. Use SEMPRE que o pedido for criar ou redesenhar
  tela, página, componente, formulário, listagem, dashboard ou layout. Trigger: nova tela, página,
  componente, redesenho, redesign, UI, interface, layout, design system, design tokens, CSS,
  React, Tailwind, acessibilidade, a11y, responsivo, "algo simples e padrão".
---

# frontend-design — interface com critério, mesmo quando é simples

Toda interface tem uma direção visual. Ou alguém a escolheu, ou ela veio do default do framework.
Esta skill garante a primeira opção: a tela segue o que o projeto já decidiu. Onde nada foi
decidido, a decisão é tomada às claras e fica registrada como **token**. Token é uma variável
nomeada para cor, tamanho, espaço ou raio, que o resto do código consome.

"Simples e padrão" pede sobriedade, não ausência de critério. Uma listagem sóbria ainda tem uma
coisa mais importante que as outras, ainda carrega, ainda falha e ainda fica vazia.

## 1. Antes de escrever código: o que o projeto já decidiu

Procure, nesta ordem, e diga ao usuário o que encontrou:

1. **Tokens** — arquivo de variáveis CSS (`tokens.css`, `:root` em `globals.css`), `theme` do
   Tailwind, `theme.ts` de styled-components ou MUI, JSON de tokens exportado do Figma.
2. **Componentes existentes** — `components/`, `ui/`, pacote de design system interno. Tabela,
   botão, campo de data e paginação que já existem são reaproveitados, não reinventados.
3. **Uma tela vizinha** já pronta — ela mostra densidade, alinhamento e tom de texto que o
   usuário espera ver repetidos.
4. **Perfil do projeto** — `.bks-profile.json`, campo `axes.frontend_target`, e o que o
   `brain/engineering/` diz sobre interface.

Achou? Siga. O trabalho é ser consistente, não original. Divergir do sistema existente pede
justificativa e acordo.

Não achou nada? Não invente em silêncio. Proponha a direção em poucas linhas e registre como
tokens antes do primeiro componente. Como decidir está em `references/direcao-visual.md`.

Sem acesso ao código do projeto, pergunte: "Há design system ou tokens a seguir, ou eu proponho
uma direção?" O perfil `frontend` faz a mesma pergunta na criação do projeto.

## 2. Hierarquia antes de estilo

Antes de escolher cor, responda: **o que o usuário veio buscar nesta tela?** Isso ganha o maior
peso visual. O resto recua um passo. A ação secundária não compete com a primária.

Ferramentas de hierarquia, da mais barata para a mais cara: posição, espaço, peso tipográfico,
tamanho, cor. Cor é a última a entrar e nunca é a única portadora de significado.

Uma grade onde todo elemento tem o mesmo peso não tem hierarquia. Padrões por tipo de tela, com
uma listagem completa como exemplo, em `references/estados-e-hierarquia.md`.

## 3. Os estados fazem parte da tela

Uma tela que só existe no caso feliz não está pronta. Para cada região que depende de dado,
projete:

| Estado | O que mostrar |
|---|---|
| carregando | esqueleto com a forma do conteúdo; nada de layout que pula ao chegar o dado |
| vazio de verdade | o que a tela vai conter e a ação que a preenche |
| filtro sem correspondência | os filtros ativos e como limpá-los; é outro estado, não o vazio |
| erro | o que falhou em linguagem de usuário e como tentar de novo; o filtro não se perde |
| parcial / desatualizado | quando a fonte permite, o que está velho e desde quando |

O exemplo de código em `references/estados-e-hierarquia.md` modela os estados como união
discriminada, para que esquecer um vire erro de compilação.

## 4. Acessibilidade não é etapa final

O alvo é a WCAG 2.2, as diretrizes de acessibilidade do W3C, no nível AA, o intermediário. O mínimo que esta skill não negocia:

- **Semântica nativa primeiro:** `button` para ação, `a` para navegação, `table` para dado
  tabular, `label` ligado a todo campo. ARIA, os atributos de acessibilidade do HTML, só onde o elemento nativo não alcança.
- **Contraste:** 4,5:1 para texto, 3:1 para texto grande e para borda de controle e foco.
- **Foco visível** em todo elemento interativo, e nunca escondido sob cabeçalho fixo.
- **Teclado:** tudo que o mouse faz, o teclado faz, na ordem de leitura.
- **Alvo de toque** de pelo menos 24×24 px.
- **Mudança assíncrona anunciada:** contagem de resultados e erro vão para uma região `aria-live`.

Critérios, como testar cada um e os erros que mais aparecem em revisão estão em
`references/acessibilidade.md`.

## 5. Componente e layout

- **Uma responsabilidade por componente.** O que busca dado não desenha linha de tabela.
  Container cuida de estado e efeito; apresentação recebe props e renderiza.
- **Responsivo pelo conteúdo, não pelo aparelho:** o ponto de quebra está onde o conteúdo quebra.
  Tabela larga em tela estreita vira lista de cartões ou ganha rolagem horizontal com a primeira
  coluna fixa, por decisão explícita.
- **Estado de URL:** filtro, página e ordenação vivem na query string. Recarregar e compartilhar
  o link devolvem a mesma tela.

Divisão de componentes, responsividade e composição em `references/componentes.md`.

## 6. Entrega

Ao terminar, a resposta diz em poucas linhas:

1. o que foi reaproveitado do projeto e o que é novo;
2. a direção visual, se precisou ser decidida, e onde ficaram os tokens;
3. a hierarquia: o que tem destaque e por quê;
4. os estados cobertos;
5. o que foi conferido de acessibilidade, e o que ainda pede verificação manual, como leitor de
   tela.

## Referências

| Arquivo | Quando abrir |
|---|---|
| `references/direcao-visual.md` | o projeto não tem tokens, ou os tokens não cobrem o caso |
| `references/estados-e-hierarquia.md` | ao montar listagem, formulário, detalhe ou dashboard |
| `references/acessibilidade.md` | ao escrever qualquer controle interativo, e ao revisar |
| `references/componentes.md` | ao dividir a tela em componentes e definir os pontos de quebra |

## Regras

**O projeto vence.** Token, componente e convenção existentes têm precedência sobre a
preferência desta skill.

**Nenhum valor solto.** Cor, espaço, tamanho de fonte e raio saem de token. Valor literal no
componente é decisão que ninguém registrou.

**Nenhuma tela sem estados.** Carregando, vazio, sem correspondência e erro entram no primeiro
corte, não numa segunda versão.

**Cor nunca é o único sinal.** Status leva texto ou ícone com rótulo, além da cor.
