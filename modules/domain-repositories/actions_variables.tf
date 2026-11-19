# =============================================================================
# Module: domain-repositories — Non-Sensitive GitHub Actions Variables
# =============================================================================
# Source: config/orgs/<org>/repos/<domain>.yaml -> repositories[*].environment_variables
# Guardrail: Strictly for non-sensitive values. Secret key names are rejected by
# policies/repo_guardrails.rego and scripts/validate_config.py.
# =============================================================================

locals {
  repository_actions_variables = {
    for item in flatten([
      for repo_name, repo in var.repositories : [
        for var_name, var_value in repo.environment_variables : {
          key       = "${repo_name}:${var_name}"
          repo_name = repo_name
          var_name  = var_name
          var_value = var_value
        }
      ]
    ]) : item.key => item
  }
}

resource "github_actions_variable" "this" {
  for_each = local.repository_actions_variables

  repository    = github_repository.this[each.value.repo_name].name
  variable_name = each.value.var_name
  value         = each.value.var_value
}
