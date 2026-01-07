import requests
import pandas as pd
import time

# =========================
# CONFIG (CHANGE ONLY THESE)
# =========================

TOKEN = ""
OWNER = "fastapi"
REPO = "fastapi"

# =========================

HEADERS = {
    "Authorization": f"token {TOKEN}"
}

BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"

def get_all_pages(url, max_pages=2):
    results = []
    for page in range(1, max_pages + 1):
        r = requests.get(url + f"&page={page}", headers=HEADERS)
        data = r.json()
        if not data or "message" in data:
            break
        results.extend(data)
        time.sleep(0.6)
    return results


# =========================
# CONTRIBUTORS
# =========================

print("Fetching contributors...")
contributors = get_all_pages(BASE + "/contributors?per_page=100", max_pages=2)
pd.json_normalize(contributors).to_csv("contributors.csv", index=False)


# =========================
# COMMITS
# =========================

print("Fetching commits...")
commits = get_all_pages(BASE + "/commits?per_page=100", max_pages=2)

commit_rows = []

for c in commits[:120]:
    if c.get("author"):
        sha = c["sha"]
        detail = requests.get(BASE + "/commits/" + sha, headers=HEADERS).json()

        files = detail.get("files", [])
        core_files = [f["filename"] for f in files if "core" in f["filename"].lower()]

        commit_rows.append({
            "user": c["author"]["login"],
            "sha": sha,
            "files_changed": len(files),
            "core_files": len(core_files),
            "additions": detail.get("stats", {}).get("additions", 0),
            "deletions": detail.get("stats", {}).get("deletions", 0),
            "total_changes": detail.get("stats", {}).get("total", 0)
        })

        time.sleep(0.6)

pd.DataFrame(commit_rows).to_csv("commits.csv", index=False)


# =========================
# PULL REQUESTS + REVIEWS
# =========================

print("Fetching pull requests...")
prs = get_all_pages(BASE + "/pulls?state=all&per_page=100", max_pages=2)

pr_rows = []
review_rows = []

for pr in prs[:80]:
    pr_rows.append({
        "number": pr.get("number"),
        "user": pr.get("user", {}).get("login"),
        "merged": pr.get("merged_at") is not None,
        "comments": pr.get("comments", 0),
        "title": pr.get("title", ""),
        "created_at": pr.get("created_at"),
        "merged_at": pr.get("merged_at")
    })

    reviews = requests.get(
        BASE + f"/pulls/{pr.get('number')}/reviews",
        headers=HEADERS
    ).json()

    if isinstance(reviews, list):
        for r in reviews:
            review_rows.append({
                "pr_number": pr.get("number"),
                "reviewer": r.get("user", {}).get("login"),
                "state": r.get("state")
            })

    time.sleep(0.6)

pd.DataFrame(pr_rows).to_csv("pull_requests.csv", index=False)
pd.DataFrame(review_rows).to_csv("reviews.csv", index=False)


# =========================
# ISSUES
# =========================

print("Fetching issues...")
issues = get_all_pages(BASE + "/issues?state=all&per_page=100", max_pages=2)

issue_rows = []

for i in issues:
    if "pull_request" not in i:
        issue_rows.append({
            "user": i.get("user", {}).get("login"),
            "closed": i.get("closed_at") is not None,
            "comments": i.get("comments", 0),
            "title": i.get("title", ""),
            "created_at": i.get("created_at"),
            "closed_at": i.get("closed_at")
        })

pd.DataFrame(issue_rows).to_csv("issues.csv", index=False)


# =========================
print("\nDONE ✅")
print("Files created:")
print("contributors.csv")
print("commits.csv")
print("pull_requests.csv")
print("reviews.csv")
print("issues.csv")
