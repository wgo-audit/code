# Audit Root Resolution

Every independent audit uses a root named `_whats-going-on-YYYYMMDD`, where
`YYYYMMDD` is the auditor-local calendar date when that audit's onboarding
started. Validate that the suffix is a real date. Improving an existing audit
does not rename it.

Before any WGO command, discover immediate child directories matching
`_whats-going-on-[0-9]{8}`. An audit root is valid only when it contains
`audit-brief.md` and `audit-checklist.md`. The active audit root for
`wgo:audit`, `wgo:status`, `wgo:summarize`, and `wgo:operationalize` is the
valid root with the greatest date. If none exists, direct the auditor to
`wgo:onboard`. Never combine state from multiple roots.

An audit is completed when its checklist marks Synthesis `completed` or
`completed-with-open-verification`. When onboarding needs the latest completed
audit, choose the completed root with the greatest date. A supplied baseline
date selects the exact matching completed root; report a missing, invalid, or
incomplete baseline instead of substituting another audit.

All audit roots are excluded from product source and documentation discovery.
Only the active root may be written. A comparison baseline is read-only and may
be read only by the comparison behavior that explicitly selected it. A blind
audit reviewer or synthesis worker must not receive a baseline path, artifact,
summary, finding, or prior identifier.

If the target root for today's date already exists, resume it only when its
recorded mode and baseline match the requested run. Otherwise stop and explain
that one independent audit root per day is supported; never overwrite or merge
roots.

Legacy `_whats-going-on/` is not assigned a date automatically. When it is the
only audit root, ask the auditor for its onboarding start date and permission
to rename it. When it exists beside dated roots, report it as legacy state and
do not read, rename, merge, or delete it without explicit direction.
