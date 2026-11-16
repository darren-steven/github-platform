#!/usr/bin/env bash
# =============================================================================
# Unified Validation Harness (`scripts/validate.sh`)
# =============================================================================
# Runs the multi-layer guardrail checks for AzDo-IaC:
#   Layer 1: YAML Syntax & JSON Schema Validation (`schemas/*.schema.json`)
#   Layer 2: Baseline & Archetype Policy Gate (`policies/*.rego` + Python check)
#   Layer 3: OpenTofu Formatting & Structural Validation (`modules/`, `environments/`)
#   Layer 4: Cross-Agent AI Skill & Prompt Synchronization Check
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

echo "============================================================================="
echo " AzDo-IaC Guardrails & Validation Suite"
echo "============================================================================="

# -----------------------------------------------------------------------------
# Layer 1 & 2: Schema Validation + Policy Invariant Gate
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
  conftest test config/org.yaml -p policies/org_baseline.rego
  conftest test config/projects/*.yaml -p policies/project_guardrails.rego
else
  echo ""
  echo "[2/4] Conftest CLI not found on PATH (Rego rules verified via built-in policy engine in Step 1)."
fi

# -----------------------------------------------------------------------------
# Layer 3: OpenTofu / Terraform Structural & Format Check
# -----------------------------------------------------------------------------
echo ""
echo "[3/4] Checking OpenTofu / HCL Structure & Guardrails..."

if command -v tofu >/dev/null 2>&1; then
  tofu fmt -check -recursive modules/ environments/
  echo "  PASS: OpenTofu formatting check passed."
elif command -v terraform >/dev/null 2>&1; then
  terraform fmt -check -recursive modules/ environments/
  echo "  PASS: Terraform formatting check passed."
else
  echo "  INFO: 'tofu' binary not installed in current environment; running static HCL guardrail inspection..."
fi

# Static HCL Guardrail Inspection: Verify Tier 1 hardcoded invariants in modules/
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
