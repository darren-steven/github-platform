# =============================================================================
# Module: org-baseline — Organization Runner Groups
# =============================================================================
# Source: config/orgs/<org>/org.yaml -> runner_groups[*]
# Tier 1 Immutable Baseline: allows_public_repositories is always false.
# =============================================================================

resource "github_actions_runner_group" "this" {
  for_each = { for rg in var.org.runner_groups : rg.name => rg }

  name                       = each.value.name
  visibility                 = each.value.visibility
  allows_public_repositories = false
}
