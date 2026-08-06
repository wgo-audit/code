# Reviewer Blueprint

Use this only to add or redesign a reviewer. It is not loaded by an audit run.
Follow `reviewer-contract.md` for the package, metadata, discovery,
installation, substitution, dependency, and orchestrator interfaces.

## Roles

The audit coordinator approves scope, chooses order, reads handoffs, and
synthesizes. A reviewer owns one assessment question, its evidence
reconciliation, artifacts, report, and handoff. A collector is optional,
inspects one non-overlapping evidence slice, and returns a concise packet; it
never writes audit artifacts or calls another collector. A shared collector is
reusable across reviewers and writes one packet under `evidence/packets/`.

```text
Audit coordinator → reviewer → optional evidence collectors → reviewer artifacts + handoff
```

Start a reviewer without inherited coordinator chat history. Give it the audit
paths, its card, and only relevant upstream handoffs. The reviewer does not
receive collector prompts; each collector receives only its own prompt.

## Reviewer Card

Create `references/reviewers/<reviewer-id>/reviewer.md` for a core package or
`plugins/wgo-reviewers/<reviewer-id>/reviewer.md` for an external package. Use:

```yaml
id: <stable-kebab-id>
name: <reader-facing name>
summary: <one assessment question>
version: 0.1
codegraph: none | optional | required
depends_on:
  - <core-reviewer-id>
# omit depends_on only when there is no prerequisite reviewer
# external only, when it replaces one core perspective:
supersedes: <core-reviewer-id>
```

Then include Objective and Business Questions, Output Menu, Required Evidence
Packets And Artifact Routes, Recommended Inputs and Downstream Use, Completion
Criteria, Escalation Conditions, and Cross-Reviewer Links. Add an Evidence
Collectors table only when separate,
non-overlapping source slices materially reduce reviewer work.

Recommended inputs may name shared evidence and completed `depends_on`
handoffs only. Put same-wave and later reviewers under downstream use. Keep
every reviewer-owned conditional artifact, including diagrams, under one
`controls/<namespace>/` root; `controls/open-items.md` remains shared.

Keep the reviewer task prompt to 22 lines or fewer. It should tell the reviewer
to inspect approved evidence, reconcile collector packets, create only selected
artifacts, write `report.md` and `handoff.md`, and state unknowns. Do not embed
templates, collector prompts, or every other reviewer's instructions.

## Optional Evidence Collectors

Place a collector prompt at `references/reviewers/<reviewer-id>/workers/<scope>.md`
for a core package or beside an external package's `reviewer.md`.
Keep it to 25 lines or fewer. Define one evidence boundary, exact expected packet, source limits,
and what it must not infer. Give collectors non-overlapping scopes and use only
enough to cover a broad repository; a narrow reviewer runs alone.

The reviewer deduplicates packets, decides record versus gap, creates artifacts,
and writes the handoff. This is one reviewer responsibility, not a separate
administrative agent.

## Shared Evidence Collectors

Place reusable prompts at `references/collectors/<scope>.md`. Keep each prompt
to 25 lines or fewer. A shared collector runs only when its source/action is
approved in the audit brief and a selected reviewer requests its packet. It
writes `evidence/packets/<scope>.md` from the evidence-packet template and
registers reusable material observations in the ledger. It must not write a
reviewer report, control, decision record, diagram, or operator aid.

Reviewers load only the packets named on their cards. A packet is evidence, not
a conclusion: the reviewer reconciles conflicts and decides whether it supports
an artifact or exposes a gap. Do not create packet collectors merely to scan
code again; CodeGraph and direct code collection remain reviewer/collector work.

## CodeGraph Profile

CodeGraph is for code topology only: symbols, callers, callees, dependencies,
and paths. Read documentation, configuration, migrations, tests, and history
directly. `required` means use CodeGraph before code collection; `optional`
means use it when direct navigation is insufficient; `none` means do not invoke
it for that reviewer.

| Reviewer | CodeGraph profile |
|---|---|
| Architecture, Product Value, Code Quality | required |
| Business Continuity, Maintenance Cost, Scalability, Security and Privacy | optional |
| Revenue Risk, Expense Exposure, Contributor and Vendor Value, Project Health | none |

Do not create a CodeGraph worker. Only the reviewer invokes it when its profile
permits it. Initialize or sync every distinct Git
root under the audit folder; a monorepo is one root. Always pass the absolute
root: `codegraph init|sync <absolute-root>` or `--path <absolute-root>` for
queries. Workers never invoke CodeGraph.

## Handoff Contract

Each reviewer writes `reviewer-reports/<reviewer-id>/handoff.md` with these
headings: Confirmed Navigation, Constraints And Conflicts, Material Unknowns,
and Downstream Use. Keep it under 150 words, link exact artifacts/evidence, and
state what another reviewer must not assume. It is navigation, not proof.

## Acceptance Check

Before adding a reviewer, verify its metadata and dependencies follow the
contract, its card and collector prompts meet their line limits, its
outputs/handoff paths are explicit, and its CodeGraph profile is declared.
Exercise it on a representative repository and revise it if it misses material
evidence, produces duplicate artifacts, or pulls irrelevant context.
