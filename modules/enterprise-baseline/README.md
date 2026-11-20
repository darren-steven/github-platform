# Module: `enterprise-baseline`

Manages **GitHub Enterprise Cloud** enterprise-level resources natively supported by the `integrations/github` provider, sourced from [`config/enterprise.yaml`](../../config/enterprise.yaml).

## Resources Managed (Native `integrations/github`)

| Resource | YAML Source | Tier 1 Safeguards |
| :--- | :--- | :--- |
| `data.github_enterprise.this` | `enterprise.yaml` → `enterprise.slug` | Resolves the canonical Enterprise ID for downstream enterprise resources. |
| `github_enterprise_actions_runner_group.this` | `enterprise.yaml` → `enterprise_defaults.actions.runner_groups[*]` | Hardcodes `allows_public_repositories = false`. |

## Planned Follow-Up (REST API Bridge)

Enterprise-level Copilot policy ceilings, Codespaces policy ceilings, and per-organization metered billing budgets (`copilot_dials`, `codespaces_dials`, `billing_budgets`) are validated today by JSON Schema, OPA Rego, and `scripts/validate_config.py`. Programmatic enforcement via the GitHub REST API will be added in an isolated `modules/github-api-bridge/` module once Phase 1 alignment is complete.
