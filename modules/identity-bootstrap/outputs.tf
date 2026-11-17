output "plan_group_object_id" {
  description = "Entra object ID for the standing plan group."
  value       = azuread_group.plan.object_id
}

output "apply_group_object_id" {
  description = "Entra object ID for the PIM-eligible apply group."
  value       = azuread_group.apply.object_id
}

output "apply_eligible_member_schedule_ids" {
  description = "PIM eligibility schedule IDs for apply group members."
  value       = { for object_id, assignment in azuread_privileged_access_group_eligibility_schedule.apply_members : object_id => assignment.target_schedule_id }
}
