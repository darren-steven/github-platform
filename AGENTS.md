# AI Agent Guardrails & Operating Rules (`GHEC-IaC`)

Welcome to the **GitHub Enterprise Cloud Infrastructure-as-Code (`GHEC-IaC`)** repository.
This file (`AGENTS.md`) is the **canonical source of truth** for AI assistants operating in this repository, including **Google Gemini (Antigravity / Gemini CLI)** and **GitHub Copilot (VS Code / Coding Agent)**.

---

## 1. Core Architectural Philosophy: "Hardened Engine, Simple Dials"

This repository governs a **GitHub Enterprise Cloud (GHEC)** system (~2 organizations, ~20 teams, and ~150 repositories) using a declarative **YAML Configuration Layer** (`config/`) validated by **JSON Schemas** (`schemas/`) and **OPA/Python Policy Guardrails** (`policies/`, `scripts/`).

To support maintainers of varying skill levels safely, all settings are divided into three strict tiers:

1. **Tier 1 — Immutable Baseline (Locked in `schemas/` & `policies/`)**:
   - Mandatory enterprise and organization security and governance invariants enforced by code.
   - Examples: No public repositories (`visibility` restricted to `private` or `internal`), SAML/Entra ID SSO enforced, no repository `admin` permission granted to teams in YAML, mandatory pull request reviews on `main` (`min_reviewers >= 2`), `dismiss_stale_reviews: true`, `require_last_push_approval: true`, read-only default `GITHUB_TOKEN` workflow permissions, mandatory secret scanning & push protection on non-sandbox archetypes, and no plain-text secrets in environment variables.
   - **No YAML dial exists to disable Tier 1 controls.**
2. **Tier 2 — Bounded Dials (Exposed in `config/**/*.yaml`, Constrained by `schemas/` & `policies/`)**:
   - Safe configuration parameters that maintainers can tune within approved boundaries.
   - Examples: `min_reviewers` (`2` to `5`; `3` to `5` for `regulated-workload`), merge strategy toggles (`allow_squash_merge`, `allow_merge_commit`, `allow_rebase_merge`, `allow_auto_merge`, `delete_branch_on_merge`), repository feature toggles (`has_issues`, `has_wiki`, `has_discussions`, `has_projects`), `default_job_timeout_minutes` (`15` to `180`), and CODEOWNERS / status check requirements.
3. **Tier 3 — Self-Service Catalogs (Exposed in `config/orgs/<org>/teams.yaml` & `config/orgs/<org>/repos/<domain>.yaml`)**:
   - Declarative management of GitHub Teams (with Entra ID `idp_group_id` sync and parent/child hierarchy) and domain-grouped repositories inheriting from enterprise archetypes (`standard-microservice`, `regulated-workload`, `shared-library`, `sandbox`).

---

## 2. Non-Negotiable AI Guardrails

### Guardrail 1: Never Weaken the Engine to Satisfy a Dial Request
- When a user asks to configure a repository, domain, team, or organization setting, treat it as a **Maintainer task** targeting `config/`.
- **NEVER** modify `schemas/`, `policies/`, or `scripts/` to bypass a validation error, lower a minimum security bound (e.g., changing `min_reviewers >= 2` to `>= 1`), or disable a Tier 1 baseline control unless the user **explicitly** states they are performing a **Platform Baseline Change** and confirms the security trade-off.
- If a user asks for a setting that violates a Tier 1 invariant or Tier 2 bound (for example, *"make this repository public"*, *"grant team admin access"*, or *"set minimum reviewers to 1"*), **stop and explain**:
  1. Which baseline invariant or dial bound blocks the request.
  2. Why the invariant exists.
  3. The closest compliant configuration available in `config/`.

### Guardrail 2: Zero Secrets & Zero Hardcoded Credentials
- Never write Personal Access Tokens (PATs), GitHub App private keys, Entra ID client secrets, or raw secret values into `.yaml`, `.tf`, `.tfvars`, or shell scripts.
- Repository `environment_variables` in YAML are strictly for non-sensitive configuration; any sensitive values must be managed via GitHub Encrypted Secrets or Azure Key Vault OIDC federation.

### Guardrail 3: Explicit Blast-Radius Reporting
- Before finalizing any change to `config/enterprise.yaml`, `config/orgs/<org>/org.yaml`, `config/orgs/<org>/teams.yaml`, or `config/orgs/<org>/repos/<domain>.yaml`, explicitly state the **Blast Radius** in your response:
  - **Scope**: Single repository, domain group (5–15 repos), organization-wide, or enterprise-wide.
  - **Resource Impact**: In-place policy/configuration update vs. destructive change.
  - **Approval Requirement**: Whether the modified path requires **Platform Admin** approval (`config/enterprise.yaml`, `schemas/`, `policies/`, `scripts/`, `.agents/`, `.github/`) or **Maintainer** approval (`config/orgs/<org>/repos/*.yaml`, `config/orgs/<org>/teams.yaml`).

### Guardrail 4: Mandatory Verification Loop
- After making any change to `config/`, `schemas/`, `policies/`, or `scripts/`, you **must** run `./scripts/validate.sh` before declaring the task complete.
- Never claim a configuration is valid until JSON Schema validation, cross-file team/repo integrity checks, and policy checks pass.

---

## 3. Repository Navigation & Persona Boundaries

| Directory / Path | Primary Persona | Allowed Routine Operations | Restricted Operations |
| :--- | :--- | :--- | :--- |
| `config/enterprise.yaml` | **Platform Engineers** | Manage enterprise baselines, managed org list, and reusable repository archetypes. | Weakening Tier 1 security settings or archetype floors. |
| `config/orgs/<org>/org.yaml` | **Org / Platform Admins** | Edit organization dials, Actions token settings, and runner groups. | Adding undocumented keys not present in `schemas/org.schema.json`. |
| `config/orgs/<org>/teams.yaml` | **All Maintainers** | Add/update GitHub teams, parent/child hierarchy, and Entra ID `idp_group_id` mappings. | Duplicating team slugs or referencing non-existent parent teams. |
| `config/orgs/<org>/repos/<domain>.yaml` | **All Maintainers** | Onboard repositories, set archetypes, map team access, and configure environments. | Granting `admin` team permissions, making repos `public`, or referencing unknown teams. |
| `schemas/` | **Platform Engineers** | Add or update JSON Schema definitions when exposing a new bounded dial. | Relaxing `minimum`/`maximum`/`enum` security bounds without updating `policies/`. |
| `policies/` | **Platform Engineers** | Add or update OPA/Conftest Rego policies enforcing enterprise, org, and repo rules. | Deleting or weakening `deny` rules to silence failing checks. |
| `.agents/skills/` | **Platform Engineers** | Author canonical AI skills (`SKILL.md`) shared across Gemini and GitHub Copilot. | Creating legacy `.github/prompts/*.prompt.md` files or tool-specific instructions that drift. |

---

## 4. Available AI Skills & Workflows

Both **Google Gemini (Antigravity)** and **GitHub Copilot** natively discover Agent Skills (`SKILL.md`) in `.agents/skills/`:

1. **[adjust-org-dial](.agents/skills/adjust-org-dial/SKILL.md)**: Safely inspect and modify an exposed organization, domain, or repository dial in `config/` within schema bounds.
2. **[onboard-project](.agents/skills/onboard-project/SKILL.md)**: Onboard a new repository, domain group, or team in `config/orgs/<org>/` using an approved repository archetype.
3. **[create-baseline-dial](.agents/skills/create-baseline-dial/SKILL.md)**: End-to-end platform engineering workflow to expose a new bounded dial across JSON Schema, OPA policy, validation scripts, and documentation.
4. **[author-azdo-module](.agents/skills/author-azdo-module/SKILL.md)**: Standards for authoring infrastructure modules when backing YAML definitions with OpenTofu/Terraform.
5. **[explain-policy-failure](.agents/skills/explain-policy-failure/SKILL.md)**: Run `./scripts/validate.sh`, translate schema/OPA/referential errors into plain language, and guide maintainers to a compliant fix.
