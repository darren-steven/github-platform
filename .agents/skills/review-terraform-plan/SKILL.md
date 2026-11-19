---
name: review-terraform-plan
description: Coaches contributors of any IaC experience level through running a read-only OpenTofu plan (./scripts/tofu-plan.sh), interpreting + / ~ / - / import diff symbols, tracing changes back to YAML files in config/, and safely aligning drift. Use this skill when a user asks to run, inspect, or understand a Terraform/OpenTofu plan.
---

# Reviewing & Aligning an OpenTofu Plan (`GHEC-IaC`)

Use this skill to guide users through reading `tofu plan` output clearly and building confidence with Infrastructure-as-Code.

---

## 1. Running a Safe Read-Only Plan

Always use the repository's read-only wrapper script (never raw `tofu apply` during alignment):

```bash
./scripts/tofu-plan.sh <org-slug>
```

The wrapper runs `./scripts/validate.sh` first, uses an in-memory `GITHUB_TOKEN`, initializes the stack, and executes `tofu plan` without modifying GitHub.

---

## 2. How to Explain Plan Symbols to Contributors

Translate OpenTofu plan symbols into plain English:
- **`+ create`**: A new GitHub resource (for example, a new Repository Ruleset or Deployment Environment) that exists in YAML but not yet in GitHub.
- **`~ update in-place`**: An existing GitHub resource (adopted via `imports.tf`) whose live setting differs from YAML — e.g., upgrading `min_reviewers` from `0` to `2` or downgrading a team permission from `admin` to `maintain`.
- **`-/+ destroy and then create replacement`**: A destructive replacement. **Flag this prominently** and verify why the provider requires replacement before proceeding.
- **`- destroy`**: Removing a resource. Note that `github_repository` enforces `archive_on_destroy = true`, so removing a repo from YAML archives it rather than permanently deleting it.
- **`import`**: Adopting an existing live GitHub resource into state via `environments/<org>/imports.tf` without recreating it.

---

## 3. Guiding Manual Alignment Back to YAML

When a user reviews a diff and wants to align the YAML config before applying:
1. Identify the exact resource address (e.g., `module.repositories.github_repository.this["my-repo"]`).
2. Trace it back to the owning YAML file:
   - Org settings / Actions → `config/orgs/<org>/org.yaml`
   - Teams → `config/orgs/<org>/teams.yaml`
   - Repositories, rulesets, team access, environments → `config/orgs/<org>/repos/<domain>.yaml`
   - Archetype baselines → `config/enterprise.yaml`
3. Explain whether the difference is:
   - **Intentional Baseline Enforcement** (Tier 1/2 guardrail bringing a drifted repo up to standard — keep YAML as-is), or
   - **Legitimate Domain/Repo Tuning** (adjust a bounded Tier 2 dial in YAML within schema limits).
4. After any YAML edit, run `./scripts/validate.sh` (and `python3 scripts/generate_imports.py --org <org>` if teams or repos were added/renamed), then re-run `./scripts/tofu-plan.sh <org>`.
