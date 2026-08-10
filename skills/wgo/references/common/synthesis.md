# Synthesis Workflow

Use for `wgo:summarize`. Synthesis is an audit-lead reconciliation step, not a
concatenation of reports or a workflow gate.

Before doing synthesis work or emitting the summary phase marker, recursively
reconcile every WGO task spawned from the audit root against recorded
collaboration and task-lifecycle provenance. Every start must have exactly one
terminal outcome: completed, failed, cancelled, or interrupted. Do not infer
closure from reports, checklist states, messages, or worker disappearance. If
any task remains running, open, multiply terminated, or ambiguously correlated,
do not begin synthesis; wait or report the exact blocking task/session. A
failed, cancelled, or interrupted task is lifecycle-closed but does not make
its reviewer successful; retain the existing dependency limitation.

After that gate passes, emit this normal progress message once:
`Starting synthesis. <!-- WGO_PHASE_SUMMARY_START -->`. The HTML comment is a
persisted cost-attribution marker, not audit evidence.

Read each completed reviewer report, handoff, and linked evidence/artifacts
directly. A reviewer run out of order remains publishable when its report states
the specific limitation.

Read the onboarding mode from the brief. In `blind-compare`, complete the full
blind synthesis before reading or receiving any baseline path or content.

Reconcile material findings, source-access limits, unknowns, duplicated advice,
and cross-reviewer consequences. Then create:

- `index.md` as the start-here guide;
- `executive-summary.md` for current posture, decisions, and evidence-
  supported owner-assigned 30–90 day work;
- `product-manager-notes.md` for capability, promise, and approval
  boundaries; and
- `technical-lead-notes.md` for traceable technical conclusions and safe
  evolution.

When multiple Security family reviewers are selected, present their reconciled
conclusions together under the reader-facing security discussion while
preserving each reviewer's ownership. Do not add a separate umbrella finding or
duplicate the same control gap. Supply-chain security is synthesized by route:
baseline trust-boundary signals from Security and Privacy, dependency/build
exploitability from Application Security, registry/IaC/deployment/runtime
controls from Cloud Security, and named C-SCRM requirement mapping from
Compliance Assurance.

For `compare`, also create `comparison.md` from the selected baseline items and
current reassessment evidence using the Audit Comparison template. State
prominently that this targeted run did not seek unrelated or newly introduced
issues. Put the same boundary in each of the four audience reports so none is
mistaken for a new full-audit assessment of current posture.

For `blind-compare`, after the four blind reports are complete, end the blind
phase. Only then may the coordinator read the selected baseline and create
`comparison.md`. Reconcile findings in both directions and distinguish fixed,
improved, unchanged, regressed, newly found, no longer evaluated, and
unverifiable conclusions. Do not call a finding introduced unless dated
evidence establishes that timing.

Promote a reviewer finding into a synthesis insight only when it changes a
decision, priority, sequence, claim, or stop condition. Preserve the finding's
severity, effort, and taxonomy when carrying it into synthesis or technical
lead notes; do not collapse severity into open-item priority. Preserve all
independent material insights; combine only those that change the same
decision. Do not set a target number or promote a fact merely to fill one. In
the executive summary's `Material Risks, Unknowns, And Decisions` section, add
a `### Decision-Useful Conclusions` subsection when one or more material
insights exist. Route each to the audience that must decide or act, with linked
evidence and the smallest next move.

Then separate the remaining material open items into `### Decisions Now`,
`### Evidence Needed`, and `### Implementation Corrections`, using the canonical
open-item type. Omit an empty lane. Order items by dependency and consequence
within that lane; do not compare P labels across lanes or create a second
backlog.

Update `manifest.json` after the four audience reports are created. Preserve
the schema `1.0.0` top-level contract and fill only evidence-supported values:
report title, generated date when supported, subject identity, audit type and
mode, evidence cutoff and sources, generator and reviewer versions when known,
headline/result conclusions with stable IDs, and explicit relationships for
compare or blind-compare runs. Do not invent generator commits, reviewer
versions, model names, finding counts, timestamps, or source citations. Omit
unsupported optional fields; for required unknowns use `null`, `[]`, or a
controlled `unknown` value.

## Cost Closeout

After the four audience reports pass synthesis validation, run the complete
provider workflow selected from `audit-brief.md`: `cost-estimation.md` for
Codex, `cost-estimation-claude.md` for Claude, or
`cost-estimation-opencode.md` for OpenCode. This is the final
end-of-audit phase, before the operationalization question. It creates
`controls/cost-estimate.md` with frozen calculation evidence; link the control
from `index.md`, `executive-summary.md`,
`product-manager-notes.md`, and `technical-lead-notes.md` as an
API-equivalent estimate with its reconciliation status.

Immediately before starting that cost workflow, emit this normal progress
message once: `Synthesis validated; starting cost estimation. <!--
WGO_AUDIT_COMPLETE_COST_PHASE_STARTS -->`. The marker is the audit-only cost
cutoff; the cost workflow itself is excluded from the estimate.

Do not delay or omit the audit cost phase because a rate, JSONL field, session
file, or reconciliation result is unknown. State the limitation, mark the
affected model or aggregate unpriced/unreconciled, and preserve the exact
manifest and disputed records instead.

Do not create an action backlog, decision queue, status table, or a separate
reconciliation workflow. Any operator aid remains a later, explicitly
authorized `wgo:operationalize` activity. After the summary and cost closeout
are complete, ask exactly: `Should I proceed with wgo:operationalize?` Do not
draft operator aids until the auditor answers yes.
