import json
from collections import defaultdict

# ---------- LOAD FILES ----------
with open("metric_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

with open("actor_roles.json", "r", encoding="utf-8") as f:
    roles = json.load(f)

# ---------- AGGREGATE SUPPORTING DATA ----------
actor_stats = defaultdict(lambda: {
    "high_impact": 0,
    "reviews": 0,
    "total_events": 0
})

for e in events:
    actor = e["actor"]
    actor_stats[actor]["total_events"] += 1

    if e["metrics"]["final_impact"] >= 7:
        actor_stats[actor]["high_impact"] += 1

    if e["event_type"] == "review":
        actor_stats[actor]["reviews"] += 1

# ---------- EXPLANATION GENERATOR ----------
explanations = {}

for actor, role_data in roles.items():
    role = role_data["role"]
    avg = role_data["avg_impact"]
    total = role_data["events"]

    hi = actor_stats[actor]["high_impact"]
    reviews = actor_stats[actor]["reviews"]

    if role == "Noisy Contributor":
        explanation = (
            f"High activity ({total} events) but consistently low impact "
            f"(average impact score {avg}). Contributions were largely minor "
            f"and did not significantly affect outcomes."
        )

    elif role == "Firefighter":
        explanation = (
            f"Handled multiple high-impact situations ({hi} critical events), "
            f"often addressing urgent or breaking issues. Average impact "
            f"score of {avg} reflects reactive but valuable contributions."
        )

    elif role == "Silent Architect":
        explanation = (
            f"Delivered high-impact contributions with low visible activity. "
            f"Despite only {total} events, work had strong influence "
            f"(average impact {avg})."
        )

    elif role == "Impact Driver":
        explanation = (
            f"Consistently delivered high-impact work across {total} events. "
            f"Average impact score of {avg} indicates sustained execution "
            f"on important tasks."
        )

    elif role == "Mentor":
        explanation = (
            f"Provided significant guidance through reviews ({reviews} review events), "
            f"helping others improve while maintaining solid impact "
            f"(average impact {avg})."
        )

    else:  # Builder
        explanation = (
            f"Steady contributor with balanced participation ({total} events). "
            f"Average impact score of {avg} reflects reliable execution."
        )

    explanations[actor] = {
        "role": role,
        "average_impact": avg,
        "total_events": total,
        "explanation": explanation
    }

# ---------- SAVE ----------
with open("explainability.json", "w", encoding="utf-8") as f:
    json.dump(explanations, f, indent=2)

print("✅ Layer 6 complete: explainability.json created")
