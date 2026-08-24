# DISSONANCE-002: Compounding Memory Claim vs Plain File Mechanism

- **ID:** 002
- **Status:** resolved
- **Created:** 2026-08-24
- **Updated:** 2026-08-24
- **Closed:** 2026-08-24
- **Owner:** Memory Owner
- **Surface:** `MANIFESTO.md`, `.kortix/opencode/skills/kortix-memory/SKILL.md`, `.kortix/memory/MEMORY.md`

## Claim
"Agents compound shared company memory across sessions, preventing rediscovery loops and accumulating durable context."

## Mirror
Agents maintain durable compounding memory across sessions.

## Dissonance
Project memory is implemented as flat, unindexed markdown files in `.kortix/memory/`. Memory files lack automated schema validation, semantic search, or retrieval quality evaluation. Agents must manually discover and load memory files via the `memory` tool. In practice, long sessions often miss relevant sub-files or fail to record durable knowledge before context resets.

## Phase
- **Action:** Implement automated schema validation and linting for `.kortix/memory/` files in CI, and introduce a retrieval hit rate metric for session reflection.
- **Owner:** Memory Owner
- **Metric:** 0 malformed memory files on main; session retrieval hit rate ≥ 80% across 50 benchmark test runs.
- **Target Date:** 2026-09-07

## Resolution Log
- 2026-08-24: Entry opened during Phase Mirror integration pilot.
- 2026-08-24: Resolved. Landed scripts/validate_memory.py implementing schema validation and 50-query retrieval benchmark (100% hit rate, 0 malformed files). Integrated into test suite.
