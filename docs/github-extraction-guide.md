# Extracting Existing GitHub Enterprise Config & Generating Candidates

This guide explains how to extract the current state of your existing **GitHub Enterprise Cloud** organizations (~2 organizations, ~20 teams, ~150 repositories), automatically deduce **domain-grouped YAML files** (`config/orgs/<org>/repos/<domain>.yaml`), and review a **Governance Drift Report** before bringing repositories under control.

---

## Overview of the Extraction & Candidate Pipeline

1. **Step 1 — Read-Only Inventory Snapshot (`scripts/export_github_inventory.py`)**:
   - Queries the GitHub REST API using a read-only token (`GITHUB_TOKEN`, `GH_TOKEN`, or `gh auth token`).
   - Exports organization settings, teams (including hierarchy and Entra ID group mappings), and all repositories (including team permissions, branch protection on the default branch, GHAS settings, and deployment environments) to `inventory/<org>.inventory.json`.
2. **Step 2 — Domain Deduction & Candidate YAML Generation (`scripts/generate_config_candidates.py`)**:
   - Reads `inventory/<org>.inventory.json` offline and generates schema-compliant YAML candidates in `candidates/<org>/`:
     - `candidates/<org>/org.yaml`
     - `candidates/<org>/teams.yaml`
     - `candidates/<org>/repos/<domain>.yaml`
     - `candidates/<org>/drift-report.md`
3. **Step 3 — Review & Promote by Domain**:
   - Inspect `candidates/<org>/drift-report.md` with domain maintainers, then copy approved domain YAML files into `config/orgs/<org>/repos/<domain>.yaml` and run `./scripts/validate.sh`.

---

## How Domain Alignment Is Deduced Automatically

When `scripts/generate_config_candidates.py` processes ~150 repositories in an organization, it groups them into `repos/<domain>.yaml` files using three signals in priority order:

1. **Team Associations (Primary Signal)**:
   - Inspects non-cross-cutting teams granted `push`, `maintain`, or `admin` access on a repository (ignoring org-wide teams like `platform-admins` or `security-auditors`).
   - Strips role suffixes (`-developers`, `-maintainers`, `-contributors`, `-leads`, `-engineers`, `-admins`) to identify the owning domain stem.
   - *Example*: Repositories assigned to `data-integration-developers` and `data-integration-maintainers` are automatically grouped into `repos/data-integration.yaml`.
2. **Multi-Repository Name Prefixes (Secondary Signal)**:
   - If a repository has no domain-specific team assigned yet, the generator checks for 1- or 2-token hyphenated prefixes shared by 2 or more repositories in the organization.
   - *Example*: `gis-viewer-api` and `gis-viewer-web` are automatically grouped into `repos/gis-viewer.yaml`.
3. **Repository Topics & Fallback (Tertiary Signal)**:
   - Falls back to the primary repository topic, or places standalone uncategorized repositories into `repos/general-services.yaml`.

Within each deduced domain file, the generator computes the **most common `archetype` and `team_access` matrix** across the domain's repositories and hoists them into the top-level `defaults:` block, keeping per-repository YAML entries minimal.

---

## Commands to Run (GitHub Actions or Local CLI)

> **Cross-Platform Case-Sensitivity Note (Windows / macOS / Linux)**: Always keep file and directory names **lowercase** (e.g. `taswater`, never `TasWater`). Even when GitHub's display login uses mixed case (`TasWater`), our scripts and manual workflow normalize slugs to lowercase automatically, and `./scripts/validate.sh` blocks case-colliding paths (`[PATH-CASE-COLLISION]` / `[PATH-UPPERCASE-SLUG]`) so checkouts never break on Windows.

### Option A — Run via GitHub Actions Manual Workflow (Recommended)

1. Open the **Actions** tab in GitHub and select **Export GitHub Org Inventory** ([`.github/workflows/export-inventory.yml`](../.github/workflows/export-inventory.yml)).
2. Click **Run workflow** on your branch with:
   - **`org`**: `taswater`
   - **`update_imports`**: `true` (regenerates `environments/taswater/imports.tf`, including existing repos, teams, permissions, and Jira autolinks)
   - **`update_candidates`**: `false` (or `true` if refreshing `candidates/taswater/`)
   - **`commit_to_branch`**: `true` to commit the refreshed `inventory/taswater.inventory.json` and `environments/taswater/imports.tf` directly to your branch, or `false` to download them as a workflow artifact.

### Option B — Export Live Organization Inventory Locally (Read-Only)

Authenticate with `gh auth login` (or export a read-only `GITHUB_TOKEN` with `read:org` and repository `Administration: Read` access), then run:

```bash
python3 scripts/export_github_inventory.py --org taswater
python3 scripts/generate_imports.py --org taswater
```

`export_github_inventory.py` streams timestamped `[team i/N]` and `[repo i/N]` progress lines to `stderr` so you can monitor long exports in real time (pass `--quiet` to suppress progress output). This writes `inventory/taswater.inventory.json` and updates `environments/taswater/imports.tf`.

### 2. Generate Candidate YAML Files & Drift Reports

Run the candidate generator against each snapshot:

```bash
python3 scripts/generate_config_candidates.py --inventory inventory/taswater-core.inventory.json
python3 scripts/generate_config_candidates.py --inventory inventory/taswater-digital.inventory.json
```

*(By default, `archived: true` repositories are excluded from active governance and listed in the report. Pass `--include-archived` if you want to generate YAML entries for archived repos as well.)*

### 3. Review the Drift Report & Promote into `config/`

1. Open `candidates/<org>/drift-report.md` to review:
   - Deduced domain files and how each domain was inferred.
   - Archived repositories excluded from onboarding.
   - **Baseline Drift Remediations**, such as:
     - **Team Admin Permission Downgraded**: Teams that currently have `admin` on a repo are converted to `maintain` in the candidate YAML to satisfy the Tier 1 baseline.
     - **Branch Protection Upgraded**: Repositories with unprotected default branches or `min_reviewers < 2` that will be upgraded to `2` (or `3` for `regulated-workload`).
     - **Non-Standard Default Branch**: Legacy repositories still using `master` instead of `main`.
     - **Production Environment Gate Added**: Any `prod` environment missing `require_approval: true`.
2. Copy the reviewed `teams.yaml` and `repos/<domain>.yaml` files into `config/orgs/<org>/` and validate:
   ```bash
   ./scripts/validate.sh
   ```
