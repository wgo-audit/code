# Onboarding Workflow

Use for `wgo:onboard`. Onboarding agrees a bounded audit before it writes
anything. Explain that WGO audits the current folder, reads approved sources,
and creates evidence-backed outputs without changing the audited system.

## Sequential Intake

Quietly inspect the full current project folder first and identify its Git
roots. The audit is always detailed and covers the whole folder plus any
confirmed supporting code repositories. A GitHub URL supplied for code, or a
current repository `origin` that resolves to GitHub, permits read-only use of
its public data and any private data available through the existing GitHub
session. Do not ask for consent to use it. Ask one question at a time and wait
for its answer before asking the next. Do not bundle the mandate, business
decision, concerns, and harmful failure mode.

When `_whats-going-on/audit-checklist.md` exists, read it and the audit brief
before intake and reuse confirmed answers that have not changed. If one or more
reviewer rows have state `completed` or beginning with `completed-`, ask exactly
one question and wait:

`I found completed reviewer work. Should I complete only missing work
(idempotent), or rerun all selected reviewers using the prior findings as a
launchpad?`

Retain the answer and, after approval, record `complete-missing` or `rerun-all`
as the reviewer run disposition in the brief. Do not ask this question when no
reviewer is marked complete; record `fresh` after approval. Do not infer a
choice from the active model or platform.

Ask in this order:

1. Confirm company and product context when it is not clear from the approved
   material.
2. If the current folder has no Git root, ask for the primary GitHub code
   repository URL and requested ref. Clone the accessible ref immediately into
   a system temporary workspace, inspect whether it is a monorepo, and retain
   it as the planned local code root. Do not create audit artifacts yet.
3. When the primary current-folder or temporary-clone repository is not a
   monorepo, ask whether other code repositories support the product. Ask for
   one GitHub URL and requested ref per line; retain each as a planned local
   clone. Do not ask this question for a confirmed monorepo.
4. Ask for every additional evidence or documentation source in one answer:
   local folders and GitHub repositories containing supporting records. Ask for
   one path or URL per line (relative to the audit folder or absolute). Tell the
   auditor: local copies enable fast, repeatable cross-document search and exact
   evidence citations while keeping content inside the agreed audit boundary.
   A dated cloud export is useful, but the auditor chooses what to provide.
   Prefer Markdown, plain text, HTML, CSV, JSON, or YAML. DOCX, XLSX, PPTX,
   and PDF are also useful exports, but their layout or tables can be less
   reliable after conversion. Say: “Use Shift+Enter to add another source; send
   when the list is complete.” Record a supplied GitHub URL and requested ref
   as a planned local clone.
5. Ask for the audit mandate.
6. Ask which business or project decision the audit must support.
7. Ask for the auditor's main concerns.
8. Ask which harmful failure mode the audit must avoid.
9. Ask for the evidence cutoff.
10. Ask for report audiences.

Then discover core packages under this skill at
`references/reviewers/*/reviewer.md` and external packages relative to the
audited project at `plugins/wgo-reviewers/*/reviewer.md`; do not use a separate
reviewer registry.
Require unique `id`, `name`, `summary`, and `codegraph` frontmatter. Require
`depends_on` whenever another reviewer is a prerequisite; allow external
`supersedes`. Treat malformed metadata, unknown dependencies, or a cycle as
unavailable and state why. Present the core reviewers WGO recommends, any it
will not run with a reason, and every external reviewer as an optional
addition. Name any proposed core substitution. External reviewers and
substitutions always require auditor approval.

For an approved external reviewer, run its platform `validate_install` by
absolute path when present. No validator means no installation is needed. A
zero exit means ready. On any other exit, pause and tell the auditor to run the
matching `install` script, showing its full absolute path; never run it for
them. Rerun validation after they report completion.

Resolve substitutions, then calculate reviewer dependencies and waves from the
resolved graph. Present any missing required dependency with its reviewer; do
not add it silently. Do not ask for or offer a reviewer order. Ask only whether
the auditor wants to add an optional reviewer, approve a substitution, or
reinstate an omitted one. Ask for success criteria. If the mandate still admits
materially different acceptable outcomes that would change the scope,
acceptance criteria, or headline conclusion, ask one focused disambiguation
question before approval. For example, distinguish preserving an existing
identity from operating an independent equivalent. Do not add routine
clarification questions.

## Approval Gate

Summarize the answers and obtain approval for the mandate, business decision,
concerns, harmful failure mode, cutoff, audiences, evidence and documentation
sources, primary/supporting code repositories, selected reviewer packages and
substitutions, and success criteria. State the fixed defaults: detailed
full-folder review, available shared collectors, read-only public and
existing-session GitHub access, and coordinator-owned dependency waves.

Do not create `_whats-going-on/` before approval unless the auditor expressly
asks for provisional drafts. Mark every provisional assumption. Never silently
include an unrelated repository, reviewer, source, or state-changing action.

If `_whats-going-on/` exists, read it first. Preserve useful evidence and
artifacts. On a resume in the same audit root, treat its open-items table and
decision inventories/registers as the canonical re-run baseline. Do not reuse
their IDs for a different item or decision, and do not automatically compare a
deleted, moved, or separately archived audit; the auditor may explicitly supply
one as evidence. Write the lean layout only when the auditor explicitly chooses
to resume under this workflow; do not build a migration engine.

For `complete-missing`, retain completed reviewer states and run only missing
work. For `rerun-all`, retain prior reports, handoffs, evidence, controls, and
IDs as the launchpad; after approval mark every selected reviewer and Synthesis
`rerun-pending`. A rerunning reviewer must challenge prior conclusions against
direct evidence, not treat them as approved facts.

## Create The Lean Start

After approval, create only:

```text
audit-brief.md
audit-checklist.md
evidence/evidence-ledger.md
evidence/source-access-register.md
controls/open-items.md
```

Use the selected templates. `audit-brief.md` contains context, mandate, cutoff,
full-folder detailed standard, primary/supporting code repositories, evidence
and documentation sources, automatic GitHub repository sources, each selected
reviewer's ID/source/absolute package path, substitutions, resolved dependency
waves, reviewer run disposition, material auditor answers, and major unknowns.
The checklist has one task entry per selected reviewer with state, next action,
recommended next reviewer, and factual closeout condition.
The ledger records reusable evidence; source access records only material access
events. The shared open-items table uses `risk`, `decision-needed`,
`verification`, or `action` as its `Type`.

For each primary or supporting GitHub code repository that is not already a
local current-folder Git root or temporary intake clone, clone the requested
accessible ref into a system temporary workspace such as
`<temp>/wgo-code-repositories/<audit-id>/<repository-name>/`. Record every
repository's URL, ref, resolved commit, local path, and clone failure as a
source-access fact. Use the local root or clone as a code root; it is not an
audit artifact. Inspect each accessible GitHub repository's PRs, issues,
Projects, Actions, releases, and history as a read-only source. Use public data
and private data available through the existing GitHub session; record material
access results or limits without asking for a second approval.

First clone each supplied GitHub evidence/documentation repository's requested
accessible ref into `documentation/tmp/<repository-name>/` and record its URL,
ref, resolved commit, and any inaccessible repository as a source-access fact.
Identify documentation-bearing paths in every audited code root, including
README files and evident documentation, runbook, contributor, and GitHub
project-record folders; do not send source-code trees to the documentation
worker.

Then delegate exactly one documentation-preparation worker before asking to
start the audit. Give it `documentation-prep.md`, the discovered
documentation-bearing paths, approved local source paths and prepared clones,
repository URL/ref/resolved-commit/local-root mappings, converter availability,
catalog output path, audit mandate, selected reviewer IDs, cheap
source-discovery capability signals, active audit platform, and selected
catalog model. Select only from that active platform: Codex/OpenAI uses
`gpt-5.6-luna` at high reasoning, Claude/Anthropic uses Sonnet 5 at high
reasoning, and Antigravity/Gemini uses `gemini-3.5-flash-lite`; another platform
uses its active audit model. If the preferred same-platform model is not
selectable, use the active audit model. Do not request, configure, or use another provider's credentials or API.
It does not ask the auditor questions, clone repositories, set scope, or choose
reviewers. It creates only
`documentation/catalog.md`; the catalog and its missing-content signals are
navigation metadata, not evidence or reviewer outputs.

After the worker finishes, read only the material rows under `Referenced
Content Outside The Corpus` and `Documentation Coverage Signals`. If there are
any, present a concise deduplicated list, clearly described as potentially
missing or unresolved in the available corpus rather than absent in reality.
Then ask exactly one question and wait:

`I found potentially material content that is missing from or unresolved in
the available corpus. Would you like to add any sources before I start the
audit?`

If the auditor answers yes, ask in the next turn for one local path or GitHub
URL/ref per line and remind them to use Shift+Enter for a newline. Treat that
answer as approval for those added sources, prepare them using the same rules,
record them in the brief and source-access register, and continue the same
documentation worker with the same model. It catalogs only new or changed
documents, preserves unchanged entries, then reruns reference resolution and
coverage signals against the full corpus. Present any remaining material
signals without turning them into findings. If the auditor declines, retain
them as evidence limits. Do not follow or import an unapproved reference.

When a selected reviewer benefits from CodeGraph and `codegraph` is available,
discover the distinct Git roots in the audit folder and each approved code
clone. If all audited code belongs to one root, including a monorepo, initialize
or sync that root once. Otherwise initialize or sync every distinct root.
Always pass the absolute root: `codegraph init <absolute-root>` or `codegraph
sync <absolute-root>`. If CodeGraph is unavailable, use direct code navigation
and state the limit only if material.

Do not create claims, collection logs, per-type control registers, status
tables, coverage maps, manifests, handoffs, or reviewer-owned folders at
onboarding unless a selected output needs one.

Shared collectors are internal and available by default. Do not discuss packets
with the auditor; create a packet later when a selected reviewer needs it.

## Closeout

Summarize the boundary, evidence limits, reviewers, dependency waves, and
success criteria. After the lean start, documentation preparation, and any
auditor-approved catalog additions are complete, ask exactly:
`Should I proceed with wgo:audit all?` Do not start reviewers until the auditor
answers yes.
