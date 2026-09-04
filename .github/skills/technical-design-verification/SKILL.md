---
name: technical-design-verification
description: Independently verify a proposed TDD against requirement, current source, verified gaps, mandatory static/dynamic architecture content, provenance/exposure evidence, compatibility, and traceability before downstream detailed design or test planning.
license: MIT
---

# Technical Design Verification — 4.0

## Mission

Do not merely verify that the proposal sounds reasonable.

Verify:

```text
Requirement
→ Gap
→ Current Source
→ Static Architecture
→ Runtime Architecture
→ Proposed Change
→ Compatibility
→ Traceability
```

The verifier must NOT silently repair the TDD.

---

## 1. Mandatory Architecture Contract

Check for the exact sections:

```text
## CURRENT Static Architecture
## PROPOSED Static Architecture
## Component Responsibilities
## PROPOSED Dynamic Architecture / Runtime Sequences
```

Rules:

- `PROPOSED Static Architecture` is mandatory for a reviewer-grade TDD.
- If structural responsibility changes, the section must contain a static Mermaid diagram.
- If no static structural change exists, the section must explicitly show/describe the unchanged resulting structure and why.
- sequence diagrams do not satisfy the static architecture requirement.

Missing applicable static architecture => `TDD_PARTIALLY_VERIFIED` at best.
Do not return `TDD_VERIFIED`.

---

## 2. Diagram ↔ Source ↔ Prose Consistency

For every existing type/component in CURRENT/PROPOSED diagrams:

- prove it exists
- prove its relevant role/relationship

For every proposed type/component:

- confirm it is explicitly marked PROPOSED
- confirm responsibility is defined
- confirm it appears in the exact change set when implementation is required

Check consistency across:

```text
PROPOSED Static Architecture
↔ Component Responsibilities
↔ Class/Interface Design
↔ Runtime Sequences
↔ Exact Change Set
```

Contradictory names/relationships are verification failures.

---

## 3. Requirement / Gap Scope Verification

Create:

| TDD Decision ID | Requirement IDs | Gap IDs | Surface | Proposed Behavior | In Scope? | Evidence |
|---|---|---|---|---|---:|---|

No design item may widen scope silently.

---


## 3A. Implementation-Significant Proposed Unit Ownership

Before declaring the TDD verified, enumerate every implementation-significant PROPOSED unit
introduced by the design.

Examples include, when present:

- new class
- new interface
- new data carrier / DTO / value object
- new exception type
- new policy / strategy / provider
- new adapter / client
- new configuration owner
- new persistence object / schema
- materially new method/contract requiring independent implementation work

Do not treat every helper method or local variable as a design unit. A unit is
implementation-significant when it creates a distinct responsibility, contract, lifecycle,
dependency boundary, failure behavior, configuration/state ownership, or verification obligation.

For each unit prove explicit ownership:

```text
PROPOSED unit
→ static/component design presence when structurally material
→ explicit owning responsibility
→ intended artifact ownership:
     DEDICATED_ARTIFACT
     OR
     SUBORDINATE_TO:<future ART-ID>
```

Create:

| Proposed Unit | Type | Why Significant? | Static/Component Evidence | Intended Owner | Dedicated/Subordinate | Ownership Explicit? | Verdict |
|---|---|---|---|---|---|---:|---|

Required threshold:

```text
PROPOSED_UNIT_OWNERSHIP_COVERAGE = 100%
```

If any implementation-significant proposed unit has no explicit owner:

`TDD_INCOMPLETE_PROPOSED_UNIT_OWNERSHIP`

If a structurally material proposed unit is absent from `PROPOSED Static Architecture`:

`TDD_INCOMPLETE_ARCHITECTURE`

A mention, JavaDoc reference, `@see`, import, dependency arrow, method signature, or nearby prose
does not by itself prove ownership.


## 3B. Authoritative Decision-Matrix Execution Gate

When the requirement contains a MUST LOG / MUST NOT LOG decision matrix or equivalent scenario table,
treat that matrix as executable specification. For every TDD policy, predicate, decision tree, or
branching algorithm:

1. enumerate every authoritative scenario row;
2. evaluate the proposed logic with representative inputs for that row;
3. record actual proposed outcome vs required outcome;
4. require 100% row agreement.

Create:

| Requirement Row | Representative Inputs | Required Outcome | Proposed Logic Outcome | Match? | Evidence |
|---|---|---|---|---:|---|

Required threshold:

```text
DECISION_MATRIX_SEMANTIC_COVERAGE = 100%
DECISION_MATRIX_MISMATCHES = 0
```

A document that mentions all requirement IDs but implements a predicate that returns the wrong result
for any row is not verified. Use `TDD_CONTRADICTED` when the design logic directly contradicts an
authoritative requirement row.

## 3C. Requirement-Fidelity Gate

For every mandatory-looking field, behavior, scenario, or acceptance criterion in the TDD, trace it
back to an authoritative requirement or label it explicitly as PROPOSED design. Source availability
alone does not convert a field into a requirement.

Unsupported requirement expansion blocks `TDD_VERIFIED`.

## 4. Current Source Anchor Verification

For each existing file/class/method/config/boundary named by TDD:

- exists?
- current role?
- relevant caller/callee?
- reachable insertion point?

Unproven existing anchor:

`DESIGN_SOURCE_ANCHOR_NOT_PROVEN`

---

## 5. Field / Data Provenance Verification

Where data/context/output changes:

```text
CURRENT provenance
→ proven break point
→ PROPOSED change
→ observable behavior
```

Reject redundant or misplaced fixes.

---

## 6. Boundary → Exposure Verification

Where integration boundary changes:

```text
boundary
← all invocation sites
← all material callers
← all external/internal roots
```

No representative-endpoint shortcuts.

---

## 7. Compatibility / Exclusion Verification

Check:

- unaffected behavior
- MUST-NOT / non-goals
- API/protocol behavior
- error/result preservation
- configuration defaults
- internal/background flows
- sensitive-data rules
- failure isolation

---

## 8. Traceability Verification

| Requirement | Gap | TDD Decision | Static Component | Runtime Flow | Change | Test | Verdict |
|---|---|---|---|---|---|---|---|

A major component/change with no backward traceability is a finding.

---


## 8A. Proposed Unit Ownership Gate

Before the final TDD gate, verify:

- implementation-significant proposed units enumerated = 100%
- explicit ownership assigned = 100%
- structurally material proposed units represented in static architecture = 100%
- no unit is "owned" only because another artifact mentions it

Any failure blocks `TDD_VERIFIED`.

## 9. Verification Gate

`TDD_VERIFIED` requires:

```text
[ ] mandatory static architecture contract satisfied
[ ] diagram/prose/change-set consistency proven
[ ] every material decision maps to requirement/gap
[ ] authoritative decision matrix evaluated semantically with 100% row agreement
[ ] no unsupported requirement expansion
[ ] existing source anchors proven
[ ] proposed artifacts clearly proposed
[ ] provenance complete where applicable
[ ] exposure closure complete where applicable
[ ] compatibility/non-goals preserved
[ ] no HIGH/CRITICAL source-resolvable uncertainty
```

Statuses:

- `TDD_VERIFIED`
- `TDD_PARTIALLY_VERIFIED`
- `TDD_CONTRADICTED`
- `TDD_BLOCKED_SOURCE_GAPS`
- `TDD_INCOMPLETE_ARCHITECTURE`
- `TDD_INCOMPLETE_PROPOSED_UNIT_OWNERSHIP`

Output:

Use the active workflow-declared output path. Do not invent or reuse a legacy verification filename.


<!-- workflow-status-contract:start -->
```yaml
emitted_statuses:
  - TDD_VERIFIED
  - TDD_PARTIALLY_VERIFIED
  - TDD_CONTRADICTED
  - TDD_BLOCKED_SOURCE_GAPS
  - TDD_INCOMPLETE_ARCHITECTURE
  - TDD_INCOMPLETE_PROPOSED_UNIT_OWNERSHIP
```
<!-- workflow-status-contract:end -->
