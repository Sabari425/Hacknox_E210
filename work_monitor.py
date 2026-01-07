import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
from typing import Dict, List, Optional
import io
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Workforce Contribution Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #21262d;
    --border-color: #30363d;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --text-tertiary: #6e7681;
    --accent-blue: #58a6ff;
    --accent-green: #3fb950;
    --accent-red: #f85149;
    --accent-yellow: #d29922;
    --accent-purple: #bc8cff;
    --accent-orange: #db6d28;
}

.stApp {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}
h1 {
    font-size: 24px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
    margin-bottom: 24px;
}
h2 { font-size: 20px; }
h3 { font-size: 16px; }
h4 { font-size: 14px; }

.github-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background-color: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
    padding: 16px 0;
    margin: -16px -16px 24px -16px;
}

.github-tabs {
    display: flex;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 24px;
    padding: 0 16px;
}
.github-tab {
    padding: 8px 16px;
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
}
.github-tab:hover {
    color: var(--text-primary);
    text-decoration: none;
}
.github-tab.active {
    color: var(--text-primary);
    border-bottom-color: var(--accent-blue);
    font-weight: 600;
}

.insight-card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    transition: border-color 0.2s ease;
}
.insight-card:hover {
    border-color: var(--accent-blue);
}
.insight-card h4 {
    margin-top: 0;
    margin-bottom: 12px;
    color: var(--text-primary);
    font-size: 16px;
    font-weight: 600;
}
.insight-card p {
    color: var(--text-secondary);
    font-size: 14px;
    margin-bottom: 16px;
    line-height: 1.5;
}

.role-block {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    height: 180px;
    display: flex;
    flex-direction: column;
}
.role-block-header {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
}
.role-icon {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    margin-right: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
}
.role-block h4 {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}
.role-members {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 8px;
    overflow-y: auto;
}
.role-member {
    display: flex;
    align-items: center;
    padding: 4px 8px;
    background-color: var(--bg-tertiary);
    border-radius: 6px;
    font-size: 12px;
    color: var(--text-secondary);
}
.role-member-point {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}

.repo-card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}
.repo-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.repo-name {
    font-weight: 600;
    color: var(--accent-blue);
    font-size: 15px;
}
.repo-stats {
    display: flex;
    gap: 12px;
    font-size: 12px;
    color: var(--text-tertiary);
}
.repo-files {
    background-color: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 12px;
    font-family: monospace;
    font-size: 13px;
    color: var(--text-secondary);
}
.file-item {
    display: flex;
    align-items: center;
    padding: 4px 0;
}
.file-icon {
    margin-right: 8px;
    font-size: 14px;
}
.folder-icon { color: var(--accent-yellow); }
.file-icon-code { color: var(--accent-blue); }
.file-icon-doc { color: var(--text-tertiary); }

.quadrant-graph {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    height: 500px;
}

.dataframe {
    background-color: var(--bg-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
}
.dataframe th {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
}
.dataframe td {
    border-color: var(--border-color) !important;
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    padding: 8px 16px !important;
}
.dataframe tr:hover td {
    background-color: var(--bg-tertiary) !important;
}

.stButton button {
    background-color: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 5px 16px !important;
    height: auto !important;
    min-height: 32px !important;
    transition: background-color 80ms cubic-bezier(0.33, 1, 0.68, 1) !important;
}
.stButton button:hover {
    background-color: var(--border-color) !important;
    border-color: var(--text-tertiary) !important;
}
.stButton button:active {
    background-color: var(--bg-secondary) !important;
}
.stButton button[kind="primary"] {
    background-color: var(--accent-green) !important;
    border-color: var(--accent-green) !important;
    color: white !important;
}
.stButton button[kind="primary"]:hover {
    background-color: #2ea043 !important;
    border-color: #2ea043 !important;
}

.stTextInput input, .stSelectbox select, .stMultiselect div, .stDateInput input, .stSlider div {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-size: 14px !important;
    padding: 5px 12px !important;
}
.stTextInput input:focus, .stSelectbox select:focus, .stMultiselect div:focus, .stDateInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3) !important;
    outline: none !important;
}
.stTextInput label, .stSelectbox label, .stMultiselect label, .stDateInput label, .stSlider label {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    margin-bottom: 4px !important;
}

.stMetric {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    padding: 16px !important;
}
.stMetric label {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.stMetric div {
    color: var(--text-primary) !important;
    font-size: 24px !important;
    font-weight: 600 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    border-bottom: 1px solid var(--border-color);
    padding: 0 16px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    border-radius: 6px 6px 0 0;
    padding: 8px 16px !important;
    color: var(--text-secondary) !important;
    border: 1px solid transparent !important;
    font-size: 14px !important;
}
.stTabs [aria-selected="true"] {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) var(--border-color) var(--bg-primary) !important;
    border-bottom: 2px solid var(--accent-blue) !important;
    font-weight: 600 !important;
}

.streamlit-expanderHeader {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background-color: var(--bg-primary) !important;
    border-color: var(--border-color) !important;
}

.stProgress > div > div {
    background-color: var(--accent-blue) !important;
}

.stAlert {
    border-radius: 6px !important;
    border: 1px solid var(--border-color) !important;
    font-size: 14px !important;
}
.stAlert[data-kind="success"] {
    background-color: rgba(63, 185, 80, 0.1) !important;
    border-color: var(--accent-green) !important;
}
.stAlert[data-kind="error"] {
    background-color: rgba(248, 81, 73, 0.1) !important;
    border-color: var(--accent-red) !important;
}
.stAlert[data-kind="info"] {
    background-color: rgba(88, 166, 255, 0.1) !important;
    border-color: var(--accent-blue) !important;
}
.stAlert[data-kind="warning"] {
    background-color: rgba(210, 153, 34, 0.1) !important;
    border-color: var(--accent-yellow) !important;
}

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}
::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--text-tertiary);
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 8px;
}
.status-active { background-color: var(--accent-green); }
.status-inactive { background-color: var(--text-tertiary); }
.status-warning { background-color: var(--accent-yellow); }
.status-error { background-color: var(--accent-red); }

.avatar {
    border-radius: 50%;
    object-fit: cover;
}

.badge {
    display: inline-block;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 500;
    border-radius: 12px;
    line-height: 18px;
}
.badge-green { background-color: var(--accent-green); color: white; }
.badge-blue { background-color: var(--accent-blue); color: white; }
.badge-red { background-color: var(--accent-red); color: white; }
.badge-yellow { background-color: var(--accent-yellow); color: black; }
.badge-purple { background-color: var(--accent-purple); color: white; }
.badge-gray { background-color: var(--bg-tertiary); color: var(--text-secondary); }
.badge-orange { background-color: var(--accent-orange); color: white; }

.spacing-8 { margin-bottom: 8px; }
.spacing-16 { margin-bottom: 16px; }
.spacing-24 { margin-bottom: 24px; }
.spacing-32 { margin-bottom: 32px; }

.grid-2x3 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
}
@media (min-width: 1200px) {
    .grid-2x3 {
        grid-template-columns: repeat(3, 1fr);
    }
}

*:focus {
    outline: 2px solid var(--accent-blue);
    outline-offset: 2px;
}
</style>
""", unsafe_allow_html=True)


class DataManager:
    ROLE_DEFINITIONS = {
        "Mentor": {"color": "#58a6ff", "icon": "👨‍🏫", "criteria": lambda emp: emp.get("code_reviews", 0) > 10},
        "Silent Architect": {"color": "#3fb950", "icon": "🏗️", "criteria": lambda emp: emp.get("impact_score", 0) > 75 and emp.get("visibility_score", 0) < 50},
        "Firefighter": {"color": "#f85149", "icon": "🚒", "criteria": lambda emp: emp.get("critical_bugs_fixed", 0) > 5},
        "Builder": {"color": "#db6d28", "icon": "🔨", "criteria": lambda emp: emp.get("features_delivered", 0) > 5},
        "Impact Driver": {"color": "#bc8cff", "icon": "🚀", "criteria": lambda emp: emp.get("impact_score", 0) > 80},
        "Noisy Contributor": {"color": "#d29922", "icon": "📢", "criteria": lambda emp: emp.get("visibility_score", 0) > 80 and emp.get("impact_score", 0) < 50}
    }

    @staticmethod
    def load_local_data():
        """Load files specifically from the 'github_data' folder"""
        data_cache = {}
        
        # DEFINING THE FOLDER PATH
        base_path = "github_data" 
        
        # 1. Load CSVs (Raw Counts)
        csv_files = {
            "commits": "commits.csv",
            "prs": "pull_requests.csv", 
            "issues": "issues.csv",
            "reviews": "reviews.csv",
            "contributors": "contributors.csv"
        }
        
        for key, filename in csv_files.items():
            # Combine folder path with filename (e.g., github_data/commits.csv)
            full_path = os.path.join(base_path, filename)
            
            if os.path.exists(full_path):
                try:
                    data_cache[key] = pd.read_csv(full_path)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    data_cache[key] = pd.DataFrame()
            else:
                data_cache[key] = pd.DataFrame()

        # 2. Load JSONs (Intelligence/Summaries)
        json_files = {
            "pr_intel": "graphql_pr_intelligence.json",
            "issue_intel": "graphql_issue_intelligence.json",
            "commit_intel": "graphql_commit_intelligence.json"
        }

        for key, filename in json_files.items():
            full_path = os.path.join(base_path, filename)
            
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data_cache[key] = json.load(f)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    data_cache[key] = []
            else:
                data_cache[key] = []
                
        return data_cache

    @staticmethod
    @st.cache_data(ttl=300)
    def generate_team_data(_team_name: str, size: int) -> pd.DataFrame:
        """Generate team data from LOCAL FILES"""
        try:
            raw_data = DataManager.load_local_data()
            
            # --- 1. AGGREGATE STATS BY USER ---
            user_stats = {}

            def normalize_user(u): return str(u).lower().strip() if u else "unknown"

            # Process Commits
            if not raw_data['commits'].empty:
                col = next((c for c in raw_data['commits'].columns if c.lower() in ['author', 'login', 'username', 'user']), None)
                if col:
                    counts = raw_data['commits'][col].value_counts()
                    for user, count in counts.items():
                        u = normalize_user(user)
                        if u not in user_stats: user_stats[u] = {}
                        user_stats[u]['commits'] = count

            # Process PRs
            if not raw_data['prs'].empty:
                col = next((c for c in raw_data['prs'].columns if c.lower() in ['author', 'login', 'username', 'user']), None)
                if col:
                    counts = raw_data['prs'][col].value_counts()
                    for user, count in counts.items():
                        u = normalize_user(user)
                        if u not in user_stats: user_stats[u] = {}
                        user_stats[u]['prs'] = count

            # Process Issues
            if not raw_data['issues'].empty:
                col = next((c for c in raw_data['issues'].columns if c.lower() in ['author', 'login', 'username', 'user']), None)
                if col:
                    counts = raw_data['issues'][col].value_counts()
                    for user, count in counts.items():
                        u = normalize_user(user)
                        if u not in user_stats: user_stats[u] = {}
                        user_stats[u]['issues'] = count

            # Process Reviews
            if not raw_data['reviews'].empty:
                col = next((c for c in raw_data['reviews'].columns if c.lower() in ['author', 'login', 'username', 'user']), None)
                if col:
                    counts = raw_data['reviews'][col].value_counts()
                    for user, count in counts.items():
                        u = normalize_user(user)
                        if u not in user_stats: user_stats[u] = {}
                        user_stats[u]['reviews'] = count

            # --- 2. MAP INTELLIGENCE (JSON) ---
            def get_ai_summary(username, json_list):
                summary_points = []
                topics = set()
                for item in json_list:
                    item_user = item.get('author', item.get('user', item.get('login', '')))
                    if normalize_user(item_user) == username:
                        if 'summary' in item: summary_points.append(item['summary'])
                        if 'title' in item: topics.add(item['title'])
                        if 'topics' in item: topics.update(item['topics'])
                return summary_points, list(topics)

            # --- 3. BUILD DATAFRAME ---
            employees = []
            
            if not user_stats:
                return DataManager._generate_dummy_fallback(_team_name, size)

            for username, stats in user_stats.items():
                if "bot" in username or "action" in username: continue 
                
                n_commits = stats.get('commits', 0)
                n_prs = stats.get('prs', 0)
                n_issues = stats.get('issues', 0)
                n_reviews = stats.get('reviews', 0)
                
                pr_summaries, pr_topics = get_ai_summary(username, raw_data['pr_intel'])
                issue_summaries, issue_topics = get_ai_summary(username, raw_data['issue_intel'])
                
                combined_topics = (pr_topics + issue_topics)[:6]
                
                # Combine summaries, defaulting to a generic string if empty
                ai_summary_text = " • ".join(pr_summaries[:2] + issue_summaries[:1])
                if not ai_summary_text: 
                    ai_summary_text = f"Contributor active in {n_commits} commits."

                # CALCULATE SCORES (Simple Heuristic)
                vis_score = min(100, (n_commits * 1.5) + (n_issues * 2) + (n_reviews * 3))
                imp_score = min(100, (n_prs * 8) + (n_reviews * 5) + (n_commits * 0.5))

                # Role logic
                emp_roles = []
                if n_reviews > 10: emp_roles.append("Mentor")
                if imp_score > 70 and vis_score < 50: emp_roles.append("Silent Architect")
                if imp_score > 80: emp_roles.append("Impact Driver")
                if not emp_roles: emp_roles.append("Normal Contributor")

                employees.append({
                    "employee_id": username[:8],
                    "name": username, 
                    "username": username,
                    "email": f"{username}@company.com",
                    "role": "Developer",
                    "primary_role": emp_roles[0],
                    "all_roles": emp_roles,
                    "team": _team_name,
                    "join_date": "2024-01-01",
                    "last_active": datetime.now().strftime("%Y-%m-%d"),
                    
                    "visibility_score": round(vis_score, 1),
                    "impact_score": round(imp_score, 1),
                    "quality_score": round(np.random.uniform(70, 95), 1),
                    "contribution_score": round((vis_score + imp_score)/2, 1),
                    
                    "commits": n_commits,
                    "slack_messages": 0,
                    "code_reviews": n_reviews,
                    "mentoring_sessions": int(n_reviews/3),
                    "critical_bugs_fixed": int(n_issues/2),
                    "features_delivered": n_prs,
                    "design_docs": 0,
                    
                    "meeting_summary": ai_summary_text,
                    "meeting_topics": combined_topics,
                    
                    "impact_level": "High" if imp_score > 60 else "Medium",
                    "avatar_color": "#58a6ff"
                })

            df = pd.DataFrame(employees)
            
            if not df.empty:
                df["is_silent_architect"] = df["all_roles"].apply(lambda x: "Silent Architect" in x)
                df["is_mentor"] = df["all_roles"].apply(lambda x: "Mentor" in x)
                df["is_firefighter"] = df["all_roles"].apply(lambda x: "Firefighter" in x)
                df["is_impact_driver"] = df["all_roles"].apply(lambda x: "Impact Driver" in x)
                df["is_noisy_contributor"] = df["all_roles"].apply(lambda x: "Noisy Contributor" in x)
                df["is_builder"] = df["all_roles"].apply(lambda x: "Builder" in x)
                
                df = df.sort_values('contribution_score', ascending=False)
                df['team_rank'] = range(1, len(df) + 1)
            
            return df

        except Exception as e:
            st.error(f"Error loading local data: {e}")
            return DataManager._generate_dummy_fallback(_team_name, size)

    @staticmethod
    def _generate_dummy_fallback(_team_name, size):
        return pd.DataFrame([{
            "name": "No Data Found", "impact_score": 0, "visibility_score": 0, 
            "role": "None", "primary_role": "Normal Contributor", "all_roles": [],
            "team_rank": 0, "last_active": "N/A", "commits": 0, "username": "none"
        }])

    @staticmethod
    def get_member_activity_history(employee_id: str) -> pd.DataFrame:
        try:
            history = []
            start_date = datetime.now() - timedelta(days=180)
            for i in range(180):
                date = start_date + timedelta(days=i)
                history.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "commits": np.random.randint(0, 5),
                    "role_change": None
                })
            return pd.DataFrame(history)
        except: return pd.DataFrame()

    @staticmethod
    @st.cache_data(ttl=600)
    def generate_repository_structure():
        return {
            "platform-modernization": {"name": "platform-modernization", "description": "Migrating legacy monolith", "language": "Go", "stars": 42, "forks": 12, "last_updated": "2024-01-01", "folders": {"src": ["main.go"], "api": ["handlers.go"]}, "assigned_members": ["Alex Smith"]},
        }


class AuthenticationSystem:

    USER_DB = {
        "manager_a": {
            "password": "manager123",
            "name": "Sarah Johnson",
            "username": "sarahj",
            "title": "Senior Engineering Manager",
            "department": "Platform Engineering",
            "avatar_color": "#58a6ff",
            "teams": {
                "Team A": {"size": 12, "focus": "Backend Services"},
                "Team B": {"size": 8, "focus": "Frontend Development"}
            }
        },
        "manager_b": {
            "password": "manager456",
            "name": "Michael Chen",
            "username": "michaelc",
            "title": "Product Engineering Manager",
            "department": "Product Development",
            "avatar_color": "#3fb950",
            "teams": {
                "Team C": {"size": 15, "focus": "Mobile Applications"},
                "Team D": {"size": 10, "focus": "Data Platform"}
            }
        }
    }

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict]:
        """Authenticate user"""
        try:
            if username in AuthenticationSystem.USER_DB:
                if AuthenticationSystem.USER_DB[username]["password"] == password:
                    return AuthenticationSystem.USER_DB[username]
            return None
        except Exception:
            return None


class VisualizationEngine:
    """Create enhanced visualizations"""

    @staticmethod
    def create_four_quadrant_chart(data: pd.DataFrame, team_name: str):
        """Create four-quadrant activity vs impact chart with floating quadrant labels"""
        try:
            fig = go.Figure()

            # Define quadrant colors
            quadrant_colors = {
                "Impact Drivers": "#bc8cff",  # Q1: High impact, high activity
                "Noisy Contributors": "#db6d28",  # Q2: Low impact, high activity
                "Normal Contributors": "#d29922",  # Q3: Low impact, low activity
                "Silent Architects": "#3fb950"  # Q4: High impact, low activity
            }

            # Add traces for each quadrant
            for quadrant, color in quadrant_colors.items():
                if quadrant == "Impact Drivers":
                    quadrant_data = data[(data["impact_score"] > 70) & (data["visibility_score"] > 55)]
                elif quadrant == "Noisy Contributors":
                    quadrant_data = data[(data["impact_score"] <= 70) & (data["visibility_score"] > 55)]
                elif quadrant == "Normal Contributors":
                    quadrant_data = data[(data["impact_score"] <= 70) & (data["visibility_score"] <= 55)]
                else:  # Silent Architects
                    quadrant_data = data[(data["impact_score"] > 70) & (data["visibility_score"] <= 55)]

                if not quadrant_data.empty:
                    fig.add_trace(go.Scatter(
                        x=quadrant_data["visibility_score"],
                        y=quadrant_data["impact_score"],
                        mode="markers",
                        name=quadrant,
                        marker=dict(
                            size=12,
                            color=color,
                            line=dict(width=1, color="white")
                        ),
                        text=quadrant_data["name"],
                        hovertemplate=(
                                "<b>%{text}</b><br>"
                                "Role: " + quadrant_data["role"] + "<br>"
                                                                   "Activity: %{x:.1f}<br>"
                                                                   "Impact: %{y:.1f}<br>"
                                                                   "Contribution: " + quadrant_data[
                                    "contribution_score"].astype(str) + "<extra></extra>"
                        )
                    ))

            # Add quadrant lines
            fig.add_hline(y=70, line_dash="dash", line_color="#6e7681", line_width=1)
            fig.add_vline(x=55, line_dash="dash", line_color="#6e7681", line_width=1)

            # Add floating quadrant labels
            fig.add_annotation(
                x=80, y=85,
                text="Impact Drivers",
                showarrow=False,
                font=dict(size=14, color="#bc8cff", family="Arial Black"),
                bgcolor="rgba(0,0,0,0.7)",
                bordercolor="#bc8cff",
                borderwidth=1,
                borderpad=4,
                opacity=0.9
            )

            fig.add_annotation(
                x=80, y=30,
                text="Noisy Contributors",
                showarrow=False,
                font=dict(size=14, color="#db6d28", family="Arial Black"),
                bgcolor="rgba(0,0,0,0.7)",
                bordercolor="#db6d28",
                borderwidth=1,
                borderpad=4,
                opacity=0.9
            )

            fig.add_annotation(
                x=20, y=30,
                text="Normal Contributors",
                showarrow=False,
                font=dict(size=14, color="#d29922", family="Arial Black"),
                bgcolor="rgba(0,0,0,0.7)",
                bordercolor="#d29922",
                borderwidth=1,
                borderpad=4,
                opacity=0.9
            )

            fig.add_annotation(
                x=20, y=85,
                text="Silent Architects",
                showarrow=False,
                font=dict(size=14, color="#3fb950", family="Arial Black"),
                bgcolor="rgba(0,0,0,0.7)",
                bordercolor="#3fb950",
                borderwidth=1,
                borderpad=4,
                opacity=0.9
            )

            fig.update_layout(
                title=f"Activity vs Impact Analysis - {team_name}",
                xaxis_title="Activity Score (Visibility)",
                yaxis_title="Impact Score",
                height=500,
                hovermode="closest",
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font=dict(color="#c9d1d9", size=13),
                legend=dict(
                    bgcolor="#161b22",
                    bordercolor="#30363d",
                    borderwidth=1,
                    font=dict(size=12)
                ),
                margin=dict(l=60, r=40, t=60, b=60)
            )

            fig.update_xaxes(
                gridcolor="#21262d",
                zerolinecolor="#30363d",
                range=[0, 100]
            )
            fig.update_yaxes(
                gridcolor="#21262d",
                zerolinecolor="#30363d",
                range=[0, 100]
            )

            return fig

        except Exception:
            return go.Figure()

    @staticmethod
    def create_activity_timeline(activity_data: pd.DataFrame, member_name: str):
        """Create activity timeline for member detail view"""
        try:
            if activity_data.empty:
                return None

            fig = go.Figure()

            # Add commits trace
            fig.add_trace(go.Scatter(
                x=activity_data["date"],
                y=activity_data["commits"].rolling(7).mean(),
                mode="lines",
                name="Commits (7-day avg)",
                line=dict(color="#58a6ff", width=2),
                fill='tozeroy',
                fillcolor='rgba(88, 166, 255, 0.1)'
            ))

            # Add markers for role changes
            role_changes = activity_data[activity_data["role_change"].notna()]
            if not role_changes.empty:
                fig.add_trace(go.Scatter(
                    x=role_changes["date"],
                    y=[5] * len(role_changes),
                    mode="markers",
                    name="Role Changes",
                    marker=dict(
                        size=10,
                        color="#3fb950",
                        symbol="diamond"
                    ),
                    text=role_changes["role_change"],
                    hovertemplate="<b>%{text}</b><extra></extra>"
                ))

            fig.update_layout(
                title=f"Activity Timeline - {member_name}",
                xaxis_title="Date",
                yaxis_title="Average Daily Commits",
                height=300,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font=dict(color="#c9d1d9", size=13),
                legend=dict(
                    bgcolor="#161b22",
                    bordercolor="#30363d",
                    borderwidth=1,
                    font=dict(size=12)
                ),
                margin=dict(l=40, r=40, t=40, b=40)
            )

            fig.update_xaxes(gridcolor="#21262d")
            fig.update_yaxes(gridcolor="#21262d")

            return fig

        except Exception:
            return None

    @staticmethod
    def create_impact_breakdown(employee: pd.Series):
        """Create impact breakdown chart for member detail"""
        try:
            categories = ["Bug Fixes", "Features", "Code Reviews", "Mentoring", "Design"]
            values = [
                employee.get("critical_bugs_fixed", 0),
                employee.get("features_delivered", 0),
                employee.get("code_reviews", 0) / 10,  # Normalize
                employee.get("mentoring_sessions", 0),
                employee.get("design_docs", 0) * 3  # Weight design docs
            ]

            fig = go.Figure(data=[go.Bar(
                x=categories,
                y=values,
                marker_color=["#f85149", "#3fb950", "#58a6ff", "#bc8cff", "#db6d28"]
            )])

            fig.update_layout(
                title="Impact Breakdown",
                height=300,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font=dict(color="#c9d1d9", size=13),
                showlegend=False,
                margin=dict(l=40, r=40, t=40, b=40)
            )

            fig.update_xaxes(gridcolor="#21262d")
            fig.update_yaxes(gridcolor="#21262d")

            return fig

        except Exception:
            return None


class LoginPage:
    """GitHub-style login page"""

    @staticmethod
    def show():
        """Display login page"""
        st.markdown("""
        <div style='max-width: 340px; margin: 120px auto; padding: 24px; 
                    background-color: #161b22; border: 1px solid #30363d; 
                    border-radius: 6px;'>
            <div style='text-align: center; margin-bottom: 24px;'>
                <div style='font-size: 20px; font-weight: 600; color: #c9d1d9;'>
                    Workforce Contribution Monitor
                </div>
                <div style='font-size: 14px; color: #8b949e; margin-top: 8px;'>
                    Sign in to your account
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            with st.container():
                with st.form("login_form"):
                    username = st.text_input("Username or email address")
                    password = st.text_input("Password", type="password")

                    submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)

                    if submit:
                        with st.spinner("Signing in..."):
                            time.sleep(0.3)
                            user = AuthenticationSystem.authenticate(username, password)
                            if user:
                                st.session_state.user = user
                                st.session_state.username = username
                                st.session_state.authenticated = True
                                st.session_state.current_team = None
                                st.session_state.current_employee = None
                                st.rerun()
                            else:
                                st.error("Incorrect username or password")

                st.markdown("---")

                st.markdown("""
                <div style='font-size: 13px; color: #8b949e; text-align: center;'>
                    <div style='margin-bottom: 8px;'>Demo credentials:</div>
                    <div>• manager_a / manager123</div>
                    <div>• manager_b / manager456</div>
                </div>
                """, unsafe_allow_html=True)


class ManagerDashboard:
    """Manager dashboard - shows all teams"""

    @staticmethod
    def show():
        """Display manager dashboard"""
        # Header with GitHub styling
        col1, col2, col3 = st.columns([6, 1, 1])

        with col1:
            st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 16px;'>
                <div style='width: 40px; height: 40px; border-radius: 50%; 
                            background-color: {st.session_state.user.get('avatar_color', '#6e7681')};
                            display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: 600;'>
                    {st.session_state.user['name'][0]}
                </div>
                <div>
                    <div style='font-size: 20px; font-weight: 600; color: #c9d1d9;'>
                        {st.session_state.user['name']}
                    </div>
                    <div style='font-size: 14px; color: #8b949e;'>
                        {st.session_state.user['title']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if st.button("Sign out", type="secondary", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        st.markdown("---")

        # Teams section
        st.markdown("<h2>Your Teams</h2>", unsafe_allow_html=True)

        teams = st.session_state.user["teams"]
        cols = st.columns(min(len(teams), 2))

        for idx, (team_name, team_info) in enumerate(teams.items()):
            with cols[idx % len(cols)]:
                with st.container(border=True):
                    st.markdown(f"### {team_name}")
                    st.markdown(f"<span style='color: #8b949e; font-size: 14px;'>{team_info['focus']}</span>",
                                unsafe_allow_html=True)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"<div style='color: #6e7681; font-size: 13px;'>Team size</div>",
                                    unsafe_allow_html=True)
                        st.markdown(
                            f"<div style='color: #c9d1d9; font-size: 18px; font-weight: 600;'>{team_info['size']}</div>",
                            unsafe_allow_html=True)

                    with col_b:
                        if st.button("View team", key=f"team_{team_name}", use_container_width=True):
                            st.session_state.current_team = team_name
                            st.rerun()


class TeamDashboard:
    """Team dashboard with new hierarchical structure"""

    @staticmethod
    def show(team_name: str):
        """Display team dashboard"""
        # Header with navigation
        col1, col2 = st.columns([6, 1])
        with col1:
            st.title(f"Team: {team_name}")
        with col2:
            if st.button("← Back", type="secondary", use_container_width=True):
                st.session_state.current_team = None
                st.session_state.current_employee = None
                st.rerun()

        st.markdown("---")

        # Load team data
        team_size = st.session_state.user["teams"][team_name]["size"]
        team_data = DataManager.generate_team_data(team_name, team_size)

        # Team metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Team Size", team_size)

        st.markdown("---")

        # New tab structure
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Hidden High-Impact Contributors",
            "Team Members",
            "Project Structure",
            "Contribution Roles",
            "Activity vs Impact",
            "Member Detail"
        ])

        with tab1:
            TeamDashboard._show_hidden_contributors(team_data, team_name)
        with tab2:
            TeamDashboard._show_team_members(team_data, team_name)
        with tab3:
            TeamDashboard._show_project_structure(team_name)
        with tab4:
            TeamDashboard._show_contribution_roles(team_data, team_name)
        with tab5:
            TeamDashboard._show_activity_vs_impact(team_data, team_name)
        with tab6:
            TeamDashboard._show_member_detail(team_data, team_name)

    @staticmethod
    def _show_hidden_contributors(data: pd.DataFrame, team_name: str):
        """Show insight layer with different contributor types"""
        st.markdown("<h3>Hidden High-Impact Contributors</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #8b949e; font-size: 14px;'>Identifying team members who contribute significant value but may be overlooked</p>",
            unsafe_allow_html=True)

        # Insight cards in a 2x2 grid
        col1, col2 = st.columns(2)

        with col1:
            # Silent Architects card
            silent_archs = data[data["is_silent_architect"]]
            with st.container(border=True):
                st.markdown("<h4 style='color: #3fb950;'>Silent Architects</h4>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: #8b949e; font-size: 14px;'>High impact with low visibility. Often work on complex problems without seeking recognition.</p>",
                    unsafe_allow_html=True)

                if not silent_archs.empty:
                    for _, arch in silent_archs.iterrows():
                        st.markdown(f"<div style='display: flex; align-items: center; margin: 8px 0;'>"
                                    f"<div style='width: 8px; height: 8px; border-radius: 50%; background-color: #3fb950; margin-right: 8px;'></div>"
                                    f"<span>{arch['name']}</span>"
                                    f"<span style='color: #6e7681; font-size: 12px; margin-left: 8px;'>(Impact: {arch['impact_score']})</span>"
                                    f"</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #6e7681; font-size: 13px;'>No silent architects identified</p>",
                                unsafe_allow_html=True)

            # Firefighters card
            firefighters = data[data["is_firefighter"]]
            with st.container(border=True):
                st.markdown("<h4 style='color: #f85149;'>Firefighters</h4>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: #8b949e; font-size: 14px;'>Handle critical incidents and last-minute fixes. Often work under pressure to resolve urgent issues.</p>",
                    unsafe_allow_html=True)

                if not firefighters.empty:
                    for _, firefighter in firefighters.iterrows():
                        st.markdown(f"<div style='display: flex; align-items: center; margin: 8px 0;'>"
                                    f"<div style='width: 8px; height: 8px; border-radius: 50%; background-color: #f85149; margin-right: 8px;'></div>"
                                    f"<span>{firefighter['name']}</span>"
                                    f"<span style='color: #6e7681; font-size: 12px; margin-left: 8px;'>(Critical fixes: {firefighter['critical_bugs_fixed']})</span>"
                                    f"</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #6e7681; font-size: 13px;'>No firefighters identified</p>",
                                unsafe_allow_html=True)

        with col2:
            # Mentors card
            mentors = data[data["is_mentor"]]
            with st.container(border=True):
                st.markdown("<h4 style='color: #58a6ff;'>Mentors</h4>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: #8b949e; font-size: 14px;'>Invest time in developing others through code reviews, pair programming, and guidance.</p>",
                    unsafe_allow_html=True)

                if not mentors.empty:
                    for _, mentor in mentors.iterrows():
                        st.markdown(f"<div style='display: flex; align-items: center; margin: 8px 0;'>"
                                    f"<div style='width: 8px; height: 8px; border-radius: 50%; background-color: #58a6ff; margin-right: 8px;'></div>"
                                    f"<span>{mentor['name']}</span>"
                                    f"<span style='color: #6e7681; font-size: 12px; margin-left: 8px;'>(Mentoring sessions: {mentor['mentoring_sessions']})</span>"
                                    f"</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #6e7681; font-size: 13px;'>No mentors identified</p>",
                                unsafe_allow_html=True)

            # Removed Builders card as requested

        # Removed Insights summary and Recommendations sections as requested

    @staticmethod
    def _show_team_members(data: pd.DataFrame, team_name: str):
        """Show team members with enhanced filtering"""
        st.markdown(f"<h3>Team Members - {team_name}</h3>", unsafe_allow_html=True)

        # Filters section
        st.markdown("#### Filters")

        col1, col2, col3 = st.columns(3)

        with col1:
            # Role filter
            roles = sorted(data["role"].unique())
            selected_roles = st.multiselect(
                "Filter by Role",
                options=roles,
                default=roles,
                key="role_filter"
            )

        with col2:
            # Impact level filter
            impact_levels = ["High", "Medium", "Low"]
            selected_impact = st.multiselect(
                "Filter by Impact Level",
                options=impact_levels,
                default=impact_levels,
                key="impact_filter"
            )

        with col3:
            # Search bar instead of Activity Score Range
            search_query = st.text_input(
                "Search members",
                placeholder="Type name or username...",
                key="member_search"
            )

        # Apply filters
        filtered_data = data.copy()

        if selected_roles:
            filtered_data = filtered_data[filtered_data["role"].isin(selected_roles)]

        if selected_impact:
            filtered_data = filtered_data[filtered_data["impact_level"].isin(selected_impact)]

        if search_query:
            search_query_lower = search_query.lower()
            filtered_data = filtered_data[
                filtered_data["name"].str.lower().str.contains(search_query_lower) |
                filtered_data["username"].str.lower().str.contains(search_query_lower)
            ]

        # Members Table - Simple table without column links
        st.markdown("#### Members Table")

        # Prepare display data
        display_data = filtered_data[["name", "impact_score", "team_rank", "last_active"]].copy()
        display_data = display_data.rename(columns={
            "name": "Name",
            "impact_score": "Impact Score",
            "team_rank": "Rank",
            "last_active": "Last Active"
        })

        # Sort by rank by default
        display_data = display_data.sort_values("Rank")

        # Display as a simple table
        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Name": st.column_config.TextColumn(width="large"),
                "Impact Score": st.column_config.NumberColumn(format="%.1f"),
                "Rank": st.column_config.NumberColumn(format="%d"),
                "Last Active": st.column_config.DateColumn()
            }
        )

        # Quick stats
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Showing Members", len(filtered_data), delta=f"{len(filtered_data)}/{len(data)}")
        with col2:
            avg_impact = filtered_data["impact_score"].mean()
            st.metric("Average Impact Score", f"{avg_impact:.1f}")
        with col3:
            if st.button("Export to CSV", type="secondary", use_container_width=True):
                csv = filtered_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{team_name}_members_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

    @staticmethod
    def _show_project_structure(team_name: str):
        """Show repository structure"""
        st.markdown("<h3>Project Structure</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8b949e; font-size: 14px;'>Repository organization and assigned team members</p>",
                    unsafe_allow_html=True)

        repos = DataManager.generate_repository_structure()

        if not repos:
            st.info("No repository data available")
            return

        # Display each repository
        for repo_id, repo in repos.items():
            with st.container(border=True):
                # Repository header
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"<h4 style='color: #58a6ff;'>{repo['name']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #8b949e; font-size: 14px;'>{repo['description']}</p>",
                                unsafe_allow_html=True)

                with col2:
                    st.markdown(f"<div style='text-align: right;'>"
                                f"<div style='color: #6e7681; font-size: 12px;'>Language: {repo['language']}</div>"
                                f"<div style='color: #6e7681; font-size: 12px;'>Last updated: {repo['last_updated']}</div>"
                                f"</div>", unsafe_allow_html=True)

                # Repository content in columns
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("#### Folders & Files")
                    with st.container(border=True):
                        for folder, files in repo["folders"].items():
                            st.markdown(
                                f"<div style='color: #d29922; font-family: monospace; margin: 4px 0;'>📁 {folder}/</div>",
                                unsafe_allow_html=True)
                            for file in files:
                                icon = "📄" if file.endswith((".go", ".tsx", ".ts", ".js", ".py", ".css")) else "📝"
                                st.markdown(
                                    f"<div style='color: #8b949e; font-family: monospace; margin-left: 20px; margin: 2px 0;'>{icon} {file}</div>",
                                    unsafe_allow_html=True)

                with col2:
                    st.markdown("#### Assigned Members")
                    with st.container(border=True):
                        for member in repo["assigned_members"]:
                            st.markdown(f"<div style='display: flex; align-items: center; margin: 8px 0;'>"
                                        f"<div style='width: 8px; height: 8px; border-radius: 50%; background-color: #58a6ff; margin-right: 8px;'></div>"
                                        f"<span>{member}</span>"
                                        f"</div>", unsafe_allow_html=True)

                        # Repository statistics
                        st.markdown("<div style='margin-top: 16px; padding-top: 16px; border-top: 1px solid #30363d;'>"
                                    f"<div style='display: flex; justify-content: space-between;'>"
                                    f"<span style='color: #6e7681; font-size: 12px;'>Stars: {repo['stars']}</span>"
                                    f"<span style='color: #6e7681; font-size: 12px;'>Forks: {repo['forks']}</span>"
                                    f"</div>"
                                    "</div>", unsafe_allow_html=True)

    @staticmethod
    def _show_contribution_roles(data: pd.DataFrame, team_name: str):
        """Show contribution roles in 2x3 block layout"""
        st.markdown("<h3>Contribution Roles</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #8b949e; font-size: 14px;'>Team members categorized by their primary contribution patterns</p>",
            unsafe_allow_html=True)

        # Create role blocks data
        role_data = {}
        for role_name, role_def in DataManager.ROLE_DEFINITIONS.items():
            members = []
            for _, member in data.iterrows():
                if role_name in member["all_roles"]:
                    members.append({
                        "name": member["name"],
                        "color": role_def["color"]
                    })
            role_data[role_name] = members

        # Add Normal Contributors
        normal_members = []
        for _, member in data.iterrows():
            if member["primary_role"] == "Normal Contributor":
                normal_members.append({
                    "name": member["name"],
                    "color": "#6e7681"
                })
        role_data["Normal Contributor"] = normal_members

        # Display in 2x3 grid
        st.markdown('<div class="grid-2x3">', unsafe_allow_html=True)

        # Define display order
        display_order = [
            "Mentor", "Silent Architect", "Firefighter",
            "Builder", "Impact Driver", "Noisy Contributor"
        ]

        for role_name in display_order:
            if role_name in role_data:
                members = role_data[role_name]
                role_def = DataManager.ROLE_DEFINITIONS.get(role_name, {"color": "#6e7681", "icon": "👤"})

                # Create role block
                st.markdown(f"""
                <div class="role-block">
                    <div class="role-block-header">
                        <div class="role-icon" style="background-color: {role_def['color']};">
                            {role_def.get('icon', '👤')}
                        </div>
                        <h4>{role_name}</h4>
                    </div>
                    <div class="role-members">
                """, unsafe_allow_html=True)

                if members:
                    for member in members[:10]:  # Show first 10 members
                        st.markdown(f"""
                        <div class="role-member">
                            <div class="role-member-point" style="background-color: {member['color']};"></div>
                            {member['name']}
                        </div>
                        """, unsafe_allow_html=True)

                    if len(members) > 10:
                        st.markdown(f"""
                        <div class="role-member" style="color: #6e7681; font-style: italic;">
                            +{len(members) - 10} more
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="role-member" style="color: #6e7681; font-style: italic;">
                        No members in this role
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Role statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            total_roles = sum(len(members) for members in role_data.values())
            unique_members = set()
            for members in role_data.values():
                for member in members:
                    unique_members.add(member["name"])

            st.metric("Total Role Assignments", total_roles)

        with col2:
            st.metric("Unique Members", len(unique_members))

        with col3:
            avg_roles = total_roles / len(unique_members) if unique_members else 0
            st.metric("Avg Roles per Member", f"{avg_roles:.1f}")

    @staticmethod
    def _show_activity_vs_impact(data: pd.DataFrame, team_name: str):
        """Show four-quadrant analysis"""
        st.markdown("<h3>Activity vs Impact Analysis</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #8b949e; font-size: 14px;'>Visualizing team members across four quadrants based on activity and impact scores</p>",
            unsafe_allow_html=True)

        # Create four-quadrant chart
        fig = VisualizationEngine.create_four_quadrant_chart(data, team_name)
        st.plotly_chart(fig, use_container_width=True)

        # Quadrant breakdown (simplified version without expander)
        st.markdown("#### Quadrant Breakdown")

        quadrants = {
            "Impact Drivers": (data["impact_score"] > 70) & (data["visibility_score"] > 55),
            "Noisy Contributors": (data["impact_score"] <= 70) & (data["visibility_score"] > 55),
            "Normal Contributors": (data["impact_score"] <= 70) & (data["visibility_score"] <= 55),
            "Silent Architects": (data["impact_score"] > 70) & (data["visibility_score"] <= 55)
        }

        cols = st.columns(4)
        quadrant_colors = {
            "Impact Drivers": "#bc8cff",
            "Noisy Contributors": "#db6d28",
            "Normal Contributors": "#d29922",
            "Silent Architects": "#3fb950"
        }

        for idx, (name, condition) in enumerate(quadrants.items()):
            with cols[idx]:
                count = len(data[condition])
                percent = (count / len(data) * 100) if len(data) > 0 else 0

                with st.container(border=True):
                    st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>{name}</div>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='color: {quadrant_colors[name]}; font-size: 24px; font-weight: 600;'>{count}</div>",
                        unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #6e7681; font-size: 12px;'>{percent:.1f}% of team</div>",
                                unsafe_allow_html=True)

        # Removed "Quadrant Analysis & Recommendations" expander as requested

    @staticmethod
    def _show_member_detail(data: pd.DataFrame, team_name: str):
        """Show member detail view (on click from other sections)"""
        st.markdown("<h3>Member Detail View</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8b949e; font-size: 14px;'>Select a team member to view detailed information</p>",
                    unsafe_allow_html=True)

        # Member selection
        member_options = [f"{row['name']} ({row['role']})" for _, row in data.iterrows()]
        selected_member = st.selectbox(
            "Select Team Member",
            options=member_options,
            key="member_select"
        )

        if selected_member:
            # Extract member name from selection
            member_name = selected_member.split(" (")[0]
            member_data = data[data["name"] == member_name].iloc[0]

            # Generate activity history
            activity_history = DataManager.get_member_activity_history(member_data["employee_id"])

            # Display member detail sections
            col1, col2 = st.columns([2, 1])

            with col1:
                # Profile Summary
                with st.container(border=True):
                    st.markdown("#### Profile Summary")

                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Team Rank", f"#{member_data['team_rank']}")
                    with col_b:
                        st.metric("Impact Score", f"{member_data['impact_score']:.1f}")
                    with col_c:
                        st.metric("Activity Score", f"{member_data['visibility_score']:.1f}")

                    # Primary role and skills
                    st.markdown("**Primary Role:**")
                    role_color = DataManager.ROLE_DEFINITIONS.get(
                        member_data["primary_role"],
                        {"color": "#6e7681"}
                    )["color"]

                    st.markdown(f"<div style='display: inline-block; padding: 4px 12px; border-radius: 12px; "
                                f"background-color: {role_color}; color: white; font-size: 12px; font-weight: 500;'>"
                                f"{member_data['primary_role']}</div>", unsafe_allow_html=True)

                    st.markdown("**Primary Technology:**")
                    st.code(member_data["primary_tech"], language=None)

            with col2:
                # Quick stats
                with st.container(border=True):
                    st.markdown("#### Quick Stats")

                    stats = [
                        ("Commits", member_data["commits"]),
                        ("Critical Fixes", member_data["critical_bugs_fixed"]),
                        ("Features", member_data["features_delivered"]),
                        ("Code Reviews", member_data["code_reviews"]),
                        ("Mentoring", member_data["mentoring_sessions"])
                    ]

                    for label, value in stats:
                        st.markdown(f"<div style='display: flex; justify-content: space-between; margin: 8px 0;'>"
                                    f"<span style='color: #8b949e;'>{label}</span>"
                                    f"<span style='color: #c9d1d9; font-weight: 500;'>{value}</span>"
                                    f"</div>", unsafe_allow_html=True)

            # Additional sections
            # Role History
            with st.container(border=True):
                st.markdown("#### Role History")

                if not activity_history.empty:
                    role_changes = activity_history[activity_history["role_change"].notna()]

                    if not role_changes.empty:
                        for _, change in role_changes.iterrows():
                            st.markdown(f"<div style='margin: 8px 0;'>"
                                        f"<span style='color: #8b949e; font-size: 12px;'>{change['date']}</span><br>"
                                        f"<span style='color: #c9d1d9;'>{change['role_change']}</span>"
                                        f"</div>", unsafe_allow_html=True)
                    else:
                        st.info("No role changes recorded")
                else:
                    st.info("No activity history available")

            # Activity Timeline
            with st.container(border=True):
                st.markdown("#### Activity Timeline")

                fig = VisualizationEngine.create_activity_timeline(activity_history, member_name)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Activity timeline not available")

            # Impact Breakdown
            col1, col2 = st.columns([2, 1])

            with col1:
                with st.container(border=True):
                    st.markdown("#### Impact Breakdown")

                    fig = VisualizationEngine.create_impact_breakdown(member_data)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Impact breakdown not available")

            with col2:
                # Project Ownership
                with st.container(border=True):
                    st.markdown("#### Project Ownership")

                    repos = DataManager.generate_repository_structure()
                    member_projects = []

                    for repo_id, repo in repos.items():
                        if member_name in repo["assigned_members"]:
                            member_projects.append(repo["name"])

                    if member_projects:
                        for project in member_projects[:5]:  # Show first 5 projects
                            st.markdown(f"<div style='margin: 8px 0;'>"
                                        f"<span style='color: #58a6ff;'>📁 {project}</span>"
                                        f"</div>", unsafe_allow_html=True)

                        if len(member_projects) > 5:
                            st.markdown(f"<div style='color: #6e7681; font-size: 12px;'>"
                                        f"+{len(member_projects) - 5} more projects"
                                        f"</div>", unsafe_allow_html=True)
                    else:
                        st.info("No project assignments")


def main():
    """Main application controller"""
    try:
        # Initialize session state
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "user" not in st.session_state:
            st.session_state.user = None
        if "username" not in st.session_state:
            st.session_state.username = None
        if "current_team" not in st.session_state:
            st.session_state.current_team = None
        if "current_employee" not in st.session_state:
            st.session_state.current_employee = None

        # Application routing
        if not st.session_state.authenticated:
            LoginPage.show()

        elif st.session_state.authenticated and not st.session_state.current_team:
            ManagerDashboard.show()

        elif st.session_state.current_team:
            TeamDashboard.show(st.session_state.current_team)

    except Exception as e:
        # Global error handler
        st.error("An unexpected error occurred")
        st.info("The application will restart")

        # Clear state and restart
        time.sleep(2)
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


if __name__ == "__main__":
    main()
