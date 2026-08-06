---
id: example-reviewer
name: Example Reviewer
summary: What distinct decision should this reviewer help the auditor make?
version: 0.1
codegraph: none
# depends_on:
#   - architecture
# external reviewers may optionally replace one core perspective:
# supersedes: core-reviewer-id
---

# Reviewer: Example Reviewer

## Objective And Business Questions

State the one bounded question this reviewer owns and the decisions it informs.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Example assessment | Always, in `reviewer-reports/example-reviewer/report.md` |
| Conditional | Example control view in `controls/example/` | A material example boundary is evidenced |
| Not owned | Adjacent concern | Link the owning reviewer |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `github-history-and-hosted-ci` | Targeted source-control context is material | Reconcile provenance only; link from the report |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs.
Downstream reviewers may use linked findings without inferring unobserved facts.

## Evidence Collectors

Use collectors only when a broad repository needs parallel source collection.

| Collector | Scope | Prompt |
|---|---|---|
| Example evidence slice | One non-overlapping evidence boundary | `workers/example-evidence-slice.md` |

## Completion Criteria

State the evidenced position, material gaps, selected outputs, and downstream
limits.

## Escalation Conditions

- A mandate, authority, or acceptable outcome question would change the result.

## Cross-Reviewer Links

Name upstream evidence owners and downstream consumers.
