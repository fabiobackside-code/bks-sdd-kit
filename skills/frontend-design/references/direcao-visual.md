# Direção visual — decidir quando o projeto ainda não decidiu

Quando o projeto não tem tokens, a direção visual é decidida uma vez, em poucas linhas, e vira
código antes do primeiro componente. Decidir depois significa reescrever cada componente.

## A direção cabe em cinco decisões

Proponha ao usuário, numa tabela curta, e só então gere os tokens:

| Decisão | Pergunta que a resolve | Exemplo para um back-office |
|---|---|---|
| tom | a interface é ferramenta de trabalho, vitrine ou leitura longa? | ferramenta: densa, calma |
| tipografia | uma família ou duas? números precisam alinhar em coluna? | uma família sem serifa com algarismos tabulares |
| escala | qual a razão entre tamanhos consecutivos? | 1,2 — contraste discreto, cabe muito dado |
| cor | qual a cor de ação? quantos neutros? que cores de status? | um azul de ação, 8 neutros, 4 status |
| espaço | qual a unidade base? | 4 px, com degraus 4, 8, 12, 16, 24, 32, 48 |

O tom decide os outros quatro. Ferramenta de trabalho pede densidade e contraste baixo entre
superfícies. Vitrine aceita escala tipográfica mais larga e mais espaço em branco. Leitura longa
pede linha de 60 a 75 caracteres e corpo de 17 px ou mais.

## Por que não o default do framework

O default existe para funcionar em qualquer projeto, por isso não diz nada sobre nenhum. Os sinais
mais comuns de que a tela ficou no default:

- toda superfície com a mesma sombra média e o mesmo raio grande;
- a cor primária do framework em todo botão, link e cabeçalho ao mesmo tempo;
- todo texto no mesmo tamanho, com negrito como único recurso de hierarquia;
- espaçamento que não segue degrau nenhum: 13 px aqui, 18 px ali;
- gradiente ou ilustração decorativa sem função.

Sobriedade é uma direção legítima. A diferença é que ela foi escolhida: poucas cores, escala
contida, um único acento usado onde há ação.

## Os tokens, em três camadas

**Primitivo** é o valor cru: `--blue-600`. **Semântico** diz o papel: `--color-action`.
**Componente**, quando precisa, especializa: `--table-row-hover`. O componente consome a camada
semântica. Trocar o tema muda a camada semântica e não toca em componente.

```css
:root {
  /* primitivos */
  --gray-0: #ffffff;
  --gray-50: #f6f7f9;
  --gray-200: #dde1e6;
  --gray-500: #6b7380;
  --gray-700: #3d4450;
  --gray-900: #171a1f;
  --blue-600: #1f5fbf;
  --blue-700: #194d9b;
  --red-600: #b42318;
  --green-700: #1d6b3f;
  --amber-700: #8a5a00;

  /* semânticos */
  --color-bg: var(--gray-50);
  --color-surface: var(--gray-0);
  --color-border: var(--gray-200);
  --color-text: var(--gray-900);
  --color-text-muted: var(--gray-700);
  --color-text-subtle: var(--gray-500);
  --color-action: var(--blue-600);
  --color-action-hover: var(--blue-700);
  --color-focus: var(--blue-600);
  --color-danger: var(--red-600);
  --color-success: var(--green-700);
  --color-warning: var(--amber-700);

  --font-sans: "Inter", system-ui, sans-serif;
  --font-numeric: tabular-nums;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-md: 1rem;
  --text-lg: 1.2rem;
  --text-xl: 1.44rem;
  --leading-tight: 1.25;
  --leading-normal: 1.5;

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;

  --radius-sm: 4px;
  --radius-md: 6px;
  --shadow-raised: 0 1px 2px rgb(23 26 31 / 0.08);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: var(--gray-900);
    --color-surface: #20242b;
    --color-border: #343a44;
    --color-text: #eef0f3;
    --color-text-muted: #c3c8d0;
    --color-text-subtle: #9aa1ac;
  }
}
```

O `--gray-500` é o texto mais claro permitido sobre branco: contraste de 4,8:1. Abaixo disso o
texto deixa de passar no AA. Cada par texto/fundo dos tokens semânticos é conferido uma vez, na
criação, e não em cada tela.

## Onde registrar

- Os tokens ficam num arquivo só, importado na raiz da aplicação.
- Com Tailwind, os tokens semânticos entram em `theme.extend` apontando para as variáveis CSS, e
  as classes utilitárias de cor crua deixam de ser usadas no código de tela.
- A direção, com as cinco decisões e o motivo de cada uma, vai para o `ARCHITECTURE.md` do
  projeto. O arquivo de tokens não carrega a justificativa em comentário.

## Movimento

Animação explica mudança de estado: um painel que abre, uma linha que some. Fora disso, é ruído.
Duração entre 120 e 240 ms para interface de trabalho. Respeite `prefers-reduced-motion`
reduzindo a transição a uma troca de opacidade ou a nada.
