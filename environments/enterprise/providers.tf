# =============================================================================
# Environment: enterprise — GitHub Provider Configuration
# =============================================================================
# Uses GITHUB_TOKEN from shell memory (never hardcoded).
# =============================================================================

provider "github" {
  owner = module.config.enterprise.enterprise.slug
}
