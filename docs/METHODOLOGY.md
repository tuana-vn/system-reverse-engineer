# Methodology — Evidence-First Controlled Agentic Engineering

## Five-layer model

```text
1. AGENT       orchestration role and global evidence rules
2. WORKFLOW    state machine, transitions, gates
3. PROMPT      task-specific scope and deliverable
4. SKILL       reusable investigation/design methodology
5. EVIDENCE    current source, runtime facts, verified artifacts
```

Artifacts produced by one step become explicit inputs to later steps.

## Why workflows exist

Skills intentionally remain generic.
Prompts intentionally remain task-specific.
Workflows connect them without forcing the model to invent stage order.

A workflow step is complete only when its output artifact contains the expected
`WORKFLOW_GATE` block and the status is allowed by the workflow definition.

## Core engineering gates

```text
scope isolation
→ control-flow trace
→ boundary → exposure closure
→ field/data provenance
→ counterexample search
→ evidence-backed verdict/oracle
→ promotion/design/test
```

## Non-goals

This package does not claim that YAML makes Copilot deterministic.
The workflow control plane constrains LLM orchestration; it does not replace engineering judgment.

This package also does not require repo-specific scripts for core correctness.


## Design Compilation Model

4.0 treats implementation planning like a controlled compilation pipeline:

```text
Requirement          = source specification
Verified TDD         = architecture-level intermediate representation
Design Artifact DD   = implementation-level intermediate representation
WBS                  = executable implementation plan
Tests                = verification oracle
```

This is an analogy, not a claim of deterministic compilation.

The point is that every transformation has:
- explicit inputs
- traceability
- a verification gate
- a persistent artifact

### Design-to-implementation gates

```text
TDD_VERIFIED
→ ARTIFACT_REGISTRY_READY
→ ALL_REQUIRED_DD_VERIFIED
→ WBS_VERIFIED
→ IMPLEMENTATION_READY
```

Skipping a gate reintroduces guesswork.

## Operational Navigation Layer

The engineering methodology and the operating model are separate.

```text
METHOD:
skills + evidence gates

EXECUTION:
prompts + workflows

HUMAN NAVIGATION:
use cases + matrices + runbook
```

This matters because adding more skills does not automatically make the system easier to use.

The operator should normally start from a use case, not from a skill name.

```text
engineering intent
→ use case
→ workflow
→ prompt
→ skill
→ evidence
→ artifact
→ gate
```


## Packaging Architecture

The package now has three physical layers:

```text
.github/
→ execution-platform adapter

.ai-engineering/
→ portable engineering control plane

docs/reverse-engineering/
→ target-project evidence/artifacts
```

This mirrors the conceptual architecture:

```text
Agent Adapter
→ Workflow / Prompt / Skill Methodology
→ Project Evidence
```

The physical layout should not change the evidence hierarchy or verification gates.

## Architecture as a Verification Artifact

Technical design must contain both structural and dynamic views.

```text
Static Architecture
= what components/types exist and how responsibilities/dependencies are arranged

Dynamic Architecture
= how those components cooperate at runtime
```

A sequence diagram cannot substitute for a static design diagram.

For materially structural changes:

```text
CURRENT Static Architecture
→ PROPOSED Static Architecture
→ Component Responsibilities
→ Runtime Sequences
→ Exact Change Set
```

must describe one consistent design.

Architecture is not decoration; it is an implementation-planning and review artifact.

## Whole-Package Verification

Independent verification now exists at three scales:

```text
artifact:
DD generation → DD verification

plan:
WBS generation → WBS verification

whole package:
IMPLEMENTATION_READY → post-readiness adversarial audit
```

The final audit uses persisted workflow state as the artifact locator and independently
rechecks source-backed traceability and exclusion/boundary coverage.

This reduces dependence on conversational memory and catches self-consistent but incorrect
planning packages before implementation handoff.

## Semantic Traceability

Traceability has two independent dimensions:

```text
syntactic traceability:
ID/link exists

semantic traceability:
linked artifacts describe the same approved implementation responsibility
```

A valid chain requires both.

Canonical identity rule:

```text
Artifact ID
→ canonical registry name/responsibility
→ VERIFIED DD-owned implementation unit
```

Downstream WBS/audit prose cannot redefine that identity.

Sampling rule:

```text
sampled proof supports sampled claims only
```

A verifier may claim all-task completeness only for checks actually executed over all tasks.

## Proposed Unit Ownership Closure

Before DD/WBS:

```text
verified TDD
→ enumerate implementation-significant proposed units
→ assign exactly one explicit owner each
→ 100% ownership closure
→ artifact registry ready
```

A unit can be a dedicated artifact or an explicitly-owned subordinate unit.

## Fresh Execution Semantics

Workflow completion is run-specific.

```text
execution_mode: fresh
OR ignore_previous_completion: true
→ previous completion != current execution
```

## Gate Contract Integrity

Skill rule, prompt output contract, and workflow state machine are one executable contract:

```text
skill can emit X
→ prompt allows X
→ workflow routes X
```

If any link is missing, the gate is not operational.

Required invariant:

`EMITTED_GATE_STATUS ⊆ WORKFLOW_ALLOWED_STATUS`

## Artifact Provenance

Fresh execution requires identity, isolation, and provenance:

```text
package version
+ run_id
+ source commit
+ exact artifact path
→ run manifest
```

A prior-run artifact cannot satisfy a current-run gate.

## Decomposition Verification

Design artifact decomposition is now independently verified before detailed design:

```text
TDD
→ artifact decomposition
→ independent decomposition verification
→ DD loop
```

The verifier independently inventories implementation-significant proposed units and checks
explicit registry ownership.

## Filename Simplicity

Artifact identity is:

```text
run directory
+ manifest metadata
+ stable filename
```

not:

```text
metadata encoded into the filename
```

Version/date/run identity must not be appended to generated filenames.


## Current-State Consumer Model Quality

Full reverse engineering must convert verified evidence into a consumer-usable current-state technical model.

Required full-baseline outputs:

```text
CURRENT_STATE_TDD.md
5 evidence-linked Mermaid diagram artifacts
component/runtime-flow/integration/configuration/persistence-state model artifacts
separate readiness audit
```

Readiness requires both evidence correctness and model usability. A fact inventory or adversarial audit report does not substitute for a Current-State TDD.

Mandatory diagram families:

```text
system context
component architecture
primary runtime sequence
integration boundaries
state/persistence/lifecycle
```

Run `python .ai-engineering/tools/validate-reverse-engineering-quality.py --artifact-root docs/reverse-engineering` before declaring the full baseline ready.
