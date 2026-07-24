# Python/FastAPI Onboarding Example

This guide shows the minimum concrete work needed to onboard a Python/FastAPI repository today.
Use it as an example, then replace paths and commands with the target repository's real values.

## Outcome

After onboarding, the workflow package should know:

- the repository uses `python-fastapi` for backend work
- the repository uses `pytest` for Python tests
- where application code, tests, PRDs, architecture, docs, and evidence live
- which commands prove a change is safe
- which workflows are available for feature, bug, chore, and docs work

## Step 1: Copy The Workflow Package

Copy the package into the target repository, including:

- `.agents/`
- `.claude/`
- `.codex/agents/`
- `AGENTS.md`
- `CLAUDE.md`
- `scripts/`
- `docs/agentic-workflow/`
- `.github/workflows/agent-portability.yml`, if the repository uses GitHub Actions

Keep `.agents/` as the source of truth. Regenerate `.claude/` and `.codex/agents/` after changes.

## Step 2: Fill Project Conventions

Copy `.agents/rules/project-conventions-template.md` to
`.agents/rules/project-conventions.md` and replace placeholders with real project values.

Example for a Python/FastAPI API:

```md
# Project Conventions

## Project Bindings

| Role term | Project value |
|---|---|
| Project name | ticket-system |
| Product/domain summary | Internal ticket system API for ticket lookup, ticket status, and assignment workflows. |
| Primary language/framework | Python 3.11 / FastAPI |
| Backend stack skills | python-fastapi |
| Backend test skills | pytest |
| Frontend stack skills | none |
| Database/change-data skills | postgres-migrations if PostgreSQL schema changes are in scope; otherwise none |
| Rule-engine skills | none |
| Application source root | src/ticket_system |
| Test root | tests |
| PRD directory | docs/application/prd |
| Feature architecture directory | docs/application/architecture/features |
| Documentation root | docs |
| Verification evidence location | PR body and docs/application/verification |
| Global verification commands | python -m ruff check src tests; python -m mypy src; python -m pytest |
| Feature-specific verification source | PRD and architecture Verification sections |
| Local runtime command | uvicorn ticket_system.main:app --reload |
| Deployment target | none for initial local onboarding |
```

Use only commands that actually exist in the target repository. If the project does not use Ruff or
Mypy, do not list those commands.

## Step 3: Make Source Layout Explicit

Agents need enough layout detail to avoid guessing where code belongs.

Example:

```md
## Source Layout

- `src/ticket_system/main.py` creates the FastAPI app.
- `src/ticket_system/api/routes/` contains HTTP routers.
- `src/ticket_system/schemas/` contains Pydantic request and response models.
- `src/ticket_system/services/` contains business orchestration.
- `src/ticket_system/repositories/` contains persistence or downstream data access.
- `src/ticket_system/config.py` owns runtime configuration.
- `tests/unit/` contains fast unit tests.
- `tests/integration/` contains tests requiring app wiring or external service fakes.
- No generated source files currently; if generated files are added later, document their path here
  before agents edit nearby code.
```

## Step 4: Make Coding Conventions Explicit

Write the rules the agent must follow for this Python project.

Example:

```md
## Coding Conventions

- Keep FastAPI route handlers thin; put business logic in services.
- Use Pydantic models for request and response schemas.
- Do not return raw persistence models from API routes.
- Use dependency injection for services, repositories, settings, and clients.
- Keep configuration in environment-backed settings; do not hardcode secrets or service URLs.
- Use structured errors matching the existing API error shape.
- Add or update pytest coverage with every behavior change.
- Preserve existing package naming, import style, logging style, and async/sync conventions.
```

The exact conventions should match the repository. Do not copy the example if the codebase uses a
different layout or framework style.

## Step 5: Replace Gate Command Placeholders

The reusable package ships with placeholder gates such as:

```yaml
checks_green:
  checks:
    - <project-conventions:verification.global_checks>
```

Replace them in `.agents/process/gates.yaml` with real commands from project conventions.

Example:

```yaml
checks_green:
  description: Global project verification passes: lint, typecheck, tests, builds, and other required repository checks.
  agent: verifier
  on_fail: full-stack-developer
  checks:
    - python -m ruff check src tests
    - python -m mypy src
    - python -m pytest
```

If the project has a single Make target, use that instead:

```yaml
checks_green:
  description: Global project verification passes.
  agent: verifier
  on_fail: full-stack-developer
  checks:
    - make verify
```

The key requirement is that `checks_green.checks` contains commands the verifier can run directly.

## Step 6: Select Provider Mode

For first onboarding, use local mode:

```yaml
provider: local
```

in `.agents/process/config.yaml`.

Local mode does not create GitHub issues or pull requests. Human approval gates become explicit
approval prompts in the session.

Switch to GitHub mode when the repository is ready for `gh` CLI backed Issues and Pull Requests:

```yaml
provider: github
```

## Step 7: Regenerate And Validate

Run:

```bash
python3 scripts/generate-agent-adapters.py
python3 scripts/validate-agent-portability.py
```

Commit the canonical and generated files after validation passes.

## Step 8: Start Workflows

Use the workflow process files as the operating contract.

### Feature

Use `.agents/process/feature.yaml` when the work needs requirements and architecture before code.

Example request:

```text
Use the feature workflow for "add ticket status search". Start with the PRD phase.
```

The expected path is:

1. `prd-writer` writes the PRD.
2. Human approves and merges the PRD artifact.
3. `architect` writes the feature architecture.
4. Human approves and merges the architecture artifact.
5. `full-stack-developer` implements the feature.
6. `verifier` runs `checks_green` and `feature_verification`.
7. `code-reviewer` runs `review_approved`.
8. Human approves and merges the final change.

For this Python repository, feature agents should use `python-fastapi` and `pytest` when backend
code or Python tests are in scope. They should not use Java, JUnit, React, or PostgreSQL
skills unless project conventions explicitly select those skills and the files being changed match.

### Bug

Use `.agents/process/bug.yaml` when fixing existing behavior.

Example request:

```text
Use the bug workflow to fix the incorrect 404 response for ticket lookup.
```

The developer should reproduce or characterize the defect, add a regression test when feasible,
fix the behavior, run checks, and route through review.

### Chore

Use `.agents/process/chore.yaml` for scoped maintenance.

Example request:

```text
Use the chore workflow to update the pytest configuration and keep behavior unchanged.
```

The change should stay inside the stated maintenance scope and still pass checks and review.

### Docs

Use `.agents/process/docs.yaml` for documentation-only changes.

Example request:

```text
Use the docs workflow to update the local development setup guide.
```

If the documentation change requires source or behavior changes, use feature, bug, or chore instead.

## What To Check Before Calling It Onboarded

- `.agents/rules/project-conventions.md` has no unfilled placeholders.
- Stack skills say `python-fastapi` and `pytest` for a Python/FastAPI project.
- `checks_green` has runnable commands, not placeholders.
- PRD, architecture, docs, and evidence paths exist or are intentionally created by workflow usage.
- `python3 scripts/validate-agent-portability.py` passes.
- Codex and Claude Code can discover the generated agents after restart if needed.

## Where To Find All Supported Use Cases

Use the workflow-specific docs for detailed operating instructions:

- [Feature workflow](../feature/README.md)
- [Bug workflow](../bug/README.md)
- [Chore workflow](../chore/README.md)
- [Docs workflow](../docs/README.md)
- [Migration workflow](../migration/README.md)
