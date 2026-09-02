# Emitir em archify

## Antes de comecar

O `archify` e skill externa e nao vem no kit. Verifique se esta instalada.

**Se nao estiver:** avise em uma linha e gere em Mermaid. Nao falhe, e nao peca ao usuario para
instalar no meio do trabalho.

## Aplicar a paleta BKS

O `archify` tem estilo proprio. Sem sobrepor as cores, o diagrama sai no estilo dele — nao no seu.

Defina a cor de cada no pelo papel semantico:

| Papel | fill | stroke | color |
|---|---|---|---|
| backend | `#336698` | `#1F4266` | `#FFFFFF` |
| storage | `#4A7C63` | `#2E5140` | `#FFFFFF` |
| broker | `#B5713C` | `#8A5228` | `#FFFFFF` |
| acesso | `#9E4B4B` | `#733535` | `#FFFFFF` |
| componente | `#B39038` | `#8A6E26` | `#1A1A1A` |
| externo | `#6B7280` | `#4B5563` | `#FFFFFF` |
| destaque | `#98CBFF` | `#336698` | `#1A1A1A` |

Tema escuro: os tokens de fundo e texto estao em `paleta.md`. O `archify` suporta os dois temas —
verifique o contraste nos dois antes de entregar.

## Linhas

Continua para sincrono, tracejada para assincrono. A convencao e a mesma do Mermaid; muda so a
sintaxe do motor.

## Icones de infraestrutura

Use os SVG genericos de `../icons/`. O kit nao distribui marca de terceiro — logo oficial de AWS,
Azure ou Kafka tem licenca de uso de marca, e redistribuir num pacote MIT criaria um problema que
nao e nosso.

Nos seus proprios diagramas, use o que quiser. A restricao vale para o que o kit distribui.

## Versionamento

O `archify` gera HTML, e um HTML de centenas de kilobytes nao se revisa em diff.

**Versione o arquivo de entrada** — o JSON ou a descricao que gerou o diagrama. O HTML e saida,
como binario compilado: vai para `outputs/`, e o `.gitignore` do projeto decide se acompanha o
repositorio.

## Quando vale a pena

- infraestrutura com logo e posicionamento controlado
- entrega para apresentacao ou consulta, nao para revisao em diff
- sistema grande, onde navegar por camadas ajuda mais que ver tudo de uma vez
- reconstrucao de arquitetura de legado, onde explorar importa mais que versionar

Fora disso, Mermaid entrega o mesmo com menos dependencia.
