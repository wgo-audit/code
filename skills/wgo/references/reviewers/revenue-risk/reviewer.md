---
id: revenue-risk
name: Revenue Risk
summary: What could interrupt demos, sales, pilots, onboarding, renewals, expansion, trust, or customer delivery?
version: 0.2
codegraph: none
depends_on:
  - product-value
  - business-continuity
---

# Reviewer: Revenue Risk

## Objective And Business Questions

Assess claim, demo, and commercial delivery exposure from approved evidence.
Do not infer contract terms, customer commitments, or revenue amount.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Claim/demo/commercial assessment | Always, in `reviewer-reports/revenue-risk/report.md` |
| Conditional | Claim-governance, demo-readiness, or exposure register in `controls/revenue/` | A material promise, demo, onboarding, renewal, or delivery boundary is evidenced |
| Not owned | Capability, cost, and operational truth | Link Product Value, Expense Exposure, and Business Continuity |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `golden-path-observation` | The brief approves a safe demo identity, fixture, and observation | Reconcile observed demo readiness; link from `controls/revenue/demo-readiness.md` |
| `vendor-ownership-commercial` | Approved claims, commitments, renewal, or entitlement evidence is needed | Reconcile claim/commercial boundary; link from `controls/revenue/claim-governance.md` |

The reviewer requests a packet only when approved and absent or stale. It never creates an operator aid; one may be eligible later through `wgo:operationalize`.

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Product Value and Business Continuity. Project Health may use the result. Do
not treat public positioning as proof of implementation.

## Completion Criteria

State evidenced promises/exposure, material unknowns, and selected output links.

## Escalation Conditions

- A material claim exceeds demonstrated or approved capability evidence.
- A demo/customer workflow depends on unowned access or unverified operation.

## Cross-Reviewer Links

Product Value owns capability; Business Continuity owns operating control;
Security/Privacy owns exposure posture; Expense Exposure owns cost risk.
