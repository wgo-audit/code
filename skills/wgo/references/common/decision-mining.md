# Decision Mining

Use only inside detailed Architecture or Product Value work. It is not a lens,
command, queue, approval process, or target-count exercise.

After inspecting approved evidence, create the required candidate inventory
before drafting records. Architecture covers applicable component, runtime/
deployment, release/configuration, identity/secrets, data authority, jobs,
contracts, dependencies, capacity/cost, and business-critical algorithm/pipeline
domains. Product Value covers applicable maturity/demo, users/workflows,
lifecycle, configuration/persistence, outputs/provenance, identity/governance,
specialist sign-off, external dependencies, public promises, and operator/admin
acceptance domains.

Use stable `ARCH-DC-###` or `PROD-DC-###` candidates. For each, record the
decision or durable observed behavior, domain, precise evidence, observed versus
approved status, and one disposition: `record-created`, `merged-into`,
`not-a-decision`, `blocked`, or `deferred`. Give every non-record disposition a
specific reason and closure route. Missing rationale or approval never prevents
recording a source-backed observation as `unknown`.

Create an ADR/PDR for every material `record-created` candidate and list every
created record in its register. The register is an index, not a substitute for
the records. A complex project with few candidates needs a source-bounded
explanation.

On a resume in the same audit root, read the prior inventory and register before
creating records. Retain an existing ADR/PDR ID for the same decision; do not
reuse it for another decision. When a later decision replaces it, mark the prior
record `superseded`, link the replacement, and assign the replacement after the
highest existing ID in that family.

Bounded collectors may inspect non-overlapping source slices and return candidate
evidence; the reviewer deduplicates, registers evidence, and creates all
canonical outputs.
