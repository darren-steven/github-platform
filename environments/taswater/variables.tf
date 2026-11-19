# =============================================================================
# Environment: taswater — Input Variables
# =============================================================================

variable "enterprise_config_path" {
  type        = string
  default     = "../../config/enterprise.yaml"
  description = "Path to the canonical enterprise baseline and archetype catalog."
}

variable "org_config_dir" {
  type        = string
  default     = "../../config/orgs/taswater"
  description = "Path to the organization configuration directory (org.yaml, teams.yaml, repos/*.yaml)."
}
