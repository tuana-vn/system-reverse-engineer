#!/usr/bin/env python3
"""Validate existence of required workflow artifact inputs.

Usage:
  python .ai-engineering/tools/validate-required-inputs.py \
    requirement_path=... current_state_artifact=... gap_artifact=... tdd_path=...

Paths are repository-relative unless absolute. This validator intentionally checks existence only;
semantic provenance is verified by the workflow precheck stage.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = {"requirement_path", "current_state_artifact", "gap_artifact", "tdd_path"}
vals = {}
errors = []
for arg in sys.argv[1:]:
    if "=" not in arg:
        errors.append(f"invalid argument (expected key=path): {arg}")
        continue
    k, v = arg.split("=", 1)
    vals[k] = v

missing_keys = sorted(REQUIRED - vals.keys())
for k in missing_keys:
    errors.append(f"missing required argument: {k}")

for k in sorted(REQUIRED & vals.keys()):
    raw = Path(vals[k])
    p = raw if raw.is_absolute() else ROOT / raw
    if not p.is_file():
        errors.append(f"REQUIRED_INPUT_ARTIFACT_MISSING: {k} -> {vals[k]}")

if errors:
    print("REQUIRED_INPUT_VALIDATION_FAIL")
    for e in errors:
        print("- " + e)
    sys.exit(1)

print("REQUIRED_INPUT_VALIDATION_PASS")
for k in sorted(REQUIRED):
    print(f"{k}={vals[k]}")
