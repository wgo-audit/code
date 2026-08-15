---
name: cost
description: Produce a reconciled API-equivalent cost estimate for a completed Whats.Going.On. audit.
skills: wgo
disable-model-invocation: true
---

# /cost

Invoke this as `wgo:cost` in Codex, `/wgo:cost` in Claude, or `/wgo-cost` in
OpenCode.

Load and use the WGO skill. Resolve the newest dated audit root with its
`references/common/audit-root.md`, then read the audit platform recorded in
`audit-brief.md` and run exactly one matching workflow:

- Codex: `references/common/cost-estimation.md`;
- Claude: `references/common/cost-estimation-claude.md`; or
- OpenCode: `references/common/cost-estimation-opencode.md`.

Do not inspect a provider's session store or apply its usage schema to an audit
recorded on another platform. If the platform is missing, ambiguous, or
unsupported, write an `Unreconciled` cost control naming that limitation rather
than guessing.

This is a read-only analysis of accessible provider-native session records that
writes `<audit-root>/controls/cost-estimate.md` and its frozen calculation
evidence, then updates `<audit-root>/manifest.json` at
`execution.costEstimate` with the result's exact total or explicitly labeled
unreconciled subtotal.
Do not install a package, invoke `ccusage`, add a helper program, or use an
OS-specific binary.
The active-platform coordinator discovers the audit descendants from recorded
collaboration and task-lifecycle provenance, freezes the manifest before any
calculation, and runs exactly two independent calculations over that unchanged
manifest using the worker configuration in the selected provider workflow.
Never identify an included session solely by date, CWD, folder, or model; those
may corroborate recorded provenance only.
After every calculation or refresh, follow
`references/templates/cost-estimate-template.md` to replace the manifest cost
summary and validate `manifest.json` again.
