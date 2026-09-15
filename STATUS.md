# STATUS — prj-bks-kit

> Ponto de entrada do projeto. Leia só este arquivo para saber onde as coisas estão e o que fazer
> a seguir. Atualizado pelo `/save` ao fim de cada sessão; lido pelo `/brain`.
>
> Última atualização: 2026-09-15

---

## Em uma frase

Os onze comandos deixaram de existir em duas cópias: a instalação global morreu e o plugin é a
única origem. O `/save` unificado está instalado como `0.3.0` e rodou pela primeira vez, aqui, pelo
caminho do silêncio — o comando certo, desta vez. Falta o caminho do alerta. A medição de eval
segue parada esperando crédito.

---

## Fase atual

**Manutenção com rede incompleta** — o conteúdo está escrito e validado pelo uso; o que falta é
prova de que cada skill muda a decisão do agente. A fase termina quando houver baseline dos 18
casos com o delta `with` × `without` medido.

---

## O que trava

| Bloqueio | Espera | Quem destrava |
|---|---|---|
| Testar o `/save` 0.3.0 no caminho do alerta | árvore limpa no `dash-scheduller` | Fabio |
| Empurrar os 15 commits da `main` | aval do Fabio | Fabio |
| Baseline dos 18 casos de eval | saldo de crédito da conta | Fabio |
| Caso de eval para Go | a baseline acima | — |
| Adelgaçar o `bks-sdd` (2062 linhas) | a baseline acima | — |
| Publicar o repositório | aval do Fabio | Fabio |

O `/save` de `0.3.0` rodou nesta sessão, depois do `claude plugin update`, e o passo 4 ficou em
silêncio como previsto: não existe `docs/canonical/CONTEXT.md` aqui, e nenhuma linha de defasagem
foi acrescentada. Desta vez o comando exercitado é o certo — o prompt trouxe os passos 4 e 7, que
só a `0.3.0` tem. O falso positivo mais caro, alertar projeto sem canônico, está descartado por
execução.

Falta o caminho do alerta: o `dash-scheduller`, com a árvore dele limpa antes. O `/save` reescreve
o `STATUS.md` por inteiro, e rodar sobre trabalho inacabado misturaria a classificação dele com a
do teste.

O alvo escolhido foi o `dash-scheduller`, e ele estava com dez arquivos modificados sem commit,
incluindo o próprio `STATUS.md` e o `CONTEXT.md`. O `/save` reescreve o `STATUS.md` por inteiro —
rodar sobre trabalho alheio inacabado misturaria a classificação dele com a do teste.

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

O caminho do alerta, no `dash-scheduller`. Commitar ou descartar os dez arquivos modificados dele
primeiro. O esperado é uma linha na seção do que trava nomeando o `CONTEXT.md` v6 e os dois ADRs
mais novos que ele.

Decidir se os comandos passam a responder sem prefixo. Hoje são `bks-sdd-kit:save` e afins, porque
o frontmatter não traz `name:`. Acrescentá-lo aos onze devolveria `/save` puro — muda o contrato de
nome de todos, e não foi decidido.

Decidir o que fazer com a citação a `agents/INSTALL-AGENTS.md` e `agents/USE-AGENTS-STEPBYSTEP.md`
no `bks-sdd`: pipeline Node.js externo que nunca foi versionado aqui. Está marcado como exceção
conhecida na suíte, o que é dívida, não solução.

Segue valendo, e não espera crédito: exercitar a `bks-go-solutions` numa geração real. Ela nunca
gerou projeto; a entrevista, o registro na base de aprendizado e a anonimização são caminhos
escritos e não percorridos. Um worker ou CLI pequeno basta.

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

`python tests/test_structure.py` → 722 verificações, 0 falhas.

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
| 12 | O canônico é realimentado pela spec; o `/save` acusa, o `/canonize` corrige | `docs/ARCHITECTURE.md` |
| 13 | Comando do método existe só no plugin; a instalação global morreu | `docs/ARCHITECTURE.md` |
| 14 | Ponteiro para arquivo do kit é verificado pela suíte, acento incluído | `docs/ARCHITECTURE.md` |

---

## Aberto

- O frontmatter dos renderers usa a chave `padrão`, com acento, contra a regra de que chave de
  frontmatter segue ASCII. A suíte aceita as duas grafias; a decisão de padronizar a chave e migrar
  os cinco arquivos está em aberto
- Nenhum caso de eval cobre Go; os 18 existentes são de .NET, TypeScript e comandos
- A base de aprendizado em `${BKS_KNOWLEDGE}/wiki/go/` está criada e vazia, e não é versionada:
  `knowledge/**` está no `.gitignore` do vault, logo ela existe só nesta máquina
- Ícones genéricos de infraestrutura declarados em `skills/bks-arch/icons/` mas não desenhados
- `bks-sdd` com 2062 linhas num `SKILL.md` único — o adelgaçamento está planejado, não iniciado
- O repositório não tem `brain/domain/` nem `brain/engineering/`; o conhecimento está todo em
  `docs/ARCHITECTURE.md` e nas próprias skills
- O `/save` de `0.3.0` foi exercitado só no caminho do silêncio; o do alerta segue sem prova
- `skills/bks-sdd/SKILL.md` cita dois arquivos de um pipeline Node.js que não existe no repositório,
  marcados como exceção conhecida em `tests/test_structure.py`
- A regra nova não tem guarda executável, e o kit exige que tenha. A guarda cairia no projeto
  consumidor, não aqui — é o primeiro caso em que a regra vale para fora e o teste não tem onde
  morar deste lado
- A detecção usa `mtime`, então spec mexida só na formatação acusa divergência. Escolha consciente,
  registrada no `ARCHITECTURE.md`: o falso positivo custa uma reconsolidação, o falso negativo
  custa um canônico errado alimentando o `/prd`
- Quinze commits sem push na `main`
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
