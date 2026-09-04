---
name: current-state-tdd-synthesis
description: Synthesize verified reverse-engineering evidence and architecture models into a consumer-facing CURRENT_STATE_TDD.md that explains current responsibilities, dependencies, runtime flows, boundaries, state, variants, failure behavior, and evidence without turning the audit report into the baseline.
---

# Current-State TDD Synthesis — 4.0

## Mission

Produce the canonical consumer-facing current-system technical design:

```text
docs/reverse-engineering/CURRENT_STATE_TDD.md
```

This document is the durable input for later Design Agent work.

The readiness audit is a separate artifact. Do not make an audit table the primary baseline document.

## Consumer Test

A backend developer unfamiliar with the repository should be able to understand, within approximately 15–20 minutes:

- system boundary and purpose;
- major component responsibilities;
- dependency direction;
- primary runtime flows;
- external integration boundaries;
- state/persistence ownership;
- lifecycle/concurrency behavior;
- configuration/runtime selection;
- failure/error behavior;
- build/runtime structure;
- material unknowns and evidence anchors.

## Required TDD Sections

Use these headings in this order:

```text
# Current-State Technical Design
## 1. System Context
## 2. Architecture Overview
## 3. Component Responsibilities
## 4. Runtime Entry Points
## 5. Primary Runtime Flows
## 6. Integration Architecture
## 7. Persistence and State Ownership
## 8. Background Processing and Lifecycle
## 9. Configuration and Runtime Selection
## 10. Error, Retry, and Fallback Behavior
## 11. Security Boundaries
## 12. Observability
## 13. Build and Runtime Model
## 14. Critical Current-System Rules
## 15. Runtime Variants and Alternate Paths
## 16. Known Unknowns and External Blockers
## 17. Evidence and Diagram Index
```

If a section is not applicable, write `NOT_APPLICABLE` plus the evidence supporting that classification.

## Diagram Integration

Reference the mandatory diagram artifacts from the relevant TDD sections:

```text
diagrams/01_system_context.md
diagrams/02_component_architecture.md
diagrams/03_primary_runtime_sequence.md
diagrams/04_integration_boundaries.md
diagrams/05_state_persistence_lifecycle.md
```

Do not duplicate five large diagrams in every artifact. The TDD may embed the most important diagram and link the rest by repository-relative path.

## Evidence Precision

Material current-state statements must use evidence precise enough to re-open quickly:

Preferred:

```text
path + symbol/method/config key + optional line/range
```

Minimum for source-backed material claims:

```text
repo-relative path
```

Class name alone is not a sufficient source anchor when a path can be determined.

## Synthesis Rules

Prefer:

```text
relationship > inventory
behavior > file count
responsibility > package list
runtime selection > implementation existence
state ownership > entity dump
consumer usability > audit verbosity
```

Large schema tables, exhaustive class inventories, and exhaustive evidence ledgers belong in supporting model/evidence artifacts. Summarize the important meaning in the TDD.

## Completion Gate

Do not declare synthesis complete until:

```text
[ ] all required sections exist
[ ] all 5 mandatory diagram artifacts exist and are referenced
[ ] all material subsystems are represented in component catalog
[ ] primary runtime flows are represented in runtime flow catalog
[ ] all known external integrations are represented in integration catalog
[ ] behavior-changing configuration selectors are represented in configuration model
[ ] persistence/state ownership is represented or explicitly NOT_APPLICABLE
[ ] material current-state claims use repo-relative evidence paths
[ ] unresolved HIGH/CRITICAL items remain explicit
```
