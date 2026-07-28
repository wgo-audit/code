---
id: maintenance-cost
name: Maintenance Cost
summary: What skill mix, effort, operating burden, and change risk will a small replacement team face?
codegraph: optional
depends_on:
  - architecture
  - code-quality
  - business-continuity
---

# Reviewer: Maintenance Cost

## Objective And Business Questions

Assess the evidence-bounded burden of maintaining and safely changing the
product. Do not estimate staffing cost as a financial fact without rate evidence.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Maintenance burden assessment | Always, in `reviewer-reports/maintenance-cost/report.md` |
| Conditional | Complexity/hotspot, skills/operations, or time-to-safety map in `controls/maintenance/` | A material maintenance or successor question is found |
| Not owned | Defect/test truth and contributor ownership | Link Code Quality and Contributor/Vendor Value |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `delivery-and-quality` | Approved setup, test, release, or repair evidence is needed | Reconcile safe-change burden; link from `controls/maintenance/time-to-safety.md` |
| `vendor-ownership-commercial` | Approved owner, successor, vendor, or operating-role evidence is needed | Reconcile replacement boundary; link from `controls/maintenance/time-to-safety.md` |

The reviewer requests a packet only when approved and absent or stale. It never creates an operator aid; one may be eligible later through `wgo:operationalize`.

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture, Code Quality, and Business Continuity. Project Health may use the
result. Do not turn code complexity into a defect or staffing claim.

## Completion Criteria

State skill, hotspot, and operating burden with evidence limits and selected
outputs.

## Escalation Conditions

- A critical subsystem has no plausible safe-change or successor route.
- Material operational knowledge is concentrated and unrecorded.

## Cross-Reviewer Links

Code Quality owns test/defect evidence; Contributor/Vendor Value owns knowledge
and handoff; Expense Exposure owns cash impact.
