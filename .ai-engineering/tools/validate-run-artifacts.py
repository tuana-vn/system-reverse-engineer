#!/usr/bin/env python3
"""
Validate run-scoped artifact isolation and basic provenance.

Usage:
  python .ai-engineering/tools/validate-run-artifacts.py <run_id>

This is intentionally structural. It does not replace semantic verifiers.
"""
from pathlib import Path
import sys, re, yaml

ROOT = Path(__file__).resolve().parents[2]
if len(sys.argv) != 2:
    print("usage: validate-run-artifacts.py <run_id>")
    sys.exit(2)

run_id = sys.argv[1]
run_root = ROOT / "docs" / "reverse-engineering" / "runs" / run_id
manifest = run_root / "RUN_MANIFEST.yaml"

errors = []
for forbidden_name in ["00_workflow_state.md", "workflow_state.md"]:
    forbidden = run_root / forbidden_name
    if forbidden.exists():
        errors.append(f"forbidden duplicate run state artifact: {forbidden.relative_to(ROOT)}")
if not run_root.exists():
    errors.append(f"run root missing: {run_root}")
if not manifest.exists():
    errors.append(f"run manifest missing: {manifest}")
else:
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    if str(data.get("run_id")) != run_id:
        errors.append(f"manifest run_id mismatch: {data.get('run_id')!r}")
    if not data.get("agent_package_version"):
        errors.append("manifest missing agent_package_version")
    artifacts = data.get("artifacts") or {}
    for key, val in artifacts.items():
        if isinstance(val, dict):
            path = val.get("path")
        else:
            path = val
        if not path:
            continue
        p = ROOT / path
        try:
            p.relative_to(run_root)
        except Exception:
            errors.append(f"artifact escapes run root: {key} -> {path}")
        if not p.exists():
            errors.append(f"manifest artifact missing: {key} -> {path}")

if errors:
    print("RUN_ARTIFACT_VALIDATION_FAIL")
    for e in errors:
        print("- " + e)
    sys.exit(1)

print("RUN_ARTIFACT_VALIDATION_PASS")
print(f"run_id={run_id}")
print(f"run_root={run_root.relative_to(ROOT)}")
