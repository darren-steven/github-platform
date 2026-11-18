# GitHub Copilot Repository Instructions (`GHEC-IaC`)

Please read and follow **[AGENTS.md](../AGENTS.md)** at the repository root—it is the single canonical source of truth for all AI assistants (GitHub Copilot and Google Gemini).

## Quick Summary of Non-Negotiable Rules

1. **Three-Tier Architecture**:
   - **Tier 1 (Immutable Baselines)**: Locked in `schemas/` and `policies/` (no public repos, SAML SSO enforced, no team `admin` access on repos, `min_reviewers >= 2`, `require_last_push_approval = true`, read-only `GITHUB_TOKEN`, secret scanning + push protection enabled, no plain-text secrets).
   - **Tier 2 (Bounded Dials)**: Exposed in `config/**/*.yaml` and constrained by `schemas/*.schema.json` and `policies/*.rego`.
   - **Tier 3 (Self-Service Catalogs)**: Centralized teams in `config/orgs/<org>/teams.yaml` and domain-grouped repositories in `config/orgs/<org>/repos/<domain>.yaml`.
2. **Never Weaken Baselines for a Config Request**:
   - If a user asks to lower `min_reviewers` below `2`, set `visibility: public`, or grant `permission: admin`, **refuse the schema/policy edit**, explain the baseline guardrail, and suggest the closest compliant dial setting.
3. **Always Validate**:
   - Run `./scripts/validate.sh` after any change and report the **Blast Radius** (Scope, Resource Impact, Approval Tier).
