#!/usr/bin/env python3
"""Verify Tier 1 invariants remain hardcoded in the OpenTofu modules."""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main():
    proj_main = (REPO_ROOT / "modules/project-archetype/main.tf").read_text(encoding="utf-8")
    branch_pol = (REPO_ROOT / "modules/project-archetype/branch_policies.tf").read_text(encoding="utf-8")
    bridge_main = (REPO_ROOT / "modules/org-settings-api-bridge/main.tf").read_text(encoding="utf-8")

    checks = [
        (bool(re.search(r'visibility\s*=\s*"private"', proj_main)), "Tier 1 invariant: project visibility must remain hardcoded to 'private' in modules/project-archetype/main.tf"),
        (bool(re.search(r'submitter_can_vote\s*=\s*false', branch_pol)), "Tier 1 invariant: submitter_can_vote must remain hardcoded to false in modules/project-archetype/branch_policies.tf"),
        (bool(re.search(r'last_pusher_cannot_approve\s*=\s*true', branch_pol)), "Tier 1 invariant: last_pusher_cannot_approve must remain hardcoded to true in modules/project-archetype/branch_policies.tf"),
        (bool(re.search(r'"Policy\.AllowOrgPublicProjects"\s*=\s*false', bridge_main)), "Tier 1 invariant: Policy.AllowOrgPublicProjects must remain false in modules/org-settings-api-bridge/main.tf"),
        (bool(re.search(r'"Policy\.DisallowAnonymousAccess"\s*=\s*true', bridge_main)), "Tier 1 invariant: Policy.DisallowAnonymousAccess must remain true in modules/org-settings-api-bridge/main.tf"),
    ]

    failed = False
    for ok, description in checks:
        if not ok:
            print(f"  FAIL: {description}", file=sys.stderr)
            failed = True

    if failed:
        return 1
    print("  PASS: All Tier 1 immutable baseline invariants verified in HCL modules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
