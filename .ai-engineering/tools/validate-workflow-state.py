#!/usr/bin/env python3
from pathlib import Path
import sys, yaml

if len(sys.argv) != 2:
    print("usage: validate-workflow-state.py <workflow_state.yaml>")
    sys.exit(2)

p = Path(sys.argv[1])
errors = []
if not p.exists():
    errors.append(f"state file missing: {p}")
else:
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        data = None
        errors.append(f"workflow state is not valid YAML: {e}")

    if not isinstance(data, dict):
        errors.append("workflow state must be a YAML mapping")
    else:
        for key in ["workflow", "run_id", "status", "active_step", "completed_steps", "last_gate", "artifacts"]:
            if key not in data:
                errors.append(f"missing state key: {key}")

        completed = set(data.get("completed_steps") or [])
        active = data.get("active_step")
        if isinstance(active, str) and active in completed:
            errors.append(f"active_step is already completed: {active}")

        last_gate = data.get("last_gate") or {}
        if isinstance(last_gate, dict):
            gate_artifact = last_gate.get("artifact")
            if gate_artifact and gate_artifact not in set((data.get("artifacts") or {}).values()) and gate_artifact not in set(
                v.get("path") for v in (data.get("artifacts") or {}).values() if isinstance(v, dict)
            ):
                errors.append("last_gate artifact is not persisted in artifacts")

if errors:
    print("WORKFLOW_STATE_VALIDATION_FAIL")
    for e in errors:
        print("- " + e)
    sys.exit(1)

print("WORKFLOW_STATE_VALIDATION_PASS")
print(f"state={p}")
