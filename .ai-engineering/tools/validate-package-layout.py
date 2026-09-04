#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml

parser = argparse.ArgumentParser(description='Validate System Reverse Engineer package layout.')
parser.add_argument('--strict-package-root', action='store_true')
args = parser.parse_args()

ROOT = Path(__file__).resolve().parents[2]
required_root_dirs={'.ai-engineering','.github','docs'}
required_root_files={'README.md','SECURITY.md','LICENSE'}
required=required_root_dirs|required_root_files
errors=[]
actual={p.name for p in ROOT.iterdir()}
missing=sorted(required-actual)
if missing: errors.append('missing required package root entries: '+', '.join(missing))
if args.strict_package_root:
    unexpected=sorted(actual-required)
    if unexpected: errors.append('unexpected root entries in strict package-root mode: '+', '.join(unexpected))

pv=ROOT/'.ai-engineering/package-version.yaml'
if not pv.is_file():
    errors.append('missing .ai-engineering/package-version.yaml')
    version=''
else:
    try:
        data=yaml.safe_load(pv.read_text(encoding='utf-8')) or {}
        version=str(data.get('package_version','')).strip()
    except Exception as exc:
        errors.append(f'package-version YAML parse failed: {exc}')
        version=''
if version!='4.0': errors.append(f'package_version must be 4.0, found {version!r}')

for rel in [
    'docs/METHODOLOGY_BASELINE.md',
    'docs/package/VERSION.txt',
    'docs/package/4.0_MANIFEST.json',
    '.ai-engineering/tools/validate-reverse-engineering-quality.py',
    '.github/skills/architecture-reconstruction-and-diagrams/SKILL.md',
    '.github/skills/current-state-tdd-synthesis/SKILL.md',
]:
    if not (ROOT/rel).is_file(): errors.append(f'missing required package file: {rel}')

vtxt=(ROOT/'docs/package/VERSION.txt')
if vtxt.is_file() and vtxt.read_text(encoding='utf-8').strip()!='4.0':
    errors.append('docs/package/VERSION.txt must contain exactly 4.0')

for forbidden in ['docs/archive','docs/releases','docs/run-prompts']:
    if (ROOT/forbidden).exists(): errors.append(f'historical package material must not be delivered: {forbidden}')

# Active package must contain no stale package-style V-labels.
import re
version_token_re=re.compile(r"(?i)(?<![A-Za-z0-9])V(\d+(?:\.\d+){0,3})(?![0-9.])")
def stale_token(text):
    for m in version_token_re.finditer(text):
        if m.group(1) != '4.0':
            return m.group(0)
    return None
for path in ROOT.rglob('*'):
    if not path.is_file():
        continue
    rel=path.relative_to(ROOT).as_posix()
    stale=stale_token(rel)
    if stale:
        errors.append(f'stale version label {stale!r} in path: {rel}')
    if path.suffix.lower() in {'.md','.yaml','.yml','.py','.json','.txt'} and rel != 'docs/package/4.0_MANIFEST.json':
        try:
            text=path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        stale=stale_token(text)
        if stale:
            errors.append(f'stale version label {stale!r} in {rel}')

if errors:
    print('PACKAGE_LAYOUT_VALIDATION_FAIL')
    for e in errors: print('- '+e)
    sys.exit(1)
print('PACKAGE_LAYOUT_VALIDATION_PASS')
print('mode='+('strict-package-root' if args.strict_package_root else 'repository-overlay'))
print('package_version=4.0')
