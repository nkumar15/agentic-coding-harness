#!/usr/bin/env python3
"""Validate the portable agent workflow layout and generated host adapters."""

from __future__ import annotations

from pathlib import Path
import re
import sys

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".agents"
IGNORED_NAMES = {"__pycache__", ".DS_Store"}
ROLE_SKILL_PATTERN = re.compile(r"Apply the `([^`]+)` skill")


REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "docs/agentic-workflow/agent-portability.md",
    "docs/agentic-workflow/claude-codex-agentic-workflow-design.md",
    "docs/agentic-workflow/README.md",
    "docs/agentic-workflow/bmad-comparison.md",
    "docs/agentic-workflow/feature/README.md",
    "docs/agentic-workflow/bug/README.md",
    "docs/agentic-workflow/chore/README.md",
    "docs/agentic-workflow/docs/README.md",
    "docs/agentic-workflow/onboarding/python-fastapi.md",
    "scripts/generate-agent-adapters.py",
    "scripts/validate-agent-portability.py",
    ".github/workflows/agent-portability.yml",
    ".agents/rules/project-conventions.md",
    ".agents/rules/project-conventions-template.md",
    ".agents/rules/scm-conventions.md",
    ".agents/rules/llm-behavior.md",
    ".agents/rules/command-execution.md",
    ".agents/rules/feature-verification.md",
    ".agents/process/config.yaml",
    ".agents/process/gates.yaml",
    ".agents/process/provider.github.yaml",
    ".agents/process/provider.local.yaml",
]

REQUIRED_DIRS = [
    AGENTS / "rules",
    AGENTS / "process",
    AGENTS / "skills",
    AGENTS / "roles",
    AGENTS / "adapters" / "claude",
    AGENTS / "adapters" / "codex",
    ROOT / ".claude" / "agents",
    ROOT / ".claude" / "rules",
    ROOT / ".claude" / "process",
    ROOT / ".claude" / "skills",
    ROOT / ".codex" / "agents",
]


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
                raise ValueError(f"List item without list key in {path.relative_to(ROOT)}")
            metadata.setdefault(current_list, []).append(raw_line.split("- ", 1)[1].strip())
            continue
        current_list = None
        key, sep, value = raw_line.partition(":")
        if not sep:
            raise ValueError(f"Unsupported metadata line in {path.relative_to(ROOT)}: {raw_line}")
        if value.strip():
            metadata[key.strip()] = parse_value(value)
        else:
            metadata[key.strip()] = []
            current_list = key.strip()
    return metadata


def relative_files(path: Path) -> set[Path]:
    return {
        item.relative_to(path)
        for item in path.rglob("*")
        if item.is_file() and not any(part in IGNORED_NAMES for part in item.parts)
    }


def rewritten(text: str) -> str:
    return text.replace(".agents/", ".claude/")


def role_declared_skills(role: Path) -> set[str]:
    return set(ROLE_SKILL_PATTERN.findall(role.read_text(encoding="utf-8")))


def parse_toml(path: Path, errors: list[str]) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if tomllib is not None:
        try:
            return tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"invalid TOML in {path.relative_to(ROOT)}: {exc}")
            return {}

    values: dict[str, str] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep:
            errors.append(f"unsupported TOML line in {path.relative_to(ROOT)}: {line}")
            continue
        key = key.strip()
        value = value.strip()
        if value.startswith('"""'):
            body: list[str] = []
            while index < len(lines):
                raw = lines[index]
                index += 1
                if raw.endswith('"""'):
                    body.append(raw.removesuffix('"""'))
                    break
                body.append(raw)
            values[key] = "\n".join(body)
        elif value.startswith('"') and value.endswith('"'):
            values[key] = value[1:-1]
        else:
            errors.append(f"unsupported TOML value in {path.relative_to(ROOT)}: {line}")
    return values


def frontmatter(metadata: dict[str, object]) -> str:
    keys = ["name", "description", "tools", "model", "skills", "memory", "color", "maxTurns"]
    lines = ["---"]
    for key in keys:
        if key not in metadata:
            continue
        value = metadata[key]
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {item}" for item in value)
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def validate_required(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")
    for directory in REQUIRED_DIRS:
        if not directory.is_dir():
            errors.append(f"missing required directory: {directory.relative_to(ROOT)}")
    for directory in [AGENTS / "rules", AGENTS / "process", AGENTS / "skills", AGENTS / "roles"]:
        if directory.is_dir():
            for path in directory.rglob("*"):
                if path.is_symlink():
                    errors.append(f"canonical source must not contain symlink: {path.relative_to(ROOT)}")


def validate_generated_tree(source: Path, destination: Path, errors: list[str]) -> None:
    source_files = relative_files(source)
    destination_files = relative_files(destination)
    for missing in sorted(source_files - destination_files):
        errors.append(f"missing generated file: {(destination / missing).relative_to(ROOT)}")
    for extra in sorted(destination_files - source_files):
        errors.append(f"unexpected generated file: {(destination / extra).relative_to(ROOT)}")
    for rel in sorted(source_files & destination_files):
        expected = rewritten((source / rel).read_text(encoding="utf-8"))
        actual = (destination / rel).read_text(encoding="utf-8")
        if actual != expected:
            errors.append(f"generated file is out of sync: {(destination / rel).relative_to(ROOT)}")


def validate_roles_and_adapters(errors: list[str]) -> None:
    roles = sorted(path for path in (AGENTS / "roles").glob("*.md") if path.name != "README.md")
    if not roles:
        errors.append("no role files found")
        return

    skill_names = {path.name for path in (AGENTS / "skills").iterdir() if path.is_dir()}
    for skill_name in skill_names:
        skill_file = AGENTS / "skills" / skill_name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"skill missing SKILL.md: {skill_file.relative_to(ROOT)}")

    for role in roles:
        role_name = role.stem
        declared_skills = role_declared_skills(role)
        for skill in declared_skills:
            if skill not in skill_names:
                errors.append(f"{role.relative_to(ROOT)} references missing skill: {skill}")

        for host in ["claude", "codex"]:
            metadata_path = AGENTS / "adapters" / host / f"{role_name}.yaml"
            if not metadata_path.is_file():
                errors.append(f"missing {host} adapter metadata: {metadata_path.relative_to(ROOT)}")
                continue
            metadata = read_metadata(metadata_path)
            if metadata.get("name") != role_name:
                errors.append(f"{metadata_path.relative_to(ROOT)} name must match role {role_name}")
            if metadata.get("source_role") != f".agents/roles/{role_name}.md":
                errors.append(f"{metadata_path.relative_to(ROOT)} source_role mismatch")
            adapter_skills = set(metadata.get("skills", []))
            for skill in adapter_skills:
                if skill not in skill_names:
                    errors.append(f"{metadata_path.relative_to(ROOT)} references missing skill: {skill}")
            missing = declared_skills - adapter_skills
            if missing:
                errors.append(
                    f"{metadata_path.relative_to(ROOT)} missing role-declared skills: "
                    + ", ".join(sorted(missing))
                )


def validate_generated_agents(errors: list[str]) -> None:
    roles = sorted(path for path in (AGENTS / "roles").glob("*.md") if path.name != "README.md")
    expected_claude = {f"{role.stem}.md" for role in roles}
    expected_codex = {f"{role.stem}.toml" for role in roles}

    found_claude = {path.name for path in (ROOT / ".claude" / "agents").glob("*.md")}
    found_codex = {path.name for path in (ROOT / ".codex" / "agents").glob("*.toml")}
    if found_claude != expected_claude:
        errors.append(f".claude/agents mismatch: expected={sorted(expected_claude)}, found={sorted(found_claude)}")
    if found_codex != expected_codex:
        errors.append(f".codex/agents mismatch: expected={sorted(expected_codex)}, found={sorted(found_codex)}")

    note = "<!-- Generated from .agents/. Do not edit directly. -->"
    for role in roles:
        role_name = role.stem
        claude_metadata = read_metadata(AGENTS / "adapters" / "claude" / f"{role_name}.yaml")
        claude_file = ROOT / ".claude" / "agents" / f"{role_name}.md"
        if claude_file.is_file():
            expected = (
                frontmatter(claude_metadata)
                + "\n\n"
                + note
                + "\n\n"
                + rewritten(role.read_text(encoding="utf-8").rstrip())
                + "\n"
            )
            if claude_file.read_text(encoding="utf-8") != expected:
                errors.append(f"generated Claude agent out of sync: {claude_file.relative_to(ROOT)}")

        codex_metadata = read_metadata(AGENTS / "adapters" / "codex" / f"{role_name}.yaml")
        codex_file = ROOT / ".codex" / "agents" / f"{role_name}.toml"
        if codex_file.is_file():
            config = parse_toml(codex_file, errors)
            for key in ["name", "model"]:
                if config.get(key) != codex_metadata.get(key):
                    errors.append(f"{codex_file.relative_to(ROOT)} {key} mismatch")
            if config.get("model_reasoning_effort") != codex_metadata.get("reasoning_effort"):
                errors.append(f"{codex_file.relative_to(ROOT)} model_reasoning_effort mismatch")
            instructions = str(config.get("developer_instructions", ""))
            if str(codex_metadata["source_role"]) not in instructions:
                errors.append(f"{codex_file.relative_to(ROOT)} missing source role instruction")
            for skill in codex_metadata.get("skills", []):
                if f".agents/skills/{skill}/SKILL.md" not in instructions:
                    errors.append(f"{codex_file.relative_to(ROOT)} missing skill instruction: {skill}")


def gate_names(errors: list[str]) -> set[str]:
    gates_file = AGENTS / "process" / "gates.yaml"
    names: set[str] = set()
    for line in gates_file.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^  ([A-Za-z0-9_]+):\s*$", line)
        if match:
            names.add(match.group(1))
    if not names:
        errors.append("no gates found in .agents/process/gates.yaml")
    return names


def process_files() -> list[Path]:
    ignored = {"config.yaml", "gates.yaml"}
    return sorted(
        path
        for path in (AGENTS / "process").glob("*.yaml")
        if path.name not in ignored and not path.name.startswith("provider.")
    )


def validate_processes(errors: list[str]) -> None:
    roles = {path.stem for path in (AGENTS / "roles").glob("*.md") if path.name != "README.md"}
    gates = gate_names(errors)
    config_text = (AGENTS / "process" / "config.yaml").read_text(encoding="utf-8")
    provider_match = re.search(r"^provider:\s*([A-Za-z0-9_-]+)\s*$", config_text, re.MULTILINE)
    if not provider_match:
        errors.append(".agents/process/config.yaml missing provider")
    elif not (AGENTS / "process" / f"provider.{provider_match.group(1)}.yaml").is_file():
        errors.append(f"selected provider file missing: provider.{provider_match.group(1)}.yaml")

    for path in process_files():
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^process:\s*[A-Za-z0-9_-]+\s*$", text, re.MULTILINE):
            errors.append(f"{path.relative_to(ROOT)} missing process id")
        for role in re.findall(r"^[ \t]*(?:agent|on_fail):[ \t]*([A-Za-z0-9_-]+)", text, re.MULTILINE):
            if role not in roles:
                errors.append(f"{path.relative_to(ROOT)} references missing role: {role}")
        refs = re.findall(r"^[ \t]*(?:entry_gate|exit_gate|requires):[ \t]*([A-Za-z0-9_:-]+)", text, re.MULTILINE)
        refs.extend(re.findall(r"^[ \t]*-[ \t]*([A-Za-z0-9_]+(?::[A-Za-z0-9_-]+)?)[ \t]*(?:#.*)?$", text, re.MULTILINE))
        for ref in refs:
            base = ref.split(":", 1)[0]
            if base not in gates:
                errors.append(f"{path.relative_to(ROOT)} references missing gate: {ref}")


def validate_host_neutral_canonical(errors: list[str]) -> None:
    for directory in [AGENTS / "rules", AGENTS / "process", AGENTS / "roles", AGENTS / "skills"]:
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if ".claude/" in text or ".codex/" in text:
                errors.append(f"canonical shared file references host adapter path: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    if not errors:
        validate_roles_and_adapters(errors)
        validate_generated_tree(AGENTS / "rules", ROOT / ".claude" / "rules", errors)
        validate_generated_tree(AGENTS / "process", ROOT / ".claude" / "process", errors)
        validate_generated_tree(AGENTS / "skills", ROOT / ".claude" / "skills", errors)
        validate_generated_agents(errors)
        validate_processes(errors)
        validate_host_neutral_canonical(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("agent portability layout OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
