import json
import re
from pathlib import Path

# ---------- LOAD NORMALIZED EVENTS ----------
with open("normalized_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# ---------- SIMPLE NLP HELPERS ----------

BUG_KEYWORDS = ["bug", "fix", "error", "break", "fail", "regression"]
FEATURE_KEYWORDS = ["add", "introduce", "support", "enable", "feature"]
REFACTOR_KEYWORDS = ["refactor", "cleanup", "remove", "simplify", "drop"]
DOC_KEYWORDS = ["doc", "readme", "documentation", "typo"]

MENTOR_KEYWORDS = ["suggest", "consider", "recommend", "maybe", "could you"]
ARCH_KEYWORDS = ["design", "architecture", "approach", "structure"]
BLOCKING_KEYWORDS = ["block", "blocking", "depends", "unblock"]

def classify_intent(text):
    t = text.lower()
    if any(k in t for k in BUG_KEYWORDS):
        return "bug_fix"
    if any(k in t for k in FEATURE_KEYWORDS):
        return "feature"
    if any(k in t for k in REFACTOR_KEYWORDS):
        return "refactor"
    if any(k in t for k in DOC_KEYWORDS):
        return "docs"
    return "other"

def extract_signals(text):
    t = text.lower()
    signals = []
    if any(k in t for k in MENTOR_KEYWORDS):
        signals.append("mentoring")
    if any(k in t for k in ARCH_KEYWORDS):
        signals.append("architecture")
    if any(k in t for k in BLOCKING_KEYWORDS):
        signals.append("blocking")
    if len(text.strip()) < 10:
        signals.append("noise")
    return signals

def quality_score(text):
    length = len(text.split())
    if length > 15:
        return "high", 0.9
    if length > 6:
        return "medium", 0.6
    return "low", 0.3

# ---------- MAIN SEMANTIC PASS ----------
semantic_events = []

for e in events:
    text = e.get("text", "") or ""

    intent = classify_intent(text)
    signals = extract_signals(text)
    quality, confidence = quality_score(text)

    e["semantic"] = {
        "intent": intent,
        "signals": signals,
        "quality": quality,
        "confidence": confidence
    }

    semantic_events.append(e)

# ---------- SAVE OUTPUT ----------
with open("semantic_events.json", "w", encoding="utf-8") as f:
    json.dump(semantic_events, f, indent=2)

print("✅ Layer 2 complete: semantic_events.json created")
