import os
import requests

def restart_service(service: str):
    print(f"[HANDLER] Restarting service: {service}")

def scale_service(service: str, replicas: int):
    print(f"[HANDLER] Scaling service: {service} to {replicas} replicas")

def ignore_alert(alert_id: str):
    print(f"[HANDLER] Ignoring alert: {alert_id}")

def print_message(message: str):
    print(f"[HANDLER] {message}")


def create_pull_request(repo: str, owner: str, branch: str, title: str, base:str="main", body: str = ""):
    """
    Creates a Pull Request on GitHub.
    
    Args:
        repo: 'owner/repo' format
        branch: source branch for the PR
        title: PR title
        body: PR description (optional)
    """
    token = os.environ.get("GITHUB_TOKEN")  # GitHub Personal Access Token
    if not token:
        print("[ERROR] GITHUB_TOKEN not set")
        return

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {token}"}
    payload = {
        "title": title,
        "head": branch,  # branch with changes
        "base": base,  # target branch
        "body": body
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        pr_url = response.json().get("html_url")
        print(f"[HANDLER] Pull Request created successfully: {pr_url}")
    else:
        print(f"[ERROR] Failed to create PR: {response.status_code} {response.text}")