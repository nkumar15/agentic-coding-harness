#!/usr/bin/env python3
"""Import an external skill package into canonical `.agents/skills/`.

Wraps `npx skills add`, always targeting `-a universal` (which the CLI installs to
`.agents/skills/`) and never `-a claude-code` (which would write into this package's
generated `.claude/skills/` output). See docs/agentic-workflow/agent-portability.md.

This script only fetches skill content into canonical source. It does not wire the
skill into any role's adapter metadata, does not regenerate host adapters, and does
not track skill provenance/updates — those stay manual, human-judgment steps.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".agents"
LOCK_FILE = ROOT / "skills-lock.json"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="Source repo, e.g. owner/repo")
    parser.add_argument("--skill", required=True, help="Skill name to install (matches SKILL.md frontmatter name)")
    return parser.parse_args(argv)


def snapshot(directory: Path) -> set[Path]:
    if not directory.is_dir():
        return set()
    return set(directory.rglob("*"))


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if shutil.which("npx") is None:
        print("npx is required but was not found on PATH.", file=sys.stderr)
        return 1

    before_claude = snapshot(ROOT / ".claude")
    before_codex = snapshot(ROOT / ".codex")
    lock_before = LOCK_FILE.read_text(encoding="utf-8") if LOCK_FILE.is_file() else None

    result = subprocess.run(
        [
            "npx", "skills", "add", args.repo,
            "--skill", args.skill,
            "-a", "universal",
            "--copy",
            "-y",
        ],
        cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"npx skills add failed for {args.repo} --skill {args.skill}", file=sys.stderr)
        return result.returncode

    # skills-lock.json is the CLI's own provenance manifest; tracking it is out of scope
    # here (see issue #12), so restore whatever was there before this run rather than
    # discarding entries a prior, unrelated `npx skills add` run may have recorded.
    if lock_before is None:
        if LOCK_FILE.is_file():
            LOCK_FILE.unlink()
    else:
        LOCK_FILE.write_text(lock_before, encoding="utf-8")

    skill_file = AGENTS / "skills" / args.skill / "SKILL.md"
    if not skill_file.is_file():
        print(f"expected {skill_file.relative_to(ROOT)} after import, but it was not found.", file=sys.stderr)
        return 1

    if snapshot(ROOT / ".claude") != before_claude or snapshot(ROOT / ".codex") != before_codex:
        print("npx skills add wrote into generated .claude/ or .codex/ output; aborting.", file=sys.stderr)
        return 1

    print(f"imported {args.skill} into {skill_file.parent.relative_to(ROOT)}")
    print("Next steps (manual):")
    print(f'  1. Add "{args.skill}" to the relevant skills: list(s) in .agents/adapters/{{claude,codex}}/*.yaml')
    print("  2. python3 scripts/generate-agent-adapters.py")
    print("  3. python3 scripts/validate-agent-portability.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
