#!/usr/bin/env python3
"""Verify unified agent skills and repository guardrail integrity."""

import glob
import os
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)


def main():
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
            print(f"  FAIL: {skill_file} frontmatter name '{frontmatter.get('name')}' does not match folder '{folder_name}'", file=sys.stderr)
            return 1
        if not frontmatter.get("description"):
            print(f"  FAIL: {skill_file} is missing frontmatter description", file=sys.stderr)
            return 1
        if frontmatter.get("disable-model-invocation") is True:
            print(f"  FAIL: {skill_file} sets disable-model-invocation: true (breaks automatic skill loading)", file=sys.stderr)
            return 1
        skills.append(folder_name)

    legacy_prompts = glob.glob(".github/prompts/*.prompt.md")
    if legacy_prompts:
        print(f"  FAIL: Found deprecated .github/prompts/*.prompt.md files ({legacy_prompts}). Use unified SKILL.md files instead.", file=sys.stderr)
        return 1

    required_files = ["AGENTS.md", "GEMINI.md", "config/AGENTS.md", "modules/AGENTS.md", ".github/copilot-instructions.md"]
    for required_file in required_files:
        if not os.path.isfile(required_file):
            print(f"  FAIL: Missing required AI guardrail file: {required_file}", file=sys.stderr)
            return 1

    # This file contains the patterns being checked, so scanning it would be self-matching.
    scanner_path = Path(__file__).resolve()
    for root, dirs, files in os.walk("."):
        dirs[:] = [directory for directory in dirs if directory not in {".git", ".terraform"}]
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
                    print(f"  FAIL: {file_path} contains hardcoded path pattern '{bad_pattern}'. Use repository-relative paths instead.", file=sys.stderr)
                    return 1

    print(f"  PASS: {len(skills)} unified Agent Skills and relative paths validated for Gemini and GitHub Copilot: {', '.join(skills)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
