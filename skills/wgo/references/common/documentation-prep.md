# Documentation-Preparation Worker

The onboarding lead delegates this worker once after approval. It receives the
documentation-bearing paths discovered in every audited code root plus any
approved local evidence/documentation folders or prepared GitHub
supporting-record clones. It makes those records discoverable and identifies
potentially material content gaps; it does not audit the documents, judge their
accuracy, create findings, ask the auditor questions, clone repositories, set
scope, or select reviewers.

## Active Platform And Model

Use only the active audit platform and its existing session or credentials. Do
not request, configure, or call another provider. The onboarding lead supplies
one catalog model: Codex/OpenAI uses `gpt-5.6-terra` at high reasoning,
Claude/Anthropic uses Sonnet 5 at high reasoning, Antigravity/Gemini uses
`gemini-3.5-flash-lite`, and another platform uses its active audit model. If a
preferred same-platform model is unavailable, use that active audit model.

Use the supplied model consistently for the full catalog run, including every
batch and summary. Do not mix models or providers. This model classifies and
summarizes navigation metadata; it does not make audit conclusions.

## Boundaries

Read only the supplied documentation-bearing paths in audited code roots,
approved folders, and prepared GitHub source clones. Record inaccessible
content as a limit. Do not follow a reference outside those sources, install
tools, alter source documents, copy secrets or unnecessary PII into audit
artifacts, or browse cloud services. Use an approved local converter when
available; otherwise use the agent's built-in reader. If neither can read a
document, record the limit and continue.

Write one durable navigation artifact:

```text
<audit-root>/documentation/catalog.md
```

Use a system temporary cache such as `<temp>/wgo-document-cache/<audit-id>/` for
converted text. Never put converted document bodies under an audit root.
The cache may be recreated from the approved source when an audit resumes.

## Two Passes, One Worker

Use the supplied model and this worker for both passes. Do not delegate further
workers or write intermediate audit artifacts.

First inventory the supplied paths, exclude duplicate paths, convert and
classify documents in bounded batches, then remove duplicate paths, assign
stable `DOC-NNN` IDs, and finish every catalog row. Freeze the factual
classification, reviewer routing, summary, and limits before the second pass.

For a source that is already searchable text, use its qualified portable
locator as the cached-text locator; do not create a duplicate. For PDF, DOCX,
XLSX, and PPTX,
cache converted text only when a reader or approved converter makes it useful.
Record `not-created` and a concise limitation when conversion is unavailable or
unreliable.

Second, use the completed catalog, the supplied repository clone mappings,
audit mandate, selected reviewer IDs, and cheap repository capability signals
to identify only material documentation-coverage gaps and material references
to content that is not resolved in the corpus. This pass may add the two signal
sections below, but it must not rewrite or bias the first-pass catalog rows.

## Catalog Contract

Start `catalog.md` with `# Documentation Catalog`, then this statement: “This
catalog is navigation metadata, not audit evidence. Cite the original document
and section for every finding.” Then create one row per document:

```markdown
| ID | Original locator | Cached text locator | Format | Type and topics | Relevant reviewers | Summary (target 75–100 words; max 120) | Limits |
|---|---|---|---|---|---|---|---|
```

Both locator columns follow the portable artifact-path rule: use the stable
source ID plus a path relative to that source root. Runtime clone, attachment,
conversion-cache, and home-directory paths are never written to the catalog.

Use only factual, source-visible metadata. `Type and topics` is a short routing
label such as product, technical, operational, security, commercial, delivery,
or customer. `Relevant reviewers` uses WGO reviewer IDs. The summary targets
75–100 words and must not exceed 120; it states purpose, audience, scope/time,
major topics, and important exclusions. It contains no assessment,
recommendation, or assertion of truth. `Limits` records stale/unknown date,
failed conversion, inaccessible child file, or similar material constraint.

After all document rows, add these two sections. They remain navigation
metadata, not evidence or findings.

### Referenced Content Outside The Corpus

Inspect source-visible references to content broadly: documents, repositories,
issues, pull requests, releases, Actions runs, Projects, tickets, dashboards,
designs, incidents, chat records, APIs/specifications, policies, contracts, and
other records. Keep only a reference that could materially affect an audit
decision, control, ownership claim, operational procedure, product promise, or
reviewer conclusion.

Resolve each candidate against the complete corpus identity index before
reporting it. The index includes original and cached portable locators,
repository URL/ref/resolved commit/source-ID mappings, repository-relative paths, normalized
GitHub blob/tree/raw URL forms, document IDs, titles, and distinctive headings.
Resolve relative links from the referring file. Strip harmless URL fragments
and query parameters when matching. For GitHub URLs, map the repository and
path to its prepared local clone before deciding that content is external.

HTML requires special care: ignore page navigation, same-page anchors, assets,
scripts, styles, fonts, `mailto:`, and `tel:` links. Do not report an ordinary
HTML hyperlink merely because it is external. Report it only when its context
shows that the target is material audit content and it cannot be resolved to an
available local copy.

Track candidates with one of these statuses:

- `resolved-in-corpus`
- `available-approved-source`
- `referenced-outside-corpus`
- `broken-local-reference`
- `ambiguous-reference`

Omit `resolved-in-corpus` rows. Write the remaining material rows as:

```markdown
## Referenced Content Outside The Corpus

| Referrer and location | Referenced content | Status | Relevant reviewers | Why it may matter |
|---|---|---|---|---|
```

Use `available-approved-source` only when the content is inside a supplied
source but was inaccessible, unreadable, or missed by the first-pass inventory.
Never infer that referenced content exists, is current, or supports the
referrer's claim.

### Documentation Coverage Signals

Use the mandate, selected reviewers, catalog topics, and supplied cheap
repository capability signals to test for likely critical documentation
categories. Examples include deployment/release, recovery/restore, runtime
operations, observability/alert response, access/credential ownership, data
stores and migration, background jobs, public API/integration contracts,
architecture boundaries, product commitments, ownership/continuity, and
contributor setup. Evaluate a category only when the mandate or a visible
capability makes it relevant.

Use `covered`, `partial`, `not-found-in-corpus`, or `not-triggered`. Omit
`covered` and `not-triggered` rows. `Partial` and `not-found-in-corpus` describe
the available corpus, not the real world; they do not prove that content does
not exist.

```markdown
## Documentation Coverage Signals

| Category | Trigger | Status | Available content | Relevant reviewers | Why it may matter |
|---|---|---|---|---|---|
```

Keep this pass cheap. Do not score completeness, require a universal document
set, turn every code capability into a gap, or create findings.

## Adding Sources

If the auditor adds sources after seeing the signals, the onboarding lead gives
the same worker and model the new prepared paths. Catalog only new or changed
documents, preserve unchanged IDs and first-pass rows, rebuild the complete
corpus identity index, and rerun both signal sections against the full corpus.
Do not append stale unresolved references from the earlier pass.

## Reviewer Use

Reviewers search the catalog by their reviewer ID and topic; they do not load it
in full. They also search the two signal sections for their reviewer ID. They
assign each worker only the matching rows and paths for its scoped question.
Workers use the catalog as navigation, read available original or cached text
directly, and cite the original document and section. A missing-content signal
is a search lead or evidence limit, never proof or an automatic finding. A
reviewer may expand the slice when a document is materially cross-cutting.
CodeGraph is never used for documents.
