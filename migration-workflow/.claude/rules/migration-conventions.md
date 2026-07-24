# Migration Conventions

Reusable package defaults for legacy-to-target migration work. In a consuming repository, replace
this file with project-specific values from `migration-conventions-template.md`.

## Project Bindings

| Role term | Project value |
|---|---|
| Migration unit | `<FILL_IN: domain, service, module, endpoint group, etc.>` |
| Legacy source root | `<FILL_IN>` |
| Target source root | `<FILL_IN>` |
| Target API or interface contract | `<FILL_IN>` |
| Target architecture artifact path | `<FILL_IN>` |
| Characterization artifact path | `<FILL_IN>` |
| Progress artifact path | `<FILL_IN>` |
| Implementation verification report path | `<FILL_IN>` |
| Rule source paths | `<FILL_IN or none>` |
| Rule fixture path pattern | `<FILL_IN or none>` |
| Rule fixture generator | `<FILL_IN or none>` |
| Data access boundary | `<FILL_IN or none>` |
| Local runtime command | `<FILL_IN or none>` |
| Local health endpoint | `<FILL_IN or none>` |
| Remote parity base URL env var | `<FILL_IN or none>` |
| Deployment environment | `<FILL_IN or none>` |

## Source Of Truth

- Legacy behavior must be characterized from the authoritative legacy sources listed here.
- Target contracts listed here win when legacy behavior and contract shape disagree.
- Existing target implementation is implementation evidence only, not legacy truth.
- Project-specific exclusions, stale sources, parser choices, and fixture rules belong here.

## Verification Commands

Replace placeholder gate commands in `.claude/process/gates.yaml` with project-backed commands or
document how each placeholder resolves from this file.

| Gate | Project command source |
|---|---|
| `domain_migration_checks_green` | `<FILL_IN>` |
| `contract_verified` | `<FILL_IN>` |
| `rules_parity_verified` | `<FILL_IN or none>` |
| `cross_domain_regression_green` | `<FILL_IN>` |
| `springboot_app_health_checked` | `<FILL_IN or none>` |
| `api_parity_verified` | `<FILL_IN or none>` |

## Hard Rules

- Do not start design until legacy code analysis is approved.
- Do not start migration implementation until design is approved.
- Do not bypass parity, contract, health, regression, review, deploy, manual test, or human merge
  gates.
- Do not hardcode paths, commands, env vars, domain lists, or deployment names in roles or skills.
