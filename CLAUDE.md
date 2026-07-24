# Claude Code Instructions

Claude Code entrypoint for this reusable agentic workflow package. The canonical workflow source is
under `.agents/`, and generated Claude-compatible output is committed under `.claude/`.

## Required Reads

- Before changing this workflow package, read `.claude/rules/project-conventions.md`.
- Before branch, commit, or change-request work, read `.claude/rules/scm-conventions.md`.
- For agent behavior, read `.claude/rules/llm-behavior.md`.
- For shell command discipline, read `.claude/rules/command-execution.md`.
- For tracked work, use `.claude/skills/orchestrate/SKILL.md`.
- Resolve phases and gates from `.claude/process/`.
- Launch named Claude agents from `.claude/agents/` through Claude Code's host mechanism.

## Workflows

Supported process specs:

- `feature`: PRD -> architecture -> development.
- `bug`: reproduce -> fix -> test.
- `chore`: describe -> implement.
- `docs`: write -> review.

## Canonical Source

- Humans edit `.agents/` first.
- `.claude/` is generated Claude adapter output plus Claude-local settings/memory if a consuming
  repo chooses to add those.
- `.codex/agents/` is generated Codex adapter output.
- Do not move shared project conventions into `.codex/rules/`; Codex reads canonical rules from
  `.agents/rules/`.
