# Claude Cost Estimation Workflow

Use only when the audit platform recorded in `audit-brief.md` is Claude. This
is a portable Anthropic-API-equivalent estimate from Claude Code's own root and
subagent JSONL records. It is not a Claude subscription or provider invoice.

The active Claude audit lead is the coordinator and final decision-maker. After
freezing the manifest, launch exactly two independent `haiku` Agent workers to
run the bounded calculation below. If `haiku` is unavailable, use the active
Claude model and disclose the substitution. Do not create one worker per
session, use `/usage` or `/cost` as the source of truth, install a package, or
add a persistent helper program.

## 1. Discover And Freeze The Claude Manifest

Start with the current audit's exact Claude root session ID from runtime/session
metadata. Resolve that ID to its transcript under Claude's application-data
directory. Never select a session by date, CWD, project-directory encoding, or
model; those may corroborate an ID but cannot establish membership.

Recursively inspect only that root and its proven descendants:

1. Find an assistant `Agent` or `Task` `tool_use` and record its tool-use ID,
   description/WGO role, and parent transcript.
2. Match it to exactly one `subagents/agent-<agent-id>.meta.json` whose
   `toolUseId` matches. Require the child JSONL records to carry that `agentId`
   and the audit root `sessionId`.
3. Require exactly one terminal result. A synchronous result has the matching
   tool-use ID and terminal `toolUseResult.status`. For an asynchronous launch,
   `async_launched` is not terminal: require the later `task-notification` with
   matching agent/task ID and `completed`, `failed`, `cancelled`, or
   `interrupted` status.
4. Repeat for nested Agent/Task spawns found in an included child transcript.

A missing transcript, metadata file, parent link, or terminal outcome is a
named reconciliation issue. Exclude other sessions and subagents in the same
project/day explicitly. Claude's documented transcript location is supporting
storage information, not proof that every file there belongs to this audit.

Use the completion marker emitted immediately before this cost phase:

- audit-only: `WGO_AUDIT_COMPLETE_COST_PHASE_STARTS`;
- through operationalization:
  `WGO_OPERATIONALIZATION_COMPLETE_COST_PHASE_STARTS`.

For the root, freeze the exact byte prefix through the line containing that
marker, including its terminating newline. For each terminal descendant, freeze
its complete JSONL and its metadata file, plus the exact parent spawn and
terminal line numbers. The parent marker's request belongs to the phase active
before the marker; the marker changes attribution only for later requests.

Write
`<project-root>/tmp_debug/wgo-cost/<audit-id>/cost-manifest-claude.json`, or
`cost-manifest-claude-operationalized.json` beside it for the refresh, before
calculating. These files are temporary working data outside the audit root; the
public cost control and receipt use audit-local aliases only.
Do not rewrite a manifest to make two calculations agree. Include at least:

Resolve Claude's application-data/session root as a transient runtime path.
Every `file_path` and `metadata_path` persisted in the manifest is portable and
relative to that root; never store the root or an absolute provider path in an
audit artifact. Pass the runtime root separately to the one-off recipe.

```json
{
  "schema_version": 1,
  "provider": "claude-code",
  "coverage": "audit",
  "root_session_id": "root-session-uuid",
  "pricing_basis": {
    "rate_card": "references/data/anthropic-api-rate-card-2026-08-07.json",
    "default_service_tier_when_not_returned": "standard",
    "default_inference_geo_when_not_returned": "global"
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
      "record_set_id": "root-session-uuid",
      "session_id": "root-session-uuid",
      "agent_id": null,
      "file_path": "root-session-uuid.jsonl",
      "prefix_sha256": "...",
      "wgo_role_task_name": "Claude audit coordinator",
      "phase": "from-markers",
      "parent_record_set_id": null,
      "root_relationship": "root",
      "decision": "included",
      "rationale": "Current Claude audit root through the explicit cutoff.",
      "cutoff": {
        "marker": "WGO_AUDIT_COMPLETE_COST_PHASE_STARTS",
        "line_number": 81
      },
      "usage_schema": "claude-code-assistant-message-usage-v1"
    },
    {
      "record_set_id": "root-session-uuid:agent:abc123",
      "session_id": "root-session-uuid",
      "agent_id": "abc123",
      "file_path": "root-session-uuid/subagents/agent-abc123.jsonl",
      "prefix_sha256": "...",
      "metadata_path": "root-session-uuid/subagents/agent-abc123.meta.json",
      "metadata_sha256": "...",
      "tool_use_id": "toolu_123",
      "wgo_role_task_name": "wgo reviewer: security-privacy",
      "phase": "audit",
      "parent_record_set_id": "root-session-uuid",
      "root_relationship": "descendant",
      "decision": "included",
      "rationale": "Matching spawn, subagent metadata, child agentId, and terminal result.",
      "lifecycle": {
        "spawn_line": 20,
        "terminal_line": 62,
        "outcome": "completed"
      },
      "cutoff": {"line_number": 40},
      "usage_schema": "claude-code-assistant-message-usage-v1"
    }
  ],
  "exclusions": [
    {
      "record_set_id": "unrelated-session",
      "file_path": "unrelated.jsonl",
      "decision": "excluded",
      "rationale": "No Agent/Task provenance path from the audit root."
    }
  ]
}
```

For an operationalization refresh, verify and reference the immutable
audit-only manifest, retain its membership, and add only the explicitly invoked
operationalization root/descendants. Extend a reused root only in the new
manifest. Exclude both cost phases by marker. Never rediscover the older audit
from dates or directory proximity.

## 2. Calculate Request-Level Usage

Read only included manifest prefixes. A request record is a Claude JSONL
`type: assistant` record with `message.model` and `message.usage`. Use
top-level `requestId`; fall back to `message.id` only when the request ID is
absent. Claude may append progressive copies of one assistant response. For a
stable ID, require the same message ID, model, phase, service tier, geography,
input, cache-creation, and cache-read values, then retain only the last
non-decreasing `output_tokens` value. Identical repeats are echoes. A changed
fixed field, message ID, phase, or decreasing output is disputed; do not choose
one silently.

Total separately: input, 5-minute cache creation, 1-hour cache creation, cache
read, and output. Claude Code does not expose a separate reasoning-token total
in this schema. Require the nested 5-minute/1-hour cache split to equal
`cache_creation_input_tokens`; a nonzero unsplit value is unpriced. Never add a
tool result's aggregate `usage` or `totalTokens` to assistant-message usage.

Use `../data/anthropic-api-rate-card-2026-08-07.json`. Price only exact model
and service-tier matches:

```text
input × input rate
+ 5-minute cache creation × 5-minute write rate
+ 1-hour cache creation × 1-hour write rate
+ cache read × cache-read rate
+ output × output rate
```

Apply the US geography multiplier only when `inference_geo` is `us`. When the
field is missing or `not_available`, use the manifest's declared global
API-equivalent basis and disclose that geography was not observed. An unknown
model, tier, geography, cache split, or expired dated rate is `unpriced`, never
zero.

## Portable One-Off Recipe

Run this standard-library recipe independently twice. It writes JSON to stdout
and creates no helper file.

```sh
python3 - /absolute/path/to/cost-manifest-claude.json /absolute/path/to/anthropic-api-rate-card-2026-08-07.json /absolute/claude/session-store/root <<'PY'
import hashlib, json, sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

manifest_path = Path(sys.argv[1]).resolve()
manifest = json.loads(manifest_path.read_text(), parse_float=Decimal)
rates = json.loads(Path(sys.argv[2]).read_text(), parse_float=Decimal)
source_root = Path(sys.argv[3]).resolve()
issues, limitations, duplicates, events, invalid = [], [], [], {}, set()
rows = defaultdict(lambda: {
    "input_tokens": 0, "cache_write_5m_tokens": 0,
    "cache_write_1h_tokens": 0, "cache_read_tokens": 0,
    "output_tokens": 0, "reasoning_tokens": None,
    "cost_usd": Decimal("0"), "priced": True, "request_ids": []
})
policy = manifest.get("phase_policy", {})
included_phases = set(policy.get("included", ["unattributed"]))
markers = policy.get("markers", {})
default_tier = manifest["pricing_basis"]["default_service_tier_when_not_returned"]
default_geo = manifest["pricing_basis"]["default_inference_geo_when_not_returned"]

def integer(value, field, record_set_id, line):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        issues.append({"kind": "schema", "record_set_id": record_set_id,
                       "line_number": line, "field": field})
        return None
    value = Decimal(str(value))
    if value < 0 or value != value.to_integral_value():
        issues.append({"kind": "schema", "record_set_id": record_set_id,
                       "line_number": line, "field": field})
        return None
    return int(value)

def message_text(message):
    content = message.get("content", [])
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(item.get("text", "") for item in content
                     if isinstance(item, dict) and isinstance(item.get("text"), str))

if manifest.get("provider") != "claude-code":
    issues.append({"kind": "wrong-provider", "observed": manifest.get("provider")})
session_specs = {
    item.get("record_set_id"): item for item in manifest.get("sessions", [])
    if item.get("decision") == "included"
}

for session in manifest.get("sessions", []):
    if session.get("decision") != "included":
        continue
    record_set_id = session.get("record_set_id")
    locator = session.get("file_path", "")
    path = Path(locator)
    if path.is_absolute() or ".." in path.parts:
        issues.append({"kind": "nonportable-file-path", "record_set_id": record_set_id})
        continue
    path = source_root / path
    if not path.is_file():
        issues.append({"kind": "missing-file", "record_set_id": record_set_id,
                       "file_path": locator})
        continue
    lines = path.read_bytes().splitlines(keepends=True)
    end = session.get("cutoff", {}).get("line_number")
    if not isinstance(end, int) or end < 1 or end > len(lines):
        issues.append({"kind": "invalid-cutoff", "record_set_id": record_set_id})
        continue
    prefix = b"".join(lines[:end])
    digest = hashlib.sha256(prefix).hexdigest()
    if digest != session.get("prefix_sha256"):
        issues.append({"kind": "changed-prefix", "record_set_id": record_set_id,
                       "expected": session.get("prefix_sha256"), "actual": digest})
        continue
    marker = session.get("cutoff", {}).get("marker")
    if marker and marker.encode() not in lines[end - 1]:
        issues.append({"kind": "cutoff-marker-mismatch",
                       "record_set_id": record_set_id, "marker": marker})
        continue
    if session.get("root_relationship") == "descendant":
        metadata_locator = session.get("metadata_path", "")
        meta_path = Path(metadata_locator)
        if meta_path.is_absolute() or ".." in meta_path.parts:
            issues.append({"kind": "nonportable-metadata-path",
                           "record_set_id": record_set_id})
            continue
        meta_path = source_root / meta_path
        if not meta_path.is_file():
            issues.append({"kind": "missing-subagent-metadata",
                           "record_set_id": record_set_id})
            continue
        meta_bytes = meta_path.read_bytes()
        if hashlib.sha256(meta_bytes).hexdigest() != session.get("metadata_sha256"):
            issues.append({"kind": "changed-subagent-metadata",
                           "record_set_id": record_set_id})
            continue
        try:
            meta = json.loads(meta_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError):
            issues.append({"kind": "invalid-subagent-metadata",
                           "record_set_id": record_set_id})
            continue
        if meta.get("toolUseId") != session.get("tool_use_id"):
            issues.append({"kind": "subagent-tool-use-mismatch",
                           "record_set_id": record_set_id})
            continue
        parent = session_specs.get(session.get("parent_record_set_id"))
        lifecycle = session.get("lifecycle", {})
        spawn_line, terminal_line = lifecycle.get("spawn_line"), lifecycle.get("terminal_line")
        outcome = lifecycle.get("outcome")
        if parent is None or outcome not in ("completed", "failed", "cancelled", "interrupted"):
            issues.append({"kind": "missing-parent-lifecycle",
                           "record_set_id": record_set_id})
            continue
        parent_path = Path(parent.get("file_path", ""))
        if parent_path.is_absolute() or ".." in parent_path.parts:
            issues.append({"kind": "nonportable-parent-path",
                           "record_set_id": record_set_id})
            continue
        parent_path = source_root / parent_path
        if not parent_path.is_file():
            issues.append({"kind": "missing-parent-file", "record_set_id": record_set_id})
            continue
        parent_lines = parent_path.read_bytes().splitlines(keepends=True)
        parent_end = parent.get("cutoff", {}).get("line_number")
        if (not isinstance(spawn_line, int) or not isinstance(terminal_line, int) or
                not isinstance(parent_end, int) or not 1 <= spawn_line <= terminal_line <= parent_end or
                parent_end > len(parent_lines)):
            issues.append({"kind": "invalid-parent-lifecycle",
                           "record_set_id": record_set_id})
            continue
        try:
            spawn = json.loads(parent_lines[spawn_line - 1])
            terminal = json.loads(parent_lines[terminal_line - 1])
        except (UnicodeDecodeError, json.JSONDecodeError):
            issues.append({"kind": "invalid-parent-lifecycle-json",
                           "record_set_id": record_set_id})
            continue
        spawn_content = spawn.get("message", {}).get("content", [])
        spawn_matches = [item for item in spawn_content if isinstance(item, dict) and
                         item.get("type") == "tool_use" and
                         item.get("name") in ("Agent", "Task") and
                         item.get("id") == session.get("tool_use_id")]
        terminal_content = terminal.get("message", {}).get("content")
        synchronous = (
            isinstance(terminal_content, list) and
            any(isinstance(item, dict) and item.get("type") == "tool_result" and
                item.get("tool_use_id") == session.get("tool_use_id")
                for item in terminal_content) and
            terminal.get("toolUseResult", {}).get("agentId") == session.get("agent_id") and
            terminal.get("toolUseResult", {}).get("status") == outcome
        )
        asynchronous = (
            isinstance(terminal_content, str) and
            f"<task-id>{session.get('agent_id')}</task-id>" in terminal_content and
            f"<status>{outcome}</status>" in terminal_content
        )
        if len(spawn_matches) != 1 or not (synchronous or asynchronous):
            issues.append({"kind": "parent-lifecycle-mismatch",
                           "record_set_id": record_set_id})
            continue

    active_phase = "unattributed"
    fixed_phase = session.get("phase")
    for line_number, raw in enumerate(lines[:end], 1):
        try:
            record = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            issues.append({"kind": "invalid-json", "record_set_id": record_set_id,
                           "line_number": line_number})
            continue
        if record.get("type") != "assistant" or not isinstance(record.get("message"), dict):
            continue
        message = record["message"]
        usage = message.get("usage")
        phase = active_phase if fixed_phase == "from-markers" else fixed_phase
        if isinstance(usage, dict):
            request_id = record.get("requestId") or message.get("id")
            message_id = message.get("id")
            model = message.get("model")
            observed_session = record.get("sessionId")
            observed_agent = record.get("agentId")
            if (not all(isinstance(value, str) and value for value in
                        (request_id, message_id, model)) or
                    observed_session != session.get("session_id") or
                    observed_agent != session.get("agent_id")):
                issues.append({"kind": "identity", "record_set_id": record_set_id,
                               "line_number": line_number})
            else:
                inp = integer(usage.get("input_tokens"), "input_tokens", record_set_id, line_number)
                creation = integer(usage.get("cache_creation_input_tokens", 0),
                                   "cache_creation_input_tokens", record_set_id, line_number)
                read = integer(usage.get("cache_read_input_tokens", 0),
                               "cache_read_input_tokens", record_set_id, line_number)
                output = integer(usage.get("output_tokens"), "output_tokens", record_set_id, line_number)
                split = usage.get("cache_creation", {})
                five = integer(split.get("ephemeral_5m_input_tokens", 0),
                               "ephemeral_5m_input_tokens", record_set_id, line_number) if isinstance(split, dict) else None
                hour = integer(split.get("ephemeral_1h_input_tokens", 0),
                               "ephemeral_1h_input_tokens", record_set_id, line_number) if isinstance(split, dict) else None
                tier = usage.get("service_tier") or default_tier
                observed_geo = usage.get("inference_geo")
                geo = default_geo if observed_geo in (None, "", "not_available") else observed_geo
                if observed_geo in (None, "", "not_available"):
                    limitations.append({"kind": "declared-inference-geo", "request_id": request_id,
                                        "record_set_id": record_set_id, "basis": geo})
                if None not in (inp, creation, read, output, five, hour):
                    if five + hour != creation:
                        issues.append({"kind": "cache-creation-split", "request_id": request_id,
                                       "record_set_id": record_set_id, "line_number": line_number})
                        invalid.add(request_id)
                    fixed = (message_id, model, phase, tier, geo, inp, five, hour, read)
                    event = {"request_id": request_id, "message_id": message_id,
                             "record_set_id": record_set_id, "session_id": session.get("session_id"),
                             "agent_id": session.get("agent_id"), "line_number": line_number,
                             "phase": phase, "model": model, "service_tier": tier,
                             "inference_geo": geo, "input_tokens": inp,
                             "cache_write_5m_tokens": five, "cache_write_1h_tokens": hour,
                             "cache_read_tokens": read, "output_tokens": output,
                             "fixed": fixed}
                    previous = events.get(request_id)
                    if previous is None:
                        events[request_id] = event
                    elif previous["fixed"] != fixed or output < previous["output_tokens"]:
                        issues.append({"kind": "disputed-request", "request_id": request_id,
                                       "first": {"record_set_id": previous["record_set_id"],
                                                 "line_number": previous["line_number"]},
                                       "second": {"record_set_id": record_set_id,
                                                  "line_number": line_number}})
                        invalid.add(request_id)
                    else:
                        duplicates.append({"kind": "progressive" if output > previous["output_tokens"] else "echo",
                                           "request_id": request_id,
                                           "earlier": {"record_set_id": previous["record_set_id"],
                                                       "line_number": previous["line_number"]},
                                           "retained": {"record_set_id": record_set_id,
                                                        "line_number": line_number}})
                        events[request_id] = event
        if fixed_phase == "from-markers":
            text = message_text(message)
            for marker_name, next_phase in markers.items():
                if marker_name in text:
                    active_phase = next_phase

for request_id, event in sorted(events.items()):
    if request_id in invalid or event["phase"] not in included_phases:
        continue
    key = (event["phase"], event["record_set_id"], event["model"],
           event["service_tier"], event["inference_geo"])
    row = rows[key]
    for field in ("input_tokens", "cache_write_5m_tokens", "cache_write_1h_tokens",
                  "cache_read_tokens", "output_tokens"):
        row[field] += event[field]
    row["request_ids"].append(request_id)
    try:
        rate = rates["models"][event["model"]][event["service_tier"]]
        multiplier = rates["inference_geo_multipliers"][event["inference_geo"]]
    except KeyError:
        row["priced"] = False
        issues.append({"kind": "unpriced", "request_id": request_id,
                       "model": event["model"], "service_tier": event["service_tier"],
                       "inference_geo": event["inference_geo"]})
        continue
    row["cost_usd"] += multiplier * (
        Decimal(event["input_tokens"]) * rate["input"] +
        Decimal(event["cache_write_5m_tokens"]) * rate["cache_write_5m"] +
        Decimal(event["cache_write_1h_tokens"]) * rate["cache_write_1h"] +
        Decimal(event["cache_read_tokens"]) * rate["cache_read"] +
        Decimal(event["output_tokens"]) * rate["output"]
    ) / Decimal(1000000)

flat = []
for (phase, record_set_id, model, tier, geo), row in sorted(rows.items()):
    row.update({"phase": phase, "record_set_id": record_set_id, "model": model,
                "service_tier": tier, "inference_geo": geo})
    row["cost_usd"] = str(row["cost_usd"]) if row["priced"] else None
    flat.append(row)
total = None if issues else str(sum(Decimal(row["cost_usd"]) for row in flat))
print(json.dumps({"rows": flat, "duplicates": duplicates, "issues": issues,
                  "limitations": limitations, "total_cost_usd": total}, indent=2))
PY
```

## 3. Independent Verification And Output

Give both workers the same immutable manifest, JSONL prefixes, metadata files,
rate card, and this prompt:

```text
You are a Claude cost-calculation worker. Use only the frozen manifest. Parse Claude assistant-message usage at request level, collapse progressive copies by stable request/message ID, and return the recipe's machine-checkable table. Do not discover sessions, count Agent tool-result aggregates, or guess missing cache splits, models, tiers, geography, or prices. Flag exact disputed records.
```

Preserve temporary results beside the manifest as `cost-claude-pass-a.json` and
`cost-claude-pass-b.json` (or `*-operationalized-*`). Compare them exactly after
normalizing row order. Any mismatch names the record set, request ID, line, and
field and leaves the result `Unreconciled`.

Read `../templates/cost-estimate-template.md` immediately before writing
`controls/cost-estimate.md` and the alias-only
`controls/cost-calculation.json` receipt. Do not link the temporary manifest or
pass files. Show token
totals by phase, record set/session, model, tier, and geography; show the two
cache-write TTLs; show exact rate components and a total only when all included
requests reconcile and are priced. Display money as `$X.XX` while preserving
exact decimals in the public receipt.

Always state that this is an Anthropic-API-equivalent estimate, not Claude Code
subscription or provider billing. Include transcript retention/access,
plaintext-sensitive-data handling, progressive-record handling, declared
geography, unknown model/tier/rate, non-token tool charges, and rate-card expiry
among the limitations. See `../fixtures/cost-estimation-claude/README.md` for
the dry run.
