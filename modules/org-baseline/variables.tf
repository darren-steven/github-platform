# =============================================================================
# Module: org-baseline — Input Variables
# =============================================================================

variable "enterprise" {
  description = "Resolved enterprise configuration from modules/config-resolver."
  type = object({
    slug = string
    security_settings = object({
      enforce_saml_sso                       = bool
      default_repository_permission          = string
      members_can_create_public_repositories = bool
    })
  })

  validation {
    condition     = var.enterprise.security_settings.members_can_create_public_repositories == false
    error_message = "Tier 1 Baseline Violation: members_can_create_public_repositories must be false."
  }

  validation {
    condition     = contains(["none", "read"], var.enterprise.security_settings.default_repository_permission)
    error_message = "Tier 1 Baseline Violation: default_repository_permission must be 'none' or 'read'."
  }
}

variable "org" {
  description = "Resolved organization configuration from modules/config-resolver."
  type = object({
    organization = object({
      slug              = string
      name              = string
      description       = string
      billing_email     = string
      default_archetype = string
    })
    security_dials = object({
      members_can_create_private_repositories                      = bool
      members_can_create_internal_repositories                     = bool
      members_can_fork_private_repositories                        = bool
      web_commit_signoff_required                                  = bool
      dependabot_alerts_enabled_for_new_repositories               = bool
      secret_scanning_enabled_for_new_repositories                 = bool
      secret_scanning_push_protection_enabled_for_new_repositories = bool
    })
    actions_dials = object({
      allowed_actions                  = string
      allow_github_owned_actions       = bool
      allow_verified_creator_actions   = bool
      default_workflow_permissions     = string
      can_approve_pull_request_reviews = bool
      sha_pinning_required             = bool
      default_job_timeout_minutes      = number
    })
    runner_groups = list(object({
      name                      = string
      visibility                = string
      allow_public_repositories = bool
    }))
  })

  validation {
    condition     = var.org.actions_dials.default_workflow_permissions == "read"
    error_message = "Tier 1 Baseline Violation: default_workflow_permissions must be 'read'."
  }

  validation {
    condition     = var.org.actions_dials.can_approve_pull_request_reviews == false
    error_message = "Tier 1 Baseline Violation: can_approve_pull_request_reviews must be false."
  }
}
