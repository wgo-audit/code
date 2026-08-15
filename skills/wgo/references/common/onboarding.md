# Onboarding Workflow

Use for `wgo:onboard`. Onboarding agrees a bounded audit before it writes
anything. Explain that WGO audits the current folder, reads approved sources,
and creates evidence-backed outputs without changing the audited system.

Before doing onboarding work, emit this normal progress message once:
`Starting onboarding. <!-- WGO_PHASE_ONBOARDING_START -->`. The HTML comment is
a persisted cost-attribution marker, not audit evidence.

## Resolve Mode And Audit Root

Parse only these forms:

- no parameters: `improve`;
- `compare [YYYYMMDD]`: targeted comparison with the named completed audit or,
  when omitted, the latest completed audit; or
- `blind-compare [YYYYMMDD]`: blind full audit followed by detailed comparison
  with the named completed audit or latest completed audit.

Reject extra parameters and invalid dates. Resolve roots with `audit-root.md`.
Capture today's auditor-local date once when onboarding starts.

For `improve`, select the newest dated audit root and make it the read-write
active root. If none exists, this is a first audit: plan today's dated root and
run Sequential Intake. If an audit exists, reuse its brief as the configuration
and do not run Sequential Intake.

For `compare`, keep the selected completed baseline read-only and plan today's
dated root. Reuse the baseline configuration, advance the proposed evidence
cutoff to the onboarding start time, and select only reviewers that own
baseline findings or open items requiring reassessment. This run intentionally
does not seek unrelated findings.

For `blind-compare`, keep the selected completed baseline hidden from all audit
reviewers and synthesis until the new audit is complete. Reuse only its
configuration, advance the proposed evidence cutoff to the onboarding start
time, and select the same reviewer set by default. Before evidence discovery,
prepare a system temporary copy of the audited project that excludes every
audit root. Run onboarding, reviewers, and synthesis there. Copy only the
completed new dated audit root back to the original project before the separate
comparison pass reads either audit.

## Reused Configuration Gate

For all three modes when a prior brief supplies configuration, do not repeat
standard onboarding questions. Discover current reviewer packages and validate
their metadata and dependencies. Assemble one complete proposed configuration:
mode, active and baseline roots, baseline access, active audit platform/model,
company/product, audiences, mandate and decision, concerns, harmful failure
mode, detailed scope, cutoff, code repositories and refs,
evidence/documentation sources, selected reviewer IDs and recorded versions,
installed reviewer versions and paths, substitutions, dependency waves,
material auditor answers, known unknowns, and success criteria.
Show the proposed Business Concerns rows with stable IDs; derive them from the
reused mandate, decision, concerns, and harmful failure mode when an older brief
does not contain the table.

For `compare` and `blind-compare`, compare every selected baseline reviewer
version with the currently installed package of the same resolved ID. An
unavailable selected package is a blocker: report it and stop so the auditor
can make the package available. A missing baseline version or different
installed version is a mismatch. List all mismatches together with baseline and
installed values, then ask exactly:

`The selected reviewer versions do not all match the installed packages. Is it
acceptable to continue with the installed versions?`

Wait. If the auditor says no, stop so they can make the intended reviewer
versions available; do not install, select, or retrieve versions for them. If
yes, record the mismatch and acceptance in the new brief and use the installed
versions. Do not ask this version question when all versions match.

After any required version acceptance, show the configuration and ask exactly:

`Does anything in this onboarding configuration need to be updated?`

If no, treat the displayed configuration as approved and proceed with audit
preparation without another start question. If yes, ask only for the named
changes and validate their consequences. If reviewer selection, substitution,
or package availability changed, repeat package validation and the version
gate. Redisplay the complete configuration and ask the same update question
again. Never fall back to the standard intake.

## Sequential Intake

Use this section only for a first audit with no reusable brief. Quietly inspect
the full current project folder, excluding all audit roots, and identify its Git
roots. The audit is always detailed and covers the whole folder plus any
confirmed supporting code repositories. A GitHub URL supplied for code, or a
current repository `origin` that resolves to GitHub, permits read-only use of
its public data and any private data available through the existing GitHub
session. Do not ask for consent to use it. Ask one question at a time and wait
for its answer before asking the next. Do not bundle the mandate, business
decision, concerns, and harmful failure mode.

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
   one path or URL per line (relative to the current project or absolute). Tell the
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
Require unique `id`, `name`, `summary`, `version`, and `codegraph` frontmatter.
Require `depends_on` whenever another reviewer is a prerequisite; allow
external `supersedes`. Treat malformed metadata, unknown dependencies, or a
cycle as unavailable and state why. Present each reviewer's version with the
core reviewers WGO recommends, any it will not run with a reason, and every
external reviewer as an optional addition. Name any proposed core substitution.
External reviewers and substitutions always require auditor approval.

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

For a first audit, summarize the answers and obtain approval for the mandate,
business decision, concerns, harmful failure mode, cutoff, audiences, evidence
and documentation sources, primary/supporting code repositories, selected
reviewer package IDs and versions, substitutions, and success criteria. State
the fixed defaults: detailed full-folder review, available shared collectors,
read-only public and existing-session GitHub access, and coordinator-owned
dependency waves. A reused configuration is approved only through the Reused
Configuration Gate.

Do not create the target dated root before configuration approval unless the
auditor expressly asks for provisional drafts. Mark every provisional
assumption. Never silently include an unrelated repository, reviewer, source,
audit root, or state-changing action.

For `improve`, preserve useful evidence, artifacts, and IDs in the same
read-write root. If Synthesis is completed, record `rerun-all` and mark every
selected reviewer and Synthesis `rerun-pending`; otherwise record
`complete-missing` and retain completed reviewer states. A rerunning reviewer
must challenge prior conclusions against direct evidence, not treat them as
approved facts.

For `compare`, create a fresh root with disposition `fresh`, a Comparison
checklist row, and only the selected targeted reviewers. Copy no baseline
artifact into the new root; link exact read-only baseline items and evidence
from the brief. For `blind-compare`, create a fresh root with disposition
`fresh`, a Comparison row, and the approved full reviewer set in the isolated
project copy. During the blind phase, record the baseline as `hidden` without
its path or content. Add the baseline path only when synthesis is complete and
the comparison phase begins.

## Create The Lean Start

For a new dated root, create only:

```text
audit-brief.md
audit-checklist.md
evidence/evidence-ledger.md
evidence/source-access-register.md
controls/open-items.md
```

Use the selected templates. `audit-brief.md` contains onboarding date, mode,
active root, baseline and access boundary, active audit platform/model, catalog
platform/model, reviewer-version comparison and acceptance, context, mandate,
cutoff, full-folder detailed standard, primary/supporting code repositories,
evidence and documentation sources, automatic GitHub repository sources, each
selected reviewer's ID/version/source/portable package locator, substitutions,
resolved dependency waves, reviewer run disposition, material auditor answers,
and major unknowns. In every created or updated brief, record each approved
question, concern, mandate, decision, and harmful failure mode in the Business
Concerns table with a stable slug ID; preserve the ID when a later audit
reassesses the same concern.
The checklist has one task entry per selected reviewer with state, next action,
recommended next reviewer, and factual closeout condition.
The ledger records reusable evidence; source access records only material access
events. The shared open-items table uses `risk`, `decision-needed`,
`verification`, or `action` as its `Type`.

For each primary or supporting GitHub code repository that is not already a
local current-folder Git root or temporary intake clone, clone the requested
accessible ref into a system temporary workspace such as
`<temp>/wgo-code-repositories/<audit-id>/<repository-name>/`. Record every
repository's stable source ID, URL, ref, resolved commit, portable locator, and
clone failure as a source-access fact. Keep its absolute local root only in
runtime memory. Use the local root or clone as a code root; it is not an audit
artifact. Inspect each accessible GitHub repository's PRs, issues,
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
repository URL/ref/resolved-commit/source-ID mappings plus transient local
roots, converter availability,
catalog output path, audit mandate, selected reviewer IDs, cheap
source-discovery capability signals, active audit platform, and selected
catalog model. Select only from that active platform: Codex/OpenAI uses
`gpt-5.6-terra` at high reasoning, Claude/Anthropic uses Sonnet 5 at high
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
tables, coverage maps, additional manifests, handoffs, or reviewer-owned
folders at onboarding unless a selected output needs one. Synthesis creates the
single report manifest after the audience reports are final.

Shared collectors are internal and available by default. Do not discuss packets
with the auditor; create a packet later when a selected reviewer needs it.

## Closeout

Summarize the boundary, evidence limits, reviewers, dependency waves, and
success criteria. After a reused configuration is approved, the lean start or
same-root update, documentation preparation, and any auditor-approved catalog
additions are complete, proceed directly with `wgo:audit all`. For a first
audit only, ask exactly: `Should I proceed with wgo:audit all?` Do not start
reviewers until the auditor answers yes.
