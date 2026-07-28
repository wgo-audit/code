---
id: product-value
name: Product Value
summary: What customer and business value is demonstrably implemented, partial, promised, or awaiting sign-off?
version: 0.1
codegraph: required
depends_on:
  - architecture
---

# Reviewer: Product Value

## Objective And Business Questions

Answer what useful capability exists end to end, which workflow and outcome it
supports, and where implementation, demonstration, approval, or public promise
diverge. Exclude unapproved product strategy or specialist sign-off.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required (detailed) | PDR candidate inventory: `controls/product/pdr-candidate-inventory.md` | Always |
| Required (detailed) | PDR register: `controls/product/pdr-register.md` | Always |
| Conditional | Individual PDR: `controls/product/pdr/PDR-###-<slug>.md` | Material `record-created` candidate |
| Conditional | Source-bounded workflow/API, configuration-contract, output/provenance, or capability/promise view in `controls/product/` | The bounded question is materially clearer as an artifact |
| Conditional | Deep-review packet: `controls/product/capability-contract-matrix.md`, `controls/product/diagrams/product-value-flow.md`, `controls/product/rules-and-output-semantics.md`, and `controls/product/provenance-notes.md` | A material capability spans multiple entry points, execution paths, rules, dependencies, or outputs |
| Not owned | Technical topology, commercial exposure, and control ownership | Link Architecture, Revenue Risk, or Business Continuity |

Use `../../templates/detailed-artifact-templates.md` for the required inventory
and register and for every selected PDR or diagram.

When a selected workflow, capability, provenance, or configuration-contract
view is materially clearer as a flow, boundary, dependency, or state change,
make it a source-bounded diagram. Missing demonstration evidence is shown as an
unknown boundary, not a reason to reduce the view to prose.

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `github-history-and-hosted-ci` | Current source identifies a material rule requiring rationale, supersession, PR/issue, or hosted-check context | Reconcile provenance only; link it from PDRs or `provenance-notes.md` |
| `golden-path-observation` | A safe environment, test identity, and fixture are available | Establish or limit implementation-to-demonstration claims; link it from the end-to-end flow and report |

The reviewer may request these packets but never produces them. If a safe source
or action is unavailable, state the resulting evidence limit once; do not replace
it with a second local-source pass.

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture. Dependent work may use linked workflow evidence; it must not
mistake implementation presence for customer acceptance, correctness, or
approval.

## Evidence Collectors

Use collectors only when the repository is broad enough to justify parallel
source collection. The Product Value reviewer owns reconciliation and writes
all artifacts; collectors return evidence packets only. The reviewer runs one
CodeGraph topology pass before fan-out with the relevant absolute Git root;
CodeGraph is for code only. Read
configuration and documentation directly.

Select only collectors whose surfaces exist. `Capability and lifecycle` is the
catch-all and may cover a narrow product alone; never run a specialist
collector merely because it is listed.

| Collector | Scope | Prompt |
|---|---|---|
| Capability and lifecycle | Actors, problems, outcomes, entry points, capabilities, lifecycle states, and any material product surface not covered below | `workers/capability-lifecycle.md` |
| User workflow and contract | UI, API, CLI, SDK, integration, identity/access, visible controls, responses, and failure paths when present | `workers/user-workflow-contract.md` |
| Execution, data, and output | Synchronous or asynchronous processing, inputs, state, persistence, external services, artifacts/results, retries, and provenance when present | `workers/execution-output.md` |
| Rules and output semantics | Defaults, validation, configuration, permissions, transformations, calculations, eligibility/selection, output meaning, and version binding when present | `workers/rules-output-semantics.md` |
| Product evidence | Documentation, configuration, public claims, and approval/sign-off evidence | `workers/product-evidence.md` |

## Candidate Granularity

A candidate is one durable, independently changeable product rule, default,
state transition, permission, output contract, or recovery behavior. Do not
merge distinct user-visible choices just because one workflow implements them.
When the brief authorizes Git metadata, current source proves implementation and
targeted history supplies historical intent or supersession; label each rather
than inventing approval or rationale.

## Completion Criteria

- Applicable maturity/demo, user/workflow, lifecycle, configuration, output,
  governance, dependency, promise, and acceptance domains have source-bounded
  coverage.
- Detailed work has the required inventory/register and a PDR for each material
  `record-created` candidate.
- Selected views distinguish implementation, observed behavior, correctness,
  approval, and unknowns.
- When the deep-review trigger is met, the capability/contract matrix traces
  material inputs and controls through their runtime consumer, the product-value
  flow shows confirmed and unknown boundaries, and provenance is bounded to
  approved history.
- Material promise or sign-off gaps have a stated closure route.

## Escalation Conditions

- A visible control is ignored, mocked, preview-only, or transformed without a
  clear evidence path.
- A material output lacks provenance, freshness/version binding, or required
  specialist sign-off.
- A public promise exceeds demonstrated evidence.

## Cross-Reviewer Links

Promise/demo exposure belongs to Revenue Risk; operation to Business
Continuity; change safety to Code Quality; technical dependencies to
Architecture; capacity/cost limits to Scalability and Expense Exposure.
