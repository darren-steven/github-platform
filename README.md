# Azure DevOps Organization IaC (`AzDo-IaC`)

This repository manages Azure DevOps projects and organization settings. **Most maintainers only need to edit YAML files in `config/` and run the validation script.** You do not need to know OpenTofu to update a project.

## For project maintainers

### Change or onboard a project

1. Edit the existing project file in `config/projects/`, or follow the [project onboarding guide](./docs/onboarding-guide.md) to add one. The [example project](./config/projects/example-service.yaml) shows the available structure.
2. Keep changes within the documented settings and allowed bounds in the [dials and baselines catalog](./docs/dials-catalog.md).
3. Run the local checks:
   ```bash
   ./scripts/validate.sh
   ```
4. Open a pull request. CI validates the change and posts an OpenTofu plan for review before it is applied.

### Change organization settings

Organization-wide settings live in [`config/org.yaml`](./config/org.yaml); shared groups live in [`config/groups.yaml`](./config/groups.yaml). These changes can affect the whole organization, so check the [dials and baselines catalog](./docs/dials-catalog.md) and required approvals before changing them.

## Where to go

| If you need to… | Start here |
| --- | --- |
| Change a project, repository, team, or environment | [`config/projects/`](./config/projects/) |
| Change organization-wide settings or groups | [`config/org.yaml`](./config/org.yaml), [`config/groups.yaml`](./config/groups.yaml) |
| Check allowed settings and security limits | [Dials and baselines catalog](./docs/dials-catalog.md) |
| Understand the repo layout and pull request workflow | [Contributor and maintainer guide](./docs/onboarding-guide.md) |
| Set up OpenTofu access and PIM elevation | [OpenTofu access and Azure PIM](./docs/permissions-and-pim.md) |
| Manage bootstrap Entra groups and Azure DevOps association | [`config/identity-bootstrap.yaml`](./config/identity-bootstrap.yaml) |
| Change how the infrastructure engine works | [Platform engineering reference](./ARCHITECTURE.md) |

## Repository map

| Area | Who usually works here | Purpose |
| --- | --- | --- |
| [`config/`](./config/) | Maintainers | YAML settings for the organization, groups, and projects. This is the normal day-to-day edit surface. |
| [`docs/`](./docs/) | Everyone | How-to guides and the settings catalog. |
| [`scripts/`](./scripts/) | Usually platform engineers | Local validation and OpenTofu helper scripts. Maintainers normally run these rather than change them. |
| [`schemas/`](./schemas/), [`policies/`](./policies/) | Platform engineers | Define and enforce which configuration is allowed. |
| [`modules/`](./modules/), [`environments/`](./environments/) | Platform engineers | OpenTofu engine and organization deployment wiring. |
| [`.agents/`](./.agents/), [`.github/`](./.github/), [`AGENTS.md`](./AGENTS.md) | Platform engineers | AI assistant skills, repository automation, and contributor guardrails. |
| [`.devcontainer/`](./.devcontainer/) | Tooling | Development-container setup; not part of project configuration. |

## Platform engineering

Changes to the engine, policy enforcement, schemas, or deployment wiring require platform engineering knowledge and review. They are **not** needed for routine project onboarding or configuration. See the [architecture reference](./ARCHITECTURE.md) for the infrastructure data flow and implementation details.
