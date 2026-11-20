# =============================================================================
# Module: enterprise-baseline — Input Variables & Tier 1 Validations
# =============================================================================

variable "enterprise_config_path" {
  type        = string
  description = "Path to config/enterprise.yaml."
}

locals {
  enterprise_raw      = yamldecode(file(var.enterprise_config_path))
  enterprise_meta     = local.enterprise_raw.enterprise
  security_settings   = local.enterprise_raw.security_settings
  enterprise_defaults = local.enterprise_raw.enterprise_defaults
  runner_groups       = try(local.enterprise_defaults.actions.runner_groups, [])
}
