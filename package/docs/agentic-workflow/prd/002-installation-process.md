# PRD: Installation Process For Adopting This Package

- Issue: #2
- Status: Draft
- Phase: prd

## Overview

Today, adopting this package means manually copying `.agents/`, `.claude/`, `.codex/agents/`,
`AGENTS.md`, `CLAUDE.md`, `scripts/`, and `docs/agentic-workflow/` into a target repository, then
hand-filling `.agents/rules/project-conventions.md` and `.agents/process/gates.yaml` (root
`README.md#how-to-use-this`). There is no scripted install, no update path, and no way to layer an
optional add-on (such as the extracted `migration-workflow` package) onto an already-adopted repo.

This PRD defines a scripted installation process: a one-line `curl` command (POSIX shell, for
macOS/Linux) and an equivalent one-line Windows command (PowerShell), both invoking an installer that
copies the package into the target repository and interactively prompts for initial configuration
instead of leaving `project-conventions.md` fully manual.

Shipping a scripted installer also forces a repository-structure decision: this repo's own root
currently doubles as both the live Claude/Codex entrypoint for maintaining this package (`CLAUDE.md`,
`AGENTS.md`) and the literal files an installer would copy into a consumer's repo root. This PRD
includes restructuring this repo so the installable payload is a single, self-contained directory
(`package/`) that the installer copies wholesale, separate from this repo's own maintainer-only
entrypoints and conventions (see `Repository Structure` and issue #5's `MAINTAINER-CONVENTIONS.md`
work).

## Goals

- Replace "copy this package into the target repository" with a single documented command per
  platform.
- Have the installer interactively collect enough answers (process provider, stack skills, source/
  test roots, PRD/architecture directories, verification commands) to write a first-pass
  `project-conventions.md` and `config.yaml`, rather than leaving every field as `<FILL_IN>`.
- Support re-running the installer against an already-adopted repository to pick up upstream changes
  without clobbering a filled-in `project-conventions.md` or customized `gates.yaml` commands.
- Provide a mechanism for installing an optional add-on package (e.g. `migration-workflow`) on top of
  an already-installed base package.
- Separate this repo's own maintainer/dogfood entrypoints and conventions from the directory the
  installer copies, so the two never get mixed up.

## Non-Goals

- Redesigning the phases/gates/roles/skills model itself.
- Building the `migration-workflow` add-on's own packaging (tracked separately once it has its own
  repository).
- A package-manager-grade dependency/version resolver.
- A GUI installer.
- Automated CI coverage of the Windows path in this iteration (see `Decisions`).

## Repository Structure

The installable payload moves into a single top-level `package/` directory in this repo, mirroring
exactly what the installer copies into a consumer's repo root. This repo's own dogfood entrypoints
stay at this repo's root and are never copied:

```
agentic-coding-harness/                        # this repo — maintainer/dogfood context, never shipped
├── CLAUDE.md                                   # this repo's own entrypoint — points into package/
├── AGENTS.md                                   # same, for Codex
├── MAINTAINER-CONVENTIONS.md                   # this repo's own filled project facts (issue #5)
├── README.md                                   # about this project + curl/PowerShell install instructions
├── .gitignore                                  # ignores .claude/settings.local.json, config.local.yaml
├── .github/workflows/agent-portability.yml     # this repo's own CI — validates package/
├── scripts/
│   ├── install.sh                              # curl | sh entrypoint — copies package/ into target repo
│   └── install.ps1                             # irm | iex entrypoint — Windows equivalent
└── package/                                    # the install payload, copied verbatim into consumers
    ├── .agents/                                # canonical workflow source (unchanged content)
    ├── .claude/                                # generated Claude adapter output (unchanged content)
    ├── .codex/agents/                          # generated Codex adapter output (unchanged content)
    ├── AGENTS.md                               # shipped Codex entrypoint
    ├── CLAUDE.md                                # shipped Claude entrypoint
    ├── docs/agentic-workflow/                  # shipped workflow docs
    ├── scripts/
    │   ├── generate-agent-adapters.py          # consumers run this after editing their own .agents/
    │   └── validate-agent-portability.py       # consumers run this to validate their own copy
    └── .github/workflows/agent-portability.yml # CI template installed into the target's workflows
```

This resolves the mixing the installer would otherwise cause: `scripts/install.sh`/`install.ps1`
have exactly one job (copy `package/*` into the target repo's root and run the config prompts); this
repo's maintenance tooling (`package/scripts/generate-agent-adapters.py`,
`package/scripts/validate-agent-portability.py`) is the same tool a consumer runs post-install, so
there is no duplicate copy to keep in sync.

## Users

- A developer or team adopting this workflow package into an existing, already-populated repository.
- A developer on Windows without a POSIX shell available.
- A team that already adopted the package and wants to pull in later improvements.
- A team that wants to add the optional `migration-workflow` add-on after already running the base
  install.

## User Stories

1. As a developer adopting this workflow, I run one `curl` command in my repo and get a working
   `.agents/`, `.claude/`, `.codex/agents/`, `AGENTS.md`, `CLAUDE.md`, `scripts/`, and
   `docs/agentic-workflow/` without manually copying files.
2. As a Windows developer, I run one equivalent PowerShell command and get the same result.
3. As an adopter, the installer asks me a short set of configuration questions (process provider,
   stack skills, source/test roots, PRD/architecture directories, verification commands) and uses my
   answers to pre-fill `project-conventions.md` and `config.yaml`, instead of handing me an all-
   placeholder file.
4. As a team that already adopted the package, I re-run the installer and it updates the generic
   package files (`.agents/`, `.claude/`, `.codex/agents/`, `scripts/`) while leaving my filled
   `project-conventions.md` and customized `gates.yaml` commands untouched, reporting anything it
   could not safely merge.
5. As a team that wants the migration-workflow add-on, I run a documented add-on install command
   against a repo that already has the base package, without re-deriving directory layout
   conventions from scratch.

## Functional Requirements

1. A published one-line command for macOS/Linux (`curl -fsSL <install-url> | sh`) installs the
   package into the current repository.
2. A published one-line command for Windows (PowerShell, e.g. `irm <install-url> | iex`) does the
   same.
3. The installer copies the contents of this repo's `package/` directory verbatim into the target
   repository's root (see `Repository Structure`), rather than enumerating separate top-level paths.
4. The installer detects an existing install (e.g. `.agents/` already present) and switches to update
   mode instead of blind overwrite.
5. In update mode, the installer never silently overwrites an already-filled
   `.agents/rules/project-conventions.md` or a `.agents/process/gates.yaml` whose commands no longer
   match the shipped placeholders; it reports the conflict instead of guessing.
6. On first install, the installer interactively prompts for: process provider (`local`/`github`),
   backend/frontend/test stack skills, application source root, test root, PRD directory, feature
   architecture directory, verification evidence location, and global verification commands — then
   writes the answers into `project-conventions.md` and `config.yaml`.
7. After copying or updating, the installer runs `scripts/generate-agent-adapters.py` and
   `scripts/validate-agent-portability.py` and reports failures clearly before exiting.
8. The base installer accepts an `--addon <name>` flag (e.g. `--addon migration-workflow`) that
   downloads the named add-on's own versioned release and layers it into a repo that already has the
   base package installed.
9. Root `README.md#how-to-use-this` is rewritten to lead with the new install commands instead of
   "Copy this package into the target repository."
10. This repo's own `.agents/`, `.claude/`, `.codex/agents/`, `AGENTS.md`, `CLAUDE.md`, `docs/`, and
    `scripts/` (except `install.sh`/`install.ps1`/`install.bat`) move under `package/`, unchanged in
    content; this repo's root gains its own `CLAUDE.md`, `AGENTS.md`, and `MAINTAINER-CONVENTIONS.md`
    for maintaining this package, per `Repository Structure`.
11. `install.sh` (POSIX shell) and `install.ps1` (PowerShell) are small bootstrap launchers only: they
    resolve the target release version, download its release tarball, and extract `package/` into the
    target repo. The interactive configuration step (prompts, writing `project-conventions.md` and
    `config.yaml`) runs as a Python script bundled inside the downloaded package
    (`package/scripts/configure.py`), not as shell-native prompts.
12. `install.bat` is a thin wrapper for classic `cmd.exe` users: it shells out to
    `powershell -NoProfile -Command` to run the same `install.ps1` logic, so `cmd.exe` users get the
    identical installer without needing to open PowerShell themselves.

## Technical Considerations

- The `curl`/PowerShell one-liners point at a specific tagged GitHub Release, never an unpinned raw
  file on `main`, so a given install command is fully reproducible regardless of when it is run.
- The POSIX installer should be plain `sh` (not bash-only) for portability; the Windows installer
  should run on stock PowerShell without extra modules.
- Copy/update logic must be idempotent and safe by default: never destroy an adopter's existing
  customizations without an explicit confirmation or a `--force`-style flag.
- `install.sh`/`install.ps1` are deliberately minimal (download + extract only) so they are easy to
  read and audit before anyone pipes them into `sh`/`iex`; all interactive and update-diff logic lives
  in `package/scripts/configure.py`, which runs only after the payload is already on disk.
- Moving `generate-agent-adapters.py` and `validate-agent-portability.py` under `package/scripts/`
  means their internal path resolution must be relative to the script's own location (or an explicit
  package root), not the caller's working directory, so they behave identically whether run from this
  repo's root or from a freshly installed consumer repo's root.
- Python 3 becomes an explicit installer prerequisite (it already is one for
  `generate-agent-adapters.py`/`validate-agent-portability.py`), so `install.sh`/`install.ps1` should
  check for it and fail with a clear message rather than a stack trace if it's missing.

## Verification Requirements

- User-visible acceptance checks:
  - Running the macOS/Linux command against a clean, empty git repo produces a working
    `.agents/`, `.claude/`, `.codex/agents/`, `AGENTS.md`, `CLAUDE.md`, `scripts/`, and
    `docs/agentic-workflow/` tree at the target repo's root, and `scripts/validate-agent-portability.py`
    passes when run from that tree.
  - Running the Windows command against a clean, empty git repo produces the same result.
  - Running `install.bat` from `cmd.exe` produces the same result as running `install.ps1` directly
    from PowerShell.
  - Re-running either installer against a repo with an already-filled `project-conventions.md` and a
    customized `gates.yaml` leaves both files unchanged and reports what it skipped.
  - The interactive prompts, when answered, produce a `project-conventions.md` with no remaining
    `<FILL_IN>` placeholders for the fields asked.
  - This repo's own `package/scripts/generate-agent-adapters.py` and
    `package/scripts/validate-agent-portability.py` run correctly against `package/` when invoked from
    this repo's root, proving the same scripts work unmodified once installed at a consumer's root.
- Expected coverage: a scripted smoke test harness exercising (a) fresh install and (b) update-
  without-clobber, run against scratch temporary git repositories; a manual smoke pass on Windows
  PowerShell since Windows CI is out of scope for this iteration.
- Local commands a developer should run: invoke the installer against a scratch temp repo, confirm
  exit code 0 and expected files present, then run `python3 scripts/validate-agent-portability.py`.
- Test data/fixtures: a scratch empty-repo fixture (fresh install path) and a scratch repo fixture
  pre-seeded with a filled `project-conventions.md` and edited `gates.yaml` (update path).
- Explicit non-goals: no installer performance benchmarking; no automated Windows CI job in this
  iteration (the `cmd.exe`/PowerShell smoke check above is manual for now).

## Decisions

1. **Hosting**: the installer commands fetch a versioned GitHub Release asset, not an unpinned raw
   file on `main`. Every install is reproducible against the version it was run with.
2. **Installer shape**: `install.sh`/`install.ps1` are small bootstrap launchers (resolve version,
   download release tarball, extract `package/`); all interactive configuration and update-diff logic
   runs afterward as `package/scripts/configure.py`, not as shell-native prompt code.
3. **Windows support**: both PowerShell (`install.ps1`) and classic `cmd.exe` (`install.bat`, which
   shells out to the PowerShell logic) are supported.
4. **Add-on installation**: the base installer takes a `--addon <name>` flag that downloads and layers
   an add-on's own versioned release (starting with `migration-workflow`) onto an already-installed
   base package.
