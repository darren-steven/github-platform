# =============================================================================
# Module: org-baseline — Organization Settings & GitHub Actions Governance
# =============================================================================

# -----------------------------------------------------------------------------
# Organization Profile, Member Privileges & GHAS Defaults
# Source: config/orgs/<org>/org.yaml -> organization, security_dials
#         config/enterprise.yaml     -> security_settings
# -----------------------------------------------------------------------------
resource "github_organization_settings" "this" {
  billing_email = var.org.organization.billing_email
  name          = var.org.organization.name
  description   = var.org.organization.description

  # Enterprise baseline default repository permission (least privilege: none/read)
  default_repository_permission = var.enterprise.security_settings.default_repository_permission

  # Tier 1 Immutable Baseline: Public repository creation is strictly disabled
  members_can_create_public_repositories = false

  # Tier 2 Organization Security Dials
  members_can_create_private_repositories                      = var.org.security_dials.members_can_create_private_repositories
  members_can_create_internal_repositories                     = var.org.security_dials.members_can_create_internal_repositories
  members_can_fork_private_repositories                        = var.org.security_dials.members_can_fork_private_repositories
  web_commit_signoff_required                                  = var.org.security_dials.web_commit_signoff_required
  dependabot_alerts_enabled_for_new_repositories               = var.org.security_dials.dependabot_alerts_enabled_for_new_repositories
  secret_scanning_enabled_for_new_repositories                 = var.org.security_dials.secret_scanning_enabled_for_new_repositories
  secret_scanning_push_protection_enabled_for_new_repositories = var.org.security_dials.secret_scanning_push_protection_enabled_for_new_repositories
}

# -----------------------------------------------------------------------------
# GitHub Actions Organization Allowed Actions & SHA Pinning
# Source: config/orgs/<org>/org.yaml -> actions_dials
# -----------------------------------------------------------------------------
resource "github_actions_organization_permissions" "this" {
  allowed_actions      = var.org.actions_dials.allowed_actions
  enabled_repositories = "all"
  sha_pinning_required = var.org.actions_dials.sha_pinning_required

  dynamic "allowed_actions_config" {
    for_each = var.org.actions_dials.allowed_actions == "selected" ? [1] : []
    content {
      github_owned_allowed = var.org.actions_dials.allow_github_owned_actions
      verified_allowed     = var.org.actions_dials.allow_verified_creator_actions
    }
  }
}

# -----------------------------------------------------------------------------
# GitHub Actions Default GITHUB_TOKEN Permissions
# Tier 1 Immutable Baseline: Read-only token, workflows cannot approve PRs
# Source: config/orgs/<org>/org.yaml -> actions_dials
# -----------------------------------------------------------------------------
resource "github_actions_organization_workflow_permissions" "this" {
  organization_slug                = var.org.organization.slug
  default_workflow_permissions     = "read"
  can_approve_pull_request_reviews = false
}
