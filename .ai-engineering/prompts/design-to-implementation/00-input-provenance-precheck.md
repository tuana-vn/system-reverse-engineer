# Stage 00 — Required Input Existence and Provenance Precheck

## Inputs

- requirement: `{{requirement_path}}`
- current-state artifact: `{{current_state_artifact}}`
- gap artifact: `{{gap_artifact}}`
- TDD: `{{tdd_path}}`

## Goal

Block the workflow before semantic verification if a required upstream artifact is absent or if the
TDD/gap provenance references do not match the supplied upstream artifacts.

## Mandatory checks

First execute the repository structural check:

```text
python .ai-engineering/tools/validate-required-inputs.py requirement_path={{requirement_path}} current_state_artifact={{current_state_artifact}} gap_artifact={{gap_artifact}} tdd_path={{tdd_path}}
```

A non-zero result is a hard STOP. Do not continue to semantic provenance checks.

1. Verify all four input paths exist as files in the current repository. A textual reference to a path
   is not proof of existence.
2. Verify the gap artifact names/references the supplied current-state artifact, or explicitly records
   equivalent provenance.
3. Verify the TDD names/references the supplied requirement, current-state artifact, and gap artifact,
   or explicitly records equivalent provenance.
4. If an artifact was generated against a different source commit/baseline and that difference can
   materially affect the design, return provenance mismatch rather than guessing compatibility.
5. Do not create, reconstruct, or infer a missing upstream artifact in this stage.

## Status rules

- any required input file missing => `REQUIRED_INPUT_ARTIFACT_MISSING`
- files exist but declared upstream provenance is inconsistent => `UPSTREAM_PROVENANCE_MISMATCH`
- all checks pass => `INPUT_PROVENANCE_VERIFIED`

Write the result to:

`{{artifact_root}}/verification/input_provenance_precheck.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: input_provenance_precheck
  status: INPUT_PROVENANCE_VERIFIED | REQUIRED_INPUT_ARTIFACT_MISSING | UPSTREAM_PROVENANCE_MISMATCH
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/verification/input_provenance_precheck.md"
  next_recommended: tdd_verification | null
```
