# Claude Cost Estimation Dry Run

Run the inline recipe from `../../common/cost-estimation-claude.md` with
`frozen-manifest.json` and
`../../data/anthropic-api-rate-card-2026-08-07.json`.

The fixture proves that progressive copies of the root summary and child
response are each counted once. It includes the child only through matching
Agent metadata/provenance, excludes `unrelated.jsonl` despite directory/day
proximity, and excludes the root request after the explicit cost cutoff. The
reconciled exact total is USD `0.007645`.
