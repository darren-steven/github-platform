package main

import rego.v1

# =============================================================================
# Repository & Domain Guardrails (`policies/repo_guardrails.rego`)
# Enforces archetype-specific invariants and anti-secret rules on
# `config/orgs/<org>/repos/<domain>.yaml`
# =============================================================================

effective_archetype(repo, defaults) := arch if {
	arch := object.get(repo, "archetype", defaults.archetype)
}

# Guardrail 1: Regulated workloads must require at least 3 reviewers and signed commits
deny contains msg if {
	input.domain
	some repo in input.repositories
	effective_archetype(repo, input.defaults) == "regulated-workload"
	bp := object.get(repo, "branch_protection", {})
	min_rev := object.get(bp, "min_reviewers", 3)
	min_rev < 3
	msg := sprintf(
		"[REPO-POLICY-001] Repository '%s' (domain '%s') uses archetype 'regulated-workload' and must set branch_protection.min_reviewers >= 3 (got %d).",
		[repo.name, input.domain.key, min_rev],
	)
}

deny contains msg if {
	input.domain
	some repo in input.repositories
	effective_archetype(repo, input.defaults) == "regulated-workload"
	bp := object.get(repo, "branch_protection", {})
	signed := object.get(bp, "require_signed_commits", true)
	signed != true
	msg := sprintf(
		"[REPO-POLICY-002] Repository '%s' (domain '%s') uses archetype 'regulated-workload' and cannot disable branch_protection.require_signed_commits.",
		[repo.name, input.domain.key],
	)
}

# Guardrail 2: Non-sandbox repositories cannot disable secret scanning, push protection, or Dependabot alerts
deny contains msg if {
	input.domain
	some repo in input.repositories
	effective_archetype(repo, input.defaults) != "sandbox"
	sec := object.get(repo, "security", {})
	some key in ["secret_scanning", "secret_scanning_push_protection", "dependabot_alerts"]
	object.get(sec, key, true) == false
	msg := sprintf(
		"[REPO-POLICY-003] Repository '%s' (domain '%s') cannot disable security.%s on non-sandbox archetype.",
		[repo.name, input.domain.key, key],
	)
}

# Guardrail 3: Production environments ('prod', 'production', 'prd') in defaults or repo overrides must require approval and specify approver_teams
all_env_entries contains {"scope": "defaults", "env": env} if {
	input.domain
	some env in object.get(input.defaults, "environments", [])
}

all_env_entries contains {"scope": repo.name, "env": env} if {
	input.domain
	some repo in input.repositories
	some env in object.get(repo, "environments", [])
}

deny contains msg if {
	some entry in all_env_entries
	env := entry.env
	lower(env.name) in {"prod", "production", "prd"}
	env.require_approval != true
	msg := sprintf(
		"[REPO-POLICY-004] Domain '%s' (%s) environment '%s' is a production environment and must set require_approval: true.",
		[input.domain.key, entry.scope, env.name],
	)
}

deny contains msg if {
	some entry in all_env_entries
	env := entry.env
	env.require_approval == true
	approvers := object.get(env, "approver_teams", [])
	count(approvers) == 0
	msg := sprintf(
		"[REPO-POLICY-005] Domain '%s' (%s) environment '%s' has require_approval: true and must specify at least one team in approver_teams.",
		[input.domain.key, entry.scope, env.name],
	)
}

# Guardrail 4: When merge_strategies is overridden on a repo, at least one strategy must be enabled
deny contains msg if {
	input.domain
	some repo in input.repositories
	ms := repo.merge_strategies
	not object.get(ms, "allow_squash_merge", false)
	not object.get(ms, "allow_merge_commit", false)
	not object.get(ms, "allow_rebase_merge", false)
	msg := sprintf(
		"[REPO-POLICY-006] Repository '%s' (domain '%s') merge_strategies must enable at least one merge method (allow_squash_merge, allow_merge_commit, or allow_rebase_merge).",
		[repo.name, input.domain.key],
	)
}

# Guardrail 5: Reject plain-text environment_variables that look like secrets or credentials
suspicious_secret_patterns := ["SECRET", "PASSWORD", "PASSWD", "TOKEN", "API_KEY", "APIKEY", "PRIVATE_KEY", "CONNECTION_STRING", "CONN_STR", "CLIENT_SECRET", "PAT"]

deny contains msg if {
	input.domain
	some repo in input.repositories
	some var_key, _ in object.get(repo, "environment_variables", {})
	upper_key := upper(var_key)
	some pattern in suspicious_secret_patterns
	contains(upper_key, pattern)
	msg := sprintf(
		"[REPO-POLICY-007] Repository '%s' (domain '%s') defines plain-text environment_variables key '%s' matching sensitive keyword '%s'. Sensitive values must use GitHub Encrypted Secrets / Azure Key Vault OIDC instead.",
		[repo.name, input.domain.key, var_key, pattern],
	)
}
