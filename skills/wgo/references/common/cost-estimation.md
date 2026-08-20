# Codex Cost Estimation Workflow

Use only when the audit platform recorded in `audit-brief.md` is Codex. Use for
`wgo:cost`, at the end of `wgo:summarize`, and after a requested
`wgo:operationalize`. This is a portable, API-equivalent estimate of the
completed work's recorded model requests. It is not a Codex invoice.

Terra at high reasoning is the coordinator and final decision-maker. Two
independent Terra workers at high reasoning only extract and verify usage from
the coordinator's already frozen manifest. Do not
create a worker per audit session, install a package, invoke `ccusage`, or add
a persistent helper program.

## 1. Discover And Freeze The Audit Manifest

For audit-only coverage, before opening a calculator or delegating work, Terra
finds the current audit's root Codex session transcript among the accessible
session JSONL roots. Use the runtime's current root-session metadata and inspect
the JSONL headers/records to find its matching session ID and path. For an
operationalization refresh, use the preserved audit-only manifest plus the
current operationalization root as described below. If either required root
cannot be established from accessible records, write an `Unreconciled` cost
control with that exact limit; do not estimate an assumed session set.

Scan accessible JSONL files, not a date, CWD, project folder, or model filter.
Those attributes may corroborate a result but never establish membership. From
the root transcript, recursively follow only recorded Codex/WGO collaboration
spawn links and corresponding task-lifecycle records. Treat the transcript as
a versioned provider schema: current Codex Desktop records lifecycle
correlation in `payload.turn_id`, while older records may use
`payload.task_id`. For every candidate,
resolve its session ID to its own JSONL record and require provenance that ties
the spawned task to its parent and WGO role/task name. A missing child file,
missing lifecycle correlation, ambiguous parent, or unrelated later reuse is a
manifest exclusion with its exact reason and a reconciliation issue.

Use the exact completion marker emitted immediately before this cost phase:

- audit-only: `WGO_AUDIT_COMPLETE_COST_PHASE_STARTS`;
- through operationalization:
  `WGO_OPERATIONALIZATION_COMPLETE_COST_PHASE_STARTS`.

Locate the recorded response/message line containing the applicable marker,
record its line number in the manifest, and freeze through that line. For
standalone `wgo:cost`, use the latest applicable existing completion marker;
if none exists, emit the audit-only marker before calculation. The root prefix
may contain an earlier cost phase when operationalization follows synthesis;
phase attribution below excludes its requests. For every descendant, record
both boundaries of its WGO task lifecycle: the `task_started` line and exactly
one correlated terminal `task_complete`, `task_failed`, `task_cancelled`,
`task_interrupted`, or `turn_aborted` line. Correlate on `turn_id` when
present, falling back to the legacy `task_id` only when that is the field
actually observed. Parse only that inclusive interval. Do not parse
inherited history before `task_started`; when a session later does unrelated
work, stop at its terminal audit-task event. Record the exact child-specific
`session_meta` line separately and require its session ID to match the
manifest. A current child transcript normally places that metadata first,
before inherited history. In current child metadata, `payload.id` is the child
session ID while `payload.session_id` may retain the forked root; use
`payload.id` when present and fall back to `payload.session_id` only for a
legacy record that has no `id`. Never select whichever metadata record happens
to appear last. Use
recorded lifecycle markers and line positions (plus stable record IDs when
present), not a timestamp alone. Hash the exact byte prefix through each
cutoff, including its terminating newline when present. Do not hash the whole
JSONL: later reuse may append records, but any mutation before the frozen
cutoff is unreconciled.

The audit coordinator must already have passed the delegated-task lifecycle
gate before synthesis: every recursively spawned WGO task has exactly one
recorded terminal outcome. An open, multiply terminated, or ambiguously
correlated task blocks synthesis; it is not silently dropped from the cost
manifest.

Before calculation, freeze
`<project-root>/tmp_debug/wgo-cost/<audit-id>/cost-manifest.json` for the
audit-only closeout or `cost-manifest-operationalized.json` beside it for the
refresh.
Each is an immutable input for its calculation; never revise the audit-only
file or either manifest to make worker results match. The refreshed manifest
must list delegated earlier cost sessions as explicit exclusions and exclude
same-session cost requests through its phase policy. It must contain, at
minimum:

If an earlier closeout froze an `Unreconciled` manifest because its inspected
Codex schema was wrong, preserve that evidence and create the next available
`cost-manifest-repair-N.json`. Record the superseded manifest's portable path,
SHA-256, and reason in `supersedes`; use the same `-repair-N` suffix for both
worker result files. A repair corrects a demonstrated adapter/schema error; it
never changes membership merely to force agreement.

These provider-native manifests and calculation results are temporary working
data. They may retain provider session identifiers needed for verification,
but they never enter the audit root or `wgo:upload`. Resolve the Codex
session-store root as a transient runtime path. Every `file_path` in the
temporary manifest is relative to that root. Pass the runtime root separately
to the one-off recipe.

```json
{
  "schema_version": 3,
  "coverage": "audit",
  "root_session_id": "ses_root",
  "session_store": "codex-session-store",
  "pricing_basis": {
    "rate_card": "references/data/api-rate-card-2026-08-07.json",
    "default_service_tier_when_not_returned": "standard",
    "note": "Declared API-equivalent basis, not actual Codex backend tier."
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
  "phase_boundaries": [
    {"phase": "summary", "marker": "WGO_PHASE_SUMMARY_START", "session_id": "ses_root", "line_number": 70},
    {"phase": "cost-estimation", "marker": "WGO_AUDIT_COMPLETE_COST_PHASE_STARTS", "session_id": "ses_root", "line_number": 81}
  ],
  "root_cutoff": {"marker": "WGO_AUDIT_COMPLETE_COST_PHASE_STARTS", "line_number": 81},
  "sessions": [
    {
      "session_id": "ses_root",
      "file_path": "2026/08/06/root.jsonl",
      "prefix_sha256": "...",
      "wgo_role_task_name": "Terra audit coordinator",
      "phase": "from-markers",
      "parent_session_id": null,
      "root_relationship": "root",
      "decision": "included",
      "rationale": "Current audit root through explicit cost-phase cutoff.",
      "session_meta": {"line_number": 1, "session_id": "ses_root"},
      "lifecycle": null,
      "cutoff": {"marker": "WGO_AUDIT_COMPLETE_COST_PHASE_STARTS", "line_number": 81},
      "provenance": [{"kind": "session_meta"}, {"kind": "sub_agent_activity"}],
      "usage_schema": "codex-rollout-token-count-v1"
    },
    {
      "session_id": "ses_child",
      "file_path": "2026/08/06/child.jsonl",
      "prefix_sha256": "...",
      "wgo_role_task_name": "wgo reviewer: code-quality",
      "phase": "audit",
      "parent_session_id": "ses_root",
      "root_relationship": "descendant",
      "decision": "included",
      "rationale": "Recorded spawn, matching child metadata, and one bounded lifecycle.",
      "session_meta": {"line_number": 1, "session_id": "ses_child"},
      "lifecycle": {
        "turn_id": "turn_code_quality",
        "start": {"event": "task_started", "line_number": 65},
        "terminal": {"event": "task_complete", "outcome": "completed", "line_number": 92}
      },
      "cutoff": {"provenance": "task_complete", "line_number": 92},
      "provenance": [{"kind": "sub_agent_activity"}, {"kind": "thread_spawn"}, {"kind": "task_started"}, {"kind": "task_complete"}],
      "usage_schema": "codex-rollout-token-count-v1"
    }
  ],
  "exclusions": [
    {
      "session_id": "ses_unrelated",
      "file_path": "2026/08/06/unrelated.jsonl",
      "decision": "excluded",
      "rationale": "No recorded spawn and task-lifecycle path from ses_root."
    }
  ]
}
```

Record every included and excluded session, including: session ID and the
portable path relative to the transient Codex session-store root; WGO role/task
name; parent/root relationship; inclusion/exclusion
decision and rationale; spawn/lifecycle evidence; exact child-specific
`session_meta` line; descendant lifecycle start and terminal boundaries; exact
cutoff; SHA-256 of the exact cutoff byte prefix; and the inspected usage schema. The
schema makes the result reproducible when Codex JSONL schemas differ. Also
record every observed phase marker and line. Give each descendant its fixed
phase from the recorded parent spawn/task lifecycle; use `from-markers` only
for a session whose own markers are scanned. For operationalized coverage, add
`operationalization` to `phase_policy.included` and explicitly exclude every
earlier cost coordinator/worker session. Do not treat an uninspected field name
as a known schema.

For an operationalization refresh, use the immutable audit-only manifest as the
frozen audit baseline. Record its audit-root-relative path and SHA-256 in
`prior_manifest`, verify
that file and every original cutoff prefix, then add only the current
operationalization root/session and its recorded descendants. If
operationalization continues in the audit root session, extend that session's
cutoff only in the new manifest and use phase exclusion for the earlier cost
requests. If it runs in a later Codex session, keep the audit root and add the
current session as `operationalization_root_session_id`; the explicit
`wgo:operationalize` invocation against that resolved audit root plus its phase
and completion markers establish the follow-on relationship. Never use date,
CWD, folder, or model alone, and never rediscover or change the audit-only
membership during the refresh.

## 2. Calculate Request-Level Usage

For accessible Codex rollout JSONL, take model and active turn ID from the most
recent `turn_context` record, then take a request-level usage record only from
an `event_msg` whose payload type is `token_count`, at
`payload.info.last_token_usage`. Never add `payload.info.total_token_usage`:
it is cumulative and forked agents can inherit parent context.

Use root `event_msg` `sub_agent_activity` records (`event_id`,
`agent_thread_id`, `agent_path`, `kind: started`) together with the child
`session_meta.payload.source.subagent.thread_spawn` and child `event_msg`
`task_started` plus correlated terminal records to establish provenance. The
current lifecycle key is `turn_id`; accept `task_id` only as a legacy adapter
when the inspected records contain it. If a raw
token-count record carries a stable request/event ID, deduplicate it globally
and retain duplicate locations. If legacy `token_count` has no stable ID,
treat `last_token_usage` as request state: within the same session, turn,
model, tier, and context band, count a changed state once and classify
consecutive identical states as unchanged echoes of the first line. Give each
counted state the deterministic identity
`legacy-state:<session-id>:<active-turn-id>:<first-prefix-line-number>`.
Disclose that this is a schema-aware fallback, not a provider request ID; it
cannot distinguish two genuinely separate legacy requests with identical
usage state. A missing active turn ID is a schema ambiguity. If the same stable
ID has non-identical usage or model fields, flag those exact records as
disputed rather than choosing one.

For a session marked `from-markers`, scan assistant `response_item` text in
line order and change its active phase when an exact `phase_policy.markers`
value appears. A marker applies only to later request events. For a descendant,
use its manifest `phase` derived from the parent spawn/task lifecycle. Include
only `phase_policy.included`; record every request in an excluded phase with
its session, line, request ID, phase, and rationale. Never include
`cost-estimation` in the priced audit total. Retain `unattributed` for legacy
or pre-marker requests instead of guessing from a timestamp or command name.

For each accepted request, total separately:

- uncached input = `input_tokens - cached_input_tokens`;
- cached input;
- output; and
- reasoning, as informational output subcomponent.

Reject any negative input, cached input, output, reasoning, or cache-write
field; also reject cached input greater than total input. Reasoning tokens are
already part of output for this estimate. Show them, but never add them again
to billable output.

Use the checked-in dated rate card
`references/data/api-rate-card-2026-08-07.json`. It records the official
OpenAI API basis in USD per one million tokens, service tier, and context band.
Use an actual returned tier (`default` normalizes to `standard`; `priority`
normalizes to `fast`) when present. Codex rollout JSONL often has no returned
tier, so then use the frozen manifest/rate-card declared `standard` tier. Label
that as an API-equivalent declared basis, not the actual backend tier.

Use an actual returned context band when present. Otherwise derive `long` only
when that request's recorded `input_tokens` is greater than the rate card's
official 272,000-token threshold; use `short` at or below it. An unknown model
or rate is `unpriced`, never zero. The required formula excludes cache-write
charges: when raw usage reports nonzero cache-write tokens, list their exact
session/event/token count as a limitation rather than silently charging or
ignoring them. Do not infer regional uplift, tool charges, or other surcharges.

For a priced request, calculate only:

```text
uncached input × input rate + cached input × cached-input rate + output × output rate
```

## Portable One-Off Recipe

Run this inline Python standard-library recipe once per verification pass from any
machine where the frozen manifest, its referenced JSONL files, and the rate
card are accessible. It writes JSON to stdout and creates no helper file. The
manifest must first record the inspected Codex rollout `token_count` schema.

```sh
python3 - /absolute/path/to/cost-manifest.json /absolute/path/to/api-rate-card-2026-08-07.json /absolute/codex/session-store/root <<'PY'
import hashlib, json, sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

manifest_path = Path(sys.argv[1]).resolve()
manifest = json.loads(manifest_path.read_text(), parse_float=Decimal)
rates = json.loads(Path(sys.argv[2]).read_text(), parse_float=Decimal)
source_root = Path(sys.argv[3]).resolve()
issues, limitations, seen, legacy_states = [], [], {}, {}
duplicates, excluded_requests = [], []
rows = defaultdict(lambda: {
    "uncached_input_tokens": 0, "cached_input_tokens": 0,
    "output_tokens": 0, "reasoning_tokens": 0, "cost_usd": Decimal("0"),
    "priced": True, "rate_per_million": None, "request_ids": [], "tier_sources": set(),
    "context_band_sources": set()
})
long_threshold = int(rates["context_band_rule"]["long_context_input_tokens_gt"])
declared_tier = manifest["pricing_basis"]["default_service_tier_when_not_returned"]
phase_policy = manifest.get("phase_policy", {})
included_phases = set(phase_policy.get("included", ["unattributed"]))
phase_markers = phase_policy.get("markers", {})

def number(value, label, session_id, line_number):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        issues.append({"kind": "schema", "session_id": session_id,
                       "line_number": line_number, "field": label})
        return None
    parsed = Decimal(str(value))
    if parsed != parsed.to_integral_value() or parsed < 0:
        issues.append({"kind": "schema", "session_id": session_id,
                       "line_number": line_number, "field": label})
        return None
    return int(parsed)

def optional_text(*values):
    return next((value for value in values if isinstance(value, str) and value), None)

def assistant_message_text(record):
    payload = record.get("payload", {})
    if (record.get("type") != "response_item" or not isinstance(payload, dict) or
            payload.get("type") != "message" or payload.get("role") != "assistant"):
        return ""
    content = payload.get("content", [])
    if not isinstance(content, list):
        return ""
    return "\n".join(item.get("text", "") for item in content
                     if isinstance(item, dict) and isinstance(item.get("text"), str))

def decode_record(raw, session_id, line_number):
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        issues.append({"kind": "invalid-json", "session_id": session_id,
                       "line_number": line_number})
        return None

def lifecycle_event(record):
    if not isinstance(record, dict) or record.get("type") != "event_msg":
        return None
    payload = record.get("payload", {})
    return payload.get("type") if isinstance(payload, dict) else None

prior_manifest = manifest.get("prior_manifest")
if isinstance(prior_manifest, dict):
    prior_locator = prior_manifest.get("file_path", "")
    prior_path = Path(prior_locator)
    if prior_path.is_absolute() or ".." in prior_path.parts:
        issues.append({"kind": "nonportable-prior-manifest-path"})
        prior_path = None
    else:
        prior_path = manifest_path.parent / prior_path
    if prior_path is None:
        pass
    elif not prior_path.is_file():
        issues.append({"kind": "missing-prior-manifest", "file_path": prior_locator})
    else:
        prior_digest = hashlib.sha256(prior_path.read_bytes()).hexdigest()
        if prior_digest != prior_manifest.get("sha256"):
            issues.append({"kind": "changed-prior-manifest", "file_path": prior_locator,
                           "expected_sha256": prior_manifest.get("sha256"),
                           "actual_sha256": prior_digest})

for session in manifest["sessions"]:
    if session["decision"] != "included":
        continue
    locator = session["file_path"]
    path = Path(locator)
    if path.is_absolute() or ".." in path.parts:
        issues.append({"kind": "nonportable-file-path", "session_id": session["session_id"]})
        continue
    path = source_root / path
    session_id, cutoff = session["session_id"], session["cutoff"]
    if not path.is_file():
        issues.append({"kind": "missing-file", "session_id": session_id, "file_path": locator})
        continue
    byte_lines = path.read_bytes().splitlines(keepends=True)
    end_line = cutoff.get("line_number")
    if not isinstance(end_line, int) or end_line < 1 or end_line > len(byte_lines):
        issues.append({"kind": "invalid-cutoff", "session_id": session_id})
        continue
    prefix = b"".join(byte_lines[:end_line])
    digest = hashlib.sha256(prefix).hexdigest()
    if digest != session["prefix_sha256"]:
        issues.append({"kind": "changed-prefix", "session_id": session_id,
                       "expected_sha256": session["prefix_sha256"], "actual_sha256": digest})
        continue
    marker = cutoff.get("marker")
    if marker and marker not in byte_lines[end_line - 1].decode("utf-8", errors="replace"):
        issues.append({"kind": "cutoff-marker-mismatch", "session_id": session_id,
                       "line_number": end_line, "marker": marker})
        continue

    meta_spec = session.get("session_meta", {})
    meta_line = meta_spec.get("line_number") if isinstance(meta_spec, dict) else None
    if not isinstance(meta_line, int) or meta_line < 1 or meta_line > end_line:
        issues.append({"kind": "invalid-session-meta-boundary", "session_id": session_id})
        continue
    meta_record = decode_record(byte_lines[meta_line - 1], session_id, meta_line)
    meta_payload = meta_record.get("payload", {}) if isinstance(meta_record, dict) else {}
    observed_meta_id = meta_payload.get("id") or meta_payload.get("session_id")
    if (not isinstance(meta_record, dict) or meta_record.get("type") != "session_meta" or
            observed_meta_id != session_id or
            meta_spec.get("session_id") != session_id):
        issues.append({"kind": "session-meta-mismatch", "session_id": session_id,
                       "line_number": meta_line, "observed_session_id": observed_meta_id})
        continue

    start_line = 1
    if session.get("root_relationship") == "descendant":
        lifecycle = session.get("lifecycle", {})
        start = lifecycle.get("start", {}) if isinstance(lifecycle, dict) else {}
        terminal = lifecycle.get("terminal", {}) if isinstance(lifecycle, dict) else {}
        start_line, terminal_line = start.get("line_number"), terminal.get("line_number")
        if (not isinstance(start_line, int) or not isinstance(terminal_line, int) or
                start_line < 1 or start_line > terminal_line or terminal_line != end_line):
            issues.append({"kind": "invalid-lifecycle-interval", "session_id": session_id})
            continue
        start_record = decode_record(byte_lines[start_line - 1], session_id, start_line)
        terminal_record = decode_record(byte_lines[terminal_line - 1], session_id, terminal_line)
        start_event, terminal_event = lifecycle_event(start_record), lifecycle_event(terminal_record)
        allowed_terminal_events = {"task_complete", "task_failed", "task_cancelled",
                                   "task_interrupted", "turn_aborted"}
        terminal_outcomes = {"task_complete": "completed", "task_failed": "failed",
                             "task_cancelled": "cancelled", "task_interrupted": "interrupted",
                             "turn_aborted": "interrupted"}
        if start_event != "task_started" or start.get("event") != start_event:
            issues.append({"kind": "lifecycle-start-mismatch", "session_id": session_id,
                           "line_number": start_line, "observed_event": start_event})
            continue
        if (terminal_event not in allowed_terminal_events or
                terminal.get("event") != terminal_event or
                terminal.get("outcome") != terminal_outcomes.get(terminal_event)):
            issues.append({"kind": "lifecycle-terminal-mismatch", "session_id": session_id,
                           "line_number": terminal_line, "observed_event": terminal_event})
            continue
        correlation_field = "turn_id" if lifecycle.get("turn_id") else "task_id"
        correlation_id = lifecycle.get(correlation_field)
        start_payload = start_record.get("payload", {})
        terminal_payload = terminal_record.get("payload", {})
        if (not isinstance(correlation_id, str) or not correlation_id or
                start_payload.get(correlation_field) != correlation_id or
                terminal_payload.get(correlation_field) != correlation_id):
            issues.append({"kind": "lifecycle-correlation-mismatch", "session_id": session_id,
                           "field": correlation_field, "correlation_id": correlation_id})
            continue
        task_events = []
        for candidate_line in range(start_line, terminal_line + 1):
            try:
                candidate = json.loads(byte_lines[candidate_line - 1].decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            candidate_payload = candidate.get("payload", {})
            candidate_event = lifecycle_event(candidate)
            if (isinstance(candidate_payload, dict) and
                    candidate_payload.get(correlation_field) == correlation_id and
                    candidate_event in allowed_terminal_events | {"task_started"}):
                task_events.append({"event": candidate_event, "line_number": candidate_line})
        if task_events != [{"event": "task_started", "line_number": start_line},
                           {"event": terminal_event, "line_number": terminal_line}]:
            issues.append({"kind": "lifecycle-event-count", "session_id": session_id,
                           "field": correlation_field, "correlation_id": correlation_id,
                           "events": task_events})
            continue

    active_turn = {}
    active_phase = session.get("phase", "unattributed")
    if active_phase == "from-markers":
        active_phase = "unattributed"
    for line_number in range(start_line, end_line + 1):
        record = decode_record(byte_lines[line_number - 1], session_id, line_number)
        if record is None:
            continue
        payload = record.get("payload", {})
        message_text = assistant_message_text(record)
        if message_text:
            for phase_marker, marker_phase in phase_markers.items():
                if phase_marker in message_text:
                    active_phase = marker_phase
            continue
        if record.get("type") == "turn_context" and isinstance(payload, dict):
            active_turn = {
                "turn_id": payload.get("turn_id"), "model": payload.get("model"),
                "service_tier": payload.get("service_tier"),
                "context_band": payload.get("context_band")
            }
            continue
        if record.get("type") != "event_msg" or not isinstance(payload, dict) or payload.get("type") != "token_count":
            continue
        info = payload.get("info", {})
        usage = info.get("last_token_usage", {}) if isinstance(info, dict) else {}
        if not isinstance(usage, dict):
            issues.append({"kind": "schema", "session_id": session_id, "line_number": line_number,
                           "field": "payload.info.last_token_usage"})
            continue
        inp = number(usage.get("input_tokens"), "input_tokens", session_id, line_number)
        cached = number(usage.get("cached_input_tokens"), "cached_input_tokens", session_id, line_number)
        output = number(usage.get("output_tokens"), "output_tokens", session_id, line_number)
        reasoning = number(usage.get("reasoning_output_tokens", 0), "reasoning_output_tokens", session_id, line_number)
        cache_write = number(usage.get("cache_write_input_tokens", 0), "cache_write_input_tokens", session_id, line_number)
        turn_id, model = active_turn.get("turn_id"), active_turn.get("model")
        if None in (inp, cached, output, reasoning, cache_write) or cached > inp or not isinstance(turn_id, str) or not turn_id or not isinstance(model, str) or not model:
            issues.append({"kind": "incomplete-usage", "session_id": session_id, "line_number": line_number})
            continue
        raw_id = optional_text(usage.get("request_id"), info.get("request_id"),
                               payload.get("request_id"), usage.get("event_id"),
                               info.get("event_id"), payload.get("event_id"))
        tier = optional_text(usage.get("service_tier"), info.get("service_tier"), active_turn.get("service_tier"))
        tier_source = "returned" if tier else "declared-api-equivalent"
        tier = {"default": "standard", "priority": "fast"}.get(tier, tier or declared_tier)
        band = optional_text(usage.get("context_band"), info.get("context_band"), active_turn.get("context_band"))
        band_source = "returned" if band else "derived-input-threshold"
        band = band or ("long" if inp > long_threshold else "short")
        fingerprint = (model, inp, cached, output, reasoning, cache_write, tier, band)
        if raw_id:
            request_id = raw_id
            legacy_states.pop((session_id, turn_id, model, tier, band), None)
        else:
            legacy_key = (session_id, turn_id, model, tier, band)
            previous_state = legacy_states.get(legacy_key)
            if previous_state and previous_state["fingerprint"] == fingerprint:
                request_id = previous_state["request_id"]
                duplicates.append({"kind": "unchanged-legacy-state", "request_id": request_id,
                                   "first": previous_state["location"],
                                   "duplicate": {"session_id": session_id,
                                                 "line_number": line_number}})
                continue
            request_id = f"legacy-state:{session_id}:{turn_id}:{line_number}"
            legacy_states[legacy_key] = {
                "fingerprint": fingerprint,
                "request_id": request_id,
                "location": {"session_id": session_id, "line_number": line_number}
            }
        if request_id in seen:
            duplicates.append({"kind": "stable-id", "request_id": request_id,
                               "first": seen[request_id]["location"],
                               "duplicate": {"session_id": session_id, "line_number": line_number}})
            if seen[request_id]["fingerprint"] != fingerprint:
                issues.append({"kind": "disputed-request", "request_id": request_id,
                               "first": seen[request_id]["location"],
                               "second": {"session_id": session_id, "line_number": line_number}})
            continue
        seen[request_id] = {"fingerprint": fingerprint,
                            "location": {"session_id": session_id, "line_number": line_number}}
        if active_phase not in included_phases:
            excluded_requests.append({"request_id": request_id, "session_id": session_id,
                                      "line_number": line_number, "phase": active_phase,
                                      "rationale": "Phase excluded by frozen manifest."})
            continue
        if not raw_id:
            limitations.append({"kind": "legacy-state-identity", "request_id": request_id,
                                "session_id": session_id, "line_number": line_number,
                                "turn_id": turn_id})
        if cache_write:
            limitations.append({"kind": "cache-write-input-excluded-by-formula", "request_id": request_id,
                                "session_id": session_id, "line_number": line_number,
                                "cache_write_input_tokens": cache_write})
        bucket = rows[(active_phase, session_id, model, tier, band)]
        bucket["uncached_input_tokens"] += inp - cached
        bucket["cached_input_tokens"] += cached
        bucket["output_tokens"] += output
        bucket["reasoning_tokens"] += reasoning
        bucket["request_ids"].append(request_id)
        bucket["tier_sources"].add(tier_source)
        bucket["context_band_sources"].add(band_source)
        try:
            rate = rates["models"][model][tier][band]
        except KeyError:
            bucket["priced"] = False
            issues.append({"kind": "unpriced", "request_id": request_id, "model": model,
                           "service_tier": tier, "context_band": band})
            continue
        bucket["rate_per_million"] = {name: str(value) for name, value in rate.items()}
        bucket["cost_usd"] += (Decimal(inp - cached) * rate["input"] +
                               Decimal(cached) * rate["cached_input"] +
                               Decimal(output) * rate["output"]) / Decimal(1000000)

flat_rows = []
for (phase, session_id, model, tier, band), row in sorted(rows.items()):
    row.update({"phase": phase, "session_id": session_id, "model": model, "service_tier": tier,
                "context_band": band, "tier_sources": sorted(row["tier_sources"]),
                "context_band_sources": sorted(row["context_band_sources"])})
    row["cost_usd"] = str(row["cost_usd"]) if row["priced"] else None
    flat_rows.append(row)
total = None if issues else str(sum(Decimal(row["cost_usd"]) for row in flat_rows))
print(json.dumps({"rows": flat_rows, "excluded_requests": excluded_requests,
                  "duplicates": duplicates, "issues": issues,
                  "limitations": limitations, "total_cost_usd": total}, indent=2, default=str))
PY
```

The coordinator supplies the same immutable manifest and rate-card path to each
pass. For audit-only coverage, preserve the raw results as
`cost-terra-pass-a.json` and `cost-terra-pass-b.json`. For operationalized
coverage, use `cost-terra-operationalized-pass-a.json` and
`cost-terra-operationalized-pass-b.json`. Keep them beside their manifest; they
are temporary verification data, not audit artifacts. After comparison, retain
them only in `tmp_debug` for troubleshooting; never copy them into the audit.

## 3. Independent Terra Verification

Launch exactly two independent `gpt-5.6-terra` workers at high reasoning after
the manifest is frozen. They
receive the same frozen manifest, referenced read-only JSONL files, rate-card
path, and the following prompt verbatim:

```text
You are a cost-calculation worker. Use only the frozen manifest supplied by the Terra coordinator. Parse only each manifest lifecycle interval and its exact matching session metadata. At request/event level, de-duplicate stable request IDs and suppress consecutive unchanged legacy last_token_usage echoes. Return a machine-checkable table of tokens by session and model. Do not infer missing records, include sessions or lines outside the manifest boundaries, or sum cumulative session totals. Flag any schema ambiguity or missing pricing input rather than guessing.
```

Each worker returns the JSON table from the one-off recipe (or an equivalent
standard-library parser) with request IDs, duplicate locations, totals by
session/model/tier/context band, and flags. They do not discover more sessions,
change the manifest, decide eligibility, or price an absent rate.

Before launching them, resolve and verify a neutral system temporary directory
that exists on the current platform, then use it as each worker's initial
working directory while passing the manifest, session-store root, and rate card
as explicit transient absolute inputs. This prevents a deleted, moved, cloud-
synced, or inherited project CWD from blocking process creation. A launch that
fails before calculation because its CWD is unavailable may be retried from the
verified temporary directory without changing the frozen manifest. Wait for a
worker that is still making progress; do not interrupt it merely because the
calculation is slower than expected. A terminal worker failure is recorded
loudly and leaves the estimate `Unreconciled`.

Terra compares both tables exactly after normalizing table order. Investigate
every mismatch by naming the session ID, request/event ID, JSONL line, field,
and worker values. Do not calculate a final total while any mismatch remains.

## 4. Write The Cost Control

Read `../templates/cost-estimate-template.md` immediately before writing
`<audit-root>/controls/cost-estimate.md` and
`<audit-root>/controls/cost-calculation.json`; follow it exactly.

Identify the pricing basis, source URL, rate-card date, currency, recorded
service tiers/context bands, coverage (`audit` or
`audit-and-operationalization`), and the exact formula. List the full manifest,
phase boundaries, excluded phases/requests, and session exclusions with their
rationales. Replace every provider session, turn, task, request, message, event,
and source-filename identifier with deterministic audit-local aliases such as
`session-001`; never copy a provider identifier into either public cost
artifact. Write exact aliased rows, totals, rate-card identity, temporary input
digest, pass count, normalized-match result, and pass-result digests to
`cost-calculation.json`. Link that receipt from `cost-estimate.md`. For refreshed
coverage, preserve the earlier public receipt and state that the readable
estimate supersedes only its earlier version.
The token table must show phase, uncached input, cached input, output, and
informational reasoning by session, model, service tier, and context band, plus
phase subtotals.
The cost table must show model, service tier/context band, rate, cost,
`unpriced` status where relevant, and a total only when every included priced
request reconciles. Identify each declared service tier and input-threshold
context band as API-equivalent rather than observed backend billing. List any
nonzero cache-write tokens as excluded-by-formula limitations.

Keep exact decimal costs in the public alias-only receipt. In
`cost-estimate.md`, display every priced rate, row, subtotal, and total as
`$X.XX`, rounded half up from its exact value. Round the exact total directly;
never sum already-rounded display rows. Use `unpriced`, not `$0.00`, for a
missing rate. When a positive exact cost rounds to `$0.00`, state the exact
value so the display is not mistaken for a zero calculation.

Set the control's status to one of:

- `Final` — manifest, phase attribution/exclusions, duplicate handling, two
  Terra tables, pricing inputs, and totals reconcile; or
- `Unreconciled` — list each disputed/missing session or event and do not state
  a falsely precise total.

Always state that the result is an API-equivalent estimate, not a Codex invoice,
and that its own calculation requests are excluded. Its limitations include
unavailable or changed session files, missing phase markers, unattributed
requests, JSONL schema ambiguity, unknown model/tier/context/rate, unpriced
non-token charges, and any provider billing or subscription differences.

See `references/fixtures/cost-estimation/README.md` for the dry-run fixture.
