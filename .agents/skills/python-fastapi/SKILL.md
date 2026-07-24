---
name: python-fastapi
description: Implement Python/FastAPI backend code: endpoints, Pydantic schemas, service layer, persistence integration, background tasks, configuration, errors, and logging. Use when a consuming repository's project conventions declare a Python/FastAPI backend.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "2.0"
---

# Python / FastAPI Backend Skill

Use this skill only when `.agents/rules/project-conventions.md` says the project uses a
Python/FastAPI backend. Project conventions are the source of truth for Python version, package
layout, database stack, auth model, command names, and runtime behavior.

## FastAPI Endpoints

- Endpoint functions should validate input, call application services, and return typed response
  models.
- Use dependency injection for request-scoped resources such as DB sessions, auth context, settings,
  and clients.
- Return explicit response models; do not leak ORM objects or raw internal data structures.
- Preserve project-defined status codes, error shape, route prefixes, header names, and auth
  requirements.

## Pydantic Schemas

- Keep API boundary schemas separate from persistence models.
- Prefer explicit create/update/response schemas when the project does not define a different
  pattern.
- Validate at the boundary; services should receive already-validated inputs or domain objects.
- Use the Pydantic version and config style declared by project conventions.

## Services

- Put business logic in services, not endpoint functions.
- Services should receive dependencies from callers instead of constructing global clients or DB
  sessions internally.
- Keep atomic write boundaries explicit and consistent with project conventions.
- Raise domain exceptions or result types that the API layer maps consistently.

## Persistence

- Follow the repository's persistence pattern from project conventions: SQLAlchemy, SQLModel, raw
  SQL, repository classes, external data service, or another declared approach.
- If the project uses PostgreSQL migrations, read the `postgres-migrations` skill before changing
  schema.
- Do not add manual tenant filters, soft-delete filters, or audit behavior unless the project
  conventions require that pattern.

## Background Tasks

- Use the task framework declared in project conventions, if any.
- Pass serializable identifiers and context, not ORM objects.
- Make retryable tasks idempotent.
- Preserve tenant/request/correlation context when project conventions require it.

## Configuration

- Load runtime configuration through the project's declared settings mechanism.
- Never hardcode hosts, credentials, secrets, or environment-specific URLs.
- Update sample env files, deployment values, or secret placeholders only when project conventions
  say those files are part of the repo contract.

## Errors And Logging

- Map service errors to the project-defined API error shape.
- Log useful operational boundaries: external calls, retries, fallbacks, side effects, and failures.
- Do not log secrets, tokens, full payloads, or sensitive personal/health data.
- Avoid duplicate exception logs and entry/exit noise.

## Tests

- Add focused unit and integration tests with the implementation.
- Use the `pytest` skill when the project uses pytest.
- Run commands from `.agents/process/gates.yaml` after resolving placeholders from project
  conventions.
