import json
import uuid

# ---------------- SAFE LOAD ----------------

def load_json_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content == "":
                return {}
            return json.loads(content)
    except:
        return {}

def safe_get(d, keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return default
    return d


# ---------------- LOAD FILES ----------------

commits_raw = load_json_safe("commits.json")
issues_raw = load_json_safe("issues.json")
prs_raw = load_json_safe("prs.json")
reviews_raw = load_json_safe("reviews.json")
transcript_raw = load_json_safe("transcript.json")

normalized_events = []


# ==================================================
# COMMITS  (history → nodes)  ✅ FIXED
# ==================================================

commit_nodes = safe_get(
    commits_raw,
    ["data", "repository", "defaultBranchRef", "target", "history", "nodes"],
    []
)

for node in commit_nodes:
    author = safe_get(node, ["author", "user", "login"], "unknown")

    normalized_events.append({
        "event_id": str(uuid.uuid4()),
        "actor": author,
        "event_type": "commit",
        "text": node.get("messageHeadline", ""),
        "timestamp": node.get("committedDate", ""),
        "related": {
            "commit": None,
            "pr": None,
            "issue": None
        },
        "metadata": {
            "additions": node.get("additions", 0),
            "deletions": node.get("deletions", 0),
            "files_changed": node.get("changedFiles", 0)
        }
    })


# ==================================================
# ISSUES
# ==================================================

issue_nodes = safe_get(
    issues_raw,
    ["data", "repository", "issues", "nodes"],
    []
)

for issue in issue_nodes:
    normalized_events.append({
        "event_id": str(uuid.uuid4()),
        "actor": safe_get(issue, ["author", "login"], "unknown"),
        "event_type": "issue",
        "text": issue.get("title", ""),
        "timestamp": issue.get("createdAt", ""),
        "related": {
            "commit": None,
            "pr": None,
            "issue": issue.get("number")
        },
        "metadata": {
            "labels": [l["name"] for l in safe_get(issue, ["labels", "nodes"], [])],
            "state": "closed" if issue.get("closedAt") else "open",
            "comments": safe_get(issue, ["comments", "totalCount"], 0)
        }
    })


# ==================================================
# PULL REQUESTS
# ==================================================

pr_nodes = safe_get(
    prs_raw,
    ["data", "repository", "pullRequests", "nodes"],
    []
)

for pr in pr_nodes:
    normalized_events.append({
        "event_id": str(uuid.uuid4()),
        "actor": safe_get(pr, ["author", "login"], "unknown"),
        "event_type": "pr",
        "text": pr.get("title", ""),
        "timestamp": pr.get("createdAt", ""),
        "related": {
            "commit": None,
            "pr": pr.get("number"),
            "issue": None
        },
        "metadata": {
            "merged": True if pr.get("mergedAt") else False,
            "state": pr.get("state")
        }
    })


# ==================================================
# REVIEWS
# ==================================================

review_pr_nodes = safe_get(
    reviews_raw,
    ["data", "repository", "pullRequests", "nodes"],
    []
)

for pr in review_pr_nodes:
    pr_number = pr.get("number")
    review_nodes = safe_get(pr, ["reviews", "nodes"], [])

    for r in review_nodes:
        normalized_events.append({
            "event_id": str(uuid.uuid4()),
            "actor": safe_get(r, ["author", "login"], "unknown"),
            "event_type": "review",
            "text": r.get("body", ""),
            "timestamp": r.get("submittedAt", ""),
            "related": {
                "commit": None,
                "pr": pr_number,
                "issue": None
            },
            "metadata": {
                "review_state": r.get("state")
            }
        })


# ==================================================
# TRANSCRIPT (SAFE IF EMPTY)
# ==================================================

if isinstance(transcript_raw, list):
    for t in transcript_raw:
        normalized_events.append({
            "event_id": str(uuid.uuid4()),
            "actor": t.get("speaker", "unknown"),
            "event_type": "transcript",
            "text": t.get("text", ""),
            "timestamp": t.get("time", ""),
            "related": {
                "commit": None,
                "pr": None,
                "issue": None
            },
            "metadata": {}
        })


# ==================================================
# SAVE OUTPUT
# ==================================================

with open("normalized_events.json", "w", encoding="utf-8") as f:
    json.dump(normalized_events, f, indent=2)

print("✅ Layer 1 DONE")
print(f"📊 Total normalized events: {len(normalized_events)}")
