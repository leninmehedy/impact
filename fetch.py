import os
import sys
from datetime import datetime, timezone
from github import Github, GithubException, Auth
from dotenv import load_dotenv

# Load .env
load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")
REPOS_ENV = os.getenv("REPOS")

if not TOKEN or not USERNAME:
    print("Please set GITHUB_TOKEN and GITHUB_USERNAME in .env")
    sys.exit(1)

if len(sys.argv) != 3:
    print("Usage: python fetch.py <start_date> <end_date>")
    print("Example: python fetch.py 2025-10-01 2025-11-15")
    sys.exit(1)

start_date, end_date = sys.argv[1], sys.argv[2]
start_dt = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
end_dt = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)

# Authenticate
g = Github(auth=Auth.Token(TOKEN))

def fetch_prs_from_repo(repo):
    try:
        prs = repo.get_pulls(state="all")
    except GithubException as e:
        print(f"Error fetching PRs from {repo.full_name}: {e.data if hasattr(e, 'data') else e}")
        return []

    filtered = []
    for pr in prs:
        pr_dt = pr.created_at.replace(tzinfo=timezone.utc)
        if start_dt <= pr_dt <= end_dt and pr.user.login == USERNAME:
            filtered.append(pr)
    return filtered

# Determine repos to scan
repos_to_scan = []

if REPOS_ENV:
    repo_names = [r.strip() for r in REPOS_ENV.split(",") if r.strip()]
    for full_name in repo_names:
        try:
            repo = g.get_repo(full_name)
            repos_to_scan.append(repo)
        except GithubException as e:
            print(f"Error fetching {full_name}: {e.data if hasattr(e, 'data') else e}")
else:
    print("No REPOS provided, scanning all accessible repos. This may be slow...")
    try:
        repos_to_scan = list(g.get_user().get_repos())
    except GithubException as e:
        print(f"Error fetching repositories: {e}")
        sys.exit(1)

# Fetch PRs
for repo in repos_to_scan:
    print(f"=== Fetching PRs for {repo.full_name} ===")
    prs = fetch_prs_from_repo(repo)
    if not prs:
        print("No PRs found in this date range or no access.\n")
        continue
    for pr in prs:
        print(f"- PR-{pr.number}: {pr.title} ({repo.full_name})\n  {pr.html_url}")
    print()

