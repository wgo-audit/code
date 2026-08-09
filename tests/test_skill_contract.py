from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills/wgo"
REVIEWERS = SKILL / "references/reviewers"
EXPECTED_REVIEWERS = {
    "architecture", "business-continuity", "code-quality",
    "contributor-vendor-value", "expense-exposure", "maintenance-cost",
    "product-value", "project-health", "revenue-risk", "scalability",
    "security-privacy",
}
EXPECTED_REVIEWER_VERSIONS = {
    "security-privacy": "0.2",
}


def reviewer_card(reviewer_id: str) -> Path:
    return REVIEWERS / reviewer_id / "reviewer.md"


def frontmatter_dependencies(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    dependencies: list[str] = []
    in_dependencies = False
    for line in lines[1:]:
        if line == "---":
            break
        if line == "depends_on: []":
            return []
        if line == "depends_on:":
            in_dependencies = True
            continue
        if in_dependencies:
            match = re.fullmatch(r"  - ([a-z0-9-]+)", line)
            if match:
                dependencies.append(match.group(1))
                continue
            break
    return dependencies


class SkillContractTests(unittest.TestCase):
    def test_skill_routes_a_lean_layout(self) -> None:
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(content.splitlines()), 180)
        for path in (
            "audit-brief.md", "audit-checklist.md", "manifest.json", "reviewer-reports/<reviewer-id>/",
            "evidence-ledger.md", "source-access-register.md", "open-items.md",
        ):
            self.assertIn(path, content)
        self.assertIn("handoff.md", content)
        for path in (
            "index.md", "executive-summary.md", "product-manager-notes.md",
            "technical-lead-notes.md",
        ):
            self.assertIn(path, content)
        self.assertNotIn("  final/", content)
        self.assertNotIn("reviewer-summaries.md", content)
        for rejected in ("audit-status.md", "claims.md", "collection-log.md", "risk-register.md"):
            self.assertNotIn(rejected, content)

    def test_every_reviewer_has_a_compact_output_menu(self) -> None:
        files = {path.parent.name: path for path in REVIEWERS.glob("*/reviewer.md")}
        self.assertEqual(EXPECTED_REVIEWERS, set(files))
        for reviewer_id, path in files.items():
            content = path.read_text(encoding="utf-8")
            self.assertRegex(content, rf"(?m)^id: {re.escape(reviewer_id)}$")
            expected_version = EXPECTED_REVIEWER_VERSIONS.get(reviewer_id, "0.1")
            self.assertRegex(content, rf"(?m)^version: {re.escape(expected_version)}$")
            self.assertRegex(content, r"(?m)^codegraph: (?:none|optional|required)$")
            dependencies = set(frontmatter_dependencies(path))
            self.assertLessEqual(dependencies, EXPECTED_REVIEWERS)
            self.assertNotIn(reviewer_id, dependencies)
            if dependencies:
                self.assertRegex(content, r"(?m)^depends_on:$")
            else:
                self.assertNotIn("depends_on:", content)
            for heading in (
                "## Objective And Business Questions", "## Output Menu",
                "## Recommended Inputs And Downstream Use", "## Completion Criteria",
                "## Escalation Conditions", "## Cross-Reviewer Links",
            ):
                self.assertIn(heading, content, f"{reviewer_id} lacks {heading}")
            self.assertIn("Required", content)
            self.assertIn("Conditional", content)
            self.assertIn("Not owned", content)

    def test_checklist_is_the_single_work_view(self) -> None:
        command = (ROOT / "commands/status.md").read_text(encoding="utf-8")
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        self.assertIn("only work/status view", command)
        self.assertIn("Do not create claims, collection logs, per-type control registers, status", onboarding)
        self.assertIn("additional manifests", onboarding)
        self.assertIn("canonical\n`manifest.json` is part of the lean start", onboarding)

    def test_onboarding_collects_evidence_sources_and_code_repositories(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        normalized_onboarding = " ".join(onboarding.split())
        command = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")
        templates = (SKILL / "references/templates/control-templates.md").read_text(encoding="utf-8")

        for phrase in (
            "every additional evidence or documentation source",
            "one path or URL per line",
            "fast, repeatable cross-document search and exact evidence citations",
            "Prefer Markdown, plain text, HTML, CSV, JSON, or YAML.",
            "Shift+Enter to add another source",
        ):
            self.assertIn(phrase, normalized_onboarding)
        for phrase in (
            "Ask one question at a time and wait",
            "Do not bundle the mandate, business decision, concerns, and harmful failure mode.",
            "current folder has no Git root",
            "Clone the accessible ref immediately",
            "other code repositories support the product",
            "Do not ask this question for a confirmed monorepo.",
            "documentation/tmp/<repository-name>/",
            "wgo-code-repositories/<audit-id>/<repository-name>/",
        ):
            self.assertIn(phrase, normalized_onboarding)
        self.assertIn(
            "onboarding asks each intake question separately and waits for its answer",
            " ".join(command.split()),
        )
        self.assertIn("Evidence and documentation sources", templates)
        self.assertIn("Supporting code repositories", templates)
        self.assertIn("## Audit Manifest", templates)
        self.assertIn('"schemaVersion": "1.0.0"', templates)
        self.assertIn('"subject"', templates)
        self.assertIn('"relationships"', templates)
        self.assertIn("Do not carry legacy\nfields", templates)
        self.assertIn("manifest.json", onboarding)
        self.assertIn("machine-readable report contract", onboarding)
        self.assertLess(
            onboarding.index("other code repositories support the product"),
            onboarding.index("Ask for every additional evidence or documentation source"),
        )
        self.assertLess(
            onboarding.index("Ask for every additional evidence or documentation source"),
            onboarding.index("Ask for the audit mandate."),
        )

    def test_onboarding_keeps_internal_defaults_out_of_auditor_questions(self) -> None:
        onboarding = " ".join((SKILL / "references/common/onboarding.md").read_text(encoding="utf-8").split())
        command = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")

        self.assertIn("always detailed and covers the whole folder", onboarding)
        self.assertIn("Do not discuss packets with the auditor", onboarding)
        self.assertIn("Do not ask for or offer a reviewer order", onboarding)
        self.assertIn("public data and any private data available through the existing GitHub session", onboarding)
        self.assertNotIn("approved depth", onboarding)
        self.assertIn("WGO owns shared collection and dependency waves", " ".join(command.split()))

    def test_codegraph_is_initialized_per_git_root_with_explicit_paths(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        reviewer = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        blueprint = (SKILL / "references/common/reviewer-blueprint.md").read_text(encoding="utf-8")

        self.assertIn("distinct Git roots", onboarding)
        self.assertIn("monorepo", onboarding)
        self.assertIn("codegraph init <absolute-root>", onboarding)
        self.assertIn("--path\n<absolute-root>", reviewer)
        self.assertIn("Never rely on the current working directory", reviewer)
        self.assertIn("Workers never invoke CodeGraph", blueprint)

    def test_github_repository_context_is_automatic_read_only_evidence(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        evidence = (SKILL / "references/common/evidence-rules.md").read_text(encoding="utf-8")
        collector = (SKILL / "references/collectors/github-history-and-hosted-ci.md").read_text(encoding="utf-8")
        command = (ROOT / "commands/audit.md").read_text(encoding="utf-8")
        templates = (SKILL / "references/templates/control-templates.md").read_text(encoding="utf-8")
        normalized_onboarding = " ".join(onboarding.split())

        for content in (onboarding, evidence, collector, command):
            self.assertIn("GitHub", content)
        self.assertIn("Do not ask for consent", normalized_onboarding)
        self.assertIn("automatically authorizes read-only use", evidence)
        self.assertIn("Every GitHub code repository URL", evidence)
        self.assertIn("PRs, issues, Projects, Actions, releases, and history", collector)
        self.assertIn("create or refresh\n   `github-history-and-hosted-ci.md` before reviewing", command)
        self.assertIn("Automatic GitHub code repository sources", templates)

    def test_documentation_preparation_is_one_delegated_worker(self) -> None:
        preparation = (SKILL / "references/common/documentation-prep.md").read_text(encoding="utf-8")
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        reviewer = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("documentation/catalog.md", preparation)
        self.assertIn("it does not audit the documents", preparation)
        self.assertIn(
            "ask the auditor questions, clone repositories, set scope, or select reviewers",
            " ".join(preparation.split()),
        )
        self.assertIn("Do not delegate further workers", " ".join(preparation.split()))
        self.assertIn("Summary (target 75–100 words; max 120)", preparation)
        self.assertIn("75–100 words and must not exceed 120", preparation)
        self.assertIn("not audit evidence", preparation)
        self.assertIn("CodeGraph is never used for documents", " ".join(preparation.split()))
        self.assertIn("delegate exactly one documentation-preparation worker", onboarding)
        self.assertIn("clone each supplied GitHub evidence/documentation repository", onboarding)
        self.assertIn("onboarding lead does\n  not read that instruction file", skill)
        self.assertIn("search it by the current reviewer ID", reviewer)

    def test_documentation_preparation_flags_material_missing_content(self) -> None:
        preparation = (SKILL / "references/common/documentation-prep.md").read_text(encoding="utf-8")
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        reviewer = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        command = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")
        normalized_preparation = " ".join(preparation.split())
        normalized_onboarding = " ".join(onboarding.split())

        for phrase in (
            "Two Passes, One Worker",
            "Freeze the factual classification, reviewer routing, summary, and limits before the second pass.",
            "Referenced Content Outside The Corpus",
            "Documentation Coverage Signals",
            "repository URL/ref/ resolved commit/local-root mappings",
            "map the repository and path to its prepared local clone",
            "ignore page navigation, same-page anchors, assets, scripts, styles, fonts",
            "resolved-in-corpus",
            "referenced-outside-corpus",
            "not-found-in-corpus",
            "same worker and model",
            "preserve unchanged IDs and first-pass rows",
        ):
            self.assertIn(phrase, normalized_preparation)
        self.assertIn("documentation-bearing paths in every audited code root", normalized_onboarding)
        self.assertIn("read only the material rows", normalized_onboarding)
        self.assertIn(
            "I found potentially material content that is missing from or unresolved in the available corpus. "
            "Would you like to add any sources before I start the audit?",
            normalized_onboarding,
        )
        self.assertIn("ask in the next turn for one local path or GitHub URL/ref per line", normalized_onboarding)
        self.assertIn("continue the same documentation worker with the same model", normalized_onboarding)
        self.assertIn("navigation metadata, not evidence", normalized_preparation)
        self.assertIn("not proof or an automatic finding", " ".join(reviewer.split()))
        self.assertIn("If it flags material missing or unresolved content", command)

    def test_documentation_catalog_uses_only_the_active_audit_platform(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        preparation = (SKILL / "references/common/documentation-prep.md").read_text(encoding="utf-8")
        command = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        for content in (onboarding, preparation):
            self.assertIn("gpt-5.6-luna", content)
            self.assertIn("Sonnet 5", content)
            self.assertIn("gemini-3.5-flash-lite", content)
            self.assertIn("active audit model", content)
        self.assertIn("Do not request, configure, or use another provider's credentials or API.", onboarding)
        self.assertIn("Do\nnot request, configure, or call another provider.", preparation)
        self.assertIn("Use the supplied model consistently for the full catalog run", preparation)
        self.assertIn(
            "never request or use another provider's credentials",
            " ".join(command.split()),
        )
        self.assertIn(
            "active audit platform, and chosen same-platform catalog model",
            " ".join(skill.split()),
        )

    def test_audit_without_a_reviewer_runs_the_resolved_dependency_graph(self) -> None:
        command = (ROOT / "commands/audit.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('args: "[reviewer-id|all]"', command)
        self.assertIn("## All Selected Reviewers", command)
        self.assertIn("resolved dependency graph", command)
        self.assertIn("currently unblocked reviewer in parallel", command)
        self.assertIn("superseded core ID resolves to its\napproved replacement", command)
        self.assertNotIn("| 1 | Architecture |", command)
        self.assertIn("serializes updates to the shared evidence ledger", command)
        self.assertIn("wgo:audit [reviewer-id|all]", skill)
        self.assertIn("automatically run `wgo:summarize`", command)

    def test_core_reviewer_dependencies_preserve_the_five_execution_waves(self) -> None:
        remaining = {
            reviewer_id: set(frontmatter_dependencies(reviewer_card(reviewer_id)))
            for reviewer_id in EXPECTED_REVIEWERS
        }
        waves: list[set[str]] = []
        completed: set[str] = set()
        while remaining:
            wave = {
                reviewer_id
                for reviewer_id, dependencies in remaining.items()
                if dependencies <= completed
            }
            self.assertTrue(wave, "reviewer dependency graph contains a cycle")
            waves.append(wave)
            completed |= wave
            for reviewer_id in wave:
                del remaining[reviewer_id]

        self.assertEqual(
            [
                {"architecture"},
                {"product-value", "security-privacy", "code-quality"},
                {"business-continuity", "expense-exposure", "scalability"},
                {"revenue-risk", "maintenance-cost", "contributor-vendor-value"},
                {"project-health"},
            ],
            waves,
        )

    def test_reviewer_inputs_use_only_declared_predecessors(self) -> None:
        contract = (
            SKILL / "references/common/reviewer-contract.md"
        ).read_text(encoding="utf-8")
        blueprint = (
            SKILL / "references/common/reviewer-blueprint.md"
        ).read_text(encoding="utf-8")
        authoring = (
            SKILL / "references/common/reviewer-authoring.md"
        ).read_text(encoding="utf-8")

        for reviewer_id in EXPECTED_REVIEWERS:
            card = reviewer_card(reviewer_id).read_text(encoding="utf-8")
            section = card.split("## Recommended Inputs And Downstream Use", 1)[1].split(
                "\n## ", 1
            )[0]
            self.assertIn(
                "only completed `depends_on` handoffs",
                " ".join(section.split()),
            )
        self.assertIn("This reviewer has no predecessor", reviewer_card("architecture").read_text(encoding="utf-8"))
        for content in (contract, blueprint, authoring):
            self.assertRegex(content.lower(), r"same-wave (?:or|and) later reviewer")

    def test_each_reviewer_owns_one_control_namespace(self) -> None:
        for reviewer_id in EXPECTED_REVIEWERS:
            content = reviewer_card(reviewer_id).read_text(encoding="utf-8")
            output_menu = content.split("## Output Menu", 1)[1].split("\n## ", 1)[0]
            roots = set(re.findall(r"`controls/([^/`]+)/", output_menu))
            self.assertLessEqual(len(roots), 1, f"{reviewer_id} uses {sorted(roots)}")

        contract = (
            SKILL / "references/common/reviewer-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("exactly one `controls/<namespace>/`", contract)
        continuity = reviewer_card("business-continuity").read_text(encoding="utf-8")
        self.assertNotIn("controls/business-continuity/", continuity)

    def test_audit_flow_confirms_then_summarizes_then_confirms_operationalization(self) -> None:
        onboard = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        audit = (ROOT / "commands/audit.md").read_text(encoding="utf-8")
        summary = (ROOT / "commands/summarize.md").read_text(encoding="utf-8")
        synthesis = (SKILL / "references/common/synthesis.md").read_text(encoding="utf-8")

        for content in (onboard, onboarding):
            self.assertIn("Should I proceed with wgo:audit all?", content)
        self.assertIn("With `all` or no parameter", audit)
        self.assertNotIn("| 6 | Synthesis |", audit)
        self.assertIn("Should I proceed with\nwgo:operationalize?", summary)
        self.assertIn("Should I proceed with wgo:operationalize?", synthesis)

    def test_architecture_and_product_require_decision_inventory_and_register(self) -> None:
        architecture = reviewer_card("architecture").read_text(encoding="utf-8")
        product = reviewer_card("product-value").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("adr-candidate-inventory.md", architecture)
        self.assertIn("adr-register.md", architecture)
        self.assertIn("pdr-candidate-inventory.md", product)
        self.assertIn("pdr-register.md", product)
        self.assertIn("record-created", architecture)
        self.assertIn("record-created", product)
        self.assertIn("../../templates/detailed-artifact-templates.md", architecture)
        self.assertIn("../../templates/detailed-artifact-templates.md", product)
        self.assertIn("references/templates/detailed-artifact-templates.md", skill)

    def test_selected_templates_are_self_directing(self) -> None:
        content = (SKILL / "references/templates/detailed-artifact-templates.md").read_text(encoding="utf-8")
        for phrase in ("Use when:", "Reader question:", "Create from:", "Do not infer:", "Minimum completion:", "If unknown:"):
            self.assertGreaterEqual(content.count(phrase), 3)
        self.assertIn("## Evidence Dimensions Used", content)

        packet = (SKILL / "references/templates/evidence-packet-template.md").read_text(encoding="utf-8")
        for heading in (
            "## Scope And Evidence Boundary", "## Observations",
            "## Material Unknowns And Access Limits", "## Reuse Guidance",
        ):
            self.assertIn(heading, packet)

    def test_manifest_is_a_validated_report_contract(self) -> None:
        validator = (SKILL / "scripts/validate_audit_structure.py").read_text(encoding="utf-8")
        synthesis = (SKILL / "references/common/synthesis.md").read_text(encoding="utf-8")
        templates = (SKILL / "references/templates/control-templates.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        normalized_synthesis = " ".join(synthesis.split())
        normalized_templates = " ".join(templates.split())

        self.assertIn('"manifest.json"', validator)
        self.assertIn("MANIFEST_TOP_LEVEL", validator)
        self.assertIn("FULL_SHA_PATTERN", validator)
        self.assertIn("duplicate conclusion id", validator)
        self.assertIn("execution.reviewers", validator)
        self.assertIn("Update `manifest.json` after the four audience reports", synthesis)
        self.assertIn("Do not invent generator commits, reviewer versions", normalized_synthesis)
        self.assertIn("schemaVersion`, `report`, `subject`, `audit`", normalized_templates)
        self.assertIn("subject.id` is the eventual `audits/<subject>/`", templates)
        self.assertIn("Every Git source commit must be a full 40-character SHA", templates)
        self.assertIn("Machine-readable identity, provenance, evidence boundary", readme)

    def test_source_bounded_diagrams_are_explicit(self) -> None:
        template = (SKILL / "references/templates/detailed-artifact-templates.md").read_text(encoding="utf-8")
        self.assertIn("Source/configuration evidence", template)
        for label in ("Confirmed notation:", "Inferred notation:", "Unknown notation:"):
            self.assertIn(label, template)

    def test_horizontal_diagrams_use_readable_staged_layouts(self) -> None:
        workflow = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        template = (SKILL / "references/templates/detailed-artifact-templates.md").read_text(encoding="utf-8")
        quality = (SKILL / "references/common/artifact-quality-review.md").read_text(encoding="utf-8")

        self.assertIn("compact `direction LR` stage subgraphs", workflow)
        self.assertIn("Connect stage boundaries", workflow)
        self.assertIn("never use a bare `flowchart LR`", workflow)
        self.assertIn("flowchart TB", template)
        self.assertIn("connect the stage boundaries", template)
        self.assertIn("viewport shrinking", quality)
        self.assertIn("exact\ncross-stage node links", quality)

    def test_detailed_reviews_default_to_useful_source_bounded_diagrams_and_quality_review(self) -> None:
        workflow = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        quality = (SKILL / "references/common/artifact-quality-review.md").read_text(encoding="utf-8")
        command = (ROOT / "commands/audit.md").read_text(encoding="utf-8")
        architecture = reviewer_card("architecture").read_text(encoding="utf-8")
        product = reviewer_card("product-value").read_text(encoding="utf-8")

        self.assertIn("Missing live evidence is not a reason to omit it", workflow)
        self.assertIn("delegate one bounded quality worker", workflow)
        self.assertIn("The reviewer does not read the worker rubric", workflow)
        self.assertIn("ephemeral artifact-quality review", command)
        self.assertIn("returns concrete edits", quality)
        self.assertIn("shared audit state", quality)
        self.assertIn("decorative box-and-arrow prose", quality)
        self.assertIn("Do not merge unrelated reader", architecture)
        self.assertIn("Missing demonstration evidence", product)

    def test_reviewer_context_routes_only_role_relevant_shared_files(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        reviewer_route = skill.split("- Reviewer audit:", 1)[1].split(
            "- Reviewer design:", 1
        )[0]
        synthesis_route = skill.split("- Synthesis:", 1)[1].split(
            "- Operationalize:", 1
        )[0]
        reviewer_template = (
            SKILL / "references/templates/reviewer-report-template.md"
        ).read_text(encoding="utf-8")
        synthesis_templates = (
            SKILL / "references/templates/report-templates.md"
        ).read_text(encoding="utf-8")
        evidence = (
            SKILL / "references/common/evidence-rules.md"
        ).read_text(encoding="utf-8")

        self.assertIn("reviewer-report-template.md", reviewer_route)
        self.assertNotIn("references/common/reconciliation.md", reviewer_route)
        self.assertNotIn("references/templates/report-templates.md", reviewer_route)
        self.assertIn("reviewer does not read\n  that worker rubric", reviewer_route)
        self.assertIn("references/common/reconciliation.md", synthesis_route)
        self.assertIn("references/templates/report-templates.md", synthesis_route)

        self.assertIn("# Reviewer Report Template", reviewer_template)
        self.assertNotIn("## Executive Summary", reviewer_template)
        self.assertNotIn("## Reviewer Report", synthesis_templates)
        self.assertIn("## Executive Summary", synthesis_templates)

        self.assertIn("summaries and handoffs are navigation,\nnot proof", evidence)
        self.assertIn("State when no material conflict was found", evidence)
        self.assertIn(
            "preserve post-cutoff and inaccessible-evidence limits",
            " ".join(evidence.split()),
        )

    def test_decision_insights_are_qualitative_not_a_quota(self) -> None:
        reviewer = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        quality = (SKILL / "references/common/artifact-quality-review.md").read_text(encoding="utf-8")
        synthesis = (SKILL / "references/common/synthesis.md").read_text(encoding="utf-8")
        normalized_synthesis = " ".join(synthesis.split())
        reviewer_template = (
            SKILL / "references/templates/reviewer-report-template.md"
        ).read_text(encoding="utf-8")
        synthesis_templates = (
            SKILL / "references/templates/report-templates.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Derive zero or more decision insights", reviewer)
        self.assertIn("Do not create an insight to fill a count", reviewer)
        self.assertIn("Do not require or cap candidates", quality)
        self.assertIn("Do not set a target number", normalized_synthesis)
        self.assertIn("### Decision Insights", reviewer_template)
        self.assertIn("### Decision-Useful Conclusions", synthesis_templates)

    def test_open_items_are_prioritized_within_their_next_move(self) -> None:
        reviewer = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        synthesis = (SKILL / "references/common/synthesis.md").read_text(encoding="utf-8")
        controls = (SKILL / "references/templates/control-templates.md").read_text(encoding="utf-8")
        reports = (
            SKILL / "references/templates/reviewer-report-template.md"
        ).read_text(encoding="utf-8")
        templates = (SKILL / "references/templates/report-templates.md").read_text(encoding="utf-8")
        normalized_reviewer = " ".join(reviewer.split())
        normalized_reports = " ".join(reports.split())
        normalized_synthesis = " ".join(synthesis.split())

        self.assertIn("Type` as the next-move lane", reviewer)
        self.assertIn("Priority orders work within its lane", reviewer)
        self.assertIn("| Finding | Severity | Effort | Evidence links | Confidence and limitation | Consequence | Taxonomy |", reports)
        self.assertIn("Severity is `Critical`, `High`, `Medium`, or `Low`", reports)
        self.assertIn("Effort is `S`, `M`, or `L`", reports)
        self.assertIn("CWE, ASVS, SLSA, OSPS", normalized_reports)
        self.assertIn("For every Key Findings row", normalized_reviewer)
        self.assertIn("Severity is consequence-based", normalized_reviewer)
        self.assertIn("Effort is the smallest responsible next move", normalized_reviewer)
        self.assertIn("Use taxonomy only when it is a direct fit", normalized_reviewer)
        self.assertIn("severity, effort, and taxonomy", normalized_synthesis)
        self.assertIn("do not collapse severity into open-item priority", normalized_synthesis)
        self.assertIn("### Decisions Now", synthesis)
        self.assertIn("### Evidence Needed", synthesis)
        self.assertIn("### Implementation Corrections", synthesis)
        self.assertIn("Priority orders items within their type", controls)
        self.assertIn("Preserve reviewer severity, effort, and taxonomy", templates)
        self.assertIn("do not present all P1 items as one queue", templates)

    def test_same_root_resume_preserves_open_item_and_decision_ids(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        normalized_onboarding = " ".join(onboarding.split())
        workflow = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        mining = (SKILL / "references/common/decision-mining.md").read_text(encoding="utf-8")
        controls = (SKILL / "references/templates/control-templates.md").read_text(encoding="utf-8")
        command = (ROOT / "commands/audit.md").read_text(encoding="utf-8")
        normalized_command = " ".join(command.split())
        onboard_command = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")

        self.assertIn("same read-write root", normalized_onboarding)
        self.assertIn("If Synthesis is completed, record `rerun-all`", normalized_onboarding)
        self.assertIn("otherwise record `complete-missing`", normalized_onboarding)
        self.assertIn(
            "mark every selected reviewer and Synthesis `rerun-pending`",
            normalized_onboarding,
        )
        self.assertIn("preserve prior artifacts and IDs", onboard_command)
        self.assertIn("without another start question", onboard_command)
        self.assertIn("`verified-fixed`", controls)
        self.assertIn("Reviewer run disposition", controls)
        self.assertIn("use `rerun-pending` for every selected reviewer", controls)
        self.assertIn("current highest ID", workflow)
        self.assertIn("prior prose and completion state are not proof", workflow)
        self.assertIn("existing decision\nstatus", workflow)
        self.assertIn("highest existing ID in that family", mining)
        self.assertIn("canonical ID baseline", command)
        for disposition in ("`fresh`", "`complete-missing`", "`rerun-all`"):
            self.assertIn(disposition, command)
        self.assertIn("prior prose is not proof", normalized_command)
        self.assertIn("do not rewrite it; report that nothing was missing", normalized_command)
        self.assertIn("always rerun synthesis", normalized_command)

    def test_dated_audit_roots_and_modes_are_routed_consistently(self) -> None:
        roots = (SKILL / "references/common/audit-root.md").read_text(encoding="utf-8")
        normalized_roots = " ".join(roots.split())
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        onboard = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")

        self.assertIn("_whats-going-on-YYYYMMDD", roots)
        self.assertIn("greatest date", roots)
        self.assertIn("Synthesis `completed` or", roots)
        self.assertIn("exact matching completed root", normalized_roots)
        self.assertIn("All audit roots are excluded", roots)
        self.assertIn("one independent audit root per day", roots)
        self.assertIn("Legacy `_whats-going-on/`", roots)
        self.assertIn("args: \"[compare|blind-compare] [YYYYMMDD]\"", onboard)
        self.assertIn("wgo:onboard [compare|blind-compare] [YYYYMMDD]", skill)
        for command_name in (
            "audit.md", "status.md", "summarize.md", "operationalize.md",
        ):
            command = (ROOT / "commands" / command_name).read_text(encoding="utf-8")
            self.assertIn("references/common/audit-root.md", command)

    def test_reused_configuration_and_version_mismatch_gates(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        normalized = " ".join(onboarding.split())
        docs = (ROOT / "docs/onboarding-expectations.md").read_text(encoding="utf-8")

        self.assertIn("For all three modes when a prior brief supplies configuration", normalized)
        self.assertIn("do not repeat standard onboarding questions", normalized)
        self.assertIn(
            "Does anything in this onboarding configuration need to be updated?",
            onboarding,
        )
        self.assertIn("Never fall back to the standard intake", onboarding)
        self.assertIn("without another start question", normalized)
        self.assertIn("active audit platform/model", normalized)
        self.assertIn("repeat package validation and the version gate", normalized)
        self.assertIn("For `compare` and `blind-compare`", onboarding)
        self.assertIn("An unavailable selected package is a blocker", normalized)
        self.assertIn(
            "The selected reviewer versions do not all match the installed packages. "
            "Is it acceptable to continue with the installed versions?",
            normalized,
        )
        self.assertIn("Do not ask this version question when all versions match", normalized)
        self.assertIn("WGO does not install or retrieve a reviewer", docs)

    def test_compare_and_blind_compare_preserve_their_evidence_boundaries(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        audit = (ROOT / "commands/audit.md").read_text(encoding="utf-8")
        synthesis = (SKILL / "references/common/synthesis.md").read_text(encoding="utf-8")
        controls = (SKILL / "references/templates/control-templates.md").read_text(encoding="utf-8")
        normalized_onboarding = " ".join(onboarding.split())
        normalized_synthesis = " ".join(synthesis.split())

        self.assertIn("select only reviewers that own baseline findings", normalized_onboarding)
        self.assertIn("does not seek unrelated findings", normalized_onboarding)
        self.assertIn("temporary copy of the audited project that excludes every audit root", normalized_onboarding)
        self.assertIn("Copy only the completed new dated audit root back", normalized_onboarding)
        self.assertIn("only the selected read-only\nbaseline items", audit)
        self.assertIn("do not give reviewers any baseline content", audit)
        self.assertIn("complete the full blind synthesis before reading", normalized_synthesis)
        self.assertIn("Reconcile findings in both directions", synthesis)
        self.assertIn("same boundary in each of the four audience reports", normalized_synthesis)
        self.assertIn("## Audit Comparison", controls)
        self.assertIn("Audit platform/model and catalog platform/model", controls)
        for disposition in (
            "`fixed`", "`improved`", "`unchanged`", "`regressed`",
            "`unverifiable`", "`newly-found`", "`no-longer-evaluated`",
        ):
            self.assertIn(disposition, controls)
        self.assertIn("Use `introduced` only when dated evidence proves", controls)

    def test_auditor_questions_are_distinguished_from_evidence_gaps(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        normalized_onboarding = " ".join(onboarding.split())
        workflow = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        normalized_workflow = " ".join(workflow.split())
        command = (ROOT / "commands/audit.md").read_text(encoding="utf-8")
        normalized_command = " ".join(command.split())
        controls = (SKILL / "references/templates/control-templates.md").read_text(encoding="utf-8")
        reports = (
            SKILL / "references/templates/reviewer-report-template.md"
        ).read_text(encoding="utf-8")

        self.assertIn("materially different acceptable outcomes", normalized_onboarding)
        self.assertIn("one focused disambiguation question", normalized_onboarding)
        self.assertIn("Material auditor answers and success boundaries", controls)
        self.assertIn("Return one exact question to the coordinator when it concerns mandate", normalized_workflow)
        self.assertIn("The reviewer never contacts the auditor", normalized_workflow)
        self.assertIn("do not bury the question in the report", normalized_workflow)
        self.assertIn("Use a `verification` when proof of a fact", normalized_workflow)
        self.assertIn("At the end of the wave, surface a qualifying auditor question", normalized_command)
        self.assertIn("ask one exact question, wait for its answer", normalized_command)
        self.assertIn("Do not let `wgo:audit all` defer", normalized_command)
        self.assertIn("## Material Omissions, Unknowns, And Auditor Questions", reports)
        self.assertIn("under verification rather than presenting them as questions", reports)

    def test_transition_control_is_the_only_audit_standard(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        validator = (SKILL / "scripts/validate_audit_structure.py").read_text(encoding="utf-8")
        operationalization = (SKILL / "references/common/operationalization.md").read_text(encoding="utf-8")

        self.assertNotIn("assessment` or `transition-control", onboarding)
        self.assertNotIn('parser.add_argument("--mode"', validator)
        self.assertIn("completed or bounded synthesis", operationalization)

    def test_operationalization_reuses_existing_runbooks(self) -> None:
        workflow = (SKILL / "references/common/operationalization.md").read_text(encoding="utf-8")
        command = (ROOT / "commands/operationalize.md").read_text(encoding="utf-8")
        template = (SKILL / "references/templates/operator-aid-template.md").read_text(encoding="utf-8")

        self.assertIn("existing runbook or operating procedure", workflow)
        self.assertIn("do not reproduce it", workflow)
        self.assertIn("complement only the missing", workflow)
        self.assertIn("Do not create a\nparallel runbook library.", workflow)
        self.assertIn("Link and complement an applicable runbook", command)
        self.assertIn("## Existing Runbook And Coverage", template)

    def test_executable_check_boundary_is_preserved(self) -> None:
        workflow = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        self.assertIn("Never install", workflow)
        self.assertIn("installation authorization", workflow)

    def test_minor_evidence_and_reviewer_improvements_remain_bounded(self) -> None:
        evidence = (SKILL / "references/common/evidence-rules.md").read_text(encoding="utf-8")
        workflow = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        quality = (SKILL / "references/common/artifact-quality-review.md").read_text(encoding="utf-8")
        reports = (
            SKILL / "references/templates/reviewer-report-template.md"
        ).read_text(encoding="utf-8")
        code_quality = reviewer_card("code-quality").read_text(encoding="utf-8")
        security = reviewer_card("security-privacy").read_text(encoding="utf-8")
        identity = (REVIEWERS / "security-privacy/workers/identity-secrets-data-boundaries.md").read_text(encoding="utf-8")

        self.assertIn("Documented outside audited scope; not independently\n   verified.", evidence)
        self.assertIn("smallest useful\nscope expansion", workflow)
        self.assertIn("Do not turn it into a new\n   register", evidence)
        self.assertIn("verified-fixed", workflow)
        self.assertIn("Never reuse\nan ID for a different item or decision", workflow)
        self.assertIn("evidence-supported strengths", quality)
        self.assertIn("## Mandate-Relevant Strengths", reports)
        self.assertIn("declared-gate inventory", code_quality)
        self.assertIn("green suite", code_quality)
        self.assertIn("runtime-build-surfaces.md", code_quality)
        self.assertIn("public security, privacy, and disclosure claims", security)
        self.assertIn("abuse or\nmisuse controls", security)
        self.assertIn("trust material to its consumer validation", identity)
        self.assertIn("vulnerability-class checklist", security)
        self.assertIn("OSPS Baseline tier", security)
        self.assertIn("trust-anchor consumption", security)
        self.assertIn("supply-chain-and-tooling.md", security)

        checklist = (REVIEWERS / "security-privacy/vulnerability-class-checklist.md").read_text(encoding="utf-8")
        tooling = (REVIEWERS / "security-privacy/workers/supply-chain-and-tooling.md").read_text(encoding="utf-8")
        for phrase in ("Canonicalization", "Data minimization", "Product-Class Abuse"):
            self.assertIn(phrase, checklist)
        for phrase in ("OpenSSF Scorecard", "OSV-Scanner", "gitleaks", "SBOM", "trust anchor"):
            self.assertIn(phrase, tooling)

    def test_structural_validation_is_optional(self) -> None:
        workflow = (SKILL / "references/common/reviewer-audit.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for phrase in (
            "Structural validation is optional.",
            "without installing anything",
            "installed for approved PyMuPDF4LLM support",
            "Structural validation not run: <reason>.",
            "do not describe the audit as\nstructurally validated",
        ):
            self.assertIn(phrase, workflow)
        self.assertIn("The bundled validator is optional.", readme)

    def test_synthesis_uses_handoffs_for_navigation_not_proof(self) -> None:
        synthesis = (SKILL / "references/common/synthesis.md").read_text(encoding="utf-8")
        self.assertIn("directly", synthesis)
        self.assertIn("handoff", synthesis)
        self.assertIn("out of order", synthesis)

    def test_product_value_collectors_are_bounded_and_separate(self) -> None:
        content = reviewer_card("product-value").read_text(encoding="utf-8")
        worker_dir = REVIEWERS / "product-value" / "workers"
        blocks = [path.read_text(encoding="utf-8") for path in sorted(worker_dir.glob("*.md"))]

        self.assertEqual(5, len(blocks))
        for block in blocks:
            self.assertLessEqual(len(block.splitlines()), 25)
            self.assertIn("do not write audit artifacts", block)
            self.assertIn("exact file and", block)
            self.assertIn("shared history collector", block)
        self.assertIn("CodeGraph is for code only", content)
        self.assertIn("## Evidence Collectors", content)
        self.assertIn("## Candidate Granularity", content)
        self.assertIn("## Required Evidence Packets And Artifact Routes", content)
        self.assertIn("Capability and lifecycle` is the\ncatch-all", content)
        self.assertIn("never run a specialist\ncollector merely because it is listed", content)
        for output in (
            "capability-contract-matrix.md", "product-value-flow.md",
            "rules-and-output-semantics.md", "provenance-notes.md",
        ):
            self.assertIn(output, content)

        capability = (worker_dir / "capability-lifecycle.md").read_text(encoding="utf-8")
        self.assertIn("any material product surface not covered by the other collectors", capability)

        semantics = (worker_dir / "rules-output-semantics.md").read_text(encoding="utf-8")
        for boundary in (
            "product rules", "validation", "permissions", "transformations",
            "version/result binding", "externally consumed outcome",
        ):
            self.assertIn(boundary, semantics)

        execution = (worker_dir / "execution-output.md").read_text(encoding="utf-8")
        for boundary in ("asynchronous execution", "state", "external services", "artifacts/results", "retries"):
            self.assertIn(boundary, execution)

        core_text = "\n".join([content, *blocks]).lower()
        for product_specific_term in (
            "qpm", "backtest", "dataops", "risk-free-rate",
            "strategy api", "strategy model", "selection/weighting/benchmark",
        ):
            self.assertNotIn(product_specific_term, core_text)

    def test_workerized_reviewers_have_one_preflight_and_compact_collectors(self) -> None:
        expected_workers = {
            "architecture": 3,
            "code-quality": 4,
            "product-value": 5,
            "security-privacy": 3,
            "business-continuity": 2,
            "scalability": 2,
            "contributor-vendor-value": 1,
        }
        for reviewer_id, expected_count in expected_workers.items():
            card = reviewer_card(reviewer_id).read_text(encoding="utf-8")
            workers = sorted((REVIEWERS / reviewer_id / "workers").glob("*.md"))
            self.assertIn("## Evidence Collectors", card)
            if reviewer_id in {"architecture", "code-quality", "product-value"}:
                self.assertIn("one\nCodeGraph", card)
            else:
                self.assertIn("collectors never call CodeGraph", card)
            self.assertEqual(expected_count, len(workers))
            for worker in workers:
                content = worker.read_text(encoding="utf-8")
                self.assertLessEqual(len(content.splitlines()), 25)
                self.assertIn("do not write audit artifacts", content)
                self.assertIn("do not invoke codegraph", content.lower())
                self.assertIn("exact file", content)
                self.assertIn("shared history", content)

    def test_business_reviewers_route_only_approved_shared_packets(self) -> None:
        expected = {
            "revenue-risk": ("golden-path-observation", "vendor-ownership-commercial", "demo-readiness.md"),
            "expense-exposure": ("vendor-ownership-commercial", "burn-and-renewal.md"),
            "contributor-vendor-value": ("vendor-ownership-commercial", "ownership-and-successor.md"),
            "maintenance-cost": ("delivery-and-quality", "time-to-safety.md"),
            "project-health": ("github-history-and-hosted-ci", "release-change-control.md"),
        }
        for reviewer_id, phrases in expected.items():
            content = reviewer_card(reviewer_id).read_text(encoding="utf-8")
            self.assertIn("## Required Evidence Packets And Artifact Routes", content)
            self.assertIn("wgo:operationalize", content)
            for phrase in phrases:
                self.assertIn(phrase, content)

    def test_contributor_value_uses_feature_evidence_not_activity_volume(self) -> None:
        card = reviewer_card("contributor-vendor-value").read_text(encoding="utf-8")
        normalized_card = " ".join(card.split())
        worker = (REVIEWERS / "contributor-vendor-value/workers/contribution-value.md").read_text(encoding="utf-8")
        templates = (SKILL / "references/templates/detailed-artifact-templates.md").read_text(encoding="utf-8")

        self.assertIn("contribution-value.md", card)
        self.assertIn("project-lifetime top-80% list", card)
        self.assertIn("cutoff-anchored 12-month period", normalized_card)
        self.assertIn("Do not treat commit volume,", card)
        self.assertIn("LoC, PR count", card)
        self.assertLessEqual(len(worker.splitlines()), 25)
        self.assertIn("do not write audit artifacts", worker)
        self.assertIn("Do not invoke CodeGraph", worker)
        self.assertIn("exact file/symbol", worker)
        self.assertIn("shared history", worker)
        self.assertIn("never rank people from raw PR, commit, or LoC volume", worker)
        self.assertIn("critical = 8", templates)
        self.assertIn("Project-Lifetime Top-80% Contributors", templates)
        self.assertIn("Cutoff-Anchored 12-Month Periods", templates)

    def test_operationalization_has_a_transition_packet_and_canonical_output_path(self) -> None:
        template = (SKILL / "references/templates/operator-aid-template.md").read_text(encoding="utf-8")
        for heading in (
            "## Purpose And Evidence Boundary", "## Authority And Preconditions",
            "## Procedure And Stop Conditions", "## Expected Evidence And Records",
            "## Escalation, Recovery, And Unknowns",
        ):
            self.assertIn(heading, template)
        workflow = (SKILL / "references/common/operationalization.md").read_text(encoding="utf-8")
        self.assertIn("operator-aids/<slug>.md", workflow)
        for aid in (
            "replacement-maintainer", "recovery", "observability",
            "iam-and-credential-control", "worker-data-operations",
            "isolated-rebuild", "network-exposure", "demo", "demo-reset", "delivery",
        ):
            self.assertIn(aid, workflow)
        self.assertIn("Ask whether to add any optional aid", workflow)

    def test_shared_collectors_are_compact_and_packet_only(self) -> None:
        collectors = sorted((SKILL / "references/collectors").glob("*.md"))
        self.assertEqual(6, len(collectors))
        for collector in collectors:
            content = collector.read_text(encoding="utf-8")
            self.assertLessEqual(len(content.splitlines()), 25)
            self.assertIn("Use the evidence-packet template", content)
            self.assertIn("Do not write reviewer reports", content)
            self.assertIn("Register each reusable material observation", content)

    def test_reviewer_blueprint_keeps_runtime_and_authoring_separate(self) -> None:
        blueprint = (SKILL / "references/common/reviewer-blueprint.md").read_text(encoding="utf-8")
        self.assertIn("not loaded by an audit run", blueprint)
        self.assertIn("22 lines or fewer", blueprint)
        self.assertIn("25 lines or fewer", blueprint)
        self.assertIn("CodeGraph is for code topology only", blueprint)
        self.assertIn("## Shared Evidence Collectors", blueprint)
        self.assertIn("version: 0.1", blueprint)

    def test_external_reviewer_contract_is_self_contained_and_coordinator_owned(self) -> None:
        contract = (SKILL / "references/common/reviewer-contract.md").read_text(encoding="utf-8")
        normalized = " ".join(contract.split())
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        self.assertFalse(list(REVIEWERS.glob("*.md")))
        self.assertIn("plugins/wgo-reviewers/<reviewer-id>/", contract)
        for field in (
            "id:", "name:", "summary:", "version:", "codegraph:", "depends_on:",
            "supersedes:",
        ):
            self.assertIn(field, contract)
        self.assertIn("`version` identifies the reviewer definition version", normalized)
        self.assertIn("Do not increment a reviewer version for changes only to shared WGO workflow", normalized)
        self.assertIn("validate_reviewer_contract.py", contract)
        self.assertIn(
            "`depends_on` is required whenever the reviewer has a prerequisite reviewer",
            normalized,
        )
        self.assertIn("omit it only when there is no dependency", normalized)
        self.assertIn("does not maintain a second reviewer registry", normalized)
        self.assertIn("Every external reviewer is optional", normalized)
        self.assertIn("do not run both", contract)
        self.assertIn("dependencies on the core ID to the replacement", contract)
        self.assertIn("run all currently unblocked reviewers in parallel", normalized)

        self.assertIn("No platform `validate_install` file means no reviewer installation is needed", normalized)
        self.assertIn("exit `0`: the reviewer is ready", contract)
        self.assertIn("showing its full absolute path", contract)
        self.assertIn("never run the installer on the auditor's behalf", contract)
        self.assertIn("rerun the validator before continuing", normalized)

        self.assertIn("The reviewer never talks directly to the auditor", contract)
        self.assertIn("Proof of implementation, access, ownership, or live state is a verification", normalized)
        self.assertIn("asks qualifying questions one at a time at a wave boundary", normalized)
        self.assertIn("more than one reviewer-owned control namespace", normalized)
        self.assertIn("references/reviewers/*/reviewer.md", onboarding)
        self.assertIn("under this skill", onboarding)
        self.assertIn("plugins/wgo-reviewers/*/reviewer.md", onboarding)
        self.assertIn("reviewer-contract.md", skill)

    def test_onboarding_records_selected_reviewer_versions(self) -> None:
        onboarding = (SKILL / "references/common/onboarding.md").read_text(encoding="utf-8")
        normalized_onboarding = " ".join(onboarding.split())
        controls = (
            SKILL / "references/templates/control-templates.md"
        ).read_text(encoding="utf-8")
        expectations = (ROOT / "docs/onboarding-expectations.md").read_text(
            encoding="utf-8"
        )
        normalized_expectations = " ".join(expectations.split())
        contract = (
            SKILL / "references/common/reviewer-contract.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "Require unique `id`, `name`, `summary`, `version`, and `codegraph`",
            onboarding,
        )
        self.assertIn("Present each reviewer's version", onboarding)
        self.assertIn("selected reviewer package IDs and versions", normalized_onboarding)
        self.assertIn(
            "reviewer's ID/version/source/absolute package path",
            normalized_onboarding,
        )
        self.assertIn(
            "Selected reviewer packages (ID, version, core/external, absolute path)",
            controls,
        )
        self.assertIn("selected reviewer IDs and versions", normalized_expectations)
        self.assertIn("change in a way that can affect results", contract)
        self.assertIn("shared WGO workflow", contract)

    def test_public_docs_explain_cross_agent_resume_and_reviewer_extensions(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        onboarding = (
            ROOT / "docs/onboarding-expectations.md"
        ).read_text(encoding="utf-8")
        guide_path = SKILL / "references/common/reviewer-authoring.md"
        guide = guide_path.read_text(encoding="utf-8")
        normalized_guide = " ".join(guide.split())

        self.assertIn("## Improve Or Compare An Audit", readme)
        self.assertIn("begin an audit with Codex", readme)
        self.assertIn("not blindly append-only", readme)
        self.assertIn("Comparison modes never modify the\nbaseline", readme)
        self.assertIn(
            "skills/wgo/references/common/reviewer-authoring.md",
            readme,
        )
        self.assertIn("## Returning To An Audited Project", onboarding)
        self.assertIn("Does anything in this onboarding configuration need to be updated?", onboarding)
        self.assertIn("## Audit Roots And Comparison", onboarding)
        self.assertIn("temporary project copy", " ".join(onboarding.split()))
        self.assertIn("Plain `wgo:onboard` reopens the newest root", readme)
        self.assertIn(
            "require the auditor to accept the installed versions",
            " ".join(readme.split()),
        )

        self.assertIn("# Building A WGO Reviewer", guide)
        self.assertIn("references/reviewer-scaffold/example-reviewer/", guide)
        self.assertIn("## Frontmatter Contract", guide)
        self.assertIn("## Version Governance", guide)
        self.assertIn("## What Every Reviewer Inherits", guide)
        self.assertIn("## What Makes A Reviewer Unique", guide)
        self.assertIn("## Discovery And Validation", guide)
        self.assertIn("`depends_on`", guide)
        self.assertIn("`supersedes`", guide)
        self.assertIn("validate_reviewer_contract.py", guide)
        self.assertIn("Bump a\nreviewer's version", guide)
        self.assertIn("Do not bump a reviewer version for spelling", guide)
        self.assertIn("validator is optional and structural", normalized_guide)
        self.assertIn(
            "(reviewer-contract.md)",
            guide,
        )
        self.assertIn(
            "references/common/reviewer-authoring.md",
            (SKILL / "SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertIn("skills/wgo/references/reviewer-scaffold/example-reviewer/", readme)
        self.assertIn("validate_reviewer_contract.py", readme)

    def test_reviewer_scaffold_and_contract_validator_are_pr_ready(self) -> None:
        validator = SKILL / "scripts/validate_reviewer_contract.py"
        scaffold = SKILL / "references/reviewer-scaffold/example-reviewer"
        readme = (scaffold.parent / "README.md").read_text(encoding="utf-8")
        reviewer = (scaffold / "reviewer.md").read_text(encoding="utf-8")
        worker = (scaffold / "workers/example-evidence-slice.md").read_text(encoding="utf-8")

        self.assertTrue(validator.is_file())
        self.assertTrue(scaffold.is_dir())
        self.assertIn("Copy `example-reviewer/`", readme)
        self.assertIn("id: example-reviewer", reviewer)
        self.assertIn("version: 0.1", reviewer)
        self.assertIn("do not invoke CodeGraph", worker)
        self.assertIn("do not delegate", worker)

        ok = subprocess.run(
            [sys.executable, str(validator), str(scaffold)],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual("", ok.stderr)
        self.assertEqual(0, ok.returncode)

        with tempfile.TemporaryDirectory() as temp:
            bad = Path(temp) / "bad-reviewer"
            bad.mkdir()
            (bad / "reviewer.md").write_text(
                "---\n"
                "id: bad-reviewer\n"
                "name: Bad Reviewer\n"
                "summary: Broken on purpose?\n"
                "version: draft\n"
                "codegraph: maybe\n"
                "depends_on:\n"
                "  - missing-core\n"
                "---\n"
                "# Reviewer: Bad Reviewer\n",
                encoding="utf-8",
            )
            failed = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    str(bad),
                    "--core-id",
                    "architecture",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(0, failed.returncode)
        self.assertIn("version must be numeric", failed.stderr)
        self.assertIn("invalid codegraph value", failed.stderr)
        self.assertIn("unknown dependency: missing-core", failed.stderr)
        self.assertIn("missing required section", failed.stderr)


if __name__ == "__main__":
    unittest.main()
