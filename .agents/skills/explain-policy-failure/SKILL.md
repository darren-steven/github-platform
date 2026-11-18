---
name: explain-policy-failure
description: >-
  Runs the validation suite (./scripts/validate.sh), parses JSON Schema, cross-file
  referential, or OPA/Conftest policy validation errors, explains in plain English why
  the guardrail blocked the change, and offers compliant remediation options. Use this
  skill when validation fails or when a maintainer asks why their change was rejected.
---

# Explain & Remediate Policy or Validation Failures (`explain-policy-failure`)

Use this skill whenever `./scripts/validate.sh` or a CI check fails, or when a maintainer is unsure why an edit to `config/` was rejected.

## Workflow Steps

### Step 1: Execute Validation & Capture Output
Run the unified validation script:
```bash
./scripts/validate.sh
```

### Step 2: Classify the Failure Source
Identify which guardrail layer caught the issue:
1. **Layer 1 — JSON Schema Validation (`schemas/*.schema.json`)**:
   - Triggered by syntax errors, unknown YAML keys, wrong data types, disallowed `visibility: public`, disallowed `permission: admin`, or out-of-range numbers (`minimum` / `maximum` / `enum`).
2. **Layer 2 — Cross-File Referential Integrity (`scripts/validate_config.py`)**:
   - Triggered when a domain repository file references a team slug not present in that organization's `teams.yaml` (`[REPO-TEAM-REF]`), duplicates a repository name within an org (`[REPO-DUPLICATE]`), or mismatches a filename/organization slug.
3. **Layer 3 — Policy-as-Code Gate (`policies/*.rego`)**:
   - Triggered when a configuration violates an enterprise or archetype invariant (e.g., `regulated-workload` with fewer than 3 reviewers or unsigned commits, disabling GHAS on a production archetype, production environment missing `require_approval: true` / `approver_teams`, or secret keywords in `environment_variables`).

### Step 3: Translate into Plain Language for the Maintainer
Format your explanation clearly:
1. **What Failed**: File path, error code (e.g. `[REPO-POLICY-001]` or `[REPO-TEAM-REF]`), and YAML field.
2. **Why It Was Blocked**: The specific security or governance reason behind the guardrail (reference [docs/dials-catalog.md](../../../docs/dials-catalog.md)).
3. **How to Fix It Safely**: Provide the exact compliant YAML snippet within allowed Tier 2 bounds.
   - *Reminder*: Never suggest editing `schemas/`, `policies/`, or `scripts/` to silence a validation error on a routine `config/` change.
