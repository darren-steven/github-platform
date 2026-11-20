# =============================================================================
# Environment: enterprise — State Backend Configuration
# =============================================================================
# Phase 1 (Current): Local state for read-only `tofu plan` validation.
# Phase 2 (Production): Switch to Azure Storage (`azurerm`) with Entra ID OIDC.
# =============================================================================

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }

  # backend "azurerm" {
  #   resource_group_name  = "rg-github-platform-tfstate"
  #   storage_account_name = "stgithubplatformstate"
  #   container_name       = "tfstate"
  #   key                  = "github-enterprise/enterprise.tfstate"
  #   use_azuread_auth     = true
  #   use_oidc             = true
  # }
}
