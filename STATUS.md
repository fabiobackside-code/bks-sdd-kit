# STATUS — prj-bks-kit

> Ponto de entrada do projeto. Leia só este arquivo para saber onde as coisas estão e o que fazer
> a seguir. Atualizado pelo `/bks:save` ao fim de cada sessão; lido pelo `/bks:brain`.
>
> Última atualização: 2026-10-14

---

## Em uma frase

O kit ganhou a skill `bks-writing`, o padrão de escrita da documentação viva que nasceu no
NQuantic, com a guarda `writing_guard` depois de cada escrita e o `/bks:review` conferindo a
escrita. A `0.6.0` está na `main` do GitHub, pelo PR #1, e instalada nesta máquina. Falta o eval do caso
novo, o caminho do alerta do `/bks:save` e a baseline, parada por crédito.

---

## Fase atual

**Manutenção com rede incompleta** — o conteúdo está escrito e validado pelo uso; o que falta é
prova de que cada skill muda a decisão do agente. A fase termina quando houver baseline dos 19
casos com o delta `with` × `without` medido.

---

## O que trava

| Bloqueio | Espera | Quem destrava |
|---|---|---|
| Eval do caso `writing-decisao-no-texto` | saldo de crédito da conta | Fabio |
| Testar o `/bks:save` no caminho do alerta | árvore limpa no `dash-scheduller` | Fabio |
| Decidir se o `planner` fica em Opus | dez FEATs medidas contra as dez anteriores | Fabio |
| Baseline dos 19 casos de eval | saldo de crédito da conta | Fabio |
| Caso de eval para Go | a baseline acima | — |
| Adelgaçar o `bks-sdd` (2062 linhas) | a baseline acima | — |

O `/bks:save` rodou duas vezes nesta data pelo caminho do silêncio, e a segunda valeu: o prompt
trouxe os passos 4 e 7, que só a versão unificada tem. O falso positivo mais caro — alertar
projeto sem canônico — está descartado por execução.

O caminho do alerta segue sem prova. A detecção foi verificada isolada no `dash-scheduller`, onde
o `find` do passo 4 devolve `decisions/ADR-003.md` e `decisions/ADR-004.md`, mais novos que o
`CONTEXT.md`. Falta o comando inteiro, e ele espera a árvore daquele projeto: 17 arquivos
modificados de uma sessão de `/canonize` inacabada, incluindo o `STATUS.md` que o comando
reescreveria por inteiro.

O `planner` subiu para Opus nesta sessão, para medição. A comparação não se faz lendo duas specs —
o método está no `ARCHITECTURE.md`: tentativas do LOOP-4, achados do `reviewer` e retrabalho de
FEAT aprovada, medidos sobre dez specs contra as dez anteriores.

O crédito segue sendo o bloqueio de cabeça da eval, isolado e confirmado com casos válidos:
`Ablation: 2 arms × 18 cases` carrega, e todo grader devolve
`judge call failed: Credit balance is too low`.

A `bks-writing` foi verificada sem modelo: a suíte estrutural passa, os 20 testes da guarda passam,
e a guarda conta o mesmo que o `Conferir-Escrita.ps1` do NQuantic — 75 achados no `ARCHITECTURE.md`
do motor antes da reescrita, nenhum depois. Se a skill muda a decisão do agente, só o eval diz, e
ele não rodou. O hook novo só vale depois de reiniciar a sessão.

Go entrou sem caso de eval — os 18 primeiros cobrem .NET, TypeScript e os comandos. Escrever caso de Go
antes da baseline seria escrever no escuro. O adelgaçamento do `bks-sdd` depende da baseline pela
mesma razão: refatorar skill validada em uso sem rede de teste é aposta.

---

## Próximo passo

Abrir uma sessão nova em qualquer projeto, editar um `README.md` e conferir que o hook devolve os
achados e mostra o lembrete do `/bks:review`. O merge já aconteceu, então falha aqui vira correção
na `main`.

Com crédito, o caso novo primeiro, antes da suíte:

```
claude plugin eval . --case writing-decisao-no-texto --runs 1
```

O caminho do alerta, no `dash-scheduller`. Commitar ou descartar os 17 arquivos dele primeiro — o
`/bks:save` reescreve o `STATUS.md` por inteiro, e rodar sobre trabalho inacabado misturaria a
classificação dele com a do teste. O esperado é uma linha na seção do que trava nomeando o
`CONTEXT.md` e os dois ADRs mais novos que ele.

Acumular dez FEATs com o `planner` em Opus e comparar contra as dez anteriores, pelos três sinais
do `ARCHITECTURE.md`. Sem isso, a escolha de tier volta a ser opinião.

Segue valendo, e não espera crédito: exercitar a `bks-go-solutions` numa geração real. Ela nunca
gerou projeto; a entrevista, o registro na base de aprendizado e a anonimização são caminhos
escritos e não percorridos.

Com crédito disponível, a suíte segue o mesmo caminho, um caso por vez:

```
cd ${BKS_VAULT}/repos/backside/prj-bks-kit
claude plugin eval . --case dotnet-sem-dispatcher --runs 1
```

Ao ler o resultado, o número que importa não é o score: é o **delta** entre o braço `with` e o
`without`. Score alto sem delta significa que o modelo já acertava sozinho.

---

## O que existe

| Peça | Quantidade |
|---|---|
| Skills | 16 |
| Slash commands | 11 |
| Subagentes | 5 |
| Perfis de projeto | 9 |
| Versão publicada | `0.6.0`, na `main` |
| Guardas executáveis | 5, todos com teste em `hooks/tests/` |
| Casos de eval | 19, com 91 graders |

`python tests/test_structure.py` → 763 verificações, 0 falhas.
`bash hooks/tests/run.sh` → `falhas: 0` nas três suítes.

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
| 12 | O canônico é realimentado pela spec; o `/bks:save` acusa, o `/bks:canonize` corrige | `docs/ARCHITECTURE.md` |
| 13 | Comando do método existe só no plugin; a instalação global morreu | `docs/ARCHITECTURE.md` |
| 14 | Ponteiro para arquivo do kit é verificado pela suíte, acento incluído | `docs/ARCHITECTURE.md` |
| 15 | O namespace é `bks`; comando de plugin sempre tem prefixo | `docs/ARCHITECTURE.md` |
| 16 | O tier do agente é anunciado, e o subagente entra na medição | `docs/ARCHITECTURE.md` |
| 17 | `planner` em Opus: spec errada contamina toda task abaixo | `docs/ARCHITECTURE.md` |
| 18 | A decisão entra no texto; o número do ADR fica só no fim da nota de decisão | `skills/bks-writing/SKILL.md` |
| 19 | A guarda de escrita roda depois da escrita, devolve achados e lembra o `/bks:review` | `docs/ARCHITECTURE.md` |
| 20 | Skill de terceiro é vendorizada como consulta, com licença e mapeamento, nunca instalada | `docs/ARCHITECTURE.md` |
| 21 | Comentário de código não aponta para documento | `docs/ARCHITECTURE.md` |
| 22 | `/bks:canonize` confronta a skill referenciada com o que o projeto concretizou | `docs/ARCHITECTURE.md` |

---

## Aberto

- O frontmatter dos renderers usa a chave `padrão`, com acento, contra a regra de que chave de
  frontmatter segue ASCII. A suíte aceita as duas grafias; a decisão de padronizar a chave e migrar
  os cinco arquivos está em aberto
- Nenhum caso de eval cobre Go; os 19 existentes são de .NET, TypeScript, escrita e comandos
- O `README.md` e o `docs/ARCHITECTURE.md` do kit têm 17 achados da guarda de escrita, todos em
  texto anterior a esta sessão: siglas sem definição e três frases longas
- O vínculo da spec com a decisão no frontmatter (`relacionada:`) entrou no template FEAT e no
  `planner`; o NQuantic ainda o trata como proposta em aberto
- A base de aprendizado em `${BKS_KNOWLEDGE}/wiki/go/` está criada e vazia, e não é versionada:
  `knowledge/**` está no `.gitignore` do vault, logo ela existe só nesta máquina
- Ícones genéricos de infraestrutura declarados em `skills/bks-arch/icons/` mas não desenhados
- `bks-sdd` com 2062 linhas num `SKILL.md` único — o adelgaçamento está planejado, não iniciado
- O repositório não tem `brain/domain/` nem `brain/engineering/`; o conhecimento está todo em
  `docs/ARCHITECTURE.md` e nas próprias skills
- O `/bks:save` foi exercitado só no caminho do silêncio; o do alerta segue sem prova
- `skills/bks-sdd/SKILL.md` cita dois arquivos de um pipeline Node.js que não existe no repositório,
  marcados como exceção conhecida em `tests/test_structure.py`
- A regra nova não tem guarda executável, e o kit exige que tenha. A guarda cairia no projeto
  consumidor, não aqui — é o primeiro caso em que a regra vale para fora e o teste não tem onde
  morar deste lado
- A detecção usa `mtime`, então spec mexida só na formatação acusa divergência. Escolha consciente,
  registrada no `ARCHITECTURE.md`: o falso positivo custa uma reconsolidação, o falso negativo
  custa um canônico errado alimentando o `/bks:prd`
- Doze decisões fora do canônico em três projetos consumidores, achado desta sessão e não
  endereçado: `layan` v2 com sete ADRs posteriores, `nquantic` v6 com uma FEAT, um TEST e o
  ADR-024, `dash-scheduller` v6 com ADR-003 e ADR-004. O `layan` é o pior caso
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
