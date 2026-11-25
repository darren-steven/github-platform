# GitHub Actions Workflows (`.github/workflows/`)

This directory contains the CI validation, OpenTofu planning, and manual inventory export workflows for `GHEC-IaC`.

## Workflows

| Workflow | Trigger | Purpose |
| :--- | :--- | :--- |
| [`ci-validate-plan.yml`](./ci-validate-plan.yml) | `pull_request` (`main`), `push` (`main`, `feature/*`, `hotfix/*`) | Runs `./scripts/validate.sh` on every change, and executes read-only `tofu plan` runs for [`environments/taswater/`](../../environments/taswater/README.md) and [`environments/enterprise/`](../../environments/enterprise/README.md) when `vars.TOFU_PLAN_ENABLED == 'true'`. |
| [`export-inventory.yml`](./export-inventory.yml) | Manual (`workflow_dispatch`) | Exports a fresh point-in-time snapshot (`inventory/<org>.inventory.json`), regenerates `environments/<org>/imports.tf` (and optionally `candidates/<org>/`), uploads an Actions artifact, and optionally commits the refreshed files back to the branch. |

## Required Repository Secrets & Variables

- **`secrets.GH_APP_ID`** & **`secrets.GH_APP_PRIVATE_KEY`**: GitHub App credentials used via `actions/create-github-app-token@v2` to mint short-lived installation tokens in memory (never stored on disk).
  - Required read permissions for `export-inventory.yml` and `tofu plan`: Organization `Members: Read`, Organization `Administration: Read`, Repository `Metadata: Read`, Repository `Administration: Read` (needed for branch protections and autolinks), and Repository `Environments: Read`.
- **`vars.TOFU_PLAN_ENABLED`**: Set to `'true'` in repository variables to enable the live OpenTofu plan jobs in `ci-validate-plan.yml`.

## Cross-Platform Case-Sensitivity Safeguards

All workflow inputs (`org`) are automatically normalized to **lowercase** (`taswater`, never `TasWater`) before writing to `inventory/`, `candidates/`, `config/orgs/`, or `environments/`, and verified by `./scripts/validate.sh` so checkouts work identically on Windows, macOS, and Linux.
