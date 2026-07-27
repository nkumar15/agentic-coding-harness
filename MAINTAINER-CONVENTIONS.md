# Maintainer Conventions

Filled-in project bindings for maintaining this repository (the Portable Agentic Coding Harness
package source itself). Use this file — not `package/.agents/rules/project-conventions.md` — as the
conventions source when running `package/.agents/skills/orchestrate/SKILL.md` on this repo's own
chore, docs, bug, or feature work.

`package/.agents/rules/project-conventions.md` and
`package/.agents/rules/project-conventions-template.md` must stay generic placeholders: they are the
files every consuming repository copies and fills in for itself. This file exists precisely so this
repo's own facts never leak into that shipped template.

## Project Bindings

| Role term | This repo's value |
|---|---|
| Project name | agentic-coding-harness (Portable Agentic Coding Harness) |
| Primary language/framework | Markdown/YAML workflow package, Python maintenance tooling |
| Backend/frontend/test stack skills | none — this repo has no application code |
| Application source root | `package/.agents/` |
| Test root | none |
| PRD directory | `package/docs/agentic-workflow/prd/` |
| Feature architecture directory | `package/docs/agentic-workflow/architecture/` |
| Verification evidence location | PR body |
| Global verification commands | `python3 package/scripts/generate-agent-adapters.py`, `python3 package/scripts/validate-agent-portability.py` |
| Feature-specific verification source | PRD `Verification Requirements` / architecture `Verification Strategy` sections |
| Local runtime command | none |
| Process provider | github |
