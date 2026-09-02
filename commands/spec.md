---
description: Fluxo bks-sdd de especificacao: entrevista sobre o bounded context e gera FEAT-[nome].md e, apos aprovacao, TEST-[nome].md.
---

Fluxo bks-sdd: entreviste-me sobre o bounded context, objetivos,
entidades, operações, integrações (TCP? filas? SEDA?) e critérios
de aceite VERIFICÁVEIS. Rode este comando com o Claude Code aberto
na RAIZ DO REPO do projeto (não no _bks-ai). Gere FEAT-[nome].md em
specs/features/ usando o template ${BKS_BRAIN}/templates/FEAT.md.
Depois de aprovado, gere TEST-[nome].md em specs/tests/. NUNCA
implemente nesta etapa.
