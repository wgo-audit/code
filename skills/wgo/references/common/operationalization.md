# Operationalization

Use only after a completed or bounded synthesis and the auditor explicitly asks
for it. Read the brief, final reports, selected artifacts, and evidence
directly. Do not infer a completed synthesis from a status table.

Before doing operationalization work, emit this normal progress message once:
`Starting operationalization. <!-- WGO_PHASE_OPERATIONALIZATION_START -->`. The
HTML comment is a persisted cost-attribution marker, not audit evidence.

Before drafting, tell the auditor that WGO will create the required four-part
transition packet: `replacement-maintainer`, `recovery`, `observability`, and
`iam-and-credential-control`. Also list the optional additions:
`worker-data-operations`, `isolated-rebuild`, `network-exposure`, `demo`,
`demo-reset`, and `delivery`. Ask whether to add any optional aid, and wait for
the answer before writing. An explicit "no" proceeds with the required packet.

Before drafting each aid, search the approved documentation catalog and source
for an existing runbook or operating procedure that answers its operator
question. Treat an applicable runbook as the primary procedure: link its exact
source and do not reproduce it. The aid may be a short transition guide that
states applicability, authority, evidence boundary, known gaps, and cross-links.
When a runbook is incomplete, complement only the missing precondition, stop
condition, evidence, ownership, or recovery detail. Draft a new procedure only
when no applicable runbook exists. Existing text is not proof that a procedure
was executed or remains current.

Draft the core operating packet: four distinct, source-linked operator aids
covering successor acceptance, recovery, observability, and IAM/credential
control. Mark every unexecuted procedure `untested`; state unknown identity,
fixture, threshold, rollback, and owner details. Never authenticate, deploy,
restore, rotate a credential, change billing, install a dependency, or execute
a procedure.

Read `references/templates/operator-aid-template.md` immediately before writing.
Create the following four aids at `operator-aids/<slug>.md`. They form one
transition packet, not a generic runbook library:

| Evidence focus | Required aid |
|---|---|
| Maintenance delivery/ownership evidence | `replacement-maintainer` |
| Recovery/operations packet | `recovery` |
| Recovery/operations packet | `observability` |
| Security/live environment/access evidence | `iam-and-credential-control` |
| Recovery/operations packet | optional: `worker-data-operations` or `isolated-rebuild` |
| Security/live environment/access evidence | optional: `network-exposure` |
| Revenue/Product golden-path evidence | optional: `demo` or `demo-reset` |
| Project Health delivery/quality evidence | optional: `delivery` |

Keep each aid focused on its operator question; cross-link rather than merge
procedures. `executed-successfully` requires a linked canonical record of an
authorized execution; source evidence alone is never enough. Do not create a
parallel runbook library.

Update the relevant checklist entry and add an open item only when a future
owner, authority decision, or proof is required.

After the selected operator packet is complete, emit this normal progress
message once: `Operationalization complete; refreshing cost estimate. <!--
WGO_OPERATIONALIZATION_COMPLETE_COST_PHASE_STARTS -->`. Then rerun the complete
cost-estimation workflow in `cost-estimation.md` with coverage through
operationalization. Update `controls/cost-estimate.md`, but preserve the frozen
audit-only manifest and verification outputs. Exclude both cost-calculation
phases from the estimate itself. If the refreshed result is unreconciled,
publish that status and its exact limitations rather than retaining the earlier
precise total as though it included operationalization.
