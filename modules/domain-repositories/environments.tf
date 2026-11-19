# =============================================================================
# Module: domain-repositories — Deployment Environments & Approval Gates
# =============================================================================
# Source: config/orgs/<org>/repos/<domain>.yaml -> defaults.environments / repo.environments
# =============================================================================

locals {
  repository_environments = {
    for item in flatten([
      for repo_name, repo in var.repositories : [
        for env in repo.environments : {
          key                      = "${repo_name}:${env.name}"
          repo_name                = repo_name
          env_name                 = env.name
          require_approval         = env.require_approval
          approver_teams           = env.approver_teams
          deployment_branch_policy = env.deployment_branch_policy
        }
      ]
    ]) : item.key => item
  }
}

resource "github_repository_environment" "this" {
  for_each = local.repository_environments

  repository  = github_repository.this[each.value.repo_name].name
  environment = each.value.env_name

  dynamic "reviewers" {
    for_each = each.value.require_approval && length(each.value.approver_teams) > 0 ? [1] : []
    content {
      teams = [for slug in each.value.approver_teams : tonumber(var.team_ids_by_slug[slug])]
    }
  }

  dynamic "deployment_branch_policy" {
    for_each = each.value.deployment_branch_policy == "protected_branches" ? [1] : []
    content {
      protected_branches     = true
      custom_branch_policies = false
    }
  }
}
