# =============================================================================
# Module: domain-repositories — Input Variables & Tier 1 Validations
# =============================================================================

variable "repositories" {
  description = "Map of fully resolved repository definitions keyed by repository name from modules/config-resolver."
  type = map(object({
    name           = string
    description    = string
    domain_key     = string
    domain_name    = string
    archetype_name = string
    visibility     = string
    default_branch = string
    topics         = list(string)

    features = object({
      has_issues      = bool
      has_wiki        = bool
      has_discussions = bool
      has_projects    = bool
    })

    merge_strategies = object({
      allow_squash_merge     = bool
      allow_merge_commit     = bool
      allow_rebase_merge     = bool
      allow_auto_merge       = bool
      delete_branch_on_merge = bool
    })

    branch_protection = object({
      min_reviewers                   = number
      dismiss_stale_reviews           = bool
      require_code_owner_reviews      = bool
      require_last_push_approval      = bool
      require_conversation_resolution = bool
      require_signed_commits          = bool
      require_linear_history          = bool
    })

    security = object({
      dependabot_alerts               = bool
      dependabot_security_updates     = bool
      secret_scanning                 = bool
      secret_scanning_push_protection = bool
      code_scanning_default_setup     = bool
    })

    required_status_checks = list(string)

    team_access = list(object({
      team       = string
      permission = string
    }))

    codeowners_teams = list(object({
      path  = string
      teams = list(string)
    }))

    environments = list(object({
      name                     = string
      description              = string
      require_approval         = bool
      approver_teams           = list(string)
      deployment_branch_policy = string
    }))

    environment_variables = map(string)
  }))

  # Tier 1 Immutable Baseline: Public repositories are strictly blocked
  validation {
    condition     = alltrue([for _, r in var.repositories : contains(["private", "internal"], r.visibility)])
    error_message = "Tier 1 Baseline Violation: Repository visibility must be 'private' or 'internal' (never 'public')."
  }

  # Tier 1 Immutable Baseline: Team 'admin' permission is strictly blocked
  validation {
    condition = alltrue(flatten([
      for _, r in var.repositories : [
        for ta in r.team_access : contains(["pull", "triage", "push", "maintain"], ta.permission)
      ]
    ]))
    error_message = "Tier 1 Baseline Violation: team_access permission must be one of pull, triage, push, maintain ('admin' is blocked)."
  }

  # Tier 1 & Archetype Floor: Minimum PR reviewers >= 2 (>= 3 for regulated-workload)
  validation {
    condition = alltrue([
      for _, r in var.repositories :
      r.archetype_name == "regulated-workload" ? r.branch_protection.min_reviewers >= 3 : r.branch_protection.min_reviewers >= 2
    ])
    error_message = "Tier 1 Baseline Violation: min_reviewers must be >= 2 (>= 3 for regulated-workload)."
  }
}

variable "team_ids_by_slug" {
  description = "Map of team slug to GitHub numeric team ID from modules/teams."
  type        = map(string)
}
