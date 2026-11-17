# Contributor & Maintainer Guide (`AzDo-IaC`)

This guide explains how to make changes safely in `AzDo-IaC`, regardless of your familiarity with OpenTofu/Terraform or Azure DevOps internals.

---

## 1. Choose Your Path

For routine project work, use the **Maintainer / Contributor** path. You can update YAML and run the validation script without learning OpenTofu. Only use the Platform Engineer path when changing the rules or infrastructure engine itself.

| Role | What You Edit | What You Need to Know |
| :--- | :--- | :--- |
| **Maintainer / Contributor** | [`config/projects/`](../config/projects/), [`config/groups.yaml`](../config/groups.yaml), [`config/org.yaml`](../config/org.yaml) | YAML configuration only. Use the schema guidance in the files and run `./scripts/validate.sh` to check your changes. Project files are usually project-scoped; organization settings can affect the whole organization. |
| **Platform Engineer** | [`modules/`](../modules/), [`schemas/`](../schemas/), [`policies/`](../policies/), [`environments/`](../environments/), [`.agents/skills/`](../.agents/skills/) | OpenTofu/HCL, JSON Schema, and OPA/Rego. You maintain the engine and the guardrails that safely expose configuration to maintainers. |

### Maintainer quick path

1. Edit the relevant YAML file in `config/`.
2. Keep settings within the bounds documented in the [dials and baselines catalog](./dials-catalog.md).
3. Run `./scripts/validate.sh`.
4. Open a pull request and review the validation results and proposed plan.

If a setting is blocked by a schema or policy, do not change the engine just to make it pass. Ask a Platform Engineer if the available configuration options do not meet your need.

---

## 2. Using AI Assistants Safely (Google Gemini & GitHub Copilot)

This repository includes built-in AI skills and guardrails that work identically in **Google Gemini (Antigravity / Gemini CLI)** and **GitHub Copilot (VS Code / Coding Agent)**.

### Common Tasks & Prompts You Can Use

| Goal | Natural Language Prompt (Gemini / Copilot) | Copilot Slash Command |
| :--- | :--- | :--- |
| **Change a project or org setting** | *"Increase minimum reviewers for `example-service` to 3 and require squash merge only."* | `/adjust-org-dial` |
| **Onboard a new AzDO project** | *"Onboard a new `standard-microservice` project called `billing-engine` with `api` and `worker` repos."* | `/onboard-project` |
| **Understand why validation failed** | *"Explain why `./scripts/validate.sh` failed on my project YAML and show me how to fix it."* | `/explain-policy-failure` |
| **Expose a new dial (Platform Engineers)** | *"Expose a new bounded dial for PR status check timeout across schema, policy, and module."* | `/create-baseline-dial` |

> **Built-in Safety Net**: If you ask the AI for a setting that violates our security baseline (such as setting `min_reviewers: 1` or putting a secret in a plain-text variable group), the AI is instructed to explain the policy constraint and suggest a compliant option rather than modifying the underlying OpenTofu modules.

---

## 3. Step-by-Step: Onboarding a New Project

1. **Copy the example or ask your AI assistant**:
   - Copy [config/projects/example-service.yaml](../config/projects/example-service.yaml) to `config/projects/<your-project-key>.yaml` (the filename must match `project.key`).
2. **Choose your archetype**:
   - `standard-microservice`, `regulated-workload`, or `sandbox` (see [docs/dials-catalog.md](./dials-catalog.md)).
3. **Define teams, repositories, and environments**:
   - Any environment named `prod` or `production` must set `require_approval: true` and name an `approver_team` from your `teams` list.
   - Any secret variables must use a `key_vault` block referencing an Azure Key Vault and service connection—never commit raw secrets.
4. **Validate locally**:
   ```bash
   ./scripts/validate.sh
   ```
5. **Open a Pull Request**:
   - The CI pipeline will run `./scripts/validate.sh` and `tofu plan`, posting the planned Azure DevOps changes on your PR.

Before running OpenTofu against Azure DevOps, make sure your standing
permissions allow planning and use time-limited PIM elevation for applies. See
the [OpenTofu access and Azure PIM guide](./permissions-and-pim.md) for the
required access setup and commands.

## 4. Platform Engineering (Usually Not Needed for Project Changes)

Platform Engineers maintain the underlying infrastructure implementation, not individual project settings:

- `modules/` and `environments/` define how Azure DevOps resources are provisioned.
- `schemas/` and `policies/` define which YAML configurations are allowed.
- `.agents/skills/` contains shared AI-assisted workflows and guardrails.

Changes to these areas can affect multiple projects or the organization and require the appropriate platform review. Read the [architecture reference](../ARCHITECTURE.md) for the infrastructure data flow and the [dials and baselines catalog](./dials-catalog.md) to understand which settings are intentionally available to maintainers.
