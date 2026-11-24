#!/usr/bin/env python3
"""Verify Tier 1 invariants, documentation completeness, and formatting in OpenTofu HCL."""

import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)

FORBIDDEN_HCL_PATTERNS = [
    (
        re.compile(r'visibility\s*=\s*"public"'),
        "Tier 1 Violation: visibility = \"public\" is forbidden in HCL.",
    ),
    (
        re.compile(r'permission\s*=\s*"admin"'),
        "Tier 1 Violation: permission = \"admin\" is forbidden on github_team_repository.",
    ),
    (
        re.compile(r"members_can_create_public_repositories\s*=\s*true"),
        "Tier 1 Violation: members_can_create_public_repositories must remain false.",
    ),
    (
        re.compile(r'default_workflow_permissions\s*=\s*"write"'),
        "Tier 1 Violation: default_workflow_permissions must remain \"read\".",
    ),
    (
        re.compile(r"can_approve_pull_request_reviews\s*=\s*true"),
        "Tier 1 Violation: can_approve_pull_request_reviews must remain false.",
    ),
    (
        re.compile(r"allows_public_repositories\s*=\s*true"),
        "Tier 1 Violation: allows_public_repositories must remain false on runner groups.",
    ),
    (
        re.compile(r"archive_on_destroy\s*=\s*false"),
        "Tier 1 Violation: archive_on_destroy must remain true on github_repository.",
    ),
]


def main() -> int:
    tf_files = sorted(
        glob.glob("modules/**/*.tf", recursive=True)
        + glob.glob("environments/**/*.tf", recursive=True)
    )
    if not tf_files:
        print("  INFO: No OpenTofu files present in modules/ or environments/.")
        return 0

    errors = []

    # 1. Static Tier 1 invariant scan across all .tf files
    for tf_path in tf_files:
        content = Path(tf_path).read_text(encoding="utf-8")
        # Ignore comment-only lines when checking forbidden assignments
        code_lines = [
            line for line in content.splitlines() if not line.lstrip().startswith(("#", "//"))
        ]
        code_text = "\n".join(code_lines)
        for pattern, message in FORBIDDEN_HCL_PATTERNS:
            if pattern.search(code_text):
                errors.append(f"{tf_path}: {message}")

    # Ensure github_repository retains archive_on_destroy = true
    repo_main = Path("modules/domain-repositories/main.tf")
    if repo_main.is_file():
        repo_text = repo_main.read_text(encoding="utf-8")
        if not re.search(r"archive_on_destroy\s*=\s*true", repo_text):
            errors.append(
                "modules/domain-repositories/main.tf: github_repository must explicitly set archive_on_destroy = true."
            )

    # 2. Documentation completeness: every module and environment directory must have a README.md
    for base in ("modules", "environments"):
        base_path = Path(base)
        if not base_path.is_dir():
            continue
        if not (base_path / "README.md").is_file():
            errors.append(f"Missing required documentation file: {base}/README.md")
        if not (base_path / "AGENTS.md").is_file():
            errors.append(f"Missing required scoped guardrail file: {base}/AGENTS.md")
        for sub in sorted(p for p in base_path.iterdir() if p.is_dir() and not p.name.startswith(".")):
            if not (sub / "README.md").is_file():
                errors.append(f"Missing required documentation file: {sub}/README.md")

    # 3. Optional formatting check if tofu or terraform CLI is available
    tf_bin = shutil.which("tofu") or shutil.which("terraform")
    if tf_bin:
        fmt_proc = subprocess.run(
            [tf_bin, "fmt", "-check", "-recursive", "modules", "environments"],
            capture_output=True,
            text=True,
        )
        if fmt_proc.returncode != 0:
            print(f"WARN: HCL formatting check failed (`{os.path.basename(tf_bin)} fmt -recursive modules environments`):\n{fmt_proc.stdout.strip()}")

    if errors:
        for err in errors:
            print(f"  FAIL: {err}", file=sys.stderr)
        return 1

    fmt_note = f" + `{os.path.basename(tf_bin)} fmt -check`" if tf_bin else " (tofu CLI not on PATH; static checks verified)"
    print(f"  PASS: Verified {len(tf_files)} OpenTofu file(s), Tier 1 HCL invariants, and directory READMEs{fmt_note}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
