# =============================================================================
# Module: enterprise-baseline — Outputs
# =============================================================================

output "enterprise_slug" {
  description = "GitHub Enterprise slug."
  value       = data.github_enterprise.this.slug
}

output "enterprise_id" {
  description = "GitHub Enterprise ID."
  value       = data.github_enterprise.this.id
}

output "enterprise_defaults_summary" {
  description = "Summary of active Enterprise-wide policy ceilings from config/enterprise.yaml."
  value = {
    copilot_policy_mode           = local.enterprise_defaults.copilot.policy_mode
    copilot_public_code_policy    = local.enterprise_defaults.copilot.public_code_suggestions
    codespaces_policy_mode        = local.enterprise_defaults.codespaces.policy_mode
    codespaces_max_idle_minutes   = local.enterprise_defaults.codespaces.max_idle_timeout_minutes
    codespaces_max_retention_days = local.enterprise_defaults.codespaces.max_retention_period_days
    max_org_monthly_budget_usd    = local.enterprise_defaults.billing.max_org_monthly_budget_usd
    enterprise_runner_group_count = length(local.runner_groups)
  }
}
