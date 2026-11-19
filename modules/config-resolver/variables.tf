# =============================================================================
# Module: config-resolver — Input Variables
# =============================================================================

variable "enterprise_config_path" {
  type        = string
  description = "Relative or absolute path to config/enterprise.yaml (archetype catalog & enterprise baselines)."
}

variable "org_config_dir" {
  type        = string
  description = "Path to the organization config directory (e.g., ../../config/orgs/taswater) containing org.yaml, teams.yaml, and repos/*.yaml."
}
