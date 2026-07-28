---
id: contributor-vendor-value
name: Contributor and Vendor Value
summary: What usable output, ownership, knowledge, handoff, and cost-relative value did people or vendors provide?
version: 0.1
codegraph: none
depends_on:
  - product-value
  - business-continuity
---

# Reviewer: Contributor and Vendor Value

## Objective And Business Questions

Assess usable contribution, knowledge concentration, vendor dependency, and
successor needs from approved evidence. Do not infer performance, blame, or
contractual acceptance.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Contribution/successor assessment | Always, in `reviewer-reports/contributor-vendor-value/report.md`; include contributor-value coverage and any resulting top-80% list |
| Conditional | Contribution-value assessment: `controls/contributors/contribution-value.md` | GitHub/Git or approved evidence supports feature-level contributor attribution |
| Conditional | Contribution/successor or vendor-dependency map in `controls/contributors/` | Material ownership, handoff, or vendor concentration evidence |
| Not owned | Cost fact and identity control | Link Expense Exposure and Business Continuity |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `vendor-ownership-commercial` | Approved role, handoff, successor, vendor, or acceptance evidence is needed | Reconcile accountable ownership; link from `controls/contributors/ownership-and-successor.md` |

The reviewer requests a packet only when approved and absent or stale. It never creates an operator aid; one may be eligible later through `wgo:operationalize`.

## Evidence Collectors

The reviewer owns reconciliation and writes all artifacts. When auditable
repository history or approved contribution evidence exists, run the collector
below; it returns evidence only; collectors never call CodeGraph.

| Collector | Scope | Prompt |
|---|---|---|
| Feature-level contribution value | Linked PRs, commits, reviews, issues, tests, debugging, documentation, and approved non-GitHub evidence | `workers/contribution-value.md` |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Product Value and Business Continuity. Project Health may use the result. Do
not infer performance from activity volume. Do not treat commit volume,
LoC, PR count, or account control as value.

## Completion Criteria

- State evidenced contribution/control position, material unknowns, and selected
  outputs.
- When feature-level attribution is supported, create the contribution-value
  assessment with a project-lifetime top-80% list. When history spans more than
  12 months, add one list for each consecutive, cutoff-anchored 12-month
  period. A list contains the smallest contributor set that reaches
  approximately 80% of attributed feature-value units, not the top 80% of
  accounts.
- Keep outcome value, task magnitude, delivery quality, contribution share, and
  confidence separate. Rank with the published bands in the selected template;
  do not create a performance score or infer uncredited work.

## Escalation Conditions

- A critical product or vendor boundary has no accountable successor.
- Knowledge or access concentration threatens handoff.

## Cross-Reviewer Links

Business Continuity owns account transfer; Maintenance Cost owns replacement
burden; Expense Exposure owns commercial commitments.
