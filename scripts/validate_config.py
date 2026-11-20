#!/usr/bin/env python3
"""Validate GitHub Enterprise Cloud YAML configuration against schemas and policy guardrails."""

import glob
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: python3-yaml (PyYAML) is required to parse config/**/*.yaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)

errors = []
warnings = []

SECRET_KEYWORDS = [
    "SECRET",
    "PASSWORD",
    "PASSWD",
    "TOKEN",
    "API_KEY",
    "APIKEY",
    "PRIVATE_KEY",
    "CONNECTION_STRING",
    "CONN_STR",
    "CLIENT_SECRET",
    "PAT",
]


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
            return
        if "enum" in schema and data not in schema["enum"]:
            errors.append(f"{path_prefix}: boolean value '{data}' must be {schema['enum']}")
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


def validate_environments(envs, team_slugs, file_label, scope_label):
    for env in envs or []:
        if not isinstance(env, dict):
            continue
        ename = env.get("name", "")
        req_app = env.get("require_approval", False)
        approvers = env.get("approver_teams") or []
        if ename.lower() in {"prod", "production", "prd"} and req_app is not True:
            errors.append(
                f"[REPO-POLICY-004] {file_label} ({scope_label}): production environment '{ename}' must set require_approval: true"
            )
        if req_app is True and len(approvers) == 0:
            errors.append(
                f"[REPO-POLICY-005] {file_label} ({scope_label}): environment '{ename}' requires approval and must specify at least one team in approver_teams"
            )
        for team_slug in approvers:
            if team_slug not in team_slugs:
                errors.append(
                    f"[REPO-TEAM-REF] {file_label} ({scope_label}): environment '{ename}' approver_teams references unknown team slug '{team_slug}'"
                )


def main():
    enterprise_schema = load_json("schemas/enterprise.schema.json")
    org_schema = load_json("schemas/org.schema.json")
    teams_schema = load_json("schemas/teams.schema.json")
    domain_repos_schema = load_json("schemas/domain-repos.schema.json")

    # 1. Validate config/enterprise.yaml
    ent_path = "config/enterprise.yaml"
    if not os.path.isfile(ent_path):
        errors.append("Missing required enterprise configuration file: config/enterprise.yaml")
        return 1

    ent_data = load_yaml(ent_path)
    validate_against_schema(ent_data, enterprise_schema, ent_path)

    archetypes = (ent_data or {}).get("archetypes", {})
    for arch_name, arch in archetypes.items():
        if not isinstance(arch, dict):
            continue
        bp = arch.get("branch_protection", {})
        ms = arch.get("merge_strategies", {})
        if arch_name == "regulated-workload":
            if bp.get("min_reviewers", 0) < 3:
                errors.append(
                    f"[ENT-BASELINE-004] {ent_path}: archetype 'regulated-workload' must enforce min_reviewers >= 3"
                )
            if bp.get("require_signed_commits") is not True:
                errors.append(
                    f"[ENT-BASELINE-005] {ent_path}: archetype 'regulated-workload' must enforce require_signed_commits: true"
                )
        if not any(ms.get(k) for k in ("allow_squash_merge", "allow_merge_commit", "allow_rebase_merge")):
            errors.append(
                f"[ENT-BASELINE-006] {ent_path}: archetype '{arch_name}' must enable at least one merge strategy"
            )

    managed_orgs = (ent_data or {}).get("enterprise", {}).get("managed_organizations", [])
    ent_defaults = (ent_data or {}).get("enterprise_defaults") or {}
    ent_copilot = ent_defaults.get("copilot") or {}
    ent_codespaces = ent_defaults.get("codespaces") or {}
    ent_billing = ent_defaults.get("billing") or {}
    ent_allowed_skus = set(ent_codespaces.get("allowed_machine_types") or [])
    ent_max_idle = ent_codespaces.get("max_idle_timeout_minutes", 120)
    ent_max_retention = ent_codespaces.get("max_retention_period_days", 30)
    ent_max_budget = ent_billing.get("max_org_monthly_budget_usd", 50000)

    for rg in (ent_defaults.get("actions") or {}).get("runner_groups") or []:
        if isinstance(rg, dict):
            for sel_org in rg.get("selected_organizations") or []:
                if sel_org not in managed_orgs:
                    errors.append(
                        f"[ENT-RUNNER-ORG] {ent_path}: enterprise runner group '{rg.get('name')}' references unknown managed organization '{sel_org}'"
                    )
    discovered_org_dirs = sorted(
        os.path.basename(p) for p in glob.glob("config/orgs/*") if os.path.isdir(p)
    )

    for org_slug in managed_orgs:
        if org_slug not in discovered_org_dirs:
            errors.append(
                f"[ENT-ORG-MISSING] {ent_path}: managed organization '{org_slug}' is missing directory config/orgs/{org_slug}/"
            )
    for org_dir in discovered_org_dirs:
        if org_dir not in managed_orgs:
            errors.append(
                f"[ENT-ORG-UNREGISTERED] config/orgs/{org_dir}: organization directory is not registered in config/enterprise.yaml managed_organizations"
            )

    total_teams = 0
    total_domains = 0
    total_repos = 0

    # 2. Validate each Organization (org.yaml, teams.yaml, repos/*.yaml)
    for org_slug in discovered_org_dirs:
        org_dir_path = f"config/orgs/{org_slug}"
        org_yaml_path = f"{org_dir_path}/org.yaml"
        teams_yaml_path = f"{org_dir_path}/teams.yaml"

        if not os.path.isfile(org_yaml_path):
            errors.append(f"Missing required organization file: {org_yaml_path}")
            continue
        if not os.path.isfile(teams_yaml_path):
            errors.append(f"Missing required teams catalog file: {teams_yaml_path}")
            continue

        org_data = load_yaml(org_yaml_path)
        validate_against_schema(org_data, org_schema, org_yaml_path)

        if isinstance(org_data, dict):
            declared_slug = (org_data.get("organization") or {}).get("slug")
            if declared_slug != org_slug:
                errors.append(
                    f"[ORG-SLUG-MISMATCH] {org_yaml_path}: organization.slug '{declared_slug}' must match directory name '{org_slug}'"
                )
            merges = (org_data.get("repository_defaults") or {}).get("allowed_merge_types", {})
            if not any(merges.get(k) for k in ("squash", "merge_commit", "rebase")):
                errors.append(
                    f"[ORG-BASELINE-003] {org_yaml_path}: repository_defaults.allowed_merge_types must enable at least one merge strategy."
                )
            for rg in org_data.get("runner_groups", []):
                if rg.get("visibility") == "all":
                    warnings.append(
                        f"[ORG-BASELINE-WARN-001] {org_yaml_path}: runner group '{rg.get('name')}' has visibility='all'."
                    )

        # Validate teams.yaml
        teams_data = load_yaml(teams_yaml_path)
        validate_against_schema(teams_data, teams_schema, teams_yaml_path)

        team_slugs = set()
        teams_list = (teams_data or {}).get("teams", []) if isinstance(teams_data, dict) else []
        if isinstance(teams_data, dict) and teams_data.get("organization") != org_slug:
            errors.append(
                f"[TEAMS-ORG-MISMATCH] {teams_yaml_path}: organization '{teams_data.get('organization')}' must match directory '{org_slug}'"
            )

        for t in teams_list:
            if not isinstance(t, dict):
                continue
            tslug = t.get("slug")
            if tslug in team_slugs:
                errors.append(f"[TEAMS-DUPLICATE] {teams_yaml_path}: duplicate team slug '{tslug}'")
            team_slugs.add(tslug)
            total_teams += 1

        for t in teams_list:
            if not isinstance(t, dict):
                continue
            parent = t.get("parent_team")
            if parent:
                if parent == t.get("slug"):
                    errors.append(f"[TEAMS-SELF-PARENT] {teams_yaml_path}: team '{parent}' cannot be its own parent_team")
                elif parent not in team_slugs:
                    errors.append(
                        f"[TEAMS-UNKNOWN-PARENT] {teams_yaml_path}: team '{t.get('slug')}' references unknown parent_team '{parent}'"
                    )

        # Cross-file FinOps & Enterprise Ceiling checks on org.yaml (Copilot, Codespaces, Budgets)
        if isinstance(org_data, dict):
            copilot = org_data.get("copilot_dials") or {}
            codespaces = org_data.get("codespaces_dials") or {}
            budgets = org_data.get("billing_budgets") or []

            if copilot.get("enabled") is True:
                if ent_copilot.get("policy_mode") == "disabled":
                    errors.append(
                        f"[ORG-FINOPS-005] {org_yaml_path}: copilot_dials.enabled cannot be true while enterprise_defaults.copilot.policy_mode is 'disabled'."
                    )
                if copilot.get("seat_management") == "disabled":
                    errors.append(
                        f"[ORG-FINOPS-002] {org_yaml_path}: copilot_dials.enabled is true, so seat_management cannot be 'disabled'."
                    )
                if copilot.get("seat_management") == "assign_selected" and not (copilot.get("assigned_teams") or []):
                    errors.append(
                        f"[ORG-FINOPS-002] {org_yaml_path}: copilot_dials.seat_management is 'assign_selected' and requires at least one team in assigned_teams."
                    )
            for tslug in copilot.get("assigned_teams") or []:
                if tslug not in team_slugs:
                    errors.append(
                        f"[ORG-FINOPS-003] {org_yaml_path}: copilot_dials.assigned_teams references unknown team slug '{tslug}' (not in {teams_yaml_path})."
                    )

            if codespaces.get("enabled") is True:
                if ent_codespaces.get("policy_mode") == "disabled":
                    errors.append(
                        f"[ORG-FINOPS-005] {org_yaml_path}: codespaces_dials.enabled cannot be true while enterprise_defaults.codespaces.policy_mode is 'disabled'."
                    )
                if codespaces.get("access_policy") == "selected_members" and not (codespaces.get("allowed_teams") or []):
                    errors.append(
                        f"[ORG-FINOPS-002] {org_yaml_path}: codespaces_dials.access_policy is 'selected_members' and requires at least one team in allowed_teams."
                    )
                has_cs_cap = any(
                    isinstance(b, dict) and b.get("product_sku") == "codespaces" and b.get("prevent_further_usage") is True
                    for b in budgets
                )
                if not has_cs_cap:
                    errors.append(
                        f"[ORG-FINOPS-001] {org_yaml_path}: codespaces_dials.enabled is true, so billing_budgets must define a 'codespaces' budget with prevent_further_usage: true."
                    )
            for tslug in codespaces.get("allowed_teams") or []:
                if tslug not in team_slugs:
                    errors.append(
                        f"[ORG-FINOPS-003] {org_yaml_path}: codespaces_dials.allowed_teams references unknown team slug '{tslug}' (not in {teams_yaml_path})."
                    )
            for sku in codespaces.get("allowed_machine_types") or []:
                if ent_allowed_skus and sku not in ent_allowed_skus:
                    errors.append(
                        f"[ORG-FINOPS-004] {org_yaml_path}: codespaces_dials.allowed_machine_types includes '{sku}', which is not permitted by enterprise_defaults.codespaces.allowed_machine_types."
                    )
            if codespaces.get("default_idle_timeout_minutes", 0) > ent_max_idle:
                errors.append(
                    f"[ORG-FINOPS-004] {org_yaml_path}: codespaces_dials.default_idle_timeout_minutes exceeds enterprise ceiling ({ent_max_idle})."
                )
            if codespaces.get("default_retention_period_days", 0) > ent_max_retention:
                errors.append(
                    f"[ORG-FINOPS-004] {org_yaml_path}: codespaces_dials.default_retention_period_days exceeds enterprise ceiling ({ent_max_retention})."
                )

            for b in budgets:
                if isinstance(b, dict) and b.get("budget_amount_usd", 0) > ent_max_budget:
                    errors.append(
                        f"[ORG-FINOPS-004] {org_yaml_path}: billing_budgets entry for '{b.get('product_sku')}' (${b.get('budget_amount_usd')}) exceeds enterprise max_org_monthly_budget_usd (${ent_max_budget})."
                    )

        # Validate domain repository files in config/orgs/<org>/repos/*.yaml
        domain_files = sorted(glob.glob(f"{org_dir_path}/repos/*.yaml"))
        if not domain_files:
            errors.append(f"No domain repository files found in {org_dir_path}/repos/*.yaml")

        seen_repos_in_org = {}
        for df in domain_files:
            total_domains += 1
            ddata = load_yaml(df)
            validate_against_schema(ddata, domain_repos_schema, df)
            if not isinstance(ddata, dict):
                continue

            domain_meta = ddata.get("domain") or {}
            dkey = domain_meta.get("key", "<unknown>")
            expected_filename = f"{dkey}.yaml"
            if os.path.basename(df) != expected_filename:
                errors.append(
                    f"[DOMAIN-KEY-MISMATCH] {df}: domain.key '{dkey}' must match filename '{os.path.basename(df)}'"
                )
            if domain_meta.get("organization") != org_slug:
                errors.append(
                    f"[DOMAIN-ORG-MISMATCH] {df}: domain.organization '{domain_meta.get('organization')}' must match '{org_slug}'"
                )

            defaults = ddata.get("defaults") or {}
            default_arch = defaults.get("archetype", "standard-microservice")

            for ta in defaults.get("team_access") or []:
                if isinstance(ta, dict) and ta.get("team") not in team_slugs:
                    errors.append(
                        f"[REPO-TEAM-REF] {df} (defaults.team_access): references unknown team slug '{ta.get('team')}' (not in {teams_yaml_path})"
                    )

            validate_environments(defaults.get("environments"), team_slugs, df, "defaults.environments")

            for repo in ddata.get("repositories") or []:
                if not isinstance(repo, dict):
                    continue
                total_repos += 1
                rname = repo.get("name", "<unknown>")
                if rname in seen_repos_in_org:
                    errors.append(
                        f"[REPO-DUPLICATE] {df}: repository '{rname}' is already defined in {seen_repos_in_org[rname]} for organization '{org_slug}'"
                    )
                else:
                    seen_repos_in_org[rname] = df

                eff_arch = repo.get("archetype", default_arch)
                bp = repo.get("branch_protection") or {}
                if eff_arch == "regulated-workload":
                    min_rev = bp.get("min_reviewers", 3)
                    if min_rev < 3:
                        errors.append(
                            f"[REPO-POLICY-001] {df} (repo '{rname}'): regulated-workload requires branch_protection.min_reviewers >= 3 (got {min_rev})"
                        )
                    if bp.get("require_signed_commits", True) is not True:
                        errors.append(
                            f"[REPO-POLICY-002] {df} (repo '{rname}'): regulated-workload cannot disable branch_protection.require_signed_commits"
                        )

                sec = repo.get("security") or {}
                if eff_arch != "sandbox":
                    for sec_key in ("secret_scanning", "secret_scanning_push_protection", "dependabot_alerts"):
                        if sec.get(sec_key, True) is False:
                            errors.append(
                                f"[REPO-POLICY-003] {df} (repo '{rname}'): cannot disable security.{sec_key} on non-sandbox archetype '{eff_arch}'"
                            )

                ms = repo.get("merge_strategies")
                if isinstance(ms, dict):
                    if not any(ms.get(k) for k in ("allow_squash_merge", "allow_merge_commit", "allow_rebase_merge")):
                        errors.append(
                            f"[REPO-POLICY-006] {df} (repo '{rname}'): merge_strategies must enable at least one merge method"
                        )

                for ta in repo.get("team_access") or []:
                    if isinstance(ta, dict) and ta.get("team") not in team_slugs:
                        errors.append(
                            f"[REPO-TEAM-REF] {df} (repo '{rname}'): team_access references unknown team slug '{ta.get('team')}' (not in {teams_yaml_path})"
                        )

                for co in repo.get("codeowners_teams") or []:
                    if isinstance(co, dict):
                        for tslug in co.get("teams") or []:
                            if tslug not in team_slugs:
                                errors.append(
                                    f"[REPO-TEAM-REF] {df} (repo '{rname}'): codeowners_teams references unknown team slug '{tslug}' (not in {teams_yaml_path})"
                                )

                validate_environments(repo.get("environments"), team_slugs, df, f"repo '{rname}'")

                for vkey in (repo.get("environment_variables") or {}).keys():
                    ukey = vkey.upper()
                    for kw in SECRET_KEYWORDS:
                        if kw in ukey:
                            errors.append(
                                f"[REPO-POLICY-007] {df} (repo '{rname}'): environment_variables key '{vkey}' matches sensitive keyword '{kw}'. Use GitHub Encrypted Secrets / Azure Key Vault OIDC instead."
                            )

    for warning in warnings:
        print(f"  WARN: {warning}")

    if errors:
        for error in errors:
            print(f"  FAIL: {error}", file=sys.stderr)
        return 1

    print(
        f"  PASS: Validated config/enterprise.yaml, {len(discovered_org_dirs)} organization(s), "
        f"{total_teams} team(s), {total_domains} domain file(s), and {total_repos} repository definition(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
