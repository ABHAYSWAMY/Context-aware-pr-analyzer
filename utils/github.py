import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def parse_pr_url(url: str):
    parts = url.strip("/").split("/")
    owner = parts[-4]
    repo = parts[-3]
    pr_number = parts[-1]
    return owner, repo, pr_number


def fetch_pr_files(pr_url: str):
    owner, repo, pr_number = parse_pr_url(pr_url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")

    return response.json()

def fetch_file_content(file_obj):
    """
    Uses GitHub-provided raw_url (best approach)
    """
    raw_url = file_obj.get("raw_url")

    if not raw_url:
        return ""

    response = requests.get(raw_url)

    if response.status_code != 200:
        return ""

    return response.text