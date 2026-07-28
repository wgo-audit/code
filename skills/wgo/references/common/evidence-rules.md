# Evidence Rules

Use these rules whenever WGO collects or reports evidence.

Compare direct evidence and artifacts; summaries and handoffs are navigation,
not proof.

1. Register reusable material evidence as `E-###` before relying on it. Record
   source type, precise locator, observed/effective time, cutoff eligibility,
   factual summary, limitation, and sensitivity.
   Use exactly one cutoff label:
   - `within-cutoff`: the evidence was effective or observed no later than the
     audit cutoff;
   - `post-cutoff-validation`: evidence obtained after the cutoff is used only
     to validate a cutoff-bounded claim, with that limit stated;
   - `historical-undated`: the evidence is historical but has no reliable
     effective or observation date; or
   - `unknown`: its timing cannot be established.
2. Keep implementation, live state, observed behavior, ownership, approval,
   readiness, cost, security control, and data correctness distinct. Source code
   does not prove the other dimensions.
3. A material stakeholder statement needs role attribution, date, scope, and
   limitation. It does not prove live state.
4. Bound absence claims to the approved source set and cutoff. Say what was not
   found, not that it never existed.
5. When an in-scope source points to a material source outside the approved
   boundary, say `Documented outside audited scope; not independently
   verified.` Cite the pointer, state what it cannot establish, and recommend
   the smallest scope expansion or verification. Do not turn it into a new
   register or treat it as an absence claim.
6. Never store secret values, session tokens, private keys, credentials, or
   unnecessary PII. Use a redacted locator or classification.

## Source Access

An inaccessible expected source is an audit limitation, not evidence that its
content is absent. Record material access events in
`evidence/source-access-register.md` with attempted method, failure, affected
question, impact, approved fallback or exclusion, owner, and next step. Do not
substitute local Git data for unavailable hosted metadata without stating the
limitation.

Every GitHub code repository URL supplied for the audit, or a GitHub `origin`
in the current repository, automatically authorizes read-only use of that
repository's accessible PRs, issues, Projects, Actions, releases, and history.
Use public data and private data available through the existing GitHub session.
Do not ask for consent or request credentials. Bound inspection to each named
repository and the audit cutoff; record inaccessible GitHub metadata as a limit.

When material sources conflict, state the exact conflict, what each source
establishes, the risk of a wrong assumption, and the closure route in the
reviewer report. Add an open item only if a future owner, authority decision,
or proof is needed. State when no material conflict was found, and preserve
post-cutoff and inaccessible-evidence limits in the reviewer report.
