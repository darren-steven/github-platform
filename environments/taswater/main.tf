# =============================================================================
# Environment: taswater — Root Stack Composition
# =============================================================================
# Connects the 4-layer YAML configuration resolver to the hardened GitHub
# resource modules:
#   1. module.config       -> Decodes & merges YAML (zero GitHub API calls)
#   2. module.org_baseline -> Org settings, Actions permissions, runner groups
#   3. module.teams        -> Two-pass GitHub Teams (root -> child) & members
#   4. module.repositories -> Repos, Rulesets, team access, environments, vars
# =============================================================================

module "config" {
  source = "../../modules/config-resolver"

  enterprise_config_path = var.enterprise_config_path
  org_config_dir         = var.org_config_dir
}

module "org_baseline" {
  source = "../../modules/org-baseline"

  enterprise = module.config.enterprise
  org        = module.config.org
}

module "teams" {
  source = "../../modules/teams"

  teams = module.config.teams
}

module "repositories" {
  source = "../../modules/domain-repositories"

  repositories     = module.config.repositories
  team_ids_by_slug = module.teams.team_ids_by_slug
}
