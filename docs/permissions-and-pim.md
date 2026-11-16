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

## Manage the groups with identity bootstrap

The separate `identity-bootstrap` environment creates the Entra groups, links
them to Azure DevOps, grants the plan group collection-level view and project
Readers permissions, and creates PIM-eligible memberships for the apply group.
Configure [`identity-bootstrap.yaml`](../config/identity-bootstrap.yaml):

1. Add Entra user **object IDs** to `apply_group.eligible_member_object_ids`.
   These create permanent *eligibility* schedules, not standing group
   membership. Leave the list empty until approved operators are identified.
2. Add the plan users' Entra object IDs to `plan_group.member_object_ids` to
   give them standing membership in the read-only group.
3. Set `plan_project_names` to the names of existing projects that require
   OpenTofu plan access. The module adds the plan group to each project's
   built-in **Readers** group. Leave the list empty if the organization has no
   projects yet.
4. Optionally set `plan_group.owner_object_ids` to the approved owners'
   object IDs. The apply group is intentionally created without owners or
   direct members; manage its eligibility through PIM and this configuration,
   not by adding permanent members in Entra.

The apply group is linked to Azure DevOps **Project Collection
Administrators**. That is intentionally broad because `prod-org` manages
organization settings and resources across projects. The identity bootstrap
must be run by an operator with both the required Entra directory permissions
(Group Administrator/User Administrator for group creation and Privileged Role
Administrator for PIM eligibility management, or Global Administrator) and
Azure DevOps Project Collection Administrator access. Azure subscription
Owner or Contributor roles alone do not grant either permission.

PIM activation policy settings—such as MFA, justification, approval, and
maximum activation duration—are not configured by this Terraform module.
Configure and review those in Entra PIM for Groups according to organizational
policy. The module manages the group and its eligible member schedules.

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

### Run the identity bootstrap

The bootstrap uses a distinct OpenTofu root and state. Configure a dedicated,
protected backend in
[`environments/identity-bootstrap/versions.tf`](../environments/identity-bootstrap/versions.tf)
before using this beyond initial local testing; never reuse the `prod-org`
state key. Then sign in as an authorized Entra and Azure DevOps administrator
and run:

```bash
az login --tenant <tenant-id>
./scripts/tofu-local.sh --environment identity-bootstrap init
./scripts/tofu-local.sh --environment identity-bootstrap plan -out=tfplan
./scripts/tofu-local.sh --environment identity-bootstrap apply tfplan
```

Review the plan carefully: it associates the apply group with the collection
administrator group. This bootstrap path is intentionally not run by the
routine pull-request workflow. Once applied, configure the apply group's PIM
activation policy and verify the eligible users can activate and obtain the
expected Azure DevOps access. Remove the saved plan afterward:

```bash
rm environments/identity-bootstrap/tfplan
```

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
  organization settings or agent pools. The bootstrap grants collection-level
  **View instance-level information**; verify that your organization also
  permits reading its agent pools and other organization-scoped resources.
- The bootstrap grants project Readers access only to the project names listed
  in `plan_project_names`. Organization-level view permissions may still need a
  separate approved assignment.
- An OpenTofu plan is not a guaranteed read-only preview in every workflow:
  use only `plan` with the plan group. Do not use `apply`, `destroy`, or
  state-mutating commands without the separately authorized operational
  process.
- Review the plan before applying. PIM limits when the elevated group membership
  is active; it does not replace code review, change approval, or state
  protection.
