# Reviewer Scaffold

Copy `example-reviewer/` to create a new reviewer package:

- Core reviewer destination: `skills/wgo/references/reviewers/<reviewer-id>/`
- Project-local extension destination: `plugins/wgo-reviewers/<reviewer-id>/`

Rename the copied folder, update `reviewer.md` frontmatter, and remove comments
that do not apply. Keep one decision-relevant assessment question, one
reviewer-owned control namespace, and only the workers that collect genuinely
separate evidence slices.

Validate the package before opening a PR:

```bash
python3 skills/wgo/scripts/validate_reviewer_contract.py \
  skills/wgo/references/reviewers/<reviewer-id> \
  --core-id architecture \
  --core-id security-privacy
```

For an external package that uses `supersedes`, pass `--external` and include
all core reviewer IDs that dependencies or substitutions may reference.
