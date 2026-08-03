---
name: audit
description: Run one selected Whats.Going.On. reviewer, or all selected reviewers in dependency waves.
args: "[reviewer-id|all]"
skills: wgo
---

# /audit

Codex users may invoke this as `wgo:audit <reviewer-id>`, `wgo:audit all`, or
`wgo:audit`.

Resolve the newest dated audit root with
`skills/wgo/references/common/audit-root.md`. Read and write only that root.

## One Reviewer

With `<reviewer-id>`, confirm that reviewer is selected in `audit-brief.md`,
then:

1. Read the brief, the reviewer card, its relevant predecessor handoffs, and
   only named shared evidence packets and linked artifacts relevant to its question.
   Use the approved absolute reviewer-package path recorded in the brief.
   On a same-root resume, also read its prior open items and decision
   inventory/register before assigning an OI, ADR, or PDR ID.
2. When the brief names automatic GitHub code repository sources, create or refresh
   `github-history-and-hosted-ci.md` before reviewing. It inspects the named
   repositories' accessible PRs, issues, Projects, Actions, releases, and
   history without another approval, and writes only an evidence packet.
3. Inspect available evidence before selecting outputs; register reusable
   evidence and material access events. Run any other card-listed shared
   collector when it supports the question and its packet is absent or stale.
4. Select the reviewer card's required outputs and any conditional output whose
   plain-language trigger is met. Do not create routine not-applicable rows.
5. If the reviewer returns a qualifying mandate, acceptable-outcome, priority,
   or authority question, the coordinator asks it and records the answer before
   dependent work. The reviewer never contacts the auditor. Use a verification
   when proof of fact, access, or live state is required.
6. Create selected artifacts from their templates, labelling uncertainty in the
   artifact. Record a concise omission and closure route only when a required or
   triggered output cannot responsibly be created.
7. Run the one ephemeral artifact-quality review. Revise the selected outputs
   once; it never creates an audit artifact or a second approval step.
8. Write the reviewer report, including zero or more evidence-linked decision
   insights when they meet the shared standard, and compact handoff; then update
   the checklist and material shared open items.

If this completes the last selected reviewer, automatically run `wgo:summarize`.

## All Selected Reviewers

With `all` or no parameter, read the selected reviewer list in `audit-brief.md`
and the checklist. On a same-root resume, preserve prior open items and decision
inventories/registers as the canonical ID baseline. Read the reviewer run
disposition:

- `fresh`: run every selected reviewer not already completed during this run;
- `complete-missing`: skip reviewer states `completed` and `completed-*`; or
- `rerun-all`: run every selected reviewer, including previously completed
  reviewers.

For `rerun-all`, give each reviewer its prior report, handoff, linked evidence,
controls, open items, and decisions as a launchpad. It must verify direct
evidence, challenge prior findings, and explicitly retain, revise, supersede,
or close them; prior prose is not proof. Do not allocate a new ID merely
because a different model or platform performs the rerun.

When the brief names automatic
GitHub code repository sources and its packet is absent or stale, create or refresh
`github-history-and-hosted-ci.md` once before the first wave. Use the selected
reviewer package paths and resolved dependency graph recorded in the brief.
Recheck that no selected IDs conflict and the graph is acyclic. Start every
currently unblocked reviewer in parallel; after its wave is reconciled, release
the next unblocked set. A dependency on a superseded core ID resolves to its
approved replacement. Do not discover or select a new extension during audit.

Before a wave, pass each reviewer only completed predecessor handoffs. A
selected dependency that did not complete is a stated limitation and blocks its
dependents; do not run them as if the prerequisite existed. The reviewer owns
its report, handoff, and selected controls; after parallel work returns, the
coordinator serializes updates to the shared evidence ledger, open items, and
checklist. At the end of the wave, surface a qualifying auditor question before
starting dependent work: ask one exact question, wait for its answer, record it
in the brief and its existing `decision-needed` item, then ask another only if
it remains material. Do not let `wgo:audit all` defer such a question merely to
keep the run uninterrupted. Then validate the audit root and start the next
wave. Once all selected reviewers are complete, automatically run
`wgo:summarize`. Under `complete-missing`, if no reviewer work was missing and
the existing synthesis already covers the unchanged selected reviewer set, do
not rewrite it; report that nothing was missing. Under `rerun-all`, always rerun
synthesis after the reviewer waves.

For onboarding mode `compare`, give reviewers only the selected read-only
baseline items, their exact prior evidence links, and current evidence needed
to reassess them. They do not search for unrelated new findings. For
`blind-compare`, do not give reviewers any baseline content or prior
identifiers.

Do not mark work complete merely because a report exists. A bounded,
completed-with-open-verification conclusion is valid when its limits are clear.
