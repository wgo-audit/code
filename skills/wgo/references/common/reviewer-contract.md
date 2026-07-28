# Reviewer Extension Contract

This is the canonical interface between a reviewer package and the WGO
coordinator. It is for reviewer authors; audit reviewers do not load it.

## Package Layout

One folder is one self-contained reviewer:

```text
<reviewer-id>/
  reviewer.md
  workers/                    # optional
    <bounded-evidence-slice>.md
  validate_install.sh         # optional, macOS/Linux
  install.sh                  # required when the shell validator exists
  validate_install.bat        # optional, Windows
  install.bat                 # required when the Windows validator exists
```

Core packages live under the WGO skill at
`references/reviewers/<reviewer-id>/`
(`skills/wgo/references/reviewers/<reviewer-id>/` in this source repository).
External packages live at
`plugins/wgo-reviewers/<reviewer-id>/` in the audited project. The WGO
installer never replaces that external root.

## Reviewer Metadata

`reviewer.md` starts with YAML frontmatter:

```yaml
---
id: stable-kebab-id
name: Reader-facing name
summary: One assessment question
codegraph: none | optional | required
depends_on:
  - core-reviewer-id
supersedes: core-reviewer-id
---
```

`id`, `name`, `summary`, and `codegraph` are always required. `depends_on` is
required whenever the reviewer has a prerequisite reviewer; omit it only when
there is no dependency. Dependencies name core reviewer IDs and mean both
required input and execution order. Recommended inputs may name shared evidence
and completed `depends_on` handoffs only. A same-wave or later reviewer is a
downstream route, never an input. `supersedes` is
allowed only on an external reviewer and names at most one core reviewer; omit
it for an additional perspective.

IDs must be unique across discovered packages. A package is unavailable when
its metadata is malformed, a dependency is unknown, it creates a cycle, or its
platform validator lacks the matching installer, or its output menu declares
more than one reviewer-owned control namespace. Report the reason; do not
silently repair metadata.

## Discovery, Approval, And Resolution

The coordinator discovers every core and external `reviewer.md`; it does not
maintain a second reviewer registry. Core reviewers are recommended according
to the mandate. Every external reviewer is optional and must be named and
approved by the auditor before use.

An approved external `supersedes` reviewer replaces its named core reviewer:

- do not run both;
- record the substitution and absolute package path in the audit brief;
- resolve dependencies on the core ID to the replacement; and
- when multiple extensions supersede the same core reviewer, ask the auditor
  which one to use.

Selecting a reviewer also requires its declared dependencies. Present missing
dependencies with the recommendation; never expand scope silently. If the
auditor declines one, the dependent reviewer is not selected. Calculate waves
from the resolved dependency graph: run all currently unblocked reviewers in
parallel, reconcile the wave, then release the next set.

## Optional Dependency Installation

No platform `validate_install` file means no reviewer installation is needed.
Move on without mentioning installation.

For an auditor-approved external reviewer, the coordinator invokes the
platform validator by its absolute path. The validator must be read-only:

- exit `0`: the reviewer is ready;
- any other exit: pause and tell the auditor to run the matching `install`
  script, showing its full absolute path;
- never run the installer on the auditor's behalf; and
- after the auditor reports completion, rerun the validator before continuing.

The install and validation scripts belong to the extension, not WGO. They must
not alter the audited product beyond installing their declared analysis
dependencies.

## Reviewer And Orchestrator Boundary

The coordinator supplies the approved brief, reviewer card, relevant
predecessor handoffs, named evidence packets, and canonical output paths. A
reviewer may call only its own bounded workers. Workers return evidence packets;
they do not write audit artifacts, update shared state, ask the auditor, or
delegate further.

The reviewer never talks directly to the auditor. After inspecting available
evidence, it returns one exact question to the coordinator only when:

- it concerns mandate, acceptable outcome, priority, or authority the auditor
  can exercise; and
- the answer could change scope, acceptance criteria, sequencing, or the
  headline conclusion.

Proof of implementation, access, ownership, or live state is a verification,
not an auditor question. The coordinator asks qualifying questions one at a
time at a wave boundary, records each answer and effect, and then releases
dependent reviewers.

The reviewer owns evidence reconciliation, selected artifacts, `report.md`, and
`handoff.md`. It must follow WGO evidence, report, open-item, stable-ID, diagram,
and artifact-quality contracts. It must not create new shared registers,
operator aids, or state-changing procedures.

Reviewer-owned conditional outputs use exactly one `controls/<namespace>/`
root declared by their output paths. The namespace may be shorter than the
reviewer ID, but every reviewer-owned diagram stays under that same root.
Shared `controls/open-items.md` is exempt.
