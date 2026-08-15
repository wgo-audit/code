# Report Upload

Use for `wgo:upload [YYYYMMDD]`. This workflow verifies and publishes one
completed audit bundle through a draft pull request. It does not create,
revise, sanitize, or regenerate audit artifacts.

Read `config/upload.yaml`, `references/common/audit-root.md`, and
`references/common/evidence-rules.md`. With a date argument, resolve only that
dated audit root; otherwise resolve the newest root. Do not combine roots.

## Publication Gate

Before creating Git state, require all of the following:

1. The checklist marks Synthesis `completed` or
   `completed-with-open-verification`, and the final audience reports exist.
2. `manifest.json` is the final WGO schema, contains no legacy flat manifest
   fields or unresolved placeholders, and its entrypoint exists.
3. `evidence.accessBoundary.level` is `public-only`. A private, mixed, or
   unknown boundary is not publishable through this command.
4. `subject.id` matches `[a-z0-9][a-z0-9._-]*` and `evidence.cutoff` is an ISO
   date. The destination is exactly
   `audits/<subject.id>/<evidence.cutoff>/`.
5. Every Git source uses its full resolved commit when known, and every
   selected reviewer records its ID, version, and status.
6. The complete audit root passes the bundled structural validator with
   `--require-final` when Python is available. If it is unavailable, inspect
   the same required files, headings, tables, manifest contract, stable IDs,
   and credential patterns directly; never describe an unrun validator as
   passed.
7. Every filesystem path in every artifact follows the portable artifact-path
   rule. Reject absolute local paths, drive or UNC paths, home-relative paths,
   file URLs, traversal segments, credentials, agent session identifiers,
   symlinks, `.DS_Store`, nested `.git`, `__MACOSX`, `tmp`, converted-document
   caches, dependency clones, and build output. Report exact offending files;
   do not rewrite or omit them during upload.

Reports are immutable. Query the configured repository and refuse an existing
destination even when its contents differ. Do not offer an overwrite.

## GitHub Preflight And Approval

Require `git` and `gh`, an authenticated `gh` session, and push permission to
the configured report repository. Do not request credentials, install tools,
or create a fork when permission is absent. Resolve the repository's default
branch from GitHub rather than assuming a branch name.

Create a fresh checkout in a system temporary directory. Never reuse a report
checkout found in the audited project. Do not call or recreate a report-repo
importer, index builder, publishing script, or platform-specific copy script.

Before any commit or push, show the auditor:

- configured public repository and resolved base branch;
- audit root, report ID, subject ID, evidence cutoff, and access boundary;
- exact destination, file count, and audit-only or operationalized coverage;
- validation results and any checks that could not run;
- proposed branch `agent/add-<subject.id>-<evidence.cutoff>-audit`;
- proposed commit and draft-PR title
  `Add <subject.name> <evidence.cutoff> audit`.

Ask for explicit approval of that public destination, commit label, and draft
PR. A no or ambiguous answer ends the workflow without external writes.

## Package And Publish

After approval, use the agent's native cross-platform filesystem operations to
copy the complete audit root verbatim to the new destination. Because the gate
rejects non-report material, do not maintain an exclusion list and do not
silently drop files. Do not modify the source audit root or its manifest.

Review the complete diff. Require every changed path to be under the new
destination; repository-level discovery files are out of scope unless a later
report-repository contract explicitly requires them. Re-run the publication
gate against the copied destination, run `git diff --check`, and stage only the
verified destination.

Create the approved branch and commit, push it with upstream tracking, and use
`gh` to open a draft pull request against the resolved default branch. The PR
body states:

- what report was added and why;
- report ID, subject, evidence cutoff, and destination;
- public evidence boundary and important limitations;
- exact validation command and result, or the explicit checks used when the
  optional validator could not run; and
- confirmation that the manifest was verified unchanged and no report-repo
  generation script was used.

Return the branch, commit, PR URL, target branch, validation result, and any
remaining limitation. Do not mark upload complete unless the draft PR exists.
