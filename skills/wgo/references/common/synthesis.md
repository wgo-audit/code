# Synthesis Workflow

Use for `wgo:summarize`. Synthesis is an audit-lead reconciliation step, not a
concatenation of reports or a workflow gate.

Read each completed reviewer report, handoff, and linked evidence/artifacts
directly. A reviewer run out of order remains publishable when its report states
the specific limitation.

Reconcile material findings, source-access limits, unknowns, duplicated advice,
and cross-reviewer consequences. Then create:

- `index.md` as the start-here guide;
- `executive-summary.md` for current posture, decisions, and evidence-
  supported owner-assigned 30–90 day work;
- `product-manager-notes.md` for capability, promise, and approval
  boundaries; and
- `technical-lead-notes.md` for traceable technical conclusions and safe
  evolution.

Promote a reviewer finding into a synthesis insight only when it changes a
decision, priority, sequence, claim, or stop condition. Preserve all independent
material insights; combine only those that change the same decision. Do not set
a target number or promote a fact merely to fill one. In the executive summary's
`Material Risks, Unknowns, And Decisions` section, add a `### Decision-Useful
Conclusions` subsection when one or more material insights exist. Route each to
the audience that must decide or act, with linked evidence and the smallest next
move.

Then separate the remaining material open items into `### Decisions Now`,
`### Evidence Needed`, and `### Implementation Corrections`, using the canonical
open-item type. Omit an empty lane. Order items by dependency and consequence
within that lane; do not compare P labels across lanes or create a second
backlog.

Do not create an action backlog, decision queue, status table, or a separate
reconciliation workflow. Any operator aid remains a later, explicitly
authorized `wgo:operationalize` activity. After the summary is complete, ask
exactly: `Should I proceed with wgo:operationalize?` Do not draft operator aids
until the auditor answers yes.
