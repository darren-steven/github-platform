# =============================================================================
# Module: domain-repositories — Team Permission Assignments
# =============================================================================
# Source: config/orgs/<org>/repos/<domain>.yaml -> defaults.team_access / repo.team_access
# Tier 1 Baseline: 'admin' is blocked at schema, policy, and HCL validation layers.
# =============================================================================

locals {
  team_repo_assignments = {
    for item in flatten([
      for repo_name, repo in var.repositories : [
        for ta in repo.team_access : {
          key        = "${repo_name}:${ta.team}"
          repo_name  = repo_name
          team       = ta.team
          permission = ta.permission
        }
      ]
    ]) : item.key => item
  }
}

resource "github_team_repository" "this" {
  for_each = local.team_repo_assignments

  team_id    = var.team_ids_by_slug[each.value.team]
  repository = github_repository.this[each.value.repo_name].name
  permission = each.value.permission
}
