# Project Conventions Template

Copy this file to `.claude/rules/project-conventions.md` in a consuming repository and fill every
placeholder.

## Project Bindings

| Role term | Project value |
|---|---|
| Project name | `<FILL_IN>` |
| Product/domain summary | `<FILL_IN>` |
| Primary language/framework | `<FILL_IN>` |
| Backend stack skills | `<FILL_IN: e.g. python-fastapi, java-springboot, or none>` |
| Backend test skills | `<FILL_IN: e.g. pytest, junit, or none>` |
| Frontend stack skills | `<FILL_IN: e.g. react-ui, or none>` |
| Database/change-data skills | `<FILL_IN: e.g. postgres-migrations, or none>` |
| Application source root | `<FILL_IN>` |
| Test root | `<FILL_IN>` |
| PRD directory | `<FILL_IN>` |
| Feature architecture directory | `<FILL_IN>` |
| Documentation root | `<FILL_IN>` |
| Verification evidence location | `<FILL_IN>` |
| Global verification commands | `<FILL_IN>` |
| Feature-specific verification source | `<FILL_IN>` |
| Local runtime command | `<FILL_IN or none>` |
| Deployment target | `<FILL_IN or none>` |

## Source Layout

Describe module boundaries, package structure, important generated files, and files agents must not
edit.

## Coding Conventions

Describe language, framework, API, persistence, UI, configuration, logging, and security rules.

## Stack Skill Selection

Declare which reusable skills apply to this repository. Generic feature roles can expose multiple
skills, but they should apply only the skills listed in the Project Bindings table and confirmed by
the files or artifacts being changed.

- Use `python-fastapi` for Python/FastAPI backend code.
- Use `pytest` for Python tests.
- Use `java-springboot` for Java/Spring Boot backend code.
- Use `junit` for Java JUnit tests.
- Use `react-ui` for React frontend code.
- Use `postgres-migrations` for PostgreSQL schema or data migrations.

## Verification Commands

List exact commands for linting, typechecking, tests, builds, contract checks, local smoke checks,
and any required artifact validation.

## Feature Artifact Conventions

Define PRD filenames, architecture filenames, and where feature-specific verification evidence
belongs.

## Hard Rules

List project constraints that must never be inferred or bypassed.
