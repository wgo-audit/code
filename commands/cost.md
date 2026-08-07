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
`references/common/audit-root.md`, then run the complete workflow in
`references/common/cost-estimation.md`.

This is a read-only analysis of accessible Codex session JSONL files that writes
`<audit-root>/controls/cost-estimate.md` and its frozen calculation evidence.
Do not install a package, invoke `ccusage`, add a helper program, or use an
OS-specific binary.
The Terra coordinator at high reasoning discovers the audit descendants from
recorded collaboration and task-lifecycle provenance, freezes the manifest
before any calculation, and runs exactly two independent Terra calculations at
high reasoning over that unchanged manifest. Never identify an included
session solely by date, CWD, folder, or model; those may corroborate recorded
provenance only.
