# OpenCode Cost Estimation Workflow

Use only when the audit platform recorded in `audit-brief.md` is OpenCode. This
is a portable replay of OpenCode's provider/model token usage and exact
per-message cost estimate. It is not an OpenCode, provider, subscription, or
local-compute invoice.

The active OpenCode audit lead is the coordinator and final decision-maker.
After freezing the manifest, launch exactly two independent `general`
subagents over that manifest. They use the active audit model because OpenCode
provider/model availability is installation-specific. Do not create one worker
per session, build a universal cross-provider rate card, query the internal
SQLite database as the portable interface, or add a persistent helper program.

## 1. Export, Discover, And Freeze The OpenCode Manifest

Start with the current audit's exact OpenCode session ID supplied by the active
runtime. Export it with the installed CLI:

```text
opencode export --pure <session-id>
```

Save the exact stdout JSON as calculation evidence and validate that it parses.
If export fails or emits malformed JSON, record the file/command result and mark
the audit `Unreconciled`; never repair or silently skip it. `--sanitize` may be
used only after verifying that it preserves all session, parent, message,
provider, model, usage, cost, task-state, and phase-marker fields required here.

Recursively follow only explicit OpenCode task provenance from each included
export. A parent `tool` part with `tool: task` records the task description,
agent type, `state.metadata.sessionId`, and lifecycle state. Require the child
export's `info.id` to equal that child ID and `info.parentID` to equal the
parent. A `running` task is not terminal; require one terminal completed,
failed/error, cancelled, or interrupted state before synthesis/cost closeout.
Repeat for nested child sessions. Date, CWD, project ID, directory, agent name,
or model may corroborate provenance but never establish audit membership.

Use the exact completion marker emitted immediately before this cost phase:

- audit-only: `WGO_AUDIT_COMPLETE_COST_PHASE_STARTS`;
- through operationalization:
  `WGO_OPERATIONALIZATION_COMPLETE_COST_PHASE_STARTS`.

Freeze every validated export's whole-file SHA-256. In the root export, record
the exact assistant message ID containing the completion marker and count only
messages through that ID. The marker-producing request belongs to the phase
active before the marker; the marker changes only later attribution. Give a
descendant its phase from the recorded parent WGO task. Record all same-project
or same-day sessions considered and excluded for lacking the parent/child path.

Write `<audit-root>/controls/cost-manifest-opencode.json`, or
`cost-manifest-opencode-operationalized.json` for a refresh, before calculating:

```json
{
  "schema_version": 1,
  "provider": "opencode",
  "coverage": "audit",
  "root_session_id": "ses_root",
  "pricing_basis": {
    "basis_file": "references/data/opencode-cost-basis-2026-08-07.json",
    "opencode_version": "1.x.y",
    "zero_cost_authorizations": []
  },
  "phase_policy": {
    "included": ["unattributed", "onboarding", "audit", "summary"],
    "excluded": ["cost-estimation"],
    "markers": {
      "WGO_PHASE_ONBOARDING_START": "onboarding",
      "WGO_PHASE_AUDIT_START": "audit",
      "WGO_PHASE_SUMMARY_START": "summary",
      "WGO_AUDIT_COMPLETE_COST_PHASE_STARTS": "cost-estimation",
      "WGO_PHASE_OPERATIONALIZATION_START": "operationalization",
      "WGO_OPERATIONALIZATION_COMPLETE_COST_PHASE_STARTS": "cost-estimation"
    }
  },
  "sessions": [
    {
      "session_id": "ses_root",
      "export_path": "/audit/evidence/opencode/ses_root.json",
      "export_sha256": "...",
      "wgo_role_task_name": "OpenCode audit coordinator",
      "phase": "from-markers",
      "parent_session_id": null,
      "root_relationship": "root",
      "decision": "included",
      "rationale": "Current OpenCode audit root through the explicit marker message.",
      "cutoff": {
        "marker": "WGO_AUDIT_COMPLETE_COST_PHASE_STARTS",
        "message_id": "msg_cost_boundary"
      },
      "aggregate_reconciliation": "partial-export-not-applicable",
      "usage_schema": "opencode-export-assistant-info-v1"
    },
    {
      "session_id": "ses_child",
      "export_path": "/audit/evidence/opencode/ses_child.json",
      "export_sha256": "...",
      "wgo_role_task_name": "wgo reviewer: architecture",
      "phase": "audit",
      "parent_session_id": "ses_root",
      "root_relationship": "descendant",
      "decision": "included",
      "rationale": "Completed parent task and matching child parentID.",
      "provenance": {
        "parent_message_id": "msg_spawn",
        "task_part_id": "prt_task",
        "call_id": "call_task",
        "terminal_state": "completed"
      },
      "cutoff": {"message_id": "msg_child_last"},
      "aggregate_reconciliation": "full-export",
      "usage_schema": "opencode-export-assistant-info-v1"
    }
  ],
  "exclusions": [
    {
      "session_id": "ses_unrelated",
      "export_path": "/audit/evidence/opencode/ses_unrelated.json",
      "decision": "excluded",
      "rationale": "No task/parent path from ses_root."
    }
  ]
}
```

A zero-cost authorization must name the exact `provider_id` and `model_id`, its
rationale, and evidence that zero means no metered API charge (for example, an
explicit local-model configuration). Plan credits or a provider returning
`0` without an independently established basis are `unpriced`, not `$0.00`.

For an operationalization refresh, reference and hash the immutable audit-only
manifest, retain its session membership, and add only the explicitly invoked
operationalization root/children. Exclude both cost phases by marker. Do not
rediscover the older audit from project, directory, date, or model filters.

## 2. Calculate Message-Level Usage And Recorded Cost

Read only included exports through their frozen message cutoffs. Each assistant
message's `info.id` is the stable request/message identity. De-duplicate that ID
globally; identical repeats are echoes, while different provider, model, token,
cost, session, or phase fields are disputed. Never add `export.info.tokens`,
`export.info.cost`, database session totals, or `opencode stats` output to the
message-level totals. A full-export session aggregate may be compared to the
message sum as a separate validation only.

Total `tokens.input`, `tokens.cache.read`, `tokens.cache.write`,
`tokens.output`, and `tokens.reasoning` separately by phase, session, provider,
and model. OpenCode reports reasoning separately in this schema. It remains
informational because the recorded message `cost` already applies the selected
provider's billing semantics. The export does not expose cache-write TTL, so do
not invent a 5-minute/1-hour split.

Use the dated `../data/opencode-cost-basis-2026-08-07.json`. Sum exact positive
assistant-message `cost` values. An absent/invalid cost or unexplained zero is
`unpriced`. This deliberately avoids a stale, incomplete rate catalog for all
providers OpenCode can use. Record the OpenCode version and exact provider/model
IDs so the estimate is reproducible as a replay of what that runtime recorded.

## Portable One-Off Recipe

Run this standard-library recipe independently twice. It writes JSON to stdout
and creates no helper file.

```sh
python3 - /absolute/path/to/cost-manifest-opencode.json /absolute/path/to/opencode-cost-basis-2026-08-07.json <<'PY'
import hashlib, json, sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

manifest_path = Path(sys.argv[1]).resolve()
manifest = json.loads(manifest_path.read_text(), parse_float=Decimal)
basis = json.loads(Path(sys.argv[2]).read_text(), parse_float=Decimal)
issues, duplicates, events = [], [], {}
rows = defaultdict(lambda: {
    "input_tokens": 0, "cache_read_tokens": 0, "cache_write_tokens": 0,
    "output_tokens": 0, "reasoning_tokens": 0, "cost_usd": Decimal("0"),
    "priced": True, "message_ids": []
})
session_sums = {}
policy = manifest.get("phase_policy", {})
included_phases = set(policy.get("included", ["unattributed"]))
markers = policy.get("markers", {})
zero_authorized = {
    (item.get("provider_id"), item.get("model_id"))
    for item in manifest.get("pricing_basis", {}).get("zero_cost_authorizations", [])
    if isinstance(item, dict) and item.get("rationale")
}

def integer(value, field, session_id, message_id):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        issues.append({"kind": "schema", "session_id": session_id,
                       "message_id": message_id, "field": field})
        return None
    value = Decimal(str(value))
    if value < 0 or value != value.to_integral_value():
        issues.append({"kind": "schema", "session_id": session_id,
                       "message_id": message_id, "field": field})
        return None
    return int(value)

def money(value, session_id, message_id):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        issues.append({"kind": "invalid-cost", "session_id": session_id,
                       "message_id": message_id})
        return None
    value = Decimal(str(value))
    if value < 0:
        issues.append({"kind": "invalid-cost", "session_id": session_id,
                       "message_id": message_id})
        return None
    return value

def text(parts):
    if not isinstance(parts, list):
        return ""
    return "\n".join(part.get("text", "") for part in parts
                     if isinstance(part, dict) and part.get("type") == "text" and
                     isinstance(part.get("text"), str))

if manifest.get("provider") != "opencode":
    issues.append({"kind": "wrong-provider", "observed": manifest.get("provider")})
if basis.get("schema_version") != 1:
    issues.append({"kind": "unsupported-cost-basis"})
session_specs = {
    item.get("session_id"): item for item in manifest.get("sessions", [])
    if item.get("decision") == "included"
}

for session in manifest.get("sessions", []):
    if session.get("decision") != "included":
        continue
    session_id = session.get("session_id")
    path = Path(session.get("export_path", ""))
    if not path.is_absolute():
        path = manifest_path.parent / path
    if not path.is_file():
        issues.append({"kind": "missing-export", "session_id": session_id,
                       "export_path": str(path)})
        continue
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != session.get("export_sha256"):
        issues.append({"kind": "changed-export", "session_id": session_id,
                       "expected": session.get("export_sha256"), "actual": digest})
        continue
    try:
        export = json.loads(raw, parse_float=Decimal)
    except (UnicodeDecodeError, json.JSONDecodeError):
        issues.append({"kind": "malformed-export", "session_id": session_id})
        continue
    info, messages = export.get("info"), export.get("messages")
    if (not isinstance(info, dict) or not isinstance(messages, list) or
            info.get("id") != session_id or
            info.get("parentID") != session.get("parent_session_id")):
        issues.append({"kind": "session-provenance", "session_id": session_id})
        continue
    cutoff_id = session.get("cutoff", {}).get("message_id")
    cutoff_indexes = [index for index, message in enumerate(messages)
                      if isinstance(message, dict) and
                      isinstance(message.get("info"), dict) and
                      message["info"].get("id") == cutoff_id]
    if len(cutoff_indexes) != 1:
        issues.append({"kind": "invalid-cutoff", "session_id": session_id,
                       "message_id": cutoff_id})
        continue
    cutoff_index = cutoff_indexes[0]
    marker = session.get("cutoff", {}).get("marker")
    if marker and marker not in text(messages[cutoff_index].get("parts")):
        issues.append({"kind": "cutoff-marker-mismatch", "session_id": session_id,
                       "message_id": cutoff_id, "marker": marker})
        continue
    if session.get("root_relationship") == "descendant":
        parent = session_specs.get(session.get("parent_session_id"))
        provenance = session.get("provenance", {})
        terminal_state = provenance.get("terminal_state")
        if parent is None or terminal_state not in ("completed", "failed", "error", "cancelled", "interrupted"):
            issues.append({"kind": "missing-parent-task", "session_id": session_id})
            continue
        parent_path = Path(parent.get("export_path", ""))
        if not parent_path.is_absolute():
            parent_path = manifest_path.parent / parent_path
        if not parent_path.is_file():
            issues.append({"kind": "missing-parent-export", "session_id": session_id})
            continue
        parent_raw = parent_path.read_bytes()
        if hashlib.sha256(parent_raw).hexdigest() != parent.get("export_sha256"):
            issues.append({"kind": "changed-parent-export", "session_id": session_id})
            continue
        try:
            parent_export = json.loads(parent_raw, parse_float=Decimal)
        except (UnicodeDecodeError, json.JSONDecodeError):
            issues.append({"kind": "malformed-parent-export", "session_id": session_id})
            continue
        parent_messages = parent_export.get("messages", [])
        parent_message_id = provenance.get("parent_message_id")
        parent_matches = [
            (index, message) for index, message in enumerate(parent_messages)
            if isinstance(message, dict) and isinstance(message.get("info"), dict) and
            message["info"].get("id") == parent_message_id
        ]
        parent_cutoff_id = parent.get("cutoff", {}).get("message_id")
        parent_cutoffs = [
            index for index, message in enumerate(parent_messages)
            if isinstance(message, dict) and isinstance(message.get("info"), dict) and
            message["info"].get("id") == parent_cutoff_id
        ]
        if len(parent_matches) != 1 or len(parent_cutoffs) != 1 or parent_matches[0][0] > parent_cutoffs[0]:
            issues.append({"kind": "parent-task-boundary", "session_id": session_id})
            continue
        task_parts = [
            part for part in parent_matches[0][1].get("parts", [])
            if isinstance(part, dict) and part.get("type") == "tool" and
            part.get("tool") == "task" and part.get("id") == provenance.get("task_part_id")
        ]
        if len(task_parts) != 1:
            issues.append({"kind": "parent-task-part", "session_id": session_id})
            continue
        task = task_parts[0]
        state = task.get("state", {})
        if (task.get("callID") != provenance.get("call_id") or
                state.get("status") != terminal_state or
                state.get("metadata", {}).get("sessionId") != session_id):
            issues.append({"kind": "parent-task-provenance", "session_id": session_id})
            continue

    active_phase = "unattributed"
    fixed_phase = session.get("phase")
    aggregate = {"input": 0, "output": 0, "reasoning": 0,
                 "cache_read": 0, "cache_write": 0, "cost": Decimal("0")}
    for message in messages[:cutoff_index + 1]:
        message_info = message.get("info", {}) if isinstance(message, dict) else {}
        if message_info.get("role") != "assistant":
            continue
        message_id = message_info.get("id")
        provider_id = message_info.get("providerID")
        model_id = message_info.get("modelID")
        tokens = message_info.get("tokens")
        phase = active_phase if fixed_phase == "from-markers" else fixed_phase
        if (not all(isinstance(value, str) and value for value in
                    (message_id, provider_id, model_id)) or not isinstance(tokens, dict)):
            issues.append({"kind": "message-schema", "session_id": session_id,
                           "message_id": message_id})
        else:
            cache = tokens.get("cache", {})
            if not isinstance(cache, dict):
                cache = {}
            values = {
                "input_tokens": integer(tokens.get("input"), "tokens.input", session_id, message_id),
                "cache_read_tokens": integer(cache.get("read", 0), "tokens.cache.read", session_id, message_id),
                "cache_write_tokens": integer(cache.get("write", 0), "tokens.cache.write", session_id, message_id),
                "output_tokens": integer(tokens.get("output"), "tokens.output", session_id, message_id),
                "reasoning_tokens": integer(tokens.get("reasoning", 0), "tokens.reasoning", session_id, message_id)
            }
            cost = money(message_info.get("cost"), session_id, message_id)
            if all(value is not None for value in values.values()) and cost is not None:
                event = {"message_id": message_id, "session_id": session_id,
                         "phase": phase, "provider_id": provider_id,
                         "model_id": model_id, "cost_usd": cost, **values}
                fingerprint = tuple(event[key] for key in (
                    "session_id", "phase", "provider_id", "model_id", "input_tokens",
                    "cache_read_tokens", "cache_write_tokens", "output_tokens",
                    "reasoning_tokens", "cost_usd"))
                if message_id in events:
                    duplicates.append({"kind": "stable-message-id", "message_id": message_id,
                                       "first_session_id": events[message_id]["session_id"],
                                       "duplicate_session_id": session_id})
                    if events[message_id]["fingerprint"] != fingerprint:
                        issues.append({"kind": "disputed-message", "message_id": message_id,
                                       "first_session_id": events[message_id]["session_id"],
                                       "second_session_id": session_id})
                else:
                    event["fingerprint"] = fingerprint
                    events[message_id] = event
                    for source, target in (("input_tokens", "input"),
                                           ("cache_read_tokens", "cache_read"),
                                           ("cache_write_tokens", "cache_write"),
                                           ("output_tokens", "output"),
                                           ("reasoning_tokens", "reasoning")):
                        aggregate[target] += event[source]
                    aggregate["cost"] += cost
        if fixed_phase == "from-markers":
            body = text(message.get("parts", []))
            for marker_name, next_phase in markers.items():
                if marker_name in body:
                    active_phase = next_phase
    session_sums[session_id] = aggregate

    if session.get("aggregate_reconciliation") == "full-export":
        reported_tokens = info.get("tokens", {})
        reported_cache = reported_tokens.get("cache", {}) if isinstance(reported_tokens, dict) else {}
        observed = {
            "input": reported_tokens.get("input") if isinstance(reported_tokens, dict) else None,
            "output": reported_tokens.get("output") if isinstance(reported_tokens, dict) else None,
            "reasoning": reported_tokens.get("reasoning") if isinstance(reported_tokens, dict) else None,
            "cache_read": reported_cache.get("read") if isinstance(reported_cache, dict) else None,
            "cache_write": reported_cache.get("write") if isinstance(reported_cache, dict) else None,
            "cost": Decimal(str(info.get("cost"))) if isinstance(info.get("cost"), (int, float, Decimal)) and not isinstance(info.get("cost"), bool) else None
        }
        if any(observed[key] != aggregate[key] for key in aggregate):
            issues.append({"kind": "session-aggregate-mismatch", "session_id": session_id,
                           "message_sum": {key: str(value) for key, value in aggregate.items()},
                           "reported": {key: str(value) for key, value in observed.items()}})

for message_id, event in sorted(events.items()):
    if event["phase"] not in included_phases:
        continue
    key = (event["phase"], event["session_id"], event["provider_id"], event["model_id"])
    row = rows[key]
    for field in ("input_tokens", "cache_read_tokens", "cache_write_tokens",
                  "output_tokens", "reasoning_tokens"):
        row[field] += event[field]
    row["message_ids"].append(message_id)
    if event["cost_usd"] == 0 and (event["provider_id"], event["model_id"]) not in zero_authorized:
        row["priced"] = False
        issues.append({"kind": "unpriced-zero", "message_id": message_id,
                       "provider_id": event["provider_id"], "model_id": event["model_id"]})
    else:
        row["cost_usd"] += event["cost_usd"]

flat = []
for (phase, session_id, provider_id, model_id), row in sorted(rows.items()):
    row.update({"phase": phase, "session_id": session_id,
                "provider_id": provider_id, "model_id": model_id})
    row["cost_usd"] = str(row["cost_usd"]) if row["priced"] else None
    flat.append(row)
total = None if issues else str(sum(Decimal(row["cost_usd"]) for row in flat))
print(json.dumps({"rows": flat, "duplicates": duplicates, "issues": issues,
                  "total_cost_usd": total}, indent=2))
PY
```

## 3. Independent Verification And Output

Give both workers the same immutable manifest, exports, cost-basis file, and
this prompt:

```text
You are an OpenCode cost-calculation worker. Use only the frozen manifest and validated exports. De-duplicate assistant messages by info.id, total provider/model token fields, and replay exact per-message cost. Do not discover sessions, add session aggregates, invent rates or cache TTLs, or accept an unexplained zero as free. Flag exact disputed messages and malformed evidence.
```

Preserve results as `cost-opencode-pass-a.json` and
`cost-opencode-pass-b.json` (or `*-operationalized-*`). Compare them exactly
after normalizing row order. Investigate every mismatch by session, message ID,
provider/model, and field. Any mismatch remains `Unreconciled`.

Read `../templates/cost-estimate-template.md` immediately before writing
`controls/cost-estimate.md`. Link the manifest, validated exports, cost-basis
file, and both results. Show phase/session/provider/model tokens and the exact
recorded-cost basis. State that reasoning is separate and cache-write TTL is not
reported. Publish a total only when all included messages reconcile and are
priced. Display `$X.XX` while preserving exact decimals in JSON evidence.

Always state that this replays OpenCode's API-equivalent estimate and is not a
provider invoice. List export availability/validity, OpenCode version, provider
rate drift, custom or subscription pricing, local compute/electricity,
unexplained zero costs, and non-token charges as limitations. See
`../fixtures/cost-estimation-opencode/README.md` for the dry run.
