---
id: security-privacy
name: Security and Privacy
summary: What material identity, credential, exposure, privacy, PII, supply-chain, and operating-control risks are evidenced?
version: 0.3
codegraph: optional
depends_on:
  - architecture
---

# Reviewer: Security and Privacy

## Objective And Business Questions

Assess evidence-bounded security and privacy posture without copying secrets or
claiming an unperformed penetration test, cloud review, supply-chain
assessment, or compliance certification. Reconcile material public security, privacy, and disclosure claims, plus supply-chain claims, with the available
implementation and operational evidence. Answer the applicable
vulnerability-class checklist items selected from topology. For every trust
anchor the source produces, such as signatures, checksums, or provenance,
locate its consuming verifier; absent or unclear verifier use is a finding.
Identify material product-class abuse paths and assess project countermeasures
as security controls. When the brief declares an OSPS Baseline tier, assess
against that tier without claiming certification. Route deeper specialist
questions without duplicating ownership.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Security/privacy posture | Always, in `reviewer-reports/security-privacy/report.md` |
| Required | Vulnerability-class checklist verdicts, using `vulnerability-class-checklist.md` | Always, in the report; mark non-applicable classes with reason |
| Conditional | Secret surface, credential exposure, privilege/offboarding, or trust/data-flow view in `controls/security/` | A material secret, identity, privilege, data, or boundary question is found |
| Conditional | Supply-chain and tooling results view: `controls/security/supply-chain-and-tooling.md` | Tooling, dependency, release-provenance, SBOM, or verifier evidence is material |
| Conditional | Edge exposure view: `controls/security/diagrams/edge-exposure-view.md` | Detailed work has approved DNS, TLS, ingress, WAF, or reachability evidence |
| Not owned | Deep AppSec, cloud control effectiveness, compliance mapping, business continuity ownership, or technical model | Link Application Security, Cloud Security, Compliance Assurance, Business Continuity, and Architecture |

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
| Supply chain and tooling | Authorized local Scorecard, OSV, and secret-scanner runs; dependency, release-provenance, SBOM, and trust-anchor consumption evidence | `workers/supply-chain-and-tooling.md` |

## Completion Criteria

State material exposed surfaces, checklist verdicts, claim reconciliation,
trust-anchor consumption, abuse-control position, strongest security assets for
the mandate outcome, evidence limits, selected controls, specialist routes, and
closure routes without secret values or unbounded claims.

## Escalation Conditions

- A credential-like surface may have production privilege or unknown revocation.
- PII, tenant, or privilege boundaries are unknown on a critical path.
- A produced trust anchor has no locatable verifier on a consumption path.
- A public security, privacy, or disclosure claim materially contradicts
  implementation evidence.
- A source, dependency, build, vendor, or deployment trust boundary is material
  but needs Application Security, Cloud Security, or Compliance Assurance.

## Cross-Reviewer Links

Application Security owns source-level attack paths and application dependency
exploitability. Cloud Security owns cloud, IAM, network, deployment, registry,
and runtime control effectiveness. Compliance Assurance owns requirement
mapping, including named C-SCRM baselines. Continuity owns access/control
transfer; Architecture owns topology; Revenue Risk owns customer or claim
impact.
