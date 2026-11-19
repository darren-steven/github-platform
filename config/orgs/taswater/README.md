# TasWater Organization Configuration (`config/orgs/taswater`)

This directory holds the declarative GitHub Organization configuration for **`taswater`**, promoted from [`candidates/taswater/`](../../../candidates/taswater/) for OpenTofu plan-only alignment and ongoing governance.

## Directory Layout

| Path | Schema | Purpose |
| :--- | :--- | :--- |
| [`org.yaml`](./org.yaml) | [`schemas/org.schema.json`](../../../schemas/org.schema.json) | Organization-wide security dials, GitHub Actions token limits, default branch rules, and runner groups. |
| [`teams.yaml`](./teams.yaml) | [`schemas/teams.schema.json`](../../../schemas/teams.schema.json) | Canonical registry of GitHub Teams, parent/child hierarchy, and Entra ID IdP group mappings. |
| `repos/<domain>.yaml` | [`schemas/domain-repos.schema.json`](../../../schemas/domain-repos.schema.json) | Domain-grouped repositories with shared `defaults` and optional per-repository overrides. |

## Quick Workflow

1. Edit any YAML file here — VS Code provides real-time autocompletion and bound checks via `# yaml-language-server: $schema=...` and [`.vscode/settings.json`](../../../.vscode/settings.json).
2. Validate your changes locally:
   ```bash
   ./scripts/validate.sh
   ```
3. Preview live drift against GitHub without applying changes:
   ```bash
   ./scripts/tofu-plan.sh taswater
   ```
