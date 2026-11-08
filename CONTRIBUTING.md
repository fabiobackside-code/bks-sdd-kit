# Como contribuir

Issues e pull requests são bem-vindos, em português ou inglês. *Issues and pull requests are welcome,
in Portuguese or English.*

## Antes de abrir um PR

1. Abra uma issue descrevendo o problema ou a proposta. Mudança de comportamento de skill precisa de
   acordo antes do código, porque muda a decisão do agente em todo projeto que consome o kit.
2. Faça fork e crie uma branch a partir da `main`.
3. Rode a suíte estrutural, que é rápida e não custa crédito:
   ```
   python tests/test_structure.py
   bash hooks/tests/run.sh
   ```
4. Se mudou o comportamento de uma skill, rode o caso de eval correspondente e cole o **delta**
   entre os braços `with` e `without` no PR:
   ```
   claude plugin eval . --case <caso> --runs 1
   ```

## Regras do kit

As mesmas que o kit impõe aos projetos que o consomem:

- Todo hook tem teste em `hooks/tests/`. Guarda sem teste é intenção.
- Decisão, trade-off e histórico vão para `docs/ARCHITECTURE.md`, nunca para comentário de código.
- Até cinco linhas por bloco de comentário, sem marca de severidade.
- Caminhos usam `${CLAUDE_PLUGIN_ROOT}`, `${BKS_VAULT}` e `${BKS_KNOWLEDGE}`, nunca caminho absoluto.
- Documentação em português do Brasil, com acentuação. Código e identificadores em inglês.
- Conteúdo de terceiros entra só com licença compatível e linha nova em `THIRD_PARTY.md`.

## Onde cada coisa está

Ver a tabela "Onde cada coisa está" no `CLAUDE.md` e as decisões estruturais em
`docs/ARCHITECTURE.md`.
