---
name: pytest
description: Write and evaluate pytest unit, integration, contract, and smoke tests for Python projects. Use when a consuming repository's project conventions declare pytest.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "2.0"
---

# pytest Testing Skill

Use this skill only when `.claude/rules/project-conventions.md` says the project uses pytest.
Project conventions define test locations, fixture style, async test client, database setup, command
names, and coverage expectations.

## Test Placement

- Mirror the repository's source layout in test paths unless project conventions define another
  scheme.
- Keep unit tests close to the behavior they prove.
- Put boundary or integration tests in the project-defined integration test location.
- Name tests by behavior, not implementation detail.

## Unit Tests

- Test services and pure functions with focused inputs and outputs.
- Mock external systems, network clients, clocks, and nondeterministic dependencies.
- Do not mock the function under test.
- Cover failure paths and edge cases that the PRD, architecture, or bug report identifies.

## Integration Tests

- Use the project-defined real or containerized test resources.
- Keep fixture data deterministic.
- Verify API status codes, response shape, persistence effects, side effects, and authorization
  behavior when applicable.
- Do not depend on demo or production-like seed data unless project conventions explicitly allow it.

## Async Tests

- Use the async test framework and HTTP client declared by project conventions.
- Do not block the event loop with synchronous sleeps or polling.
- Isolate event-loop, DB-session, and app-lifespan fixtures as the project requires.

## Commands

- Run the exact commands declared in `.claude/process/gates.yaml` after resolving placeholders from
  project conventions.
- Run all checks required by the active gate, even if an earlier check fails.
- Report skipped or blocked tests explicitly; a skipped test is not evidence of correctness.
