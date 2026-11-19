# =============================================================================
# Environment: taswater — GitHub Provider Configuration
# =============================================================================
# Zero-Secret Design:
#   Authentication is supplied at runtime via the `GITHUB_TOKEN` environment
#   variable (or GitHub App OIDC in Phase 2 CI). Never hardcode tokens here.
# =============================================================================

provider "github" {
  owner = module.config.org.organization.slug
}
