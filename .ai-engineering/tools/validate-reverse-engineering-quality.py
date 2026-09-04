#!/usr/bin/env python3
"""Structural and semantic consumer-quality validation for full reverse-engineering output."""

from pathlib import Path
import argparse
import re
import sys


REQUIRED_DIAGRAMS = [
    "diagrams/01_system_context.md",
    "diagrams/02_component_architecture.md",
    "diagrams/03_primary_runtime_sequence.md",
    "diagrams/04_integration_boundaries.md",
    "diagrams/05_state_persistence_lifecycle.md",
]

REQUIRED_MODELS = [
    "models/component_catalog.md",
    "models/runtime_flow_catalog.md",
    "models/integration_catalog.md",
    "models/configuration_model.md",
    "models/persistence_state_model.md",
]

REQUIRED_TDD_SECTIONS = [
    "System Context",
    "Architecture Overview",
    "Component Responsibilities",
    "Runtime Entry Points",
    "Primary Runtime Flows",
    "Integration Architecture",
    "Persistence and State Ownership",
    "Background Processing and Lifecycle",
    "Configuration and Runtime Selection",
    "Error, Retry, and Fallback Behavior",
    "Security Boundaries",
    "Observability",
    "Build and Runtime Model",
    "Critical Current-System Rules",
    "Runtime Variants and Alternate Paths",
    "Known Unknowns and External Blockers",
    "Evidence and Diagram Index",
]

MANDATORY_DIAGRAM_TYPES = {
    "01_system_context.md": ("graph", "flowchart"),
    "02_component_architecture.md": ("graph", "flowchart"),
    "03_primary_runtime_sequence.md": ("sequenceDiagram",),
    "04_integration_boundaries.md": ("graph", "flowchart"),
    "05_state_persistence_lifecycle.md": ("stateDiagram-v2", "flowchart", "graph"),
}


def extract_mermaid_blocks(markdown_text):
    return re.findall(r"```mermaid\s*\n(.*?)```", markdown_text, flags=re.S | re.I)


def validate_mermaid_syntax_sanity(markdown_text, source_name):
    errors = []
    blocks = extract_mermaid_blocks(markdown_text)

    for idx, block in enumerate(blocks, start=1):
        stripped = block.strip()
        first = stripped.splitlines()[0].strip() if stripped else ""
        label = f"{source_name}#mermaid-{idx}"

        if re.match(r"^(graph|flowchart)\b", first):
            if "->>" in block or "-->>" in block:
                errors.append(
                    f"MERMAID_SYNTAX_MIX: {label}: "
                    "graph/flowchart contains sequence-diagram operator ->> or -->>"
                )

        if first == "sequenceDiagram":
            for line_no, raw in enumerate(block.splitlines(), start=1):
                line = raw.strip()
                if not line or line.startswith("%%") or line.startswith("participant "):
                    continue

                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*(\[|\(|\{)", line):
                    errors.append(
                        f"MERMAID_SYNTAX_MIX: {label}:{line_no}: "
                        "sequenceDiagram contains flowchart-style node declaration"
                    )

                if re.search(
                    r"(?:->>|-->>)\s*[A-Za-z_][A-Za-z0-9_]*\s*:\s*$",
                    line,
                ):
                    errors.append(
                        f"MERMAID_EMPTY_MESSAGE: {label}:{line_no}: "
                        "sequence message has ':' but no message text"
                    )

    return errors


def run_mermaid_syntax_sanity(root):
    errors = []
    for md in Path(root).rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "```mermaid" in text.lower():
            errors.extend(validate_mermaid_syntax_sanity(text, str(md)))
    return errors


def validate_mandatory_diagram_semantics(root):
    errors = []
    diagram_dir = Path(root) / "diagrams"

    for filename, allowed in MANDATORY_DIAGRAM_TYPES.items():
        path = diagram_dir / filename
        if not path.exists():
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        blocks = extract_mermaid_blocks(text)
        if not blocks:
            continue

        first_line = blocks[0].strip().splitlines()[0].strip() if blocks[0].strip() else ""
        declared = first_line.split()[0] if first_line else ""

        if declared not in allowed:
            errors.append(
                "MERMAID_SEMANTIC_TYPE_MISMATCH: "
                f"{path}: expected one of {allowed}, found {declared or '<empty>'}"
            )

    return errors


def validate_structure(root):
    errors = []
    mermaid_count = 0
    tdd = root / "CURRENT_STATE_TDD.md"

    if not root.exists():
        errors.append(f"artifact root missing: {root}")
        return errors, mermaid_count

    if not tdd.is_file():
        errors.append("missing CURRENT_STATE_TDD.md")
    else:
        text = tdd.read_text(encoding="utf-8", errors="replace")
        for section in REQUIRED_TDD_SECTIONS:
            if not re.search(
                r"^##\s+(?:\d+\.\s+)?" + re.escape(section) + r"\s*$",
                text,
                re.M | re.I,
            ):
                errors.append(f"TDD missing required section: {section}")

        for diagram in REQUIRED_DIAGRAMS:
            if diagram not in text and Path(diagram).name not in text:
                errors.append(f"TDD does not reference mandatory diagram: {diagram}")

    for rel in REQUIRED_DIAGRAMS:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing mandatory diagram: {rel}")
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        block_count = len(extract_mermaid_blocks(text))
        if block_count == 0:
            errors.append(f"mandatory diagram has no Mermaid block: {rel}")
        else:
            mermaid_count += block_count

        if not re.search(r"^##\s+Evidence Anchors\s*$", text, re.M | re.I):
            errors.append(f"mandatory diagram missing Evidence Anchors section: {rel}")

        evidence = text.split("Evidence Anchors", 1)[-1]
        if not re.search(
            r"(?m)^\s*[-*]\s+`?[^\n`]+\."
            r"(?:java|cs|c|cc|cpp|cxx|h|hpp|py|xml|yaml|yml|json|properties|gradle|toml|ini|sql|conf|config)\b",
            evidence,
            re.I,
        ):
            errors.append(f"mandatory diagram lacks concrete repo-relative evidence anchor: {rel}")

    for rel in REQUIRED_MODELS:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing canonical model artifact: {rel}")
        elif len(path.read_text(encoding="utf-8", errors="replace").strip()) < 200:
            errors.append(f"canonical model artifact too thin (<200 chars): {rel}")

    component_catalog = root / "models/component_catalog.md"
    if component_catalog.is_file():
        low = component_catalog.read_text(encoding="utf-8", errors="replace").lower()
        for token in [
            "responsibility",
            "inputs",
            "outputs",
            "dependencies",
            "state",
            "failure",
            "selection",
            "evidence",
        ]:
            if token not in low:
                errors.append(f"component catalog missing modeling dimension: {token}")

    if mermaid_count < 5:
        errors.append(f"mandatory Mermaid coverage insufficient: {mermaid_count}/5")

    return errors, mermaid_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", default="docs/reverse-engineering")
    args = parser.parse_args()

    root = Path(args.artifact_root)

    errors, mermaid_count = validate_structure(root)

    # IMPORTANT: syntax and semantic Mermaid validators are part of the
    # authoritative main validation flow. They are not dead helper functions.
    errors.extend(run_mermaid_syntax_sanity(root))
    errors.extend(validate_mandatory_diagram_semantics(root))

    if errors:
        print("REVERSE_ENGINEERING_QUALITY_VALIDATION_FAIL")
        print(f"mandatory_mermaid_count={mermaid_count}/5")
        for error in errors:
            print("- " + error)
        sys.exit(1)

    print("REVERSE_ENGINEERING_QUALITY_VALIDATION_PASS")
    print("mandatory_mermaid_count=5/5")
    print("canonical_tdd=CURRENT_STATE_TDD.md")
    print("canonical_models=5/5")


if __name__ == "__main__":
    main()
