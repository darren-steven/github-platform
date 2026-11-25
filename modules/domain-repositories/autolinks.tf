# -----------------------------------------------------------------------------
# Source: repositories[*].jira_autolink + enterprise_defaults.jira_autolink.
# -----------------------------------------------------------------------------
resource "github_repository_autolink_reference" "jira" {
  for_each = {
    for name, repo in var.repositories : name => repo
    if repo.jira_autolink != null
  }

  repository = github_repository.this[each.key].name
  key_prefix = "${each.value.jira_autolink.project_key}-"
  target_url_template = format(
    "%s/%s-<num>",
    trimsuffix(each.value.jira_autolink.browse_url, "/"),
    each.value.jira_autolink.project_key
  )
  is_alphanumeric = false
}
