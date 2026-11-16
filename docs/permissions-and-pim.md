# OpenTofu access and Azure PIM

OpenTofu access is granted in **Azure DevOps**, not through an Azure subscription
RBAC role. The local runner obtains a short-lived Azure DevOps access token from
the signed-in Entra ID account; the account must also be a member of the Azure
DevOps organization and have an access level that permits the required actions.

Use separate access paths for routine planning and privileged applies:

| Access path | Assignment | Purpose |
| --- | --- | --- |
| **Plan (standing)** | A read-only Entra security group added to the Azure DevOps organization, with **Readers** access to every managed project and the necessary organization-level view permissions. | Lets `tofu plan` refresh existing state and read the resources it manages without granting change permissions. |
| **Apply (eligible via PIM)** | An Entra security group linked to the Azure DevOps **Project Collection Administrators** group, with eligible membership managed by PIM for Groups. | Provides temporary rights to create and update organization settings, groups, agent pools, projects, teams, repositories, policies, environments, and variable groups. |

The apply assignment is deliberately broad: this configuration manages both
organization-wide resources and resources across projects. Keep it eligible,
not permanently active. If the organization has a tested custom permission set
that supports all these operations, it can replace Project Collection
Administrators; validate it against a complete plan and apply before relying on
it.

## Configure the Entra groups and PIM

An Entra administrator should configure the following:

1. Create an Entra security group for plan readers and another for apply
   operators. Use organization-approved names, for example
   `AzDO IaC Plan Readers` and `AzDO IaC Apply Operators`.
2. Add the plan group to the Azure DevOps organization. Grant it **Readers**
   access in each project managed by this repository. Grant only the
   organization-level **view/read** permissions needed to inspect organization
   settings, groups, and agent pools. Do not grant edit or administration rights
   to this group.
3. Add the apply group to the Azure DevOps **Project Collection
   Administrators** group. In Entra Privileged Identity Management (PIM) for
   Groups, configure users as **eligible** members of the apply group rather
   than permanently active members.
4. Apply the organization's PIM activation controls to the apply group. At a
   minimum, require MFA and a justification; use approval, activation duration,
   notifications, and access reviews according to organizational policy.
5. Confirm the Azure DevOps organization recognizes the group membership and
   that each operator has an appropriate Azure DevOps access level. Azure
   subscription Owner or Contributor roles alone do not grant Azure DevOps
   permissions.

Azure DevOps and Entra group membership changes can take time to propagate.
After activating PIM, refresh the Azure CLI sign-in if permissions are not
recognized. The first plan with a new read-only role is an important check:
OpenTofu must be able to read every managed object, and the exact view
permissions required can depend on the organization's existing resources.
Resolve access-denied errors by granting the missing **view** permission to the
plan group, not by making the plan role an administrator.

## Run a plan or apply locally

Prerequisites: Azure CLI, OpenTofu, repository dependencies, and access to the
Azure DevOps organization.

### Plan with standing read-only access

```bash
az login --tenant <tenant-id>
./scripts/tofu-local.sh plan
```

The script runs repository validation and then runs OpenTofu in
`environments/prod-org`. Planning does not need PIM apply activation when the
standing plan permissions are configured correctly.

### Apply with PIM elevation

1. Sign in and create a saved plan using the standing plan permissions:

   ```bash
   az login --tenant <tenant-id>
   ./scripts/tofu-local.sh plan -out=tfplan
   ```

2. Review the saved plan. Then activate eligible membership in the apply group
   in PIM and complete the required approval/MFA steps.
3. Refresh the Azure CLI sign-in so the Azure DevOps token reflects the active
   group membership, and apply the reviewed plan while the PIM activation is
   still active:

   ```bash
   az login --tenant <tenant-id>
   ./scripts/tofu-local.sh apply tfplan
   ```

   Treat `tfplan` as sensitive: do not commit it, publish it, or share it
   outside the approved review process. After the apply, remove the saved plan:

   ```bash
   rm environments/prod-org/tfplan
   ```

4. Deactivate the PIM membership when the privileged work is complete.

The repository's pull-request workflow runs validation and can run a plan using
its separately configured CI credential. A user's PIM activation does not
grant permissions to the workflow; CI credentials and permissions must be
managed separately.

## Scope and limitations

- The plan group must have read access to all existing managed resources,
  including organization-level resources; project Readers alone may not cover
  organization settings or agent pools.
- An OpenTofu plan is not a guaranteed read-only preview in every workflow:
  use only `plan` with the plan group. Do not use `apply`, `destroy`, or
  state-mutating commands without the separately authorized operational
  process.
- Review the plan before applying. PIM limits when the elevated group membership
  is active; it does not replace code review, change approval, or state
  protection.
