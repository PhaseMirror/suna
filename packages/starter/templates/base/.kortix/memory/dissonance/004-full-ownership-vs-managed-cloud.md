# DISSONANCE-004: Full Ownership Claim vs Managed Cloud Default Path

- **ID:** 004
- **Status:** open
- **Created:** 2026-08-24
- **Updated:** 2026-08-24
- **Closed:** N/A
- **Owner:** Self-Host Owner
- **Surface:** `MANIFESTO.md`, `README.md`, `.claude/skills/comms/SKILL.md`

## Claim
"A company you own outright — your data, your models, your infrastructure, no vendor lock-in or cage."

## Mirror
Users operate with complete data and infrastructure independence.

## Dissonance
The default setup and convenience path routes inference through third-party LLM providers and executes sandboxes on Kortix Cloud infrastructure. True air-gapped self-hosting requires manual Docker Compose setup, external image pulls from Docker Hub, and external egress. The operational reality heavily incentivizes cloud convenience over sovereign ownership.

## Phase
- **Action:** Build and publish an end-to-end air-gapped self-host verification suite (`kortix self-host test --airgapped`) that tests local inference and sandbox provisioning without external network access.
- **Owner:** Self-Host Owner
- **Metric:** Air-gapped self-host test suite executes locally in CI with zero external egress requests.
- **Target Date:** 2026-09-07

## Resolution Log
- 2026-08-24: Entry opened during Phase Mirror integration pilot.
