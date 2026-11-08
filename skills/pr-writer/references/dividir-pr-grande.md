# Dividir PR grande — quando e como propor

A atenção do revisor cai rápido com o tamanho do diff. Acima de umas 400 linhas, a revisão vira
leitura superficial, e o defeito passa. Dividir é proteger a revisão, não burocracia.

## Quando sugerir

Conte as linhas alteradas fora de arquivo gerado, lockfile, snapshot e migration gerada por
ferramenta:

```
git diff --stat origin/<base>...HEAD -- . ':!*.lock' ':!package-lock.json' ':!**/Migrations/*.Designer.cs'
```

Sugira a divisão quando qualquer uma vale:

| Sinal | Por quê |
|---|---|
| mais de 400 linhas alteradas | revisão perde profundidade |
| refatoração e mudança de comportamento juntas | o revisor não distingue regressão de intenção |
| mais de um assunto: feature e correção sem relação | um não deveria esperar o outro para entrar |
| renomeação em massa com regra nova no meio | o ruído esconde a regra |
| dependência nova ou atualização de framework junto com feature | rollback de um leva o outro |

## Como cortar

Corte por dependência, de baixo para cima. Cada PR compila, passa nos testes e pode entrar sozinho.

1. **Preparação** — refatoração sem mudança de comportamento, extração de porta, renomeação.
2. **Infraestrutura** — migration, configuração, contrato novo que ainda ninguém usa.
3. **Comportamento** — a regra nova, usando o que os anteriores prepararam.
4. **Limpeza** — remoção do caminho antigo, depois que o novo está em produção.

Feature que não pode aparecer pela metade entra atrás de uma flag desligada. O PR 3 liga a flag,
ou um PR próprio liga.

## A forma da proposta

Apresente antes de escrever qualquer descrição:

```markdown
O diff tem 1.140 linhas em 23 arquivos e mistura três assuntos. Proponho:

| PR | Conteúdo | Linhas | Depende de |
|---|---|---|---|
| 1 | refactor: extrai IDiscountRepository e move SQL para o adapter | 310 | — |
| 2 | feat(db): coluna rounding_mode em order_discount | 90 | — |
| 3 | fix(checkout): arredonda desconto para duas casas | 260 | 1, 2 |
| 4 | chore: atualiza Npgsql | 480, quase tudo lockfile | — |

Os PRs 1, 2 e 4 entram em qualquer ordem. Quer que eu monte as branches,
ou prefere manter num PR só?
```

Montar as branches mexe no histórico do usuário: faça só com o pedido explícito, e com a branch
original preservada.

## Se o usuário quiser manter num PR só

A decisão é dele. A descrição compensa o tamanho:

- **Roteiro de leitura** logo depois do resumo: "Leia por commit. 1–3 são refatoração sem
  mudança de comportamento; 4 é a migration; 5–6 são a regra nova."
- Commits organizados por assunto, se ainda dá para reorganizar sem reescrever histórico
  publicado.
- Na seção de risco, o que torna o rollback mais difícil por estar tudo junto.

## O que não é motivo para dividir

- Teste junto com o código que ele testa. Fica no mesmo PR.
- Documentação da mudança. `README.md` e `ARCHITECTURE.md` atualizados entram no mesmo PR que
  muda o tipo público.
- Migration e o código que a usa, quando a migration não serve para mais nada. Separar só cria
  um PR que não se revisa sozinho.
