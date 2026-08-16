# Report Upload

Use for `wgo:upload [YYYYMMDD]`. This workflow verifies and publishes one
completed audit bundle through a draft pull request. It does not create,
sanitize, or regenerate audit artifacts, and it revises only the narrow
Markdown whitespace defects defined below.

Read `config/upload.yaml`, `references/common/audit-root.md`, and
`references/common/evidence-rules.md`. With a date argument, resolve only that
dated audit root. When the date is omitted, resolve exactly the newest dated
audit root. Do not combine roots.

## Automatic Markdown Whitespace Repair

Before the publication gate, inspect every `.md` file below the selected audit
root and, without asking the auditor, repair only these formatting defects in
the working copy:

- remove trailing ASCII spaces or tabs from each line; and
- remove extra blank lines at end of file so the file ends with exactly one
  newline, preserving its existing newline convention.

Use the agent's native cross-platform text-editing operations, not a generated
cleanup script. Preserve all non-whitespace content and do not modify JSON or
other file types. Report every changed portable relative path and the number of
repaired lines/files. Re-run all publication validation against the repaired
working copy. Any other defect remains a blocking error.

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
   file URLs, relative paths that normalize outside the audit root,
   credentials, agent session identifiers, symlinks, nested `.git`, `__MACOSX`,
   `tmp`, converted-document caches, dependency clones, and build output.
   Report exact offending files; do not rewrite or omit them during upload.
8. Discover every `.DS_Store` file below the audit root. Treat it as packaging
   metadata, not as an audit artifact: report its portable relative locator and
   exclude it from the published package without modifying the source audit.

Reports are immutable. Query the configured repository and refuse an existing
destination even when its contents differ. Do not offer an overwrite.

The report repository must treat generated catalog/index files as its own
post-merge responsibility. A WGO upload PR is destination-only: it must not
include `README.md`, per-subject README files, `audits/index.json`, or any
other repository-level generated index. If the report repository's pull-request
checks require generated indexes to be committed in the same PR, stop and
report that the repository contract is incompatible with pull-less upload.

## GitHub Preflight And Approval

Require `git` and `gh`, an authenticated `gh` session, and push permission to
the configured report repository. Do not request credentials, install tools,
or create a fork when permission is absent. Resolve the repository's default
branch from GitHub rather than assuming a branch name.

Create a fresh shallow, blobless, no-checkout clone in a system temporary
directory. Clone only the resolved default branch with `--depth 1`,
`--filter=blob:none`, `--no-checkout`, `--single-branch`, and `--branch
<resolved-default-branch>`. Verify the clone records its origin as a promisor
remote with the `blob:none` partial-clone filter. If Git or the server does not
support that mode, stop instead of falling back to a full clone.

Configure sparse checkout for only the exact new destination, then run a
sparse-aware checkout of the fetched default-branch tip to initialize the index.
Use bounded index and worktree diff checks to prove there are no staged or
unstaged changes before creating the upload branch; do not scan repository-wide
untracked or ignored files. Do not run `git pull`, fetch additional history,
materialize existing report contents, or reuse a report checkout found in the
audited project. Do not call or recreate a report-repo importer, index builder,
publishing script, or platform-specific copy script.

Before any commit or push, show the auditor:

- configured public repository and resolved base branch;
- audit root, report ID, subject ID, evidence cutoff, and access boundary;
- Markdown whitespace repair count and changed portable relative paths;
- exact destination, source file count, `.DS_Store` exclusion count, published
  file count, and audit-only or operationalized coverage;
- validation results and any checks that could not run;
- proposed branch `agent/add-<subject.id>-<evidence.cutoff>-audit`;
- proposed commit and draft-PR title
  `Add <subject.name> <evidence.cutoff> audit`.

Ask for explicit approval of that public destination, commit label, and draft
PR. A no or ambiguous answer ends the workflow without external writes.

## Package And Publish

After approval, use the agent's native cross-platform filesystem operations to
copy the complete audit root to the new destination, preserving every relative
path and byte except files named exactly `.DS_Store`. That filename is the sole
packaging exclusion; do not introduce or maintain any other exclusion list and
do not silently drop files. Do not modify the source audit root beyond the
completed Markdown whitespace repair, and never modify its manifest.

After copying, verify that no `.DS_Store` exists in the destination, every other
source file exists at the same relative path, and its bytes are unchanged. The
published file count must equal the source file count minus the disclosed
`.DS_Store` count.

Review the complete diff. Require every changed path to be under the new
destination; repository-level discovery files are out of scope unless a later
report-repository contract explicitly requires them. Re-run the publication
gate against the copied destination, run `git diff --check`, and stage only the
verified destination. Force-add that exact destination so Git does not fetch
the repository's existing ignore-file blobs; never force-add a broader path.

Create the approved branch and commit, push it with upstream tracking, and use
`gh` to open a draft pull request against the resolved default branch. The PR
body states:

- what report was added and why;
- report ID, subject, evidence cutoff, and destination;
- public evidence boundary and important limitations;
- exact validation command and result, or the explicit checks used when the
  optional validator could not run; and
- confirmation that the manifest was verified unchanged, which Markdown files
  received automatic whitespace repair, that the disclosed `.DS_Store` files
  were the only exclusions, and that no report-repo generation script was used.

Return the repaired Markdown paths, branch, commit, PR URL, target branch,
validation result, and any remaining limitation. Do not mark upload complete
unless the draft PR exists.
