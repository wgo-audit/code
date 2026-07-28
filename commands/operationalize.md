---
name: operationalize
description: Turn an approved synthesis into explicitly untested, source-linked operator aids without executing procedures or changing systems.
skills: wgo
---

# /operationalize

Codex users may invoke this as `wgo:operationalize`.

Run the complete workflow in `skills/wgo/references/common/operationalization.md`.

Hard rules:

- Require a completed or completed-with-open-verification synthesis and explicit auditor approval before drafting operator aids.
- Before writing, announce the required four-part packet and ask whether the auditor wants any optional aid: `worker-data-operations`, `isolated-rebuild`, `network-exposure`, `demo`, `demo-reset`, or `delivery`.
- Draft documentation only. Do not run commands against environments, authenticate to new systems, deploy, restart, rotate, revoke, migrate, restore, reset data, modify billing, or change routing.
- Every procedure starts `Status: draft` or `Status: untested`; use `executed-successfully` only when canonical evidence records a real authorized execution.
- Use exact source locators only when source evidence supports them. Mark a command, prerequisite, threshold, account, fixture, expected output, rollback, or owner `UNKNOWN` when it has not been established.
- Use linked evidence and selected audit artifacts directly. The checklist remains the work view and `controls/open-items.md` holds material future work; operator aids are never competing controls.
- Search approved documentation for an existing runbook before drafting each aid. Link and complement an applicable runbook; do not copy it or create a parallel runbook library.
- Create an operating-control strategy only when the completed controls need an explicit stabilization and authority model; it is a derived decision aid, not a second backlog or a runbook.
- Create the four-part transition packet at `operator-aids/`: `replacement-maintainer`, `recovery`, `observability`, and `iam-and-credential-control`. Keep them separate, cross-linked, and evidence-bounded.
- Do not create a fixed-size 72-hour mission board. Generate the execution-priority taxonomy instead.
