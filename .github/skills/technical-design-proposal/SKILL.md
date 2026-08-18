---
name: technical-design-proposal
description: Produce a reviewer-grade technical detailed design for a new feature or change using the evidence-backed current architecture as the design baseline. Use before implementation.
license: MIT
---

# Technical Detailed Design Proposal

## Principle

First reconstruct the relevant current behavior, then propose change.

Clearly separate:

- CURRENT VERIFIED BEHAVIOR
- REQUIREMENT
- PROPOSED DESIGN
- ASSUMPTION
- OPEN QUESTION

Do not present proposed classes as existing classes.

## Required Design Depth

Include when relevant:

1. purpose/scope/non-goals
2. current affected architecture
3. normalized requirements
4. proposed architecture
5. alternatives and tradeoffs
6. component responsibilities
7. class/interface design
8. method/pseudo-signatures in repository language
9. existing integration points
10. data model/schema
11. configuration
12. runtime sequences
13. error/retry/fallback
14. lifecycle/concurrency
15. security/sensitive data
16. observability
17. compatibility
18. testing
19. implementation phases
20. exact file/class change proposal
21. risks/open questions
22. evidence index

## Architecture and Class Diagrams

Diagrams are part of the technical design, not optional decoration.

### Mandatory diagram rule

If the proposed design introduces or materially modifies any of the following:

- classes
- interfaces
- services
- factories/providers/selectors
- adapters/wrappers
- controllers/handlers
- repositories
- major dependencies between components

the TDD MUST include BOTH:

1. **CURRENT architecture/class/component diagram**
2. **PROPOSED architecture/class/component diagram**

Use Mermaid when practical.

Prefer:

```mermaid
classDiagram
```

for static type relationships, and use a component-style Mermaid diagram when package/module/system boundaries communicate the design more clearly.

Sequence diagrams do NOT replace class/component diagrams.

Sequence diagrams explain runtime behavior.
Class/component diagrams explain static design structure.
A reviewer-grade TDD normally needs both when the change affects structure and runtime behavior.

### CURRENT diagram requirements

The CURRENT diagram must:

- contain only source-verified existing types/components
- show the relevant current ownership/boundaries
- show important dependencies/call relationships
- identify external systems/boundaries where relevant
- avoid proposed types
- label uncertain relationships instead of inventing them

### PROPOSED diagram requirements

The PROPOSED diagram must:

- clearly distinguish EXISTING and NEW/MODIFIED types
- show interfaces and implementations
- show inheritance/implementation relationships
- show composition/dependency relationships
- show primary callers/consumers
- show important external boundaries
- reflect the recommended design, not every rejected alternative
- use the same names as the class/interface design and file-change sections

Do not invent extra classes merely to make the diagram visually neat.

### Diagram-to-design consistency

Every major NEW or materially MODIFIED type listed in:

- Proposed Components
- Class/Interface Design
- Exact File/Class Change Proposal

must appear in the PROPOSED class/component diagram.

Every major relationship shown in the diagram must be explainable by the written design.

If the diagram and prose disagree, the TDD is incomplete and must be corrected before completion.

## Runtime Diagrams

When the feature changes runtime behavior, include sequence/flow diagrams for the important scenarios.

At minimum cover:

- primary success flow
- primary failure/error flow
- important negative/exclusion flow when the requirement contains MUST-NOT/skip behavior
- retry/fallback flow when applicable

Do not use sequence diagrams as a substitute for static architecture/class diagrams.

## Integration Table

| Existing Class/Method | Current Role | Proposed Change | Reason | Risk |
|---|---|---|---|---|

## Proposed Components

| Component | Existing/New | Responsibility | Dependencies |
|---|---|---|---|

## Diagram Quality Gate

Before completing the TDD, perform this check:

1. Does the proposal introduce or materially modify classes/interfaces/components?
   - If YES, CURRENT and PROPOSED static diagrams are mandatory.

2. Does every major proposed type appear in the PROPOSED diagram?
   - If NO, update the diagram or remove/correct the unsupported type.

3. Does every major modified existing type appear where its relationship matters?
   - If NO, update the diagram.

4. Are existing vs proposed elements visually/textually distinguishable?
   - If NO, fix the diagram.

5. Are external boundaries represented correctly?
   - If NO, fix the diagram.

6. Are sequence diagrams present for behaviorally significant flows?
   - If NO, add them.

7. Do class/component diagrams, sequence diagrams, component responsibilities,
   pseudo-signatures, and exact file/class changes describe the SAME design?
   - If NO, reconcile the contradiction before completion.

A TDD that proposes major structural code changes but has no static
class/component diagram is INCOMPLETE.

## Output

`docs/reverse-engineering/proposals/<feature>-tdd.md`

Do not update baseline memory.
