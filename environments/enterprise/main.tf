# =============================================================================
# Environment: enterprise — Root Stack Composition
# =============================================================================


module "config" {
  source = "../../modules/config-resolver"

  enterprise_config_path = var.enterprise_config_path
  org_config_dir         = var.org_config_dir
}

module "enterprise_baseline" {
  source = "../../modules/enterprise-baseline"

  enterprise_config_path = var.enterprise_config_path
}
