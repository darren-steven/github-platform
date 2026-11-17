variable "plan_group" {
  description = "Entra group configuration for standing plan access."
  type = object({
    display_name      = string
    description       = string
    member_object_ids = list(string)
    owner_object_ids  = list(string)
  })

  validation {
    condition = (
      length(trimspace(var.plan_group.display_name)) >= 3 &&
      length(trimspace(var.plan_group.description)) >= 10
    )
    error_message = "The plan group display name must be at least 3 characters and its description at least 10 characters."
  }

  validation {
    condition = alltrue([
      for object_id in concat(var.plan_group.member_object_ids, var.plan_group.owner_object_ids) :
      can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", object_id))
    ])
    error_message = "Every plan group member and owner must be an Entra object ID in GUID format."
  }

  validation {
    condition = (
      length(var.plan_group.member_object_ids) == length(toset(var.plan_group.member_object_ids)) &&
      length(var.plan_group.owner_object_ids) == length(toset(var.plan_group.owner_object_ids))
    )
    error_message = "Plan group member and owner object ID lists must not contain duplicates."
  }
}

variable "apply_group" {
  description = "Entra group configuration for PIM-eligible apply access."
  type = object({
    display_name = string
    description  = string
  })

  validation {
    condition = (
      length(trimspace(var.apply_group.display_name)) >= 3 &&
      length(trimspace(var.apply_group.description)) >= 10
    )
    error_message = "The apply group display name must be at least 3 characters and its description at least 10 characters."
  }
}

variable "apply_eligible_member_object_ids" {
  description = "Entra user object IDs to receive permanent PIM-eligible membership in the apply group."
  type        = list(string)
  default     = []

  validation {
    condition = alltrue([
      for object_id in var.apply_eligible_member_object_ids :
      can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", object_id))
    ])
    error_message = "Every eligible member must be an Entra user object ID in GUID format."
  }

  validation {
    condition     = length(var.apply_eligible_member_object_ids) == length(toset(var.apply_eligible_member_object_ids))
    error_message = "apply_eligible_member_object_ids must not contain duplicate object IDs."
  }
}

variable "plan_project_names" {
  description = "Existing Azure DevOps projects where the plan group receives the built-in Readers role."
  type        = list(string)
  default     = []

  validation {
    condition = alltrue([
      for project_name in var.plan_project_names :
      trimspace(project_name) != ""
    ])
    error_message = "Every plan project name must be non-empty."
  }

  validation {
    condition     = length(var.plan_project_names) == length(toset(var.plan_project_names))
    error_message = "plan_project_names must not contain duplicates."
  }
}
