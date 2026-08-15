---
id: application-security
name: Application Security
summary: Can material application attack paths violate authentication, authorization, confidentiality, integrity, or tenant boundaries?
version: 0.1
codegraph: required
depends_on:
  - security-privacy
  - code-quality
---

# Reviewer: Application Security

## Objective And Business Questions

Assess evidence-bounded application security for source-visible attack paths
that could materially affect transition control, customer trust, data exposure,
or product claims. Focus on exploitable behavior and implemented controls, not
general maintainability or an unperformed penetration test.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Application security assessment | Always, in `reviewer-reports/application-security/report.md` |
| Conditional | Attack-path and control view in `controls/application-security/` | A material authentication, authorization, validation, injection, tenant, data-access, or cryptographic-control path is evidenced |
| Conditional | Dependency or build-input exploitability note in `controls/application-security/` | A vulnerable, abandoned, privileged, generated, or build-time dependency could materially affect application behavior |
| Not owned | Code maintainability, ordinary defect risk, cloud control effectiveness, compliance status, or baseline privacy posture | Link Code Quality, Cloud Security, Compliance Assurance, or Security and Privacy |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `github-history-and-hosted-ci` | Source provenance, release/build context, or security-scanning results could change exploitability or remediation confidence | Link from the report or dependency/build-input note |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Security and Privacy, Code Quality. Use Security and Privacy for baseline
identity, data, secret, exposure, privacy, and supply-chain boundary routing.
Use Code Quality for declared test and quality-gate evidence. Downstream Cloud
Security may consume application-facing boundary findings; Compliance Assurance
may map validated findings to named requirements.

## Evidence Collectors

Use collectors only for broad repositories. The reviewer reconciles packets and
writes artifacts; collectors never call CodeGraph or shared collectors.

| Collector | Scope | Prompt |
|---|---|---|
| Attack paths and application controls | Authn/authz, tenant isolation, validation, injection, data access, cryptography, session, API, and abuse controls | `workers/attack-paths-and-controls.md` |
| Dependency and build inputs | Runtime dependencies, lockfiles, package scripts, generated code, build plugins, security scanning, and source supply-chain inputs that affect application behavior | `workers/dependency-and-build-inputs.md` |

## Completion Criteria

State material application attack paths, implemented or missing controls,
evidence limits, and closure routes without claiming comprehensive AppSec,
active exploitation, or penetration-test coverage.

## Escalation Conditions

- Authentication, authorization, tenant, or data-access boundaries are unknown
  on a critical path.
- A source-visible attack path could expose sensitive data, bypass privilege, or
  corrupt material business state.
- Dependency, generated-code, or build-input evidence suggests a material
  supply-chain route into application behavior.

## Cross-Reviewer Links

Security and Privacy owns baseline identity, secret, data, privacy, exposure,
and supply-chain triage. Code Quality owns general maintainability and defect
readiness. Cloud Security owns cloud, IAM, network, deployment, registry, and
runtime control effectiveness. Compliance Assurance owns requirement mapping
and certification boundaries.
