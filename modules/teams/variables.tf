# =============================================================================
# Module: teams — Input Variables
# =============================================================================

variable "teams" {
  description = "Normalized map of GitHub Teams keyed by slug from modules/config-resolver."
  type = map(object({
    slug         = string
    name         = string
    description  = string
    privacy      = string
    role_tier    = string
    parent_team  = optional(string)
    idp_group_id = optional(string)
    maintainers  = optional(list(string), [])
    members      = optional(list(string), [])
  }))

  validation {
    condition     = alltrue([for _, t in var.teams : t.privacy == "closed"])
    error_message = "Tier 1 Baseline Violation: All GitHub Teams must use privacy = 'closed' to support nesting and CODEOWNERS."
  }
}
