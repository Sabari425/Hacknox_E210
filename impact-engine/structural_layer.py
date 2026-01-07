import json
from datetime import datetime

# ---------- LOAD SEMANTIC EVENTS ----------
with open("semantic_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

def normalize_time(ts):
    if not ts:
        return None
    try:
        return ts  # keep ISO string, JSON-safe
    except:
        return None

# ---------- STRUCTURAL SIGNAL EXTRACTION ----------
for e in events:
    structural = {}

    # Merge signal (PR only)
    structural["merged"] = (
        e["event_type"] == "pr"
        and e["metadata"].get("merged", False)
    )

    # Size signal (commit impact proxy)
    if e["event_type"] == "commit":
        structural["size_score"] = (
            e["metadata"].get("additions", 0)
            + e["metadata"].get("deletions", 0)
        )
    else:
        structural["size_score"] = 0

    # Discussion signal
    structural["discussion"] = e["metadata"].get("comments", 0)

    # Timestamp (JSON-safe)
    structural["timestamp"] = normalize_time(e.get("timestamp"))

    e["structural"] = structural

# ---------- SAVE ----------
with open("structural_events.json", "w", encoding="utf-8") as f:
    json.dump(events, f, indent=2)

print("✅ Layer 3 complete: structural_events.json created")
