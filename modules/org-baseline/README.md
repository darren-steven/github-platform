# Module: `org-baseline`

Applies organization-wide security baselines, GitHub Actions governance policies, and runner groups from `config/orgs/<org>/org.yaml` and `config/enterprise.yaml`.

## Resources Managed

| Resource | YAML Source | Tier 1 Safeguards |
| :--- | :--- | :--- |
| `github_organization_settings.this` | `org.yaml` → `organization`, `security_dials`; `enterprise.yaml` → `security_settings` | Hardcodes `members_can_create_public_repositories = false`. |
| `github_actions_organization_permissions.this` | `org.yaml` → `actions_dials` | Restricts `allowed_actions` to `"selected"` or `"local_only"`. |
| `github_actions_organization_workflow_permissions.this` | `org.yaml` → `actions_dials` | Hardcodes `default_workflow_permissions = "read"` and `can_approve_pull_request_reviews = false`. |
| `github_actions_runner_group.this` | `org.yaml` → `runner_groups[*]` | Hardcodes `allows_public_repositories = false`. |

## Convention-Only / Portal-Managed Dials

Some governance dials validated in YAML do not have a direct organization-level REST API resource in `integrations/github` and are enforced out-of-band:
- **`enterprise.security_settings.enforce_saml_sso`**: Configured in GitHub Enterprise Cloud / Entra ID SSO settings.
- **`actions_dials.default_job_timeout_minutes`**: Enforced via reusable GitHub Actions workflow templates (`timeout-minutes`).

## Inputs & Outputs

- **Inputs**: `enterprise` (from `config-resolver`), `org` (from `config-resolver`).
- **Outputs**: `organization_slug`, `runner_group_ids`.
