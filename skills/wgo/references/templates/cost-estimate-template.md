# Cost Estimate Template

Replace prompts in the completed control. Preserve exact costs in the frozen
machine-readable evidence. In this Markdown control, display every priced
monetary amount as `$X.XX`, rounded half up from its exact value. Round the
exact total independently; never sum already-rounded display rows. Use
`unpriced`, not `$0.00`, when a rate is unavailable. A priced amount below half
a cent may display as `$0.00`; link its exact machine-readable value.

```markdown
# API-Equivalent Audit Cost Estimate

| Field | Value |
|---|---|
| Coverage | audit or audit-and-operationalization |
| Reconciliation status | Final or Unreconciled |
| Rate-card date | |
| Currency | USD |
| Pricing basis | API-equivalent estimate; not a Codex invoice |

## Pricing Basis And Rate Card

State the service tier, context band, rate source, and exact formula. Display
each rate and calculated cost as `$X.XX`; preserve exact decimals in the linked
calculation evidence.

## Frozen Manifest And Exclusions

Link the applicable manifest and both independent verification results. For
operationalized coverage, also link the preserved audit-only manifest.

### Phase Boundaries

| Phase | Session | Marker and JSONL line | Included or excluded |
|---|---|---|---|

### Session And Request Exclusions

| Session/request | Phase | Rationale |
|---|---|---|

## Token Totals By Session And Model

| Phase | WGO role/task | Session | Model | Service tier | Context band | Uncached input | Cached input | Output | Reasoning (informational) | Cost |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|

Add one subtotal row per phase. Reasoning is already included in output and is
never added again. Display priced costs as `$X.XX` from exact evidence.

## Model-By-Model Cost

| Model | Service tier | Context band | Input rate / 1M | Cached-input rate / 1M | Output rate / 1M | Exact-evidence status | Displayed cost |
|---|---|---|---:|---:|---:|---|---:|
| **Total** | | | | | | | **$X.XX** |

Calculate the displayed total by rounding the exact reconciled total, not by
adding displayed rows. Omit the total when the result is unreconciled.

## Reconciliation Status

State `Final` or `Unreconciled`, the two-pass comparison result, and every
disputed session/event when applicable.

## Limitations

State that this is an API-equivalent estimate rather than a Codex invoice and
that cost-calculation requests are excluded. List material evidence, schema,
pricing, attribution, and rounding limitations.
```
