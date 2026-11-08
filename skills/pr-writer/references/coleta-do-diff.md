# Coleta do diff — o que rodar e como ler

A descrição só é tão boa quanto a leitura do diff. Esta referência cobre como achar a base certa,
como ler diff grande sem perder o que importa e onde o projeto guarda as convenções de PR.

## Achar a base

A base é a branch para onde o PR vai. Em ordem de preferência:

1. o que o usuário disse;
2. a branch upstream configurada, se for a de destino: `git rev-parse --abbrev-ref @{upstream}`;
3. a branch padrão do remoto: `git symbolic-ref refs/remotes/origin/HEAD`;
4. com GitHub CLI: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.

Fluxo com `develop` e `release/*` costuma ter base diferente da padrão. Na dúvida, pergunte.

Atualize a referência remota antes de comparar, com `git fetch origin <base>`. Comparar com uma
cópia local velha da base mostra no diff mudanças que já estão nela.

## Os comandos e o que cada um responde

| Comando | Responde |
|---|---|
| `git log --oneline --no-merges origin/<base>..HEAD` | quantos commits e qual a narrativa do autor |
| `git log --format='%h %s%n%b' origin/<base>..HEAD` | o corpo das mensagens, onde costuma estar o porquê |
| `git diff --stat origin/<base>...HEAD` | o tamanho e as áreas tocadas |
| `git diff --name-status origin/<base>...HEAD` | arquivos novos, removidos e renomeados |
| `git diff origin/<base>...HEAD -- <caminho>` | o detalhe de uma área |
| `git diff -M origin/<base>...HEAD` | renomeação detectada como renomeação, não como apagar e criar |

Dois pontos no `log`, três no `diff`. O `log A..B` lista os commits de B que não estão em A. O
`diff A...B` compara B com o ancestral comum, e por isso ignora o que entrou na base depois que a
branch saiu.

Se o PR já existe: `gh pr diff <número>` e `gh pr view <número> --json title,body,commits`. No
GitLab: `glab mr diff <número>`.

## Mudanças não commitadas

Rode `git status --short`. Arquivo modificado e não commitado não estará no PR. Avise o usuário
antes de escrever, em vez de descrever o que não vai subir.

## Ler diff grande

1. Pelo `--stat`, separe em grupos: código de produção por camada, testes, migration,
   configuração, documentação, arquivo gerado e lockfile.
2. Leia primeiro o que muda contrato: rota, DTO, evento, migration, `appsettings`, variável de
   ambiente. É o que o revisor mais precisa ver.
3. Depois o código de domínio e aplicação, onde está a regra.
4. Testes: o que cobrem e se cobrem o que mudou.
5. Arquivo gerado e lockfile: só confirme que a mudança é esperada. Lockfile alterado sem
   dependência nova declarada é achado.

Diff que mistura renomeação em massa com mudança de regra é difícil de ler. Use
`git diff -M --stat` para separar, e considere sugerir a divisão.

## Template e convenção do projeto

Procure, nesta ordem:

| Onde | O que define |
|---|---|
| `.github/PULL_REQUEST_TEMPLATE.md` ou a pasta `.github/PULL_REQUEST_TEMPLATE/` | seções do corpo no GitHub |
| `.gitlab/merge_request_templates/*.md` | seções do corpo no GitLab |
| `CONTRIBUTING.md` | título, idioma, vínculo com issue, checklist |
| `commitlint.config.*` ou `.commitlintrc*` | tipos e escopos aceitos no título |
| `gh pr list --state merged --limit 10 --json title` | a convenção que o time pratica |

Quando o template e a prática divergem, siga o template e mencione a divergência em uma linha.

Template com checklist: marque só o que o diff comprova. Um item "testes adicionados" fica
desmarcado se o diff não tem teste, e a descrição diz por quê.

## Vínculo com issue e spec

- Nome da branch como `feat/123-desconto-progressivo` indica a issue 123.
- Mensagens de commit com `Refs #123`, `Closes #123` ou o código de uma task.
- Projeto SDD: a FEAT ou a TASK em `specs/` diz o critério de aceite. A seção "Como verificar"
  pode citar os critérios que o diff atende.

`Closes #123` fecha a issue no merge. Use só quando o PR resolve a issue inteira; senão, `Refs`.
