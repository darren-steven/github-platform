#!/usr/bin/env python3
"""Read-only GitHub Organization inventory exporter.

Queries the GitHub REST API (using GITHUB_TOKEN / GH_TOKEN or `gh auth token`)
to capture a point-in-time JSON snapshot of an organization's settings, teams,
repositories, team permissions, branch protections, deployment environments,
and repository autolink references.

Streams flushed progress updates to stderr during CLI runs so long exports
(150+ repositories) show real-time progress in terminals and GitHub Actions.
"""

import argparse
from datetime import datetime, timezone
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


OPTIONAL_HTTP_STATUS_CODES = (400, 403, 404, 409, 422, 501)


def stderr_progress_logger(message: str) -> None:
    """Write a timestamped, immediately-flushed progress line to stderr."""
    ts = datetime.now(timezone.utc).strftime("%H:%M:%SZ")
    print(f"[{ts}] {message}", file=sys.stderr, flush=True)


class GitHubReadOnlyClient:
    """Minimal read-only GitHub REST API client supporting pagination."""

    def __init__(self, api_url="https://api.github.com", token=None):
        self.api_url = api_url.rstrip("/")
        self.token = token or self._discover_token()
        if not self.token:
            raise RuntimeError(
                "No GitHub token found. Set GITHUB_TOKEN / GH_TOKEN or authenticate with 'gh auth login'."
            )

    @staticmethod
    def _discover_token():
        for env_var in ("GITHUB_TOKEN", "GH_TOKEN"):
            val = os.environ.get(env_var, "").strip()
            if val:
                return val
        try:
            res = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                check=True,
            )
            return res.stdout.strip()
        except Exception:
            return None

    def get_json(self, path, params=None, allow_404=False):
        url = f"{self.api_url}/{path.lstrip('/')}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "ghec-iac-inventory-exporter",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            # Optional sub-endpoints (such as /external-groups on non-IdP/child teams,
            # or /branches/.../protection on empty repositories) can return 400, 403,
            # 404, 409, or 422 depending on token role and repository state.
            if allow_404 and exc.code in OPTIONAL_HTTP_STATUS_CODES:
                return None
            raise

    def get_paginated(self, path, list_key=None, allow_optional_errors=True):
        items = []
        page = 1
        while True:
            data = self.get_json(
                path,
                params={"per_page": 100, "page": page},
                allow_404=allow_optional_errors,
            )
            if not data:
                break
            batch = data.get(list_key, []) if list_key and isinstance(data, dict) else data
            if not isinstance(batch, list) or not batch:
                break
            items.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return items


def normalize_permission(repo_team_obj):
    """Map GitHub API team permission response to canonical YAML role."""
    role_name = (repo_team_obj.get("role_name") or repo_team_obj.get("permission") or "pull").lower()
    mapping = {
        "read": "pull",
        "pull": "pull",
        "triage": "triage",
        "write": "push",
        "push": "push",
        "maintain": "maintain",
        "admin": "admin",
    }
    return mapping.get(role_name, "pull")


def export_organization_inventory(client, org_slug, progress_callback=None):
    """Fetch organization, teams, and repositories into the normalized inventory dictionary."""
    def emit(msg: str) -> None:
        if progress_callback is not None:
            progress_callback(msg)

    emit(f"[1/3] Fetching organization metadata for '{org_slug}'...")
    org_raw = client.get_json(f"/orgs/{org_slug}")
    canonical_org_slug = (org_raw.get("login") or org_slug).lower()

    emit(f"[1/3] Listing teams and repositories in '{canonical_org_slug}'...")
    teams_raw = client.get_paginated(f"/orgs/{org_slug}/teams")
    repos_raw = client.get_paginated(f"/orgs/{org_slug}/repos")
    emit(
        f"[1/3] Discovered {len(teams_raw)} team(s) and {len(repos_raw)} repository(ies) in '{canonical_org_slug}'."
    )

    teams_by_id = {
        t.get("id"): (t.get("slug") or "").lower() for t in teams_raw if isinstance(t, dict)
    }

    sorted_teams = sorted(teams_raw, key=lambda x: (x.get("slug") or "").lower())
    total_teams = len(sorted_teams)
    emit(f"[2/3] Exporting {total_teams} team(s) (hierarchy & IdP group mappings)...")

    teams = []
    for idx, t in enumerate(sorted_teams, start=1):
        raw_slug = t.get("slug") or ""
        norm_slug = raw_slug.lower()
        emit(f"  [team {idx}/{total_teams}] {norm_slug}")
        team_entry = {
            "slug": norm_slug,
            "name": t.get("name") or raw_slug,
            "description": (t.get("description") or f"GitHub team {t.get('name') or raw_slug}").strip(),
            "privacy": "closed" if t.get("privacy") == "closed" else str(t.get("privacy") or "closed"),
        }
        parent = t.get("parent")
        if isinstance(parent, dict) and parent.get("slug"):
            team_entry["parent_slug"] = parent["slug"].lower()

        # Note: GitHub returns HTTP 400 on /external-groups if a team has explicit members,
        # is a child team, or when IdP group sync is not enabled for that team.
        if not team_entry.get("parent_slug"):
            ext_groups = client.get_json(
                f"/orgs/{org_slug}/teams/{raw_slug}/external-groups", allow_404=True
            )
            if isinstance(ext_groups, dict) and ext_groups.get("groups"):
                first_group = ext_groups["groups"][0]
                if first_group.get("group_id"):
                    team_entry["idp_group_id"] = str(first_group["group_id"])
        teams.append(team_entry)

    sorted_repos = sorted(repos_raw, key=lambda x: (x.get("name") or "").lower())
    total_repos = len(sorted_repos)
    emit(
        f"[3/3] Exporting {total_repos} repository(ies) "
        "(team permissions, branch protection, environments, autolinks)..."
    )

    repositories = []
    for idx, r in enumerate(sorted_repos, start=1):
        rname = r.get("name") or ""
        default_branch = r.get("default_branch") or "main"
        archived = bool(r.get("archived", False))
        archived_suffix = " (archived)" if archived else ""
        emit(f"  [repo {idx}/{total_repos}] {rname}{archived_suffix}")

        # Fetch team permissions on repo
        repo_teams_raw = client.get_paginated(f"/repos/{org_slug}/{rname}/teams")
        team_permissions = []
        for rt in sorted(repo_teams_raw, key=lambda x: (x.get("slug") or "").lower()):
            if rt.get("slug"):
                team_permissions.append(
                    {
                        "team_slug": rt["slug"].lower(),
                        "permission": normalize_permission(rt),
                    }
                )

        # Fetch branch protection on default branch
        bp_raw = client.get_json(
            f"/repos/{org_slug}/{rname}/branches/{urllib.parse.quote(default_branch, safe='')}/protection",
            allow_404=True,
        )
        pr_reviews = (bp_raw or {}).get("required_pull_request_reviews") or {}
        status_checks = (bp_raw or {}).get("required_status_checks") or {}
        branch_protection = {
            "protected": bp_raw is not None,
            "min_reviewers": int(pr_reviews.get("required_approving_review_count", 0)),
            "dismiss_stale_reviews": bool(pr_reviews.get("dismiss_stale_reviews", False)),
            "require_code_owner_reviews": bool(pr_reviews.get("require_code_owner_reviews", False)),
            "require_last_push_approval": bool(pr_reviews.get("require_last_push_approval", False)),
            "require_conversation_resolution": bool(
                ((bp_raw or {}).get("required_conversation_resolution") or {}).get("enabled", False)
            ),
            "require_signed_commits": bool(
                ((bp_raw or {}).get("required_signatures") or {}).get("enabled", False)
            ),
            "require_linear_history": bool(
                ((bp_raw or {}).get("required_linear_history") or {}).get("enabled", False)
            ),
            "required_status_checks": sorted(status_checks.get("contexts") or []),
        }

        # Security & analysis
        sec_analysis = r.get("security_and_analysis") or {}
        security = {
            "dependabot_alerts": (
                (sec_analysis.get("dependabot_security_updates") or {}).get("status") == "enabled"
                or bool(r.get("has_vulnerability_alerts", True))
            ),
            "secret_scanning": (sec_analysis.get("secret_scanning") or {}).get("status") == "enabled",
            "secret_scanning_push_protection": (
                sec_analysis.get("secret_scanning_push_protection") or {}
            ).get("status")
            == "enabled",
        }

        # Environments
        envs_raw = client.get_paginated(
            f"/repos/{org_slug}/{rname}/environments", list_key="environments"
        )
        environments = []
        for env_obj in envs_raw:
            ename = env_obj.get("name") or ""
            if not ename:
                continue
            approver_teams = []
            require_approval = False
            for rule in env_obj.get("protection_rules") or []:
                if rule.get("type") == "required_reviewers":
                    require_approval = True
                    for rev in rule.get("reviewers") or []:
                        if rev.get("type") == "Team":
                            reviewer_obj = rev.get("reviewer") or {}
                            tslug = (
                                (reviewer_obj.get("slug") or "").lower()
                                or teams_by_id.get(reviewer_obj.get("id"))
                            )
                            if tslug:
                                approver_teams.append(tslug)
            environments.append(
                {
                    "name": ename,
                    "require_approval": require_approval,
                    "approver_teams": sorted(set(approver_teams)),
                }
            )

        autolinks_raw = client.get_paginated(
            f"/repos/{org_slug}/{rname}/autolinks",
            allow_optional_errors=False,
        )
        autolinks = sorted(
            [
                {
                    "id": int(autolink["id"]),
                    "key_prefix": autolink["key_prefix"],
                    "url_template": autolink["url_template"],
                    "is_alphanumeric": bool(autolink.get("is_alphanumeric", True)),
                }
                for autolink in autolinks_raw
                if isinstance(autolink, dict)
            ],
            key=lambda autolink: autolink["key_prefix"],
        )

        repositories.append(
            {
                "name": rname,
                "description": (r.get("description") or f"Repository {rname}").strip(),
                "archived": archived,
                "visibility": r.get("visibility") or ("private" if r.get("private", True) else "public"),
                "default_branch": default_branch,
                "topics": sorted(t.lower() for t in (r.get("topics") or []) if isinstance(t, str)),
                "features": {
                    "has_issues": bool(r.get("has_issues", True)),
                    "has_wiki": bool(r.get("has_wiki", False)),
                    "has_discussions": bool(r.get("has_discussions", False)),
                    "has_projects": bool(r.get("has_projects", False)),
                },
                "merge_strategies": {
                    "allow_squash_merge": bool(r.get("allow_squash_merge", True)),
                    "allow_merge_commit": bool(r.get("allow_merge_commit", True)),
                    "allow_rebase_merge": bool(r.get("allow_rebase_merge", False)),
                    "allow_auto_merge": bool(r.get("allow_auto_merge", False)),
                    "delete_branch_on_merge": bool(r.get("delete_branch_on_merge", True)),
                },
                "branch_protection": branch_protection,
                "security": security,
                "team_permissions": team_permissions,
                "environments": environments,
                "autolinks": autolinks,
            }
        )

    return {
        "schema_version": "1.0",
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "organization": {
            "slug": canonical_org_slug,
            "name": org_raw.get("name") or org_raw.get("login") or org_slug,
            "description": (org_raw.get("description") or f"GitHub Organization {org_slug}").strip(),
            "billing_email": org_raw.get("billing_email") or f"platform@{canonical_org_slug}.example.com",
            "default_repository_permission": org_raw.get("default_repository_permission") or "none",
            "members_can_create_public_repositories": bool(
                org_raw.get("members_can_create_public_repositories", False)
            ),
            "members_can_create_private_repositories": bool(
                org_raw.get("members_can_create_private_repositories", False)
            ),
            "members_can_create_internal_repositories": bool(
                org_raw.get("members_can_create_internal_repositories", False)
            ),
            "members_can_fork_private_repositories": bool(
                org_raw.get("members_can_fork_private_repositories", False)
            ),
            "web_commit_signoff_required": bool(org_raw.get("web_commit_signoff_required", False)),
        },
        "teams": teams,
        "repositories": repositories,
    }


def validate_lowercase_repo_path(path: Path) -> None:
    """Reject uppercase characters in repository-managed inventory paths (Windows safety)."""
    if path.name != path.name.lower():
        raise ValueError(
            f"Output filename '{path.name}' contains uppercase characters. "
            f"Use canonical lowercase ('{path.name.lower()}') to avoid case-sensitivity collisions on Windows/macOS."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Export a read-only JSON snapshot of a GitHub Organization's teams and repositories."
    )
    parser.add_argument("--org", required=True, help="GitHub Organization slug (e.g., taswater)")
    parser.add_argument(
        "--output",
        help="Output JSON file path (default: inventory/<org-lowercase>.inventory.json)",
    )
    parser.add_argument(
        "--api-url",
        default=os.environ.get("GITHUB_API_URL", "https://api.github.com"),
        help="GitHub REST API base URL",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-team and per-repository progress lines on stderr",
    )
    args = parser.parse_args()

    out_path = Path(args.output or f"inventory/{args.org.strip().lower()}.inventory.json")
    validate_lowercase_repo_path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    start_time = time.monotonic()
    progress_fn = None if args.quiet else stderr_progress_logger

    client = GitHubReadOnlyClient(api_url=args.api_url)
    snapshot = export_organization_inventory(client, args.org.strip(), progress_callback=progress_fn)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
        f.write("\n")

    elapsed = time.monotonic() - start_time
    print(
        f"Exported organization '{snapshot['organization']['slug']}' "
        f"({len(snapshot['teams'])} teams, {len(snapshot['repositories'])} repositories) "
        f"to {out_path} in {elapsed:.1f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
