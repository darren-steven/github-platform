terraform {
  required_version = ">= 1.8.0"

  required_providers {
    azuread = {
      source  = "hashicorp/azuread"
      version = ">= 3.0.0"
    }
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = ">= 1.3.0"
    }
  }

  # Configure a dedicated protected backend for this privileged state.
  # Do not reuse the prod-org state key.
  # backend "azurerm" {
  #   resource_group_name  = "rg-azdo-iac-state"
  #   storage_account_name = "stazdoiacstate"
  #   container_name       = "tfstate"
  #   key                  = "identity-bootstrap.tfstate"
  #   use_oidc             = true
  # }
}
