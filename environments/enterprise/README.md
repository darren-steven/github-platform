# Environment Stack: `enterprise` (Enterprise-Wide Baseline)

This root OpenTofu stack manages **GitHub Enterprise Cloud** settings defined in [`config/enterprise.yaml`](../../config/enterprise.yaml) that require Enterprise-scoped authentication, keeping them isolated from per-organization stacks (`environments/<org>/`).

## Why a Separate Enterprise Stack?

- **Least-Privilege Auth**: Per-organization stacks (`environments/taswater/`) never need Enterprise Owner or Enterprise Billing tokens.
- **Blast-Radius Isolation**: Enterprise-wide runner groups and policy ceilings live in their own state file and require Platform Admin review.

## How to Run a Safe Local Plan (Read-Only)

```bash
gh auth login
export GITHUB_TOKEN="$(gh auth token)"
./scripts/tofu-plan.sh enterprise
```

> **Note**: Phase 1 uses local state (`backend "local"`) and manages native `integrations/github` enterprise resources (`data.github_enterprise`, `github_enterprise_actions_runner_group`). REST API enforcement for enterprise Copilot/Codespaces policies and per-organization billing budgets will be wired in a follow-up `modules/github-api-bridge/` pass.
