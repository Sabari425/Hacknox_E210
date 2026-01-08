import json
from datetime import datetime
from db_engine import init_db, get_db, get_next_version

MEETING_FILE = "meeting_intelligence.json"
GIT_FILE = "git_intelligence.json"
OUTPUT_FILE = "final_team_intelligence.json"

# -------------------------
# INIT DATABASE
# -------------------------
init_db()
db = get_db()
version = get_next_version("final_team_intelligence")
generated_at = datetime.now().isoformat()

# -------------------------
# LOAD DATA
# -------------------------
with open(MEETING_FILE, "r", encoding="utf-8") as f:
    meeting = json.load(f)

with open(GIT_FILE, "r", encoding="utf-8") as f:
    git = json.load(f)

meeting_people = {m["name"].lower(): m for m in meeting["member_analysis"]}
git_people = {m["name"].lower(): m for m in git["members"]}

all_users = set(meeting_people.keys()) | set(git_people.keys())

final_team = []

# -------------------------
# FUSION ENGINE
# -------------------------
for user in all_users:

    meet = meeting_people.get(user, {})
    gitp = git_people.get(user, {})

    meeting_score = meet.get("involvement_score", 0)
    git_score = gitp.get("git_scores", {}).get("git_score", 0)

    merged_score = round((meeting_score * 0.4) + (git_score * 0.6), 2)

    meeting_role = meet.get("behavior_type", "Observer")
    git_role = gitp.get("git_behavior", "Observer")

    if "Silent Architect" in [meeting_role, git_role] and merged_score > 55:
        final_role = "Silent Architect"
    elif "Firefighter" in [meeting_role, git_role] and git_score > 50:
        final_role = "Firefighter"
    elif "Mentor" in [meeting_role, git_role] and meeting_score > 25:
        final_role = "Mentor"
    elif "Coordinator" in [meeting_role, git_role] and merged_score > 40:
        final_role = "Coordinator"
    elif meeting_score > 50 and git_score < 30:
        final_role = "Noisy Contributor"
    else:
        final_role = "Observer"

    final_team.append({
        "name": user,
        "merged_score": merged_score,
        "final_behavior": final_role,
        "git_score": git_score,
        "meeting_score": meeting_score
    })

# -------------------------
# SAVE FINAL JSON FILE
# -------------------------
final_output = {
    "generated_at": generated_at,
    "members": sorted(final_team, key=lambda x: x["merged_score"], reverse=True)
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2)

print("🏁 FINAL PRODUCT FILE CREATED:", OUTPUT_FILE)

# -------------------------
# STORE MEETING DATA
# -------------------------
for m in meeting["member_analysis"]:
    db.execute("""
    INSERT INTO meeting_intelligence VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        version,
        m["name"],
        m["involvement_score"],
        m["time_spoken_seconds"],
        m["lines_spoken"],
        m["behavior_type"],
        json.dumps(m["important_topics"]),
        m["summary"],
        meeting["overall_meeting_summary"],
        json.dumps(meeting["meeting_topics"]),
        generated_at
    ))

# -------------------------
# STORE GIT DATA
# -------------------------
for g in git["members"]:
    s = g["git_scores"]
    db.execute("""
    INSERT INTO git_intelligence VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        version,
        g["name"],
        s["work_importance"],
        s["pr_involvement"],
        s["comment_quality"],
        s["activity"],
        s["collaboration_health"],
        s["git_score"],
        g["git_behavior"],
        generated_at
    ))

# -------------------------
# STORE FINAL FUSION DATA
# -------------------------
for f in final_output["members"]:
    db.execute("""
    INSERT INTO final_team_intelligence VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        version,
        f["name"],
        f["merged_score"],
        f["final_behavior"],
        f["git_score"],
        f["meeting_score"],
        generated_at
    ))

db.close()

print(f"📦 All intelligence stored in database (version {version})")
