# Report Manifest Format

Status: implemented
Schema version: `1.0.0`

## Purpose

Every published audit report contains a `manifest.json`. The manifest is a
small, machine-readable index that tells WGO and future processors:

- what report this is;
- what subject was assessed;
- why the audit was performed and what it concluded;
- which evidence boundary applies;
- how the report was produced; and
- the latest API-equivalent execution-cost result, when calculated; and
- how it relates to previous or comparison reports.

The report remains authoritative. The manifest does not copy findings,
recommendations, evidence, open items, or report prose.

WGO creates the initial manifest after `executive-summary.md` and the other
audience reports are final, then updates its cost summary after every cost
calculation or refresh. Onboarding records stable business-concern IDs in
`audit-brief.md`; upload verifies and packages the completed manifest but does
not create or revise it.

## Top-Level Contract

```json
{
  "$schema": "https://wgo-audit.com/schemas/manifest/1.0.0.json",
  "schemaVersion": "1.0.0",
  "report": {},
  "subject": {},
  "audit": {},
  "businessConcerns": [],
  "evidence": {},
  "execution": {},
  "relationships": {}
}
```

| Field | Purpose |
|---|---|
| `$schema` | Exact schema used to validate and interpret the manifest. |
| `schemaVersion` | Version used by processors to select compatible behavior. |
| `report` | Stable identity, title, entrypoint, and optional headline. |
| `subject` | Product, service, project, organization, or other thing assessed. |
| `audit` | Assessment type, mode, and depth. |
| `businessConcerns` | Reasons for the audit paired with their conclusions. |
| `evidence` | Cutoff, pinned sources, access boundary, and limitations. |
| `execution` | Generator, reviewer, and latest cost-estimate provenance needed for repeatability. |
| `relationships` | Links to previous, baseline, comparison, or superseded reports. |

Do not add website presentation fields, mutable Git or pull-request state,
local paths, agent session IDs, credentials, or raw usage records.

## Core Fields

### Report

| Field | Requirement | Meaning |
|---|---|---|
| `id` | Required | Stable report identifier that does not depend on its directory. |
| `title` | Required | Reader-facing report title. |
| `entrypoint` | Required | Relative path to the report start page. |
| `generatedAt` | Optional | Supported ISO date or timestamp; do not invent precision. |
| `language` | Optional | Report language, such as `en`. |
| `headline` | Optional | One concise overall rating and statement. |

### Subject

| Field | Requirement | Meaning |
|---|---|---|
| `id` | Required | Stable subject identifier and published `audits/<subject>/` directory. |
| `name` | Required | Reader-facing subject name. |
| `kind` | Required | Controlled subject type. |
| `description` | Optional | Concise description of the assessed subject. |
| `canonicalUrl` | Optional | Canonical public URL when supported. |

Recommended `kind` values are `software-project`, `service`, `product`,
`repository`, `repository-group`, `organization`, `platform`,
`infrastructure`, `operating-environment`, `system`, and `other`.

### Audit

| Field | Requirement | Meaning |
|---|---|---|
| `type` | Required | Stable identifier for what was assessed, not a display label. |
| `mode` | Required | `baseline`, `improve`, `compare`, `blind-compare`, or `unknown`. |
| `depth` | Required | `light`, `standard`, `deep`, or `custom`. |

## Business Concerns And Conclusions

`businessConcerns` is the central reason for the manifest. It preserves why the
audit was commissioned and pairs each material concern with the conclusion
supported by the report.

Business input may originally be a question, concern, mandate, decision, or
harmful failure to avoid. Store each material input without changing its
meaning:

```json
{
  "id": "production-approval-readiness",
  "type": "question",
  "statement": "Does the available evidence support approving DocuSeal for production use?",
  "conclusion": {
    "outcome": "no",
    "statement": "No",
    "summary": "The audit supports continued evaluation, not production approval.",
    "confidence": "high",
    "source": "index.md"
  }
}
```

### Concern fields

| Field | Requirement | Meaning |
|---|---|---|
| `id` | Required | Stable identifier reused when later audits reassess the same concern. |
| `type` | Required | `question`, `concern`, `mandate`, `decision`, or `failure-mode`. |
| `statement` | Required | Concise approved concern without changing its intent. |
| `conclusion` | Required | Evidence-supported answer from this report. |

### Conclusion fields

| Field | Requirement | Meaning |
|---|---|---|
| `outcome` | Required | `yes`, `partial`, `no`, `unknown`, or `not-applicable`. |
| `statement` | Required | Short reader-facing answer, such as `No` or `Continue evaluation conditionally`. |
| `summary` | Optional | Concise explanation when the short answer is insufficient. |
| `confidence` | Optional | `high`, `medium`, `low`, or `unknown`. |
| `source` | Optional | Relative link to the report page supporting the conclusion. |

For a question, `yes`, `partial`, and `no` are its answer. For a concern,
`yes` means the concern is substantiated. For a mandate or decision whose
answer is conditional, use `partial` and preserve the decision in
`conclusion.statement`.

Do not use changing question text as the identifier. Reusing the same `id`
allows processors to compare conclusions after reader-facing wording is
clarified.

### DocuSeal concern examples

```json
[
  {
    "id": "foundation-for-further-evaluation",
    "type": "mandate",
    "statement": "Assess whether DocuSeal Community is a sound foundation for further technical evaluation and vendor discussions.",
    "conclusion": {
      "outcome": "partial",
      "statement": "Continue evaluation conditionally",
      "summary": "The Community signing core is substantive and inspectable, while production reliance remains gated by unresolved evidence and decisions.",
      "confidence": "high",
      "source": "index.md"
    }
  },
  {
    "id": "continue-stop-decision",
    "type": "decision",
    "statement": "Should the organization continue evaluating DocuSeal, continue conditionally, or stop?",
    "conclusion": {
      "outcome": "partial",
      "statement": "Continue evaluation conditionally",
      "summary": "Further vendor and specialist evaluation is justified, but the report does not approve production use.",
      "confidence": "high",
      "source": "executive-summary.md"
    }
  },
  {
    "id": "production-approval-readiness",
    "type": "question",
    "statement": "Does the available evidence support approving DocuSeal for production use?",
    "conclusion": {
      "outcome": "no",
      "statement": "No",
      "summary": "Target architecture, Pro capabilities, identity binding, evidence trust, recovery, capacity, ownership, and specialist determinations remain unresolved.",
      "confidence": "high",
      "source": "index.md"
    }
  }
]
```

## Evidence

Required fields are:

- `cutoff`: ISO date through which evidence is eligible;
- `sources`: source objects, including the full resolved commit for every Git
  source when known; and
- `accessBoundary`: controlled access level plus optional included and excluded
  evidence descriptions.

`limitations` is an optional array of structured `code`, `description`, and
`impact` objects.

Recommended source `kind` values include `git-repository`, `document-set`,
`website`, `api-export`, `cloud-configuration`, `runtime-observation`,
`interview`, `test-result`, and `other`.

Recommended access levels are `public-only`, `authorized-private`, `mixed`, and
`unknown`.

## Execution

`generator` identifies the system that produced the report and is not
restricted to WGO. It records `name` and, when supported, `repository`,
`version`, and `commit`.

`platform`, `reviewers`, and `acceptedVariances` are optional for other
generators. WGO records its runtime when known and every selected reviewer with
its actual `id`, `version`, and `status`.

Reviewer status values are `completed`, `partial`, `not-run`, `failed`, and
`not-applicable`. A missing or null version must never be interpreted as
version `0`.

### Cost Estimate

After every cost calculation or refresh, WGO stores one lean summary at
`execution.costEstimate`:

```json
"costEstimate": {
  "basis": "api-equivalent",
  "coverage": "audit",
  "status": "final",
  "currency": "USD",
  "totalUsd": 12.35,
  "source": "controls/cost-estimate.md"
}
```

`coverage` is `audit` or `audit-and-operationalization`; a later calculation
replaces the earlier object. `status` is `final` or `unreconciled`. Round
manifest monetary values half up to dollars and cents; exact fractional values
remain in the linked calculation evidence. For an unreconciled result, set
`totalUsd` to `null` and optionally include `reconciledSubtotalUsd` when the
detailed control supports a subtotal for included evidence. The linked control
remains authoritative for models, tokens, pricing inputs, exclusions, and
limitations.
The field may be `null` only before WGO's first cost calculation, and may be
omitted by another generator that does not calculate cost.

## Relationships

```json
"relationships": {
  "previousAudit": null,
  "baseline": null,
  "comparesTo": [],
  "supersedes": null
}
```

Relationships contain stable report IDs, not local paths. `previousAudit` is
the chronological predecessor for the same subject. `baseline` is the report
formally selected as the baseline; it may be different from the previous
report.

## Complete DocuSeal Example

This example uses evidence-supported values from the completed DocuSeal audit.
Null values remain where the audit does not establish generator version,
generator commit, runtime version, or model IDs.

```json
{
  "$schema": "https://wgo-audit.com/schemas/manifest/1.0.0.json",
  "schemaVersion": "1.0.0",
  "report": {
    "id": "docuseal-2026-08-06-regulated-esignature-readiness",
    "title": "DocuSeal Regulated eSignature Readiness Audit",
    "generatedAt": null,
    "language": "en",
    "entrypoint": "index.md",
    "headline": {
      "rating": "material-gaps",
      "statement": "DocuSeal Community is a substantive foundation for further evaluation, but production reliance remains conditional on unresolved technical, vendor, specialist, and operating evidence."
    }
  },
  "subject": {
    "id": "docuseal",
    "name": "DocuSeal",
    "kind": "software-project",
    "description": "Self-hosted electronic-signature platform evaluated from the Community repository and approved public sources",
    "canonicalUrl": "https://www.docuseal.com"
  },
  "audit": {
    "type": "regulated-esignature-readiness",
    "mode": "improve",
    "depth": "deep"
  },
  "businessConcerns": [
    {
      "id": "foundation-for-further-evaluation",
      "type": "mandate",
      "statement": "Assess whether DocuSeal Community is a sound foundation for further technical evaluation and vendor discussions.",
      "conclusion": {
        "outcome": "partial",
        "statement": "Continue evaluation conditionally",
        "summary": "The Community signing core is substantive and inspectable, while production reliance remains gated by unresolved evidence and decisions.",
        "confidence": "high",
        "source": "index.md"
      }
    },
    {
      "id": "continue-stop-decision",
      "type": "decision",
      "statement": "Should the organization continue evaluating DocuSeal, continue conditionally, or stop?",
      "conclusion": {
        "outcome": "partial",
        "statement": "Continue evaluation conditionally",
        "summary": "Further vendor and specialist evaluation is justified, but the report does not approve production use.",
        "confidence": "high",
        "source": "executive-summary.md"
      }
    },
    {
      "id": "production-approval-readiness",
      "type": "question",
      "statement": "Does the available evidence support approving DocuSeal for production use?",
      "conclusion": {
        "outcome": "no",
        "statement": "No",
        "summary": "Target architecture, Pro capabilities, identity binding, evidence trust, recovery, capacity, ownership, and specialist determinations remain unresolved.",
        "confidence": "high",
        "source": "index.md"
      }
    }
  ],
  "evidence": {
    "cutoff": "2026-08-06",
    "sources": [
      {
        "id": "primary-code",
        "kind": "git-repository",
        "repository": "docusealco/docuseal",
        "url": "https://github.com/docusealco/docuseal",
        "ref": "3.1.7",
        "commit": "a2d8b855491793870b7b4acf176d2d95ae95ff83",
        "role": "primary"
      },
      {
        "id": "public-product-material",
        "kind": "website",
        "url": "https://www.docuseal.com",
        "role": "supporting"
      }
    ],
    "accessBoundary": {
      "level": "public-only",
      "included": [
        "Pinned Community repository and public GitHub evidence",
        "Approved public DocuSeal website material"
      ],
      "excluded": [
        "DocuSeal Pro implementation",
        "DocuSeal hosted cloud service",
        "Organization production and live-state evidence",
        "Legal, regulatory, and specialist determinations"
      ]
    },
    "limitations": [
      {
        "code": "PRO_IMPLEMENTATION_UNAVAILABLE",
        "description": "Pro implementation was not available for inspection.",
        "impact": "Pro-only API, webhook, embedding, SSO, role, and phone-verification behavior could not be assessed."
      },
      {
        "code": "NO_PRODUCTION_VALIDATION",
        "description": "No penetration, load, deployment, recovery, or production test was performed.",
        "impact": "Production security, capacity, recovery, and operating readiness remain unproved."
      }
    ]
  },
  "execution": {
    "generator": {
      "name": "wgo-audit",
      "repository": "wgo-audit/code",
      "version": null,
      "commit": null
    },
    "platform": {
      "runtime": "codex",
      "runtimeVersion": null,
      "models": []
    },
    "reviewers": [
      { "id": "architecture", "version": "0.2", "status": "completed" },
      { "id": "business-continuity", "version": "0.2", "status": "completed" },
      { "id": "code-quality", "version": "0.2", "status": "completed" },
      { "id": "contributor-vendor-value", "version": "0.2", "status": "completed" },
      { "id": "expense-exposure", "version": "0.2", "status": "completed" },
      { "id": "maintenance-cost", "version": "0.2", "status": "completed" },
      { "id": "product-value", "version": "0.2", "status": "completed" },
      { "id": "project-health", "version": "0.2", "status": "completed" },
      { "id": "revenue-risk", "version": "0.2", "status": "completed" },
      { "id": "scalability", "version": "0.2", "status": "completed" },
      { "id": "security-privacy", "version": "0.2", "status": "completed" }
    ],
    "acceptedVariances": [],
    "costEstimate": {
      "basis": "api-equivalent",
      "coverage": "audit",
      "status": "unreconciled",
      "currency": "USD",
      "totalUsd": null,
      "reconciledSubtotalUsd": 151.49,
      "source": "controls/cost-estimate.md"
    }
  },
  "relationships": {
    "previousAudit": null,
    "baseline": null,
    "comparesTo": [],
    "supersedes": null
  }
}
```

## Unknown Values And Validation

- Do not invent generator versions, commits, dates, model names, reviewer
  versions, relationships, sources, or conclusions.
- Omit unsupported optional fields. Use `null`, `[]`, or a controlled `unknown`
  value only where the retained field is genuinely unknown.
- Every filesystem path in every audit artifact is portable and relative:
  audit-artifact paths are relative to the audit root, and source paths use a
  stable source ID plus a path relative to that source root. Never ship
  unresolved placeholders, absolute local paths, credentials, or agent session
  identifiers.
- `subject.id` must match the published subject directory.
- `evidence.cutoff` must match the published cutoff directory.
- `report.entrypoint` must exist in the report package.
- Business-concern IDs must be unique within the report.
- Git commits must be full 40-character SHAs when present.
- Every WGO reviewer entry must include `id`, `version`, and `status`.
- A final cost must have a non-negative `totalUsd` rounded to cents; an
  unreconciled result must use `null` and must not disguise a partial subtotal
  as the total.
- `execution.costEstimate.source` must be a relative path to an existing
  report artifact.
- Relationship values must identify reports, not filesystem locations.

## Deliberate Omissions

The manifest does not contain the complete mandate, detailed findings,
recommendations, open items, evidence ledger, detailed cost-calculation
records, report file inventory, website labels, badges, or mutable publication
state. Those remain in their source artifacts or are derived by processors.
