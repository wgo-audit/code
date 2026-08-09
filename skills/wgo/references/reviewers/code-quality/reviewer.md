---
id: code-quality
name: Code Quality
summary: Which code-level risks materially affect correctness, delivery, maintainability, security, or product promises?
version: 0.2
codegraph: required
depends_on:
  - architecture
---

# Reviewer: Code Quality

## Objective And Business Questions

Assess test, defect, and change-safety evidence. A passing local command does
not prove production readiness, correctness, or deployment health. Inventory
the project-declared quality gates; run only checks whose dependencies and
authorization are already available.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Test/defect/change-safety assessment | Always, in `reviewer-reports/code-quality/report.md` |
| Conditional | Test health, defect register, or change-safety matrix in `controls/quality/` | Material test, defect, regression, or safe-change question |
| Not owned | Architecture boundary and product correctness | Link Architecture and Product Value |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `delivery-and-quality` | The brief approves executable or hosted check evidence | Reconcile checks and gates; link from test-health or change-safety output |
| `github-history-and-hosted-ci` | A material regression/control needs targeted history or hosted CI context | Reconcile provenance only; link from selected output and report |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture. Product, maintenance, and project-health work may use linked
findings. Record dependency state and authorization for every executable check;
when dependencies are absent, do not install them without authorization.

## Evidence Collectors

Use collectors only when the repository is broad enough to justify parallel
source collection. The Code Quality reviewer owns reconciliation and writes all
artifacts; collectors return evidence packets only. The reviewer runs one
CodeGraph topology preflight before fan-out with the relevant absolute Git root;
collectors do not invoke CodeGraph.

| Collector | Scope | Prompt |
|---|---|---|
| CI, test commands, and release gates | CI/CD workflow definitions, declared test/lint/type-check/build commands, test-result availability, and release/deployment gates; excludes application-code quality evidence | `workers/ci-test-release-gates.md` |
| Python, API, workers, and migrations | Python services, API routes, background workers, data access, migrations, and their Python tests; excludes CI/release definitions and TypeScript/UI surfaces | `workers/python-api-workers-migrations.md` |
| TypeScript, UI, dashboard, and generated client | TypeScript/JavaScript application code, UI/dashboard components, generated clients, and their frontend tests; excludes CI/release definitions and Python/API/worker/migration surfaces | `workers/typescript-ui-dashboard-client.md` |
| Other runtime and build surfaces | A material runtime/build/test surface not covered by the Python or TypeScript collectors; excludes CI/release definitions and those language slices | `workers/runtime-build-surfaces.md` |

## Completion Criteria

State the declared-gate inventory, exact executed and unexecuted check
boundaries, and coverage position as `measured`, brief-authorized `declined`, or
`blocked`. State material fixture provenance as `production-generated`,
`independently-built`, or `unknown`, including duplicated production contracts,
contract drift, quality evidence, and selected outputs. For any green suite,
state the critical paths it did and did not cover. Separate source inspection
from executed behavior.

## Escalation Conditions

- A product-critical workflow has no credible change-safety evidence.
- Tests cannot run because required dependencies or access are absent.

## Cross-Reviewer Links

Architecture owns topology; Product Value owns correctness/sign-off boundaries;
Maintenance Cost owns the cost of the identified burden.
