#!/usr/bin/env python3
"""Optionally validate lean WGO audit structure without judging conclusions."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


BASE_REQUIRED = (
    "audit-brief.md",
    "audit-checklist.md",
    "evidence/evidence-ledger.md",
    "evidence/source-access-register.md",
    "controls/open-items.md",
)
FINAL_REQUIRED = (
    "index.md",
    "executive-summary.md",
    "product-manager-notes.md",
    "technical-lead-notes.md",
)
FINAL_HEADINGS = {
    "index.md": (
        "## Start Here",
        "## Audience Routes",
        "## Evidence Boundary",
    ),
    "executive-summary.md": (
        "## Mandate, Boundary, And Bottom Line",
        "## Current Product And Control Position",
        "## Material Risks, Unknowns, And Decisions",
        "## Evidence-Supported 30–90 Day Plan",
        "## Reader Routing And Limits",
    ),
    "product-manager-notes.md": (
        "## Capability, Workflow, And Promise Position",
        "## Decisions And Specialist Sign-Off Boundaries",
        "## Material Gaps, Risks, And Next Work",
        "## Evidence And Limits",
    ),
    "technical-lead-notes.md": (
        "## Current Technical Position",
        "## Architecture, Operations, Quality, And Security Findings",
        "## Safe Evolution Priorities",
        "## Traceability And Limits",
    ),
}
REVIEWER_HEADINGS = (
    "## Audit Question, Depth, And Evidence Boundary",
    "## Coverage And Material Gaps",
    "## Key Findings",
    "## Selected Outputs",
    "## Material Omissions, Unknowns, And Auditor Questions",
    "## Reconciliation",
    "## Bounded Conclusion And Downstream Guidance",
)
REVIEWER_QUESTION_HEADINGS = (
    "## Material Omissions, Unknowns, And Auditor Questions",
    "## Material Omissions, Unknowns, And Stakeholder Questions",
)
HANDOFF_HEADINGS = (
    "## Confirmed Navigation",
    "## Constraints And Conflicts",
    "## Material Unknowns",
    "## Downstream Use",
)
DECISION_HEADINGS = (
    "## Decision Statement",
    "## Observed Position, Rationale, And Approval",
    "## Constraints, Options, And Tradeoffs",
    "## Impacts And Boundaries",
    "## Change, Reversal, And Follow-Up",
)
INVENTORY_HEADINGS = ("## Coverage Domains", "## Decision Candidates")
REGISTER_HEADINGS = ("## Records", "## Coverage And Disposition")
DIAGRAM_HEADINGS = (
    "## Purpose And Evidence Boundary",
    "## Diagram",
    "## Known Gaps And Follow-Up",
)
PACKET_HEADINGS = (
    "## Scope And Evidence Boundary",
    "## Observations",
    "## Material Unknowns And Access Limits",
    "## Reuse Guidance",
)
OPERATOR_AID_HEADINGS = (
    "## Purpose And Evidence Boundary",
    "## Authority And Preconditions",
    "## Procedure And Stop Conditions",
    "## Expected Evidence And Records",
    "## Escalation, Recovery, And Unknowns",
)
TRANSITION_PACKET_AIDS = (
    "replacement-maintainer.md",
    "recovery.md",
    "observability.md",
    "iam-and-credential-control.md",
)
ID_PATTERN = re.compile(r"(?:ARCH-DC|PROD-DC|E|OI|ADR|PDR|DGM)-\d{3}")
ID_CANDIDATE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:ARCH-DC|PROD-DC|E|OI|ADR|PDR|DGM)-[0-9#][A-Za-z0-9#]*"
)
OPEN_ITEM_STATUSES = {
    "open",
    "verified-fixed",
    "superseded",
    "out-of-current-scope",
}
OPEN_ITEM_TYPES = {"risk", "decision-needed", "verification", "action"}
OPEN_ITEM_PRIORITIES = {"P1", "P2", "P3"}
CHECKLIST_STATES = {
    "confirmed",
    "not-started",
    "in-progress",
    "rerun-pending",
    "completed",
    "completed-with-open-verification",
    "blocked",
}
CUTOFF_LABELS = (
    "within-cutoff",
    "post-cutoff-validation",
    "historical-undated",
    "unknown",
)
TABLE_SCHEMAS = {
    "audit-checklist.md": (
        "Work item",
        "State",
        "Next action",
        "Recommended next reviewer",
        "Factual completion condition",
    ),
    "evidence/evidence-ledger.md": (
        "Evidence ID",
        "Source type",
        "Exact locator",
        "Observed/effective time",
        "Cutoff eligibility",
        "Factual summary",
        "Limitation",
        "Sensitivity",
    ),
    "evidence/source-access-register.md": (
        "Source",
        "Attempt/time",
        "Result or limitation",
        "Question affected",
        "Material impact",
        "Approved fallback/exclusion",
        "Owner and next step",
    ),
    "controls/open-items.md": (
        "ID",
        "Type",
        "Priority",
        "Item and consequence",
        "Evidence/artifact links",
        "Owner",
        "Closure route",
        "Status",
    ),
    "documentation/catalog.md": (
        "ID",
        "Original path",
        "Cached text path",
        "Format",
        "Type and topics",
        "Relevant reviewers",
        "Summary (target 75–100 words; max 120)",
        "Limits",
    ),
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
)


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path: Path, result: Result) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        result.error(f"Cannot read as UTF-8: {path}")
        return ""


def check_required(root: Path, paths: tuple[str, ...], result: Result) -> None:
    for relative in paths:
        if not (root / relative).is_file():
            result.error(f"Missing required file: {relative}")


def check_headings(path: Path, headings: tuple[str, ...], root: Path, result: Result) -> None:
    content = read_text(path, result)
    for heading in headings:
        if heading not in content:
            result.error(f"{path.relative_to(root)} missing required heading: {heading}")


def table_cells(line: str) -> tuple[str, ...]:
    if not line.strip().startswith("|"):
        return ()
    return tuple(cell.strip() for cell in line.strip().strip("|").split("|"))


def table_rows(
    path: Path,
    expected: tuple[str, ...],
    root: Path,
    result: Result,
    report_missing: bool = True,
) -> list[tuple[int, tuple[str, ...]]]:
    lines = read_text(path, result).splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if table_cells(line) == expected),
        None,
    )
    if header_index is None:
        if report_missing:
            result.error(
                f"{path.relative_to(root)} missing required table schema: "
                f"{' | '.join(expected)}"
            )
        return []
    rows: list[tuple[int, tuple[str, ...]]] = []
    for index in range(header_index + 1, len(lines)):
        if lines[index].lstrip().startswith("#"):
            break
        cells = table_cells(lines[index])
        if not cells:
            if lines[index].strip():
                break
            if rows:
                break
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if len(cells) != len(expected):
            result.error(
                f"{path.relative_to(root)}:{index + 1} has {len(cells)} table "
                f"cells; expected {len(expected)}"
            )
            continue
        rows.append((index + 1, cells))
    return rows


def check_table_contracts(root: Path, result: Result) -> None:
    for relative, expected in TABLE_SCHEMAS.items():
        path = root / relative
        if not path.is_file():
            continue
        rows = table_rows(path, expected, root, result)
        if relative == "audit-checklist.md":
            for line_number, cells in rows:
                if cells[1] not in CHECKLIST_STATES:
                    result.error(
                        f"{relative}:{line_number} has invalid checklist state: "
                        f"{cells[1] or 'missing'}"
                    )


def check_id_formats(root: Path, result: Result) -> None:
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if relative.parts[:2] == ("documentation", "tmp"):
            continue
        for line_number, line in enumerate(read_text(path, result).splitlines(), 1):
            for candidate in ID_CANDIDATE_PATTERN.findall(line):
                if not ID_PATTERN.fullmatch(candidate):
                    result.error(
                        f"{relative}:{line_number} has invalid stable ID: "
                        f"{candidate} (expected PREFIX-NNN)"
                    )


def check_final_reports(root: Path, result: Result) -> None:
    for relative, headings in FINAL_HEADINGS.items():
        path = root / relative
        if path.is_file():
            check_headings(path, headings, root, result)


def check_reviewer_reports(root: Path, result: Result) -> None:
    reports = root / "reviewer-reports"
    if not reports.is_dir():
        result.warn("No reviewer-reports directory found")
        return
    for reviewer_dir in sorted(path for path in reports.iterdir() if path.is_dir()):
        report = reviewer_dir / "report.md"
        if not report.is_file():
            result.error(f"Missing reviewer report: {report.relative_to(root)}")
        else:
            check_headings(
                report,
                tuple(
                    heading
                    for heading in REVIEWER_HEADINGS
                    if heading != REVIEWER_QUESTION_HEADINGS[0]
                ),
                root,
                result,
            )
            content = read_text(report, result)
            if not any(heading in content for heading in REVIEWER_QUESTION_HEADINGS):
                result.error(
                    f"{report.relative_to(root)} missing required heading: "
                    f"{REVIEWER_QUESTION_HEADINGS[0]}"
                )
        handoff = reviewer_dir / "handoff.md"
        if not handoff.is_file():
            result.error(f"Missing reviewer handoff: {handoff.relative_to(root)}")
        else:
            check_headings(handoff, HANDOFF_HEADINGS, root, result)


def check_cutoffs(root: Path, result: Result) -> None:
    ledger = root / "evidence/evidence-ledger.md"
    if not ledger.is_file():
        return
    for line_number, cells in table_rows(
        ledger,
        TABLE_SCHEMAS["evidence/evidence-ledger.md"],
        root,
        result,
        report_missing=False,
    ):
        if not ID_PATTERN.fullmatch(cells[0]) or not cells[0].startswith("E-"):
            result.error(
                f"evidence/evidence-ledger.md:{line_number} has invalid evidence ID: "
                f"{cells[0] or 'missing'} (expected E-NNN)"
            )
            continue
        labels = [
            label
            for label in CUTOFF_LABELS
            if re.search(rf"(?<![a-z-]){re.escape(label)}(?![a-z-])", cells[4])
        ]
        if len(labels) != 1:
            result.error(
                "Evidence row has invalid cutoff eligibility: "
                f"evidence/evidence-ledger.md:{line_number} "
                f"{cells[4] or 'missing'}; expected one of {', '.join(CUTOFF_LABELS)}"
            )


def check_open_items(root: Path, result: Result) -> None:
    path = root / "controls/open-items.md"
    if not path.is_file():
        return
    seen: dict[str, int] = {}
    for line_number, cells in table_rows(
        path,
        TABLE_SCHEMAS["controls/open-items.md"],
        root,
        result,
        report_missing=False,
    ):
        if not ID_PATTERN.fullmatch(cells[0]) or not cells[0].startswith("OI-"):
            result.error(
                f"{path.relative_to(root)}:{line_number} has invalid open-item ID: "
                f"{cells[0] or 'missing'} (expected OI-NNN)"
            )
            continue
        identifier = cells[0]
        if identifier in seen:
            result.error(
                f"Duplicate open-item ID: {identifier} at controls/open-items.md:"
                f"{seen[identifier]} and {line_number}"
            )
        else:
            seen[identifier] = line_number
        item_type = cells[1]
        if item_type not in OPEN_ITEM_TYPES:
            result.error(
                f"{path.relative_to(root)}:{line_number} has invalid open-item type: "
                f"{item_type or 'missing'}"
            )
        priority = cells[2]
        if priority not in OPEN_ITEM_PRIORITIES:
            result.error(
                f"{path.relative_to(root)}:{line_number} has invalid open-item priority: "
                f"{priority or 'missing'}"
            )
        status = cells[-1]
        if status not in OPEN_ITEM_STATUSES:
            result.error(
                f"{path.relative_to(root)}:{line_number} has invalid open-item status: "
                f"{status or 'missing'}"
            )


def check_secrets(root: Path, result: Result) -> None:
    for path in root.rglob("*.md"):
        content = read_text(path, result)
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            result.error(f"Credential-like material found: {path.relative_to(root)}")


def check_decision_family(
    root: Path,
    family: str,
    record_prefix: str,
    reviewer_id: str,
    result: Result,
) -> None:
    folder = root / "controls" / family
    records = list((folder / record_prefix.lower()).glob(f"{record_prefix}-*.md")) if folder.is_dir() else []
    inventory = folder / f"{record_prefix.lower()}-candidate-inventory.md"
    register = folder / f"{record_prefix.lower()}-register.md"
    reviewer_completed = (root / "reviewer-reports" / reviewer_id / "report.md").is_file()
    if reviewer_completed and not inventory.is_file():
        result.error(f"Missing decision candidate inventory: {inventory.relative_to(root)}")
    if reviewer_completed and not register.is_file():
        result.error(f"Missing decision register: {register.relative_to(root)}")
    if inventory.is_file():
        check_headings(inventory, INVENTORY_HEADINGS, root, result)
    if register.is_file():
        check_headings(register, REGISTER_HEADINGS, root, result)
    seen: dict[str, Path] = {}
    for record in records:
        match = re.match(rf"{record_prefix}-(\d{{3}})(?:-|\.)", record.name)
        if not match:
            result.error(
                f"Invalid decision record filename: {record.relative_to(root)} "
                f"(expected {record_prefix}-NNN-*.md)"
            )
        else:
            identifier = f"{record_prefix}-{match.group(1)}"
            if identifier in seen:
                result.error(
                    f"Duplicate decision ID: {identifier} at "
                    f"{seen[identifier].relative_to(root)} and {record.relative_to(root)}"
                )
            else:
                seen[identifier] = record
        check_headings(record, DECISION_HEADINGS, root, result)


def check_diagrams(root: Path, result: Result) -> None:
    for path in root.glob("controls/**/diagrams/*.md"):
        check_headings(path, DIAGRAM_HEADINGS, root, result)
        content = read_text(path, result)
        for label in ("Confirmed notation:", "Inferred notation:", "Unknown notation:"):
            if label not in content:
                result.error(f"{path.relative_to(root)} missing diagram notation: {label}")


def check_evidence_packets(root: Path, result: Result) -> None:
    packets = root / "evidence" / "packets"
    if not packets.is_dir():
        return
    for path in sorted(packets.glob("*.md")):
        check_headings(path, PACKET_HEADINGS, root, result)


def check_operator_aids(root: Path, require_operationalization: bool, result: Result) -> None:
    aids = root / "operator-aids"
    paths = sorted(aids.glob("*.md")) if aids.is_dir() else []
    if require_operationalization and not paths:
        result.error("Missing required operator aids: operator-aids/")
    if require_operationalization:
        present = {path.name for path in paths}
        for aid in TRANSITION_PACKET_AIDS:
            if aid not in present:
                result.error(f"Missing required operator aid: operator-aids/{aid}")
    for path in paths:
        content = read_text(path, result)
        if not re.search(r"(?m)^- Status: (?:draft|untested|executed-successfully)$", content):
            result.error(f"{path.relative_to(root)} missing valid operator-aid status")
        check_headings(path, OPERATOR_AID_HEADINGS, root, result)


def validate(
    root: Path,
    require_final: bool = False,
    require_operationalization: bool = False,
) -> Result:
    result = Result()
    if not root.is_dir():
        result.error(f"Audit directory does not exist: {root}")
        return result
    check_required(root, BASE_REQUIRED, result)
    if require_final:
        check_required(root, FINAL_REQUIRED, result)
    check_table_contracts(root, result)
    check_id_formats(root, result)
    check_final_reports(root, result)
    check_reviewer_reports(root, result)
    check_cutoffs(root, result)
    check_open_items(root, result)
    check_secrets(root, result)
    check_decision_family(root, "architecture", "ADR", "architecture", result)
    check_decision_family(root, "product", "PDR", "product-value", result)
    check_diagrams(root, result)
    check_evidence_packets(root, result)
    check_operator_aids(root, require_operationalization, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_directory", type=Path)
    parser.add_argument("--require-final", action="store_true")
    parser.add_argument("--require-operationalization", action="store_true")
    args = parser.parse_args()
    result = validate(
        args.audit_directory,
        args.require_final,
        args.require_operationalization,
    )
    for message in result.errors:
        print(f"ERROR: {message}")
    for message in result.warnings:
        print(f"WARNING: {message}")
    print(f"{len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
