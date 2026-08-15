# What To Expect During WGO Onboarding

The WGO onboarding command turns a broad concern into an audit boundary that is
useful to the people who will act on its results. Invoke it as `wgo:onboard` in
Codex, `/wgo:onboard` in Claude, or `/wgo-onboard` in OpenCode. Every
independent audit uses `_whats-going-on-YYYYMMDD`, dated when onboarding starts.

WGO audits the complete current folder and any confirmed supporting code
repositories at detailed transition-control depth. It does not change the
project, deploy anything, or ask for credentials.

## Returning To An Audited Project

When a prior audit exists, WGO does not repeat standard onboarding questions.
It displays the complete proposed configuration and asks:

> Does anything in this onboarding configuration need to be updated?

Answering no approves that configuration and starts audit preparation. Answering
yes asks only for the fields that need changing, then displays the configuration
again. The displayed configuration includes the active audit platform/model,
scope, cutoff, sources, selected reviewer versions, dependency waves, material
answers, known unknowns, and success criteria.

Use one of three modes:

| Behavior | Codex | Claude | OpenCode |
|---|---|---|---|
| Improve the newest audit in its existing read-write root. | `wgo:onboard` | `/wgo:onboard` | `/wgo-onboard` |
| Create today's audit root and reassess only findings and open items from the specified completed baseline, or the latest completed audit when the date is omitted. | `wgo:onboard compare [YYYYMMDD]` | `/wgo:onboard compare [YYYYMMDD]` | `/wgo-onboard compare [YYYYMMDD]` |
| Run a full audit without exposing baseline findings, then compare the two completed audits in detail. | `wgo:onboard blind-compare [YYYYMMDD]` | `/wgo:onboard blind-compare [YYYYMMDD]` | `/wgo-onboard blind-compare [YYYYMMDD]` |

For either comparison mode, WGO compares the baseline reviewer versions with
the installed packages. An unavailable selected package blocks the run. WGO
lists missing or different versions together and asks whether using the
installed versions is acceptable. WGO does not install or retrieve a reviewer
version.

## First-Audit Questions

Only a project without a reusable audit configuration receives standard
intake. WGO asks one question at a time. It groups source questions first:
primary code, any additional code repositories, then supporting records.

| Question | Example answer | How WGO uses it |
|---|---|---|
| Company and product context, if unclear | “Acme operates a hosted scheduling service for clinics.” | Gives reports their business context and helps choose relevant reviewers. |
| Primary GitHub code repository — only if the current folder is not a Git repository | “`https://github.com/acme/scheduler`, ref `main`.” | Clones the accessible ref into a temporary local workspace, identifies whether it is a monorepo, and makes it the primary code root. |
| Supporting GitHub code repositories — only when the primary repository is not a monorepo | `https://github.com/acme/mobile-client`, ref `main`<br>`https://github.com/acme/workers`, ref `release` | Clones each accessible ref locally and adds it as a separately identified code root for reviewers and CodeGraph. |
| Evidence and documentation sources | `docs/`<br>`/Users/me/Exports/Notion-2026-07-20/`<br>`https://github.com/acme/operations-docs`, ref `main` | Combines these with documentation already present in audited repositories, creates a searchable catalog, and routes only relevant records to each reviewer. |
| Audit mandate | “Assess whether an incoming maintainer can safely understand, operate, and change the service.” | Defines the audit's central question and what a useful conclusion must address. |
| Decision to support | “Decide whether we can accept the vendor handoff this quarter.” | Distinguishes a fact worth reporting from a fact that changes a decision. |
| Main concerns | “Recovery, credential ownership, and undocumented deployments.” | Focuses reviewer recommendations and evidence collection. |
| Harmful failure to avoid | “Accepting the handoff, then discovering production cannot be recovered.” | Sets the consequence against which risks and priorities are judged. |
| Evidence cutoff | “Use evidence available through 2026-07-24.” | Keeps history, documents, and observations time-bounded and reproducible. |
| Report audiences | “The founder, product lead, and incoming technical lead.” | Shapes the executive summary, product-manager notes, and technical-lead notes. |
| Reviewers | “Add Security and Privacy and Application Security; omit Expense Exposure because billing is out of scope.” | Confirms the perspectives that will run. WGO may present related Security reviewers together, but records each selected reviewer's declared version, names discovered project-local extensions as optional choices, and calculates dependency waves. |
| Success criteria | “Give the incoming maintainer a prioritized, evidence-backed list of blockers and safe next steps.” | Defines what synthesis must demonstrate before the audit is useful. If two valid outcomes would lead to different conclusions, WGO asks one focused distinction. |

For the evidence-and-documentation source list, give one local folder or GitHub
URL per line. In Codex, use Shift+Enter for another line, then send the
complete list. Markdown, text, HTML, CSV, JSON, and YAML provide the most
reliable search. Dated copies of cloud documentation are useful, but the
auditor chooses what to provide; DOCX, XLSX, PPTX, and PDF remain useful when
they are the available record.

If the current folder is not a Git repository, WGO separately asks for the
primary GitHub code repository and clones the requested accessible ref into a
temporary local workspace before it recommends reviewers. If that repository is
not a monorepo, WGO then asks for the other code repositories that support the
product and clones those too. They are code sources, not
documentation-catalog entries.

## Multi-Repository Projects

Use the supporting-code question when one product is delivered by separately
versioned repositories: for example, a web application, API service, background
workers, and infrastructure definitions. WGO treats each supplied repository as
its own code root. It records the URL, ref, resolved commit, and local clone;
uses the repository's accessible GitHub history; and gives CodeGraph the
absolute path for that root. Reviewers reconcile relationships across roots,
but do not treat code in one repository as proof of another repository's live
deployment, ownership, or behavior.

Do not list a repository twice. Put a repository containing project records but
no product code in the evidence-and-documentation source list; put a repository
that implements or delivers the product in the supporting-code list.

## What WGO Decides Internally

Some safeguards are defaults rather than auditor administration:

- the whole current folder is in scope at detailed depth;
- a current GitHub origin or confirmed GitHub code repository enables read-only
  use of accessible history, pull requests, issues, Projects, Actions, and
  releases;
- WGO determines dependency waves and uses shared evidence collection only
  when a reviewer needs it; and
- CodeGraph is used for code topology where the relevant reviewer calls for it,
  never for documentation.

WGO presents reviewers it recommends, reviewers it will not run and why, and
optional additions. External reviewer packages are never selected silently. If
one replaces a core reviewer, WGO names the substitution. If its dependency
validator reports missing tools, WGO pauses and gives you the full path of the
extension's installer to run; WGO does not run it. You can add or reinstate a
reviewer; you do not need to design the execution order.

## Missing Or Unresolved Content

After building the catalog, WGO makes a cheap second pass for two kinds of
signals:

- a material reference that does not resolve to content in the available
  corpus, such as a runbook, dashboard, issue, design, policy, or another
  repository; and
- a likely critical documentation category that is only partially covered or
  not found, based on the mandate and visible project capabilities.

WGO resolves GitHub and HTML links against local clones before flagging them,
and ignores navigation and asset links. These signals mean “not found or not
resolved in the available corpus,” not “does not exist.” They do not become
findings automatically and they do not change document summaries.

When material signals remain, WGO shows a concise list and asks:

> I found potentially material content that is missing from or unresolved in
> the available corpus. Would you like to add any sources before I start the
> audit?

If you answer yes, WGO asks for the paths or GitHub URLs in a separate turn,
adds only those approved sources, and has the same worker and model update the
catalog and resolve the signals again. If you answer no, reviewers receive the
remaining signals as navigation leads or evidence limits, not proof.

## Audit Roots And Comparison

Plain onboarding improves the newest dated root read-write. An incomplete root
keeps completed reviewer states and finishes missing work; a completed root
reruns its selected reviewers and synthesis while preserving stable IDs.

Comparison modes never modify their baseline. A light comparison states that it
did not seek unrelated findings, including in its audience reports. A blind
comparison audits a temporary project copy that excludes every prior audit
root; only after blind synthesis does the comparison step read both audits.
Each comparison records the roots, cutoffs, reviewer versions actually used,
accepted differences, and disposition of prior items. A finding is called
introduced only when dated evidence proves that it arose after the baseline
cutoff.

## Approval And What Happens Next

Before creating a first audit folder, WGO summarizes the mandate, decision,
concerns, failure to avoid, cutoff, audiences, evidence sources, selected
reviewer IDs and versions, primary/supporting code repositories, and success
criteria for approval. After approval it creates only the audit brief,
checklist, evidence ledger, source-access register, and open items. The
onboarding lead delegates
one bounded preparation worker to catalog documentation in audited repositories
and supplied sources. Even an empty documentation corpus can produce a
carefully qualified coverage signal. The worker classifies and converts only
locally available approved content; it does not ask intake questions, set
scope, or select reviewers. The catalog is navigation metadata, not evidence.
It uses the auditor's active platform and existing session only; WGO never
needs another model provider's credentials to prepare the catalog.

For a reused configuration, answering no to the update question proceeds
without a second start question. First-ever onboarding asks permission to run
every selected reviewer. The corresponding commands are `wgo:audit all` in
Codex, `/wgo:audit all` in Claude, and `/wgo-audit all` in OpenCode. Once
reviewers finish, WGO automatically synthesizes the results and asks before
drafting any operator aids.
