import json

# ---------- LOAD STRUCTURAL EVENTS ----------
with open("structural_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# ---------- SCORING FUNCTIONS ----------

def work_importance(e):
    intent = e["semantic"]["intent"]

    if intent == "bugfix":
        return 5
    if intent == "feature":
        return 4
    if intent == "refactor":
        return 3
    if intent == "docs":
        return 2
    return 1  # other / noise


def complexity_score(e):
    size = e["structural"]["size_score"]
    discussion = e["structural"]["discussion"]

    score = 0
    if size > 500:
        score += 3
    elif size > 100:
        score += 2
    elif size > 20:
        score += 1

    if discussion >= 5:
        score += 2
    elif discussion >= 2:
        score += 1

    return score


def unblocking_score(e):
    # proxy: merged PRs with discussion unblock others
    if e["event_type"] == "pr" and e["structural"]["merged"]:
        return 2 + min(e["structural"]["discussion"], 3)
    return 0


def invisible_work_score(e):
    if e["event_type"] == "review":
        if e["semantic"]["quality"] == "high":
            return 3
        return 1
    return 0


def future_impact_score(e):
    intent = e["semantic"]["intent"]
    if intent in ["refactor", "bugfix"]:
        return 2
    return 0


# ---------- APPLY METRICS ----------
for e in events:
    metrics = {}

    metrics["importance"] = work_importance(e)
    metrics["complexity"] = complexity_score(e)
    metrics["unblocking"] = unblocking_score(e)
    metrics["invisible"] = invisible_work_score(e)
    metrics["future"] = future_impact_score(e)

    metrics["final_impact"] = (
        metrics["importance"]
        + metrics["complexity"]
        + metrics["unblocking"]
        + metrics["invisible"]
        + metrics["future"]
    )

    e["metrics"] = metrics

# ---------- SAVE ----------
with open("metric_events.json", "w", encoding="utf-8") as f:
    json.dump(events, f, indent=2)

print("✅ Layer 4 complete: metric_events.json created")
