---
name: post-readiness-adversarial-audit
description: Independently challenge an IMPLEMENTATION_READY package after design-to-implementation. Resolve actual artifact paths from workflow state, verify workflow/gate integrity, audit requirement-to-WBS traceability, architecture consistency, negative requirements, boundary exposure, source anchors, and missing work before downstream implementation handoff.
license: MIT
---

# Post-Readiness Adversarial Audit

## Mission

Do not trust `IMPLEMENTATION_READY` merely because the earlier workflow produced it.

This skill independently challenges the completed planning package before downstream
implementation handoff.

It is a verification skill, not a design generator and not an implementation skill.

Canonical position:

```text
design-to-implementation
→ IMPLEMENTATION_READY
→ POST-READINESS ADVERSARIAL AUDIT
→ audited handoff
```

## 1. Input Resolution — No Guessing

Resolve artifact paths in this order:

```text
1. persisted workflow state / execution report
2. explicit workflow inputs
3. exact artifact paths recorded by prior stage gates
```

Do NOT guess a replacement filename or search for a "similar-looking" artifact when an expected
path is missing.

If a required artifact path cannot be resolved:

`POST_AUDIT_INPUT_NOT_RESOLVED`

Record the exact missing artifact/path.

Required logical inputs:

- authoritative requirement
- current-state analysis
- verified gap analysis
- TDD
- TDD verification
- design artifact registry
- all implementation-required detailed designs
- all corresponding DD verification reports
- WBS
- WBS verification
- test design
- implementation-readiness report
- persisted workflow state/execution report when available
- current repository source

Current source remains authoritative for CURRENT behavior.

## 2. Workflow / Gate Integrity Audit

Verify the completed run actually passed the required lifecycle rather than merely producing files.

Create:

| Required Stage | Expected Gate | Actual Gate | Artifact Exists? | Gate/Artifact Consistent? | Verdict |
|---|---|---|---:|---:|---|

At minimum cover:

- TDD verification
- design artifact decomposition
- every implementation-required DD verification
- WBS generation
- WBS verification
- implementation readiness

Rules:

- file existence alone does not prove stage success
- prose saying "ready" does not replace structured gate evidence
- missing/malformed gate is a finding
- registry status must agree with DD verification artifacts
- WBS/readiness claims must agree with upstream statuses

## 3. WBS Semantic Consistency + Deterministic Deep Trace

### 3A. Exhaustive WBS ↔ Artifact Semantic Identity

Before sampling anything, inspect **every WBS task**.

For each WBS task derive its primary implementation deliverable and verify:

```text
WBS task title / objective / primary deliverable
↔ referenced Artifact ID
↔ canonical registry artifact name + responsibility
↔ VERIFIED DD owned implementation unit
↔ TDD decision
```

Create:

| WBS ID | Primary Deliverable | Artifact ID | Canonical Artifact Name | Registry Responsibility | DD-Owned Unit | Semantic Match? | Finding |
|---|---|---|---|---|---|---:|---|

Hard failure code:

`WBS_ARTIFACT_SEMANTIC_MISMATCH`

Use it when a task's primary deliverable does not belong to the referenced artifact according to
the registry / VERIFIED DD.

Important:

- Artifact ID existence is not semantic proof.
- A symbol merely appearing in TDD/DD is not ownership proof.
- `@see`, dependency, import, mention, cross-reference, or neighboring design prose does not allow
  re-labeling an artifact.
- The same Artifact ID MUST use the same canonical artifact name/responsibility throughout the
  report.
- If section A says `ART-001 = AuditLogger Interface`, another section may not treat
  `ART-001 = AuditException` unless the registry/DD explicitly defines that ownership.

Required threshold:

```text
WBS semantic identity consistency = 100% of ALL WBS tasks
```

Any HIGH/CRITICAL semantic mismatch forces:

`POST_READINESS_AUDIT_FAIL_WBS_GAPS`

### 3B. Deterministic Deep Backward-Trace Sample

Do not ask the human to manually choose WBS IDs.

Select up to three WBS tasks deterministically from the actual WBS:

1. lowest-ID code-changing task
2. highest-ID code-changing task
3. code-changing task with the highest dependency count
   - tie-breaker: lowest WBS ID
   - if duplicate of #1/#2, choose the next highest dependency-count distinct task

If the WBS does not expose a usable code-changing classification, use all tasks when task count <= 10;
otherwise choose lowest ID, highest ID, and highest dependency-count task.

For each selected task trace:

```text
WBS task
→ VERIFIED Detailed Design
→ Design Artifact registry entry
→ TDD decision
→ Verified Gap
→ Requirement rule
→ CURRENT source anchor (when CURRENT source exists)
```

For PROPOSED_NEW components, verify the proposed location/ownership against the approved design;
do not call a non-existent current source path "source verified".

Create:

| Sample | WBS ID | Primary Deliverable | DD | Artifact ID | Canonical Artifact Name | TDD Decision | Gap | Requirement | Source/Proposed Anchor | Broken Link? | Verdict |
|---|---|---|---|---|---|---|---|---|---|---:|---|

A generated artifact is navigation evidence, not proof of CURRENT source.

### 3C. Sampling Claim Discipline

The deep backward trace above is a **sample** unless every WBS task was selected.

Therefore:

- `3/3 sampled WBS tasks passed` is valid when three were sampled.
- `all WBS tasks trace back correctly` is forbidden unless all WBS tasks were exhaustively traced.
- Universal claims may only come from exhaustive checks, such as the all-task semantic identity
  audit in §3A.

If the report makes an unsupported universal claim from sampled evidence, record:

`AUDIT_CLAIM_EXCEEDS_EVIDENCE`

and fail workflow integrity.

## 4. Proposed Static Architecture Consistency Audit

From the TDD `PROPOSED Static Architecture` and `Component Responsibilities`:

For every major PROPOSED_NEW or materially MODIFIED component/type:

```text
TDD static architecture
↔ component responsibilities
↔ design artifact registry
↔ detailed design
↔ WBS task(s)
↔ verification/test obligations
```

For every EXISTING component named as an existing source anchor:

- verify it exists
- verify the claimed current role/relationship where implementation depends on it

Create:

| Component | Existing/Proposed | Registry Artifact | DD | WBS Coverage | Test Coverage | Current Source Proof Needed? | Verdict |
|---|---|---|---|---|---|---:|---|

No major proposed component may exist only in a diagram.

## 5. Requirement / Negative-Rule Audit

Enumerate every explicit MUST-NOT / exclusion / preserved-behavior rule from the authoritative
requirement and verified gap analysis.

For each one prove:

```text
requirement exclusion
→ TDD preservation mechanism
→ relevant DD
→ WBS impact/non-impact
→ test/verification coverage
```

Create:

| Exclusion Rule | TDD Mechanism | DD | WBS | Test | Preserved? | Evidence |
|---|---|---|---|---|---:|---|

Required target:

```text
negative-rule coverage = 100%
```

Any material exclusion without design/test coverage blocks PASS.

## 6. Boundary → Exposure Re-Audit

Identify every integration/boundary artifact that the verified TDD says is materially changed.

For each affected boundary:

```text
boundary
← ALL direct invocation/construction sites
← ALL material caller chains
← ALL external entry points / proven internal roots
```

Compare the re-audit result with:

- current-state analysis
- TDD
- artifact registry
- DD
- WBS
- tests

Create:

| Boundary | Source Invocation Sites | External/Internal Roots | TDD Coverage | DD/WBS Coverage | Missing Exposure? | Verdict |
|---|---|---|---|---|---:|---|

Do not sample one representative endpoint when the boundary has multiple callers.

## 7. WBS Missing-Work Recheck

Independently challenge the earlier WBS verification.

From verified DD/source impacts search where applicable:

- callers/references
- implementations
- constructors/factories/DI
- serializers/mappers
- configuration consumers
- persistence/migration
- tests/fixtures
- integration adapters
- sibling operations that must preserve behavior
- documentation/config samples required by the approved design

Do not add speculative work.

Create:

| Finding ID | Design Artifact / DD | Source Evidence | Missing WBS Work? | Severity | Required Action |
|---|---|---|---:|---|---|

## 8. Source-Anchor Health

For all source anchors used by the sampled WBS traces plus every major architecture/boundary
decision:

- verify exact symbol/path exists
- verify claimed current role
- verify source has not drifted from the generated artifact's assumption

Record:

```text
VERIFIED
CONTRADICTED
SOURCE_NOT_RESOLVED
```

## 8A. Cross-Section Canonical Identity Consistency

Build a canonical identity dictionary from the design artifact registry:

```text
Artifact ID → canonical artifact name → responsibility → VERIFIED DD
```

Then scan every audit section/table that mentions an Artifact ID.

Create:

| Artifact ID | Canonical Identity | Observed Labels / Responsibilities | Consistent? | Finding |
|---|---|---|---:|---|

Rules:

- one Artifact ID cannot silently change meaning between sections
- a WBS task label does not redefine the artifact
- TDD mentions do not redefine registry ownership
- any semantic contradiction that affects a HIGH/CRITICAL implementation task blocks PASS

Failure code:

`CROSS_SECTION_ARTIFACT_IDENTITY_CONTRADICTION`


## 9. Quantitative Audit Scorecard

Report measurable results:

| Metric | Required Threshold | Actual | Pass? |
|---|---:|---:|---:|
| Required workflow stages/gates valid | 100% | ... | ... |
| Implementation-required DDs verified | 100% | ... | ... |
| WBS task semantic identity consistency (ALL tasks) | 100% | ... | ... |
| Sampled deep WBS backward traces complete | 100% of selected sample | ... | ... |
| Major proposed architecture components covered by registry/DD/WBS | 100% | ... | ... |
| Explicit negative rules covered | 100% | ... | ... |
| Affected integration boundaries with exposure closure | 100% | ... | ... |
| Sampled/critical current source anchors verified | 100% | ... | ... |
| Artifact ID canonical identity consistent across report | 100% | ... | ... |
| Unresolved source-resolvable CRITICAL | 0 | ... | ... |
| Unresolved source-resolvable HIGH | 0 | ... | ... |
| HIGH/CRITICAL missing-work findings | 0 | ... | ... |

Do not replace failed thresholds with subjective Green/Yellow/Red.

## 10. Verdict

Use exactly one:

- `POST_READINESS_AUDIT_PASS`
- `POST_READINESS_AUDIT_PASS_WITH_WARNINGS`
- `POST_READINESS_AUDIT_FAIL_SOURCE_GAPS`
- `POST_READINESS_AUDIT_FAIL_DESIGN_GAPS`
- `POST_READINESS_AUDIT_FAIL_WBS_GAPS`
- `POST_READINESS_AUDIT_FAIL_WORKFLOW_INTEGRITY`
- `POST_AUDIT_INPUT_NOT_RESOLVED`

### PASS

Requires all mandatory scorecard thresholds to pass.

Additionally:

- `WBS_ARTIFACT_SEMANTIC_MISMATCH` count must be 0
- `CROSS_SECTION_ARTIFACT_IDENTITY_CONTRADICTION` count must be 0 for HIGH/CRITICAL implementation work
- `AUDIT_CLAIM_EXCEEDS_EVIDENCE` count must be 0
- sampled evidence must never be presented as exhaustive evidence

### PASS_WITH_WARNINGS

Allowed only when:

- all mandatory thresholds pass
- no HIGH/CRITICAL finding remains
- warnings are non-blocking and explicitly listed

### FAIL

Choose the failure class corresponding to the first material blocking layer.
Do not call PASS because the package "looks complete".

## 11. Mutation Rule

This audit MUST NOT silently edit:

- TDD
- registry
- DD
- WBS
- test design
- readiness report

It reports findings only.

Corrections happen in the owning upstream workflow, then the audit is rerun.

## Output

Use the active workflow-declared post-readiness audit output path. Do not reuse legacy audit artifacts.
