# =============================================================================
# Environment: enterprise — GitHub Provider Configuration
# =============================================================================
# Uses GITHUB_TOKEN from shell memory (never hardcoded).
# =============================================================================

provider "github" {
  owner = module.enterprise_baseline.enterprise.slug
}
