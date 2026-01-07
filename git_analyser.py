import csv
import json
from collections import defaultdict, Counter
from datetime import datetime

COMMITS_FILE = "github_data/commits.csv"
PRS_FILE = "github_data/pull_requests.csv"
REVIEWS_FILE = "github_data/reviews.csv"
OUTPUT_FILE = "git_intelligence.json"

# -------------------------
# LOAD CSV HELPERS
# -------------------------
def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


commits = load_csv(COMMITS_FILE)
prs = load_csv(PRS_FILE)
reviews = load_csv(REVIEWS_FILE)

# -------------------------
# DATA AGGREGATION
# -------------------------
people = defaultdict(lambda: {
    "commits": [],
    "prs": [],
    "reviews": [],
    "blocked": 0
})

for c in commits:
    people[c["user"]]["commits"].append(c)

for p in prs:
    people[p["user"]]["prs"].append(p)
    if p["merged"] == "False":
        people[p["user"]]["blocked"] += 1

for r in reviews:
    people[r["reviewer"]]["reviews"].append(r)

# -------------------------
# SCORING ENGINE
# -------------------------
final_people = []

max_commits = max(len(p["commits"]) for p in people.values())
max_prs = max(len(p["prs"]) for p in people.values())
max_reviews = max(len(p["reviews"]) for p in people.values())

for user, data in people.items():

    # 1. WORK IMPORTANCE
    importance = 0
    for c in data["commits"]:
        importance += int(c["core_files"]) * 3
        importance += int(c["files_changed"])
        importance += min(10, int(c["total_changes"]) / 40)

    work_importance = min(100, importance)

    # 2. PR INVOLVEMENT
    pr_involvement = (len(data["prs"]) / max_prs) * 100 if max_prs else 0

    # 3. COMMENT QUALITY
    approvals = sum(1 for r in data["reviews"] if r["state"] == "APPROVED")
    changes = sum(1 for r in data["reviews"] if r["state"] == "CHANGES_REQUESTED")

    comment_quality = min(100, approvals * 20 + changes * 10)

    # 4. ACTIVITY SCORE
    activity = (len(data["commits"]) / max_commits) * 100 if max_commits else 0

    # 5. COLLABORATION HEALTH
    collaboration_health = max(0, 100 - data["blocked"] * 20)

    # FINAL SCORE
    git_score = round(
        work_importance * 0.35 +
        pr_involvement * 0.25 +
        comment_quality * 0.2 +
        activity * 0.1 +
        collaboration_health * 0.1, 1
    )

    # -------------------------
    # BEHAVIOR ENGINE
    # -------------------------
    if work_importance > 70 and activity < 50:
        git_behavior = "Silent Architect"

    elif work_importance > 60 and collaboration_health < 50:
        git_behavior = "Firefighter"

    elif comment_quality > 60 and collaboration_health > 60:
        git_behavior = "Mentor"

    elif activity > 70 and work_importance < 50:
        git_behavior = "Noisy Contributor"

    elif pr_involvement > 50 and collaboration_health > 60:
        git_behavior = "Coordinator"

    else:
        git_behavior = "Observer"

    final_people.append({
        "name": user,
        "git_scores": {
            "work_importance": round(work_importance, 1),
            "pr_involvement": round(pr_involvement, 1),
            "comment_quality": round(comment_quality, 1),
            "activity": round(activity, 1),
            "collaboration_health": round(collaboration_health, 1),
            "git_score": git_score
        },
        "git_behavior": git_behavior
    })

# -------------------------
# SAVE FILE
# -------------------------
final_output = {
    "generated_at": datetime.now().isoformat(),
    "members": sorted(final_people, key=lambda x: x["git_scores"]["git_score"], reverse=True)
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2)

print("✅ Git intelligence generated:", OUTPUT_FILE)
