#!/usr/bin/env python3
"""Validate YAML configuration against schemas and project policy guardrails."""

import glob
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: python3-yaml (PyYAML) is required to parse config/*.yaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)

errors = []
warnings = []


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_against_schema(data, schema, path_prefix):
    """Lightweight recursive JSON Schema validator supporting Draft-07 constraints."""
    schema_type = schema.get("type")
    if schema_type == "object":
        if not isinstance(data, dict):
            errors.append(f"{path_prefix}: expected object, got {type(data).__name__}")
            return
        for req in schema.get("required", []):
            if req not in data:
                errors.append(f"{path_prefix}: missing required property '{req}'")
        props = schema.get("properties", {})
        add_props = schema.get("additionalProperties", True)
        for k, v in data.items():
            sub_path = f"{path_prefix}.{k}"
            if k in props:
                validate_against_schema(v, props[k], sub_path)
            elif add_props is False:
                errors.append(f"{path_prefix}: unknown/unsupported dial property '{k}' (not allowed by schema)")
            elif isinstance(add_props, dict):
                validate_against_schema(v, add_props, sub_path)
    elif schema_type == "array":
        if not isinstance(data, list):
            errors.append(f"{path_prefix}: expected array, got {type(data).__name__}")
            return
        min_items = schema.get("minItems")
        if min_items is not None and len(data) < min_items:
            errors.append(f"{path_prefix}: array must have at least {min_items} item(s)")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(data):
                validate_against_schema(item, item_schema, f"{path_prefix}[{idx}]")
    elif schema_type == "integer":
        if not isinstance(data, int) or isinstance(data, bool):
            errors.append(f"{path_prefix}: expected integer, got {data!r}")
            return
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path_prefix}: value {data} is below minimum allowed bound ({schema['minimum']})")
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path_prefix}: value {data} exceeds maximum allowed bound ({schema['maximum']})")
    elif schema_type == "boolean":
        if not isinstance(data, bool):
            errors.append(f"{path_prefix}: expected boolean, got {data!r}")
    elif schema_type == "string":
        if not isinstance(data, str):
            errors.append(f"{path_prefix}: expected string, got {data!r}")
            return
        if "enum" in schema and data not in schema["enum"]:
            errors.append(f"{path_prefix}: value '{data}' must be one of {schema['enum']}")
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path_prefix}: string length ({len(data)}) is shorter than minLength ({schema['minLength']})")
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(f"{path_prefix}: string length ({len(data)}) exceeds maxLength ({schema['maxLength']})")
        if "pattern" in schema and not re.match(schema["pattern"], data):
            errors.append(f"{path_prefix}: value '{data}' does not match required pattern '{schema['pattern']}'")


def main():
    org_schema = load_json("schemas/org.schema.json")
    org_data = load_yaml("config/org.yaml")
    validate_against_schema(org_data, org_schema, "config/org.yaml")

    if isinstance(org_data, dict) and "repository_defaults" in org_data:
        merges = org_data["repository_defaults"].get("allowed_merge_types", {})
        if not any(merges.get(k) for k in ("squash", "no_fast_forward", "rebase", "rebase_merge")):
            errors.append("[ORG-BASELINE-003] config/org.yaml: repository_defaults.allowed_merge_types must enable at least one merge strategy.")
    for pool in org_data.get("agent_pools", []):
        if pool.get("auto_provision") is True:
            warnings.append(f"[ORG-BASELINE-WARN-001] config/org.yaml: agent pool '{pool.get('name')}' has auto_provision=true.")

    groups_schema = load_json("schemas/groups.schema.json")
    groups_data = load_yaml("config/groups.yaml")
    validate_against_schema(groups_data, groups_schema, "config/groups.yaml")

    identity_schema = load_json("schemas/identity-bootstrap.schema.json")
    identity_data = load_yaml("config/identity-bootstrap.yaml")
    validate_against_schema(identity_data, identity_schema, "config/identity-bootstrap.yaml")
    if isinstance(identity_data, dict):
        plan_group = identity_data.get("plan_group")
        if not isinstance(plan_group, dict):
            plan_group = {}
        apply_group = identity_data.get("apply_group")
        if not isinstance(apply_group, dict):
            apply_group = {}
        if (
            "display_name" in plan_group
            and "display_name" in apply_group
            and plan_group["display_name"] == apply_group["display_name"]
        ):
            errors.append("config/identity-bootstrap.yaml: plan_group and apply_group must have different display_name values")
        for field in ("member_object_ids", "owner_object_ids"):
            values = plan_group.get(field, [])
            if isinstance(values, list) and all(isinstance(value, str) for value in values) and len(values) != len(set(values)):
                errors.append(f"config/identity-bootstrap.yaml: plan_group.{field} must not contain duplicate object IDs")
        eligible_members = apply_group.get("eligible_member_object_ids", [])
        if (
            isinstance(eligible_members, list)
            and all(isinstance(value, str) for value in eligible_members)
            and len(eligible_members) != len(set(eligible_members))
        ):
            errors.append("config/identity-bootstrap.yaml: apply_group.eligible_member_object_ids must not contain duplicate object IDs")
        project_names = identity_data.get("plan_project_names", [])
        if (
            isinstance(project_names, list)
            and all(isinstance(value, str) for value in project_names)
            and len(project_names) != len(set(project_names))
        ):
            errors.append("config/identity-bootstrap.yaml: plan_project_names must not contain duplicate project names")

    project_schema = load_json("schemas/project.schema.json")
    secret_keywords = ["SECRET", "PASSWORD", "PASSWD", "TOKEN", "API_KEY", "APIKEY", "PRIVATE_KEY", "CONNECTION_STRING", "CONN_STR", "CLIENT_SECRET", "PAT"]

    project_files = sorted(glob.glob("config/projects/*.yaml"))
    for pf in project_files:
        pdata = load_yaml(pf)
        validate_against_schema(pdata, project_schema, pf)
        proj = (pdata or {}).get("project", {})
        pkey = proj.get("key", "<unknown>")
        expected_filename = f"{pkey}.yaml"
        if os.path.basename(pf) != expected_filename:
            errors.append(f"[PROJ-KEY-MISMATCH] {pf}: project.key '{pkey}' must match filename '{ os.path.basename(pf) }'")

        archetype = proj.get("archetype")
        dials = proj.get("branch_policy_dials", {})
        if archetype == "regulated-workload":
            min_rev = dials.get("min_reviewers", 2)
            if min_rev < 3:
                errors.append(f"[PROJ-POLICY-001] {pf}: regulated-workload requires branch_policy_dials.min_reviewers >= 3 (got {min_rev})")
            expiry = dials.get("build_validation_expiry_hours", 24)
            if expiry > 12:
                errors.append(f"[PROJ-POLICY-002] {pf}: regulated-workload requires build_validation_expiry_hours <= 12 (got {expiry})")

        team_names = {t.get("name") for t in proj.get("teams", []) if isinstance(t, dict)}
        for env in proj.get("environments", []):
            ename = env.get("name", "")
            req_app = env.get("require_approval", False)
            approver = env.get("approver_team", "")
            if ename.lower() in {"prod", "production", "prd"} and req_app is not True:
                errors.append(f"[PROJ-POLICY-003] {pf}: production environment '{ename}' must set require_approval: true")
            if req_app is True and not approver:
                errors.append(f"[PROJ-POLICY-004] {pf}: environment '{ename}' requires approval and must set approver_team")
            if approver and approver not in team_names:
                errors.append(f"[PROJ-POLICY-005] {pf}: environment '{ename}' references unknown approver_team '{approver}'")

        for repo in proj.get("repositories", []):
            for pr in repo.get("path_reviewers", []):
                tname = pr.get("team_name", "")
                if tname not in team_names:
                    errors.append(f"[PROJ-POLICY-006] {pf}: repo '{repo.get('name')}' path_reviewers references unknown team '{tname}'")

        if (proj.get("features") or {}).get("repositories") == "enabled":
            if not proj.get("create_default_repository", False) and len(proj.get("repositories") or []) == 0:
                errors.append(f"[PROJ-POLICY-008] {pf}: project with repositories enabled must either declare at least one repo in 'repositories' or set 'create_default_repository: true'")

        for vg in proj.get("variable_groups", []):
            for vkey in (vg.get("variables") or {}).keys():
                ukey = vkey.upper()
                for kw in secret_keywords:
                    if kw in ukey:
                        errors.append(f"[PROJ-POLICY-007] {pf}: variable group '{vg.get('name')}' contains plain-text variable '{vkey}' matching secret keyword '{kw}'. Use a key_vault block instead.")

    for warning in warnings:
        print(f"  WARN: {warning}")

    if errors:
        for error in errors:
            print(f"  FAIL: {error}", file=sys.stderr)
        return 1

    print(
        f"  PASS: Validated config/org.yaml, config/groups.yaml, "
        f"config/identity-bootstrap.yaml, and {len(project_files)} project file(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
