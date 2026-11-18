---
applyTo: "config/**/*.yaml"
---
# Configuration Layer Instructions (`config/**/*.yaml`)

When editing files inside `config/`:
1. Keep the `# yaml-language-server: $schema=...` header on line 1 of every YAML file.
2. Check the matching schema in `schemas/` (`enterprise.schema.json`, `org.schema.json`, `teams.schema.json`, or `domain-repos.schema.json`) before adding or modifying fields.
3. Ensure any team slug referenced in `config/orgs/<org>/repos/<domain>.yaml` is defined in `config/orgs/<org>/teams.yaml`.
4. Never commit secrets, tokens, or passwords in `environment_variables`.
5. Run `./scripts/validate.sh` to verify JSON Schema and OPA/Python policy compliance.
