---
name: status
description: Show truthful Whats.Going.On. audit progress, blockers, and material open items.
skills: wgo
---

# /status

Codex users may invoke this as `wgo:status`.

Resolve the newest dated audit root with
`skills/wgo/references/common/audit-root.md`. Read, without modifying:

- `<audit-root>/audit-checklist.md`
- `<audit-root>/controls/open-items.md`
- `<audit-root>/evidence/source-access-register.md`
- relevant completed reviewer reports when their closeout is unclear

Report each selected reviewer's state, factual completion condition, next action,
recommended next reviewer, material source-access limits, and open-item counts by
`Type` and priority. If the audit files do not exist, direct the auditor to
`wgo:onboard`. The checklist is the only work/status view; do not reconstruct a
second status table. Treat `rerun-pending` as pending work with a completed
prior pass, not as never reviewed.
