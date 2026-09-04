# Package Maintenance Rules — System Reverse Engineer 4.0

**Status:** NORMATIVE for package maintenance.

## Current-baseline rule

The checked-out package is the only maintenance baseline. Do not reconstruct methodology files from chat memory, stale exports, or copied fragments.

## Maintenance discipline

- Read `docs/METHODOLOGY_BASELINE.md` before changing methodology, workflow semantics, quality gates, or agent boundaries.
- Make the smallest responsible change for the verified defect or requirement.
- Keep runtime engineering execution read-only for `.ai-engineering/` and `.github/`; only explicit package-maintenance work may change those paths.
- Keep deterministic mechanical checks in the delivered validators; keep semantic correctness in independent workflow verifier stages.
- Do not create feature-specific or incident-specific permanent validators when a generic invariant can cover the same failure class.
- Validate workflow references, prompt variables, resolver bindings, child workflow inputs, state paths, package provenance, and foreach bindings before delivery.
- Test the extracted delivery package in strict package-root mode and in repository-overlay mode where applicable.
- Do not introduce additional package-version labels into active docs, prompts, scripts, workflow files, or skills. The active baseline is `4.0`.

## Delivered validators

The package maintains the generic runtime validation surface under `.ai-engineering/tools/`:

- `validate-package-layout.py`
- `validate-methodology-baseline.py`
- `validate-workflow-contracts.py`
- `validate-workflow-state.py`
- `validate-required-inputs.py`
- `validate-run-artifacts.py`

A new validator is justified only when the invariant is deterministic, broadly reusable, and cannot be cleanly covered by the existing validators.

## Delivery proof

Before packaging:

- all delivered validators pass;
- every workflow YAML parses;
- every referenced prompt/skill/child workflow exists;
- every prompt placeholder is resolvable from explicit workflow inputs/defaults, foreach bindings, or documented runner-owned state;
- no workflow has multiple authoritative state files;
- no stale package-version label exists;
- no historical release/change-record/archive material is included;
- the current manifest matches the delivered files.
