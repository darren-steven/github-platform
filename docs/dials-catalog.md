# GitHub Enterprise Cloud Baseline & Dials Catalog

This catalog documents every governance control managed in `config/`, classified into:

- **Tier 1 — Immutable Baselines**: Locked by JSON Schemas (`schemas/`) and OPA/Python policies (`policies/`, `scripts/`). Cannot be weakened via YAML configuration.
- **Tier 2 — Bounded Dials**: Exposed in `config/**/*.yaml` and constrained within safe security bounds.
- **Tier 3 — Self-Service Catalogs**: Teams (`teams.yaml`) and domain-grouped repositories (`repos/<domain>.yaml`).

---

## 1. Tier 1: Immutable Baselines (Locked in Schemas & Policies)

| Domain | Control / Invariant | Enforced Value | Enforcing Schema / Policy | Security Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Enterprise Security** | `enforce_saml_sso` | `true` | `enterprise.schema.json` & `ENT-BASELINE-001` | Mandates Entra ID SAML/OIDC authentication across the enterprise. |
| **Enterprise Security** | `members_can_create_public_repositories` | `false` | `enterprise.schema.json` & `ENT-BASELINE-002` | Prevents accidental public exposure of intellectual property or source code. |
| **Repository Visibility** | `visibility` | `"private"` or `"internal"` | `domain-repos.schema.json` | Public repositories are blocked at the schema level across all archetypes. |
| **Repository Access** | `team_access[].permission` | `"pull"`, `"triage"`, `"push"`, `"maintain"` | `domain-repos.schema.json` | Blocks repository `"admin"` permissions for teams so branch rulesets and security settings remain strictly governed by IaC. |
| **Branch Protection** | `dismiss_stale_reviews` & `require_last_push_approval` | `true`, `true` | `enterprise.schema.json` & `domain-repos.schema.json` | Enforces true four-eyes review; pushing new commits resets approvals and the last pusher cannot self-approve. |
| **GitHub Actions** | `default_workflow_permissions` & `can_approve_pull_request_reviews` | `"read"`, `false` | `org.schema.json` & `ORG-BASELINE-006/007` | Scopes `GITHUB_TOKEN` to read-only by default and prevents workflows from approving pull requests. |
| **Advanced Security** | `secret_scanning`, `secret_scanning_push_protection`, `dependabot_alerts` | `true` (non-sandbox) | `repo_guardrails.rego` (`REPO-POLICY-003`) | Blocks credential leaks at push time and tracks vulnerable dependencies on all production/shared archetypes. |
| **Deployments** | Production Environment Approval (`prod` / `production`) | `require_approval: true` + valid `approver_teams` | `repo_guardrails.rego` (`REPO-POLICY-004/005`) | Requires approval from a designated maintainer team before production deployment. |
| **Secrets Management** | Plain-text secrets in `environment_variables` | Blocked (`REPO-POLICY-007`) | `repo_guardrails.rego` | Prevents tokens, passwords, or keys from being committed in YAML; mandates GitHub Encrypted Secrets / Azure Key Vault OIDC. |

---

## 2. Tier 2: Exposed Organization Dials (`config/orgs/<org>/org.yaml`)

> **Approval Requirement**: Changes to `config/orgs/<org>/org.yaml` affect the entire GitHub Organization and require Platform Admin review.

| YAML Path | Type | Default | Allowed Bounds | Description & Blast Radius |
| :--- | :--- | :--- | :--- | :--- |
| `organization.default_archetype` | `string` | `"standard-microservice"` | `"standard-microservice"`, `"regulated-workload"`, `"shared-library"`, `"sandbox"` | Default archetype for repositories in the organization. |
| `security_dials.members_can_create_private_repositories` | `boolean` | `false` | `true` / `false` | Whether members can create unmanaged private repos outside IaC. |
| `security_dials.members_can_create_internal_repositories` | `boolean` | `false` | `true` / `false` | Whether members can create unmanaged internal repos outside IaC. |
| `security_dials.members_can_fork_private_repositories` | `boolean` | `false` | `true` / `false` | Whether members can fork private/internal repositories. |
| `security_dials.web_commit_signoff_required` | `boolean` | `false` | `true` / `false` | Requires DCO sign-off on web-based commits. |
| `actions_dials.allowed_actions` | `string` | `"selected"` | `"selected"`, `"local_only"` | Restricts reusable Actions to verified/selected patterns or local-only. |
| `actions_dials.sha_pinning_required` | `boolean` | `true` | `true` / `false` | Requires third-party GitHub Actions to be pinned to a full commit SHA. |
| `actions_dials.default_job_timeout_minutes` | `integer` | `60` | `15` .. `180` | Default workflow job timeout in minutes (`ORG-BASELINE-004/005`). |
| `repository_defaults.min_reviewers` | `integer` | `2` | `2` .. `5` | Organization default minimum approving reviews on `main` PRs. |
| `repository_defaults.allowed_merge_types.*` | `object` | `squash: true`, `merge_commit: true` | At least 1 merge strategy `true` | Controls default allowed PR merge methods (`squash`, `merge_commit`, `rebase`, `auto_merge`, `delete_branch_on_merge`). |

---

## 3. Tier 2 & Tier 3: Repository Archetypes (`config/enterprise.yaml` & `config/orgs/<org>/repos/<domain>.yaml`)

> **Approval Requirement**: Changes to `config/orgs/<org>/repos/<domain>.yaml` are scoped to a domain/repository and can be approved by Maintainers.

| Archetype | Default Visibility | `min_reviewers` Bound | `require_signed_commits` | `code_scanning_default_setup` | Intended Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `standard-microservice` | `private` | `2` .. `5` (Default: `2`) | `false` (Optional) | `true` | Standard engineering microservices, APIs, workers, and web apps. |
| `regulated-workload` | `private` | **`3` .. `5`** (Enforced >= 3) | **`true`** (Enforced) | `true` | High-compliance, identity, financial, payment, or OT/SCADA workloads. |
| `shared-library` | `internal` | `2` .. `5` (Default: `2`) | `false` (Optional) | `true` | Inner-source SDKs, UI design systems, and shared libraries visible across both enterprise orgs. |
| `sandbox` | `private` | `2` .. `5` (Default: `2`) | `false` | `false` | Non-production proofs of concept and prototypes isolated from production environments. |

### Per-Repository & Domain Dials (`config/orgs/<org>/repos/<domain>.yaml`)

| YAML Path | Type | Allowed Bounds | Description |
| :--- | :--- | :--- | :--- |
| `defaults.archetype` / `repositories[].archetype` | `string` | `"standard-microservice"`, `"regulated-workload"`, `"shared-library"`, `"sandbox"` | Selects the baseline governance archetype. |
| `defaults.team_access` / `repositories[].team_access` | `array` | `permission` in `["pull", "triage", "push", "maintain"]` | Maps organization team slugs (from `teams.yaml`) to repository permissions. |
| `repositories[].branch_protection.min_reviewers` | `integer` | `2` .. `5` (`3` .. `5` for `regulated-workload`) | Overrides required approving reviewer count on `main`. |
| `repositories[].merge_strategies.*` | `object` | At least 1 of `allow_squash_merge`, `allow_merge_commit`, `allow_rebase_merge` = `true` | Overrides allowed PR merge methods for a specific repository. |
| `repositories[].required_status_checks` | `array<string>` | Non-empty strings | CI status check contexts required to pass before merging to `main`. |
| `repositories[].codeowners_teams` | `array` | Valid path (`/...`) + team slugs in `teams.yaml` | Path-scoped CODEOWNERS team review rules. |
| `defaults.environments` / `repositories[].environments` | `array` | `prod` requires `require_approval: true` & `approver_teams` | Configures deployment environments (`dev`, `staging`, `prod`) and required reviewer teams. |
