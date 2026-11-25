#!/usr/bin/env python3
"""Generate candidate GHEC YAML configs and a Governance Drift Report from an inventory snapshot.

Deduces domain groupings (`repos/<domain>.yaml`) automatically using:
  1. Team associations (stripping role suffixes like `-developers`, `-maintainers` from assigned teams)
  2. Multi-repository name prefix clustering (e.g. `ssis-manager-api` + `ssis-manager-power` -> `ssis-manager`)
  3. Topic clustering or fallback to `general-services`
"""

import argparse
from collections import Counter, defaultdict
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: python3-yaml (PyYAML) is required.", file=sys.stderr)
    sys.exit(1)

CROSS_CUTTING_TEAM_PATTERNS = (
    "platform-admins",
    "security-auditors",
    "auditors",
    "org-admins",
)

ROLE_SUFFIXES = (
    "-maintainers",
    "-developers",
    "-contributors",
    "-engineers",
    "-leads",
    "-admins",
    "-readers",
    "-team",
)


def slugify_domain(raw):
    slug = re.sub(r"[^a-z0-9-]+", "-", raw.lower()).strip("-")
    if len(slug) < 3:
        slug = f"{slug}-domain"
    return slug[:48]


def infer_team_role_tier(slug):
    s = slug.lower()
    if "admin" in s:
        return "platform-admin"
    if "audit" in s or "security" in s:
        return "auditor"
    if "maintain" in s or "lead" in s or "approver" in s:
        return "maintainer"
    if "bot" in s or "automation" in s or "ci" in s:
        return "automation"
    return "contributor"


def strip_role_suffix(team_slug):
    s = team_slug.lower()
    for suffix in ROLE_SUFFIXES:
        if s.endswith(suffix) and len(s) > len(suffix) + 2:
            return s[: -len(suffix)]
    return s


def is_cross_cutting_team(team_slug):
    s = team_slug.lower()
    return any(s == pat or s.endswith(f"-{pat}") for pat in CROSS_CUTTING_TEAM_PATTERNS)


def build_name_prefix_map(repos):
    """Find 1- or 2-token hyphenated prefixes shared by 2+ repositories."""
    two_token_counts = Counter()
    one_token_counts = Counter()
    for r in repos:
        parts = r["name"].lower().split("-")
        if len(parts) >= 3:
            two_token_counts["-".join(parts[:2])] += 1
        if len(parts) >= 2:
            one_token_counts[parts[0]] += 1

    prefix_map = {}
    for r in repos:
        rname = r["name"]
        parts = rname.lower().split("-")
        if len(parts) >= 3 and two_token_counts["-".join(parts[:2])] >= 2:
            prefix_map[rname] = slugify_domain("-".join(parts[:2]))
        elif len(parts) >= 2 and one_token_counts[parts[0]] >= 2 and len(parts[0]) >= 3:
            prefix_map[rname] = slugify_domain(parts[0])
    return prefix_map


def deduce_repository_domain(repo, prefix_map):
    """Deduce the best domain key and reason for a repository."""
    # Priority 1: Non-cross-cutting teams with write/maintain/admin access
    domain_votes = Counter()
    for tp in repo.get("team_permissions") or []:
        tslug = tp.get("team_slug", "")
        perm = tp.get("permission", "pull")
        if not tslug or is_cross_cutting_team(tslug):
            continue
        if perm in ("push", "maintain", "admin"):
            stem = strip_role_suffix(tslug)
            domain_votes[stem] += 2 if perm in ("maintain", "admin") else 1

    if domain_votes:
        best_stem = sorted(domain_votes.items(), key=lambda x: (-x[1], x[0]))[0][0]
        return slugify_domain(best_stem), f"team association ({best_stem}-*)"

    # Priority 2: Shared repository name prefix across 2+ repos
    if repo["name"] in prefix_map:
        prefix_domain = prefix_map[repo["name"]]
        return prefix_domain, f"repo name prefix ({prefix_domain}-*)"

    # Priority 3: First non-org topic
    for topic in repo.get("topics") or []:
        if len(topic) >= 3:
            return slugify_domain(topic), f"repository topic ({topic})"

    return "general-services", "fallback default"


def infer_repository_archetype(repo):
    """Infer the closest enterprise archetype for a repository."""
    rname = repo["name"].lower()
    topics = {t.lower() for t in repo.get("topics") or []}
    bp = repo.get("branch_protection") or {}

    if any(k in rname or k in topics for k in ("poc", "sandbox", "prototype", "spike")):
        return "sandbox"
    if (
        bp.get("min_reviewers", 0) >= 3
        or bp.get("require_signed_commits") is True
        or any(k in rname or k in topics for k in ("regulated", "pci", "identity", "scada", "compliance"))
    ):
        return "regulated-workload"
    if repo.get("visibility") == "internal" or any(
        rname.endswith(suf) for suf in ("-sdk", "-lib", "-design-system", "-shared")
    ):
        return "shared-library"
    return "standard-microservice"


def sanitize_description(desc, fallback_label):
    cleaned = (desc or "").strip()
    if len(cleaned) < 10:
        cleaned = f"{fallback_label} managed by GHEC-IaC."
    return cleaned


def remediate_team_permissions(raw_perms, valid_team_slugs, repo_name, drift_items):
    """Convert raw team permissions to schema-compliant team_access list."""
    remediated = []
    for tp in raw_perms or []:
        tslug = tp.get("team_slug", "")
        perm = tp.get("permission", "pull")
        if tslug not in valid_team_slugs:
            continue
        if perm == "admin":
            drift_items.append(
                {
                    "repo": repo_name,
                    "category": "Team Admin Permission Downgraded",
                    "detail": f"Team '{tslug}' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline.",
                }
            )
            perm = "maintain"
        remediated.append({"team": tslug, "permission": perm})
    return remediated


def select_fallback_maintainer_team(team_access, valid_team_slugs):
    for ta in team_access:
        if ta["permission"] == "maintain":
            return ta["team"]
    for ta in team_access:
        if ta["permission"] == "push":
            return ta["team"]
    for slug in sorted(valid_team_slugs):
        if "maintain" in slug or "admin" in slug:
            return slug
    return sorted(valid_team_slugs)[0] if valid_team_slugs else "platform-admins"


def generate_candidates(inventory, include_archived=False):
    """Transform an inventory snapshot into candidate YAML dicts and a drift report."""
    org_info = inventory["organization"]
    org_slug = org_info["slug"]

    drift_items = []
    archived_skipped = []

    # 1. Build teams.yaml candidate
    teams_list = []
    valid_team_slugs = set()
    for t in inventory.get("teams") or []:
        tslug = t["slug"]
        valid_team_slugs.add(tslug)

    if not valid_team_slugs:
        # Ensure at least one default team exists so generated files pass schema validation
        default_slug = f"{org_slug}-maintainers"
        valid_team_slugs.add(default_slug)
        teams_list.append(
            {
                "slug": default_slug,
                "name": f"{org_info['name']} Maintainers",
                "description": f"Default maintainer team for {org_slug} repositories.",
                "privacy": "closed",
                "role_tier": "maintainer",
            }
        )

    for t in inventory.get("teams") or []:
        tslug = t["slug"]
        entry = {
            "slug": tslug,
            "name": t.get("name") or tslug,
            "description": sanitize_description(t.get("description"), f"GitHub team {tslug}"),
            "privacy": "closed",
            "role_tier": infer_team_role_tier(tslug),
        }
        if t.get("privacy") != "closed":
            drift_items.append(
                {
                    "repo": f"team:{tslug}",
                    "category": "Team Privacy Standardized",
                    "detail": f"Team '{tslug}' privacy '{t.get('privacy')}' standardized to 'closed'.",
                }
            )
        parent = t.get("parent_slug")
        if parent and parent in valid_team_slugs and parent != tslug:
            entry["parent_team"] = parent
        if t.get("idp_group_id"):
            entry["idp_group_id"] = t["idp_group_id"]
        teams_list.append(entry)

    teams_yaml = {
        "organization": org_slug,
        "teams": teams_list,
    }

    # 2. Filter active repositories & deduce domain alignment
    active_repos = []
    for r in inventory.get("repositories") or []:
        if r.get("archived") and not include_archived:
            archived_skipped.append(r["name"])
            continue
        active_repos.append(r)

    prefix_map = build_name_prefix_map(active_repos)
    repos_by_domain = defaultdict(list)
    domain_reasons = {}

    for r in active_repos:
        dkey, reason = deduce_repository_domain(r, prefix_map)
        repos_by_domain[dkey].append(r)
        domain_reasons.setdefault(dkey, Counter())[reason] += 1

    # 3. Build domain repository YAML files
    domain_yamls = {}
    for dkey, drepos in sorted(repos_by_domain.items()):
        # Determine modal archetype for domain defaults
        inferred_archetypes = [infer_repository_archetype(r) for r in drepos]
        default_archetype = Counter(inferred_archetypes).most_common(1)[0][0]

        # Prepare per-repo remediated team_access and find most common team access tuple
        repo_team_access_map = {}
        access_signature_counter = Counter()
        for r in drepos:
            rname = r["name"]
            ta_list = remediate_team_permissions(
                r.get("team_permissions"), valid_team_slugs, rname, drift_items
            )
            if not ta_list:
                fallback_team = select_fallback_maintainer_team([], valid_team_slugs)
                ta_list = [{"team": fallback_team, "permission": "maintain"}]
                drift_items.append(
                    {
                        "repo": rname,
                        "category": "Missing Team Access Assigned",
                        "detail": f"Repository had no team permissions; assigned fallback team '{fallback_team}' (maintain).",
                    }
                )
            repo_team_access_map[rname] = ta_list
            sig = tuple((x["team"], x["permission"]) for x in ta_list)
            access_signature_counter[sig] += 1

        common_sig = access_signature_counter.most_common(1)[0][0]
        default_team_access = [{"team": t, "permission": p} for t, p in common_sig]
        default_approver_team = select_fallback_maintainer_team(default_team_access, valid_team_slugs)

        default_environments = [
            {
                "name": "dev",
                "description": "Development environment",
                "require_approval": False,
            },
            {
                "name": "staging",
                "description": "Staging environment",
                "require_approval": False,
            },
            {
                "name": "prod",
                "description": "Production environment",
                "require_approval": True,
                "approver_teams": [default_approver_team],
            },
        ]

        yaml_repos = []
        for r in drepos:
            rname = r["name"]
            r_arch = infer_repository_archetype(r)
            min_floor = 3 if r_arch == "regulated-workload" else 2

            # Check visibility drift
            vis = r.get("visibility", "private")
            if vis == "public":
                drift_items.append(
                    {
                        "repo": rname,
                        "category": "Public Visibility Blocked (Tier 1)",
                        "detail": "Repository is currently 'public'; set to 'private' in candidate YAML.",
                    }
                )
                vis = "private"

            # Check default branch drift
            def_branch = r.get("default_branch", "main")
            if def_branch != "main":
                drift_items.append(
                    {
                        "repo": rname,
                        "category": "Non-Standard Default Branch",
                        "detail": f"Default branch is currently '{def_branch}'; target baseline enforces 'main'.",
                    }
                )

            # Check branch protection drift
            bp = r.get("branch_protection") or {}
            live_rev = bp.get("min_reviewers", 0)
            if not bp.get("protected") or live_rev < min_floor:
                drift_items.append(
                    {
                        "repo": rname,
                        "category": "Branch Protection Upgraded",
                        "detail": (
                            f"Default branch had protected={bp.get('protected', False)}, "
                            f"min_reviewers={live_rev}; candidate applies '{r_arch}' floor (min_reviewers={min_floor})."
                        ),
                    }
                )

            repo_entry = {
                "name": rname,
                "description": sanitize_description(r.get("description"), f"Repository {rname}"),
            }
            if r_arch != default_archetype:
                repo_entry["archetype"] = r_arch

            expected_vis = "internal" if r_arch == "shared-library" else "private"
            if vis != expected_vis:
                repo_entry["visibility"] = vis

            # Preserve custom higher reviewer count (within 2..5)
            if live_rev > min_floor:
                capped_rev = min(live_rev, 5)
                repo_entry["branch_protection"] = {
                    "min_reviewers": capped_rev,
                    **({"require_signed_commits": True} if r_arch == "regulated-workload" else {}),
                }

            status_checks = bp.get("required_status_checks") or []
            if status_checks:
                repo_entry["required_status_checks"] = status_checks

            if repo_team_access_map[rname] != default_team_access:
                repo_entry["team_access"] = repo_team_access_map[rname]

            # Check environments
            live_envs = r.get("environments") or []
            if live_envs:
                remediated_envs = []
                for le in live_envs:
                    ename = le.get("name", "")
                    req_app = bool(le.get("require_approval", False))
                    approvers = [
                        a for a in (le.get("approver_teams") or []) if a in valid_team_slugs
                    ]
                    if ename.lower() in ("prod", "production", "prd") and not req_app:
                        req_app = True
                        drift_items.append(
                            {
                                "repo": rname,
                                "category": "Production Environment Gate Added",
                                "detail": f"Environment '{ename}' had require_approval=false; enforced require_approval=true.",
                            }
                        )
                    if req_app and not approvers:
                        approvers = [default_approver_team]
                        drift_items.append(
                            {
                                "repo": rname,
                                "category": "Environment Approver Team Assigned",
                                "detail": f"Environment '{ename}' had no valid team approvers; assigned '{default_approver_team}'.",
                            }
                        )
                    env_item = {
                        "name": ename,
                        "require_approval": req_app,
                    }
                    if approvers:
                        env_item["approver_teams"] = approvers
                    remediated_envs.append(env_item)
                repo_entry["environments"] = remediated_envs

            yaml_repos.append(repo_entry)

        domain_title = dkey.replace("-", " ").title()
        domain_yamls[dkey] = {
            "domain": {
                "key": dkey,
                "name": f"{domain_title} Domain",
                "description": f"Repositories aligned to the {domain_title} domain in {org_slug}.",
                "organization": org_slug,
            },
            "defaults": {
                "archetype": default_archetype,
                "topics": [dkey, org_slug],
                "team_access": default_team_access,
                "environments": default_environments,
            },
            "repositories": yaml_repos,
        }

    # 4. Build org.yaml candidate
    org_yaml = {
        "organization": {
            "slug": org_slug,
            "name": org_info.get("name") or org_slug,
            "description": sanitize_description(
                org_info.get("description"), f"GitHub Organization {org_slug}"
            ),
            "billing_email": org_info.get("billing_email") or f"platform@{org_slug}.example.com",
            "default_archetype": "standard-microservice",
        },
        "security_dials": {
            "members_can_create_private_repositories": bool(
                org_info.get("members_can_create_private_repositories", False)
            ),
            "members_can_create_internal_repositories": bool(
                org_info.get("members_can_create_internal_repositories", False)
            ),
            "members_can_fork_private_repositories": bool(
                org_info.get("members_can_fork_private_repositories", False)
            ),
            "web_commit_signoff_required": bool(
                org_info.get("web_commit_signoff_required", False)
            ),
            "dependabot_alerts_enabled_for_new_repositories": True,
            "secret_scanning_enabled_for_new_repositories": True,
            "secret_scanning_push_protection_enabled_for_new_repositories": True,
        },
        "actions_dials": {
            "allowed_actions": "selected",
            "allow_github_owned_actions": True,
            "allow_verified_creator_actions": True,
            "default_workflow_permissions": "read",
            "can_approve_pull_request_reviews": False,
            "sha_pinning_required": True,
            "default_job_timeout_minutes": 60,
        },
        "repository_defaults": {
            "default_branch": "main",
            "min_reviewers": 2,
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True,
            "require_last_push_approval": True,
            "require_conversation_resolution": True,
            "allowed_merge_types": {
                "squash": True,
                "merge_commit": True,
                "rebase": False,
                "auto_merge": True,
                "delete_branch_on_merge": True,
            },
        },
        "runner_groups": [],
        "copilot_dials": {
            "enabled": False,
            "seat_management": "disabled",
            "assigned_teams": [],
            "content_exclusions": [],
        },
        "codespaces_dials": {
            "enabled": False,
            "access_policy": "disabled",
            "allowed_teams": [],
            "allowed_machine_types": ["basicLinux32gb", "standardLinux32gb"],
            "default_idle_timeout_minutes": 30,
            "default_retention_period_days": 14,
        },
        "billing_budgets": [],
    }

    report_md = render_drift_report(
        org_slug=org_slug,
        teams_count=len(teams_list),
        active_repos_count=len(active_repos),
        archived_skipped=archived_skipped,
        domain_yamls=domain_yamls,
        domain_reasons=domain_reasons,
        drift_items=drift_items,
    )

    return {
        "org_yaml": org_yaml,
        "teams_yaml": teams_yaml,
        "domain_yamls": domain_yamls,
        "drift_report_md": report_md,
        "drift_items": drift_items,
        "archived_skipped": archived_skipped,
    }


def render_drift_report(
    org_slug,
    teams_count,
    active_repos_count,
    archived_skipped,
    domain_yamls,
    domain_reasons,
    drift_items,
):
    lines = [
        f"# GitHub Onboarding & Governance Drift Report: `{org_slug}`",
        "",
        "## 1. Extraction Summary",
        "",
        f"- **Organization**: `{org_slug}`",
        f"- **GitHub Teams Discovered**: `{teams_count}`",
        f"- **Active Repositories Analyzed**: `{active_repos_count}`",
        f"- **Archived Repositories Excluded**: `{len(archived_skipped)}`",
        f"- **Deduced Domain Files**: `{len(domain_yamls)}`",
        "",
        "## 2. Deduced Domain Alignment (`repos/<domain>.yaml`)",
        "",
        "| Domain File | Repo Count | Default Archetype | Primary Deduction Signal |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for dkey, ddoc in sorted(domain_yamls.items()):
        rcount = len(ddoc["repositories"])
        arch = ddoc["defaults"]["archetype"]
        top_reason = domain_reasons[dkey].most_common(1)[0][0]
        lines.append(f"| `repos/{dkey}.yaml` | {rcount} | `{arch}` | {top_reason} |")

    if archived_skipped:
        lines.extend(
            [
                "",
                "## 3. Archived Repositories (Skipped by Default)",
                "",
                "The following repositories are marked `archived: true` in GitHub and were excluded from active YAML governance:",
                "",
            ]
        )
        for ar in sorted(archived_skipped):
            lines.append(f"- `{ar}`")

    lines.extend(
        [
            "",
            "## 4. Baseline Drift & Remediation Items",
            "",
            "The items below show where live GitHub settings differed from Tier 1/Tier 2 baselines and were automatically normalized in the generated candidate YAML:",
            "",
        ]
    )
    if not drift_items:
        lines.append("_No baseline drift detected. All analyzed repositories already match target bounds._")
    else:
        lines.extend(
            [
                "| Target | Remediation Category | Details |",
                "| :--- | :--- | :--- |",
            ]
        )
        for item in drift_items:
            lines.append(f"| `{item['repo']}` | **{item['category']}** | {item['detail']} |")

    lines.append("")
    return "\n".join(lines)


def write_yaml_with_schema(path, schema_rel_path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f"# yaml-language-server: $schema={schema_rel_path}\n"
    body = yaml.safe_dump(data, sort_keys=False, default_flow_style=False)
    path.write_text(header + body, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Generate candidate GHEC YAML config files and a drift report from an inventory JSON file."
    )
    parser.add_argument(
        "--inventory",
        required=True,
        help="Path to the exported organization inventory JSON file",
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for generated candidate YAML files (default: candidates/<org>)",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived repositories in generated domain YAML files",
    )
    args = parser.parse_args()

    inv_path = Path(args.inventory)
    with open(inv_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    org_slug = inventory["organization"]["slug"].strip().lower()
    out_dir = Path(args.output_dir or f"candidates/{org_slug}")
    if out_dir.name != out_dir.name.lower():
        print(
            f"ERROR: Output directory '{out_dir}' contains uppercase characters in '{out_dir.name}'. "
            f"Use lowercase ('{out_dir.name.lower()}') to prevent Windows/macOS checkout collisions.",
            file=sys.stderr,
        )
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    result = generate_candidates(inventory, include_archived=args.include_archived)

    write_yaml_with_schema(out_dir / "org.yaml", "../../../schemas/org.schema.json", result["org_yaml"])
    write_yaml_with_schema(out_dir / "teams.yaml", "../../../schemas/teams.schema.json", result["teams_yaml"])

    for dkey, ddoc in result["domain_yamls"].items():
        write_yaml_with_schema(
            out_dir / "repos" / f"{dkey}.yaml",
            "../../../../schemas/domain-repos.schema.json",
            ddoc,
        )

    report_path = out_dir / "drift-report.md"
    report_path.write_text(result["drift_report_md"], encoding="utf-8")

    print(
        f"Generated candidate configs for '{org_slug}' in {out_dir}/ "
        f"({len(result['domain_yamls'])} domain files, {len(result['drift_items'])} drift remediations). "
        f"See {report_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
