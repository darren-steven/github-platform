---
name: author-github-module
description: Enforces OpenTofu coding standards for GitHub Enterprise Cloud modules using the integrations/github provider, including Tier 1 HCL invariants, modern Repository Rulesets, two-pass team nesting, and directory documentation. Use this skill when writing or refactoring HCL code in modules/ or environments/.
---

# Authoring GitHub Enterprise Cloud OpenTofu Modules

Use this skill whenever creating or modifying `.tf` files inside `modules/` or `environments/`.

---

## 1. Architecture & Provider Standards

1. **Provider**: Use `integrations/github` (`~> 6.6`) with OpenTofu `>= 1.8.0`.
2. **Per-Organization Root Stacks**: Each organization has its own root stack in `environments/<org>/` matching `config/orgs/<org>/` 1:1. Do not introduce multi-provider alias routing inside reusable modules.
3. **Pure-HCL Data Layer (`modules/config-resolver`)**: Keep YAML decoding and 4-layer inheritance merging (`Enterprise Archetype` → `Org` → `Domain` → `Repository`) isolated inside `modules/config-resolver/`. Downstream resource modules should receive clean, typed maps.
4. **Modern Repository Rulesets**: Use `github_repository_ruleset` targeting `~DEFAULT_BRANCH` rather than legacy `github_branch_protection`.
5. **Two-Pass Team Hierarchy**: In `modules/teams`, create root teams (`parent_team == null`) before child teams (`parent_team != null`) and merge them into a unified `team_ids_by_slug` output.

---

## 2. Mandatory Tier 1 Invariants in HCL

Never weaken or omit these engine-level controls:
- `github_repository`:
  - `validation {}` blocks `visibility == "public"`.
  - `archive_on_destroy = true` (prevents accidental permanent deletion).
- `github_team_repository`:
  - `validation {}` blocks `permission == "admin"`.
- `github_organization_settings`:
  - `members_can_create_public_repositories = false`.
- `github_actions_organization_workflow_permissions`:
  - `default_workflow_permissions = "read"`.
  - `can_approve_pull_request_reviews = false`.
- `github_actions_runner_group`:
  - `allows_public_repositories = false`.
- `github_repository_ruleset`:
  - `deletion = true`, `non_fast_forward = true`.
  - `dismiss_stale_reviews_on_push = true`, `require_last_push_approval = true`.
  - `required_approving_review_count >= 2` (`>= 3` for `regulated-workload`).

---

## 3. Documentation & Discoverability Checklist

Before finishing any module or environment change:
1. Ensure every directory under `modules/` and `environments/` has an up-to-date `README.md`.
2. Add concise inline header comments above each resource block linking it to the YAML dial(s) it implements.
3. Run `./scripts/validate.sh` from the repository root and confirm all 4 validation layers pass.
4. Report the **Blast Radius** (Scope, Resource Impact, Approval Requirement).
