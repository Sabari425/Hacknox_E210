import json
from collections import defaultdict

# ---------- LOAD METRIC EVENTS ----------
with open("metric_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# ---------- AGGREGATE BY ACTOR ----------
actors = defaultdict(lambda: {
    "total_impact": 0,
    "event_count": 0,
    "review_events": 0,
    "invisible_score": 0,
    "high_impact_events": 0,
    "low_impact_events": 0
})

for e in events:
    actor = e["actor"]
    impact = e["metrics"]["final_impact"]

    actors[actor]["total_impact"] += impact
    actors[actor]["event_count"] += 1

    if e["event_type"] == "review":
        actors[actor]["review_events"] += 1
        actors[actor]["invisible_score"] += e["metrics"]["invisible"]

    if impact >= 7:
        actors[actor]["high_impact_events"] += 1
    if impact <= 2:
        actors[actor]["low_impact_events"] += 1

# ---------- ROLE INFERENCE ----------
actor_roles = {}

for actor, stats in actors.items():
    avg_impact = (
        stats["total_impact"] / stats["event_count"]
        if stats["event_count"] > 0 else 0
    )

    # Mentor
    if stats["review_events"] >= 5 and stats["invisible_score"] >= 8:
        role = "Mentor"

    # Silent Architect
    elif avg_impact >= 6 and stats["event_count"] <= 10:
        role = "Silent Architect"

    # Impact Driver
    elif avg_impact >= 6 and stats["event_count"] > 10:
        role = "Impact Driver"

    # Firefighter
    elif stats["high_impact_events"] >= 3:
        role = "Firefighter"

    # Noisy Contributor
    elif avg_impact <= 2 and stats["event_count"] >= 10:
        role = "Noisy Contributor"

    # Builder (default)
    else:
        role = "Builder"

    actor_roles[actor] = {
        "role": role,
        "avg_impact": round(avg_impact, 2),
        "events": stats["event_count"]
    }

# ---------- SAVE ----------
with open("actor_roles.json", "w", encoding="utf-8") as f:
    json.dump(actor_roles, f, indent=2)

print("✅ Layer 5 complete: actor_roles.json created")
