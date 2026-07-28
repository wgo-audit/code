---
id: architecture
name: Architecture
summary: Is the current technical boundary and its material decisions understood well enough for safe change?
codegraph: required
---

# Reviewer: Architecture

## Objective And Business Questions

Answer what components, dependencies, data, runtime boundaries, and material
technical decisions exist for safe evolution. Exclude a full architecture
documentation program and unapproved live-state testing.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required (detailed) | ADR candidate inventory: `controls/architecture/adr-candidate-inventory.md` | Always |
| Required (detailed) | ADR register: `controls/architecture/adr-register.md` | Always |
| Conditional | Individual ADR: `controls/architecture/adr/ADR-###-<slug>.md` | Material `record-created` candidate |
| Conditional | Source-bounded diagram: `controls/architecture/diagrams/<question>.md` | A component, runtime/deployment, data/job/provenance, dependency, or trust-boundary question is materially clearer as a view |
| Conditional | DevOps infrastructure view: `controls/architecture/diagrams/devops-infrastructure-view.md` | Detailed work has approved live-environment evidence |
| Conditional | Deployment and runtime path: `controls/architecture/diagrams/deployment-and-runtime-path.md` | Detailed work spans delivery workflow, image/service state, migration, and runtime evidence |
| Not owned | Product workflow/promise artifacts | Link Product Value |

Use `../../templates/detailed-artifact-templates.md` for the required inventory
and register and for every selected ADR or diagram.

For each applicable component/runtime, deployment, dependency, data/provenance,
trust, or handoff domain, decide whether prose alone makes the relationship
clear. If not, create one source-bounded diagram. Do not merge unrelated reader
questions merely to reduce diagram count; label unobserved boundaries unknown.

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `live-environment-and-access` | Approved runtime, DNS, cloud, data-store, or account metadata is needed | Reconcile live boundaries; link from the detailed diagrams and report |
| `github-history-and-hosted-ci` | A material architecture rule needs targeted rationale or workflow history | Reconcile provenance only; link from ADRs or the deployment path |
| `delivery-and-quality` | Approved delivery/check evidence is needed | Reconcile release and deployment boundary; link from the deployment path |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs.
This reviewer has no predecessor. Downstream technical, security, continuity,
product, quality, cost, and scalability work may use linked source evidence;
it must not assume source topology proves live state.

## Evidence Collectors

Use collectors only when the repository is broad enough to justify parallel
source collection. The Architecture reviewer owns reconciliation and writes all
artifacts; collectors return evidence packets only. The reviewer runs one
CodeGraph preflight topology pass before fan-out; collectors must not invoke
CodeGraph. Pass the relevant absolute Git root to every CodeGraph command. Read
source and configuration directly; request shared history only
for selected material rules.

| Collector | Non-overlapping scope | Prompt |
|---|---|---|
| Component, API, UI, and shared-contract topology | Components, modules, API/UI boundaries, generated/shared contracts, and direct dependencies | `workers/component-api-ui-contracts.md` |
| Data, jobs, migrations, artifacts, and provenance | Data stores/flows, scheduled or asynchronous jobs, schema migrations, produced artifacts, and provenance paths | `workers/data-jobs-migrations-provenance.md` |
| Runtime, deployment, delivery, and identity-secrets integration | Process/runtime wiring, deployment/delivery configuration, environment integration, and identity/secrets boundaries | `workers/runtime-deployment-delivery-identity-secrets.md` |

## Completion Criteria

- Applicable component, runtime, data, dependency, contract, and decision
  domains have source-bounded coverage.
- Detailed work has the required inventory/register and a record for each
  material `record-created` candidate.
- Diagrams label confirmed, inferred, and unknown elements and do not withhold a
  useful source-bounded view for lack of live proof.
- Each selected artifact has passed the ephemeral quality review and was revised
  when it did not clearly support its stated reader question.
- Material gaps are in the report and open-items table only when future owner,
  authority, or proof is needed.

## Escalation Conditions

- An authoritative data source, critical dependency, trust boundary, or
  runtime/deployment control cannot be determined.
- Source topology conflicts with authorized live observations.
- A shared contract or migration creates unbounded change risk.

## Cross-Reviewer Links

Product behavior belongs to Product Value; operational controls to Business
Continuity; exposure boundaries to Security/Privacy; capacity to Scalability.
