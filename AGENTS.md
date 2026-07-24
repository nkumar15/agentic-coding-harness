# Repository Instructions

Codex entrypoint for this reusable agentic workflow package. The canonical workflow source lives
under `.agents/`.

## Required Reads

- Before changing this workflow package, read `.agents/rules/project-conventions.md`.
- Before branch, commit, or change-request work, read `.agents/rules/scm-conventions.md`.
- For agent behavior, read `.agents/rules/llm-behavior.md`.
- For shell command discipline, read `.agents/rules/command-execution.md`.
- For tracked work, use `.agents/skills/orchestrate/SKILL.md` and resolve phases from
  `.agents/process/`.

## Workflows

Supported process specs:

- `feature`: PRD -> architecture -> development.
- `bug`: reproduce -> fix -> test.
- `chore`: describe -> implement.
- `docs`: write -> review.

When a process names a role, use the matching `.codex/agents/<role>.toml` wrapper if it is
available in the current Codex session. If the wrapper is unavailable, run the role inline from
`.agents/roles/<role>.md` and mention that Codex may need a restart to load newly generated
wrappers.

## Canonical Source

- Humans edit `.agents/` first.
- `.claude/` is generated Claude-compatible output.
- `.codex/agents/` is generated Codex custom-agent output.
- Do not put shared project prose in `.codex/rules/`; Codex reads canonical rules from
  `.agents/rules/` through this file.

## Maintenance

After changing `.agents/` or adapter metadata, run:

```bash
python3 scripts/generate-agent-adapters.py
python3 scripts/validate-agent-portability.py
```

## Main Branch Changes

- Do not commit or push directly to `main`.
- All changes intended for `main` must go through a pull request.
- Create the PR from the active work branch to `main` and report the PR URL.
- Do not merge a PR unless the user explicitly asks for the merge.
