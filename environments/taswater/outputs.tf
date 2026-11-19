# =============================================================================
# Environment: taswater — Plan & Alignment Summary Outputs
# =============================================================================

output "config_summary" {
  description = "Summary of YAML configuration objects loaded by modules/config-resolver."
  value       = module.config.summary
}

output "repository_resource_counts" {
  description = "Counts of GitHub repository resources managed by modules/domain-repositories."
  value       = module.repositories.resource_counts
}
