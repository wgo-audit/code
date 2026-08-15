# Building A WGO Reviewer

This guide explains how to add a self-contained reviewer to WGO without
changing unrelated reviewers or enlarging every audit prompt. It is intended
for reviewer authors and maintainers.

The [canonical reviewer contract](reviewer-contract.md) is authoritative for
coordinator behavior. The [reviewer blueprint](reviewer-blueprint.md) contains
the compact authoring rules used by WGO itself.

## Contents

- [How Reviewers Fit Into WGO](#how-reviewers-fit-into-wgo)
- [Package Layout](#package-layout)
- [Frontmatter Contract](#frontmatter-contract)
- [What Every Reviewer Inherits](#what-every-reviewer-inherits)
- [What Makes A Reviewer Unique](#what-makes-a-reviewer-unique)
- [Writing The Reviewer Card](#writing-the-reviewer-card)
- [Adding Workers](#adding-workers)
- [Dependencies And Core Substitution](#dependencies-and-core-substitution)
- [Version Governance](#version-governance)
- [Optional Analysis Dependencies](#optional-analysis-dependencies)
- [Discovery And Validation](#discovery-and-validation)
- [Author Checklist](#author-checklist)

## How Reviewers Fit Into WGO

A reviewer owns one decision-relevant assessment question. It examines approved
evidence, reconciles conflicts, selects only justified artifacts, and produces:

- `reviewer-reports/<reviewer-id>/report.md`;
- `reviewer-reports/<reviewer-id>/handoff.md`;
- any required or triggered reviewer-owned controls; and
- material updates that the coordinator serializes into shared evidence and
  open-item state.

The coordinator owns onboarding, auditor interaction, reviewer selection,
dependency waves, shared-state serialization, and final synthesis. A reviewer
does not contact the auditor directly. Its workers collect bounded evidence;
they do not make the final judgment or write audit artifacts.

```text
Coordinator → reviewer → optional bounded workers
            ← question or completed reviewer artifacts
```

## Package Layout

One folder is one reviewer:

```text
<reviewer-id>/
├── reviewer.md
├── workers/                       # optional
│   └── <bounded-evidence-slice>.md
├── validate_install.sh            # optional, macOS/Linux
├── install.sh                     # required with validate_install.sh
├── validate_install.bat           # optional, Windows
└── install.bat                    # required with validate_install.bat
```

Core packages live in:

```text
skills/wgo/references/reviewers/<reviewer-id>/
```

Project-local extensions live in the project being audited:

```text
plugins/wgo-reviewers/<reviewer-id>/
```

WGO discovers packages from these paths; there is no separate reviewer
registry. Installing or updating WGO does not replace the project-local
extension root.

For a new reviewer, start from the scaffold at:

```text
skills/wgo/references/reviewer-scaffold/example-reviewer/
```

Copy it to the destination package folder, rename the folder to the final
reviewer ID, and update the frontmatter before changing the body.

## Frontmatter Contract

Every `reviewer.md` begins with YAML frontmatter:

```yaml
---
id: accessibility
name: Accessibility
summary: Can intended users complete critical workflows without material accessibility barriers?
version: 0.1
codegraph: optional
depends_on:
  - architecture
---
```

For an external reviewer that replaces a core perspective:

```yaml
supersedes: security-privacy
```

| Field | Requirement | Meaning |
|---|---|---|
| `id` | Always required | Stable, unique, kebab-case package identity. It should match the package folder. |
| `name` | Always required | Reader-facing reviewer name. |
| `summary` | Always required | One assessment question that explains the reviewer's distinct value. |
| `version` | Always required | Reviewer definition version. Start at `0.1`; increment it when a change can affect results. |
| `codegraph` | Always required | `required`, `optional`, or `none`; CodeGraph is only for code topology. |
| `depends_on` | Required only when prerequisites exist | Core reviewer IDs whose completed handoffs are required before this reviewer can run. Omit the field when there is no prerequisite. |
| `supersedes` | External reviewers only; optional | At most one core reviewer that this package can replace with explicit auditor approval. |

Use `depends_on` only for a real prerequisite. A useful input that can be
absent without invalidating the review belongs under recommended inputs, not in
frontmatter.

Recommended inputs may name shared evidence and completed `depends_on`
handoffs only. A same-wave or later reviewer is a downstream consumer, never an
input to the current run.

## Version Governance

Reviewer versions describe the package contract that produced a finding. Bump a
reviewer's version when a change can alter evidence collection, outputs,
completion criteria, dependencies, escalation, or downstream guidance. Examples:

- adding, removing, or materially changing a worker;
- changing required or conditional outputs;
- changing `depends_on`, `supersedes`, or `codegraph`;
- changing completion or escalation conditions; or
- changing domain-specific evidence rules in the reviewer card.

Do not bump a reviewer version for spelling, formatting, link repair, or a
shared WGO workflow/template change that affects every reviewer equally without
changing this package. If a shared change intentionally changes one reviewer
more than others, bump that reviewer in the same PR and explain why.

On compare and blind-compare runs, WGO records baseline and installed reviewer
versions. A mismatch is not automatically wrong, but the auditor must accept it
before the run continues because the comparison may reflect both target changes
and reviewer-package changes.

## What Every Reviewer Inherits

The shared WGO workflow supplies behavior that reviewer authors should not
duplicate in every card:

- the approved audit brief, evidence boundary, cutoff, and repository paths;
- shared evidence and source-access rules;
- stable evidence, open-item, ADR, PDR, and diagram identifiers;
- same-root rerun disposition and the rule that an identifier is never reused
  for a different subject;
- report and handoff structures;
- uncertainty, contradiction, and documented-out-of-scope handling;
- conditional artifact selection and diagram quality rules;
- decision-useful insights without quotas;
- evidence-supported, mandate-relevant strengths;
- an isolated artifact-quality worker after drafting;
- coordinator-mediated auditor questions; and
- synthesis and audience-specific final reporting.

A reviewer should refer to these common contracts rather than restating them.
This keeps the reviewer focused and makes shared behavior fixable in one place.

The main reviewer reads its card, the shared reviewer workflow, evidence rules,
the reviewer report template, and only the artifact templates it selects. The
artifact-quality rubric goes to the quality worker rather than the main
reviewer. Synthesis-only templates and reconciliation instructions are not
loaded into reviewer context.

## What Makes A Reviewer Unique

A reviewer package defines only what differs from other perspectives:

- its assessment question and business decisions;
- required and conditional outputs;
- evidence packets it can reuse and the artifact routes they support;
- recommended predecessor evidence and downstream consumers;
- completion and escalation conditions;
- its CodeGraph profile; and
- optional workers for genuinely separate evidence slices.

Examples:

- Product Value distinguishes implemented, partial, promised, and approved
  customer value.
- Security and Privacy reconciles security claims, trust anchors, identity,
  secrets, data boundaries, exposure, and material abuse paths.
- Code Quality inventories declared quality gates and examines fixture
  provenance, test boundaries, change safety, and relevant runtime/build
  surfaces.

These details belong in the reviewer package, not in the shared workflow.

## Writing The Reviewer Card

After the frontmatter and title, use these sections:

1. `## Objective And Business Questions`
2. `## Output Menu`
3. `## Required Evidence Packets And Artifact Routes`
4. `## Recommended Inputs And Downstream Use`
5. `## Evidence Collectors` — only when workers are justified
6. `## Completion Criteria`
7. `## Escalation Conditions`
8. `## Cross-Reviewer Links`

The output menu distinguishes:

- **Required:** always produced by this reviewer;
- **Conditional:** produced when a plain-language trigger is evidenced; and
- **Not owned:** linked to the reviewer that owns the conclusion.

Do not create a conditional artifact merely to mark it not applicable. When a
required or triggered artifact cannot responsibly be created, the report gives
one concise evidence gap and closure route.

Keep all reviewer-owned conditional outputs, including diagrams, under one
`controls/<namespace>/` root. The namespace may be shorter than the reviewer
ID. Shared `controls/open-items.md` is not reviewer-owned and is exempt.

Keep the card declarative and compact. Do not paste shared templates, worker
prompts, other reviewer cards, generic audit advice, or extensive tool
instructions into it.

## Adding Workers

Workers are useful when a broad reviewer has independent source slices that can
be collected in parallel. Do not add a worker for a narrow reviewer or to move
administrative work away from the reviewer.

Each worker:

- examines one non-overlapping evidence boundary;
- returns a concise evidence packet to its reviewer;
- uses exact file, line, symbol, command, or hosted-source locators;
- states observed, inferred, and unknown boundaries;
- does not write audit artifacts or shared state;
- does not ask the auditor or delegate again; and
- does not invoke CodeGraph.

Keep a worker prompt to 25 lines or fewer. The reviewer performs one CodeGraph
topology preflight when its profile permits it, gives workers the useful
topology result, reconciles their packets, and owns every conclusion.

Shared collectors under `skills/wgo/references/collectors/` are different:
they create reusable evidence packets for multiple reviewers. Add one only when
the evidence is genuinely cross-reviewer. A package-specific worker is the
simpler default.

## Dependencies And Core Substitution

During onboarding, WGO resolves declared dependencies into execution waves.
All currently unblocked reviewers can run concurrently; their results are
reconciled before dependent reviewers begin.

Selecting a reviewer does not silently select missing dependencies. WGO names
the dependency and asks the auditor whether to include it. If it is declined,
the dependent reviewer is unavailable for that audit.

An external reviewer with `supersedes` is still optional. If approved:

- it replaces the named core reviewer rather than running beside it;
- the audit brief records the substitution and portable package locator;
- dependencies on the core ID resolve to the replacement; and
- WGO asks the auditor to choose if multiple extensions replace the same core
  reviewer.

## Optional Analysis Dependencies

Most reviewers need no installer. In that case, include no validation or
installation scripts.

When an extension needs an external analysis dependency, provide the platform
pair:

```text
validate_install.sh + install.sh
validate_install.bat + install.bat
```

The validation script must be read-only:

- exit `0` when the reviewer is ready;
- return a non-zero exit code when installation is needed; and
- never modify the audited product.

For an approved extension, the coordinator runs the platform validator using
its absolute path. On a non-zero result, WGO pauses and tells the auditor to run
the matching installer by its full absolute path. WGO never runs the extension
installer itself. After the auditor reports completion, WGO reruns the
validator.

## Discovery And Validation

There are three distinct validation layers:

Reviewer-package contract validation is coordinator-driven during onboarding,
with repository tests protecting bundled core reviewers. Authors can run
`skills/wgo/scripts/validate_reviewer_contract.py` before a PR for a quick
structural check. An extension's `validate_install` script checks only whether
its own analysis dependencies are ready; it does not validate reviewer metadata
or audit quality.

### 1. Package discovery during onboarding

The coordinator rejects a package as unavailable when it finds:

- missing or malformed required metadata;
- an invalid `codegraph` value;
- duplicate reviewer IDs;
- an unknown dependency;
- a dependency cycle;
- an invalid external `supersedes` relationship; or
- a platform validator without its matching installer; or
- more than one reviewer-owned `controls/<namespace>/` root.

It reports the reason rather than silently repairing the package.

### 2. Repository contract tests

WGO's own test suite validates the bundled core packages, including:

- the expected package layout and required reviewer sections;
- declared CodeGraph profiles and core dependency waves;
- compact, bounded workers that do not invoke CodeGraph;
- worker counts and reviewer-specific evidence routes where contract-critical;
- extension discovery, substitution, installation, and coordinator boundaries;
  and
- shared stable-ID, evidence, report, artifact-quality, and question-routing
  behavior.

These tests protect core WGO packages. A project-local extension is evaluated
at onboarding from its package contract and can also be checked with
`validate_reviewer_contract.py`; it is not automatically added to WGO's
repository test suite.

### 3. Generated-audit validation

`skills/wgo/scripts/validate_audit_structure.py` validates generated audit
artifacts, not reviewer packages. It checks required audit files, report and
handoff sections, stable-ID formats and duplication, core table schemas and
controlled values, evidence cutoff labels, required decision inventories and
registers, final-report sections, decision and diagram structure, operator-aid
structure, and obvious credential-like leakage.

This validator is optional and structural. It does not judge whether an
external reviewer is insightful, whether its evidence is sufficient, or
whether its conclusions are correct.

### 4. Reviewer-package validator

`skills/wgo/scripts/validate_reviewer_contract.py` validates one or more
reviewer package folders or `reviewer.md` files. It checks required
frontmatter, version format, required sections, worker line limits and
boundaries, installer pairs, dependency IDs, `supersedes`, and the single
reviewer-owned control namespace rule. It does not run the reviewer or inspect
the audited product.

```bash
python3 skills/wgo/scripts/validate_reviewer_contract.py \
  skills/wgo/references/reviewers/security-privacy \
  --core-id architecture \
  --core-id security-privacy
```

For a project-local extension that uses `supersedes`, add `--external`.

## Author Checklist

Before proposing a reviewer:

- [ ] Give it one distinct, decision-relevant assessment question.
- [ ] Use a unique kebab-case `id` and valid frontmatter.
- [ ] Start from `references/reviewer-scaffold/example-reviewer/` when creating
      a new package.
- [ ] Bump `version` only when package behavior can affect results.
- [ ] Declare only true prerequisites in `depends_on`.
- [ ] Use `supersedes` only for an optional external replacement of one core
      reviewer.
- [ ] Separate required, conditional, and not-owned outputs.
- [ ] Reuse shared evidence packets where appropriate.
- [ ] Add workers only for non-overlapping evidence slices.
- [ ] Keep every worker at 25 lines or fewer and prohibit nested delegation.
- [ ] Define completion, escalation, and downstream boundaries.
- [ ] Add dependency scripts only when an external tool is genuinely required.
- [ ] Exercise the reviewer on a representative repository.
- [ ] Run `validate_reviewer_contract.py` before opening the PR.
- [ ] Revise it if it misses material evidence, produces duplicate artifacts,
      or pulls irrelevant context.
