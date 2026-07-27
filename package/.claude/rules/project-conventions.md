# Project Conventions

Reusable package defaults for projects adopting this workflow. In a consuming repository, replace
this file with project-specific values from `project-conventions-template.md`.

## Project Bindings

| Role term | Project value |
|---|---|
| Project name | `<FILL_IN: project name>` |
| Primary language/framework | `<FILL_IN: stack>` |
| Backend stack skills | `<FILL_IN: e.g. python-fastapi, java-springboot, or none>` |
| Backend test skills | `<FILL_IN: e.g. pytest, junit, or none>` |
| Frontend stack skills | `<FILL_IN: e.g. react-ui, or none>` |
| Database/change-data skills | `<FILL_IN: e.g. postgres-migrations, or none>` |
| Application source root | `<FILL_IN: source root>` |
| Test root | `<FILL_IN: test root>` |
| PRD directory | `<FILL_IN: e.g. docs/application/prd>` |
| Feature architecture directory | `<FILL_IN: e.g. docs/application/architecture/features>` |
| Verification evidence location | `<FILL_IN: e.g. PR body, docs, .analysis>` |
| Global verification commands | `<FILL_IN: lint/typecheck/test/build commands>` |
| Feature-specific verification source | `<FILL_IN: where feature verification commands are declared>` |
| Local runtime command | `<FILL_IN: command or none>` |

## Application Conventions

- Document source layout, module boundaries, dependency direction, API conventions, database or
  persistence rules, frontend conventions, runtime configuration, and security constraints here.
- The stack skill rows above are the source of truth for generic feature agents. Agents should
  apply only the skills that match these rows and the files or artifacts being changed.
- If a role needs a path, command, environment variable, service name, or verification requirement,
  add it here and have the role refer to this file.
- Do not duplicate mutable project facts in role files, skills, `AGENTS.md`, `CLAUDE.md`, or
  generated host adapter files.

## Verification

The `checks_green` gate in `.claude/process/gates.yaml` should run the global verification commands
listed here. The `feature_verification` gate should verify the feature-specific plan declared in the
PRD and architecture artifacts.

Replace placeholder gate commands in `.claude/process/gates.yaml` when adopting this package.
