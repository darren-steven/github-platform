# AI Guardrails: OpenTofu Modules (`modules/`)

This file scopes AI assistant behavior when reading, authoring, or refactoring HCL code inside `modules/`. It extends the root [`AGENTS.md`](../AGENTS.md).

## Non-Negotiable Rules for `modules/`

1. **Never Weaken Tier 1 Baselines in HCL**:
   - `github_repository.visibility` must NEVER allow `"public"`.
   - `github_repository.archive_on_destroy` must remain `true` so removing a repository from YAML archives rather than permanently deleting it.
   - `github_team_repository.permission` must NEVER allow `"admin"`.
   - `github_organization_settings.members_can_create_public_repositories` must remain `false`.
   - `github_actions_organization_permissions.default_workflow_permissions` must remain `"read"`, and `can_approve_pull_request_reviews` must remain `false`.
   - `github_repository_ruleset` pull request rules must enforce `dismiss_stale_reviews_on_push = true`, `require_last_push_approval = true`, and `required_approving_review_count >= 2` (`>= 3` for `regulated-workload`).
2. **Zero Secrets in HCL**:
   - Never hardcode tokens, PATs, passwords, or private keys in `.tf` files.
   - `github_actions_variable` is strictly for non-sensitive configuration variables.
3. **Documentation & Inline Clarity**:
   - Every module directory must contain an up-to-date `README.md` with purpose, inputs, outputs, and dial mappings.
   - Every resource block must have a brief header comment linking back to the corresponding YAML dial or Tier 1 baseline.
4. **Mandatory Verification**:
   - Run `./scripts/validate.sh` after any HCL change. Never commit unformatted HCL (`tofu fmt -check`).
