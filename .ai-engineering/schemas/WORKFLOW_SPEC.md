# Workflow File Specification

This is a repository convention, not a GitHub-native workflow schema.

Required top-level fields:

```yaml
version:
'4.0'
description:
runner_skill:
state_path:
inputs:
steps:
```

Each step may define:

```yaml
prompt:
inline_instruction:
skills:
output:
statuses:
retry_step:
on_success:
inputs:
child_workflow:
execution:
```

`{{variable}}` placeholders are resolved only from explicit workflow inputs, defaults,
or persisted state.

A stage artifact must end with a `WORKFLOW_GATE` YAML block.
The runner must not infer a stage result from prose when the gate is absent.

## 4.0 Extensions

### Nested phases

A top-level workflow may compose child workflows:

```yaml
phases:
  phase_name:
    workflow: .ai-engineering/workflows/child.yaml
    pass_inputs: [...]
    derived_inputs: {...}
    require_terminal_status: [...]
```

### Iterative `foreach` stages

A workflow may iterate over a registry:

```yaml
foreach:
  source: <artifact>
  items: <selection expression>
  id_field: <column/key>
  order: dependency_topological
```

The runner interprets this declaratively. This is a repository convention, not a general-purpose executable YAML engine.

### Verification loops

Verification must remain a separate pass from generation.
A verifier reports findings; a revision step applies them; the verifier then re-runs.

## 4.0 Design Quality Extension

Design-producing gates may include an optional `quality` object.

For technical design:

```yaml
quality:
  current_static_architecture: COMPLETE | JUSTIFIED_NA | INCOMPLETE
  proposed_static_architecture: COMPLETE | INCOMPLETE
  component_responsibilities: COMPLETE | INCOMPLETE
  runtime_sequences: COMPLETE | JUSTIFIED_NA | INCOMPLETE
  diagram_prose_consistency: VERIFIED | NOT_VERIFIED
```

A workflow must not treat `TDD_INCOMPLETE_ARCHITECTURE` as ready.

## Execution control: stop_after_step

A workflow runner may accept:

```yaml
stop_after_step: <declared step id | null>
```

This control is inclusive. The named step must execute, its declared output must exist, its gate must be validated and persisted, and only then may the runner stop before the workflow-derived next step. Intentional stop returns `PARTIAL_RESUMABLE`.

For fresh runs, `artifact_root` and `state_path` must resolve under `docs/reverse-engineering/runs/<run_id>/` unless an explicitly equivalent run-scoped path is supplied.


## Resolver input contract

Every step using `.ai-engineering/prompts/common/resolve-high-impact-unknowns.md` must explicitly bind:

```yaml
inputs:
  blocking_artifact: '{{blocking_artifact}}'
  blocking_qids: '{{blocking_qids}}'
  retry_step: '{{blocking_retry_step}}'
```

The runner persists these three values from the gate that entered unknown resolution.

## Child workflow steps

A step may use `child_workflow` instead of `prompt`. Required child inputs must be bound explicitly.
Fresh child execution is isolated according to the runner contract.

## Foreach bindings

Per-item prompt variables that come from registry rows must be declared under `foreach.bindings`.
A binding may name a `field` and optional deterministic `transform: slugify`.
