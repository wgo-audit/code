---
name: wgo
description: Evidence-led startup and SMB transition-control audit workflow for products, repositories, teams, vendors, continuity, value, cost, security, delivery, and architecture. Use when Codex should onboard or resume a Whats.Going.On. audit, run one approved audit reviewer, report audit status, synthesize decision-grade reports, or turn an approved synthesis into clearly untested operator aids.
---

# Whats.Going.On.

Lead a prompt-first audit of the project in the current folder. Keep the audit
read-only unless the auditor explicitly authorizes a change. Produce useful,
source-backed artifacts; do not make the auditor administer a process model.

## Commands

- `wgo:onboard [compare|blind-compare] [YYYYMMDD]`: start or improve an audit,
  run a light comparison, or run a blind audit followed by comparison.
- `wgo:audit [reviewer-id|all]`: run one selected reviewer, or `all`/no
  parameter runs every selected reviewer in coordinator-defined dependency waves
  and then synthesis.
- `wgo:status`: read the checklist and material open items.
- `wgo:summarize`: reconcile completed work into three audience reports, then
  ask before operationalization.
- `wgo:operationalize`: after explicit approval of a completed synthesis, draft
  a four-part, source-linked, untested operating packet:
  replacement-maintainer, recovery, observability, and IAM/credential control.
  Before drafting, name that packet and ask whether to add an optional aid.
  It never executes a procedure or authorizes a system change.

## Rules

- Audit the full current project folder and every approved supporting code
  repository at detailed depth.
- Do not guess company, product, architecture, ownership, approval, cost,
  customer commitment, or stakeholder intent. Ask a material question, create
  a verification, or state the unknown.
- Keep implementation, live state, behavior, approval, ownership, cost, and
  future intent distinct. One does not prove another.
- Do not copy secrets or unnecessary PII. Use redacted locators.
- A failed expected-source access attempt needs a remediation, approved
  fallback, or explicit exclusion.
- Do not install dependencies, restore packages, change lockfiles, deploy,
  restore, rotate credentials, or change billing without explicit authorization.
  Use public GitHub data and private GitHub data available through an existing
  session; do not request credentials. Record executable-check boundaries
  truthfully.
- For CodeGraph, initialize or sync every distinct Git root in the project
  folder or approved code clone; a monorepo is one root. Always pass its
  absolute root path to lifecycle commands and `--path` to queries; workers
  never invoke CodeGraph.
- Use fixed templates only for outputs selected by a reviewer card. Do not create
  an artifact merely because a template exists.
- `controls/open-items.md` holds material risks, decisions needing authority,
  verifications, and actions. ADRs/PDRs are observed decision records, not
  open-item substitutes.
- The audit coordinator owns scope and synthesis. A reviewer owns its own
  evidence reconciliation, artifacts, report, and handoff. Bounded collectors
  return evidence packets only.
- Reviewer packages are discovered during onboarding. External reviewers and
  core substitutions are optional until the auditor approves them.

## Reference Routing

Read each selected file completely, and begin evidence inspection before
reading an output template that has not been selected.

- Every command: resolve the active dated audit root with
  `references/common/audit-root.md`.
- Onboarding: `references/common/onboarding.md`,
  `references/common/evidence-rules.md`, and
  `references/templates/control-templates.md`. Delegate exactly one
  documentation-preparation worker after approval. Give it
  `references/common/documentation-prep.md`, documentation-bearing paths from
  audited code roots, approved evidence/documentation sources, repository
  mappings, mandate, selected reviewers, cheap capability signals, active audit
  platform, and chosen same-platform catalog model; the onboarding lead does
  not read that instruction file or delegate further intake.
- Reviewer audit: `references/common/reviewer-audit.md`,
  `references/common/evidence-rules.md`,
  `references/templates/reviewer-report-template.md`, the selected artifact
  template(s), and the approved package's `reviewer.md`. Read
  `references/templates/evidence-packet-template.md` only when a selected
  shared collector will run. Read
  `references/common/decision-mining.md` only for detailed Architecture or
  Product Value work; those reviewers also read
  `references/templates/detailed-artifact-templates.md` for their required
  inventory/register and any selected decision record or diagram. After
  drafting selected outputs, delegate one bounded quality worker and tell it to
  read
  `references/common/artifact-quality-review.md`; the reviewer does not read
  that worker rubric.
- Reviewer design: `references/common/reviewer-authoring.md`,
  `references/common/reviewer-contract.md`, and
  `references/common/reviewer-blueprint.md` only when adding or redesigning a
  reviewer; do not load them during an audit run.
- Status: `references/common/reviewer-audit.md`.
- Synthesis: `references/common/synthesis.md`,
  `references/common/evidence-rules.md`, `references/common/reconciliation.md`,
  and `references/templates/report-templates.md`.
- Operationalize: `references/common/operationalization.md`,
  `references/common/evidence-rules.md`, and the selected template(s).

## New-Audit Layout

```text
_whats-going-on-YYYYMMDD/
  audit-brief.md
  audit-checklist.md
  documentation/
    catalog.md
  evidence/
    evidence-ledger.md
    source-access-register.md
    packets/<selected-collector>.md
  controls/
    open-items.md
    <selected reviewer-owned artifact directories>
  reviewer-reports/<reviewer-id>/
    report.md
    handoff.md
  operator-aids/
    replacement-maintainer.md
    recovery.md
    observability.md
    iam-and-credential-control.md
  index.md
  executive-summary.md
  product-manager-notes.md
  technical-lead-notes.md
  comparison.md              # compare and blind-compare only
```

Existing audits may retain an earlier `final/` directory. Move it only when the
auditor explicitly asks to resume under this layout. The checklist is the only
lifecycle/work view. Reviewer handoffs aid navigation and are never canonical
evidence.
