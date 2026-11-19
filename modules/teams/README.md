# Module: `teams`

Manages centralized GitHub Teams, parent/child team nesting, and optional explicit team memberships defined in `config/orgs/<org>/teams.yaml`.

## How Two-Pass Nesting Works

In OpenTofu/Terraform, a single `for_each` resource cannot reference itself for `parent_team_id`. To support parent/child hierarchies (such as `j4rvis` → `digital-delivery` in `taswater`), this module creates teams in two ordered passes:
1. **`github_team.root`**: Top-level teams (`parent_team == null`).
2. **`github_team.child`**: Nested teams referencing `github_team.root[each.value.parent_team].id`.

Both maps are merged and exposed as unified outputs (`team_ids_by_slug` and `team_slugs`) for `modules/domain-repositories`.

## Resources Managed

| Resource | YAML Source | Notes |
| :--- | :--- | :--- |
| `github_team.root` | `teams.yaml` → `teams[*]` (no `parent_team`) | Enforces `privacy = "closed"`. |
| `github_team.child` | `teams.yaml` → `teams[*]` (with `parent_team`) | Enforces `privacy = "closed"`. |
| `github_team_membership.this` | `teams.yaml` → `maintainers`, `members` | Only created when explicit usernames are listed (IdP-synced teams leave these empty). |

## Inputs & Outputs

- **Inputs**: `teams` (normalized map keyed by slug from `modules/config-resolver`).
- **Outputs**: `team_ids_by_slug` (map of `slug -> numeric/string team ID`), `team_slugs` (map of `slug -> GitHub slug`).
