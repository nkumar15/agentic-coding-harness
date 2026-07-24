# Portable Agent Workflow

`.agents/` is the canonical source for portable agent orchestration. It is designed to be copied
into application repositories and then bound to project facts through convention files.

## Ownership

| Directory | Purpose |
|---|---|
| `rules/` | Durable repo conventions. Only `project-conventions.md` and `migration-conventions.md` should contain project facts. |
| `process/` | Workflow phases, gates, provider selection, and provider operation mappings. |
| `roles/` | Host-neutral agent responsibilities and output contracts. |
| `skills/` | Reusable techniques and templates. |
| `adapters/` | Host-specific metadata for Claude Code and Codex. |

Humans edit `.agents/` first. Generated host output under `.claude/` and `.codex/agents/` is
committed so a fresh clone works immediately.

## Supported Process Specs

- `feature.yaml`: PRD -> architecture -> development.
- `bug.yaml`: reproduce -> fix -> test.
- `chore.yaml`: describe -> implement.
- `docs.yaml`: write -> review.
- `migration.yaml`: analyze -> design -> migrate -> unit test -> integration test -> deploy and manual test.

## Generic Versus Project-Specific

Keep roles, skills, process mechanics, and adapters generic. Project-specific values belong in:

- `rules/project-conventions.md`
- `rules/migration-conventions.md`

When adopting this package in another repo, start from the matching `*-template.md` files and then
regenerate adapters.
