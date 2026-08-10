---
id: compliance-assurance
name: Compliance Assurance
summary: For named regulatory or assurance baselines, which applicable requirements are evidenced, partial, unknown, or awaiting specialist validation?
version: 0.1
codegraph: none
depends_on:
  - product-value
  - security-privacy
  - application-security
  - cloud-security
  - business-continuity
---

# Reviewer: Compliance Assurance

## Objective And Business Questions

Map named regulatory, assurance, privacy, security-control, or cybersecurity
supply-chain baselines to evidence-backed conclusions from selected reviewers
and approved direct records. State evidenced, partial, unknown, not in scope,
and awaiting-specialist-validation requirements without legal advice,
certification, or retesting controls.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Compliance assurance assessment | Always, in `reviewer-reports/compliance-assurance/report.md` |
| Conditional | Requirement-to-evidence matrix in `controls/compliance-assurance/` | The mandate names a regulation, standard, framework, contractual baseline, privacy baseline, or C-SCRM/control-mapping decision |
| Conditional | Validation-route note in `controls/compliance-assurance/` | A requirement depends on missing specialist evidence, legal interpretation, live-state verification, external attestation, or unselected prerequisite coverage |
| Not owned | Technical retesting, AppSec findings, cloud control effectiveness, recovery readiness, product value, legal advice, or certification | Link the reviewer that owns the underlying conclusion |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `live-environment-and-access` | Approved audit, attestation, IAM, cloud, privacy, vendor, or control evidence needs source-access reconciliation | Link from requirement-to-evidence matrix or validation-route note |
| `github-history-and-hosted-ci` | Hosted development, release, CI/CD, dependency, or supply-chain evidence is part of a named requirement | Link from requirement-to-evidence matrix |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Product Value, Security and Privacy, Application Security, Cloud Security, and
Business Continuity. Use those handoffs as conclusion routes, then inspect only
approved direct compliance records needed to map named requirements. This is a
downstream assurance reviewer; no same-wave or later reviewer is an input.

## Completion Criteria

Record the named baseline, edition or effective version when available,
approved control scope, authoritative source, evidence cutoff, mapped evidence,
gaps, limitations, and closure routes. Distinguish technical evidence gaps from
legal interpretation, auditor judgment, external attestation, and certification.

## Escalation Conditions

- The mandate names compliance, certification, customer assurance, privacy, or
  C-SCRM requirements without an authoritative baseline or control scope.
- A requirement depends on unavailable specialist validation or live-state
  evidence that could materially change a go/no-go decision.
- Evidence contradicts a public security, privacy, compliance, or supply-chain
  claim.

## Cross-Reviewer Links

Security and Privacy owns baseline identity, secret, privacy, exposure, and
supply-chain triage. Application Security owns source-level attack paths and
application dependency exploitability. Cloud Security owns cloud, IAM, network,
deployment, registry, and runtime control effectiveness. Business Continuity
owns recovery and control transfer. Product Value owns implemented or promised
product value. This reviewer owns only requirement-to-evidence mapping,
limitations, and validation routes.
