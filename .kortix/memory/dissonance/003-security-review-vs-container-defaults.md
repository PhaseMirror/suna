# DISSONANCE-003: Security Review Survival Claim vs Default Container Isolation

- **ID:** 003
- **Status:** open
- **Created:** 2026-08-24
- **Updated:** 2026-08-24
- **Closed:** N/A
- **Owner:** Runtime Owner
- **Surface:** `.claude/skills/comms/SKILL.md`, `README.md`, `kortix.yaml`

## Claim
"Built to survive an enterprise security review, not slip past one."

## Mirror
The platform satisfies enterprise security review requirements by default.

## Dissonance
The default sandbox provider runs on Daytona Linux containers rather than kernel-isolated microVMs. MicroVM isolation is supported only on the Platinum provider. Furthermore, outbound network egress blocking is disabled by default (`allowInternetAccess: true`), and approval gates are off by default (`policy.default_mode` is `allow_all`). A cold enterprise security audit evaluating default deployments encounters standard containers with unconstrained outbound network access.

## Phase
- **Action:** Add a strict enterprise profile check in `kortix.yaml` that enforces Platinum microVM isolation and explicit egress allow-lists for enterprise deployments.
- **Owner:** Runtime Owner
- **Metric:** 100% of enterprise-tier project configurations enforce Platinum microVM isolation and egress policy gates before session boot.
- **Target Date:** 2026-09-07

## Resolution Log
- 2026-08-24: Entry opened during Phase Mirror integration pilot.
