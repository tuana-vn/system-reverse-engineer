# Stage 02 — Design Artifact Decomposition

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`
Execution mode: `{{execution_mode}}`

Inputs:
- requirement: `{{requirement_path}}`
- verified gap analysis: `{{gap_artifact}}`
- verified TDD: `{{tdd_path}}`
- TDD verification: `{{tdd_verification_artifact}}`
- current repository

Run `/design-artifact-decomposition`.

Do not generate WBS yet.
Do not write detailed design yet.

Write:
`{{design_registry_artifact}}`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: design_artifact_decomposition
  status: ARTIFACT_REGISTRY_READY | ARTIFACT_REGISTRY_PARTIAL | ARTIFACT_REGISTRY_BLOCKED | ARTIFACT_DECOMPOSITION_INCOMPLETE
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{design_registry_artifact}}"
  next_recommended: artifact_detailed_design | resolve_registry_unknowns
```

## 4.0 Ownership Closure

Before `ARTIFACT_REGISTRY_READY`, create a 100% ownership map for all implementation-significant
PROPOSED units from the verified TDD:

```text
PROPOSED unit
→ DEDICATED_ARTIFACT
   OR
→ SUBORDINATE_TO:<ART-ID> with explicit responsibility ownership
```

If any unit is unowned or only implicitly owned, emit:

`ARTIFACT_DECOMPOSITION_INCOMPLETE`

and stop. Do not let DD or WBS generation compensate for missing artifact ownership.

## 4.0 Gate Routing Contract

If `ARTIFACT_DECOMPOSITION_INCOMPLETE` is emitted, do not continue to DD generation and do not
silently invent ownership. Return the finding upstream for TDD/design ownership revision.