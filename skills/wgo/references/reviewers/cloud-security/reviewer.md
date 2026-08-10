---
id: cloud-security
name: Cloud Security
summary: Do the available cloud, IAM, network, deployment, and runtime controls enforce the intended boundaries?
version: 0.1
codegraph: optional
depends_on:
  - architecture
  - security-privacy
---

# Reviewer: Cloud Security

## Objective And Business Questions

Assess evidence-bounded cloud, IAM, network, deployment, registry, and runtime
control effectiveness for the environments in scope. Focus on whether available
configuration and live-state evidence enforces the intended boundaries, not on
application-level vulnerability coverage or recoverability conclusions.

## Output Menu

| Category | Output and canonical path | Trigger |
|---|---|---|
| Required | Cloud security assessment | Always, in `reviewer-reports/cloud-security/report.md` |
| Conditional | Cloud/IAM/network/runtime control view in `controls/cloud-security/` | Material cloud account, IAM, ingress, segmentation, secret, workload, registry, image, IaC, or runtime boundary evidence is available |
| Conditional | Deployment and environment exposure view in `controls/cloud-security/` | CI/CD, registry, image provenance, environment promotion, or runtime exposure could change transition-control risk |
| Not owned | Source-level AppSec, application dependency exploitability, continuity/recovery, compliance status, or architecture topology | Link Application Security, Business Continuity, Compliance Assurance, or Architecture |

## Required Evidence Packets And Artifact Routes

| Packet | When to collect | Reuse and artifact route |
|---|---|---|
| `live-environment-and-access` | Approved cloud, IAM, DNS, certificate, runtime, registry, secret metadata, or environment inventory is needed | Reconcile effective cloud control posture; link from control views |
| `github-history-and-hosted-ci` | Hosted CI/CD, deployment provenance, registry/image build route, or IaC history could change control confidence | Link from deployment and environment exposure view |

## Recommended Inputs And Downstream Use

Read the brief, named shared packets, and only completed `depends_on` handoffs:
Architecture, Security and Privacy. Use Architecture for topology and runtime
boundaries. Use Security and Privacy for baseline identity, secret, exposure,
privacy, and supply-chain boundary routing. Downstream Business Continuity may
consume operational-control limits; Compliance Assurance may map validated
control findings to named requirements.

## Evidence Collectors

Use collectors only for broad repositories or multi-environment evidence. The
reviewer reconciles packets and writes artifacts; collectors never call
CodeGraph or shared collectors.

| Collector | Scope | Prompt |
|---|---|---|
| Cloud, IAM, and network controls | Accounts/projects, IAM, service identities, policies, network paths, ingress, DNS/TLS/WAF, segmentation, and admin access | `workers/cloud-iam-network-controls.md` |
| Deployment, registry, and runtime controls | IaC, CI/CD deployment routes, image/registry controls, environment promotion, runtime configuration, secrets metadata, monitoring, and logging | `workers/deployment-registry-runtime-controls.md` |

## Completion Criteria

State material cloud, IAM, network, deployment, registry, and runtime controls;
effective boundaries; evidence limits; and closure routes without claiming
complete cloud posture, active compromise assessment, or recovery readiness.

## Escalation Conditions

- Admin, service identity, public exposure, or runtime boundary evidence is
  missing or contradictory on a critical environment.
- A deployment, registry, image, IaC, or secret-management path could bypass
  intended control transfer or environment separation.
- Live or configuration evidence suggests public exposure, over-broad privilege,
  or unowned cloud resources.

## Cross-Reviewer Links

Architecture owns topology and component boundaries. Security and Privacy owns
baseline identity, secret, privacy, exposure, and supply-chain triage.
Application Security owns source-level attack paths and application dependency
exploitability. Business Continuity owns recovery and control transfer.
Compliance Assurance owns requirement mapping and certification boundaries.
