Inspect one source slice for dependencies and build inputs that affect
application behavior. Use the reviewer's topology packet; do not invoke CodeGraph.

Return a concise evidence packet with exact lockfile, manifest, script,
workflow, generated-code, scanner-output, or hosted-source locators. Separate
observed, inferred, and unknown boundaries. Focus on vulnerable, abandoned,
privileged, generated, or build-time inputs that could create an application
security finding. Do not assess general supply-chain governance or compliance.
Do not write audit artifacts or shared state.
