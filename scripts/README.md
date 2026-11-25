# Validation, Extraction & OpenTofu Helper Scripts (`scripts/`)

This directory contains the local validation harness, GitHub REST API inventory exporter, domain candidate generator, OpenTofu import generator, and read-only plan wrapper.

## Script Catalog

| Script | Purpose | Typical Invocation |
| :--- | :--- | :--- |
| [`validate.sh`](./validate.sh) | Unified 4-layer validation suite (JSON Schemas, OPA/Python policies, regression + HCL checks, AI skills & cross-platform path casing). | `./scripts/validate.sh` |
| [`validate_config.py`](./validate_config.py) | Validates `config/enterprise.yaml` and `config/orgs/**` against `schemas/*.schema.json`, referential integrity, and FinOps/security policies. | Called by `validate.sh` |
| [`validate_hcl.py`](./validate_hcl.py) | Verifies Tier 1 HCL invariants, `README.md`/`AGENTS.md` completeness across `modules/` & `environments/`, and `tofu fmt -check`. | Called by `validate.sh` |
| [`validate_agent_guardrails.py`](./validate_agent_guardrails.py) | Verifies `.agents/skills/*/SKILL.md` parity, blocks machine-local paths, and enforces lowercase org/domain/stack paths to prevent Windows/macOS case collisions. | Called by `validate.sh` |
| [`export_github_inventory.py`](./export_github_inventory.py) | Read-only GitHub REST API exporter with real-time stderr progress logging (`--quiet` to suppress). Writes `inventory/<org>.inventory.json`. | `python3 scripts/export_github_inventory.py --org taswater` |
| [`generate_config_candidates.py`](./generate_config_candidates.py) | Deduces domain-grouped YAML files (`candidates/<org>/repos/*.yaml`) and `drift-report.md` from an inventory JSON snapshot. | `python3 scripts/generate_config_candidates.py --inventory inventory/taswater.inventory.json` |
| [`generate_imports.py`](./generate_imports.py) | Generates config-driven OpenTofu 1.8 `import {}` blocks (`environments/<org>/imports.tf`) for teams, repos, Dependabot, team access, and Jira autolinks. | `python3 scripts/generate_imports.py --org taswater` |
| [`tofu-plan.sh`](./tofu-plan.sh) | Safe read-only local wrapper (`validate.sh` → `tofu init` → `tofu plan`) using an in-memory `GITHUB_TOKEN`. | `./scripts/tofu-plan.sh taswater` |
| [`test_inventory_and_candidates.py`](./test_inventory_and_candidates.py) | Offline regression test suite covering extraction, domain deduction, Jira autolinks, progress logging, and path case-collision detection. | Called by `validate.sh` |

## Cross-Platform Path Rule (Windows / macOS / Linux)

Always use **lowercase** slugs (`taswater`) for paths on disk. Even if a GitHub Organization's display login is `TasWater`, all CLI scripts normalize `--org` to lowercase and `validate_agent_guardrails.py` rejects mixed-case paths (`[PATH-UPPERCASE-SLUG]` / `[PATH-CASE-COLLISION]`).
