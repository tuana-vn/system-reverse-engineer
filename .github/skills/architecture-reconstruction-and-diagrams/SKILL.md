---
name: architecture-reconstruction-and-diagrams
description: Reconstruct a consumer-usable current-system architecture model from verified source evidence, emphasizing responsibilities, dependencies, runtime relationships, system boundaries, and evidence-linked Mermaid diagrams rather than file inventories.
---

# Architecture Reconstruction and Diagrams — 4.0

## Mission

Turn verified repository evidence into an understandable model of the current system.

The goal is not to inventory files. The goal is to answer:

```text
what owns each major responsibility?
what calls what?
what crosses a boundary?
where is state owned?
what selects runtime variants?
what happens on failure?
```

## Relationship-First Rule

Prefer:

```text
responsibility + relationship + behavior + evidence
```

over:

```text
package name + file count + class list
```

File counts may appear as supporting topology context only. They are never sufficient architecture.

## Major Subsystem Model

For every material subsystem, record all applicable fields:

| Subsystem | Entry | Responsibility | Inputs | Outputs | Dependencies | State Ownership | Failure Behavior | Runtime/Config Selection | Evidence |
|---|---|---|---|---|---|---|---|---|---|

A material subsystem is not considered `MODELED` while an applicable field is blank or asserted without evidence.

## Mandatory Diagram Set for Full Baseline

A full repository baseline must create these Mermaid-backed artifacts under `docs/reverse-engineering/diagrams/`:

```text
01_system_context.md
02_component_architecture.md
03_primary_runtime_sequence.md
04_integration_boundaries.md
05_state_persistence_lifecycle.md
```

Each file must contain at least one valid `mermaid` fenced block and an `Evidence Anchors` section.

### 01 — System Context

Show:
- external actors/systems
- application boundary
- major inbound surfaces
- major outbound dependencies

### 02 — Component Architecture

Show:
- major runtime components/subsystems
- dependency direction
- ownership/responsibility boundaries
- material runtime variant points

Do not produce a package-count diagram.

### 03 — Primary Runtime Sequence

Show at least one externally significant end-to-end runtime flow:

```text
entry
→ validation/conversion
→ orchestration/domain
→ integration/persistence
→ result/error mapping
→ observable response/effect
```

Use a Mermaid `sequenceDiagram` when the behavior is sequential/collaborative.

### 04 — Integration Boundaries

Show:
- abstractions/adapters
- selectors/factories/bindings
- concrete integrations
- external systems/processes
- fallback or alternate routes where material

### 05 — State / Persistence / Lifecycle

Show the most material state-bearing lifecycle. Prefer:
- persistence ownership and read/write flow;
- background-job lifecycle;
- resource/session/thread lifecycle;
- state transitions.

For systems without persistence, model another material state/lifecycle concern rather than omitting the diagram.

## Diagram Evidence Rule

Every material node and edge must be supportable from current source evidence.

Each diagram artifact must include:

```text
## Evidence Anchors
- <repo-relative path> — <symbol/method/class/config key> — <what it proves>
```

Do not invent components merely to make a diagram visually complete.

## Output Model Artifacts

Create/update:

```text
docs/reverse-engineering/models/component_catalog.md
docs/reverse-engineering/models/runtime_flow_catalog.md
docs/reverse-engineering/models/integration_catalog.md
docs/reverse-engineering/models/configuration_model.md
docs/reverse-engineering/models/persistence_state_model.md
```

Use `NOT_APPLICABLE` with evidence where a model dimension truly does not apply.

## Completion Gate

Architecture synthesis is incomplete if any of the following is true:

```text
[ ] fewer than 5 mandatory diagram artifacts exist
[ ] any mandatory diagram lacks Mermaid
[ ] any mandatory diagram lacks evidence anchors
[ ] a material subsystem lacks responsibility
[ ] a material subsystem lacks dependencies
[ ] a material subsystem lacks state/failure/selection classification where applicable
[ ] primary runtime behavior exists only as prose/class lists with no sequence model
[ ] integration boundaries exist but no boundary model exists
```


## Mermaid Syntax Safety Contract

Every generated Mermaid diagram MUST use syntax that belongs to exactly one Mermaid diagram type.

### Flowchart / graph rules

For diagrams beginning with:

```text
graph TD
graph LR
flowchart TD
flowchart LR
```

use flowchart edges only.

Valid:

```text
REST --> VALIDATOR
REST -->|validate()| VALIDATOR
PARSER -.-> LOGIC
```

Invalid in a flowchart:

```text
REST->>VALIDATOR: validate()
REST-->>MODEL: result
```

`->>` and `-->>` are sequence-diagram message operators and MUST NOT appear in a graph/flowchart.

### Sequence diagram rules

For diagrams beginning with:

```text
sequenceDiagram
```

declare participants and use sequence-message syntax.

Valid:

```text
participant REST as REST Handler
participant VALIDATOR as Validator

REST->>VALIDATOR: validate()
VALIDATOR-->>REST: valid
```

Do not use flowchart node declarations such as:

```text
REST[REST Handler]
VALIDATOR["Validator"]
```

inside a sequence diagram.

### Mandatory self-check before writing a Mermaid artifact

Before persisting any Mermaid block:

1. Identify its declared diagram type from the first Mermaid statement.
2. Check every connector/message against that diagram type.
3. For `graph`/`flowchart`, reject any line containing `->>` or `-->>`.
4. For `sequenceDiagram`, reject flowchart-style node declarations (`ID[...]`, `ID(...)`, `ID{...}`).
5. Ensure every message with `:` in a sequence diagram has non-empty text after the colon.
6. Prefer quoted flowchart node labels when labels contain `<br/>`, punctuation, parentheses, brackets, or method names.
7. Keep diagram syntax minimal; do not mix diagram grammars for visual convenience.
8. If uncertain whether a diagram will parse, simplify it rather than emitting speculative Mermaid syntax.

A diagram that does not pass this self-check MUST NOT be counted toward mandatory diagram coverage.

### Canonical examples

Component/architecture diagram:

```text
graph TD
    REST["REST Handler<br/>SnapshotGroupHandler"]
    VALIDATOR["Validator<br/>SnapshotGroupValidator"]
    LOGIC["Logic<br/>GetSnapshotGroupLogic"]

    REST -->|validate()| VALIDATOR
    REST -->|getSnapshotGroups()| LOGIC
```

Runtime sequence:

```text
sequenceDiagram
    participant REST as SnapshotGroupHandler
    participant VALIDATOR as SnapshotGroupValidator
    participant LOGIC as GetSnapshotGroupLogic

    REST->>VALIDATOR: validate()
    VALIDATOR-->>REST: valid
    REST->>LOGIC: getSnapshotGroups()
    LOGIC-->>REST: result
```



## Semantic Diagram Type Contract

The semantic purpose of a required diagram is fixed by the artifact contract.

A Mermaid syntax problem MUST be repaired **within the required diagram type**. Never change
the diagram type merely because another Mermaid grammar is easier to generate.

Canonical mapping:

| Required artifact | Required semantic representation | Allowed Mermaid form |
|---|---|---|
| System Context | system/external-boundary relationships | `graph` or `flowchart` |
| Component Architecture | components, layers, ownership, dependencies | `graph` or `flowchart` |
| Primary Runtime Sequence | time-ordered calls and responses | `sequenceDiagram` |
| Integration Boundaries | system-to-external-system boundaries and dependencies | `graph` or `flowchart` |
| State / Persistence Lifecycle | state transitions, ownership, persistence lifecycle | `stateDiagram-v2` or `flowchart`, chosen according to the evidence |

### Preservation rule

If the requested artifact is `Component Architecture`, it MUST remain a component/dependency
graph. For example, this is incorrect repair behavior:

```text
Component Architecture has invalid graph syntax
→ convert the artifact to sequenceDiagram
```

The correct behavior is:

```text
Component Architecture has invalid graph syntax
→ retain graph/flowchart
→ repair only the invalid graph connectors/labels
```

Likewise:

```text
Primary Runtime Sequence
```

must remain a sequence diagram and MUST NOT be converted into a component graph merely to avoid
sequence syntax.

### Semantic self-check

Before persisting a mandatory diagram, verify both:

1. **Grammar correctness** — connectors and declarations belong to the selected Mermaid grammar.
2. **Semantic correctness** — the selected Mermaid diagram type matches the purpose of the required artifact.

A syntactically valid diagram with the wrong semantic type MUST NOT satisfy the diagram quality gate.

For Component Architecture specifically, the diagram should primarily communicate:

- architectural layers or subsystems;
- component responsibility boundaries;
- dependency direction;
- important interfaces/adapters;
- relevant external dependencies.

Method names may label relationships when useful, but the artifact must remain an architectural
relationship graph rather than becoming a chronological call sequence.
