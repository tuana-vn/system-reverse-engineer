# Stage 04 — Independent Technical Design Verification

## Inputs

- requirement: `{{requirement_path}}`
- current-state analysis: `{{artifact_root}}/analysis/{{scope_slug}}_current_state.md`
- gap analysis: `{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap.md`
- TDD: `{{artifact_root}}/proposals/{{scope_slug}}_tdd.md`
- current repository

Run:

```text
/technical-design-verification
```

Do NOT revise the TDD in this verification pass.

Mandatory checks:
- exact `PROPOSED Static Architecture` section exists
- static structure is source/design consistent
- all major proposed/modified components appear in the diagram
- Component Responsibilities matches the diagram
- Runtime Sequences match the static design
- exact change set uses the same component names/locations
- requirement/gap traceability is complete
- provenance/exposure/compatibility gates are satisfied where applicable
- execute/evaluate each material TDD decision rule against every authoritative MUST LOG / MUST NOT LOG row; 100% must produce the required outcome
- do not accept textual traceability as proof that boolean/branching decision logic is semantically correct
- reject any TDD obligation/field that originated downstream of the requirement unless it is explicitly labeled PROPOSED and justified

Write:

`{{artifact_root}}/verification/{{scope_slug}}_tdd_verification.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: requirement-to-design
  step: technical_design_verification
  status: TDD_VERIFIED | TDD_PARTIALLY_VERIFIED | TDD_CONTRADICTED | TDD_BLOCKED_SOURCE_GAPS | TDD_INCOMPLETE_ARCHITECTURE | TDD_INCOMPLETE_PROPOSED_UNIT_OWNERSHIP
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/verification/{{scope_slug}}_tdd_verification.md"
  next_recommended: contract_test_design | revise_technical_design | resolve_design_unknowns
```

## 4.0 Proposed Unit Ownership Check

Enumerate all implementation-significant PROPOSED units in the TDD and verify 100% explicit design
ownership. A unit may become a dedicated artifact or an explicitly-owned subordinate unit.

Do not treat JavaDoc mentions, `@see`, method signatures, imports, dependencies, or nearby prose as
ownership.

If any unit has no explicit owner, do not return `TDD_VERIFIED`; return:

`TDD_INCOMPLETE_PROPOSED_UNIT_OWNERSHIP`
