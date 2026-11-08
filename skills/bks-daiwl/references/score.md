# Personal Maintainability Score (PMS) — formula 1.0

The PMS answers: *out of 100 "decision units" the AI made in this code, how many does this person
understand and endorse?* Range 0–100. In Portuguese reports it is labelled SMP (Score de Manutenibilidade Pessoal).

## Impact weight per fundamental (1–5)

| Weight | When | Examples |
|---|---|---|
| 5 | Structural: shapes the system | Hexagonal Architecture, CQRS, Event Sourcing, Saga |
| 4 | Cross-cutting pattern in many files | Repository, Unit of Work, Mediator, Result Pattern |
| 3 | Recurring local pattern | Strategy, Factory, Decorator, Retry with backoff |
| 2 | Point technique/idiom | Guard clauses, simple Value Object, immutable records |
| 1 | Convention/style | naming, folder layout |

Occurrences are dampened: `impact = weight × (1 + ln(occurrences))`. One Saga outweighs 30 guard clauses.

## Factors per class

| Class | Factor | Meaning |
|---|---|---|
| aligned / masters | 1.00 | |
| aligned / knows | 0.80 | knows it, has not practiced |
| aligned / declared | 0.70 | said so, no evidence in the sources |
| aligned / learned (confidence high) | 0.85 | |
| aligned / learned (confidence low) | 0.60 | |
| aligned / experience grounded or contextual | 1.00 | |
| aligned / experience preference | 0.50 | |
| gap | 0.00 | valid fundamental the user does not have yet |
| divergent | −0.50 | AI contradicted an anti-preference or adopted experience |
| unfounded | −0.25 | AI improvisation with no recognized basis |

```
PMS = max(0, Σ(impact × factor) / Σ(impact)) × 100
```

Bands: **≥80** maintains comfortably · **60–79** maintains while studying the gaps ·
**40–59** risk: will depend on the AI to maintain · **<40** code is foreign to its owner.

Always show raw numbers: total impact, impact per class, the 3 largest negative contributions.

## `findings.json` schema

```json
{
  "project": "payments-api",
  "date": "2026-11-07",
  "analyzed_path": "src/",
  "source_tool": "Claude Code",
  "language": "pt-BR",
  "fundamentals": [
    {
      "name": "Outbox Pattern",
      "category": "Integration/Messaging",
      "weight": 4,
      "class": "gap",
      "level": null,
      "confidence": null,
      "experience_type": null,
      "grounded": true,
      "source": "Chris Richardson, Microservices Patterns, ch. 3",
      "explanation": "Writes the event in the same transaction as the data and publishes later, avoiding dual-write.",
      "why_ai_used": "A DB write followed by a queue publish in the same use case.",
      "study": ["Read the pattern on microservices.io", "Book ch. 3", "Implement with outbox table + worker"],
      "occurrences": [{"file": "src/Infra/OutboxWriter.cs", "line": 12, "snippet": "..."}]
    }
  ]
}
```

`class`: aligned | gap | divergent | unfounded. `level` (aligned only): masters | knows | declared | learned | experience.
`confidence`: high | low. `experience_type`: grounded | contextual | preference.
Text fields (`explanation`, `why_ai_used`, `study`) are written in the user's language.
The script also accepts the 0.x Portuguese schema (`fundamentos`, `classe`, `lacuna`…) and normalizes it.
