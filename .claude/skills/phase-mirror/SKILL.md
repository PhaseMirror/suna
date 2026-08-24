---
name: phase-mirror
description: "Surfaces the gap between stated claims and actual operating incentives or mechanisms, converting the mismatch into a small testable phase with a named owner and metric. Load whenever writing, reviewing, or pressure-testing claims in kortix.yaml, agent prompts, CR descriptions, memory files, PR bodies, or public positioning."
---

# Phase Mirror

Phase Mirror is a structured method that mirrors a stated claim, surfaces the dissonance between that claim and operating incentives or mechanisms, and converts the mismatch into a small, testable phase with a named owner and metric.

## When to use this skill

Load this skill whenever you:
- Draft or review a Change Request (CR) or Pull Request (PR) containing capability, security, performance, licensing, or scaling claims.
- Author or modify agent prompts, `kortix.yaml` manifests, or tool definitions.
- Write or curate project memory files in `.kortix/memory/`.
- Review public or internal copy for "vibe claims" that lack concrete mechanism backing.
- Conduct continuous harness refinement or project reflection.

## Output structure

The output format is fixed:

```markdown
### Phase Mirror

- **Claim:** <Exact stated assertion>
- **Mirror:** <Restatement of the claim without endorsement or dilution>
- **Dissonance:** <The specific tension between the claim and underlying incentives, mechanisms, or evidence>
- **Phase:** <One small, reversible change with a named owner and quantifiable metric>
```

### Components

1. **Mirror**: Restate the claim directly. Do not endorse, soften, or elaborate.
2. **Dissonance**: Name the exact point of tension. Contrast what is asserted with how the system actually operates, what the code enforces, or what incentives govern execution.
3. **Phase**: Formulate a single, bounded, reversible experiment or change. Every phase must specify:
   - **Action**: Concrete step to test or resolve the dissonance.
   - **Owner**: Named role or individual accountable for delivery.
   - **Metric**: Verifiable measurement with a numerical target or binary pass/fail condition.

## Communication standard

Follow the ASD-STE100 precision standard:
- **Short declarative sentences**: Aim for 20 words or fewer per sentence.
- **Facts only**: State verified mechanisms, file paths, status codes, and numbers.
- **No filler or hedging**: Omit "probably", "should work", "seamless", "revolutionary", and marketing superlatives.
- **Active voice and present tense**: "The sandbox allows egress", not "Egress may be permitted".

## Worked examples

### Example 1: Licensing and source distribution

- **Claim:** "Kortix is an open-source AI Management System."
- **Mirror:** Kortix is open source.
- **Dissonance:** The repository is licensed under Elastic License 2.0 (ELv2), which is not an OSI-approved open-source license. The license prohibits offering the software as a managed service to third parties.
- **Phase:** Update documentation and comms guidelines to state "source-available under Elastic License 2.0" and eliminate unqualified "open source" claims.
  - **Owner:** Comms Owner
  - **Metric:** 100% of license mentions in root docs cite ELv2 terms.

### Example 2: Memory compounding

- **Claim:** "Agents compound shared company memory across sessions."
- **Mirror:** Agents maintain durable compounding memory across sessions.
- **Dissonance:** Memory consists of flat markdown files in `.kortix/memory/` without automated schema validation, semantic indexing, or retrieval quality evaluation.
- **Phase:** Add automated schema linting for memory entries and measure session retrieval hit rates.
  - **Owner:** Memory Owner
  - **Metric:** 0 malformed memory files on main; session retrieval hit rate ≥ 80%.

### Example 3: Enterprise security review

- **Claim:** "Built to survive an enterprise security review."
- **Mirror:** The system satisfies enterprise security review requirements.
- **Dissonance:** Default sandboxes run on Daytona containers without kernel-level microVM isolation. Egress blocking is not enabled by default (`allowInternetAccess: true`).
- **Phase:** Add a configuration check requiring Platinum microVM isolation and explicit egress policies for enterprise project profiles.
  - **Owner:** Runtime Owner
  - **Metric:** 100% of enterprise-tier project runs assert Platinum provider and egress policy compliance.

### Example 4: Full ownership vs. cloud convenience

- **Claim:** "Full data and compute ownership with no vendor lock-in."
- **Mirror:** Users retain complete ownership of data and execution.
- **Dissonance:** The default setup path routes inference through third-party managed LLM gateways and defaults to Kortix Cloud sandboxes.
- **Phase:** Implement an automated local self-host verification suite that runs with zero external cloud dependencies.
  - **Owner:** Self-Host Owner
  - **Metric:** `kortix self-host test --airgapped` passes in local CI.

## Memory and governance integration

1. **Pre-CR Gate:** Any session proposing changes with capability or security claims must include a Phase Mirror block in the CR description.
2. **Dissonance Register:** Accepted Phase Mirror findings are stored as individual files under `.kortix/memory/dissonance/`.
3. **Resolution Lifecycle:** A dissonance record moves from `open` to `resolved` only after the testable phase merges and its metric is verified.
4. **Permissions:** Every agent capable of opening a CR may invoke Phase Mirror. Only human reviewers or designated governance roles may mark a dissonance record closed.
