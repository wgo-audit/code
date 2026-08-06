---
id: expense-exposure
name: Expense Exposure
summary: What actual or potential cash exposure comes from infrastructure, software, staffing, commitments, and failure modes?
version: 0.2
codegraph: none
depends_on:
  - architecture
  - product-value
---

# Reviewer: Expense Exposure

## Objective And Business Questions

Assess cost and interruption exposure from approved billing, contract, usage,
and dependency evidence. Do not infer spend from source dependencies alone.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Cost/interruption assessment | Always, in `reviewer-reports/expense-exposure/report.md` |
| Conditional | Burn/renewal or vendor-control view in `controls/expense/` | Material spend, commitment, renewal, quota, or vendor interruption evidence |
| Not owned | Vendor access transfer and scalability model | Link Business Continuity and Scalability |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `vendor-ownership-commercial` | Approved billing, usage, term, renewal, or vendor-control evidence is needed | Reconcile the exposure; link from `controls/expense/burn-and-renewal.md` |

The reviewer requests a packet only when approved and absent or stale. It never creates an operator aid; one may be eligible later through `wgo:operationalize`.

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture and Product Value. Downstream readers must not treat a dependency
as a cost without billing evidence.

## Completion Criteria

State evidenced spend/exposure, material unknowns, and selected artifact links.

## Escalation Conditions

- A renewal, quota, or billing owner could interrupt a material product surface.
- Material cost cannot be bounded from approved evidence.

## Cross-Reviewer Links

Business Continuity owns transfer control; Architecture owns dependencies;
Revenue Risk owns commercial interruption consequences.
