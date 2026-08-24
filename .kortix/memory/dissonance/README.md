# Dissonance Register

The **Dissonance Register** (`.kortix/memory/dissonance/`) is the durable record of tensions surfaced by the Phase Mirror method. It records mismatches between stated claims (capabilities, licensing, architecture, security, scaling) and actual mechanisms or operating incentives.

## Register Schema

Every dissonance entry is a markdown file named `<id>-<slug>.md` (e.g., `001-open-source-vs-elv2.md`).

### Required Fields

```markdown
# DISSONANCE-<ID>: <Short Title>

- **ID:** <ID, e.g. 001>
- **Status:** open | in-progress | resolved | accepted-risk
- **Created:** YYYY-MM-DD
- **Updated:** YYYY-MM-DD
- **Closed:** YYYY-MM-DD (or N/A)
- **Owner:** <Role or Name>
- **Surface:** <File path, config key, PR, or doc URL where the claim originates>

## Claim
<The exact stated claim without modification>

## Mirror
<Direct restatement of the claim without endorsement or dilution>

## Dissonance
<The specific tension between the claim and underlying incentives, mechanisms, or evidence>

## Phase
- **Action:** <Single, bounded, reversible change or test>
- **Owner:** <Named role or individual>
- **Metric:** <Quantifiable target or binary pass/fail condition>
- **Target Date:** <Target completion date>

## Resolution Log
- YYYY-MM-DD: <Notes, PR links, test output, or rationale for status transition>
```

## Lifecycle States

1. **`open`**: Dissonance surfaced and accepted into the register. Phase is planned but not completed.
2. **`in-progress`**: Phase implementation or experiment is actively underway on a dedicated branch.
3. **`resolved`**: Phase merged, metric verified with empirical evidence, and claim reconciled with reality.
4. **`accepted-risk`**: Tension acknowledged by designated governance authority as an intentional operational tradeoff with documented justification.

## Governance & Permissions

- **Authoring / Opening:** Every agent or developer capable of opening a Change Request may author and propose a dissonance record.
- **Closing / Transitioning to Resolved:** Only designated review roles or human operators may mark a record `resolved` or `accepted-risk` via an approved Change Request.
- **Deduplication:** Before opening a new dissonance entry or proposing a claim in a CR, agents must inspect this directory to avoid re-litigating known tensions.
