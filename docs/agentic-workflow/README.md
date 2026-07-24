# Agentic Workflow Documentation

This directory contains the detailed design and operating notes for each reusable workflow.

Start with the root [README](../../README.md) for adoption steps, repository boundaries, and the
high-level workflow diagrams. Use these workflow pages when adapting, reviewing, or extending a
specific process.

## Workflow Guides

| Workflow | Process file | Guide |
|---|---|---|
| Feature | `.agents/process/feature.yaml` | [Feature workflow](feature/README.md) |
| Bug | `.agents/process/bug.yaml` | [Bug workflow](bug/README.md) |
| Chore | `.agents/process/chore.yaml` | [Chore workflow](chore/README.md) |
| Docs | `.agents/process/docs.yaml` | [Docs workflow](docs/README.md) |
| Migration | `.agents/process/migration.yaml` | [Migration workflow](migration/README.md) |

Each workflow guide documents the full supported use case: diagram, roles, models, skills, phase
details, gates, failure routing, required convention detail, design rationale, and done criteria.

## Onboarding Examples

| Stack | Guide | What it shows |
|---|---|---|
| Python/FastAPI | [Python/FastAPI onboarding](onboarding/python-fastapi.md) | Exact convention values, stack-skill selection, runnable gate commands, validation, and how to start supported workflows. |

## Comparisons

| Topic | Guide | What it explains |
|---|---|---|
| BMAD Method | [BMAD comparison](bmad-comparison.md) | How this lightweight repo-native workflow differs from BMAD's broader AI-native agile framework. |

## Gate Command Example

This package ships with placeholder gate commands because a reusable workflow cannot know whether a
consuming repository uses Maven, Gradle, npm, pytest, Make, Docker Compose, or another command set.

For example, the shared gate file starts with a convention-backed placeholder:

```yaml
checks_green:
  description: Global project verification passes: lint, typecheck, tests, builds, and other required repository checks.
  agent: verifier
  on_fail: full-stack-developer
  checks:
    - <project-conventions:verification.global_checks>
```

In the consuming repository, first make the convention file explicit:

```md
## Verification Commands

- Global checks:
  - `npm run lint`
  - `npm test -- --runInBand`
  - `npm run build`
- Feature-specific verification source: PRD and architecture `Verification` sections.
```

Then replace the placeholder in `.agents/process/gates.yaml` with the exact commands the verifier
should run:

```yaml
checks_green:
  description: Global project verification passes: lint, typecheck, tests, builds, and other required repository checks.
  agent: verifier
  on_fail: full-stack-developer
  checks:
    - npm run lint
    - npm test -- --runInBand
    - npm run build
```

The important rule is that `gates.yaml` should contain runnable commands, while the convention files
explain where those commands came from, when to use them, and what evidence they produce.

Migration gates follow the same pattern, backed by `.agents/rules/migration-conventions.md` instead
of `project-conventions.md`:

```yaml
domain_migration_checks_green:
  description: Migration work-unit implementation checks pass using project-defined domain/module scope.
  agent: springboot-migration-verifier
  on_fail: springboot-migrator
  checks:
    - <migration-conventions:verification.domain_checks>
```

## Shared Design Principles

- Processes own phase order, branch shape, artifacts, and gates.
- Roles own responsibility, operating mode, output contract, and routing.
- Skills own reusable technical method.
- Convention files own project-specific facts.
- Generated host files should never become the source of truth.
- Human approval remains explicit at major product, design, review, deploy, and merge boundaries.

## Convention Quality Bar

Agents should not need to guess:

- source roots and generated-file boundaries
- command names and required environment variables
- test scopes and gate commands
- PRD, architecture, evidence, and parity artifact locations
- framework versions and stack-skill selection
- deployment targets and health URLs
- API contracts and compatibility rules
- migration work-unit naming and legacy source paths

If a workflow repeatedly pauses for the same missing fact, add that fact to the relevant convention
file rather than adding it to a one-off prompt.
