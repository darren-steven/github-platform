# =============================================================================
# Environment: taswater — State Backend Configuration
# =============================================================================
# Phase 1 (Current): Local state for read-only `tofu plan` alignment.
# Local *.tfstate files are strictly excluded via `.gitignore`.
#
# Phase 2 (Production Readiness): Replace the `local` block below with the
# commented Azure Storage (`azurerm`) OIDC backend block once alignment is
# complete and the remote state container is provisioned.
# =============================================================================

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }

  # ---------------------------------------------------------------------------
  # Phase 2 Production Remote State Blueprint (Azure Storage + Entra ID OIDC)
  # ---------------------------------------------------------------------------
  # backend "azurerm" {
  #   resource_group_name  = "rg-github-platform-tfstate"
  #   storage_account_name = "stgithubplatformstate"
  #   container_name       = "tfstate"
  #   key                  = "github-orgs/taswater.tfstate"
  #   use_azuread_auth     = true
  #   use_oidc             = true
  # }
}
