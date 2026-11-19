#!/usr/bin/env bash
# =============================================================================
# Safe Local OpenTofu Plan Wrapper (`scripts/tofu-plan.sh`)
# =============================================================================
# Phase 1 Alignment Helper — Strictly READ-ONLY (never executes `tofu apply`).
#
# Usage:
#   ./scripts/tofu-plan.sh <org-slug> [extra tofu plan flags...]
#
# Example:
#   ./scripts/tofu-plan.sh taswater
#   ./scripts/tofu-plan.sh taswater -target=module.teams
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if [[ $# -lt 1 ]]; then
  echo "Usage: ./scripts/tofu-plan.sh <org-slug> [extra tofu plan flags...]" >&2
  echo "Available environments:" >&2
  ls -1 "${REPO_ROOT}/environments" | grep -vE '^(README\.md|AGENTS\.md)$' | sed 's/^/  - /' >&2
  exit 1
fi

ORG_SLUG="$1"
shift
ENV_DIR="${REPO_ROOT}/environments/${ORG_SLUG}"

if [[ ! -d "${ENV_DIR}" ]]; then
  echo "ERROR: Environment directory not found: environments/${ORG_SLUG}" >&2
  exit 1
fi

# 1. Mandatory pre-flight validation (Schemas, Policy Guardrails, HCL checks)
echo "Step 1/3: Running unified validation suite..."
"${REPO_ROOT}/scripts/validate.sh"

# 2. Resolve OpenTofu binary (prefer `tofu`, fall back to `terraform`)
if command -v tofu >/dev/null 2>&1; then
  TF_BIN="tofu"
elif command -v terraform >/dev/null 2>&1; then
  TF_BIN="terraform"
else
  echo "" >&2
  echo "ERROR: Neither 'tofu' nor 'terraform' was found on PATH." >&2
  echo "Install OpenTofu 1.8.2 via 'mise install' (pinned in mise.toml)." >&2
  exit 1
fi

# 3. Verify in-memory GitHub authentication (Zero-Secret Policy)
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    echo ""
    echo "Step 2/3: Sourcing short-lived GitHub token in memory from 'gh auth token'..."
    GITHUB_TOKEN="$(gh auth token)"
    export GITHUB_TOKEN
  else
    echo "" >&2
    echo "ERROR: GITHUB_TOKEN is not set and 'gh auth status' is not authenticated." >&2
    echo "Run 'gh auth login' or export a short-lived GITHUB_TOKEN in your shell before running plan." >&2
    exit 1
  fi
else
  echo ""
  echo "Step 2/3: Using GITHUB_TOKEN from current shell environment."
fi

# 4. Initialize and execute read-only plan
echo ""
echo "Step 3/3: Running read-only '${TF_BIN} plan' for environments/${ORG_SLUG}..."
"${TF_BIN}" -chdir="${ENV_DIR}" init -input=false
"${TF_BIN}" -chdir="${ENV_DIR}" plan -input=false "$@"
