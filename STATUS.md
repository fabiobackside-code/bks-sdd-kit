# STATUS — prj-bks-kit

> Ponto de entrada do projeto. Leia só este arquivo para saber onde as coisas estão e o que fazer
> a seguir. Atualizado pelo `/save` ao fim de cada sessão; lido pelo `/brain`.
>
> Última atualização: 2026-09-10

---

## Em uma frase

O kit ganhou Go como terceira stack de backend e está instalado como `0.2.0` em uso diário, mas
segue sem medição: a suíte de eval carrega e espera crédito para a primeira baseline — agora com
uma lacuna a mais, porque Go entrou sem caso de eval.

---

## Fase atual

**Manutenção com rede incompleta** — o conteúdo está escrito e validado pelo uso; o que falta é
prova de que cada skill muda a decisão do agente. A fase termina quando houver baseline dos 18
casos com o delta `with` × `without` medido.

---

## O que trava

| Bloqueio | Espera | Quem destrava |
|---|---|---|
| Baseline dos 18 casos de eval | saldo de crédito da conta | Fabio |
| Caso de eval para Go | a baseline acima | — |
| Adelgaçar o `bks-sdd` (2062 linhas) | a baseline acima | — |
| Publicar o repositório | aval do Fabio | Fabio |

O crédito segue sendo o bloqueio de cabeça, isolado e confirmado com casos válidos:
`Ablation: 2 arms × 18 cases` carrega, e todo grader devolve
`judge call failed: Credit balance is too low`.

Go entrou sem caso de eval — os 18 cobrem .NET, TypeScript e os comandos. Escrever caso de Go
antes da baseline seria escrever no escuro: sem saber o delta que os casos existentes produzem,
não há como calibrar o novo.

O adelgaçamento do `bks-sdd` depende da baseline por ordem, não por capricho: refatorar skill
validada em uso sem rede de teste é aposta.

---

## Próximo passo

Exercitar a `bks-go-solutions` numa geração real — é o único passo que não espera crédito. Ela
está instalada (`0.2.0`) e nunca gerou projeto; a entrevista, o registro na base de aprendizado e
a anonimização são caminhos escritos e não percorridos. Um worker ou CLI pequeno basta.

Com crédito disponível, rodar um caso só antes de gastar a suíte:

```
cd X:\2brains\repos\backside\prj-bks-kit
claude plugin eval . --case dotnet-sem-dispatcher --runs 1
```

Se passar, rodar a suíte inteira com `--output-dir evals/results`.

Ao ler o resultado, o número que importa não é o score: é o **delta** entre o braço `with` e o
`without`. Score alto sem delta significa que o modelo já acertava sozinho, e a skill não paga o
próprio contexto.

---

## O que existe

| Peça | Quantidade |
|---|---|
| Skills | 15 |
| Slash commands | 11 |
| Subagentes | 5 |
| Perfis de projeto | 9 |
| Guardas executáveis | 4, todos com teste em `hooks/tests/` |
| Casos de eval | 18, com 85 graders |

`python tests/test_structure.py` → 720 verificações, 3 falhas conhecidas (abaixo).

---

## Decisões que valem

| # | Decisão | Onde |
|---|---|---|
| 1 | Progressive disclosure: `SKILL.md` de entrada + `references/` sob demanda | `docs/ARCHITECTURE.md` |
| 2 | Caminhos por `${BKS_VAULT}` e `${BKS_KNOWLEDGE}`, nunca absolutos | `docs/ARCHITECTURE.md` |
| 3 | Guardas recusam a escrita, não avisam | `docs/ARCHITECTURE.md` |
| 4 | Guarda sem teste é intenção — todo hook tem teste | `docs/ARCHITECTURE.md` |
| 5 | Nove perfis de projeto, quatro eixos transversais | `profiles/README.md` |
| 6 | Renderers de arquitetura são plugáveis; `mermaid` é o padrão | `profiles/architecture-renderers/` |
| 7 | `archify` fica externo — 4.436 linhas de terceiro não viram fork | `profiles/architecture-renderers/archify.md` |
| 8 | Casos de eval seguem o schema do CLI, com guarda no `test_evals` | `docs/ARCHITECTURE.md` |
| 9 | O kit é um projeto em `repos/`, não um caso à parte na raiz do vault | `JOURNAL.md`, 2026-09-10 |
| 10 | Delta de linguagem vive em `bks-standards`, não na skill geradora | `docs/ARCHITECTURE.md` |
| 11 | A skill de Go lê e alimenta base de aprendizado fora do projeto, anonimizada | `docs/ARCHITECTURE.md` |

---

## Aberto

- Três falhas conhecidas no `test_structure.py`, não diagnosticadas: referência inalcançável pelo
  `SKILL.md` em `bks-arch`, comando não documentado, e mais de um renderer marcado como padrão. A
  quarta era acento — `documentação.md` citado, `documentacao.md` em disco (`607d5e1`)
- Nenhum caso de eval cobre Go; os 18 existentes são de .NET, TypeScript e comandos
- A base de aprendizado em `${BKS_KNOWLEDGE}/wiki/go/` está criada e vazia, e não é versionada:
  `knowledge/**` está no `.gitignore` do vault, logo ela existe só nesta máquina
- Ícones genéricos de infraestrutura declarados em `skills/bks-arch/icons/` mas não desenhados
- `bks-sdd` com 2062 linhas num `SKILL.md` único — o adelgaçamento está planejado, não iniciado
- O repositório não tem `brain/domain/` nem `brain/engineering/`; o conhecimento está todo em
  `docs/ARCHITECTURE.md` e nas próprias skills
- Repositório ainda não publicado

---

## Mapa dos documentos

| Documento | Para que |
|---|---|
| este arquivo | onde parei, o que trava, próximo passo |
| `WORKFLOW.md` | o ciclo mudar → provar → medir |
| `JOURNAL.md` | como o kit chegou até aqui |
| `CLAUDE.md` | o que uma sessão carrega ao abrir aqui |
| `docs/ARCHITECTURE.md` | as decisões estruturais, com o porquê |
| `docs/MIGRATION.md` | o que muda para quem consome |
| `README.md` | o que o kit é, para quem chega de fora |
| `profiles/README.md` | os nove perfis e os quatro eixos |
| `evals/README.md` | o que cada caso mede |
