# Fundamentals Catalog

Used to (1) normalize names and aliases (English and Portuguese), (2) decide whether something is grounded,
(3) point to study material. Source rule: **primary first** (original author, RFC, official docs), then
teaching material. This is a seed — users extend it; concepts outside it are not invalid, they just need a cited source.

## Architecture

| Fundamental | Aliases (EN / PT) | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| Hexagonal Architecture | Ports & Adapters / Arquitetura Hexagonal | 5 | Alistair Cockburn, "Hexagonal Architecture" (2005) | Cockburn & Garrido, *Hexagonal Architecture Explained* |
| Clean Architecture | Onion (partly) / Arquitetura Limpa | 5 | Robert C. Martin, *Clean Architecture* | Jeffrey Palermo, Onion Architecture articles |
| CQRS | Command Query Responsibility Segregation | 5 | Greg Young, "CQRS Documents" | Martin Fowler, bliki CQRS |
| Event Sourcing | | 5 | Greg Young; Fowler bliki | Young, *Versioning in an Event Sourced System* |
| Microservices | Microsserviços | 5 | Lewis & Fowler, "Microservices" (2014) | Sam Newman, *Building Microservices* |
| Modular Monolith | Monólito Modular | 5 | Simon Brown, "Modular monoliths" | Kamil Grzybek, modular monolith series |
| Vertical Slice | Fatia Vertical | 4 | Jimmy Bogard, "Vertical Slice Architecture" | |

## DDD

| Fundamental | Aliases | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| Bounded Context | Contexto Delimitado | 5 | Eric Evans, *Domain-Driven Design* | Vaughn Vernon, *Implementing DDD* |
| Aggregate | Aggregate Root / Agregado | 4 | Evans | Vernon, "Effective Aggregate Design" (3 parts) |
| Value Object | Objeto de Valor | 2 | Evans | Fowler bliki ValueObject |
| Domain Event | Evento de Domínio | 4 | Evans; Fowler | Vernon, IDDD ch. 8 |
| Anti-Corruption Layer | ACL / Camada Anticorrupção | 4 | Evans | Microsoft Architecture Center |
| Ubiquitous Language | Linguagem Ubíqua | 3 | Evans | |

## Design and enterprise patterns

| Fundamental | Aliases | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| Repository | Repositório | 4 | Fowler, *PoEAA* | Evans ch. 6 |
| Unit of Work | Unidade de Trabalho | 4 | Fowler, *PoEAA* | |
| Mediator | MediatR / Mediador | 4 | GoF, *Design Patterns* | refactoring.guru |
| Strategy, Factory, Decorator, Adapter, Observer… | | 3 | GoF | refactoring.guru |
| Specification | Especificação | 3 | Evans & Fowler, "Specifications" | |
| Result Pattern | Either, Railway-Oriented | 4 | Scott Wlaschin, "Railway Oriented Programming" | |
| Pipeline / Chain of Responsibility | Cadeia de Responsabilidade | 4 | GoF | |
| Dependency Injection | IoC / Injeção de Dependência | 3 | Fowler, "Inversion of Control Containers..." | Mark Seemann, *Dependency Injection Principles...* |

## Principles

| Fundamental | Aliases | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| SOLID (each letter separately) | SRP, OCP, LSP, ISP, DIP | 3 | Robert C. Martin, *Agile Software Development* | Liskov & Wing (1994) for LSP |
| Object Calisthenics | | 2 | Jeff Bay, *The ThoughtWorks Anthology* | |
| Law of Demeter | Lei de Demeter | 2 | Lieberherr & Holland (1989) | |
| Composition over inheritance | Composição sobre herança | 3 | GoF ch. 1 | |
| Tell, Don't Ask | | 2 | Pragmatic Programmers; Fowler bliki | |
| Fail Fast / Guard Clauses | Cláusulas de guarda | 2 | Jim Shore, "Fail Fast" (IEEE Software) | |
| YAGNI, KISS, DRY | | 1 | *The Pragmatic Programmer* (DRY); XP (YAGNI) | |

## Integration, resilience, distributed data

| Fundamental | Aliases | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| Outbox | Transactional Outbox | 4 | Chris Richardson, microservices.io | *Microservices Patterns* ch. 3 |
| Saga | Orchestrated / Choreographed — Orquestrada / Coreografada | 5 | Garcia-Molina & Salem, "Sagas" (1987) | Richardson ch. 4 |
| Idempotency | Idempotency Key / Idempotência | 4 | RFC 9110 (idempotent methods) | Stripe engineering blog |
| Retry + exponential backoff | Retentativa com backoff | 3 | AWS Architecture Blog, "Exponential Backoff and Jitter" | Polly docs |
| Circuit Breaker | | 3 | Michael Nygard, *Release It!* | Fowler bliki |
| Bulkhead, Timeout | | 3 | Nygard, *Release It!* | |
| Inbox / Deduplication | Deduplicação | 3 | Richardson | |
| Enterprise Integration Patterns | EIP | 3–4 | Hohpe & Woolf, *EIP* | enterpriseintegrationpatterns.com |

## Testing and quality

| Fundamental | Aliases | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| TDD | | 3 | Kent Beck, *TDD by Example* | |
| Test Doubles | Mock, Stub, Fake / Dublês de teste | 2 | Gerard Meszaros, *xUnit Test Patterns* | Fowler, "Mocks Aren't Stubs" |
| Test pyramid | Pirâmide de testes | 2 | Mike Cohn | Fowler, "The Practical Test Pyramid" |
| Code smells / Refactoring | Refatoração | 2 | Fowler, *Refactoring* 2nd ed. | |

## Observability and operations

| Fundamental | Aliases | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| Distributed tracing | OpenTelemetry / Rastreamento distribuído | 3 | OpenTelemetry specification | Sigelman et al., "Dapper" (Google, 2010) |
| Structured logging | Log estruturado | 2 | OpenTelemetry Logs spec | |
| Health checks | | 2 | Kubernetes docs (probes) | |
| 12-Factor App | | 3 | 12factor.net | |

## Security

| Fundamental | Aliases | Weight | Primary source | Go deeper |
|---|---|---|---|---|
| OWASP Top 10 / ASVS | | 3 | owasp.org | |
| Secrets in a vault | Vault, CyberArk / Gestão de segredos | 3 | Official docs of the vault in use | OWASP Secrets Management Cheat Sheet |
| OAuth 2.0 / OIDC | | 4 | RFC 6749, OpenID Connect Core | RFC 9700 (OAuth Security BCP) |
