# GitHub Onboarding & Governance Drift Report: `taswater`

## 1. Extraction Summary

- **Organization**: `taswater`
- **GitHub Teams Discovered**: `15`
- **Active Repositories Analyzed**: `151`
- **Archived Repositories Excluded**: `3`
- **Deduced Domain Files**: `24`

## 2. Deduced Domain Alignment (`repos/<domain>.yaml`)

| Domain File | Repo Count | Default Archetype | Primary Deduction Signal |
| :--- | :--- | :--- | :--- |
| `repos/api.yaml` | 5 | `standard-microservice` | repo name prefix (api-*) |
| `repos/bsa.yaml` | 2 | `shared-library` | team association (bsa-*) |
| `repos/customer-interaction.yaml` | 2 | `shared-library` | repo name prefix (customer-interaction-*) |
| `repos/dataandanalytics.yaml` | 1 | `standard-microservice` | team association (dataandanalytics-*) |
| `repos/dataops.yaml` | 3 | `shared-library` | repo name prefix (dataops-*) |
| `repos/digital-delivery.yaml` | 17 | `shared-library` | team association (digital-delivery-*) |
| `repos/finance.yaml` | 1 | `shared-library` | repo name prefix (finance-*) |
| `repos/fusion5.yaml` | 5 | `shared-library` | team association (fusion5-*) |
| `repos/general-services.yaml` | 62 | `shared-library` | fallback default |
| `repos/gentrack.yaml` | 16 | `standard-microservice` | team association (gentrack-*) |
| `repos/github.yaml` | 2 | `shared-library` | repo name prefix (github-*) |
| `repos/h2go.yaml` | 1 | `standard-microservice` | team association (h2go-*) |
| `repos/j4rvis.yaml` | 4 | `shared-library` | team association (j4rvis-*) |
| `repos/maximo.yaml` | 3 | `standard-microservice` | team association (maximo-*) |
| `repos/mule.yaml` | 2 | `standard-microservice` | repo name prefix (mule-*) |
| `repos/ogp.yaml` | 1 | `shared-library` | repo name prefix (ogp-*) |
| `repos/operations.yaml` | 2 | `shared-library` | team association (operations-*) |
| `repos/platform.yaml` | 2 | `shared-library` | repo name prefix (platform-*) |
| `repos/powershell.yaml` | 1 | `shared-library` | repository topic (powershell) |
| `repos/reporting.yaml` | 4 | `standard-microservice` | team association (reporting-*) |
| `repos/scada.yaml` | 1 | `shared-library` | team association (scada-*) |
| `repos/spatial-applications.yaml` | 6 | `standard-microservice` | team association (spatial-applications-*) |
| `repos/survey.yaml` | 2 | `shared-library` | repo name prefix (survey-*) |
| `repos/taswater-networks.yaml` | 6 | `shared-library` | team association (taswater-networks-*) |

## 3. Archived Repositories (Skipped by Default)

The following repositories are marked `archived: true` in GitHub and were excluded from active YAML governance:

- `FormsExpress`
- `SSIS_FormsExpress_FileMover`
- `api-work-orders-toapprove-v1`

## 4. Baseline Drift & Remediation Items

The items below show where live GitHub settings differed from Tier 1/Tier 2 baselines and were automatically normalized in the generated candidate YAML:

| Target | Remediation Category | Details |
| :--- | :--- | :--- |
| `team:bsa` | **Team Privacy Standardized** | Team 'bsa' privacy 'secret' standardized to 'closed'. |
| `team:gentrack` | **Team Privacy Standardized** | Team 'gentrack' privacy 'secret' standardized to 'closed'. |
| `team:maximo` | **Team Privacy Standardized** | Team 'maximo' privacy 'secret' standardized to 'closed'. |
| `team:operations-team` | **Team Privacy Standardized** | Team 'operations-team' privacy 'secret' standardized to 'closed'. |
| `team:reporting` | **Team Privacy Standardized** | Team 'reporting' privacy 'secret' standardized to 'closed'. |
| `team:scada` | **Team Privacy Standardized** | Team 'scada' privacy 'secret' standardized to 'closed'. |
| `team:sql` | **Team Privacy Standardized** | Team 'sql' privacy 'secret' standardized to 'closed'. |
| `api-employee-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `api-payway-proxy` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `api-people-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `api-service-desk-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `api-sewerage-pricing-estimator-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `api-employee-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-payway-proxy` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-payway-proxy` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-people-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-people-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-service-desk-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-sewerage-pricing-estimator-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-sewerage-pricing-estimator-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Excel` | **Team Admin Permission Downgraded** | Team 'bsa' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `sdautomator` | **Team Admin Permission Downgraded** | Team 'bsa' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `sdautomator` | **Team Admin Permission Downgraded** | Team 'operations-team' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `Excel` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Excel` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `sdautomator` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `customer-interaction-eapi-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `customer-interaction-papi-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `customer-interaction-eapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `customer-interaction-eapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `customer-interaction-papi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `customer-interaction-papi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `reporting` | **Team Admin Permission Downgraded** | Team 'dataandanalytics' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `reporting` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `reporting` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `dataops-fme` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `dataops-fme-test` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `dataops-general` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `dataops-fme` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `dataops-fme` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `dataops-fme-test` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `dataops-fme-test` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `dataops-general` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `dataops-general` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `azure-templates` | **Team Admin Permission Downgraded** | Team 'operations-team' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `api-address-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-address-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-banking-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-banking-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-gentrack-customer-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-gentrack-customer-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-inventory-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-inventory-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-keep-alive-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-keep-alive-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-locations-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-locations-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-logging-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-logging-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-procurement-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-procurement-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-reference-data-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-reference-data-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-sessions-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-sessions-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-something-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-something-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `api-template-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-template-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `api-work-orders-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `api-work-orders-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `azure-templates` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `cloudhub-app-bulk-update` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `common-lib` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `common-lib` | **Branch Protection Upgraded** | Default branch had protected=True, min_reviewers=1; candidate applies 'shared-library' floor (min_reviewers=2). |
| `jenkins-seed` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `jenkins-seed` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `finance-mx-sapi-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `finance-mx-sapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `finance-mx-sapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `account-bc-sapi-v1` | **Team Admin Permission Downgraded** | Team 'fusion5' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `account-mgmt-eapi-v1` | **Team Admin Permission Downgraded** | Team 'fusion5' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `finance-bc-sapi-v1` | **Team Admin Permission Downgraded** | Team 'fusion5' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `finance-db-sapi-v1` | **Team Admin Permission Downgraded** | Team 'fusion5' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `finance-integ-papi-v1` | **Team Admin Permission Downgraded** | Team 'fusion5' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `account-bc-sapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `account-bc-sapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `account-mgmt-eapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `account-mgmt-eapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `finance-bc-sapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `finance-bc-sapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `finance-db-sapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `finance-db-sapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `finance-integ-papi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `finance-integ-papi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `.github` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `761_anywhere_development` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `762_anywhere_development` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Anywhere761full` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `automation` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `azdo-iac` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `AzureNamingTool` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `BC-SSIS-Pipeline` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `BI-DataFlow` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `BI_RealisedRevenue` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `BillFileReconciliation` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `calc_IP_address_ranges` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `centrelink_concession_bulk_verification` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `CIO-Pulse` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `config` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Contacts-api` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `coo-prep-v3` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `cordova-plugin-inappbrowser` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `cornerstone-chris21-integration-report-syncer` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Cornerstone_Chris21_Integration` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `cszbarIOS11` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `DBA_Tools` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `digital-portal-eapi-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `DougsQuickReference` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `fme` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `fme-test` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `GentrackReportingDB_andGTtoGIS` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `GetFileFromHpeTrim` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `InstallationDataQuality` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `JmeterApiTests` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `JSEA-Python-HTML-Data-Extraction` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Maximo` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `mule_sandbox_email_imap` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Network-IndustrialSwitches` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Office365Scripts` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `OutSystems---H2GO` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `PRTG_Scripts` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `PS_SPtoSQL` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `PSP2-TradeWasteCalculator` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `PSP3-TradeWasteCalculator` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `PythonDataTesting` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `QPC` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Rancid-Clogin-Scripts` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `RancidAutomationScripts` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Selenium` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SELinux` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `spatial` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `sql-dba` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `ssis-gentrack-banking` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SSIS_Centrelink_ImportResponses` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SSIS_GTV_AgedDebtors_DW` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SSIS_Metadata_extractor` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `ssis_VisTas_COO_V3` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SSRS---Apps-Admin` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SSRS_Gentrack` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SSRS_Gentrack_Pricing` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `TW-Python-DATABASE` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `YARA-Rules` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `.github` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `.github` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `761_anywhere_development` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `761_anywhere_development` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `762_anywhere_development` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `762_anywhere_development` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `anypoint-wrapper-cli` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `Anywhere761full` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Anywhere761full` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `automation` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `automation` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `azdo-iac` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `AzureNamingTool` | **Public Visibility Blocked (Tier 1)** | Repository is currently 'public'; set to 'private' in candidate YAML. |
| `AzureNamingTool` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `BC-SSIS-Pipeline` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `BI-DataFlow` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `BI-DataFlow` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `BI_RealisedRevenue` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `BI_RealisedRevenue` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `BillFileReconciliation` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `BillFileReconciliation` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `calc_IP_address_ranges` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `centrelink_concession_bulk_verification` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `centrelink_concession_bulk_verification` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `CIO-Pulse` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `CIO-Pulse` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `config` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `config` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Contacts-api` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Contacts-api` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `coo-prep-v3` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `coo-prep-v3` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `cordova-plugin-inappbrowser` | **Public Visibility Blocked (Tier 1)** | Repository is currently 'public'; set to 'private' in candidate YAML. |
| `cordova-plugin-inappbrowser` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `cordova-plugin-inappbrowser` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `cornerstone-chris21-integration-report-syncer` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `Cornerstone_Chris21_Integration` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Cornerstone_Chris21_Integration` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `cszbarIOS11` | **Public Visibility Blocked (Tier 1)** | Repository is currently 'public'; set to 'private' in candidate YAML. |
| `cszbarIOS11` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `cszbarIOS11` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `DBA_Tools` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `DBA_Tools` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `digital-portal-eapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `digital-portal-eapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `DougsQuickReference` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `DougsQuickReference` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `fme` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `fme` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `fme-test` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `fme-test` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `GentrackReportingDB_andGTtoGIS` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `GentrackReportingDB_andGTtoGIS` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `GetFileFromHpeTrim` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `GetFileFromHpeTrim` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `InstallationDataQuality` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `InstallationDataQuality` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `JmeterApiTests` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `JmeterApiTests` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `JSEA-Python-HTML-Data-Extraction` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Maximo` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Maximo` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `mule_sandbox_email_imap` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `mule_sandbox_email_imap` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'sandbox' floor (min_reviewers=2). |
| `Network-IndustrialSwitches` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Office365Scripts` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Office365Scripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `OutSystems---H2GO` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `OutSystems---H2GO` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `pi_mulesoft_transforms` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `pi_mulesoft_transforms` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `PRTG_Scripts` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `PRTG_Scripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `PS_SPtoSQL` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `PSP2-TradeWasteCalculator` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `PSP2-TradeWasteCalculator` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `PSP3-TradeWasteCalculator` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `PSP3-TradeWasteCalculator` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `PythonDataTesting` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `PythonDataTesting` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `QPC` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Rancid-Clogin-Scripts` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Rancid-Clogin-Scripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `RancidAutomationScripts` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `RancidAutomationScripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `sandbox-objects-scheduler` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `sandbox-objects-scheduler` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'sandbox' floor (min_reviewers=2). |
| `Selenium` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `SELinux` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SELinux` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `spatial` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `spatial` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `sql-dba` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `sql-dba` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `ssis-gentrack-banking` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `ssis-gentrack-banking` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSIS_Centrelink_ImportResponses` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSIS_Centrelink_ImportResponses` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSIS_Chris21_ETL` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSIS_Chris21_ETL` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSIS_GTV_AgedDebtors_DW` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSIS_GTV_AgedDebtors_DW` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSIS_Metadata_extractor` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `ssis_VisTas_COO_V3` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `ssis_VisTas_COO_V3` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `SSRS---Apps-Admin` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSRS---Apps-Admin` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSRS_Gentrack` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSRS_Gentrack` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSRS_Gentrack_Pricing` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `TW-Python-DATABASE` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `TW-Python-DATABASE` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `YARA-Rules` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Gentrack-ABCorp-Integration` | **Team Admin Permission Downgraded** | Team 'gentrack' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `Gentrack-Pricing-Snapshot-system---DW` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Gentrack-RFGateways-Integration` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `gentrack-sapi-v1` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `SSRS_GT_IntegrityCheck` | **Team Admin Permission Downgraded** | Team 'gentrack' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `ARG1903_Equalisation` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `ARG1903_Equalisation` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `BillFileRecognition` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `BillFileRecognition` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `CentrePay_Receipt_ETL` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `CentrePay_Receipt_ETL` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `Gentrack-ABCorp-Integration` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Gentrack-ABCorp-Integration` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Gentrack-Pricing-Snapshot-system---DW` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Gentrack-RFGateways-Integration` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Gentrack-RFGateways-Integration` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `gentrack-sapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `gentrack-sapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Gentrack-SSIS` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Gentrack-SSIS` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `OGP-DatabaseMigration` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `PSP3` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `PSP3` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `SSIS_CreditCycles` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSIS_CreditCycles` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `SSIS_GTLetterImport` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSIS_GTLetterImport` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSIS_VisTas` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSIS_VisTas` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SSRS_GT_IntegrityCheck` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSRS_GT_IntegrityCheck` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `WestPac_FileSplitter_Reports` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `WestPac_FileSplitter_Reports` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `Westpac_FileSplitters` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Westpac_FileSplitters` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `github-copilot-iac-example` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `github-security-audit` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `github-copilot-iac-example` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `github-copilot-iac-example` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `github-security-audit` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `github-security-audit` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `mulesoft` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `mulesoft` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `AnyPoint` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `AnyPoint` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `customer-ebilling-eapi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `customer-ebilling-eapi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `ebilling-papi-v1` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `ebilling-papi-v1` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `taswater-error-handling-util` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `taswater-error-handling-util` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `anywhere_development` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `anywhere_development` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `turbine_deployment` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `turbine_deployment` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `turbine_development` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `turbine_development` | **Branch Protection Upgraded** | Default branch had protected=True, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `mule-nonprod-config` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `mule-nonprod-config` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `mule-prod-config` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `mule-prod-config` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `OGP-IntegrationAndReporting` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `OGP-IntegrationAndReporting` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `OGP-IntegrationAndReporting` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `SCOM-ManagementPacks` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SCOM-ManagementPacks` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `TasWater-Scripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `platform-azuredevops` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `platform-github` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `platform-azuredevops` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `platform-github` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `PI-TaKaDu-Integration` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `PI-TaKaDu-Integration` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `PI-TaKaDu-Integration` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `BI_IRIS_IncidentsHazards` | **Team Admin Permission Downgraded** | Team 'reporting' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `ExtractExchangeAttachment` | **Team Admin Permission Downgraded** | Team 'reporting' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `Scripts_BureauOfMetereology` | **Team Admin Permission Downgraded** | Team 'reporting' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `SSIS_BureauOfMetereology` | **Team Admin Permission Downgraded** | Team 'reporting' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `BI_IRIS_IncidentsHazards` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `BI_IRIS_IncidentsHazards` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `ExtractExchangeAttachment` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `ExtractExchangeAttachment` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `Scripts_BureauOfMetereology` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Scripts_BureauOfMetereology` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `SSIS_BureauOfMetereology` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `SSIS_BureauOfMetereology` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `test` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `test` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `GIS_Scripts` | **Team Admin Permission Downgraded** | Team 'spatial-applications' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `spatial_batch_processing_scripts` | **Team Admin Permission Downgraded** | Team 'spatial-applications' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `spatial_geocortex_config` | **Team Admin Permission Downgraded** | Team 'spatial-applications' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `TW-809-PythonTools` | **Team Admin Permission Downgraded** | Team 'taswater-networks' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `GIS_Scripts` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `GIS_Scripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `spatial_arcgis_desktop_aim_tools` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `spatial_arcgis_desktop_aim_tools` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `spatial_arcgis_server_service_config` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `spatial_arcgis_server_service_config` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `spatial_batch_processing_scripts` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `spatial_batch_processing_scripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `spatial_geocortex_config` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `spatial_geocortex_config` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `TW-809-PythonTools` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `TW-809-PythonTools` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Survey-ASDS_CADtoGIS_Translator` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Survey-ASDS_V2_Support_Files` | **Missing Team Access Assigned** | Repository had no team permissions; assigned fallback team 'bsa' (maintain). |
| `Survey-ASDS_CADtoGIS_Translator` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Survey-ASDS_CADtoGIS_Translator` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Survey-ASDS_V2_Support_Files` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `CiscoWhisper-SSH` | **Team Admin Permission Downgraded** | Team 'taswater-networks' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `Dougs809` | **Team Admin Permission Downgraded** | Team 'taswater-networks' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `RouterScripts` | **Team Admin Permission Downgraded** | Team 'taswater-networks' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `TW-NetworkTeam` | **Team Admin Permission Downgraded** | Team 'taswater-networks' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `TW-Router-Configurations` | **Team Admin Permission Downgraded** | Team 'taswater-networks' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `TW-Switch-Configurations` | **Team Admin Permission Downgraded** | Team 'taswater-networks' had 'admin' permission; converted to 'maintain' to enforce Tier 1 no-repo-admin baseline. |
| `CiscoWhisper-SSH` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `CiscoWhisper-SSH` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `Dougs809` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `Dougs809` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `RouterScripts` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `RouterScripts` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'standard-microservice' floor (min_reviewers=2). |
| `TW-NetworkTeam` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `TW-NetworkTeam` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `TW-Router-Configurations` | **Non-Standard Default Branch** | Default branch is currently 'master'; target baseline enforces 'main'. |
| `TW-Router-Configurations` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
| `TW-Switch-Configurations` | **Branch Protection Upgraded** | Default branch had protected=False, min_reviewers=0; candidate applies 'shared-library' floor (min_reviewers=2). |
