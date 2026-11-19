# AI Guardrails: OpenTofu Environments (`environments/`)

This file scopes AI assistant behavior when working inside `environments/`. It extends the root [`AGENTS.md`](../AGENTS.md).

## Non-Negotiable Rules for `environments/`

1. **Phase 1 Is Strictly Plan-Only**:
   - Do **not** run `tofu apply` or `tofu destroy` during Phase 1 alignment unless the user explicitly transitions to Phase 2 and confirms the blast radius.
   - Always invoke `./scripts/tofu-plan.sh <org>` (which runs `./scripts/validate.sh` first) rather than raw `tofu` commands.
2. **Zero Secrets & Zero State Files in Git**:
   - Never commit `*.tfstate`, `*.tfstate.*`, `*.tfvars`, `tfplan`, or hardcoded GitHub tokens.
   - Authentication must use `GITHUB_TOKEN` injected in shell memory (e.g., via `gh auth token`).
3. **Keep `imports.tf` Synchronized**:
   - Regenerate `environments/<org>/imports.tf` via `python3 scripts/generate_imports.py --org <org>` whenever `teams.yaml` or `repos/*.yaml` changes during initial alignment.
4. **Coaching Contributors**:
   - When explaining `tofu plan` output to a user, follow [`.agents/skills/review-terraform-plan/SKILL.md`](../.agents/skills/review-terraform-plan/SKILL.md) to walk through `+` / `~` / `-` changes clearly and link every diff back to its YAML source file.
