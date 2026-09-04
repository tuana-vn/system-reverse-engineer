#!/usr/bin/env python3
from pathlib import Path
import sys, yaml
ROOT=Path(__file__).resolve().parents[2]
errors=[]
base=ROOT/'docs/METHODOLOGY_BASELINE.md'
if not base.is_file(): errors.append('missing docs/METHODOLOGY_BASELINE.md')
else:
    txt=base.read_text(encoding='utf-8')
    required=[
        '# METHODOLOGY_BASELINE','## 1. Agent Purpose','## 2. Agent Boundary','## 3. Core Methodology',
        '## 5. Mandatory Quality Targets','## 7. Failure Investigation and Earliest-Divergence Rule',
        '## 8. Requirement Fidelity and Source-Fact Promotion','## 9. Workflow Input and State Preconditions',
        '## 10. Methodology vs Execution Plumbing','## 11. Change-Control Rule',
        '## 12. Package Maintenance and Tooling Discipline','IMPLEMENTATION_READY','purpose_or_boundary_change = NO'
    ]
    for token in required:
        if token not in txt: errors.append('baseline missing required token: '+token)

pv=ROOT/'.ai-engineering/package-version.yaml'
try: version=str((yaml.safe_load(pv.read_text(encoding='utf-8')) or {}).get('package_version',''))
except Exception as exc:
    errors.append(f'cannot read package version: {exc}'); version=''
if version!='4.0': errors.append(f'active package version must be 4.0, found {version!r}')
if not (ROOT/'docs/PACKAGE_MAINTENANCE_RULES.md').is_file(): errors.append('missing docs/PACKAGE_MAINTENANCE_RULES.md')
for rel in ['.github/agents/system-reverse-engineer.agent.md','.github/copilot-instructions.md','.github/skills/run-engineering-workflow/SKILL.md','docs/AGENT_CONTEXT.md']:
    p=ROOT/rel
    if not p.is_file() or 'docs/METHODOLOGY_BASELINE.md' not in p.read_text(encoding='utf-8'):
        errors.append(f'normative baseline not referenced by {rel}')
if errors:
    print('METHODOLOGY_BASELINE_VALIDATION_FAIL')
    for e in errors: print('- '+e)
    sys.exit(1)
print('METHODOLOGY_BASELINE_VALIDATION_PASS')
print('version=4.0')
print('purpose_boundary_checkpoint=present')
