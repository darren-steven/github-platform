# Module: `domain-repositories`

Provisions and governs GitHub repositories across all domain files (`config/orgs/<org>/repos/<domain>.yaml`) using fully resolved inputs from [`modules/config-resolver`](../config-resolver/README.md).

## File Organization

| File | Responsibility | GitHub Resources |
| :--- | :--- | :--- |
| [`main.tf`](./main.tf) | Repository creation, visibility, features, merge strategies, and GHAS/Dependabot security. | `github_repository`, `github_repository_dependabot_security_updates` |
| [`branch_protection.tf`](./branch_protection.tf) | Modern GitHub Repository Rulesets targeting `~DEFAULT_BRANCH`. | `github_repository_ruleset` |
| [`team_access.tf`](./team_access.tf) | Least-privilege team permission assignments (`pull`, `triage`, `push`, `maintain`). | `github_team_repository` |
| [`environments.tf`](./environments.tf) | Deployment environments (`dev`, `staging`, `prod`), reviewer gates, and branch policies. | `github_repository_environment` |
| [`actions_variables.tf`](./actions_variables.tf) | Non-sensitive repository GitHub Actions variables. | `github_actions_variable` |
| [`autolinks.tf`](./autolinks.tf) | Optional per-repository Jira issue references using an enterprise default or repository-specific browse URL. | `github_repository_autolink_reference` |

The `resource_counts` output includes `jira_autolinks` for the number of enabled
repository references.

## Tier 1 Safeguards Enforced in HCL

- **No Public Repositories**: Variable validation blocks `visibility == "public"`.
- **Safe Destruction (`archive_on_destroy = true`)**: Removing a repository from YAML archives it instead of permanently deleting it.
- **No Team Admin Access**: Variable validation blocks `permission == "admin"` in `team_access`.
- **Mandatory PR Review Controls**: Rulesets enforce `dismiss_stale_reviews_on_push = true`, `require_last_push_approval = true`, `deletion = true`, `non_fast_forward = true`, and `required_approving_review_count >= 2` (`>= 3` for `regulated-workload`).

## Notes on Opt-In Features

- **`codeowners_teams`**: Validated in YAML and passed through `config-resolver`. Managing `.github/CODEOWNERS` commits via `github_repository_file` is intentionally deferred until after initial plan-only alignment so no unexpected commits are proposed across existing repositories.
- **`security.code_scanning_default_setup`**: Tracked in YAML and enforced via GitHub Advanced Security org/repo configuration policies.
- **`jira_autolink.project_key`**: Opts a repository into a Jira autolink. The module generates a numeric issue reference using the enterprise `browse_url` default or the repository override.
- **Permissions**: The GitHub App used for planning/managing autolinks needs repository `Administration` permission; use the least level that supports the operation (read to inspect, write to manage).

Example opt-in:

```yaml
jira_autolink:
  project_key: PPLCTNS
  # Optional; defaults to enterprise_defaults.jira_autolink.browse_url
  browse_url: https://taswater-applications.atlassian.net/browse
```

This config generates `key_prefix = "PPLCTNS-"` and a target URL template ending in `/PPLCTNS-<num>`, so `PPLCTNS-23` links to the Jira issue.
