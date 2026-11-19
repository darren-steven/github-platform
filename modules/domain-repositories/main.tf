# =============================================================================
# Module: domain-repositories — Repositories & Security Settings
# =============================================================================
# Source: config/orgs/<org>/repos/<domain>.yaml (merged with enterprise archetypes)
# =============================================================================

resource "github_repository" "this" {
  for_each = var.repositories

  name        = each.value.name
  description = each.value.description
  visibility  = each.value.visibility
  topics      = each.value.topics

  # Repository feature toggles (from archetype + optional repo override)
  has_issues      = each.value.features.has_issues
  has_wiki        = each.value.features.has_wiki
  has_discussions = each.value.features.has_discussions
  has_projects    = each.value.features.has_projects

  # Pull request merge strategies (from archetype + optional repo override)
  allow_squash_merge     = each.value.merge_strategies.allow_squash_merge
  allow_merge_commit     = each.value.merge_strategies.allow_merge_commit
  allow_rebase_merge     = each.value.merge_strategies.allow_rebase_merge
  allow_auto_merge       = each.value.merge_strategies.allow_auto_merge
  delete_branch_on_merge = each.value.merge_strategies.delete_branch_on_merge

  # Dependabot vulnerability alerts
  vulnerability_alerts = each.value.security.dependabot_alerts

  # GitHub Advanced Security (Secret Scanning & Push Protection)
  security_and_analysis {
    secret_scanning {
      status = each.value.security.secret_scanning ? "enabled" : "disabled"
    }
    secret_scanning_push_protection {
      status = each.value.security.secret_scanning_push_protection ? "enabled" : "disabled"
    }
  }

  # Tier 1 Safety Net: Removing a repository from YAML archives it rather than deleting it
  archive_on_destroy = true
}

# -----------------------------------------------------------------------------
# Dependabot Automated Security Updates
# Source: archetype.security.dependabot_security_updates (+ optional repo override)
# -----------------------------------------------------------------------------
resource "github_repository_dependabot_security_updates" "this" {
  for_each = var.repositories

  repository = github_repository.this[each.key].name
  enabled    = each.value.security.dependabot_security_updates
}
