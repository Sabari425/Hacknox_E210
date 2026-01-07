import json
from collections import defaultdict

# ---------- LOAD FINAL DATA ----------
with open("metric_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

with open("actor_roles.json", "r", encoding="utf-8") as f:
    roles = json.load(f)

with open("explainability.json", "r", encoding="utf-8") as f:
    explanations = json.load(f)

# ---------- DASHBOARD OVERVIEW ----------
dashboard_overview = []

for actor, data in explanations.items():
    dashboard_overview.append({
        "actor": actor,
        "role": data["role"],
        "average_impact": data["average_impact"],
        "events": data["total_events"]
    })

dashboard_overview.sort(key=lambda x: x["average_impact"], reverse=True)

# ---------- EMPLOYEE PROFILES ----------
employee_profiles = {}

for actor, data in explanations.items():
    employee_profiles[actor] = {
        "summary": data,
        "events": [
            e for e in events if e["actor"] == actor
        ]
    }

# ---------- ACTIVITY VS IMPACT ----------
activity_vs_impact = []

for actor, data in explanations.items():
    activity_vs_impact.append({
        "actor": actor,
        "activity": data["total_events"],
        "impact": data["average_impact"],
        "role": data["role"]
    })

# ---------- ROLE GROUPS ----------
role_groups = defaultdict(list)

for actor, data in explanations.items():
    role_groups[data["role"]].append(actor)

# ---------- SAVE FILES ----------
with open("dashboard_overview.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_overview, f, indent=2)

with open("employee_profiles.json", "w", encoding="utf-8") as f:
    json.dump(employee_profiles, f, indent=2)

with open("activity_vs_impact.json", "w", encoding="utf-8") as f:
    json.dump(activity_vs_impact, f, indent=2)

with open("role_groups.json", "w", encoding="utf-8") as f:
    json.dump(role_groups, f, indent=2)

print("✅ Layer 7 complete: Dashboard artifacts created")
