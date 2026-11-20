# =============================================================================
# Module: enterprise-baseline — Native Enterprise Resources
# =============================================================================
# Source: config/enterprise.yaml -> enterprise, enterprise_defaults.actions
# =============================================================================

data "github_enterprise" "this" {
  slug = local.enterprise_meta.slug
}

# -----------------------------------------------------------------------------
# Enterprise-Level Actions Runner Groups
# Tier 1 Immutable Baseline: allows_public_repositories is always false.
# -----------------------------------------------------------------------------
resource "github_enterprise_actions_runner_group" "this" {
  for_each = { for rg in local.runner_groups : rg.name => rg }

  enterprise_slug            = data.github_enterprise.this.slug
  name                       = each.value.name
  visibility                 = each.value.visibility
  allows_public_repositories = false
}
