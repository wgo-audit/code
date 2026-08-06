---
id: project-health
name: Project Health
summary: Can a small team understand, prioritize, review, accept, release, and learn from the work?
version: 0.2
codegraph: none
depends_on:
  - code-quality
  - revenue-risk
  - maintenance-cost
  - contributor-vendor-value
---

# Reviewer: Project Health

## Objective And Business Questions

Assess delivery/process evidence, not product capability or implementation
correctness.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Delivery/process assessment | Always, in `reviewer-reports/project-health/report.md` |
| Conditional | Work-in-flight, operating-cadence, or release/change-control view in `controls/project-health/` | The relevant delivery boundary is material |
| Not owned | Capability, test/defect, staffing, or continuity evidence | Link Product Value, Code Quality, Contributor/Vendor Value, or Business Continuity |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `delivery-and-quality` | Approved release, acceptance, deployment, or check evidence is needed | Reconcile delivery boundary; link from `controls/project-health/release-change-control.md` |
| `github-history-and-hosted-ci` | Targeted branch, PR, workflow, or historical release context is needed | Reconcile provenance only; link from release/change-control output |

The reviewer requests a packet only when approved and absent or stale. It never creates an operator aid; one may be eligible later through `wgo:operationalize`.

## Recommended Inputs And Downstream Use

Read the brief, approved delivery records, named shared packets, and only
completed `depends_on` handoffs: Code Quality, Revenue Risk, Maintenance Cost,
and Contributor/Vendor Value. Do not infer a healthy cadence from a few commits.

## Completion Criteria

State the evidence-bounded delivery position, material gaps, and selected
outputs. When documentation is material, state its audience/task coverage,
currency, and conflicts; route each conflict to the reviewer owning its
consequence.

## Escalation Conditions

- Work cannot be prioritized, accepted, released, or traced through a material boundary.
- Material release/change authority is unknown.

## Cross-Reviewer Links

Product Value determines capability and requirements truth. Code Quality
determines CI and implementation evidence. Contributor/Vendor Value determines
staffing and ownership concentration. Business Continuity determines operational
continuity.
