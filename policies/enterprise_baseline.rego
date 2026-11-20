package main

import rego.v1

# =============================================================================
# Enterprise Baseline Policies (`policies/enterprise_baseline.rego`)
# Enforces Tier 1 invariants and archetype floor rules on `config/enterprise.yaml`
# =============================================================================

# Guardrail 1: SAML SSO and public repository restriction must remain enforced
deny contains msg if {
	input.enterprise
	input.security_settings.enforce_saml_sso != true
	msg := "[ENT-BASELINE-001] security_settings.enforce_saml_sso must be set to true."
}

deny contains msg if {
	input.enterprise
	input.security_settings.members_can_create_public_repositories != false
	msg := "[ENT-BASELINE-002] security_settings.members_can_create_public_repositories must be set to false (Tier 1 no-public-repos baseline)."
}

# Guardrail 2: All archetypes must enforce min_reviewers >= 2 and dismiss_stale_reviews / require_last_push_approval
deny contains msg if {
	input.enterprise
	some arch_name, arch in input.archetypes
	arch.branch_protection.min_reviewers < 2
	msg := sprintf(
		"[ENT-BASELINE-003] Archetype '%s' sets branch_protection.min_reviewers to %d, violating the Tier 1 four-eyes baseline (>= 2).",
		[arch_name, arch.branch_protection.min_reviewers],
	)
}

# Guardrail 3: Regulated workload archetype must enforce min_reviewers >= 3 and signed commits
deny contains msg if {
	input.enterprise
	reg := input.archetypes["regulated-workload"]
	reg.branch_protection.min_reviewers < 3
	msg := sprintf(
		"[ENT-BASELINE-004] Archetype 'regulated-workload' must enforce branch_protection.min_reviewers >= 3 (got %d).",
		[reg.branch_protection.min_reviewers],
	)
}

deny contains msg if {
	input.enterprise
	reg := input.archetypes["regulated-workload"]
	reg.branch_protection.require_signed_commits != true
	msg := "[ENT-BASELINE-005] Archetype 'regulated-workload' must enforce branch_protection.require_signed_commits: true."
}

# Guardrail 4: Every archetype must enable at least one merge strategy
deny contains msg if {
	input.enterprise
	some arch_name, arch in input.archetypes
	ms := arch.merge_strategies
	not ms.allow_squash_merge
	not ms.allow_merge_commit
	not ms.allow_rebase_merge
	msg := sprintf(
		"[ENT-BASELINE-006] Archetype '%s' must enable at least one merge strategy in merge_strategies.",
		[arch_name],
	)
}

# Guardrail 5: FinOps ceilings on enterprise Codespaces defaults
deny contains msg if {
	input.enterprise
	cs := input.enterprise_defaults.codespaces
	cs.max_idle_timeout_minutes > 120
	msg := sprintf(
		"[ENT-FINOPS-001] enterprise_defaults.codespaces.max_idle_timeout_minutes (%d) cannot exceed 120 minutes.",
		[cs.max_idle_timeout_minutes],
	)
}

deny contains msg if {
	input.enterprise
	cs := input.enterprise_defaults.codespaces
	cs.max_retention_period_days > 30
	msg := sprintf(
		"[ENT-FINOPS-001] enterprise_defaults.codespaces.max_retention_period_days (%d) cannot exceed 30 days.",
		[cs.max_retention_period_days],
	)
}
