---
name: wgo
description: Evidence-led startup and SMB transition-control audit workflow for products, repositories, teams, vendors, continuity, value, cost, security, delivery, and architecture. Use when the active agent should onboard or resume a Whats.Going.On. audit, run one approved audit reviewer, report status, synthesize reports, draft approved operator aids, or publish a completed public audit through a draft PR.
when_to_use: Use when Claude should onboard or resume a Whats.Going.On. audit, run one approved audit reviewer, report status, synthesize reports, draft approved operator aids, or publish a completed public audit through a draft PR.
user-invocable: false
---

# Whats.Going.On.

Lead a prompt-first audit of the project in the current folder. Keep the audit
read-only unless the auditor explicitly authorizes a change. Produce useful,
source-backed artifacts; do not make the auditor administer a process model.

## Commands

- `wgo:onboard [compare|blind-compare] [YYYYMMDD]` (Codex),
  `/wgo:onboard [compare|blind-compare] [YYYYMMDD]` (Claude), or
  `/wgo-onboard [compare|blind-compare] [YYYYMMDD]` (OpenCode): start or improve an audit,
  run a light comparison, or run a blind audit followed by comparison.
- `wgo:audit [reviewer-id|all]` (Codex), `/wgo:audit [reviewer-id|all]`
  (Claude), or `/wgo-audit [reviewer-id|all]` (OpenCode): run one selected reviewer, or `all`/no
  parameter runs every selected reviewer in coordinator-defined dependency waves
  and then synthesis.
- `wgo:status` (Codex), `/wgo:status` (Claude), or `/wgo-status` (OpenCode):
  read the checklist and material open items.
- `wgo:summarize` (Codex), `/wgo:summarize` (Claude), or `/wgo-summarize`
  (OpenCode): reconcile completed work into three audience reports, calculate
  a reconciled API-equivalent audit cost estimate, then ask before
  operationalization.
- `wgo:cost` (Codex), `/wgo:cost` (Claude), or `/wgo-cost` (OpenCode):
  calculate a reproducible API-equivalent cost estimate from the completed
  audit's provider-native session records.
- `wgo:operationalize` (Codex), `/wgo:operationalize` (Claude), or
  `/wgo-operationalize` (OpenCode): after explicit approval of a completed synthesis, draft
  a four-part, source-linked, untested operating packet:
  replacement-maintainer, recovery, observability, and IAM/credential control.
  Before drafting, name that packet and ask whether to add an optional aid.
  It never executes a procedure or authorizes a system change. After the
  packet is complete, it refreshes the cost estimate through operationalization.
- `wgo:upload [YYYYMMDD]` (Codex), `/wgo:upload [YYYYMMDD]` (Claude), or
  `/wgo-upload [YYYYMMDD]` (OpenCode): verify one completed public audit and
  open a draft report-repository PR without revising the audit.

## Rules

- Audit the full current project folder and every approved supporting code
  repository at detailed depth.
- Do not guess company, product, architecture, ownership, approval, cost,
  customer commitment, or stakeholder intent. Ask a material question, create
  a verification, or state the unknown.
- Keep implementation, live state, behavior, approval, ownership, cost, and
  future intent distinct. One does not prove another.
- Do not copy secrets or unnecessary PII. Use redacted locators.
- Persist only portable relative filesystem paths: audit-root-relative,
  safely artifact-relative, or stable-source-ID-qualified.
  Absolute paths are transient tool inputs only.
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
- Keep model routing centralized rather than declaring models in reviewer
  packages. In Codex, coordinators and reviewers use the auditor-selected
  active model; every delegated WGO worker uses `gpt-5.6-terra` at high
  reasoning. If Terra is not selectable, use the active audit model. Other
  platforms use the same-platform model named by the workflow or their active
  audit model.
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
  and `references/templates/report-templates.md`. After the audience reports
  are final, read `references/templates/manifest-template.json`; after
  synthesis validation, read the matching cost workflow below.
- Cost estimation: select exactly one provider workflow from the platform in
  `audit-brief.md`: Codex `references/common/cost-estimation.md`, Claude
  `references/common/cost-estimation-claude.md`, or OpenCode
  `references/common/cost-estimation-opencode.md`; then read
  `references/templates/cost-estimate-template.md`. It is a coordinator phase:
  discover and freeze the audit-session manifest before calculation, run
  exactly two independent provider-specific verification passes over that same
  manifest, and write `controls/cost-estimate.md` with its frozen calculation
  evidence, then refresh `manifest.json`'s lean cost summary. A missing or
  unsupported platform is `Unreconciled`, never an
  invitation to inspect another provider's records.
- Operationalize: `references/common/operationalization.md`,
  `references/common/evidence-rules.md`, the selected template(s), and then
  the same provider cost workflow to refresh the cost estimate.
- Upload: `references/common/upload.md`, `references/common/evidence-rules.md`,
  and `config/upload.yaml`.

## New-Audit Layout

```text
_whats-going-on-YYYYMMDD/
  audit-brief.md
  audit-checklist.md
  manifest.json             # synthesis output
  documentation/
    catalog.md
  evidence/
    evidence-ledger.md
    source-access-register.md
    packets/<selected-collector>.md
  controls/
    open-items.md
    cost-estimate.md
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
