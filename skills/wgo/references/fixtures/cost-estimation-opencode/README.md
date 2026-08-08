# OpenCode Cost Estimation Dry Run

Run the inline recipe from `../../common/cost-estimation-opencode.md` with
`frozen-manifest.json` and
`../../data/opencode-cost-basis-2026-08-07.json`.

The fixture proves that the parent and child assistant messages are counted
once at message level. The deliberately inflated root session aggregate is not
added, the child's matching full-export aggregate is only reconciled, the
post-cutoff cost message is excluded, and `unrelated.json` is excluded despite
workspace/day proximity. The reconciled exact total is USD `0.0079`.
