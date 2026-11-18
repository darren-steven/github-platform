---
name: onboard-project
description: >-
  Walks maintainers through onboarding a new GitHub repository, domain group, or team,
  configuring its governance archetype, team permissions, branch protection, CODEOWNERS,
  and deployment environments via config/orgs/<org>/repos/<domain>.yaml and teams.yaml.
  Use this skill when a user asks to create or onboard a new repository, domain, or team.
---

# Onboard a GitHub Repository, Domain, or Team (`onboard-project`)

Use this skill when a maintainer wants to onboard a new GitHub repository into an existing domain file, scaffold a new domain repository group in `config/orgs/<org>/repos/<domain>.yaml`, or register a new team in `config/orgs/<org>/teams.yaml`.

## Workflow Steps

### Step 1: Gather Required Parameters
If the user has not specified them, ask for or confirm:
1. **Target Organization**: `taswater-core` or `taswater-digital`.
2. **Target Domain File**: Existing domain (e.g., `platform-services`, `data-integration`, `customer-channels`) or a new `<domain-key>.yaml`.
3. **Governance Archetype**:
   - `standard-microservice` (Default: `private`, min 2 reviewers, squash/merge-commit, GHAS enabled).
   - `regulated-workload` (High security: `private`, min 3 reviewers, mandatory signed commits, linear history, GHAS enabled).
   - `shared-library` (Inner-source: `internal` visibility across enterprise orgs, min 2 reviewers, discussions enabled).
   - `sandbox` (Experimentation: `private`, min 2 reviewers on `main`, isolated to non-production environments).
4. **Teams & Access**: Confirm that any team slugs referenced in `team_access`, `codeowners_teams`, or `environments[].approver_teams` exist in `config/orgs/<org>/teams.yaml`.

### Step 2: Scaffold or Update YAML Configuration
- Reference the example template at [standard-microservice.yaml](./examples/standard-microservice.yaml) and schema at [domain-repos.schema.json](../../../schemas/domain-repos.schema.json).
- If adding to an existing domain file, append a concise entry under `repositories:` (inheriting the domain's `defaults` block).
- If creating a new domain file `config/orgs/<org>/repos/<domain-key>.yaml`, include `# yaml-language-server: $schema=../../../../schemas/domain-repos.schema.json` on line 1.
- Never store sensitive values in `environment_variables`.

### Step 3: Run Pre-Flight Validation
1. Execute the repository validation harness:
   ```bash
   ./scripts/validate.sh
   ```
2. Confirm that JSON Schema validation, cross-file team slug checks, and Rego policy checks pass with zero errors.

### Step 4: Summarize Configured Resources & Blast Radius
Provide a clear summary of the configuration:
- Organization, domain file, and repository visibility (`private` or `internal`).
- Effective archetype and branch protection settings on `main`.
- Team access mappings and deployment environment approval gates.
