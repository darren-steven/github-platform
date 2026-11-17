#!/usr/bin/env python3
"""Reconcile the Azure DevOps auto-created '<project_name>' default Git repository.

Modes:
  apply:
    - create_default_repository == false: Deletes the unmanaged '<project_name>'
      default repository (after explicit repositories have been created).
    - create_default_repository == true: Adopts the '<project_name>' repository
      in-place (or creates it if previously deleted) and initializes refs/heads/main
      with an initial README.md commit if empty.
  destroy:
    - create_default_repository == false: Restores an empty '<project_name>'
      placeholder repository before OpenTofu destroys explicit repositories so
      Azure DevOps does not reject deleting the last repository in the project
      (TF400948).
"""

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request


def build_headers(token: str) -> dict:
    if token.startswith("eyJ"):
        auth_hdr = f"Bearer {token}"
    else:
        encoded = base64.b64encode(f":{token}".encode("utf-8")).decode("utf-8")
        auth_hdr = f"Basic {encoded}"
    return {"Authorization": auth_hdr, "Content-Type": "application/json"}


def api_call(url: str, headers: dict, method: str = "GET", payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def handle_apply(org_url: str, project_id: str, project_name: str, create_default: bool, headers: dict) -> int:
    repos_url = f"{org_url}/{project_id}/_apis/git/repositories?api-version=7.1"
    repos = api_call(repos_url, headers).get("value", [])
    default_repo = next((r for r in repos if r.get("name") == project_name), None)

    if not create_default:
        if default_repo:
            del_url = f"{org_url}/{project_id}/_apis/git/repositories/{default_repo['id']}?api-version=7.1"
            api_call(del_url, headers, method="DELETE")
            print(f"Deleted unmanaged default repository '{project_name}' ({default_repo['id']})")
        return 0

    # create_default is True: Adopt existing repo in-place or create it if previously deleted
    if not default_repo:
        default_repo = api_call(
            repos_url,
            headers,
            method="POST",
            payload={"name": project_name, "project": {"id": project_id}},
        )
        print(f"Created default repository '{project_name}' ({default_repo['id']})")
        time.sleep(2)

    repo_id = default_repo["id"]
    refs_url = f"{org_url}/{project_id}/_apis/git/repositories/{repo_id}/refs?filter=heads/main&api-version=7.1"
    refs = api_call(refs_url, headers).get("value", [])

    if not refs:
        push_url = f"{org_url}/{project_id}/_apis/git/repositories/{repo_id}/pushes?api-version=7.1"
        push_payload = {
            "refUpdates": [
                {
                    "name": "refs/heads/main",
                    "oldObjectId": "0000000000000000000000000000000000000000",
                }
            ],
            "commits": [
                {
                    "comment": "Initial commit (Managed by AzDo-IaC)",
                    "changes": [
                        {
                            "changeType": "add",
                            "item": {"path": "/README.md"},
                            "newContent": {
                                "content": f"# {project_name}\n\nManaged by AzDo-IaC.\n",
                                "contentType": "rawtext",
                            },
                        }
                    ],
                }
            ],
        }
        for attempt in range(5):
            try:
                api_call(push_url, headers, method="POST", payload=push_payload)
                print(f"Initialized default repository '{project_name}' with refs/heads/main")
                break
            except urllib.error.HTTPError as e:
                if attempt < 4:
                    time.sleep(2)
                else:
                    err_body = e.read().decode("utf-8", errors="replace")
                    print(f"Failed initializing '{project_name}': HTTP {e.code} - {err_body}", file=sys.stderr)
                    return 1
    return 0


def handle_destroy(org_url: str, project_id: str, project_name: str, create_default: bool, headers: dict) -> int:
    if create_default:
        return 0

    repos_url = f"{org_url}/{project_id}/_apis/git/repositories?api-version=7.1"
    try:
        repos = api_call(repos_url, headers).get("value", [])
        default_repo = next((r for r in repos if r.get("name") == project_name), None)
        if not default_repo:
            created = api_call(
                repos_url,
                headers,
                method="POST",
                payload={"name": project_name, "project": {"id": project_id}},
            )
            print(
                f"Restored placeholder default repository '{project_name}' ({created.get('id')}) "
                "to allow clean deletion of explicit repositories"
            )
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 0
        err_body = e.read().decode("utf-8", errors="replace")
        print(
            f"Warning: could not restore placeholder repository '{project_name}': HTTP {e.code} - {err_body}",
            file=sys.stderr,
        )
    return 0


def main() -> int:
    if len(sys.argv) != 6:
        print(
            "Usage: reconcile_default_repo.py <apply|destroy> <org_url> <project_id> <project_name> <create_default>",
            file=sys.stderr,
        )
        return 1

    mode = sys.argv[1].lower()
    org_url = sys.argv[2].rstrip("/")
    project_id = sys.argv[3]
    project_name = sys.argv[4]
    create_default = sys.argv[5].lower() == "true"

    token = os.environ.get("AZDO_PERSONAL_ACCESS_TOKEN", "")
    if not token:
        return 0

    headers = build_headers(token)

    if mode == "apply":
        return handle_apply(org_url, project_id, project_name, create_default, headers)
    if mode == "destroy":
        return handle_destroy(org_url, project_id, project_name, create_default, headers)

    print(f"Unknown mode '{mode}' (expected 'apply' or 'destroy')", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
