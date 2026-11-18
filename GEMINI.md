# Gemini / Antigravity Workspace Rules

# AI Agent Guardrails & Operating Rules (`GHEC-IaC`)

Welcome to the **GitHub Enterprise Cloud Infrastructure-as-Code (`GHEC-IaC`)** repository.
This file (`GEMINI.md`) mirrors [`AGENTS.md`](AGENTS.md) as the canonical source of truth for AI assistants operating in this repository.

---

## 1. Core Architectural Philosophy: "Hardened Engine, Simple Dials"

This repository governs a **GitHub Enterprise Cloud (GHEC)** system (~2 organizations, ~20 teams, and ~150 repositories) using a declarative **YAML Configuration Layer** (`config/`) validated by **JSON Schemas** (`schemas/`) and **OPA/Python Policy Guardrails** (`policies/`, `scripts/`).

1. **Tier 1 — Immutable Baseline (Locked in `schemas/` & `policies/`)**:
   - No public repositories (`visibility` restricted to `private` or `internal`), SAML SSO enforced, no repository `admin` permission granted to teams in YAML, mandatory pull request reviews on `main` (`min_reviewers >= 2`), `dismiss_stale_reviews: true`, `require_last_push_approval: true`, read-only default `GITHUB_TOKEN` workflow permissions, mandatory secret scanning & push protection on non-sandbox archetypes, and no plain-text secrets in environment variables.
2. **Tier 2 — Bounded Dials (Exposed in `config/**/*.yaml`, Constrained by `schemas/` & `policies/`)**:
   - Safe configuration parameters tunable within approved boundaries (`min_reviewers` `2..5`, merge strategies, repository feature toggles, `default_job_timeout_minutes` `15..180`, CODEOWNERS, and status checks).
3. **Tier 3 — Self-Service Catalogs (`config/orgs/<org>/teams.yaml` & `config/orgs/<org>/repos/<domain>.yaml`)**:
   - Declarative onboarding of GitHub Teams and domain-grouped repositories inheriting from enterprise archetypes (`standard-microservice`, `regulated-workload`, `shared-library`, `sandbox`).

---

## 2. Non-Negotiable AI Guardrails

1. **Never Weaken the Engine to Satisfy a Dial Request**:
   - Never modify `schemas/`, `policies/`, or `scripts/` to bypass a validation error or weaken a baseline bound unless explicitly performing a Platform Baseline Change.
2. **Zero Secrets & Zero Hardcoded Credentials**:
   - Never commit PATs, private keys, or secrets in YAML.
3. **Explicit Blast-Radius Reporting**:
   - State Scope (single repo, domain group, org-wide, or enterprise-wide), Resource Impact, and Approval Requirement before finalizing changes.
4. **Mandatory Verification Loop**:
   - Always run `./scripts/validate.sh` inside the standard sandbox (`BypassSandbox: false`) after editing YAML configs, schemas, policies, or scripts.
