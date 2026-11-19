# GitHub Enterprise Cloud Governance & Configuration (`GHEC-IaC`)

This repository manages **GitHub Enterprise Cloud (GHEC)** organizations, teams, and repository archetypes using a declarative YAML configuration layer. **Maintainers only need to edit YAML files in `config/` and run `./scripts/validate.sh`.**

---

## Configuration Hierarchy (2 Orgs, ~20 Teams, ~150 Repositories)

```text
config/
├── enterprise.yaml                              # Enterprise settings & reusable repository archetypes
└── orgs/
    ├── taswater-core/                           # Organization 1: Core Engineering & Integration
    │   ├── org.yaml                             # Org-level security, Actions, and default branch dials
    │   ├── teams.yaml                           # Centralized GitHub Teams & Entra ID group mappings
    │   └── repos/
    │       ├── platform-services.yaml           # Domain group: 5–15 related repos + domain defaults
    │       └── data-integration.yaml            # Domain group: Data & integration repos
    └── taswater-digital/                        # Organization 2: Digital & Customer Channels
        ├── org.yaml
        ├── teams.yaml
        └── repos/
            └── customer-channels.yaml
```

---

## For Maintainers

### Onboard or Update a Repository

1. Open the appropriate domain file in `config/orgs/<org>/repos/<domain>.yaml` (or create a new `<domain>.yaml` file—see the [Onboarding Guide](./docs/onboarding-guide.md)).
2. Because each domain file defines shared `defaults` (`archetype`, `team_access`, `environments`), adding a standard repository takes just a few lines:
   ```yaml
   - name: "my-new-service"
     description: "Backend API for water meter telemetry."
   ```
3. Keep any overrides within the bounds documented in the [Dials & Baselines Catalog](./docs/dials-catalog.md).
4. Run the local validation suite:
   ```bash
   ./scripts/validate.sh
   ```

### Add or Update a GitHub Team

1. Edit `config/orgs/<org>/teams.yaml` to add or update the team's `slug`, `name`, `description`, `role_tier`, `parent_team`, and `idp_group_id`.
2. Reference the team's `slug` in `config/orgs/<org>/repos/<domain>.yaml` under `team_access`, `codeowners_teams`, or `environments[].approver_teams`.
3. Run `./scripts/validate.sh` to verify cross-file team slug references.

---

## Where to Go

| If you need to… | Start here |
| :--- | :--- |
| Onboard or configure a repository or deployment environment | `config/orgs/<org>/repos/<domain>.yaml` |
| Manage GitHub Teams or Entra ID group mappings | `config/orgs/<org>/teams.yaml` |
| Adjust organization-wide security or Actions settings | `config/orgs/<org>/org.yaml` |
| Inspect enterprise archetypes (`standard-microservice`, `regulated-workload`, `shared-library`, `sandbox`) | [`config/enterprise.yaml`](./config/enterprise.yaml) |
| Check allowed settings and security limits | [Dials & Baselines Catalog](./docs/dials-catalog.md) |
| Preview live GitHub drift (read-only OpenTofu plan) | [`environments/taswater/README.md`](./environments/taswater/README.md) (`./scripts/tofu-plan.sh taswater`) |
| Explore the OpenTofu module engine | [`modules/README.md`](./modules/README.md) |
| Extract existing GitHub Enterprise config & deduce domains | [GitHub Extraction & Candidate Guide](./docs/github-extraction-guide.md) |
| Understand the repo layout and pull request workflow | [Contributor & Maintainer Guide](./docs/onboarding-guide.md) |
| Review the architecture and inheritance model | [Architecture Reference](./ARCHITECTURE.md) |
