# Module: `config-resolver`

A **pure-HCL data transformation module** (creates zero GitHub resources) that loads the declarative YAML configuration for one GitHub Organization and resolves the four-layer inheritance chain.

## Inheritance Precedence (Lowest → Highest)

1. **Enterprise Archetype** (`config/enterprise.yaml` → `archetypes.<name>`)
2. **Organization Defaults** (`config/orgs/<org>/org.yaml` → `repository_defaults`)
3. **Domain Defaults** (`config/orgs/<org>/repos/<domain>.yaml` → `defaults`)
4. **Repository Overrides** (`config/orgs/<org>/repos/<domain>.yaml` → `repositories[*]`)

Jira autolinks are deliberately opt-in per repository: the shared
`enterprise_defaults.jira_autolink.browse_url` is used only when a repository
sets `jira_autolink.project_key`, and a repository `browse_url` overrides the
shared URL.

## Inputs

| Name | Type | Description |
| :--- | :--- | :--- |
| `enterprise_config_path` | `string` | Path to `config/enterprise.yaml`. |
| `org_config_dir` | `string` | Path to `config/orgs/<org>` containing `org.yaml`, `teams.yaml`, and `repos/*.yaml`. |

## Outputs

| Name | Description |
| :--- | :--- |
| `enterprise` | Decoded enterprise metadata and security settings. |
| `org` | Decoded organization metadata, `security_dials`, `actions_dials`, `repository_defaults`, and `runner_groups`. |
| `teams` | Normalized map of GitHub Teams keyed by team `slug`. |
| `repositories` | Fully merged map of repositories across all domain files, keyed by repository `name`; includes an optional Jira autolink resolved from the enterprise browse URL and repository override. |
| `summary` | High-level counts (`team_count`, `domain_count`, `repository_count`) for quick plan verification. |
