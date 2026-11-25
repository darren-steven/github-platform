# =============================================================================
# Module: config-resolver — 4-Layer YAML Inheritance Engine
# =============================================================================
# Pure-HCL transformation module (provisions zero resources).
# Reads enterprise.yaml, org.yaml, teams.yaml, and repos/*.yaml and resolves:
#   1. Enterprise Archetype Baseline (config/enterprise.yaml)
#   2. Organization Defaults         (config/orgs/<org>/org.yaml)
#   3. Domain Defaults               (config/orgs/<org>/repos/<domain>.yaml)
#   4. Per-Repository Overrides      (config/orgs/<org>/repos/<domain>.yaml)
# =============================================================================

locals {
  # ---------------------------------------------------------------------------
  # Layer 1 & 2: Decode Enterprise, Organization, and Teams YAML
  # ---------------------------------------------------------------------------
  enterprise_raw = yamldecode(file(var.enterprise_config_path))
  org_raw        = yamldecode(file("${var.org_config_dir}/org.yaml"))
  teams_raw      = yamldecode(file("${var.org_config_dir}/teams.yaml"))

  archetypes = local.enterprise_raw.archetypes

  # Normalize teams into a map keyed by immutable team slug for for_each usage.
  teams_by_slug = {
    for team in try(local.teams_raw.teams, []) : team.slug => {
      slug         = team.slug
      name         = team.name
      description  = team.description
      privacy      = try(team.privacy, "closed")
      role_tier    = team.role_tier
      parent_team  = try(team.parent_team, null)
      idp_group_id = try(team.idp_group_id, null)
      maintainers  = try(team.maintainers, [])
      members      = try(team.members, [])
    }
  }

  # ---------------------------------------------------------------------------
  # Layer 3: Decode all Domain Repository Files (repos/*.yaml)
  # ---------------------------------------------------------------------------
  domain_files = sort(fileset("${var.org_config_dir}/repos", "*.yaml"))

  domains_raw = {
    for filename in local.domain_files :
    trimsuffix(filename, ".yaml") => yamldecode(file("${var.org_config_dir}/repos/${filename}"))
  }

  # ---------------------------------------------------------------------------
  # Layer 4: Flatten & Merge Every Repository Across All Domains
  # ---------------------------------------------------------------------------
  resolved_repositories_list = flatten([
    for domain_key, domain_doc in local.domains_raw : [
      for repo in try(domain_doc.repositories, []) : {
        name           = repo.name
        description    = repo.description
        domain_key     = domain_key
        domain_name    = domain_doc.domain.name
        archetype_name = coalesce(try(repo.archetype, null), try(domain_doc.defaults.archetype, null), local.org_raw.organization.default_archetype)

        # Resolve visibility: Repo override -> Domain default -> Archetype baseline
        visibility = coalesce(
          try(repo.visibility, null),
          try(domain_doc.defaults.visibility, null),
          local.archetypes[coalesce(try(repo.archetype, null), try(domain_doc.defaults.archetype, null), local.org_raw.organization.default_archetype)].visibility
        )

        # Default branch (Tier 2 standardized to 'main')
        default_branch = coalesce(
          try(repo.default_branch, null),
          try(local.org_raw.repository_defaults.default_branch, "main")
        )

        # Combine domain-level and repo-level topics (deduplicated)
        topics = distinct(concat(
          try(domain_doc.defaults.topics, []),
          try(repo.topics, [])
        ))

        # Merge feature toggles: Archetype baseline <- Repo override
        features = merge(
          local.archetypes[coalesce(try(repo.archetype, null), try(domain_doc.defaults.archetype, null), local.org_raw.organization.default_archetype)].features,
          try(repo.features, {})
        )

        # Merge PR merge strategies: Archetype baseline <- Repo override
        merge_strategies = merge(
          local.archetypes[coalesce(try(repo.archetype, null), try(domain_doc.defaults.archetype, null), local.org_raw.organization.default_archetype)].merge_strategies,
          try(repo.merge_strategies, {})
        )

        # Merge branch protection / ruleset dials: Archetype baseline <- Repo override
        branch_protection = merge(
          local.archetypes[coalesce(try(repo.archetype, null), try(domain_doc.defaults.archetype, null), local.org_raw.organization.default_archetype)].branch_protection,
          try(repo.branch_protection, {})
        )

        # Merge GHAS & Dependabot security toggles: Archetype baseline <- Repo override
        security = merge(
          local.archetypes[coalesce(try(repo.archetype, null), try(domain_doc.defaults.archetype, null), local.org_raw.organization.default_archetype)].security,
          try(repo.security, {})
        )

        required_status_checks = try(repo.required_status_checks, [])

        # Team access: Repo-level list replaces domain defaults when explicitly specified
        team_access = length(try(repo.team_access, [])) > 0 ? repo.team_access : try(domain_doc.defaults.team_access, [])

        codeowners_teams = try(repo.codeowners_teams, [])

        # Deployment environments: Repo-level list replaces domain defaults when specified
        environments = [
          for env in coalescelist(
            try(tolist(repo.environments), []),
            try(tolist(domain_doc.defaults.environments), [])
            ) : 
          {
            name                     = env.name
            description              = try(env.description, "")
            require_approval         = env.require_approval
            approver_teams           = try(env.approver_teams, [])
            deployment_branch_policy = try(env.deployment_branch_policy, "protected_branches")
          }
        ]

        # Non-sensitive GitHub Actions variables
        environment_variables = try(repo.environment_variables, {})
      }
    ]
  ])

  repositories_by_name = {
    for repo in local.resolved_repositories_list : repo.name => repo
  }
}
