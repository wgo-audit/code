# Cost Estimation Dry Run

This fixture uses the minimal Codex rollout shape used by the portable recipe:
`session_meta`, `turn_context` with `turn_id` and `model`, and
`event_msg`/`token_count` records with
`payload.info.last_token_usage` plus the cumulative `total_token_usage` object.

Run the one-off Python recipe in `../../common/cost-estimation.md` with:

```text
audit-only manifest: frozen-manifest.json
operationalized manifest: operationalized-manifest.json
rate card: ../../data/api-rate-card-2026-08-07.json
```

The expected machine-checkable results are `expected-result.json` and
`expected-operationalized-result.json`.

`root.jsonl` records onboarding, audit, summary, cost-estimation, and
operationalization phase markers plus a `sub_agent_activity` start with its
event ID, child thread ID, and agent path. `child.jsonl` is a full-history fork:
it begins with inherited root metadata and usage, then records child-specific
metadata, `task_started`, one child request echoed twice, a nested spawn, and
`task_complete`. Unrelated reuse is appended after that terminal boundary.
`nested-child.jsonl` repeats this pattern for the nested quality worker.

The manifests select the child-specific metadata and parse only each inclusive
`task_started`-through-terminal interval. They therefore exclude inherited
parent requests and later reuse. Both dry runs read only `last_token_usage`, so
inherited cumulative usage is not counted again. Because these events have no
raw request IDs, consecutive identical usage states are disclosed as unchanged
echoes and counted once under deterministic `legacy-state` identities.

The audit-only cutoff is the root's line 12
`WGO_AUDIT_COMPLETE_COST_PHASE_STARTS` marker. It produces separate onboarding,
audit, and summary rows, including both descendant levels, totaling USD
0.009573. Later records do not alter the frozen prefixes.

The operationalized cutoff is line 18
`WGO_OPERATIONALIZATION_COMPLETE_COST_PHASE_STARTS`. It adds the USD 0.00202
operationalization row while explicitly excluding the earlier line 14
cost-estimation request, producing USD 0.011593. The later refresh calculation
at lines 19–20 is outside the cutoff. This proves that refreshing
`cost-estimate.md` includes operationalization without charging either cost
calculation to the audit. The refreshed manifest also verifies the SHA-256 of
the preserved audit-only manifest before calculating.

`unrelated.jsonl` has the same workspace/day signal and a much larger request,
but no recorded collaboration spawn or task-lifecycle path from `ses-root`; it
is excluded. Both results also report 40 root `cache_write_input_tokens` as an
excluded-by-formula limitation. Pricing uses the declared standard tier and
threshold-derived short-context API-equivalent rates. It is not a Codex
invoice.

Before synthesis, the workflow separately requires the coordinator to prove
that every recursively spawned task has exactly one completed, failed,
cancelled, or interrupted outcome. Removing either fixture terminal record is
therefore a blocking lifecycle defect, not a session that may be omitted from
the manifest.
