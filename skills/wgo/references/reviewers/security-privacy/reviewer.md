---
id: security-privacy
name: Security and Privacy
summary: What material identity, credential, exposure, privacy, PII, and operating-control risks are evidenced?
version: 0.1
codegraph: optional
depends_on:
  - architecture
---

# Reviewer: Security and Privacy

## Objective And Business Questions

Assess evidence-bounded security and privacy posture without copying secrets or
claiming an unperformed penetration test or compliance certification. Reconcile
material public security, privacy, and disclosure claims with the available
implementation and operational evidence.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Security/privacy posture | Always, in `reviewer-reports/security-privacy/report.md` |
| Conditional | Secret surface, credential exposure, privilege/offboarding, or trust/data-flow view in `controls/security/` | A material secret, identity, privilege, data, or boundary question is found |
| Conditional | Edge exposure view: `controls/security/diagrams/edge-exposure-view.md` | Detailed work has approved DNS, TLS, ingress, WAF, or reachability evidence |
| Not owned | Business continuity ownership and technical model | Link Business Continuity and Architecture |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `live-environment-and-access` | Approved IAM, secret metadata, edge, DNS, certificate, or runtime inventory is needed | Reconcile effective exposure and access; link from posture and edge view |
| `github-history-and-hosted-ci` | A material source control needs targeted provenance | Reconcile history only; link from the selected control or report |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture. For each material externally reachable use case, inspect abuse or
misuse controls only when that question could change the transition-control
decision; otherwise state it is not applicable once in the report. Downstream
reviewers may use redacted findings; they must not infer active compromise from
historical source exposure alone.

## Evidence Collectors

Use collectors only for broad repositories. The reviewer reconciles packets and
writes artifacts; collectors never call CodeGraph or shared collectors.

| Collector | Scope | Prompt |
|---|---|---|
| Identity, secrets, and privacy boundaries | Authn/authz, service identity, secret consumers/metadata, PII/data boundaries, and lifecycle controls | `workers/identity-secrets-data-boundaries.md` |
| Edge and runtime exposure | Ingress, DNS/TLS/WAF declarations, network paths, admin/public routes, and runtime exposure configuration | `workers/edge-runtime-exposure.md` |

## Completion Criteria

State material exposed surfaces, evidence limits, selected controls, and closure
routes without secret values or unbounded claims.

## Escalation Conditions

- A credential-like surface may have production privilege or unknown revocation.
- PII, tenant, or privilege boundaries are unknown on a critical path.

## Cross-Reviewer Links

Continuity owns access/control transfer; Architecture owns topology; Revenue
Risk owns customer or claim impact.
