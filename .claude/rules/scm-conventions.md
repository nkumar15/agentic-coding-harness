# SCM Conventions

Provider-neutral conventions for branches, commits, and change requests.

What is not here:

- Lifecycle phase order and gates live in `.claude/process/<type>.yaml`.
- Tracker and PR commands live in `.claude/process/provider.<provider>.yaml`.
- Project-specific work-unit names, release rules, and verification commands live in
  `.claude/rules/project-conventions.md` or `.claude/rules/migration-conventions.md`.

## Core Principles

- All work traces to a work item. With `github` provider this is a GitHub issue. With `local`
  provider this is a manually identified work item in the session.
- Check for duplicate in-progress work before branching.
- One phase owns one branch and one change request.
- Human approval gates are hard stops. Agents do not self-merge.
- Push only when project conventions and the active process allow it.
- Never force-push a protected branch. Force-pushing any shared branch requires explicit human
  instruction.

## Process Types

| Type | Spec | Shape |
|---|---|---|
| `feature` | `.claude/process/feature.yaml` | PRD -> architecture -> development |
| `bug` | `.claude/process/bug.yaml` | reproduce -> fix -> test |
| `chore` | `.claude/process/chore.yaml` | describe -> implement |
| `docs` | `.claude/process/docs.yaml` | write -> review |
| `migration` | `.claude/process/migration.yaml` | analyze -> design -> migrate -> unit test -> integration test -> deploy and manual test |

## Branch Naming

The exact branch pattern is defined by each process phase's `branch:` field. Current generic
prefixes include:

- `docs/`
- `feature/arch-`
- `feature/dev-`
- `bugfix/`
- `chore/`
- `migrate/arch-`
- `migrate/dev-`
- `migrate/unit-`
- `migrate/integration-`
- `migrate/deploy-`

## Change Requests

- Use one change request per phase.
- Use the phase's `link:` value to choose the provider adapter's intermediate or final link syntax.
- Record verification evidence in the project-defined location before requesting human review.

## Commit Messages

Use clear conventional-style commits unless the consuming repository defines a stricter format:

```text
<type>: <short description>

<optional body>

Part of #<work-item>
Co-Authored-By: ...
```

Common types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`.
