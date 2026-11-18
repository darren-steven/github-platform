---
name: adjust-org-dial
description: >-
  Guides maintainers through safely inspecting and modifying an exposed organization,
  team, domain, or repository configuration dial in config/**/*.yaml within approved
  baseline bounds. Use this skill when a user asks to change a GitHub repository
  policy, branch setting, Actions timeout, reviewer count, or organization setting.
---

# Adjust Organization, Domain, or Repository Dial (`adjust-org-dial`)

Use this skill whenever a user wants to modify an existing setting for the GitHub Enterprise (`config/enterprise.yaml`), an organization (`config/orgs/<org>/org.yaml`), teams (`config/orgs/<org>/teams.yaml`), or domain-grouped repositories (`config/orgs/<org>/repos/<domain>.yaml`).

## Workflow Steps

### Step 1: Identify Target Scope & Classify the Request
1. Determine whether the user wants to adjust:
   - **Enterprise-wide setting or archetype** -> [config/enterprise.yaml](../../../config/enterprise.yaml) (Schema: [schemas/enterprise.schema.json](../../../schemas/enterprise.schema.json))
   - **Organization-wide setting** -> `config/orgs/<org>/org.yaml` (Schema: [schemas/org.schema.json](../../../schemas/org.schema.json))
   - **Organization team catalog** -> `config/orgs/<org>/teams.yaml` (Schema: [schemas/teams.schema.json](../../../schemas/teams.schema.json))
   - **Domain or repository setting** -> `config/orgs/<org>/repos/<domain>.yaml` (Schema: [schemas/domain-repos.schema.json](../../../schemas/domain-repos.schema.json))
2. Check [docs/dials-catalog.md](../../../docs/dials-catalog.md) and the corresponding JSON Schema in `schemas/` to verify whether the requested setting is:
   - **Tier 2 (Exposed Bounded Dial)**: Check the allowed `minimum`, `maximum`, or `enum` values.
   - **Tier 1 (Locked Baseline)**: Locked by `schemas/` or `policies/*.rego` (e.g., making a repository public, granting team `admin` access, allowing 1 reviewer on `main`, disabling secret scanning on production archetypes, or enabling write-all default `GITHUB_TOKEN`).

### Step 2: Enforce Baseline Guardrail (If Out of Bounds)
- **STOP** if the requested value violates a Tier 1 baseline or falls outside Tier 2 schema bounds.
- **Do NOT** edit `schemas/`, `policies/`, or `scripts/` to force the change through.
- Explain clearly to the user:
  1. Why the requested value is blocked by the enterprise/organization baseline.
  2. The allowed bounds for that dial (e.g., `min_reviewers` allows `2` to `5`).
  3. Ask if they would like to apply the nearest compliant value instead.

### Step 3: Apply the Change in `config/`
- Edit only the relevant YAML file in `config/`.
- Preserve the `# yaml-language-server: $schema=...` directive at the top of the file and keep existing comments intact.

### Step 4: Validate & Report Blast Radius
1. Run the validation suite:
   ```bash
   ./scripts/validate.sh
   ```
2. Summarize the change for the user, explicitly stating:
   - **Modified Dial & Value**: Old value -> New value.
   - **Blast Radius**: Single repository, domain group (5–15 repos), organization-wide, or enterprise-wide.
   - **Approval Required**: `Maintainer` approval (for `config/orgs/<org>/repos/*` and `teams.yaml`) or `Platform Admin` approval (for `config/enterprise.yaml` and `config/orgs/<org>/org.yaml`).
