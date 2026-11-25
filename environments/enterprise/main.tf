# =============================================================================
# Environment: enterprise — Root Stack Composition
# =============================================================================


module "enterprise_baseline" {
  source = "../../modules/enterprise-baseline"

  enterprise_config_path = var.enterprise_config_path
}
