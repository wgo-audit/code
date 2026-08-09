from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "skills/wgo/scripts/validate_audit_structure.py"
SPEC = importlib.util.spec_from_file_location("validate_audit_structure", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class ValidateAuditStructureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "_whats-going-on-20260712"
        self.root.mkdir()
        self.write("audit-brief.md")
        self.write(
            "manifest.json",
            '{\n'
            '  "schemaVersion": "1.0.0",\n'
            '  "report": {\n'
            '    "id": "acme-2026-07-12-transition-control",\n'
            '    "title": "Acme Transition Control Audit",\n'
            '    "generatedAt": null,\n'
            '    "language": "en",\n'
            '    "entrypoint": "index.md"\n'
            '  },\n'
            '  "subject": {\n'
            '    "id": "acme",\n'
            '    "name": "Acme",\n'
            '    "kind": "software-project"\n'
            '  },\n'
            '  "audit": {\n'
            '    "type": "transition-control",\n'
            '    "mode": "unknown",\n'
            '    "depth": "deep"\n'
            '  },\n'
            '  "evidence": {\n'
            '    "cutoff": "2026-07-12",\n'
            '    "sources": [],\n'
            '    "accessBoundary": { "level": "unknown" },\n'
            '    "limitations": []\n'
            '  },\n'
            '  "execution": {\n'
            '    "generator": {\n'
            '      "name": "wgo-audit",\n'
            '      "repository": "wgo-audit/code",\n'
            '      "version": null,\n'
            '      "commit": null\n'
            '    },\n'
            '    "reviewers": []\n'
            '  },\n'
            '  "results": {\n'
            '    "headline": null,\n'
            '    "conclusions": []\n'
            '  },\n'
            '  "relationships": {\n'
            '    "baseline": null,\n'
            '    "previousAudit": null,\n'
            '    "comparesTo": [],\n'
            '    "supersedes": null\n'
            '  }\n'
            '}\n',
        )
        self.write(
            "audit-checklist.md",
            "# Audit Checklist\n\n"
            "| Work item | State | Next action | Recommended next reviewer | Factual completion condition |\n"
            "|---|---|---|---|---|\n"
            "| Onboarding | confirmed | | architecture | Brief confirmed |\n",
        )
        self.write(
            "evidence/evidence-ledger.md",
            "# Evidence Ledger\n\n"
            "| Evidence ID | Source type | Exact locator | Observed/effective time | Cutoff eligibility | Factual summary | Limitation | Sensitivity |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| E-001 | repo | src/app.py:1 | 2026-07-12 | within-cutoff | App exists | source only | internal |\n",
        )
        self.write(
            "evidence/source-access-register.md",
            "# Source Access Register\n\n"
            "| Source | Attempt/time | Result or limitation | Question affected | Material impact | Approved fallback/exclusion | Owner and next step |\n"
            "|---|---|---|---|---|---|---|\n",
        )
        self.write(
            "controls/open-items.md",
            "# Open Items\n\n"
            "| ID | Type | Priority | Item and consequence | Evidence/artifact links | Owner | Closure route | Status |\n"
            "|---|---|---|---|---|---|---|---|\n",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, content: str = "# Artifact\n") -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_reviewer(self) -> None:
        self.write("reviewer-reports/architecture/report.md", "# Architecture\n\n" + "\n\n".join(validator.REVIEWER_HEADINGS))
        self.write("reviewer-reports/architecture/handoff.md", "# Architecture Handoff\n\n" + "\n\n".join(validator.HANDOFF_HEADINGS))
        self.inventory("architecture")

    def inventory(self, kind: str) -> None:
        folder, prefix, candidate = ("architecture", "ADR", "ARCH-DC-001") if kind == "architecture" else ("product", "PDR", "PROD-DC-001")
        lower = prefix.lower()
        self.write(f"controls/{folder}/{lower}-candidate-inventory.md", "# Inventory\n\n" + "\n\n".join(validator.INVENTORY_HEADINGS) + f"\n\n| {candidate} | | | | | | |\n")
        self.write(f"controls/{folder}/{lower}-register.md", "# Register\n\n" + "\n\n".join(validator.REGISTER_HEADINGS))

    def test_valid_lean_fixture(self) -> None:
        self.write_reviewer()
        result = validator.validate(self.root)
        self.assertEqual([], result.errors)

    def test_missing_lean_administration_is_an_error(self) -> None:
        (self.root / "audit-brief.md").unlink()
        result = validator.validate(self.root)
        self.assertIn("Missing required file: audit-brief.md", result.errors)

    def test_manifest_contract_is_enforced(self) -> None:
        self.write(
            "manifest.json",
            '{\n'
            '  "schemaVersion": "1.0.0",\n'
            '  "asset": "legacy",\n'
            '  "report": { "entrypoint": "missing.md" },\n'
            '  "subject": {},\n'
            '  "audit": {},\n'
            '  "evidence": {\n'
            '    "sources": [\n'
            '      { "kind": "git-repository", "commit": "abc123" }\n'
            '    ]\n'
            '  },\n'
            '  "execution": {\n'
            '    "reviewers": [\n'
            '      { "id": "architecture", "version": null, "status": "done" }\n'
            '    ]\n'
            '  },\n'
            '  "results": {\n'
            '    "conclusions": [\n'
            '      { "id": "same", "confidence": "certain", "severity": "urgent" },\n'
            '      { "id": "same" }\n'
            '    ]\n'
            '  },\n'
            '  "relationships": { "baseline": "TODO" }\n'
            '}\n',
        )
        self.write("index.md")

        errors = validator.validate(self.root).errors
        self.assertTrue(any("unknown top-level keys: asset" in error for error in errors))
        self.assertTrue(any("unresolved TODO/TBD placeholder" in error for error in errors))
        self.assertTrue(any("commit must be a full Git SHA" in error for error in errors))
        self.assertTrue(any("status is invalid: done" in error for error in errors))
        self.assertTrue(any("duplicate conclusion id: same" in error for error in errors))
        self.assertTrue(any("confidence is invalid: certain" in error for error in errors))
        self.assertTrue(any("severity is invalid: urgent" in error for error in errors))

    def test_old_status_file_is_not_required(self) -> None:
        self.write_reviewer()
        result = validator.validate(self.root)
        self.assertFalse(any("audit-status" in error for error in result.errors))

    def test_reviewer_headings_are_checked(self) -> None:
        self.write("reviewer-reports/architecture/report.md", "# Architecture\n")
        result = validator.validate(self.root)
        self.assertTrue(any("missing required heading" in error for error in result.errors))

    def test_legacy_stakeholder_question_heading_remains_resumable(self) -> None:
        self.write_reviewer()
        path = self.root / "reviewer-reports/architecture/report.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                validator.REVIEWER_QUESTION_HEADINGS[0],
                validator.REVIEWER_QUESTION_HEADINGS[1],
            ),
            encoding="utf-8",
        )
        self.assertEqual([], validator.validate(self.root).errors)

    def test_reviewer_handoff_is_required(self) -> None:
        self.write_reviewer()
        (self.root / "reviewer-reports/architecture/handoff.md").unlink()
        result = validator.validate(self.root)
        self.assertTrue(any("Missing reviewer handoff" in error for error in result.errors))

    def test_cutoff_and_secret_checks_remain(self) -> None:
        self.write(
            "evidence/evidence-ledger.md",
            "# Evidence Ledger\n\n"
            "| Evidence ID | Source type | Exact locator | Observed/effective time | Cutoff eligibility | Factual summary | Limitation | Sensitivity |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| E-001 | source | repo:file | 2026-07-12 | Eligible | Fact | limit | internal |\n",
        )
        self.write("reviewer-reports/architecture/report.md", "-----BEGIN PRIVATE KEY-----\n")
        result = validator.validate(self.root)
        self.assertTrue(any("invalid cutoff eligibility" in error for error in result.errors))
        self.assertTrue(any("within-cutoff" in error for error in result.errors))
        self.assertTrue(any("Credential-like" in error for error in result.errors))

    def test_open_item_ids_and_dispositions_are_durable(self) -> None:
        self.write(
            "controls/open-items.md",
            "# Open Items\n\n"
            "| ID | Type | Priority | Item and consequence | Evidence/artifact links | Owner | Closure route | Status |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| OI-001 | verification | P2 | Check deployment | E-001 | Owner | Verify | open |\n",
        )
        self.assertEqual([], validator.validate(self.root).errors)

        self.write(
            "controls/open-items.md",
            "# Open Items\n\n"
            "| ID | Type | Priority | Item and consequence | Evidence/artifact links | Owner | Closure route | Status |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| OI-001 | verification | P2 | Check deployment | E-001 | Owner | Verify | open |\n"
            "| OI-001 | action | P2 | Different subject | E-001 | Owner | Fix | verified-fixed |\n"
            "| OI-002 | action | P2 | Bad status | E-001 | Owner | Fix | done |\n",
        )
        errors = validator.validate(self.root).errors
        self.assertTrue(any("Duplicate open-item ID: OI-001" in error for error in errors))
        self.assertTrue(any("invalid open-item status: done" in error for error in errors))

    def test_stable_id_format_is_enforced(self) -> None:
        self.write(
            "audit-brief.md",
            "# Audit Brief\n\nBad evidence link E-12. E-Commerce is ordinary text.\n",
        )
        errors = validator.validate(self.root).errors
        self.assertTrue(any("invalid stable ID: E-12" in error for error in errors))
        self.assertFalse(any("E-Commerce" in error for error in errors))

    def test_core_table_schemas_and_controlled_values_are_enforced(self) -> None:
        self.write(
            "audit-checklist.md",
            "# Audit Checklist\n\n"
            "| Work item | State | Next action | Recommended next reviewer | Factual completion condition |\n"
            "|---|---|---|---|---|\n"
            "| Architecture | done | | | Report exists |\n"
            "| Broken | row |\n",
        )
        self.write(
            "documentation/catalog.md",
            "# Documentation Catalog\n\n| Document | Summary |\n|---|---|\n",
        )
        errors = validator.validate(self.root).errors
        self.assertTrue(any("invalid checklist state: done" in error for error in errors))
        self.assertTrue(any("has 2 table cells; expected 5" in error for error in errors))
        self.assertTrue(any("documentation/catalog.md missing required table schema" in error for error in errors))

    def test_open_item_type_and_priority_are_enforced(self) -> None:
        self.write(
            "controls/open-items.md",
            "# Open Items\n\n"
            "| ID | Type | Priority | Item and consequence | Evidence/artifact links | Owner | Closure route | Status |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| OI-001 | question | urgent | Decide | E-001 | Owner | Ask | open |\n",
        )
        errors = validator.validate(self.root).errors
        self.assertTrue(any("invalid open-item type: question" in error for error in errors))
        self.assertTrue(any("invalid open-item priority: urgent" in error for error in errors))

    def test_decision_ids_are_unique_within_their_family(self) -> None:
        self.write_reviewer()
        self.inventory("architecture")
        headings = "\n\n".join(validator.DECISION_HEADINGS)
        self.write("controls/architecture/adr/ADR-001-one.md", f"# ADR\n\n{headings}")
        self.write("controls/architecture/adr/ADR-001-two.md", f"# ADR\n\n{headings}")
        result = validator.validate(self.root)
        self.assertTrue(any("Duplicate decision ID: ADR-001" in error for error in result.errors))

    def test_decision_record_requires_inventory_and_register(self) -> None:
        self.write_reviewer()
        (self.root / "controls/architecture/adr-candidate-inventory.md").unlink()
        (self.root / "controls/architecture/adr-register.md").unlink()
        self.write("controls/architecture/adr/ADR-001-example.md", "# ADR\n\n" + "\n\n".join(validator.DECISION_HEADINGS))
        result = validator.validate(self.root)
        self.assertTrue(any("candidate inventory" in error for error in result.errors))
        self.assertTrue(any("decision register" in error for error in result.errors))

    def test_completed_decision_reviewer_requires_empty_inventory_and_register(self) -> None:
        self.write_reviewer()
        (self.root / "controls/architecture/adr-candidate-inventory.md").unlink()
        (self.root / "controls/architecture/adr-register.md").unlink()
        result = validator.validate(self.root)
        self.assertTrue(any("candidate inventory" in error for error in result.errors))
        self.assertTrue(any("decision register" in error for error in result.errors))

    def test_unknown_runtime_does_not_reject_complete_source_bounded_output(self) -> None:
        self.write_reviewer()
        self.inventory("architecture")
        self.write("controls/architecture/adr/ADR-001-example.md", "# ADR\n\n" + "\n\n".join(validator.DECISION_HEADINGS) + "\n\n| Runtime/live state | unknown | E-001 | No authorized observation |\n")
        self.write("controls/architecture/diagrams/context.md", "# Context\n\n" + "\n\n".join(validator.DIAGRAM_HEADINGS) + "\n\nConfirmed notation:\nInferred notation:\nUnknown notation:\n")
        result = validator.validate(self.root)
        self.assertEqual([], result.errors)

    def test_evidence_packet_requires_the_packet_contract(self) -> None:
        self.write_reviewer()
        self.write("evidence/packets/golden-path-observation.md", "# Packet\n")
        result = validator.validate(self.root)
        self.assertTrue(any("golden-path-observation.md missing required heading" in error for error in result.errors))
        self.write(
            "evidence/packets/golden-path-observation.md",
            "# Packet\n\n" + "\n\n".join(validator.PACKET_HEADINGS),
        )
        self.assertEqual([], validator.validate(self.root).errors)

    def test_operator_aid_is_checked_only_when_required(self) -> None:
        self.write_reviewer()
        result = validator.validate(self.root, require_operationalization=True)
        self.assertTrue(any("Missing required operator aids" in error for error in result.errors))

        self.write("operator-aids/demo.md", "# Demo\n\n- Status: complete\n")
        result = validator.validate(self.root, require_operationalization=True)
        self.assertTrue(any("missing valid operator-aid status" in error for error in result.errors))

        self.write(
            "operator-aids/demo.md",
            "# Demo\n\n- Status: untested\n\n" + "\n\n".join(validator.OPERATOR_AID_HEADINGS),
        )
        self.assertEqual([], validator.validate(self.root).errors)
        result = validator.validate(self.root, require_operationalization=True)
        self.assertTrue(any("replacement-maintainer.md" in error for error in result.errors))
        for aid in validator.TRANSITION_PACKET_AIDS:
            self.write(
                f"operator-aids/{aid}",
                f"# {aid}\n\n- Status: untested\n\n" + "\n\n".join(validator.OPERATOR_AID_HEADINGS),
            )
        self.assertEqual([], validator.validate(self.root, require_operationalization=True).errors)
        with mock.patch.object(
            sys,
            "argv",
            ["validator", str(self.root), "--require-operationalization"],
        ):
            self.assertEqual(0, validator.main())

    def test_operationalization_requires_the_complete_operator_packet(self) -> None:
        self.write_reviewer()
        self.write(
            "operator-aids/recovery.md",
            "# Recovery\n\n- Status: untested\n\n" + "\n\n".join(validator.OPERATOR_AID_HEADINGS),
        )
        result = validator.validate(self.root, require_operationalization=True)
        self.assertTrue(any("replacement-maintainer.md" in error for error in result.errors))
        for aid in validator.TRANSITION_PACKET_AIDS:
            self.write(
                f"operator-aids/{aid}",
                f"# {aid}\n\n- Status: untested\n\n" + "\n\n".join(validator.OPERATOR_AID_HEADINGS),
            )
        self.assertEqual(
            [],
            validator.validate(self.root, require_operationalization=True).errors,
        )

    def test_final_and_cli_exit_status(self) -> None:
        self.write_reviewer()
        for relative in validator.FINAL_REQUIRED:
            self.write(
                relative,
                f"# {relative}\n\n" + "\n\n".join(validator.FINAL_HEADINGS[relative]),
            )
        self.assertEqual([], validator.validate(self.root, require_final=True).errors)
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["validator", str(self.root)]):
            with redirect_stdout(output):
                self.assertEqual(0, validator.main())
        self.assertIn("0 error(s)", output.getvalue())
        with mock.patch.object(sys, "argv", ["validator", str(self.root), "--mode", "assessment"]):
            with redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    validator.main()

    def test_existing_final_report_sections_are_enforced(self) -> None:
        self.write("index.md", "# Audit Index\n")
        errors = validator.validate(self.root).errors
        self.assertTrue(any("index.md missing required heading" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
