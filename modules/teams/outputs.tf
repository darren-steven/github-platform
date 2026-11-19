# =============================================================================
# Module: teams — Outputs
# =============================================================================

output "team_ids_by_slug" {
  description = "Map of YAML team slug to GitHub numeric team ID (used by repository team_access and environment reviewers)."
  value       = { for slug, team in local.all_teams : slug => team.id }
}

output "team_slugs" {
  description = "Map of YAML team slug to GitHub resolved team slug."
  value       = { for slug, team in local.all_teams : slug => team.slug }
}
