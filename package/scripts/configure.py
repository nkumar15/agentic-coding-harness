#!/usr/bin/env python3
"""Interactive first-pass configuration for project-conventions.md and config.yaml.

Runs from the target repository's root after the installer has extracted the package there.
Never touches project-conventions.md if it is already filled in (no `<FILL_IN` tokens remain).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
CONVENTIONS = ROOT / ".agents" / "rules" / "project-conventions.md"
CONFIG = ROOT / ".agents" / "process" / "config.yaml"

FIELDS = [
    ("Project name", "Project name"),
    ("Primary language/framework", "Primary language/framework"),
    ("Backend stack skills", "Backend stack skills (e.g. python-fastapi, java-springboot, or none)"),
    ("Backend test skills", "Backend test skills (e.g. pytest, junit, or none)"),
    ("Frontend stack skills", "Frontend stack skills (e.g. react-ui, or none)"),
    ("Database/change-data skills", "Database/change-data skills (e.g. postgres-migrations, or none)"),
    ("Application source root", "Application source root"),
    ("Test root", "Test root"),
    ("PRD directory", "PRD directory"),
    ("Feature architecture directory", "Feature architecture directory"),
    ("Verification evidence location", "Verification evidence location"),
    ("Global verification commands", "Global verification commands"),
    ("Feature-specific verification source", "Feature-specific verification source"),
    ("Local runtime command", "Local runtime command"),
]


def is_unfilled(text: str) -> bool:
    return "<FILL_IN" in text


def fill_table(text: str, answers: dict[str, str]) -> str:
    lines = text.splitlines()
    for row_name, _ in FIELDS:
        prefix = f"| {row_name} |"
        for index, line in enumerate(lines):
            if line.startswith(prefix):
                lines[index] = f"{prefix} {answers[row_name]} |"
    return "\n".join(lines) + "\n"


def set_provider(text: str, provider: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("provider:"):
            lines[index] = f"provider: {provider}"
    return "\n".join(lines) + "\n"


def main() -> int:
    if not CONVENTIONS.is_file():
        print(f"missing {CONVENTIONS.relative_to(ROOT)}")
        return 1

    conventions_text = CONVENTIONS.read_text(encoding="utf-8")
    if not is_unfilled(conventions_text):
        print("project-conventions.md is already filled in; skipping interactive configuration")
        return 0

    print("First-time setup: answer the following to fill in project-conventions.md.")
    answers = {row_name: input(f"{prompt}: ").strip() for row_name, prompt in FIELDS}

    provider = ""
    while provider not in ("local", "github"):
        provider = input("Process provider (local/github): ").strip().lower()

    CONVENTIONS.write_text(fill_table(conventions_text, answers), encoding="utf-8")
    if CONFIG.is_file():
        CONFIG.write_text(set_provider(CONFIG.read_text(encoding="utf-8"), provider), encoding="utf-8")

    print("Wrote project-conventions.md and config.yaml.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
