# Environment Stack: `taswater` (Phase 1 — Plan-Only Alignment)

This root OpenTofu stack compiles [`config/orgs/taswater/`](../../config/orgs/taswater/README.md) and [`config/enterprise.yaml`](../../config/enterprise.yaml) into an execution plan against the **`taswater`** GitHub Organization.

## Stack Files

| File | Purpose |
| :--- | :--- |
| [`versions.tf`](./versions.tf) | Pins OpenTofu `>= 1.8.0` and `integrations/github` `~> 6.6`. |
| [`backend.tf`](./backend.tf) | Configures local state for Phase 1 development, with a commented Azure Storage remote-state blueprint for Phase 2. |
| [`providers.tf`](./providers.tf) | Configures the `github` provider scoped to `taswater` (reads `GITHUB_TOKEN` from environment). |
| [`variables.tf`](./variables.tf) | Declares paths to `config/enterprise.yaml` and `config/orgs/taswater`. |
| [`main.tf`](./main.tf) | Wires `config-resolver` → `org-baseline`, `teams`, and `domain-repositories`. |
| [`imports.tf`](./imports.tf) | Config-driven `import {}` blocks generated from `inventory/taswater.inventory.json` so `tofu plan` diffs existing GitHub resources in-place. |
| [`outputs.tf`](./outputs.tf) | Prints concise counts of resolved teams, domains, repositories, rulesets, and environments. |

## How to Run a Safe Local Plan (Read-Only)

1. **Authenticate** in your terminal (token stays in memory only — never written to disk):
   ```bash
   gh auth login
   export GITHUB_TOKEN="$(gh auth token)"
   ```
2. **Run the unified plan wrapper** from the repository root:
   ```bash
   ./scripts/tofu-plan.sh taswater
   ```
   This script automatically:
   - Runs `./scripts/validate.sh` (JSON Schema, cross-file integrity, OPA policy, and HCL guardrails).
   - Runs `tofu init` inside `environments/taswater/`.
   - Runs `tofu plan` (read-only) and displays exact in-place diffs (`~`) against live GitHub.
3. **Refresh `imports.tf`** if you rename or reorganize teams/repositories during alignment:
   ```bash
   python3 scripts/generate_imports.py --org taswater
   ```
