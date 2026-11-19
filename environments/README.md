# OpenTofu Environments (`environments/`)

Each subdirectory under `environments/` is an independent **root OpenTofu stack** corresponding 1:1 to a GitHub Organization under `config/orgs/<org>/`.

## Why One Stack per Organization?

The `integrations/github` provider scopes organization settings, teams, and repositories to a single `owner` (organization slug). Separating each organization into its own root stack:
- **Isolates blast radius and state files** per organization.
- **Mirrors `config/orgs/<org>/`** 1:1 so contributors can immediately locate the stack for any organization.
- **Avoids multi-provider alias complexity** inside reusable modules.

## Active Stacks

| Stack | Config Directory | State Mode | Status |
| :--- | :--- | :--- | :--- |
| [`taswater/`](./taswater/README.md) | [`config/orgs/taswater/`](../config/orgs/taswater/README.md) | Local state (Phase 1 — Plan-Only Alignment) | Active |

## Lifecycle Phases

1. **Phase 1 — Local-State Plan-Only Alignment (Current)**:
   - Uses local state (`backend "local"`) and config-driven `import {}` blocks (`imports.tf`) to diff our YAML configuration against live GitHub without modifying any resources.
   - Run safely via `./scripts/tofu-plan.sh <org>`.
2. **Phase 2 — Production Remote State (Planned)**:
   - Switches `backend.tf` to encrypted Azure Storage remote state with Entra ID / OIDC state locking.
   - Executes `tofu plan` on Pull Requests and gated `tofu apply` on merge to `main`.
