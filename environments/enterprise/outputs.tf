# =============================================================================
# Environment: enterprise — Plan Summary Outputs
# =============================================================================

output "enterprise_slug" {
  description = "Managed GitHub Enterprise slug."
  value       = module.enterprise_baseline.enterprise_slug
}

output "enterprise_defaults_summary" {
  description = "Active Enterprise-wide defaults and FinOps ceilings."
  value       = module.enterprise_baseline.enterprise_defaults_summary
}
