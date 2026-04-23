#!/usr/bin/env python3
"""Generate AAP template reference and Ansible role reference docs."""
import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
COLLECTIONS_ROOT = REPO_ROOT / "collections" / "ansible_collections" / "osac"
CONTROLLER_YML = COLLECTIONS_ROOT / "config_as_code" / "roles" / "aap" / "vars" / "controller.yml"
AAP_TEMPLATES_MD = REPO_ROOT / "docs" / "reference" / "aap-templates.md"
ANSIBLE_ROLES_MD = REPO_ROOT / "docs" / "reference" / "ansible-roles.md"

OSAC_COLLECTIONS = [
    "service",
    "templates",
    "config_as_code",
    "workflows",
    "test_overrides",
]

BEGIN_MARKER = "<!-- {key} -->"
END_MARKER = "<!-- /{key} -->"


def escape_jinja(value: str) -> str:
    """Escape Jinja2 expressions so MkDocs doesn't interpret them."""
    if not isinstance(value, str):
        return value
    # Named variable patterns: {{ var }} -> <var>
    value = re.sub(r"\{\{\s*(\w+)\s*\}\}", r"<\1>", value)
    # Remaining {{ }} (filter expressions, etc.)
    value = value.replace("{{", "&#123;&#123;").replace("}}", "&#125;&#125;")
    return value


def escape_value(value) -> str:
    """Escape a value for markdown table display."""
    if value is None:
        return ""
    s = str(value)
    s = escape_jinja(s)
    # Escape pipe characters that would break markdown tables
    s = s.replace("|", "\\|")
    # Collapse newlines for table cells
    s = s.replace("\n", " ").strip()
    return s


def replace_marker(content: str, key: str, replacement: str) -> str:
    """Replace content between HTML comment markers."""
    begin = BEGIN_MARKER.format(key=key)
    end = END_MARKER.format(key=key)
    pattern = re.compile(
        re.escape(begin) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    new_block = f"{begin}\n{replacement}\n{end}"
    result, count = pattern.subn(new_block, content)
    if count == 0:
        raise ValueError(f"Marker pair not found: {key!r}")
    return result


def load_yaml_safe(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# AAP template reference
# ---------------------------------------------------------------------------

def _template_table(templates: list) -> str:
    if not templates:
        return "_None defined._\n"
    rows = ["| Name | Playbook | Inventory | Instance Group |",
            "|------|----------|-----------|----------------|"]
    for t in templates:
        name = escape_value(t.get("name", ""))
        playbook = escape_value(t.get("playbook", ""))
        inventory = escape_value(t.get("inventory", ""))
        igs = t.get("instance_groups", [])
        ig = escape_value(", ".join(igs) if igs else "")
        rows.append(f"| {name} | {playbook} | {inventory} | {ig} |")
    return "\n".join(rows) + "\n"


def _workflow_table(workflows: list) -> str:
    if not workflows:
        return "_None defined._\n"
    rows = ["| Name | Description | Nodes |",
            "|------|-------------|-------|"]
    for w in workflows:
        name = escape_value(w.get("name", ""))
        desc = escape_value(w.get("description", ""))
        nodes = w.get("workflow_nodes", [])
        node_names = [escape_value(n.get("identifier", "")) for n in nodes]
        rows.append(f"| {name} | {desc} | {', '.join(node_names)} |")
    return "\n".join(rows) + "\n"


def _categorise_templates(templates: list):
    """Split templates into logical categories by name suffix."""
    cluster = []
    compute = []
    networking = []
    other = []
    for t in templates:
        name = t.get("name", "")
        # Strip prefix placeholder for matching
        suffix = re.sub(r"^<[^>]+>-", "", name)
        if any(k in suffix for k in ("hosted-cluster", "cluster-post-install", "config-as-code",
                                     "publish-templates", "report-hosted-cluster")):
            cluster.append(t)
        elif "compute-instance" in suffix:
            compute.append(t)
        elif any(k in suffix for k in ("virtual-network", "subnet", "security-group",
                                        "public-ip-pool")):
            networking.append(t)
        else:
            other.append(t)
    return cluster, compute, networking, other


def generate_aap_templates_content(data: dict) -> dict:
    """Return {marker_key: markdown_block} for aap-templates.md."""
    templates = data.get("controller_templates", [])
    workflows = data.get("controller_workflows", [])

    cluster, compute, networking, other = _categorise_templates(templates)

    return {
        "aap:cluster-templates": _template_table(cluster),
        "aap:compute-templates": _template_table(compute),
        "aap:networking-templates": _template_table(networking),
        "aap:other-templates": _template_table(other) if other else "_None._\n",
        "aap:workflows": _workflow_table(workflows),
    }


# ---------------------------------------------------------------------------
# Ansible role reference
# ---------------------------------------------------------------------------

def _param_table(options: dict) -> str:
    if not options:
        return "_No parameters._\n"
    rows = ["| Parameter | Type | Required | Default | Description |",
            "|-----------|------|----------|---------|-------------|"]
    for param, spec in sorted(options.items()):
        if not isinstance(spec, dict):
            continue
        ptype = escape_value(spec.get("type", ""))
        required = "yes" if spec.get("required") else "no"
        default = escape_value(spec.get("default", ""))
        desc = escape_value(spec.get("description", ""))
        rows.append(f"| `{param}` | {ptype} | {required} | {default} | {desc} |")
        # Show nested options inline
        sub_options = spec.get("options", {})
        if sub_options and isinstance(sub_options, dict):
            for sub_param, sub_spec in sorted(sub_options.items()):
                if not isinstance(sub_spec, dict):
                    continue
                sp_type = escape_value(sub_spec.get("type", ""))
                sp_req = "yes" if sub_spec.get("required") else "no"
                sp_default = escape_value(sub_spec.get("default", ""))
                sp_desc = escape_value(sub_spec.get("description", ""))
                rows.append(
                    f"| &nbsp;&nbsp;`{param}.{sub_param}` | {sp_type} | {sp_req} | {sp_default} | {sp_desc} |"
                )
    return "\n".join(rows) + "\n"


def generate_roles_content_for_collection(collection: str) -> str:
    """Generate markdown for all roles in an osac.* collection."""
    roles_dir = COLLECTIONS_ROOT / collection / "roles"
    if not roles_dir.exists():
        return ""

    sections = []
    for role_dir in sorted(roles_dir.iterdir()):
        if not role_dir.is_dir():
            continue
        spec_file = role_dir / "meta" / "argument_specs.yaml"
        if not spec_file.exists():
            continue
        data = load_yaml_safe(spec_file)
        if not data or "argument_specs" not in data:
            continue
        specs = data["argument_specs"]

        role_name = role_dir.name
        sections.append(f"#### `osac.{collection}.{role_name}`\n")

        for entrypoint, ep_spec in specs.items():
            if not isinstance(ep_spec, dict):
                continue
            options = ep_spec.get("options", {}) or {}
            if entrypoint == "main":
                sections.append(_param_table(options))
            else:
                sections.append(f"**Entrypoint: `{entrypoint}`**\n\n{_param_table(options)}")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------

def update_file(path: Path, markers: dict, check: bool) -> bool:
    """
    Inject content into marker regions.
    Returns True if the file was or would be changed.
    """
    original = path.read_text(encoding="utf-8")
    updated = original
    for key, content in markers.items():
        updated = replace_marker(updated, key, content)

    changed = updated != original
    if not check:
        if changed:
            path.write_text(updated, encoding="utf-8")
    return changed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AAP documentation.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if generated content differs from committed files.",
    )
    args = parser.parse_args()

    errors = []

    # --- aap-templates.md ---
    controller_data = load_yaml_safe(CONTROLLER_YML)
    template_markers = generate_aap_templates_content(controller_data)
    try:
        changed = update_file(AAP_TEMPLATES_MD, template_markers, args.check)
        if args.check and changed:
            errors.append(f"{AAP_TEMPLATES_MD} is stale — run 'make docs-generate' to update.")
    except ValueError as exc:
        errors.append(f"aap-templates.md: {exc}")

    # --- ansible-roles.md ---
    roles_markers = {}
    for col in OSAC_COLLECTIONS:
        key = f"roles:osac.{col}"
        roles_markers[key] = generate_roles_content_for_collection(col)

    try:
        changed = update_file(ANSIBLE_ROLES_MD, roles_markers, args.check)
        if args.check and changed:
            errors.append(f"{ANSIBLE_ROLES_MD} is stale — run 'make docs-generate' to update.")
    except ValueError as exc:
        errors.append(f"ansible-roles.md: {exc}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
