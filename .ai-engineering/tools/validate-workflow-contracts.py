#!/usr/bin/env python3
"""Validate deterministic workflow contracts for System Reverse Engineer 4.0."""
from pathlib import Path
import re, sys, yaml
ROOT=Path(__file__).resolve().parents[2]
WF_DIR=ROOT/'.ai-engineering/workflows'
RESOLVER='.ai-engineering/prompts/common/resolve-high-impact-unknowns.md'
RUNNER_RESERVED={'agent_package_version','blocking_artifact','blocking_qids','blocking_retry_step'}
TERMINAL={'DONE','BLOCKED'}
LOCAL_TOKENS={'verify','next_artifact','revise_current_dd','defer_current_artifact','design','resolve_dd_design_unknowns','resolve_dd_verification_unknowns'}
errors=[]; checked=0

def placeholders(text):
    return set(re.findall(r'\{\{([A-Za-z0-9_]+)\}\}', text or ''))

def prompt_statuses(path):
    if not path.is_file(): return None
    txt=path.read_text(encoding='utf-8')
    matches=re.findall(r'^\s*status:\s*(.+)$',txt,re.M)
    if not matches: return None
    raw=matches[-1].strip()
    return {x.strip().strip('`"\'') for x in raw.split('|') if x.strip()}

def skill_contract(name):
    p=ROOT/'.github/skills'/name/'SKILL.md'
    if not p.is_file(): return None
    txt=p.read_text(encoding='utf-8')
    m=re.search(r'<!-- workflow-status-contract:start -->\s*```yaml\s*(.*?)\s*```\s*<!-- workflow-status-contract:end -->',txt,re.S)
    if not m: return None
    vals=(yaml.safe_load(m.group(1)) or {}).get('emitted_statuses') or []
    return set(vals)

def walk_stage_nodes(node,path='steps',foreach_bindings=None):
    if isinstance(node,dict):
        fb=foreach_bindings
        if 'foreach' in node and isinstance(node['foreach'],dict):
            fb=set((node['foreach'].get('bindings') or {}).keys())
        if ('prompt' in node or 'child_workflow' in node or 'inline_instruction' in node) and isinstance(node.get('statuses'),dict):
            yield path,node,fb or set()
        for k,v in node.items():
            yield from walk_stage_nodes(v,f'{path}.{k}',fb)
    elif isinstance(node,list):
        for i,v in enumerate(node): yield from walk_stage_nodes(v,f'{path}[{i}]',foreach_bindings)

for wf_path in sorted(WF_DIR.glob('*.yaml')):
    try: wf=yaml.safe_load(wf_path.read_text(encoding='utf-8')) or {}
    except Exception as exc:
        errors.append(f'{wf_path.name}: YAML parse failed: {exc}'); continue
    if str(wf.get('version'))!='4.0': errors.append(f'{wf_path.name}: workflow version must be 4.0')
    if str(wf.get('state_path','')).lower().endswith('.md'): errors.append(f'{wf_path.name}: state_path must be YAML, not Markdown')
    raw=wf_path.read_text(encoding='utf-8')
    if re.search(r'agent_package_version\s*:\s*["\']?\d',raw):
        errors.append(f'{wf_path.name}: must not duplicate literal agent_package_version; runner injects package version')
    inp=wf.get('inputs') or {}
    available=set(inp.get('required') or [])|set(inp.get('optional') or [])|set((inp.get('defaults') or {}).keys())|RUNNER_RESERVED
    all_steps=set((wf.get('steps') or {}).keys())

    for stage_path,stage,foreach_vars in walk_stage_nodes(wf.get('steps',{})):
        checked+=1
        allowed=set(stage.get('statuses') or {})
        stage_available=available|set((stage.get('inputs') or {}).keys())|foreach_vars
        if 'prompt' in stage:
            pr=ROOT/stage['prompt']
            if not pr.is_file(): errors.append(f'{wf_path.name}:{stage_path}: missing prompt {stage["prompt"]}')
            else:
                used=placeholders(pr.read_text(encoding='utf-8'))
                missing=sorted(used-stage_available)
                if missing: errors.append(f'{wf_path.name}:{stage_path}: unresolved prompt variables {missing}')
                declared=prompt_statuses(pr)
                if declared is not None and declared!=allowed:
                    errors.append(f'{wf_path.name}:{stage_path}: prompt/workflow status mismatch prompt-only={sorted(declared-allowed)} workflow-only={sorted(allowed-declared)}')
            for sk in stage.get('skills') or []:
                sp=ROOT/'.github/skills'/sk/'SKILL.md'
                if not sp.is_file(): errors.append(f'{wf_path.name}:{stage_path}: missing skill {sk}')
                emitted=skill_contract(sk)
                if emitted is not None and emitted-allowed:
                    errors.append(f'{wf_path.name}:{stage_path}: skill {sk} emits unrouted statuses {sorted(emitted-allowed)}')
            if stage.get('prompt')==RESOLVER:
                keys=set((stage.get('inputs') or {}).keys())
                req={'blocking_artifact','blocking_qids','retry_step'}
                if keys!=req: errors.append(f'{wf_path.name}:{stage_path}: resolver must bind exactly {sorted(req)}')
                exp={'blocking_artifact':'{{blocking_artifact}}','blocking_qids':'{{blocking_qids}}','retry_step':'{{blocking_retry_step}}'}
                if stage.get('inputs')!=exp: errors.append(f'{wf_path.name}:{stage_path}: resolver bindings must come from persisted runner state')
        if 'prompt' not in stage:
            for sk in stage.get('skills') or []:
                sp=ROOT/'.github/skills'/sk/'SKILL.md'
                if not sp.is_file(): errors.append(f'{wf_path.name}:{stage_path}: missing skill {sk}')

        if 'child_workflow' in stage:
            cp=ROOT/stage['child_workflow']
            if not cp.is_file(): errors.append(f'{wf_path.name}:{stage_path}: missing child workflow {stage["child_workflow"]}')
            else:
                child=yaml.safe_load(cp.read_text(encoding='utf-8')) or {}
                child_req=set(((child.get('inputs') or {}).get('required') or []))
                bound=set((stage.get('inputs') or {}).keys())
                missing=sorted(child_req-bound)
                if missing: errors.append(f'{wf_path.name}:{stage_path}: child required inputs not bound {missing}')
            if ((stage.get('execution') or {}).get('execution_mode')=='fresh' and not (stage.get('execution') or {}).get('ignore_previous_completion')):
                errors.append(f'{wf_path.name}:{stage_path}: fresh child workflow must ignore previous completion')
        # Validate placeholders in outputs and child input values.
        vals=[]
        if stage.get('output'): vals.append(stage['output'])
        vals.extend(v for v in (stage.get('inputs') or {}).values() if isinstance(v,str))
        for val in vals:
            miss=placeholders(val)-stage_available
            if miss: errors.append(f'{wf_path.name}:{stage_path}: unresolved stage variables {sorted(miss)} in {val}')
        # Top-level transitions only.
        if stage_path.count('.')==1:
            for status,target in (stage.get('statuses') or {}).items():
                if isinstance(target,str) and target not in all_steps and target not in TERMINAL and target not in LOCAL_TOKENS:
                    errors.append(f'{wf_path.name}:{stage_path}: unknown transition target {target!r} for {status}')

    # Foreach binding integrity.
    for name,step in (wf.get('steps') or {}).items():
        fe=step.get('foreach') if isinstance(step,dict) else None
        if not isinstance(fe,dict): continue
        bindings=fe.get('bindings') or {}
        for var,b in bindings.items():
            if not isinstance(b,dict) or not b.get('field'): errors.append(f'{wf_path.name}:steps.{name}: invalid foreach binding {var}')
            tr=b.get('transform')
            if tr not in (None,'slugify'): errors.append(f'{wf_path.name}:steps.{name}: unsupported foreach transform {tr!r}')

if errors:
    print('WORKFLOW_CONTRACT_VALIDATION_FAIL'); print(f'managed_stages_checked={checked}')
    for e in errors: print('\n- '+e)
    sys.exit(1)
print('WORKFLOW_CONTRACT_VALIDATION_PASS')
print(f'managed_stages_checked={checked}')
print('resolver_bindings=validated')
print('child_workflows=validated')
print('prompt_variables=validated')
print('foreach_bindings=validated')
