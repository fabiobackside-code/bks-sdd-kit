# Acessibilidade — WCAG 2.2 AA no código, não no relatório

A WCAG 2.2 (Web Content Accessibility Guidelines) é a norma do W3C para acessibilidade web, com
critérios em três níveis: A, AA e AAA. O nível AA é o alvo de qualquer interface desta skill. Esta referência traz o que mais
aparece em tela de produto e como conferir cada item sem ferramenta paga.

## Os critérios que mais quebram

| Critério | Exigência | Como conferir |
|---|---|---|
| 1.1.1 conteúdo não textual | imagem informativa tem `alt`; decorativa tem `alt=""` | inspecionar cada `img` e ícone sem texto |
| 1.3.1 informação e relações | estrutura visual existe no HTML: cabeçalho, lista, tabela, `label` | navegar só por cabeçalhos no leitor de tela |
| 1.4.3 contraste mínimo | 4,5:1 texto normal; 3:1 texto a partir de 24 px, ou 18,66 px em negrito | DevTools, painel de acessibilidade |
| 1.4.10 refluxo | nada se perde a 320 px de largura, sem rolagem nas duas direções | zoom de 400% em tela de 1280 px |
| 1.4.11 contraste não textual | borda de campo, ícone funcional e foco a 3:1 | mesma ferramenta, sobre a borda |
| 2.1.1 teclado | toda função alcançável por Tab, Enter, Espaço e setas | desconectar o mouse e usar a tela |
| 2.4.3 ordem do foco | segue a ordem de leitura | Tab do topo ao fim |
| 2.4.7 foco visível | indicador de foco em todo controle | Tab e olhar |
| 2.4.11 foco não encoberto | o elemento focado não fica sob cabeçalho fixo ou banner | Tab perto das bordas |
| 2.5.7 movimento de arrastar | arrastar tem alternativa por clique | procurar todo drag and drop |
| 2.5.8 tamanho do alvo | 24×24 px, ou espaçamento equivalente | inspecionar ícones-botão |
| 3.3.1 identificação de erro | o erro diz qual campo e o que está errado, em texto | enviar o formulário vazio |
| 3.3.7 entrada redundante | dado já informado no fluxo não é pedido de novo | percorrer o fluxo inteiro |
| 3.3.8 autenticação acessível | login não exige memorizar nem transcrever; colar senha funciona | testar o campo de senha |
| 4.1.2 nome, função, valor | controle customizado expõe nome, papel e estado | leitor de tela anuncia o controle |
| 4.1.3 mensagens de status | resultado e erro assíncronos chegam ao leitor sem mover o foco | região `aria-live` |

Os critérios 2.4.11, 2.5.7, 2.5.8, 3.3.7 e 3.3.8 entraram na versão 2.2. São os mais esquecidos
porque checklist antigo não os tem.

## Semântica antes de ARIA

ARIA (Accessible Rich Internet Applications) são atributos que descrevem papel e estado de um
elemento para a tecnologia assistiva.

O HTML nativo já entrega papel, estado e teclado. ARIA só corrige o que o HTML não alcança.

```tsx
<button type="button" onClick={onRetry}>Tentar de novo</button>

<a href={`/orders/${order.id}`}>{order.number}</a>

<label htmlFor="status-filter">Status</label>
<select id="status-filter" value={status} onChange={onStatusChange}>
  <option value="">Todos</option>
  <option value="paid">Pago</option>
</select>
```

Um `div` com `onClick` não recebe foco, não responde a Enter e não é anunciado como botão. Corrigir
isso à mão pede `role`, `tabIndex` e tratamento de tecla, e ainda fica atrás do `button`.

## Tabela de dados

- `<caption>` com o título da tabela, que pode ficar visualmente oculto.
- `<th scope="col">` em cada cabeçalho.
- Coluna ordenável: o botão fica dentro do `th`, e o `th` recebe `aria-sort` com o sentido atual.
- Linha clicável não substitui um link na primeira coluna. Quem usa teclado precisa de um alvo
  focável.

## Foco

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

html {
  scroll-padding-top: 4rem;
}
```

O `scroll-padding-top` com a altura do cabeçalho fixo evita que o elemento focado fique escondido
sob ele. Remover o `outline` sem colocar outro indicador no lugar reprova o 2.4.7.

Ao abrir um diálogo, o foco vai para dentro dele e fica preso ali até fechar. Ao fechar, volta
para o controle que o abriu. O elemento `dialog` nativo com `showModal()` já faz o confinamento.

## Mudança assíncrona

```tsx
<p role="status" aria-live="polite" className="visually-hidden">
  {resultCountMessage}
</p>
```

A região existe desde a primeira renderização. Criá-la junto com a mensagem faz o leitor de tela
não anunciar nada. Erro que bloqueia a tarefa usa `role="alert"`.

## Formulário

- Todo campo tem `label` visível. Placeholder não é rótulo: some ao digitar.
- O erro fica ao lado do campo, ligado por `aria-describedby`, e o campo recebe
  `aria-invalid="true"`.
- No envio com erro, o foco vai para o primeiro campo inválido ou para um resumo de erros no topo.
- `autocomplete` correto em nome, e-mail, telefone e endereço.

## O que a ferramenta automática não pega

Verificador automático encontra perto de um terço dos problemas. Ordem de foco que não faz
sentido, texto alternativo inútil e anúncio que confunde só aparecem usando a tela com teclado e
com leitor de tela, como NVDA no Windows ou VoiceOver no macOS. A entrega diz o que foi conferido
assim e o que ficou pendente.
