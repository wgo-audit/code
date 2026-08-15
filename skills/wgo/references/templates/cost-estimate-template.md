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
| Rate-card/basis date | |
| Currency | USD |
| Pricing basis | Provider-specific API-equivalent estimate; not a provider invoice |

## Pricing Basis And Dated Data

State the provider, dated source, exact formula or recorded-cost rule, and the
service tier/context/geography where applicable. Display each priced component
and calculated cost as `$X.XX`; preserve exact decimals in the linked
calculation evidence.

## Frozen Manifest And Exclusions

Link the applicable manifest and both independent verification results. For
operationalized coverage, also link the preserved audit-only manifest.

### Phase Boundaries

| Phase | Session | Marker and record boundary | Included or excluded |
|---|---|---|---|

### Session And Request Exclusions

| Session/request | Phase | Rationale |
|---|---|---|

## Token Totals By Session And Model

| Phase | WGO role/task | Session | Model/provider | Service tier/basis | Uncached/new input | Cache read | Cache write | Cache-write detail | Output | Reasoning (informational) | Cost |
|---|---|---|---|---|---:|---:|---:|---|---:|---:|---:|

Add one subtotal row per phase. State whether the provider reports reasoning as
part of output or separately. Reasoning is informational and is never added a
second time to billable output or a provider-recorded cost. For Claude, split
cache writes into 5-minute and 1-hour tokens in `Cache-write detail`; for
OpenCode, state that its export does not expose the TTL split. Display priced
costs as `$X.XX` from exact evidence.

## Model-By-Model Cost

| Model/provider | Service tier/context | Rate components or recorded-cost basis | Exact-evidence status | Displayed cost |
|---|---|---|---|---:|
| **Total** | | | | **$X.XX** |

Calculate the displayed total by rounding the exact reconciled total, not by
adding displayed rows. Omit the total when the result is unreconciled.

## Reconciliation Status

State `Final` or `Unreconciled`, the two-pass comparison result, and every
disputed session/event when applicable.

## Limitations

State that this is an API-equivalent estimate rather than a Codex, Claude, or
OpenCode/provider invoice and that cost-calculation requests are excluded. List
material evidence, schema, pricing, attribution, and rounding limitations.
```

After every calculation or refresh, update `manifest.json` at
`execution.costEstimate` and validate the manifest again:

```json
{
  "basis": "api-equivalent",
  "coverage": "audit",
  "status": "final",
  "currency": "USD",
  "totalUsd": 12.35,
  "source": "controls/cost-estimate.md"
}
```

Round manifest monetary values half up from the exact machine-readable result
to dollars and cents; never store fractions of a cent there. Keep exact values
only in the frozen calculation evidence. Set `coverage` to `audit` or
`audit-and-operationalization`. For an `unreconciled` result, set `totalUsd` to
`null`; when the control reports a subtotal for reconciled included evidence,
add `reconciledSubtotalUsd`, rounded the same way. Never label that subtotal as
a total. Replace the previous object on refresh; do not append cost history or
copy token/model tables into the report manifest.
