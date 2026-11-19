# Architecture & Configuration Inheritance (`GHEC-IaC`)

This document explains how the declarative YAML configuration in `config/` is structured to manage **~150 repositories** and **~20 GitHub Teams** across **2 GitHub Organizations** in **GitHub Enterprise Cloud (GHEC)**.

---

## 1. High-Level Configuration Flow & Inheritance Chain

To keep day-to-day repository configuration concise and easy to navigate, settings flow through a **four-layer inheritance hierarchy**:

```text
1. Enterprise Archetype Catalog (config/enterprise.yaml)
   Defines baseline settings for:
   - standard-microservice
   - regulated-workload
   - shared-library
   - sandbox
          │
          ▼
2. Organization Dials (config/orgs/<org>/org.yaml) + Teams Catalog (config/orgs/<org>/teams.yaml)
   Sets org-wide security, GitHub Actions token limits, runner groups,
   and the canonical registry of valid team slugs for that organization.
          │
          ▼
3. Domain Defaults (config/orgs/<org>/repos/<domain>.yaml -> defaults)
   Sets the default archetype, default team_access matrix, default topics,
   and standard dev/staging/prod environments for all 5–15 repos in that domain.
          │
          ▼
4. Individual Repository Definition (config/orgs/<org>/repos/<domain>.yaml -> repositories[*])
   Inherits all domain defaults and archetype baselines; specifies only
   repo-specific metadata (name, description) and optional bounded overrides.
```

---

## 2. Why Domain-Grouped YAML Files?

In Azure DevOps, **Projects** acted as natural grouping containers for 5–15 related repositories, teams, and environments. GitHub Enterprise Cloud has a flatter hierarchy (`Enterprise -> Organization -> Repository`).

With ~150 repositories across 2 organizations (`taswater-core` and `taswater-digital`):
- **A single `repositories.yaml` per organization** (~75 repos in one file) becomes thousand-line YAML prone to merge conflicts.
- **150 separate single-repo YAML files** creates directory clutter and repeats identical `team_access` and `environments` blocks 150 times.
- **Domain-grouped files (`config/orgs/<org>/repos/<domain>.yaml`)** group 5–15 related repositories per business domain or product team (~10–15 files total across the enterprise) and provide a `defaults:` block at the top of each file. Most repositories require only `name` and `description`.

---

## 3. Multi-Layer Validation Architecture (`./scripts/validate.sh`)

Every change to `config/` passes through four automated verification gates before merge:

1. **Layer 1: JSON Schema Validation (`schemas/*.schema.json`)**:
   - Validates `config/enterprise.yaml` against [`schemas/enterprise.schema.json`](schemas/enterprise.schema.json).
   - Validates `config/orgs/*/org.yaml` against [`schemas/org.schema.json`](schemas/org.schema.json).
   - Validates `config/orgs/*/teams.yaml` against [`schemas/teams.schema.json`](schemas/teams.schema.json).
   - Validates `config/orgs/*/repos/*.yaml` against [`schemas/domain-repos.schema.json`](schemas/domain-repos.schema.json).
   - Provides real-time IDE autocompletion and inline squiggles via `# yaml-language-server: $schema=...`.
2. **Layer 2: Cross-File Referential Integrity (`scripts/validate_config.py`)**:
   - Ensures every organization in `config/enterprise.yaml` (`managed_organizations`) matches a `config/orgs/<org>/` folder.
   - Ensures every `parent_team` in `teams.yaml` resolves to an existing team slug in the same organization.
   - Ensures every team slug referenced in `repos/<domain>.yaml` (`team_access`, `environments[].approver_teams`, `codeowners_teams[].teams`) exists in that organization's `teams.yaml`.
   - Ensures repository names are globally unique across all domain files within the same organization.
3. **Layer 3: Policy Guardrails (`policies/*.rego` & `scripts/validate_config.py`)**:
   - Enforces archetype floors (e.g., `regulated-workload` requires `min_reviewers >= 3` and `require_signed_commits: true`).
   - Enforces GHAS protections (`secret_scanning`, `secret_scanning_push_protection`, `dependabot_alerts`) on non-sandbox repositories.
   - Enforces mandatory reviewer gates on `prod` / `production` environments.
   - Blocks secret-like key names in plain-text `environment_variables`.
4. **Layer 4: Cross-Agent AI Skill Integrity (`scripts/validate_agent_guardrails.py`)**:
   - Verifies that `.agents/skills/*/SKILL.md` and `AGENTS.md` / `GEMINI.md` / `.github/copilot-instructions.md` remain synchronized.

---

## 4. OpenTofu IaC Engine (`modules/` & `environments/`)

Validated YAML configurations in `config/` are consumed by a modular OpenTofu (`>= 1.8.0`) backend powered by the `integrations/github` (`~> 6.6`) provider:

- **`environments/<org>/`**: One isolated root stack per GitHub Organization (starting with [`environments/taswater/`](./environments/taswater/README.md)), isolating blast radius and state files.
- **`modules/config-resolver/`**: Pure-HCL transformation layer that decodes `enterprise.yaml`, `org.yaml`, `teams.yaml`, and `repos/*.yaml` and merges the 4-layer inheritance hierarchy.
- **`modules/org-baseline/`**: Manages `github_organization_settings`, `github_actions_organization_permissions`, `github_actions_organization_workflow_permissions`, and `github_actions_runner_group`.
- **`modules/teams/`**: Manages centralized `github_team` resources in two ordered passes (root teams → child teams) and optional explicit memberships.
- **`modules/domain-repositories/`**: Manages `github_repository` (`archive_on_destroy = true`), modern `github_repository_ruleset` (`~DEFAULT_BRANCH`), `github_team_repository`, `github_repository_environment`, and `github_actions_variable`.
- **Config-Driven Alignment (`scripts/generate_imports.py` + `scripts/tofu-plan.sh`)**: Generates native `import {}` blocks from `inventory/<org>.inventory.json` so read-only `tofu plan` runs display exact in-place diffs (`~`) against live GitHub during Phase 1 alignment.
