---
name: create-baseline-dial
description: >-
  Guides Platform Engineers through exposing a new Tier 2 bounded configuration dial
  across JSON Schemas, OPA Rego policies, Python validation, YAML configs, and the
  dials catalog. Use this skill when a Platform Engineer asks to expose a new configurable
  dial or modify the baseline engine.
---

# Create or Evolve a Baseline Dial (`create-baseline-dial`)

Use this skill when a **Platform Engineer** wants to expose a new Tier 2 configuration dial or promote/demote a setting between Tier 1 (Immutable Baseline) and Tier 2 (Bounded Dial).

## Pre-Check: Confirm Platform Engineering Intent
Before modifying `schemas/`, `policies/`, or `scripts/`, verify that the user is intentionally modifying the **Platform Baseline Engine** (and not just trying to work around a validation error on a single repository).

## Lockstep Workflow

Every Tier 2 dial must be defined across all validation and documentation layers simultaneously so IDE validation, Policy-as-Code, and documentation never drift:

### Step 1: Update JSON Schema (`schemas/*.schema.json`)
1. Add the property to [enterprise.schema.json](../../../schemas/enterprise.schema.json), [org.schema.json](../../../schemas/org.schema.json), [teams.schema.json](../../../schemas/teams.schema.json), or [domain-repos.schema.json](../../../schemas/domain-repos.schema.json).
2. Always include:
   - `type` (`integer`, `boolean`, `string`, `object`, `array`)
   - `description` (including the allowed bounds and default value)
   - Explicit bounds (`minimum` / `maximum`, `enum`, or `pattern`)
   - `default` value

### Step 2: Update OPA / Conftest Policy & Validator (`policies/*.rego` & `scripts/validate_config.py`)
1. Add or update a `deny contains msg if { ... }` rule in [enterprise_baseline.rego](../../../policies/enterprise_baseline.rego), [org_baseline.rego](../../../policies/org_baseline.rego), or [repo_guardrails.rego](../../../policies/repo_guardrails.rego).
2. Mirror any cross-field or cross-file checks in [scripts/validate_config.py](../../../scripts/validate_config.py).

### Step 3: Update Documentation & Default Config (`docs/` & `config/`)
1. Document the new dial, its default, its allowed bounds, and its blast radius in [docs/dials-catalog.md](../../../docs/dials-catalog.md).
2. Add the dial with comments to the relevant YAML file in `config/`.

### Step 4: Execute Full Validation Suite
```bash
./scripts/validate.sh
```
Ensure all schema, Rego policy, and AI guardrail checks pass.
