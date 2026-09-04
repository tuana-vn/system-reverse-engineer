# Stage 03 — Source-Backed Technical Design

## Inputs

- requirement: `{{requirement_path}}`
- current-state analysis: `{{artifact_root}}/analysis/{{scope_slug}}_current_state.md`
- verified gap analysis: `{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap.md`
- current repository
- scope: `{{scope}}`

## Preconditions

Do not run if Stage 02 returned `DESIGN_NOT_READY_SOURCE_GAPS`.

Run:

```text
/technical-design-proposal
```

## Goal

Produce a reviewer-grade technical design that closes VERIFIED gaps only.

This is not merely a gap-remediation table.
The output must describe the proposed software structure and runtime behavior.

## Mandatory TDD Sections

The output MUST contain these headings in this order:

```text
## Design Decision Summary
## Requirement / Scope Matrix
## CURRENT Static Architecture
## PROPOSED Static Architecture
## Component Responsibilities
## Class / Interface / Contract Design
## PROPOSED Dynamic Architecture / Runtime Sequences
## Field / Data / Context Provenance
## Boundary / Integration Design
## Gap → Solution Traceability
## Compatibility / Non-Goal Preservation
## Exact Proposed Change Set
## Design Traceability
## Risks / Open Questions
## TDD Readiness
```

### HARD architecture rule

`## PROPOSED Static Architecture` MUST NOT be omitted.

If the change introduces or materially modifies software structure/responsibilities,
include a Mermaid static class/component diagram.

If no structural change is required, keep the section and explicitly document the unchanged
resulting static architecture and modified responsibility location.

Sequence diagrams are mandatory for materially changed runtime flows, but they do not replace
the static architecture diagram.

## Rules

- current repository = truth for existing structure
- requirement = intended behavior
- proposed components must be labeled PROPOSED
- do not redesign already-compliant behavior
- target proven break points
- preserve explicit non-goals
- do not invent common wrappers/seams
- verify field/data provenance before fixing data/output behavior
- close Boundary → Exposure for affected integration boundaries
- unresolved evidence remains a blocker

## Architecture Consistency Requirement

Before declaring ready, verify the same proposed components/names appear consistently in:

```text
PROPOSED Static Architecture
↔ Component Responsibilities
↔ Class / Interface / Contract Design
↔ Runtime Sequences
↔ Exact Proposed Change Set
```

If these disagree, do not issue `TDD_READY`.

## Output

Write:

`{{artifact_root}}/proposals/{{scope_slug}}_tdd.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: requirement-to-design
  step: technical_design
  status: TDD_READY | TDD_READY_WITH_EXTERNAL_BLOCKERS | TDD_NOT_READY_SOURCE_GAPS | TDD_INCOMPLETE_ARCHITECTURE
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  quality:
    current_static_architecture: COMPLETE | JUSTIFIED_NA | INCOMPLETE
    proposed_static_architecture: COMPLETE | INCOMPLETE
    component_responsibilities: COMPLETE | INCOMPLETE
    runtime_sequences: COMPLETE | JUSTIFIED_NA | INCOMPLETE
    diagram_prose_consistency: VERIFIED | NOT_VERIFIED
  artifact: "{{artifact_root}}/proposals/{{scope_slug}}_tdd.md"
  next_recommended: technical_design_verification | resolve_design_unknowns
```
