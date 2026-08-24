# DISSONANCE-005: Upstream Divergence vs Fork-Only Phase Mirror Invariant

- **ID:** 005
- **Status:** accepted-risk
- **Created:** 2026-08-24
- **Updated:** 2026-08-24
- **Closed:** 2026-08-24
- **Owner:** PhaseMirror Maintainer
- **Surface:** `https://github.com/kortix-ai/suna`, `https://github.com/PhaseMirror/suna`

## Claim
"Phase Mirror is the first-class governance and claim validation system for the company repository."

## Mirror
Phase Mirror governs the canonical Kortix company codebase.

## Dissonance
The Phase Mirror skill, dissonance memory register, verification suites, and qualified Elastic License 2.0 copy exist within the `PhaseMirror/suna` repository. Upstream `kortix-ai/suna` maintains raw unhedged "open source" claims, lacks the Phase Mirror pre-CR gate, and does not enforce memory schema validation or air-gapped test verification. External users encountering `kortix-ai/suna` operate without these governance mechanisms until upstream adopts the change request.

## Phase
- **Action:** Maintain `PhaseMirror/suna` as the authoritative reference implementation of the Phase Mirror governance model. Prepare and track an upstream Change Request against `kortix-ai/suna` to upstream the skill, memory register, validation scripts, and license qualifications. Accept the fork divergence as an operational invariant until upstream merges.
- **Owner:** PhaseMirror Maintainer
- **Metric:** Upstream CR drafted with tracking link; permanent fork divergence explicitly documented and justified as an accepted risk.
- **Target Date:** 2026-09-07

## Resolution Log
- 2026-08-24: Entry opened and classified as `accepted-risk`. Upstream repository `kortix-ai/suna` operates independently. PhaseMirror fork serves as the authoritative canonical testbed and reference standard for all Phase Mirror invariants.
