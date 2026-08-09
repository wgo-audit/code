#!/usr/bin/env python3
"""Validate WGO reviewer package structure without judging audit quality."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_FIELDS = ("id", "name", "summary", "version", "codegraph")
REQUIRED_SECTIONS = (
    "## Objective And Business Questions",
    "## Output Menu",
    "## Recommended Inputs And Downstream Use",
    "## Completion Criteria",
    "## Escalation Conditions",
    "## Cross-Reviewer Links",
)
CODEGRAPH_VALUES = {"none", "optional", "required"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+(?:\.[0-9]+)?$")


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)


def package_dir(path: Path) -> Path:
    return path.parent if path.name == "reviewer.md" else path


def read_text(path: Path, result: Result) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        result.error(f"{path}: cannot read: {exc}")
        return ""


def parse_frontmatter(content: str, result: Result, path: Path) -> dict[str, object]:
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        result.error(f"{path}: missing YAML frontmatter")
        return {}

    metadata: dict[str, object] = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        if line == "---":
            return metadata
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line.startswith("  - "):
            result.error(f"{path}:{index + 1}: list item without key")
            index += 1
            continue
        if ":" not in line:
            result.error(f"{path}:{index + 1}: malformed frontmatter line")
            index += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            metadata[key] = value
            index += 1
            continue
        items: list[str] = []
        index += 1
        while index < len(lines) and lines[index].startswith("  - "):
            items.append(lines[index][4:].strip())
            index += 1
        metadata[key] = items
    result.error(f"{path}: frontmatter is not closed")
    return metadata


def validate_package(path: Path, core_ids: set[str], external: bool) -> Result:
    result = Result()
    root = package_dir(path)
    reviewer = root / "reviewer.md"
    if not reviewer.is_file():
        result.error(f"{root}: missing reviewer.md")
        return result

    content = read_text(reviewer, result)
    metadata = parse_frontmatter(content, result, reviewer)

    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] in ("", []):
            result.error(f"{reviewer}: missing required metadata field: {field}")

    reviewer_id = metadata.get("id")
    if isinstance(reviewer_id, str):
        if not ID_PATTERN.fullmatch(reviewer_id):
            result.error(f"{reviewer}: id must be kebab-case: {reviewer_id}")
        if root.name != reviewer_id:
            result.error(f"{reviewer}: id must match package folder name: {root.name}")

    version = metadata.get("version")
    if isinstance(version, str) and not VERSION_PATTERN.fullmatch(version):
        result.error(f"{reviewer}: version must be numeric, for example 0.1 or 1.2.0")

    codegraph = metadata.get("codegraph")
    if isinstance(codegraph, str) and codegraph not in CODEGRAPH_VALUES:
        result.error(f"{reviewer}: invalid codegraph value: {codegraph}")

    dependencies = metadata.get("depends_on", [])
    if dependencies and not isinstance(dependencies, list):
        result.error(f"{reviewer}: depends_on must be a YAML list")
        dependencies = []
    for dependency in dependencies:
        if not ID_PATTERN.fullmatch(dependency):
            result.error(f"{reviewer}: dependency must be kebab-case: {dependency}")
        if core_ids and dependency not in core_ids:
            result.error(f"{reviewer}: unknown dependency: {dependency}")
        if dependency == reviewer_id:
            result.error(f"{reviewer}: reviewer cannot depend on itself")

    supersedes = metadata.get("supersedes")
    if supersedes:
        if not isinstance(supersedes, str) or not ID_PATTERN.fullmatch(supersedes):
            result.error(f"{reviewer}: supersedes must name one kebab-case core reviewer")
        if not external:
            result.error(f"{reviewer}: supersedes is allowed only for external reviewers")
        if core_ids and isinstance(supersedes, str) and supersedes not in core_ids:
            result.error(f"{reviewer}: supersedes unknown core reviewer: {supersedes}")

    for section in REQUIRED_SECTIONS:
        if section not in content:
            result.error(f"{reviewer}: missing required section: {section}")

    validate_installers(root, result)
    validate_workers(root, result)
    validate_control_namespace(content, reviewer, result)
    return result


def validate_installers(root: Path, result: Result) -> None:
    pairs = (
        ("validate_install.sh", "install.sh"),
        ("validate_install.bat", "install.bat"),
    )
    for validator, installer in pairs:
        if (root / validator).exists() and not (root / installer).exists():
            result.error(f"{root}: {validator} requires matching {installer}")


def validate_workers(root: Path, result: Result) -> None:
    worker_dir = root / "workers"
    if not worker_dir.exists():
        return
    for worker in sorted(worker_dir.glob("*.md")):
        content = read_text(worker, result)
        if len(content.splitlines()) > 25:
            result.error(f"{worker}: worker prompt exceeds 25 lines")
        lowered = content.lower()
        for required in (
            "do not write audit artifacts",
            "do not invoke codegraph",
        ):
            if required not in lowered:
                result.error(f"{worker}: missing worker boundary: {required}")


def validate_control_namespace(content: str, reviewer: Path, result: Result) -> None:
    output_menu = content.split("## Output Menu", 1)
    if len(output_menu) != 2:
        return
    output_menu = output_menu[1].split("\n## ", 1)[0]
    roots = {
        match
        for match in re.findall(r"`controls/([^/`]+)/", output_menu)
        if match != "open-items.md"
    }
    if len(roots) > 1:
        result.error(f"{reviewer}: more than one reviewer-owned control namespace: {sorted(roots)}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packages", nargs="+", type=Path)
    parser.add_argument("--core-id", action="append", default=[])
    parser.add_argument("--external", action="store_true")
    args = parser.parse_args(argv)

    errors: list[str] = []
    for package in args.packages:
        errors.extend(validate_package(package, set(args.core_id), args.external).errors)

    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
