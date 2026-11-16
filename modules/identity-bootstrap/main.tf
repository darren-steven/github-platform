resource "azuread_group" "plan" {
  display_name     = var.plan_group.display_name
  description      = var.plan_group.description
  security_enabled = true
  mail_enabled     = false
  members          = var.plan_group.member_object_ids
  owners           = var.plan_group.owner_object_ids

  prevent_duplicate_names = true

  lifecycle {
    prevent_destroy = true
  }
}

resource "azuread_group" "apply" {
  display_name     = var.apply_group.display_name
  description      = var.apply_group.description
  security_enabled = true
  mail_enabled     = false

  prevent_duplicate_names = true

  lifecycle {
    prevent_destroy = true
  }
}

resource "azuread_privileged_access_group_eligibility_schedule" "apply_members" {
  for_each = toset(var.apply_eligible_member_object_ids)

  group_id             = azuread_group.apply.object_id
  principal_id         = each.value
  assignment_type      = "member"
  permanent_assignment = true
  justification        = "Eligible Azure DevOps IaC apply access managed by identity bootstrap."
}

resource "azuredevops_group" "plan" {
  origin_id = azuread_group.plan.object_id
}

resource "azuredevops_group" "apply" {
  origin_id = azuread_group.apply.object_id
}

data "azuredevops_security_namespace" "collection" {
  name = "Collection"
}

data "azuredevops_security_namespace_token" "collection" {
  namespace_name = "Collection"
}

resource "azuredevops_security_permissions" "plan_collection_view" {
  namespace_id = data.azuredevops_security_namespace.collection.id
  token        = data.azuredevops_security_namespace_token.collection.token
  principal    = azuredevops_group.plan.descriptor
  permissions = {
    GENERIC_READ = "allow"
  }
  replace = false
}

data "azuredevops_group" "collection_administrators" {
  name = "Project Collection Administrators"
}

resource "azuredevops_group_membership" "apply_collection_administrators" {
  group   = data.azuredevops_group.collection_administrators.descriptor
  members = [azuredevops_group.apply.descriptor]
  mode    = "add"
}

data "azuredevops_project" "plan_scope" {
  for_each = toset(var.plan_project_names)

  name = each.value
}

data "azuredevops_group" "project_readers" {
  for_each = data.azuredevops_project.plan_scope

  project_id = each.value.id
  name       = "Readers"
}

resource "azuredevops_group_membership" "plan_project_readers" {
  for_each = data.azuredevops_group.project_readers

  group   = each.value.descriptor
  members = [azuredevops_group.plan.descriptor]
  mode    = "add"
}
