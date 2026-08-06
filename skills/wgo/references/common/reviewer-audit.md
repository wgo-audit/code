# Reviewer Audit Workflow

Use for `wgo:audit <reviewer-id>`. A reviewer is a bounded evidence-to-artifact loop,
not a parallel state system.

## Inputs And Output Selection

Read `audit-brief.md`, the reviewer card, its relevant predecessor handoffs,
and only named shared evidence packets and linked artifacts relevant to the
reviewer question. Confirm the reviewer is selected; detailed work is the
standard.

When the brief records `rerun-all` and this reviewer has prior outputs, also
read its prior report, handoff, linked evidence, controls, open items, and
decisions. Use them to target collection, but verify direct evidence and
challenge every material conclusion. Explicitly retain, revise, supersede, or
close prior findings; prior prose and completion state are not proof.

Run a
card-listed shared collector when it supports the reviewer question and its
packet is absent or stale. Shared collectors are internal and available by
default. For a supplied GitHub repository or current-folder GitHub origin, use
public data and private data available through the existing session; record a
limit if any material portion is inaccessible. Start inspecting evidence before
reading templates for outputs that have not been selected.

Each reviewer card identifies required outputs, conditional outputs with a
plain-language trigger, not-owned outputs to link, and canonical paths. Create
all required outputs at detailed depth. Create a conditional output only when
its trigger is met. If a required or triggered output cannot be responsibly
produced, state one concise material omission in the report with the evidence
gap and a closure route. Do not make routine `not-applicable` rows.

For detailed work, create a source-bounded diagram whenever it materially
reduces reader ambiguity about a flow, boundary, dependency, state transition,
or ownership handoff. Missing live evidence is not a reason to omit it: show
the unknown boundary. Only a named diagram whose trigger explicitly requires
live evidence remains blocked without that evidence.

For a horizontally arranged flow, use `flowchart TB` for the outer graph and
compact `direction LR` stage subgraphs. Connect stage boundaries, rather than
a node inside one stage directly to a node outside it, so Mermaid preserves the
stage direction. When exact cross-stage node links matter, use a plain
`flowchart TB`; never use a bare `flowchart LR` or `useMaxWidth: false` to make
a wide diagram fit.

## Evidence And Questions

Register reusable evidence in `evidence/evidence-ledger.md`. Record a
source-access event only when access is materially relevant. Keep source,
live-state, stakeholder, approval, and future-intent evidence distinct.

When `documentation/catalog.md` exists, search it by the current reviewer ID
and topic instead of loading it in full, including matching rows in its
referenced-content and coverage-signal sections. Give each collector only its
relevant catalog rows and paths. The catalog is navigation metadata, not
evidence; read and cite the available original document and section. Treat an
unresolved reference or coverage signal as a search lead or evidence limit, not
proof or an automatic finding. The reviewer decides materiality and routes a
remaining proof, authority, or correction need through the normal open-item
rules. CodeGraph is not used for documentation.

For CodeGraph, use the absolute Git root for the code being examined. Use
`codegraph status|sync <absolute-root>` for lifecycle checks and `--path
<absolute-root>` for queries, context, callers, callees, impact, files, or
affected. Never rely on the current working directory; workers do not invoke
CodeGraph.

For a material gap, first inspect available evidence, then choose its route:

- Return one exact question to the coordinator when it concerns mandate,
  acceptable success outcome, priority, or authority the auditor can exercise;
  the answer must be available from the auditor and capable of changing
  remaining scope, acceptance criteria, or the headline conclusion. The
  reviewer never contacts the auditor. Create a `decision-needed` item until
  answered; do not bury the question in the report.
- Use a `verification` when proof of a fact, implementation, access, or live
  state is required. Do not ask the auditor to prove such a fact by assertion.
- Use `decision-needed` without an auditor question when another authority must
  decide. Use `action` when the correction is already clear.

Do not complete a reviewer while a material topic has been silently skipped.

When an examined source names a material document, system, or repository outside
the approved boundary, apply the shared `Documented outside audited scope; not
independently verified.` wording. Link the pointer and state the smallest useful
scope expansion; do not report it as missing or silently substitute a proxy.

For an executable check, record exact working directory, command, intended
coverage, tool versions when known, pass/fail/error/skip outcome, dependency
state, installation authorization, and bounded conclusion. Never install
packages, restore dependencies, change lockfiles, or otherwise alter the
workspace without explicit authorization.

## Decision Usefulness

For every Key Findings row, assign severity, effort, and optional taxonomy from
the evidence. Severity is consequence-based: `Critical` for exploitable
security exposure, data-loss risk, or production-failure conditions; `High` for
material risk likely in normal operation; `Medium` for meaningful contained or
near-term-unlikely risk; and `Low` for minor cleanup or hardening. Effort is
the smallest responsible next move: `S` for a local/single-owner proof or
change, `M` for coordinated multi-file/process work, and `L` for broad
architecture, governance, migration, or external-party work. Use taxonomy only
when it is a direct fit, such as CWE, ASVS, SLSA, OSPS, or a project-defined
control label; otherwise write `none`.

Derive zero or more decision insights from the reviewed evidence. An insight
names the decision it changes, the causal relationship or conflict behind it,
the consequence of a wrong choice, and the smallest next proof or action. A
fact, generic risk label, or unsupported recommendation is not an insight.
Do not create an insight to fill a count. Combine facts that change the same
decision; retain every independent material decision rather than imposing a
maximum.

For a material open item, use its existing `Type` as the next-move lane:
`decision-needed` means decision now, `verification` means evidence needed, and
`action` means implementation correction. Use `risk` only when no responsible
next move can yet be stated. Priority orders work within its lane, not across
lanes: assign P1 only when delay blocks safe operation, release, or transfer;
do not elevate an item merely because it is material.

## Reviewer And Collector Boundaries

The audit coordinator starts the reviewer with the brief, its approved package
path, only named shared evidence packets, and relevant handoffs. The reviewer owns evidence
reconciliation and all artifacts. It invokes card-listed collectors only for
non-overlapping, broad source slices; collectors return packets and never write
audit state or contact the auditor. Shared collectors write their own concise packets under
`evidence/packets/`; they never write reviewer artifacts.

## Produce And Close

Create selected artifacts from their templates. Label uncertainty in the
artifact. Update `controls/open-items.md` only for material work needing an
owner, authority, or future proof. An ADR/PDR is an observed decision or durable
behavior and is never an open-item substitute.

Before writing the report, delegate one bounded quality worker and tell it to
read `artifact-quality-review.md`. Give it the reviewer question, draft outputs,
and their cited evidence. The reviewer does not read the worker rubric. Revise
the selected outputs once from its feedback; the worker writes no artifact,
shared state, or gate.

On a resume in the same audit root, read the prior open-items table and relevant
decision inventory/register before writing. For each material prior open item,
retain its identifier and mark it `open`, `verified-fixed`, `superseded`, or
`out-of-current-scope`; a materially changed item receives a new ID linked to
the superseded item. For an ADR/PDR, retain its decision ID and existing decision
status; only mark it `superseded` when a later decision replaces it. Never reuse
an ID for a different item or decision. Allocate a new OI/ADR/PDR ID only after
the current highest ID of that family in this audit root.

Write `reviewer-reports/<reviewer-id>/report.md` with
`reviewer-report-template.md`.
It links evidence and outputs, records material omissions and reconciliation,
and ends with a bounded conclusion. Include `### Decision Insights` only when
one or more meet the decision-usefulness standard. Write the fixed, under-150-word
`handoff.md`; it links navigation evidence and states what downstream reviewers
may use and must not assume. Record any material auditor question raised and its
current route in the report. Once the auditor answers at the wave boundary, the
coordinator records the answer and effect in the audit brief and existing open
item for downstream reviewers. The handoff is navigation, not proof.

Structural validation is optional. When useful and an interpreter is available,
the reviewer may run the audit root's canonical `validate_audit_structure.py`
without installing anything: use `python3` or `python`; if neither is available,
reuse the Python interpreter installed for approved PyMuPDF4LLM support, if
present. If validation is not run, add this warning with the reason to the
report, handoff, and checklist: `Structural validation not run: <reason>.`

If the validator runs, fix every reported error. Do not replace its result with
a reviewer-specific check. If it does not run, do not describe the audit as
structurally validated.

Update the single checklist entry with its current state, next action,
recommended next reviewer, and factual completion condition. A reviewer can be
`completed-with-open-verification` when analysis is complete but proof remains
open.
