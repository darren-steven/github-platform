# =============================================================================
# Environment: enterprise — GitHub Provider Configuration
# =============================================================================
# Uses GITHUB_TOKEN from shell memory (never hardcoded).
# =============================================================================

locals {
  enterprise_meta = yamldecode(file(var.enterprise_config_path)).enterprise
}

provider "github" {
  owner = local.enterprise_meta.slug
}