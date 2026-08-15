# Lean Administrative Templates

Replace placeholders in completed files. Keep templates in English; translate
generated reports at synthesis when requested.

## Audit Brief

```markdown
# Audit Brief

| Field | Confirmed value |
|---|---|
| Onboarding start date, mode, and audit root | |
| Baseline audit root and access (`none`, `read-only`, or `hidden`) | |
| Audit platform/model and catalog platform/model | |
| Reviewer-version comparison and auditor acceptance | |
| Company and product | |
| Audience and business context | |
| Mandate and decision enabled | |
| Detailed standard and cutoff | Detailed; |
| Current-folder repository scope | Entire current project folder |
| Primary code repository (source ID, URL/origin, ref, portable locator) | |
| Supporting code repositories (source ID, URL, ref, portable locator) | |
| Automatic GitHub code repository sources | |
| Evidence and documentation sources (source ID, portable locator or GitHub URL/ref) | |
| Source limits | |
| Selected reviewer packages (ID, version, core/external, portable package locator) | |
| Approved substitutions and resolved dependency waves | |
| Reviewer run disposition (`fresh`, `complete-missing`, or `rerun-all`) | |
| Material auditor answers and success boundaries | |
| Major known unknowns | |
| Success criteria | |
```

## Business Concerns

```markdown
| ID | Type | Approved statement |
|---|---|---|
| <stable-slug> | <question, concern, mandate, decision, or failure-mode> | <approved wording> |
```

Preserve an existing ID when a later audit reassesses the same concern.

## Audit Checklist

```markdown
# Audit Checklist

| Work item | State | Next action | Recommended next reviewer | Factual completion condition |
|---|---|---|---|---|
| Onboarding | confirmed | | wgo:audit all | Brief and selected reviewers confirmed |
| <reviewer-id> | not-started | | | Report, handoff, selected outputs, material omissions, and reconciliation complete |
| Synthesis | not-started | | | Final reports reconcile completed reviewer work |
```

On a `rerun-all`, use `rerun-pending` for every selected reviewer and
Synthesis. Do not delete their prior artifacts.
For `compare` and `blind-compare`, add a `Comparison` row. It completes only
after `comparison.md` identifies both audit roots, their cutoffs, reviewer
versions actually used, and the mode-appropriate dispositions.
`State` is exactly `confirmed`, `not-started`, `in-progress`, `rerun-pending`,
`completed`, `completed-with-open-verification`, or `blocked`.

## Reviewer Handoff

```markdown
# <Reviewer Name> Handoff

## Confirmed Navigation
## Constraints And Conflicts
## Material Unknowns
## Downstream Use

Keep this under 150 words. Link exact evidence/artifacts and state what
downstream reviewers may use and must not assume.
```

## Evidence Ledger

```markdown
# Evidence Ledger

| Evidence ID | Source type | Exact locator | Observed/effective time | Cutoff eligibility | Factual summary | Limitation | Sensitivity |
|---|---|---|---|---|---|---|---|
```

Use exactly one listed cutoff label in every evidence row; a contextual
qualification may follow it. The definitions and post-cutoff boundary are in
`../common/evidence-rules.md`.

## Source Access Register

```markdown
# Source Access Register

| Source | Attempt/time | Result or limitation | Question affected | Material impact | Approved fallback/exclusion | Owner and next step |
|---|---|---|---|---|---|---|
```

## Open Items

```markdown
# Open Items

| ID | Type | Priority | Item and consequence | Evidence/artifact links | Owner | Closure route | Status |
|---|---|---|---|---|---|---|---|
```

`Type` is exactly `risk`, `decision-needed`, `verification`, or `action`.
Use `decision-needed` for a decision now, `verification` for evidence needed,
and `action` for an implementation correction. Use `risk` only when no
responsible next move can yet be stated; do not duplicate a risk and its route.
Priority orders items within their type, not as one global queue. Use P1 only
when delay blocks safe operation, release, or transfer; P2 for material planned
work; P3 for material but non-blocking work.
For every `OI-###`, `Status` is exactly `open`, `verified-fixed`, `superseded`,
or `out-of-current-scope`. Preserve the ID on a re-run; a materially changed
item gets a new ID and links to the superseded item. New IDs continue after the
highest prior ID in this audit root.
An observed ADR/PDR must not be represented as an open item.

## Audit Comparison

```markdown
# Audit Comparison

| Field | Value |
|---|---|
| Mode | compare or blind-compare |
| Baseline audit root and cutoff | |
| Current audit root and cutoff | |
| Baseline reviewer versions | |
| Current reviewer versions | |
| Accepted version differences | |
| Comparison boundary | |

| Prior item or finding | Current evidence | Disposition | Explanation and limits |
|---|---|---|---|
```

For `compare`, disposition is exactly `fixed`, `improved`, `unchanged`,
`regressed`, or `unverifiable`; assess only baseline items and state that the
run did not seek unrelated findings. For `blind-compare`, reconcile both
completed audits after blind synthesis and may additionally use `newly-found`
or `no-longer-evaluated`. Use `introduced` only when dated evidence proves the
issue arose after the baseline cutoff.
