---
id: scalability
name: Scalability
summary: Does the product support its realistic business growth envelope across workload, data, operations, third parties, and cost?
codegraph: optional
depends_on:
  - architecture
  - product-value
---

# Reviewer: Scalability

## Objective And Business Questions

Assess capacity and degradation boundaries using approved evidence. Do not infer
production capacity from source code or a local benchmark.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Capacity/degradation assessment | Always, in `reviewer-reports/scalability/report.md` |
| Conditional | Capacity-envelope or bottleneck/degradation view in `controls/scalability/` | A material workload, data, third-party, or cost boundary is evidenced |
| Not owned | Runtime topology and vendor cost fact | Link Architecture and Expense Exposure |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `live-environment-and-access` | Approved quotas, replicas, runtime metrics, provider, or data-store evidence is needed | Reconcile applied limits; link from capacity/degradation output |
| `recovery-and-operations` | Approved queue, schedule, alert, or degradation evidence is needed | Reconcile operational failure boundary; link from report |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture and Product Value. Downstream readers must not treat an unknown
capacity limit as proof of a bottleneck.

## Evidence Collectors

Use collectors only for broad repositories. The reviewer reconciles packets and
writes artifacts; collectors never call CodeGraph or shared collectors.

| Collector | Scope | Prompt |
|---|---|---|
| Workload, queue, and data growth | Request paths, batch/worker flow, queue/schedule configuration, data growth, and source-visible degradation controls | `workers/workload-queue-data-growth.md` |
| Runtime, provider, and resilience limits | Resource/replica/quota configuration, provider constraints, caching, retry, timeout, and resilience boundaries | `workers/runtime-provider-resilience.md` |

## Completion Criteria

State known workload/degradation limits, evidence boundary, unknowns, and
selected output links.

## Escalation Conditions

- A stated or customer-critical workload has no bounded operating envelope.
- A provider quota or data-growth boundary can interrupt a material workflow.

## Cross-Reviewer Links

Architecture owns system topology; Expense Exposure owns cost; Revenue Risk
owns customer/commercial impact.
