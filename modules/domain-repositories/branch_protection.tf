# =============================================================================
# Module: domain-repositories — Default Branch Repository Rulesets
# =============================================================================
# Uses modern GitHub Repository Rulesets (`github_repository_ruleset`) targeting
# `~DEFAULT_BRANCH` so protection stays attached automatically to the repo's
# configured default branch.
#
# Source: enterprise.yaml archetypes[*].branch_protection + optional repo override
# =============================================================================

resource "github_repository_ruleset" "default_branch" {
  for_each = var.repositories

  name        = "default-branch-baseline"
  repository  = github_repository.this[each.key].name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
      exclude = []
    }
  }

  rules {
    # Tier 1 Immutable Baselines: Protect default branch from deletion and force-pushes
    deletion         = true
    non_fast_forward = true

    # Tier 2 Bounded Dials (from archetype + optional repo override)
    required_linear_history = each.value.branch_protection.require_linear_history
    required_signatures     = each.value.branch_protection.require_signed_commits

    pull_request {
      required_approving_review_count   = each.value.branch_protection.min_reviewers
      require_code_owner_review         = each.value.branch_protection.require_code_owner_reviews
      required_review_thread_resolution = each.value.branch_protection.require_conversation_resolution

      # Tier 1 Immutable Baselines
      dismiss_stale_reviews_on_push = true
      require_last_push_approval    = true
    }

    # Optional CI status check contexts required before merge
    dynamic "required_status_checks" {
      for_each = length(each.value.required_status_checks) > 0 ? [1] : []
      content {
        strict_required_status_checks_policy = true

        dynamic "required_check" {
          for_each = each.value.required_status_checks
          content {
            context = required_check.value
          }
        }
      }
    }
  }
}
