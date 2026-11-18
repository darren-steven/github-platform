# Configuration Dials Rules (`config/`)

You are operating inside `config/`, which is the **Declarative Maintainer Surface ("The Dials")** for our GitHub Enterprise Cloud (GHEC) organizations, teams, and repositories.

## Directory Layout

- `config/enterprise.yaml` — Enterprise settings, managed organization list, and reusable repository archetypes (`standard-microservice`, `regulated-workload`, `shared-library`, `sandbox`).
- `config/orgs/<org>/org.yaml` — Organization-level security, GitHub Actions, default branch protection, and runner group dials.
- `config/orgs/<org>/teams.yaml` — Centralized catalog of GitHub Teams for `<org>` (referenced by `slug` in repository files).
- `config/orgs/<org>/repos/<domain>.yaml` — Domain-grouped repository definitions (5–15 related repos per file) with shared `defaults` and per-repository overrides.

## Rules for Editing `config/**/*.yaml`

1. **Schema First**:
   - Before modifying `config/enterprise.yaml`, check [enterprise.schema.json](../schemas/enterprise.schema.json).
   - Before modifying `config/orgs/<org>/org.yaml`, check [org.schema.json](../schemas/org.schema.json).
   - Before modifying `config/orgs/<org>/teams.yaml`, check [teams.schema.json](../schemas/teams.schema.json).
   - Before modifying `config/orgs/<org>/repos/<domain>.yaml`, check [domain-repos.schema.json](../schemas/domain-repos.schema.json).
2. **Preserve Schema Directive**:
   - Every YAML file in `config/` must keep its top-level `# yaml-language-server: $schema=...` comment for instant IDE autocomplete and inline validation.
3. **Stay Within Bounded Dials (Tier 2) & Maintain Referential Integrity**:
   - Do not invent new YAML keys that do not exist in `schemas/`.
   - Every team slug referenced in `repos/<domain>.yaml` (`team_access`, `environments[].approver_teams`, `codeowners_teams[].teams`) must exist in that organization's `teams.yaml`.
   - If a maintainer wants a setting outside the allowed bounds (e.g., `min_reviewers: 1`, `visibility: public`, or `permission: admin`), explain that the value is blocked by the enterprise baseline and offer the nearest compliant value.
   - **Never** edit `schemas/` or `policies/` just to make an out-of-bounds YAML value pass validation.
4. **Validate Before Completing**:
   - Run `./scripts/validate.sh` after any edit in `config/`.
