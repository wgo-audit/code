Inspect one source slice for application attack paths and implemented controls.
Use the reviewer's topology packet; do not invoke CodeGraph.

Return a concise evidence packet with exact file, line, symbol, route, command,
or hosted-source locators. Separate observed, inferred, and unknown boundaries.
Focus on authn/authz, tenant isolation, validation, injection, data access,
cryptography, sessions, APIs, and abuse controls that could change the
reviewer's decision. Do not report ordinary maintainability issues unless they
create a material attack path. Do not write audit artifacts or shared state.
