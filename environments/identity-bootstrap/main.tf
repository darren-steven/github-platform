locals {
  identity_config = yamldecode(file("${path.module}/../../config/identity-bootstrap.yaml"))
}

provider "azuread" {}

provider "azuredevops" {
  org_service_url = yamldecode(file("${path.module}/../../config/org.yaml")).organization.service_url
}

module "identity_bootstrap" {
  source = "../../modules/identity-bootstrap"

  plan_group                       = local.identity_config.plan_group
  apply_group                      = local.identity_config.apply_group
  apply_eligible_member_object_ids = local.identity_config.apply_group.eligible_member_object_ids
  plan_project_names               = local.identity_config.plan_project_names
}

output "plan_group_object_id" {
  description = "Entra object ID for the standing plan group."
  value       = module.identity_bootstrap.plan_group_object_id
}

output "apply_group_object_id" {
  description = "Entra object ID for the PIM-eligible apply group."
  value       = module.identity_bootstrap.apply_group_object_id
}
