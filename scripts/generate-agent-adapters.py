#!/usr/bin/env python3
"""Generate host adapter files from canonical `.agents` sources."""

from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".agents"
IGNORED = shutil.ignore_patterns("__pycache__", ".DS_Store")


def parse_value(raw: str) -> object:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        body = raw[1:-1].strip()
        if not body:
            return []
        return [item.strip().strip('"').strip("'") for item in body.split(",")]
    if raw.isdigit():
        return int(raw)
    return raw.strip('"').strip("'")


def read_metadata(path: Path) -> dict[str, object]:
    metadata: dict[str, object] = {}
    current_list: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith("  - "):
            if current_list is None:
                raise SystemExit(f"List item without list key in {path.relative_to(ROOT)}")
            metadata.setdefault(current_list, []).append(raw_line.split("- ", 1)[1].strip())
            continue

        current_list = None
        key, sep, value = raw_line.partition(":")
        if not sep:
            raise SystemExit(f"Unsupported adapter metadata line in {path.relative_to(ROOT)}: {raw_line}")
        key = key.strip()
        value = value.strip()
        if value:
            metadata[key] = parse_value(value)
        else:
            metadata[key] = []
            current_list = key

    return metadata


def toml_value(value: object) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def toml_multiline(value: str) -> str:
    escaped = value.replace('"""', '\\"\\"\\"')
    return '"""\n' + escaped.rstrip() + '\n"""'


def replace_agent_paths(text: str) -> str:
    return text.replace(".agents/", ".claude/")


def sync_tree(source: Path, destination: Path, *, rewrite_agent_paths: bool) -> None:
    if not source.is_dir():
        raise SystemExit(f"Missing source directory: {source.relative_to(ROOT)}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=IGNORED)
    if rewrite_agent_paths:
        for path in destination.rglob("*"):
            if path.is_file():
                path.write_text(replace_agent_paths(path.read_text(encoding="utf-8")), encoding="utf-8")


def role_description(metadata_path: Path, metadata: dict[str, object]) -> str:
    if metadata.get("description"):
        return str(metadata["description"])
    claude_metadata = AGENTS / "adapters" / "claude" / metadata_path.name
    if claude_metadata.is_file():
        return str(read_metadata(claude_metadata).get("description", metadata.get("name", metadata_path.stem)))
    return str(metadata.get("name", metadata_path.stem))


def write_claude_agent(metadata_path: Path) -> None:
    metadata = read_metadata(metadata_path)
    output = ROOT / str(metadata["output"])
    role = ROOT / str(metadata["source_role"])
    output.parent.mkdir(parents=True, exist_ok=True)

    frontmatter_keys = ["name", "description", "tools", "model", "skills", "memory", "color", "maxTurns"]
    frontmatter: list[str] = ["---"]
    for key in frontmatter_keys:
        if key not in metadata:
            continue
        value = metadata[key]
        if isinstance(value, list):
            frontmatter.append(f"{key}:")
            frontmatter.extend(f"  - {item}" for item in value)
        else:
            frontmatter.append(f"{key}: {value}")
    frontmatter.append("---")

    body = replace_agent_paths(role.read_text(encoding="utf-8").rstrip())
    generated_note = "<!-- Generated from .agents/. Do not edit directly. -->"
    output.write_text("\n".join(frontmatter) + "\n\n" + generated_note + "\n\n" + body + "\n", encoding="utf-8")


def codex_instructions(role_name: str, source_role: str, skills: list[str]) -> str:
    lines = [
        f"Load and follow `{source_role}`.",
        "",
        "Read and follow:",
        "- AGENTS.md",
        "- .agents/rules/llm-behavior.md",
        "- .agents/rules/scm-conventions.md",
        "- .agents/rules/command-execution.md",
        "- .agents/rules/project-conventions.md for feature, bug, chore, and docs work",
    ]
    if (AGENTS / "rules" / "migration-conventions.md").is_file():
        lines.append("- .agents/rules/migration-conventions.md for migration work")
    if skills:
        lines.extend(
            [
                "",
                "Resolve project conventions (and migration conventions when this repository has",
                "adopted the migration workflow), active process phase, and touched files first. Then",
                "read and apply only the relevant skills from this adapter list:",
            ]
        )
        lines.extend(f"- .agents/skills/{skill}/SKILL.md" for skill in skills)
    lines.extend(
        [
            "",
            "Use the repository tools available in the current Codex session. If a referenced custom",
            "agent wrapper or skill is unavailable, proceed inline from the shared role instructions.",
            f"Role id: {role_name}",
        ]
    )
    return "\n".join(lines)


def write_codex_agent(metadata_path: Path) -> None:
    metadata = read_metadata(metadata_path)
    output = ROOT / str(metadata["output"])
    output.parent.mkdir(parents=True, exist_ok=True)

    skills = metadata.get("skills", [])
    if not isinstance(skills, list):
        skills = []

    lines = [
        f"name = {toml_value(metadata['name'])}",
        f"description = {toml_value(role_description(metadata_path, metadata))}",
        f"model = {toml_value(metadata['model'])}",
        f"model_reasoning_effort = {toml_value(metadata['reasoning_effort'])}",
        "",
        f"developer_instructions = {toml_multiline(codex_instructions(str(metadata['name']), str(metadata['source_role']), [str(skill) for skill in skills]))}",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    sync_tree(AGENTS / "rules", ROOT / ".claude" / "rules", rewrite_agent_paths=True)
    sync_tree(AGENTS / "process", ROOT / ".claude" / "process", rewrite_agent_paths=True)
    sync_tree(AGENTS / "skills", ROOT / ".claude" / "skills", rewrite_agent_paths=True)

    claude_agents = ROOT / ".claude" / "agents"
    if claude_agents.exists():
        shutil.rmtree(claude_agents)
    claude_agents.mkdir(parents=True, exist_ok=True)

    codex_agents = ROOT / ".codex" / "agents"
    if codex_agents.exists():
        shutil.rmtree(codex_agents)
    codex_agents.mkdir(parents=True, exist_ok=True)

    for metadata_path in sorted((AGENTS / "adapters" / "claude").glob("*.yaml")):
        write_claude_agent(metadata_path)
    for metadata_path in sorted((AGENTS / "adapters" / "codex").glob("*.yaml")):
        write_codex_agent(metadata_path)

    print("generated Claude and Codex adapter files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
