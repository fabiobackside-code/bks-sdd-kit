# Renderers de arquitetura

Registro extensivel. Cada arquivo declara um jeito de desenhar diagrama.

**Adicionar** e criar um arquivo. **Substituir** e trocar o conteudo de um. Nenhuma skill do kit
tem renderer embutido — todas leem este diretorio.

A notacao — paleta, semantica de cor, convencao de linha — e a mesma para todos, e vive em
`skills/bks-arch/`. O renderer decide **como desenhar**; a notacao decide **o que cada cor e cada
linha significam**.

## Disponiveis

| Renderer | Tipo | Notacao | Logo de infra |
|---|---|---|---|
| [`mermaid`](mermaid.md) | nativo | completa | nao |
| [`archify`](archify.md) | skill externa | completa | sim |
| [`c4`](c4.md) | template + mermaid | completa | nao |
| [`togaf`](togaf.md) | template documental | parcial | nao |

`mermaid` e o padrao: nativo, versionavel em texto, sem dependencia.

## Formato

Ver [`_TEMPLATE.md`](_TEMPLATE.md).
