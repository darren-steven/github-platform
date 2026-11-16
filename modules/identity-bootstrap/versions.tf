terraform {
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
}
