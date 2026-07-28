---
id: business-continuity
name: Business Continuity
summary: Can the company demo, deploy, operate, recover, and transfer control if a person, vendor, account, or environment disappears?
version: 0.1
codegraph: optional
depends_on:
  - architecture
  - security-privacy
---

# Reviewer: Business Continuity

## Objective And Business Questions

Assess continuity and control boundaries from approved evidence. Runbook creation
or updating is outside this reviewer.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Continuity/control assessment | Always, in `reviewer-reports/business-continuity/report.md` |
| Conditional | Access/ownership, environment/service, vendor-control, expiry/maintenance, or recovery/control view in `controls/continuity/` | The corresponding boundary is material to interruption or transfer |
| Conditional | Observability and response path: `controls/continuity/diagrams/observability-and-response-path.md` | Detailed work has approved dashboard, alert, ownership, or incident evidence |
| Not owned | Technical topology and security posture | Link Architecture and Security/Privacy |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `recovery-and-operations` | Approved backup, queue, alert, restore, reset, or drill evidence is needed | Reconcile recovery/response position; link from selected controls and response path |
| `live-environment-and-access` | Approved service, runtime, account, or ownership inventory is needed | Reconcile effective operating dependencies; link from report |
| `vendor-ownership-commercial` | Approved vendor/control or successor evidence is needed | Reconcile accountable control; link from continuity controls |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture and Security/Privacy. Expense, contributor, and other downstream
work may use linked control evidence but must not assume an untested runbook
proves recovery.

## Evidence Collectors

Use collectors only for broad repositories. The reviewer reconciles packets and
writes artifacts; collectors never call CodeGraph or shared collectors.

| Collector | Scope | Prompt |
|---|---|---|
| Recovery, data operations, and alerting | Backup/restore declarations, queue/schedule controls, observability and alert configuration, recovery/restart boundaries | `workers/recovery-dataops-alerting.md` |
| Delivery, account, and transfer control | Runtime/deploy control transfer, account/admin dependencies, vendor/service ownership, and successor boundaries | `workers/delivery-account-transfer.md` |

## Completion Criteria

State the continuity/control position, evidence boundary, material gaps, and
selected artifact links. Label all unobserved recovery and ownership facts.

## Escalation Conditions

- Control of a critical account, environment, vendor, or recovery path is unknown.
- A demo or customer-critical service has no bounded interruption route.

## Cross-Reviewer Links

Security owns exposure posture; Expense Exposure owns financial commitments;
Architecture owns topology; operational aids require later explicit approval.
