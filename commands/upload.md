---
name: upload
description: Verify a completed public WGO audit and open a draft PR in the configured report repository.
args: "[YYYYMMDD]"
skills: wgo
argument-hint: "[YYYYMMDD]"
disable-model-invocation: true
---

# /upload

Invoke this as `wgo:upload [YYYYMMDD]` in Codex,
`/wgo:upload [YYYYMMDD]` in Claude, or `/wgo-upload [YYYYMMDD]` in OpenCode.
The date is optional; when omitted, use the newest dated audit root.

Load and use the WGO skill, then run its complete
`references/common/upload.md` workflow. Upload is an explicit public
publication request, but the workflow still previews and confirms the exact
repository, destination, commit label, and draft PR before external writes.

Automatically repair only the Markdown trailing-whitespace and end-of-file
blank-line defects defined by the workflow. Never otherwise modify the audit to
make it publishable, create or revise its manifest, call a report-repository
generation script, publish a broader-than-`public-only` evidence boundary
without the auditor's explicit acknowledgement, or overwrite an existing
report. Exclude only disclosed `.DS_Store` packaging metadata and reject
provider session identifiers anywhere in the public package.
