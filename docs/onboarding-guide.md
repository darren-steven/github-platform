# Contributor & Maintainer Guide (`GHEC-IaC`)

This guide explains how to manage GitHub Organizations, Teams, and Repositories safely through YAML in `config/`.

---

## 1. Choose Your Path

| Role | What You Edit | What You Need to Know |
| :--- | :--- | :--- |
| **Maintainer / Contributor** | `config/orgs/<org>/repos/<domain>.yaml`, `config/orgs/<org>/teams.yaml` | YAML configuration only. Use IDE autocomplete powered by JSON Schemas and run `./scripts/validate.sh` before opening a PR. |
| **Organization / Platform Admin** | `config/orgs/<org>/org.yaml`, `config/enterprise.yaml`, `schemas/`, `policies/`, `scripts/`, `.agents/skills/` | JSON Schema, OPA/Rego, and enterprise governance guardrails. |

---

## 2. Common Day-to-Day Tasks

### A. Add a New Repository to an Existing Domain

1. Open the domain file for your area (for example, [`config/orgs/taswater-core/repos/platform-services.yaml`](../config/orgs/taswater-core/repos/platform-services.yaml) or [`config/orgs/taswater-digital/repos/customer-channels.yaml`](../config/orgs/taswater-digital/repos/customer-channels.yaml)).
2. Append your repository under `repositories:`. Because `archetype`, `team_access`, and `environments` are already set in the file's `defaults:` block, you only need to specify what is unique to your repo:
   ```yaml
   - name: "leak-detection-service"
     description: "Acoustic sensor ingestion service for pipeline leak detection."
     required_status_checks:
       - "ci / build-and-test"
   ```
3. If your repository handles regulated data (e.g., PCI, identity, SCADA control), set `archetype: "regulated-workload"`.
4. Run `./scripts/validate.sh` to verify your changes.

### B. Create a New Domain Repository File (for 5–15 Related Repos)

1. Copy an existing domain file to `config/orgs/<org>/repos/<your-domain-key>.yaml` (the filename must match `domain.key`).
2. Set the `defaults:` block with your domain's default `archetype`, `team_access` (referencing team slugs from `config/orgs/<org>/teams.yaml`), and `environments`.
3. Add your repositories under `repositories:` and run `./scripts/validate.sh`.

### C. Add or Update a GitHub Team

1. Open `config/orgs/<org>/teams.yaml` (e.g., [`config/orgs/taswater-core/teams.yaml`](../config/orgs/taswater-core/teams.yaml)).
2. Add your team with a unique kebab-case `slug`, `name`, `description`, `privacy: "closed"`, `role_tier`, optional `parent_team`, and optional Entra ID `idp_group_id`.
3. Reference that `slug` in your domain repository file's `team_access`, `codeowners_teams`, or `environments[].approver_teams`.
4. Run `./scripts/validate.sh`.

---

## 3. Using AI Assistants Safely (Google Gemini & GitHub Copilot)

This repository includes built-in AI skills in `.agents/skills/` that work across **Google Gemini (Antigravity)** and **GitHub Copilot**:

| Goal | Example Prompt | Skill |
| :--- | :--- | :--- |
| **Change a repo, domain, or org dial** | *"Set `min_reviewers` to 3 on `customer-portal-bff` and require squash merge only."* | `adjust-org-dial` |
| **Onboard a new repo, domain, or team** | *"Add a new `standard-microservice` repo called `meter-reads-api` to `customer-channels`."* | `onboard-project` |
| **Understand why validation failed** | *"Explain why `./scripts/validate.sh` failed and show me how to fix it."* | `explain-policy-failure` |
| **Expose a new dial (Platform Engineers)** | *"Expose a new bounded dial for `allow_update_branch` across schema, policy, and docs."* | `create-baseline-dial` |
