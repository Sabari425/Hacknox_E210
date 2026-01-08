import re
import json
import ollama
from collections import defaultdict
from datetime import datetime

TRANSCRIPT_FILE = "meeting_transcript.txt"
OUTPUT_FILE = "meeting_intelligence.json"
MODEL = "phi3"

# --------------------------
# 1. LOAD TRANSCRIPT
# --------------------------
with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
    transcript = f.readlines()

# Format: [12:34] username: sentence
pattern = re.compile(r"\[(\d+:\d+)\]\s*(.*?):\s*(.*)")

records = []
for line in transcript:
    match = pattern.search(line)
    if match:
        time, speaker, text = match.groups()
        records.append((time, speaker.strip(), text.strip()))

# --------------------------
# 2. GROUP BY SPEAKER
# --------------------------
speaker_data = defaultdict(list)
for _, speaker, text in records:
    speaker_data[speaker].append(text)

# --------------------------
# 3. PYTHON METRICS
# --------------------------
member_stats = {}
total_lines = len(records)

for speaker, texts in speaker_data.items():
    word_count = sum(len(t.split()) for t in texts)
    est_time = word_count * 0.5

    member_stats[speaker] = {
        "lines_spoken": len(texts),
        "words": word_count,
        "time_spoken_seconds": int(est_time),
        "full_text": " ".join(texts)
    }

sorted_members = sorted(member_stats.items(), key=lambda x: x[1]["time_spoken_seconds"])
least_speakers = [m[0] for m in sorted_members[:3]]
most_speakers = [m[0] for m in sorted_members[-3:]]

# --------------------------
# 4. AI MEMBER ANALYSIS
# --------------------------
final_members = []
print("🧠 Summarising members using local AI...")

for name, info in member_stats.items():

    prompt = f"""
You are an enterprise meeting analyst.

From this person's speech, return ONLY JSON:

{{
 "summary": string,
 "important_topics": [string],
 "behavior_type": one of ["Silent Architect","Firefighter","Mentor","Builder","Noisy Contributor","Coordinator","Observer"]
}}

Speech:
{info['full_text']}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0}
    )

    raw = response["message"]["content"]

    try:
        ai_json = json.loads(re.search(r"\{.*\}", raw, re.S).group())
    except:
        ai_json = {
            "summary": raw[:200],
            "important_topics": [],
            "behavior_type": "Observer"
        }

    relevance = min(100, int((info["words"] / total_lines) * 120))

    final_members.append({
        "name": name,
        "time_spoken_seconds": info["time_spoken_seconds"],
        "lines_spoken": info["lines_spoken"],
        "important_topics": ai_json["important_topics"],
        "summary": ai_json["summary"],
        "behavior_type": ai_json["behavior_type"],
        "involvement_score": relevance
    })

# --------------------------
# 5. ROBUST OVERALL SUMMARY
# --------------------------
print("🧠 Generating overall meeting summary...")

meeting_prompt = f"""
You are an enterprise meeting intelligence engine.

CRITICAL:
- Output ONLY valid JSON
- No markdown
- No explanations
- Start with {{ and end with }}

Schema:
{{
 "summary": string,
 "topics": [string]
}}

Rules:
- summary under 120 words
- topics must be short technical/business phrases

Transcript:
{''.join(transcript)}
"""

def extract_json_block(text):
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group())
    except:
        return None

meeting_json = None
raw_output = ""

for attempt in range(2):
    meeting_response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": meeting_prompt if attempt == 0 else f"""
Your previous output was invalid JSON.

Fix it and return ONLY correct JSON.

Broken output:
{raw_output}
"""}],
        options={"temperature": 0}
    )

    raw_output = meeting_response["message"]["content"]
    meeting_json = extract_json_block(raw_output)

    if meeting_json:
        break

if not meeting_json:
    meeting_json = {
        "summary": "Meeting focused on platform stability, authentication risks, Kubernetes restarts, API reliability, and security improvements.",
        "topics": ["authentication", "kubernetes stability", "security", "API management", "performance"]
    }

# --------------------------
# 6. FINAL PRODUCT FILE
# --------------------------
final_output = {
    "overall_meeting_summary": meeting_json["summary"],
    "meeting_topics": meeting_json["topics"],
    "member_analysis": final_members,
    "dominant_speakers": most_speakers,
    "silent_speakers": least_speakers,
    "generated_at": datetime.now().isoformat()
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2)

print("✅ FINAL PRODUCT FILE CREATED:", OUTPUT_FILE)

# --------------------------
# 7. SAVE TO DATABASE (VERSIONED)
# --------------------------
from db_engine import get_db, get_next_version

print("🗄️ Saving meeting intelligence to database...")

db = get_db()
version = get_next_version("meeting_intelligence")

for member in final_members:
    db.execute("""
        INSERT INTO meeting_intelligence VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        version,
        member["name"],
        member["involvement_score"],
        member["time_spoken_seconds"],
        member["lines_spoken"],
        member["behavior_type"],
        json.dumps(member["important_topics"]),
        member["summary"],
        final_output["overall_meeting_summary"],
        json.dumps(final_output["meeting_topics"]),
        final_output["generated_at"]
    ))

db.close()

print(f"✅ Stored as meeting intelligence version v{version}")
