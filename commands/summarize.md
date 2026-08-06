---
name: summarize
description: Reconcile completed Whats.Going.On. reviewers and create decision-grade audience reports.
skills: wgo
disable-model-invocation: true
---

# /summarize

Invoke this as `wgo:summarize` in Codex, `/wgo:summarize` in Claude, or
`/wgo-summarize` in OpenCode.

Load and use the WGO skill. Resolve the newest dated audit root with its
`references/common/audit-root.md`.

Run its `references/common/synthesis.md`. Read completed
reviewer reports, their handoffs, and linked evidence/artifacts directly.
Reconcile before drafting and preserve source-access limits, uncertainty, and
evidence cutoff.

Always create `index.md`, `executive-summary.md`, `product-manager-notes.md`,
and `technical-lead-notes.md` at the audit root. Include an owner-assigned
30–90 day section only where evidence supports it. Do not create a separate
reconciliation command, decision queue, or action backlog.

After the summary is complete, ask exactly: `Should I proceed with
wgo:operationalize?` Do not draft operator aids until the auditor answers yes.
