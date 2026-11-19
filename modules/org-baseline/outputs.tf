# =============================================================================
# Module: org-baseline — Outputs
# =============================================================================

output "organization_slug" {
  description = "Managed GitHub Organization slug."
  value       = var.org.organization.slug
}

output "runner_group_ids" {
  description = "Map of organization runner group names to their GitHub IDs."
  value       = { for name, rg in github_actions_runner_group.this : name => rg.id }
}
