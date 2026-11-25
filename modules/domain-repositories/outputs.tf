# =============================================================================
# Module: domain-repositories — Outputs
# =============================================================================

output "repository_names" {
  description = "List of managed repository names."
  value       = sort(keys(github_repository.this))
}

output "resource_counts" {
  description = "Summary counts of managed repository resources."
  value = {
    repositories        = length(github_repository.this)
    rulesets            = length(github_repository_ruleset.default_branch)
    team_access_links   = length(github_team_repository.this)
    environments        = length(github_repository_environment.this)
    actions_variables   = length(github_actions_variable.this)
    jira_autolinks      = length(github_repository_autolink_reference.jira)
  }
}
