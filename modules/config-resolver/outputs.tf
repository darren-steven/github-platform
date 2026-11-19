# =============================================================================
# Module: config-resolver — Outputs
# =============================================================================

output "enterprise" {
  description = "Decoded enterprise metadata and Tier 1 security settings from config/enterprise.yaml."
  value = {
    slug                  = local.enterprise_raw.enterprise.slug
    name                  = local.enterprise_raw.enterprise.name
    url                   = local.enterprise_raw.enterprise.url
    managed_organizations = local.enterprise_raw.enterprise.managed_organizations
    security_settings     = local.enterprise_raw.security_settings
  }
}

output "org" {
  description = "Decoded organization dials from config/orgs/<org>/org.yaml."
  value = {
    organization        = local.org_raw.organization
    security_dials      = local.org_raw.security_dials
    actions_dials       = local.org_raw.actions_dials
    repository_defaults = local.org_raw.repository_defaults
    runner_groups       = try(local.org_raw.runner_groups, [])
  }
}

output "teams" {
  description = "Map of normalized GitHub Teams keyed by team slug."
  value       = local.teams_by_slug
}

output "repositories" {
  description = "Map of fully resolved GitHub repositories across all domain files, keyed by repository name."
  value       = local.repositories_by_name
}

output "summary" {
  description = "High-level resource counts resolved from YAML for plan verification."
  value = {
    organization     = local.org_raw.organization.slug
    team_count       = length(local.teams_by_slug)
    domain_count     = length(local.domain_files)
    repository_count = length(local.repositories_by_name)
  }
}
