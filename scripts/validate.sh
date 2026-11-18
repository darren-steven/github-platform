#!/usr/bin/env bash
# =============================================================================
# Unified Validation Harness (`scripts/validate.sh`)
# =============================================================================
# Runs the multi-layer guardrail checks for GitHub Enterprise Cloud IaC:
#   Layer 1: YAML Syntax, JSON Schema & Cross-File Referential Validation (`schemas/*.schema.json`)
#   Layer 2: Baseline & Archetype Policy Gate (`policies/*.rego` + Python check)
#   Layer 3: Inventory Extraction & Candidate Generation Regression Tests
#   Layer 4: Cross-Agent AI Skill & Prompt Synchronization Check
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

echo "============================================================================="
echo " GitHub Enterprise Cloud Governance & Validation Suite"
echo "============================================================================="

# -----------------------------------------------------------------------------
# Layer 1 & 2: Schema Validation + Policy Invariant & Cross-File Gate
# -----------------------------------------------------------------------------
echo ""
echo "[1/4] Validating YAML Configurations against JSON Schemas & Policy Guardrails..."
python3 "${REPO_ROOT}/scripts/validate_config.py"

# -----------------------------------------------------------------------------
# Optional Conftest / OPA CLI Execution (if installed)
# -----------------------------------------------------------------------------
if command -v conftest >/dev/null 2>&1; then
  echo ""
  echo "[2/4] Running Conftest Rego Policies..."
  conftest test config/enterprise.yaml -p policies/enterprise_baseline.rego
  conftest test config/orgs/*/org.yaml -p policies/org_baseline.rego
  conftest test config/orgs/*/repos/*.yaml -p policies/repo_guardrails.rego
else
  echo ""
  echo "[2/4] Conftest CLI not found on PATH (Rego rules verified via built-in policy engine in Step 1)."
fi

# -----------------------------------------------------------------------------
# Layer 3: Inventory Extraction & Candidate Generator Regression Suite
# -----------------------------------------------------------------------------
echo ""
echo "[3/4] Running Inventory Extraction & Domain Deduction Regression Tests..."
python3 "${REPO_ROOT}/scripts/test_inventory_and_candidates.py"
python3 "${REPO_ROOT}/scripts/validate_hcl.py"

# -----------------------------------------------------------------------------
# Layer 4: Cross-Agent AI Skill & Guardrail Integrity Check (Gemini + Copilot)
# -----------------------------------------------------------------------------
echo ""
echo "[4/4] Verifying Unified Agent Skills (.agents/skills/) & Cross-Agent Guardrails..."
python3 "${REPO_ROOT}/scripts/validate_agent_guardrails.py"

echo ""
echo "============================================================================="
echo " ALL GUARDRAIL & VALIDATION CHECKS PASSED"
echo "============================================================================="
