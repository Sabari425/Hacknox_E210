import subprocess
import time
import os
import sys
from datetime import datetime, timedelta

# --- CONFIGURATION ---
TARGET_HOUR = 9
TARGET_MINUTE = 30
SUB_DIR = "github_data"

# List of scripts in execution order
SCRIPTS = [
    ("github_export.py", SUB_DIR),
    ("graphql_pr_intelligence.py", SUB_DIR),
    ("graphql_commit.py", SUB_DIR),
    ("graphql_issue.py", SUB_DIR),
    ("graphql_review.py", SUB_DIR),
    ("meeting_analyser.py", "."),
    ("git_analyser.py", "."),
    ("fusion.py", ".")
]

def run_pipeline():
    print(f"\n🏎️  GREEN LIGHT: Starting Workflow at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    for script_name, folder in SCRIPTS:
        print(f"Drafting: {script_name}...")
        try:
            subprocess.run([sys.executable, script_name], cwd=folder, check=True)
            print(f"✅ Success: {script_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ CRASH: {script_name} failed. Stopping pipeline.")
            return
        except FileNotFoundError:
             print(f"❌ ERROR: Could not find file {script_name} in {folder}")
             return

    print("-" * 50)
    print(f"🏁 Lap Complete at {datetime.now().strftime('%H:%M:%S')}")

def get_seconds_until_target():
    now = datetime.now()
    # Create a datetime object for Today at 9:30 AM
    target = now.replace(hour=TARGET_HOUR, minute=TARGET_MINUTE, second=0, microsecond=0)
    
    # If 9:30 AM has already passed today, target 9:30 AM tomorrow
    if now >= target:
        target += timedelta(days=1)
        
    wait_seconds = (target - now).total_seconds()
    
    print(f"⏳ Next run scheduled for: {target.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   (Waiting for {wait_seconds/3600:.2f} hours)")
    
    return wait_seconds

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("🤖 Automation System Online.")
    
    while True:
        # 1. Calculate how long to sleep until next 9:30 AM
        seconds_to_wait = get_seconds_until_target()
        
        # 2. Sleep until that time
        time.sleep(seconds_to_wait)
        
        # 3. Run the scripts
        run_pipeline()
        
        # 4. Loop repeats, finds the next day's 9:30 AM