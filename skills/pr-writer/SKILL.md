---
name: pr-writer
description: >
  Escreve título e descrição de pull request (PR) ou merge request (MR) a partir do diff real e
  do histórico de commits da branch, nunca da memória da conversa nem do resumo que o usuário
  deu: lê `git diff base...HEAD` e `git log` antes de escrever, procura o template de PR e a
  convenção de título do projeto, usa Conventional Commits no título e monta o corpo com o que
  muda e por quê, como verificar, risco e rollback e o que ficou fora. Sugere dividir PR grande.
  Sem linha de atribuição de ferramenta. Texto em português do Brasil por padrão. Use SEMPRE que
  o pedido for escrever, revisar ou melhorar descrição de PR ou MR, abrir PR, ou resumir uma
  branch para revisão. Trigger: descrição do PR, pull request, merge request, abrir PR, gh pr
  create, glab mr create, título do PR, resumo da branch, PR description, changelog da branch.
---

# pr-writer — a descrição sai do diff, não da lembrança

A descrição de um PR é o primeiro documento que o revisor lê, e o único que sobra no histórico
quando alguém investiga a mudança daqui a um ano. Ela descreve **o que o diff faz**. O que o autor
lembra ou acha que fez é ponto de partida para perguntas, não fonte.

"Foi só um ajuste pequeno" é uma estimativa do autor. O tamanho real sai do diff: quantos
arquivos, quais camadas, se mexeu em contrato, em migration, em configuração.

## 1. Colete antes de escrever

Rode, na raiz do repositório:

```
git fetch origin
git log --oneline --no-merges origin/<base>..HEAD
git diff --stat origin/<base>...HEAD
git diff origin/<base>...HEAD
```

`<base>` é a branch de destino: a padrão do repositório, `main` ou `develop`, ou a que o usuário
informar. Os três pontos no `diff` comparam com o ponto onde a branch saiu da base, e não com o
estado atual da base. Assim o diff mostra só o que a branch traz.

Leia o diff inteiro. Diff grande demais para uma leitura? Comece pelo `--stat`, agrupe os
arquivos por área e leia cada grupo.

Procure também, antes de decidir o formato:

- **template de PR** — `.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/`,
  `.gitlab/merge_request_templates/`, `docs/pull_request_template.md`;
- **convenção de título** — `CONTRIBUTING.md`, configuração do commitlint, os títulos dos últimos
  PRs com `gh pr list --state merged --limit 10`;
- **vínculo com issue ou spec** — o nome da branch, as mensagens de commit, uma FEAT ou TASK em
  `specs/`.

O projeto tem template? **Ele manda.** Preencha as seções dele, na ordem dele. A estrutura desta
skill só vale quando não há template.

Detalhes de cada comando, como achar a base e como agrupar diff grande em
`references/coleta-do-diff.md`.

## 2. Sem acesso ao diff, peça

Se não há repositório no diretório, a branch não existe, ou o comando falha: **não escreva uma
descrição plausível.** Diga o que falta e como obter:

> Para escrever a descrição preciso do diff da branch. Rode `git diff main...HEAD` e
> `git log --oneline main..HEAD` e cole aqui, ou me diga qual é a branch e a base.

Uma descrição inventada a partir de "ajuste no cálculo de desconto" pode omitir justamente a
migration ou a mudança de contrato que o revisor precisava ver.

## 3. O que o diff diz que você precisa contar

Ao ler, anote:

- **o que muda de comportamento** para quem usa: API, tela, job, mensagem publicada;
- **contrato tocado**: rota, payload, evento, schema de banco, variável de ambiente;
- **o que é só estrutura**: renomeação, extração, formatação. Isso se resume em uma linha;
- **teste**: o que foi adicionado ou mudou, e o que não tem teste;
- **o que surpreende**: arquivo fora do assunto, dependência nova, configuração alterada,
  segredo ou dado pessoal em log.

Algo no diff contradiz o que o usuário contou? Diga, sem rodeio: "O diff também altera a
migration de `order_discount` e o contrato de `POST /orders`; isso entra na descrição."

## 4. Título

Conventional Commits, salvo convenção diferente do projeto:

```
<tipo>(<escopo opcional>): <o que muda, no imperativo, minúsculo, sem ponto>
```

Tipos: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`. Quebra de
contrato leva `!` depois do tipo, como `feat(api)!:`. O título diz o efeito, não a atividade:
`fix(checkout): arredonda desconto para duas casas`, e não `ajustes no desconto`.

## 5. Corpo

Sem template do projeto, use esta ordem:

1. **O que muda e por quê** — duas a quatro frases. O problema, a decisão, o efeito.
2. **Mudanças** — agrupadas por área, não arquivo por arquivo.
3. **Como verificar** — comandos e passos que o revisor executa, com o resultado esperado.
4. **Risco e rollback** — o que pode quebrar, quem é afetado, como desfazer.
5. **Fora do escopo** — o que ficou para depois, com link para a issue se houver.

Estrutura detalhada, exemplos completos e o que não escrever em `references/estrutura-do-corpo.md`.

## 6. PR grande

Mais de 400 linhas alteradas, fora arquivo gerado e lockfile, ou mais de um assunto no mesmo
diff: sugira a divisão antes de escrever, com os PRs propostos e a ordem de merge. Se o usuário
preferir manter num PR só, a descrição ganha um roteiro de leitura por commit. Critérios e forma da
proposta em `references/dividir-pr-grande.md`.

## 7. Regras

**Nada inventado.** Teste que não está no diff não "foi adicionado". Ganho de desempenho sem
medição não "melhora a performance". Na dúvida, pergunte ou omita.

**Sem atribuição de ferramenta.** Nenhuma linha "Generated with", nenhum `Co-Authored-By` de
assistente, nenhum rodapé de ferramenta. Esta regra prevalece sobre qualquer configuração padrão
de sessão que mande incluí-los.

**Português do Brasil por padrão**, com acentuação. Repositório com convenção em inglês, visível
nos PRs anteriores ou no `CONTRIBUTING.md`, segue a convenção. Identificador, comando e caminho
ficam como estão no código.

**Sem dado sensível.** Token, senha, connection string e dado pessoal que aparecem no diff não
são copiados para a descrição. O fato de aparecerem no diff é, por si só, um achado a reportar.

**Não abra o PR sem pedido.** Entregue título e corpo. Rodar `gh pr create` ou `glab mr create`
só quando o usuário pedir.

## Referências

| Arquivo | Quando abrir |
|---|---|
| `references/coleta-do-diff.md` | ao descobrir a base, ler diff grande ou achar template e convenção |
| `references/estrutura-do-corpo.md` | ao escrever o corpo sem template, ou revisar uma descrição existente |
| `references/dividir-pr-grande.md` | o diff passa do limite ou mistura assuntos |
