#!/usr/bin/env python3
"""Offline regression tests for GitHub inventory extraction and domain candidate generation."""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import generate_config_candidates as gen  # noqa: E402
import export_github_inventory as exp  # noqa: E402
import generate_imports as gen_imports  # noqa: E402
import validate_config as val  # noqa: E402
import urllib.error  # noqa: E402


SAMPLE_INVENTORY = {
    "schema_version": "1.0",
    "exported_at": "2026-11-18T06:00:00Z",
    "organization": {
        "slug": "taswater-core",
        "name": "TasWater Core Engineering",
        "description": "Core platform and integration services.",
        "billing_email": "cloud-platform@taswater.com.au",
        "default_repository_permission": "none",
        "members_can_create_public_repositories": False,
        "members_can_create_private_repositories": False,
        "members_can_create_internal_repositories": False,
        "members_can_fork_private_repositories": False,
        "web_commit_signoff_required": False,
    },
    "teams": [
        {
            "slug": "platform-admins",
            "name": "Platform Admins",
            "description": "Enterprise platform administrators.",
            "privacy": "closed",
            "idp_group_id": "11111111-1111-1111-1111-111111111101",
        },
        {
            "slug": "security-auditors",
            "name": "Security Auditors",
            "description": "Read-only security auditors.",
            "privacy": "closed",
        },
        {
            "slug": "billing-maintainers",
            "name": "Billing Maintainers",
            "description": "Technical leads for billing services.",
            "privacy": "closed",
        },
        {
            "slug": "billing-developers",
            "name": "Billing Developers",
            "description": "Contributors for billing services.",
            "privacy": "secret",
            "parent_slug": "billing-maintainers",
        },
        {
            "slug": "scada-telemetry-maintainers",
            "name": "SCADA Telemetry Maintainers",
            "description": "Leads for SCADA and OT telemetry workloads.",
            "privacy": "closed",
        },
    ],
    "repositories": [
        {
            "name": "invoice-worker",
            "description": "Processes customer invoice batches.",
            "archived": False,
            "visibility": "private",
            "default_branch": "main",
            "topics": ["billing"],
            "features": {
                "has_issues": True,
                "has_wiki": False,
                "has_discussions": False,
                "has_projects": False,
            },
            "merge_strategies": {
                "allow_squash_merge": True,
                "allow_merge_commit": True,
                "allow_rebase_merge": False,
                "allow_auto_merge": True,
                "delete_branch_on_merge": True,
            },
            "branch_protection": {
                "protected": True,
                "min_reviewers": 2,
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": True,
                "require_last_push_approval": True,
                "require_conversation_resolution": True,
                "require_signed_commits": False,
                "require_linear_history": False,
                "required_status_checks": ["ci / test"],
            },
            "security": {
                "dependabot_alerts": True,
                "secret_scanning": True,
                "secret_scanning_push_protection": True,
            },
            "team_permissions": [
                {"team_slug": "billing-developers", "permission": "push"},
                {"team_slug": "billing-maintainers", "permission": "admin"},
                {"team_slug": "security-auditors", "permission": "pull"},
            ],
            "environments": [
                {"name": "prod", "require_approval": False, "approver_teams": []}
            ],
            "autolinks": [
                {
                    "id": 42,
                    "key_prefix": "PPLCTNS-",
                    "url_template": "https://taswater-applications.atlassian.net/browse/PPLCTNS-<num>",
                    "is_alphanumeric": False,
                }
            ],
        },
        {
            "name": "payment-pci-vault",
            "description": "PCI-regulated card tokenization service.",
            "archived": False,
            "visibility": "private",
            "default_branch": "main",
            "topics": ["pci", "billing"],
            "features": {
                "has_issues": True,
                "has_wiki": False,
                "has_discussions": False,
                "has_projects": False,
            },
            "merge_strategies": {
                "allow_squash_merge": True,
                "allow_merge_commit": False,
                "allow_rebase_merge": False,
                "allow_auto_merge": False,
                "delete_branch_on_merge": True,
            },
            "branch_protection": {
                "protected": False,
                "min_reviewers": 0,
                "dismiss_stale_reviews": False,
                "require_code_owner_reviews": False,
                "require_last_push_approval": False,
                "require_conversation_resolution": False,
                "require_signed_commits": False,
                "require_linear_history": False,
                "required_status_checks": [],
            },
            "security": {
                "dependabot_alerts": True,
                "secret_scanning": True,
                "secret_scanning_push_protection": True,
            },
            "team_permissions": [
                {"team_slug": "billing-developers", "permission": "push"},
                {"team_slug": "billing-maintainers", "permission": "maintain"},
            ],
            "environments": [],
        },
        {
            "name": "gis-viewer-api",
            "description": "Backend API for GIS spatial asset viewer.",
            "archived": False,
            "visibility": "private",
            "default_branch": "master",
            "topics": [],
            "features": {
                "has_issues": True,
                "has_wiki": False,
                "has_discussions": False,
                "has_projects": False,
            },
            "merge_strategies": {
                "allow_squash_merge": True,
                "allow_merge_commit": True,
                "allow_rebase_merge": False,
                "allow_auto_merge": False,
                "delete_branch_on_merge": True,
            },
            "branch_protection": {
                "protected": True,
                "min_reviewers": 1,
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "require_last_push_approval": False,
                "require_conversation_resolution": False,
                "require_signed_commits": False,
                "require_linear_history": False,
                "required_status_checks": [],
            },
            "security": {
                "dependabot_alerts": True,
                "secret_scanning": True,
                "secret_scanning_push_protection": True,
            },
            "team_permissions": [
                {"team_slug": "security-auditors", "permission": "pull"}
            ],
            "environments": [],
        },
        {
            "name": "gis-viewer-web",
            "description": "Frontend map portal for GIS spatial asset viewer.",
            "archived": False,
            "visibility": "public",
            "default_branch": "main",
            "topics": [],
            "features": {
                "has_issues": True,
                "has_wiki": False,
                "has_discussions": False,
                "has_projects": False,
            },
            "merge_strategies": {
                "allow_squash_merge": True,
                "allow_merge_commit": True,
                "allow_rebase_merge": False,
                "allow_auto_merge": False,
                "delete_branch_on_merge": True,
            },
            "branch_protection": {
                "protected": True,
                "min_reviewers": 2,
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": True,
                "require_last_push_approval": True,
                "require_conversation_resolution": True,
                "require_signed_commits": False,
                "require_linear_history": False,
                "required_status_checks": [],
            },
            "security": {
                "dependabot_alerts": True,
                "secret_scanning": True,
                "secret_scanning_push_protection": True,
            },
            "team_permissions": [
                {"team_slug": "security-auditors", "permission": "pull"}
            ],
            "environments": [],
        },
        {
            "name": "legacy-soap-adapter",
            "description": "Retired SOAP adapter from 2019.",
            "archived": True,
            "visibility": "private",
            "default_branch": "master",
            "topics": [],
            "features": {
                "has_issues": False,
                "has_wiki": False,
                "has_discussions": False,
                "has_projects": False,
            },
            "merge_strategies": {
                "allow_squash_merge": True,
                "allow_merge_commit": True,
                "allow_rebase_merge": False,
                "allow_auto_merge": False,
                "delete_branch_on_merge": True,
            },
            "branch_protection": {
                "protected": False,
                "min_reviewers": 0,
                "dismiss_stale_reviews": False,
                "require_code_owner_reviews": False,
                "require_last_push_approval": False,
                "require_conversation_resolution": False,
                "require_signed_commits": False,
                "require_linear_history": False,
                "required_status_checks": [],
            },
            "security": {
                "dependabot_alerts": False,
                "secret_scanning": False,
                "secret_scanning_push_protection": False,
            },
            "team_permissions": [],
            "environments": [],
        },
    ],
}


def main():
    val.errors.clear()

    # 1. Validate sample inventory against schemas/organization-inventory.schema.json
    inv_schema = val.load_json(str(REPO_ROOT / "schemas/organization-inventory.schema.json"))
    val.validate_against_schema(SAMPLE_INVENTORY, inv_schema, "sample_inventory")
    if val.errors:
        print(f"  FAIL: Sample inventory failed schema validation: {val.errors}", file=sys.stderr)
        return 1

    # 2. Generate candidates and verify domain deduction
    result = gen.generate_candidates(SAMPLE_INVENTORY, include_archived=False)

    # Archived repo should be skipped
    assert result["archived_skipped"] == ["legacy-soap-adapter"], (
        f"Expected ['legacy-soap-adapter'] in archived_skipped, got {result['archived_skipped']}"
    )

    # Should deduce two domains:
    # - 'billing' (from team associations billing-developers / billing-maintainers)
    # - 'gis-viewer' (from shared 2-token repo name prefix 'gis-viewer-*' since only security-auditors was attached)
    domains = set(result["domain_yamls"].keys())
    assert domains == {"billing", "gis-viewer"}, (
        f"Expected deduced domains {{'billing', 'gis-viewer'}}, got {domains}"
    )

    billing_repos = {r["name"]: r for r in result["domain_yamls"]["billing"]["repositories"]}
    assert set(billing_repos.keys()) == {"invoice-worker", "payment-pci-vault"}
    # payment-pci-vault has 'pci' topic so its archetype should be inferred as 'regulated-workload'
    assert (
        billing_repos["payment-pci-vault"].get("archetype") == "regulated-workload"
        or result["domain_yamls"]["billing"]["defaults"]["archetype"] == "regulated-workload"
    )

    # 3. Validate all generated candidate dicts against our production JSON Schemas
    org_schema = val.load_json(str(REPO_ROOT / "schemas/org.schema.json"))
    teams_schema = val.load_json(str(REPO_ROOT / "schemas/teams.schema.json"))
    domain_schema = val.load_json(str(REPO_ROOT / "schemas/domain-repos.schema.json"))

    val.validate_against_schema(result["org_yaml"], org_schema, "candidate:org.yaml")
    val.validate_against_schema(result["teams_yaml"], teams_schema, "candidate:teams.yaml")
    for dkey, ddoc in result["domain_yamls"].items():
        val.validate_against_schema(ddoc, domain_schema, f"candidate:repos/{dkey}.yaml")

    if val.errors:
        print(f"  FAIL: Generated candidate YAML failed schema validation: {val.errors}", file=sys.stderr)
        return 1

    # 4. Verify drift items captured key remediations
    drift_categories = {item["category"] for item in result["drift_items"]}
    expected_categories = {
        "Team Admin Permission Downgraded",
        "Public Visibility Blocked (Tier 1)",
        "Non-Standard Default Branch",
        "Branch Protection Upgraded",
        "Production Environment Gate Added",
    }
    missing = expected_categories - drift_categories
    if missing:
        print(f"  FAIL: Drift report missed expected categories: {missing}", file=sys.stderr)
        return 1

    test_exporter_handles_400_on_external_groups()
    test_jira_autolink_config_validation()
    test_jira_autolink_import_blocks()

    print(
        "  PASS: Inventory schema, domain deduction (team + repo prefix), schema-valid candidate generation, and drift detection verified."
    )
    return 0


def test_exporter_handles_400_on_external_groups():
    """Verify export_organization_inventory handles HTTP 400 on /external-groups and mixed-case org names."""

    class MockClient:
        def get_json(self, path, params=None, allow_404=False):
            if path == "/orgs/TasWater":
                return {
                    "login": "TasWater",
                    "name": "TasWater",
                    "description": "TasWater GitHub Organization",
                    "billing_email": "cloud@taswater.com.au",
                }
            if "/external-groups" in path:
                if allow_404 and 400 in exp.OPTIONAL_HTTP_STATUS_CODES:
                    return None
                raise urllib.error.HTTPError(path, 400, "Bad Request", None, None)
            if "/protection" in path:
                return None
            return None

        def get_paginated(self, path, list_key=None, allow_optional_errors=True):
            if path == "/orgs/TasWater/teams":
                return [
                    {
                        "id": 1,
                        "slug": "Platform-Admins",
                        "name": "Platform Admins",
                        "description": "Admins",
                        "privacy": "closed",
                    }
                ]
            if path == "/orgs/TasWater/repos":
                return [
                    {
                        "name": "platform-github",
                        "description": "GitHub IaC repo",
                        "archived": False,
                        "visibility": "private",
                        "default_branch": "main",
                        "topics": ["IaC"],
                    }
                ]
            if path == "/repos/TasWater/platform-github/autolinks":
                assert allow_optional_errors is False
                return [
                    {
                        "id": 42,
                        "key_prefix": "PPLCTNS-",
                        "url_template": "https://taswater-applications.atlassian.net/browse/PPLCTNS-<num>",
                        "is_alphanumeric": False,
                    }
                ]
            return []

    snap = exp.export_organization_inventory(MockClient(), "TasWater")
    assert snap["organization"]["slug"] == "taswater", f"Expected lowercase slug 'taswater', got {snap['organization']['slug']}"
    assert snap["teams"][0]["slug"] == "platform-admins"
    assert snap["repositories"][0]["topics"] == ["iac"]
    assert snap["repositories"][0]["autolinks"][0]["key_prefix"] == "PPLCTNS-"


def test_jira_autolink_import_blocks():
    blocks = gen_imports.jira_autolink_import_blocks(
        "platform-github",
        {"project_key": "PPLCTNS"},
        [{"key_prefix": "PPLCTNS-"}],
    )
    assert 'to = module.repositories.github_repository_autolink_reference.jira["platform-github"]' in blocks
    assert 'id = "platform-github/PPLCTNS-"' in blocks

    assert not gen_imports.jira_autolink_import_blocks(
        "platform-github",
        {"project_key": "PPLCTNS"},
        [{"key_prefix": "OTHER-"}],
    )
    assert not gen_imports.jira_autolink_import_blocks(
        "platform-github",
        None,
        [{"key_prefix": "PPLCTNS-"}],
    )


def test_jira_autolink_config_validation():
    domain_schema = val.load_json(str(REPO_ROOT / "schemas/domain-repos.schema.json"))
    domain_doc = gen_imports.load_yaml(REPO_ROOT / "config/orgs/taswater/repos/platform.yaml")
    domain_doc["repositories"][0]["jira_autolink"] = {"project_key": "PPLCTNS"}

    val.errors.clear()
    val.validate_against_schema(domain_doc, domain_schema, "jira_valid")
    assert not val.errors, f"Expected a valid Jira opt-in to pass schema validation, got {val.errors}"

    val.validate_jira_browse_url(
        "https:///browse",
        "jira_invalid",
        "jira_autolink.browse_url",
    )
    assert val.errors, "Expected a browse URL without a hostname to fail validation"

    domain_doc["repositories"][0]["jira_autolink"]["project_key"] = "pplctns"
    val.errors.clear()
    val.validate_against_schema(domain_doc, domain_schema, "jira_invalid_key")
    assert val.errors, "Expected a lowercase Jira project key to fail schema validation"
    val.errors.clear()


if __name__ == "__main__":
    sys.exit(main())
