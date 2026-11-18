# GitHub Onboarding & Governance Drift Report: `TasWater`

## 1. Extraction Summary

- **Organization**: `TasWater`
- **GitHub Teams Discovered**: `1`
- **Active Repositories Analyzed**: `5`
- **Archived Repositories Excluded**: `0`
- **Deduced Domain Files**: `1`

## 2. Deduced Domain Alignment (`repos/<domain>.yaml`)

| Domain File | Repo Count | Default Archetype | Primary Deduction Signal |
| :--- | :--- | :--- | :--- |
| `repos/general-services.yaml` | 5 | `standard-microservice` | fallback default |

## 4. Baseline Drift & Remediation Items

The items below show where live GitHub settings differed from Tier 1/Tier 2 baselines and were automatically normalized in the generated candidate YAML:

| Target | Remediation Category | Details |
| :--- | :--- | :--- |
| `AzureNamingTool` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'TasWater-maintainers' (maintain). |
| `azdo-iac` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'TasWater-maintainers' (maintain). |
| `cordova-plugin-inappbrowser` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'TasWater-maintainers' (maintain). |
| `cszbarIOS11` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'TasWater-maintainers' (maintain). |
| `platform-github` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'TasWater-maintainers' (maintain). |
| `AzureNamingTool` | **Public Visibility Blocked (Tier 1)** | Repository is currently 'public'; set to 'private' in candidate YAML. |
| `AzureNamingTool` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `azdo-iac` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `cordova-plugin-inappbrowser` | **Public Visibility Blocked (Tier 1)** | Repository is currently 'public'; set to 'private' in candidate YAML. |
| `cordova-plugin-inappbrowser` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `cordova-plugin-inappbrowser` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `cszbarIOS11` | **Public Visibility Blocked (Tier 1)** | Repository is currently 'public'; set to 'private' in candidate YAML. |
| `cszbarIOS11` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `cszbarIOS11` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `platform-github` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
