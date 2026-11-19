# =============================================================================
# Module: teams — Two-Pass GitHub Team Hierarchy & Memberships
# =============================================================================
# Source: config/orgs/<org>/teams.yaml
# =============================================================================

locals {
  root_teams  = { for slug, team in var.teams : slug => team if try(team.parent_team, null) == null }
  child_teams = { for slug, team in var.teams : slug => team if try(team.parent_team, null) != null }

  # Flatten explicit maintainer & member assignments (when not solely IdP-synced)
  explicit_memberships = merge(
    {
      for item in flatten([
        for slug, team in var.teams : [
          for username in try(team.maintainers, []) : {
            key      = "${slug}:${username}"
            slug     = slug
            username = username
            role     = "maintainer"
          }
        ]
      ]) : item.key => item
    },
    {
      for item in flatten([
        for slug, team in var.teams : [
          for username in try(team.members, []) : {
            key      = "${slug}:${username}"
            slug     = slug
            username = username
            role     = "member"
          }
        ]
      ]) : item.key => item
    }
  )
}

# -----------------------------------------------------------------------------
# Pass 1: Root GitHub Teams (no parent_team)
# -----------------------------------------------------------------------------
resource "github_team" "root" {
  for_each = local.root_teams

  name        = each.value.name
  description = each.value.description
  privacy     = "closed"
}

# -----------------------------------------------------------------------------
# Pass 2: Child GitHub Teams (nested under a root team)
# -----------------------------------------------------------------------------
resource "github_team" "child" {
  for_each = local.child_teams

  name           = each.value.name
  description    = each.value.description
  privacy        = "closed"
  parent_team_id = github_team.root[each.value.parent_team].id
}

locals {
  all_teams = merge(github_team.root, github_team.child)
}

# -----------------------------------------------------------------------------
# Optional Explicit Team Memberships (prefer Entra ID IdP sync where available)
# -----------------------------------------------------------------------------
resource "github_team_membership" "this" {
  for_each = local.explicit_memberships

  team_id  = local.all_teams[each.value.slug].id
  username = each.value.username
  role     = each.value.role
}
