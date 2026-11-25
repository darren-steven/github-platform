# =============================================================================
# Environment: enterprise — Input Variables
# =============================================================================

variable "enterprise_config_path" {
  type        = string
  default     = "../../config/enterprise.yaml"
  description = "Path to config/enterprise.yaml."
}


variable "org_config_dir" {
  type        = string
  default     = "../../config/orgs/taswater"
  description = "Path to the organization configuration directory (org.yaml, teams.yaml, repos/*.yaml)."
}