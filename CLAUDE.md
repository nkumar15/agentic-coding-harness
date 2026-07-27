# Claude Code Instructions

This repo is the source of the Portable Agentic Coding Harness package. The distributable package
lives entirely under `package/` — that is exactly what `scripts/install.sh`/`install.ps1` copy into a
consumer repository's root. Nothing outside `package/` is ever shipped.

## Required Reads

- Before changing anything under `package/`, read `package/.agents/rules/scm-conventions.md` and
  `package/.agents/rules/llm-behavior.md`.
- For this repo's own project facts (source root, verification commands, process provider), read
  `MAINTAINER-CONVENTIONS.md` — not `package/.agents/rules/project-conventions.md`, which must stay a
  generic placeholder because it ships to every consumer.
- For shell command discipline, read `package/.agents/rules/command-execution.md`.
- For tracked maintenance work on this repo, use `package/.agents/skills/orchestrate/SKILL.md`.

## Maintenance Rules

- Edit `package/.agents/` first.
- Regenerate host adapters with `python3 package/scripts/generate-agent-adapters.py`.
- Validate with `python3 package/scripts/validate-agent-portability.py` before committing.
- Never hand-edit `package/.claude/` or `package/.codex/agents/` directly; they are generated.
- Do not add this repo's own facts to `package/.agents/rules/project-conventions.md` or
  `package/.agents/rules/project-conventions-template.md` — those files ship as-is to every consumer
  and must stay generic.
