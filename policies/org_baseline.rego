package main

import rego.v1

# =============================================================================
# Organization Baseline Policies (`policies/org_baseline.rego`)
# Enforces cross-field invariants on `config/orgs/<org>/org.yaml`
# =============================================================================

# Guardrail 1: Default minimum reviewers must be between 2 and 5
deny contains msg if {
	input.organization
	count_val := input.repository_defaults.min_reviewers
	count_val < 2
	msg := sprintf(
		"[ORG-BASELINE-001] repository_defaults.min_reviewers is set to %d, which violates the Tier 1 four-eyes baseline (minimum allowed is 2).",
		[count_val],
	)
}

deny contains msg if {
	input.organization
	count_val := input.repository_defaults.min_reviewers
	count_val > 5
	msg := sprintf(
		"[ORG-BASELINE-002] repository_defaults.min_reviewers is set to %d, which exceeds the maximum bound of 5.",
		[count_val],
	)
}

# Guardrail 2: At least one merge strategy must be enabled in repository_defaults
deny contains msg if {
	input.organization
	merges := input.repository_defaults.allowed_merge_types
	not merges.squash
	not merges.merge_commit
	not merges.rebase
	msg := "[ORG-BASELINE-003] repository_defaults.allowed_merge_types must enable at least one merge strategy (squash, merge_commit, or rebase)."
}

# Guardrail 3: GitHub Actions job timeout must be within 15..180 minutes and token permissions read-only
deny contains msg if {
	input.organization
	timeout := input.actions_dials.default_job_timeout_minutes
	timeout < 15
	msg := sprintf(
		"[ORG-BASELINE-004] actions_dials.default_job_timeout_minutes (%d) cannot be less than 15 minutes.",
		[timeout],
	)
}

deny contains msg if {
	input.organization
	timeout := input.actions_dials.default_job_timeout_minutes
	timeout > 180
	msg := sprintf(
		"[ORG-BASELINE-005] actions_dials.default_job_timeout_minutes (%d) cannot exceed 180 minutes.",
		[timeout],
	)
}

deny contains msg if {
	input.organization
	input.actions_dials.default_workflow_permissions != "read"
	msg := "[ORG-BASELINE-006] actions_dials.default_workflow_permissions must be 'read' to enforce least privilege on GITHUB_TOKEN."
}

deny contains msg if {
	input.organization
	input.actions_dials.can_approve_pull_request_reviews != false
	msg := "[ORG-BASELINE-007] actions_dials.can_approve_pull_request_reviews must be false."
}

# Guardrail 4: Warn if runner groups are exposed to all repositories rather than selected
warn contains msg if {
	input.organization
	some rg in input.runner_groups
	rg.visibility == "all"
	msg := sprintf(
		"[ORG-BASELINE-WARN-001] Runner group '%s' has visibility='all'. Consider setting visibility='selected' for least privilege.",
		[rg.name],
	)
}
