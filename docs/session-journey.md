# From Blank Repo to Live Governed Azure DevOps Org: Session Journey & Presentation Guide

This document captures every prompt, architectural decision, guardrail catch, and live debugging step from the initial build session of `AzDo-IaC`. It is structured so you can use it directly as a **presentation storyboard or live-demo script**.

---

## Presentation Story Arc (5-Slide Summary)

1. **The Problem**: Managing Azure DevOps at scale across maintainers of mixed skill levels usually fails in one of two ways: either everyone edits raw Terraform (leading to weakened branch policies and snowflaked projects) or everything is locked behind a platform bottleneck.
2. **The Architecture ("Hardened Engine, Simple Dials")**:
   - **Tier 1 (Immutable Baselines)**: Locked in OpenTofu modules and OPA policies.
   - **Tier 2 (Bounded Dials)**: Exposed via IDE-validated YAML (`config/*.yaml` + JSON Schemas).
   - **Tier 3 (Self-Service Catalogs)**: Archetype-driven project onboarding (`standard-microservice`, `regulated-workload`, `sandbox`).
3. **AI-First Guardrails (Gemini + GitHub Copilot Parity)**:
   - Built `AGENTS.md`, scoped directory rules, and 5 canonical `SKILL.md` skills *before* writing a single line of HCL, ensuring AI assistants refuse to weaken engine baselines when adjusting dials.
4. **Zero-Secret Live Bootstrap (`tofutest`)**:
   - Exchanged a local `az login` session for a short-lived Entra ID token (`499b84ac-1321-427f-aa17-267ca6975798`) in memory—provisioning org groups, pools, projects, teams, repos, branch policies, and approval gates with **zero PATs**.
5. **Real-World Hardening & Guardrails in Action**:
   - Caught deprecated Copilot `.prompt.md` files, blocked hardcoded `file:` URI paths automatically via `validate.sh`, solved Azure DevOps's hidden "default repository" creation quirk with a new `create_default_repository` dial, and hardened CI permissions for public access.

---

## Complete Prompt-by-Prompt Session Log

### Phase 1: Architecture & Control-Plane Design

#### Step 1 — Initial Vision & Framework Blueprint
* **Prompt**:
  > *"This project is going to be an IaC implementation for managing an AzureDevOps organisation. We will start of with the assumption that the AzDo org has been created. we want to manage org policy, exposing imprtant dials against a strong baseline enforced by code. we want to start by creating a stong set of AI skills and guardrails. This repo will be maintained by people with various skill levels, so we want a well formed IaC structure, effective AI skills and guides (with compatability across gemini and github copilot). can we plan out what the framework would look like"*
* **Actions Taken**:
  * Designed the **Three-Tier Governance Model** (Tier 1 Immutable Baselines, Tier 2 Bounded Dials, Tier 3 Self-Service Catalogs).
  * Designed the **Cross-Agent AI Compatibility Layer** combining `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, and `.agents/skills/*/SKILL.md`.
  * Identified the `microsoft/azuredevops` provider gap for org-level security toggles and proposed isolating it in a bridge module.

---

#### Step 2 — OpenTofu & Out-of-Band Control Plane (`CODEOWNERS` vs. Azure Repos)
* **Prompt**:
  > *"looks good. Opentofu is fine (provided the maturity in providers is there). One thing I noticed is the use of CODEOWNERS. If this repo is hosted in AzDo repos, which is our target platform, I beleive that doesn't exist. Having said that, there may be some advantage to hosting this in github (which we have also), so we can bootstrap wothout AzDo being operational"*
* **Actions Taken**:
  * Confirmed 1:1 provider parity for `microsoft/azuredevops` in the OpenTofu Registry (`registry.opentofu.org`).
  * Documented the **"Out-of-Band Control Plane"** pattern: hosting the IaC repository in **GitHub** prevents circular bootstrap/recovery dependencies (if an AzDO policy change locks out AzDO pipelines, GitHub Actions can still roll it back) and provides native `.github/CODEOWNERS` enforcement.
  * Added a portable [modules/self-governance-policies](../modules/self-governance-policies/main.tf) module using `azuredevops_branch_policy_auto_reviewers` with `path_filters` (`/modules/*`, `/schemas/*`, `/policies/*`) so the repo has an exact `CODEOWNERS` equivalent if ever mirrored or moved to Azure Repos.

---

#### Step 3 — Full Repository Scaffolding
* **Prompt**:
  > *[Approved the Framework Plan artifact]*
* **Actions Taken**:
  * Scaffolded 40+ files across 5 layers:
    1. **AI Guardrails & Skills**: [AGENTS.md](../AGENTS.md), [GEMINI.md](../GEMINI.md), [config/AGENTS.md](../config/AGENTS.md), [modules/AGENTS.md](../modules/AGENTS.md), [.github/copilot-instructions.md](../.github/copilot-instructions.md), and 5 skills in `.agents/skills/` (`adjust-org-dial`, `onboard-project`, `create-baseline-dial`, `author-azdo-module`, `explain-policy-failure`).
    2. **JSON Schemas**: [org.schema.json](../schemas/org.schema.json), [groups.schema.json](../schemas/groups.schema.json), and [project.schema.json](../schemas/project.schema.json) wired into [.vscode/settings.json](../.vscode/settings.json).
    3. **Declarative YAML Configs**: [config/org.yaml](../config/org.yaml), [config/groups.yaml](../config/groups.yaml), and [config/projects/example-service.yaml](../config/projects/example-service.yaml).
    4. **OPA Rego Policies**: [org_baseline.rego](../policies/org_baseline.rego) and [project_guardrails.rego](../policies/project_guardrails.rego).
    5. **OpenTofu Engine & Validation Harness**: `modules/*`, `environments/prod-org/*`, and [scripts/validate.sh](../scripts/validate.sh).

---

### Phase 2: Refining Cross-Agent AI & Guardrails

#### Step 4 — Unifying on `SKILL.md` for GitHub Copilot's New Agent Runtime
* **Prompt**:
  > *[Shared screenshot of VS Code / GitHub Copilot's "Keep your customizations working: Convert Prompt to Skills (Workspace)" migration banner flagging `.github/prompts/*.prompt.md`]*
* **Actions Taken**:
  * Identified that GitHub Copilot's new agent runtime deprecated `.github/prompts/*.prompt.md` in favor of the unified `SKILL.md` standard—and that Copilot's auto-migrator sets `disable-model-invocation: true` on converted prompts, which breaks automatic skill activation.
  * Deleted `.github/prompts/*.prompt.md` so both Gemini and Copilot load the canonical `.agents/skills/*/SKILL.md` files directly.
  * Added a guardrail in [scripts/validate.sh](../scripts/validate.sh) blocking `.github/prompts/*.prompt.md` and ensuring no `SKILL.md` sets `disable-model-invocation: true`.

---

#### Step 5 — Eliminating Hardcoded Machine Paths
* **Prompt**:
  > *"we have some hardocded references to the full path of this project that e need to mak project relative"*
* **Actions Taken**:
  * Replaced all machine-specific `file:` URI links across markdown documentation and `SKILL.md` files with repository-relative paths.
  * Added a permanent check in Layer 4 of [scripts/validate.sh](../scripts/validate.sh) that scans every file in the repository and fails validation if any file contains local machine path prefixes or `file:` URIs.

---

#### Step 6 — Clarifying `Mastercard/restapi`
* **Prompt**:
  > *"what's teh mastercard rest api for?"*
* **Actions Taken**:
  * Explained that `Mastercard/restapi` is the open-source generic REST API provider for Terraform/OpenTofu, used inside [modules/org-settings-api-bridge](../modules/org-settings-api-bridge/main.tf) to manage Azure DevOps organization-level security toggles (`Policy.AllowOrgPublicProjects`, `Policy.DisallowAnonymousAccess`, etc.) that aren't exposed as native resources in `microsoft/azuredevops`.

---

### Phase 3: Live Provisioning Against Azure DevOps (`tofutest`)

#### Step 7 — Zero-PAT Local Environment Setup
* **Prompt**:
  > *"all good. OK, I have created a branch. I want to create a real test against my personal azure account. what do we need to do to setup the repo and the local environment for that. I have done an az login to my subscription and tenant, and create the emty org"*
* **Actions Taken**:
  * Created [mise.toml](../mise.toml) pinning `opentofu = "1.8.2"`.
  * Created [scripts/tofu-local.sh](../scripts/tofu-local.sh) to exchange the active `az login` session for a short-lived Azure DevOps Entra ID access token (`az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798`) in memory—requiring zero PATs on disk.
  * Removed placeholder Entra group GUIDs from [config/groups.yaml](../config/groups.yaml) and fixed `azuredevops_check_approval.approvers` to pass team `.id` instead of `.descriptor`.

---

#### Step 8 — Targeting `https://dev.azure.com/tofutest`
* **Prompt**:
  > *"Org is https://dev.azure.com/tofutest"*
* **Actions Taken**:
  * Updated [config/org.yaml](../config/org.yaml) to point to `tofutest`, validated via `./scripts/validate.sh`, and reported the organization-wide blast radius.

---

#### Step 9 — Fixing `tofu fmt` Alignment
* **Prompt**:
  > *[Pasted output of `./scripts/validate.sh` where `tofu fmt -check` flagged 3 module `.tf` files]*
* **Actions Taken**:
  * Aligned `=` signs in [modules/org-settings-api-bridge/main.tf](../modules/org-settings-api-bridge/main.tf), [modules/security-namespaces/main.tf](../modules/security-namespaces/main.tf), and [modules/self-governance-policies/main.tf](../modules/self-governance-policies/main.tf) and updated the static regex in `scripts/validate.sh` to tolerate whitespace formatting.

---

#### Step 10 — Fixing `allow_basic_no_fast_forward` on `tofu plan`
* **Prompt**:
  > *[Pasted `./scripts/tofu-local.sh plan` error: `An argument named "allow_no_fast_forward" is not expected here` in `azuredevops_branch_policy_merge_types`]*
* **Actions Taken**:
  * Inspected the `terraform-provider-azuredevops_v1.16.0` binary struct tags (`AllowNoFastForward tf:"allow_basic_no_fast_forward"`) and updated [modules/project-archetype/branch_policies.tf](../modules/project-archetype/branch_policies.tf) to map the YAML dial `no_fast_forward` to `allow_basic_no_fast_forward`.

---

#### Step 11 — Fixing Plain-Text Variable Group Schema on `tofu apply`
* **Prompt**:
  > *[Pasted `./scripts/tofu-local.sh apply` output showing successful creation of groups, pools, project, teams, repos, branch policies, and permissions, followed by `LOG_LEVEL variable can have either only value attribute or both is_secret and secret_value attributes`]*
* **Actions Taken**:
  * Updated `azuredevops_variable_group.plain_vars` in [modules/project-archetype/main.tf](../modules/project-archetype/main.tf) to omit `is_secret = false` on non-secret variables. Subsequent `apply` completed 100% cleanly.

---

#### Step 12 — Operator Portal Verification Walkthrough
* **Prompt**:
  > *"OK, that completed - run me through what an operator should see inthe azure portal for this"*
* **Actions Taken**:
  * Produced a screen-by-screen verification guide ([docs/portal-check.md](./portal-check.md)) showing where to inspect the 4 org groups, 2 agent pools, private project overview, hidden Test Plans tab, 6 pipeline security switches, least-privilege Git permissions (`ForcePush = Deny`, `EditPolicies = Deny`), 5 branch policies on `main`, `prod` environment approval gate, and restricted variable group.

---

#### Step 13 — Guardrail Catching `file:` Links in Pasted Docs
* **Prompt**:
  > *[Pasted output of `./scripts/tofu-local.sh plan` failing at Step `[4/4]` due to hardcoded `file:` URI links in `./docs/portal-check.md`]*
* **Actions Taken**:
  * Demonstrated the repository guardrail catching machine-local `file:` links when chat text was saved to `docs/portal-check.md`. Converted the links to relative paths (`../config/...`).

---

### Phase 4: Architecture Deep-Dive, Public Readiness & Default Repo Dial

#### Step 14 — Module-by-Module OpenTofu Walkthrough
* **Prompt**:
  > *"OK, can you walk me through the terraform in detail - module by module, explaining how it all works together"*
* **Actions Taken**:
  * Documented the end-to-end data flow from `yamldecode()` in `environments/prod-org/main.tf` through `org-baseline`, `org-settings-api-bridge`, `security-namespaces`, `project-archetype`, and `self-governance-policies` (saved in [ARCHITECTURE.md](../ARCHITECTURE.md)).

---

#### Step 15 & 16 — Security Audit & Workflow Hardening for Public Access
* **Prompts**:
  > *"I'd like to give this repo readonly public access - anything sensitive I should eb aware of?"*
  > *"yes, tighten the perms"*
* **Actions Taken**:
  * Audited `.gitignore`, working tree, and `git log -p` history to confirm zero secrets, tokens, or `.tfstate` files were ever tracked.
  * Hardened [.github/workflows/ci-validate-plan.yml](../.github/workflows/ci-validate-plan.yml) to use top-level `permissions: contents: read`, scoped `id-token: write` and `pull-requests: write` strictly to `opentofu-plan`, and added a fork guard so PRs from external forks never trigger `opentofu-plan`.

---

#### Step 17 & 18 — Solving the Unmanaged Default Repository Quirk (`create_default_repository` Dial)
* **Prompts**:
  > *"It seems we create an "Example Platform Service" repo. where does that come from?"*
  > *"first option makes sense - we don;t want any unecpected objects. perhaps another option is to allow it's creation, with rules, just like any other repo? that is, we flag "create default" or similar, and can apply default policies"*
* **Actions Taken**:
  * Explained that Azure DevOps's Create Project API automatically provisions an unmanaged, uninitialized `<Project Name>` repository whenever Repos is enabled.
  * Used the **`create-baseline-dial` 4-layer workflow** to expose `create_default_repository` (`boolean`, default `false`) across [schemas/project.schema.json](../schemas/project.schema.json), [policies/project_guardrails.rego](../policies/project_guardrails.rego) (`[PROJ-POLICY-008]`), [modules/project-archetype/main.tf](../modules/project-archetype/main.tf), and [docs/dials-catalog.md](./dials-catalog.md).

---

#### Step 19 & 20 — Debugging Azure DevOps Default Repo API Race Conditions (`HTTP 400` & `TF401035`)
* **Prompts**:
  > *[Pasted `HTTP Error 400: Bad Request` on `PATCH` rename attempt, and then `TF401035: The object 'd0ccda453ae9e52f6c33b402e1d14462f5727e3a' does not exist` when deleting and immediately recreating a repo of the same name]*
* **Actions Taken**:
  * Replaced the delete-and-recreate approach with an **Adopt-In-Place** reconciliation resource (`terraform_data.reconcile_default_repository` + `data.azuredevops_git_repository.default_repo` in [modules/project-archetype/main.tf](../modules/project-archetype/main.tf)):
    * When `create_default_repository: false`, it deletes the unmanaged `<Project Name>` repository.
    * When `create_default_repository: true`, it adopts the existing `<Project Name>` repository in-place (or creates it if previously deleted), pushes an initial `/README.md` commit to `refs/heads/main` with retry backoff, and attaches all 5 branch policies and team permissions via `data.azuredevops_git_repository.default_repo`.

---

#### Step 21 — Role of OPA `.rego` Policy Files
* **Prompt**:
  > *"what re teh .rego files for"*
* **Actions Taken**:
  * Explained the division of labor between **JSON Schemas** (single-field type and range validation in the IDE) and **OPA Rego Policies** (cross-field governance invariants like requiring `min_reviewers >= 3` on `regulated-workload` projects, requiring `approver_team` on `prod` environments, and blocking plain-text secrets in variable groups).
