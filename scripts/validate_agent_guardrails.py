#!/usr/bin/env python3
"""Verify unified agent skills, cross-platform path casing, and repository guardrail integrity."""

import glob
import os
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def find_case_and_slug_violations(paths: list[str]) -> list[str]:
    """Detect Windows/macOS case-insensitive path collisions and uppercase org/domain slugs.

    Args:
        paths: Repository-relative POSIX paths (files and directories).

    Returns:
        List of human-readable error strings (empty when compliant).
    """
    violations = []
    seen_lower: dict[str, str] = {}

    # Also check every parent directory prefix so colliding directories
    # (e.g. 'candidates/taswater/a.yaml' vs 'candidates/TasWater/b.yaml') are caught
    # even if the leaf filenames inside them differ!
    all_entries: set[str] = set()
    for raw in paths:
        norm = raw.strip().lstrip("./").replace("\\", "/")
        if not norm:
            continue
        parts = norm.split("/")
        for idx in range(1, len(parts) + 1):
            all_entries.add("/".join(parts[:idx]))

    for entry in sorted(all_entries):
        lowered = entry.lower()
        if lowered in seen_lower and seen_lower[lowered] != entry:
            violations.append(
                f"[PATH-CASE-COLLISION] '{seen_lower[lowered]}' and '{entry}' differ only by letter case, "
                "which breaks git checkouts on Windows and macOS."
            )
        else:
            seen_lower[lowered] = entry

        parts = entry.split("/")
        # Enforce canonical lowercase slugs for orgs, candidates, stacks, and inventories
        if len(parts) >= 2 and parts[0] in {"candidates", "environments"}:
            target = parts[1]
            if target not in {"README.md", "AGENTS.md"} and target != target.lower():
                violations.append(
                    f"[PATH-UPPERCASE-SLUG] '{entry}': directory/stack slug '{target}' must be lowercase "
                    f"('{target.lower()}') for cross-platform compatibility."
                )
        if len(parts) >= 3 and parts[0] == "config" and parts[1] == "orgs":
            org_slug = parts[2]
            if org_slug not in {"README.md", "AGENTS.md"} and org_slug != org_slug.lower():
                violations.append(
                    f"[PATH-UPPERCASE-SLUG] '{entry}': organization directory '{org_slug}' must be lowercase "
                    f"('{org_slug.lower()}') for cross-platform compatibility."
                )
        if len(parts) == 2 and parts[0] == "inventory" and parts[1].endswith(".json"):
            if parts[1] != parts[1].lower():
                violations.append(
                    f"[PATH-UPPERCASE-SLUG] '{entry}': inventory filename '{parts[1]}' must be lowercase "
                    f"('{parts[1].lower()}')."
                )
        if entry.endswith((".yaml", ".yml")) and (
            entry.startswith("config/") or entry.startswith("candidates/")
        ):
            leaf = parts[-1]
            if leaf != leaf.lower():
                violations.append(
                    f"[PATH-UPPERCASE-SLUG] '{entry}': YAML filename '{leaf}' must be lowercase ('{leaf.lower()}')."
                )

    return violations


def collect_repository_paths(repo_root: Path) -> list[str]:
    """Collect relative POSIX paths from both git index (if available) and working tree."""
    collected: set[str] = set()

    # 1. Include git index paths so case-colliding tracked files are caught even on Windows/macOS
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        for line in proc.stdout.splitlines():
            if line.strip():
                collected.add(line.strip())
    except Exception:
        pass

    # 2. Include working-tree directories and files
    ignored_dirs = {".git", ".terraform", "__pycache__"}
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        rel_root = Path(root).resolve().relative_to(repo_root.resolve())
        if str(rel_root) != ".":
            collected.add(rel_root.as_posix())
        for filename in files:
            rel_file = (rel_root / filename) if str(rel_root) != "." else Path(filename)
            collected.add(rel_file.as_posix())

    return sorted(collected)


def main():
    os.chdir(REPO_ROOT)

    skill_files = sorted(glob.glob(".agents/skills/*/SKILL.md"))
    if not skill_files:
        print("  FAIL: No canonical skills found in .agents/skills/*/SKILL.md", file=sys.stderr)
        return 1

    skills = []
    for skill_file in skill_files:
        folder_name = os.path.basename(os.path.dirname(skill_file))
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.startswith("---"):
            print(f"  FAIL: {skill_file} is missing YAML frontmatter", file=sys.stderr)
            return 1
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1]) or {}
        if frontmatter.get("name") != folder_name:
            print(
                f"  FAIL: {skill_file} frontmatter name '{frontmatter.get('name')}' does not match folder '{folder_name}'",
                file=sys.stderr,
            )
            return 1
        if not frontmatter.get("description"):
            print(f"  FAIL: {skill_file} is missing frontmatter description", file=sys.stderr)
            return 1
        if frontmatter.get("disable-model-invocation") is True:
            print(
                f"  FAIL: {skill_file} sets disable-model-invocation: true (breaks automatic skill loading)",
                file=sys.stderr,
            )
            return 1
        skills.append(folder_name)

    legacy_prompts = glob.glob(".github/prompts/*.prompt.md")
    if legacy_prompts:
        print(
            f"  FAIL: Found deprecated .github/prompts/*.prompt.md files ({legacy_prompts}). Use unified SKILL.md files instead.",
            file=sys.stderr,
        )
        return 1

    required_files = ["AGENTS.md", "GEMINI.md", "config/AGENTS.md", ".github/copilot-instructions.md"]
    for required_file in required_files:
        if not os.path.isfile(required_file):
            print(f"  FAIL: Missing required AI guardrail file: {required_file}", file=sys.stderr)
            return 1

    # Cross-platform Windows/macOS path case-sensitivity & lowercase slug check
    repo_paths = collect_repository_paths(REPO_ROOT)
    case_violations = find_case_and_slug_violations(repo_paths)
    if case_violations:
        for violation in case_violations:
            print(f"  FAIL: {violation}", file=sys.stderr)
        return 1

    # This file contains the patterns being checked, so scanning it would be self-matching.
    scanner_path = Path(__file__).resolve()
    for root, dirs, files in os.walk("."):
        dirs[:] = [directory for directory in dirs if directory not in {".git", ".terraform", "__pycache__"}]
        for filename in files:
            file_path = os.path.join(root, filename)
            if Path(file_path).resolve() == scanner_path:
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                continue
            for bad_pattern in ("file://", "/home/", "/Users/"):
                if bad_pattern in text:
                    print(
                        f"  FAIL: {file_path} contains hardcoded path pattern '{bad_pattern}'. Use repository-relative paths instead.",
                        file=sys.stderr,
                    )
                    return 1

    print(
        f"  PASS: {len(skills)} unified Agent Skills, cross-platform path casing, and relative paths validated: {', '.join(skills)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
