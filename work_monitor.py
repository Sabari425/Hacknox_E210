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

st.set_page_config(
    page_title="Workforce Contribution Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* GitHub Dark Theme - Strict Implementation */
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
}

/* Base app styling */
.stApp {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

/* Headers */
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

/* GitHub-style navigation */
.nav-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background-color: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
    padding: 16px 0;
    margin: -16px -16px 24px -16px;
}

/* GitHub-style tabs */
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

/* Cards and containers */
.stContainer, .stTabs, .stExpander {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    padding: 16px !important;
}

/* Dataframes with GitHub styling */
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

/* GitHub-style buttons */
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
    transform: none !important;
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

/* Inputs with GitHub styling */
.stTextInput input, .stSelectbox select, .stMultiselect div, .stDateInput input {
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
.stTextInput label, .stSelectbox label, .stMultiselect label, .stDateInput label {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    margin-bottom: 4px !important;
}

/* Metrics with GitHub styling */
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

/* Tabs styling */
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

/* Expanders */
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

/* Progress bars */
.stProgress > div > div {
    background-color: var(--accent-blue) !important;
}

/* Success/Error/Info/Warning */
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

/* Custom scrollbar */
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

/* Remove Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Status indicators */
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

/* Avatar styling */
.avatar {
    border-radius: 50%;
    object-fit: cover;
}

/* Badge styling */
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

/* Spacing system */
.spacing-8 { margin-bottom: 8px; }
.spacing-16 { margin-bottom: 16px; }
.spacing-24 { margin-bottom: 24px; }
.spacing-32 { margin-bottom: 32px; }

/* Focus ring for accessibility */
*:focus {
    outline: 2px solid var(--accent-blue);
    outline-offset: 2px;
}
</style>
""", unsafe_allow_html=True)


class DataManager:

    @staticmethod
    @st.cache_data(ttl=300)
    def generate_team_data(_team_name: str, size: int) -> pd.DataFrame:
        try:
            # Set seed for reproducibility
            seed = hash(_team_name) % 10000
            random.seed(seed)
            np.random.seed(seed)

            # First names and last names
            first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley",
                           "Avery", "Quinn", "Blake", "Hayden", "Drew", "Cameron",
                           "Jamie", "Robin", "Skyler", "Dakota", "Rowan", "Sage"]

            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                          "Miller", "Davis", "Rodriguez", "Martinez", "Lee", "Gonzalez"]

            roles = ["Senior Developer", "Developer", "Junior Developer", "Tech Lead",
                     "Software Architect", "DevOps Engineer", "QA Engineer"]

            employees = []

            for i in range(size):
                emp_id = f"{_team_name[:3].upper()}{i + 1:03d}"
                first = random.choice(first_names)
                last = random.choice(last_names)
                role = random.choice(roles)

                # Generate base performance score (0-1)
                base_perf = np.random.beta(2, 2)

                # Activity metrics (visibility)
                commits = int(np.random.gamma(shape=2, scale=15) * (1.5 if "Senior" in role else 1))
                slack_msgs = int(np.random.gamma(shape=1.5, scale=30) * base_perf)
                meetings = int(np.random.gamma(shape=1, scale=15) * base_perf)

                # Impact metrics
                critical_fixes = int(np.random.poisson(5) * (2 if "Senior" in role else 1))
                features = int(np.random.poisson(4) * base_perf)
                code_reviews = int(np.random.gamma(shape=2, scale=8) * (1.5 if "Senior" in role else 1))
                mentoring = int(np.random.poisson(3) * (2 if "Senior" in role else 0.5))

                # Quality metrics
                pr_approval = np.clip(base_perf * 0.8 + np.random.normal(0.1, 0.05), 0.65, 0.98)
                bug_rate = np.clip((1 - base_perf) * 0.2 + np.random.normal(0.03, 0.01), 0.01, 0.15)
                code_coverage = np.clip(base_perf * 0.7 + np.random.normal(0.15, 0.05), 0.6, 0.95)

                # Calculate scores
                visibility_score = min(100, np.log1p(commits) * 12 + np.log1p(slack_msgs) * 8 + meetings * 0.4)
                impact_score = min(100,
                                   critical_fixes * 2.5 + features * 3 + np.log1p(code_reviews) * 8 + mentoring * 1.5)
                quality_score = min(100, pr_approval * 60 + (1 - bug_rate) * 30 + code_coverage * 10)

                # Determine if silent architect
                is_silent_architect = (impact_score > 70 and
                                       visibility_score < 55 and
                                       pr_approval > 0.85)

                # Contribution score (scale-invariant)
                contribution_raw = (
                        impact_score * 0.35 +
                        quality_score * 0.30 +
                        np.log1p(mentoring + code_reviews) * 15 * 0.20 +
                        (100 - abs(visibility_score - 50)) * 0.15
                )

                employees.append({
                    "employee_id": emp_id,
                    "name": f"{first} {last}",
                    "username": f"{first.lower()}{last[0].lower()}",
                    "email": f"{first.lower()}.{last.lower()}@company.com",
                    "role": role,
                    "team": _team_name,
                    "join_date": (datetime.now() - timedelta(days=random.randint(180, 1800))).strftime("%Y-%m-%d"),
                    "last_active": (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),

                    # Activity metrics
                    "commits": commits,
                    "slack_messages": slack_msgs,
                    "meetings_attended": meetings,
                    "prs_created": int(commits * 0.25),
                    "prs_reviewed": code_reviews,
                    "code_reviews": code_reviews,

                    # Impact metrics
                    "critical_bugs_fixed": critical_fixes,
                    "features_delivered": features,
                    "design_docs": random.randint(0, 5),
                    "mentoring_sessions": mentoring,

                    # Quality metrics
                    "pr_approval_rate": round(pr_approval, 3),
                    "bug_introduction_rate": round(bug_rate, 3),
                    "code_coverage": round(code_coverage, 3),

                    # Scores
                    "visibility_score": round(visibility_score, 1),
                    "impact_score": round(impact_score, 1),
                    "quality_score": round(quality_score, 1),
                    "collaboration_score": round(np.log1p(mentoring + code_reviews) * 20, 1),
                    "raw_contribution": round(contribution_raw, 1),

                    # Flags
                    "is_silent_architect": is_silent_architect,
                    "tenure_months": random.randint(6, 72),
                    "status": random.choice(["active", "active", "active", "on_leave"]),

                    # Additional
                    "primary_tech": random.choice(["Python", "Java", "JavaScript", "Go", "TypeScript"]),
                    "current_project": random.choice(["Platform Modernization", "API Gateway", "Database Migration"]),
                    "avatar_color": random.choice(["#58a6ff", "#3fb950", "#bc8cff", "#e3b341"])
                })

            df = pd.DataFrame(employees)

            # Apply scale-invariant scoring
            df = DataManager._calculate_scale_invariant_scores(df)

            return df

        except Exception as e:
            return pd.DataFrame([{
                "employee_id": "ERR001",
                "name": "System Error",
                "role": "System",
                "team": _team_name,
                "visibility_score": 0,
                "impact_score": 0,
                "contribution_score": 0
            }])

    @staticmethod
    def _calculate_scale_invariant_scores(df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Normalize using percentiles within team
            for col in ['raw_contribution', 'impact_score', 'quality_score', 'collaboration_score']:
                if col in df.columns:
                    df[f'{col}_percentile'] = df[col].rank(pct=True)

            # Final contribution score (percentile-based, scale-invariant)
            weights = {
                'impact_score_percentile': 0.40,
                'quality_score_percentile': 0.30,
                'collaboration_score_percentile': 0.20,
                'raw_contribution_percentile': 0.10
            }

            df['contribution_score'] = 0
            for col, weight in weights.items():
                if col in df.columns:
                    df['contribution_score'] += df[col] * weight * 100

            df['contribution_score'] = df['contribution_score'].round(1)

            # Add rank within team
            df = df.sort_values('contribution_score', ascending=False)
            df['team_rank'] = range(1, len(df) + 1)

            return df

        except Exception:
            # Fallback
            df['contribution_score'] = df['raw_contribution']
            df = df.sort_values('contribution_score', ascending=False)
            df['team_rank'] = range(1, len(df) + 1)
            return df

    @staticmethod
    @st.cache_data(ttl=600)
    def generate_project_structure():
        try:
            current_date = datetime.now()

            projects = {
                "platform-modernization": {
                    "name": "Platform Modernization",
                    "description": "Migrating legacy monolith to microservices architecture",
                    "status": "active",
                    "priority": "high",
                    "start_date": (current_date - timedelta(days=120)).strftime("%Y-%m-%d"),
                    "end_date": (current_date + timedelta(days=180)).strftime("%Y-%m-%d"),
                    "budget": "2.5M",
                    "owner": "Alex Smith",
                    "subdivisions": {
                        "backend-services": {
                            "name": "Backend Services",
                            "teams": {
                                "api-gateway": {
                                    "name": "API Gateway",
                                    "members": ["Alex Smith", "Jordan Johnson"],
                                    "tech_stack": ["Go", "gRPC", "Redis"],
                                    "progress": 75,
                                    "start_date": (current_date - timedelta(days=90)).strftime("%Y-%m-%d"),
                                    "end_date": (current_date + timedelta(days=60)).strftime("%Y-%m-%d"),
                                    "commits": 245,
                                    "prs_merged": 89
                                },
                                "user-service": {
                                    "name": "User Service",
                                    "members": ["Taylor Williams"],
                                    "tech_stack": ["Python", "FastAPI", "PostgreSQL"],
                                    "progress": 60,
                                    "start_date": (current_date - timedelta(days=75)).strftime("%Y-%m-%d"),
                                    "end_date": (current_date + timedelta(days=90)).strftime("%Y-%m-%d"),
                                    "commits": 180,
                                    "prs_merged": 67
                                }
                            }
                        },
                        "frontend-applications": {
                            "name": "Frontend Applications",
                            "teams": {
                                "admin-dashboard": {
                                    "name": "Admin Dashboard",
                                    "members": ["Riley Garcia", "Avery Miller"],
                                    "tech_stack": ["React", "TypeScript", "Tailwind"],
                                    "progress": 85,
                                    "start_date": (current_date - timedelta(days=60)).strftime("%Y-%m-%d"),
                                    "end_date": (current_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                                    "commits": 320,
                                    "prs_merged": 112
                                }
                            }
                        }
                    }
                },
                "api-gateway-redesign": {
                    "name": "API Gateway Redesign",
                    "description": "Redesigning API gateway for improved performance and security",
                    "status": "planning",
                    "priority": "medium",
                    "start_date": (current_date - timedelta(days=30)).strftime("%Y-%m-%d"),
                    "end_date": (current_date + timedelta(days=120)).strftime("%Y-%m-%d"),
                    "budget": "800K",
                    "owner": "Morgan Brown",
                    "subdivisions": {
                        "api-design": {
                            "name": "API Design",
                            "teams": {
                                "rest-apis": {
                                    "name": "REST APIs",
                                    "members": ["Morgan Brown", "Taylor Williams"],
                                    "tech_stack": ["OpenAPI", "Swagger"],
                                    "progress": 30,
                                    "start_date": (current_date - timedelta(days=20)).strftime("%Y-%m-%d"),
                                    "end_date": (current_date + timedelta(days=100)).strftime("%Y-%m-%d"),
                                    "commits": 45,
                                    "prs_merged": 18
                                }
                            }
                        }
                    }
                }
            }
            return projects
        except Exception:
            return {}

    @staticmethod
    def get_activity_data(employee_id: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        try:
            days = (end_date - start_date).days + 1
            if days <= 0:
                return pd.DataFrame()

            activities = []
            for i in range(days):
                current_date = start_date + timedelta(days=i)
                is_weekend = current_date.weekday() >= 5
                base = 0.2 if is_weekend else 1.0

                activities.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "commits": int(np.random.poisson(2) * base),
                    "prs_created": int(np.random.poisson(1) * base),
                    "prs_reviewed": int(np.random.poisson(1.5) * base),
                    "code_reviews": int(np.random.poisson(2) * base),
                    "hours_active": round(np.random.uniform(3, 8) * base, 1),
                    "slack_messages": int(np.random.poisson(15) * base),
                    "meetings": int(np.random.poisson(1) * base),
                    "bugs_fixed": int(np.random.poisson(0.5) * base),
                    "is_weekend": is_weekend,
                    "day_of_week": current_date.strftime("%A")
                })

            return pd.DataFrame(activities)
        except Exception:
            return pd.DataFrame()


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
        try:
            if username in AuthenticationSystem.USER_DB:
                if AuthenticationSystem.USER_DB[username]["password"] == password:
                    return AuthenticationSystem.USER_DB[username]
            return None
        except Exception:
            return None


class UIComponents:

    @staticmethod
    def github_header(title: str, show_back: bool = False):
        col1, col2, col3 = st.columns([6, 1, 1])

        with col1:
            st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)

        with col2:
            if show_back and st.session_state.get("current_team"):
                if st.button("Back to Team", type="secondary", use_container_width=True):
                    st.session_state.current_employee = None
                    st.rerun()

        with col3:
            if st.button("Sign Out", type="secondary", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        st.markdown("---")

    @staticmethod
    def date_range_filter(key_suffix: str = ""):
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.now() - timedelta(days=30),
                key=f"start_date_{key_suffix}"
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.now(),
                key=f"end_date_{key_suffix}"
            )

        with col3:
            st.markdown("<div style='height: 38px; display: flex; align-items: flex-end;'>", unsafe_allow_html=True)
            if st.button("Apply Filter", key=f"apply_filter_{key_suffix}", use_container_width=True):
                st.session_state[f"date_filter_applied_{key_suffix}"] = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Validate dates
        if start_date > end_date:
            st.error("Start date must be before end date")
            return None, None

        return start_date, end_date

    @staticmethod
    def member_card(employee: pd.Series, show_actions: bool = True):
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 3, 2])

            with col1:
                # Avatar
                st.markdown(f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; 
                                background-color: {employee.get('avatar_color', '#6e7681')};
                                display: flex; align-items: center; justify-content: center;
                                color: white; font-weight: 600;">
                        {employee['name'][0]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                # Name and info
                st.markdown(f"**{employee['name']}**")
                st.markdown(f"<span style='color: #8b949e; font-size: 13px;'>{employee['role']}</span>",
                            unsafe_allow_html=True)
                st.markdown(f"<span style='color: #6e7681; font-size: 12px;'>{employee['username']}</span>",
                            unsafe_allow_html=True)

            with col3:
                # Actions and stats
                if show_actions:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(
                            f"<div style='color: #8b949e; font-size: 13px;'>Rank #{employee.get('team_rank', 'N/A')}</div>",
                            unsafe_allow_html=True)
                    with col_b:
                        if st.button("View", key=f"view_{employee['employee_id']}", use_container_width=True):
                            st.session_state.current_employee = employee['employee_id']
                            st.rerun()

    @staticmethod
    def metric_card(label: str, value, delta: str = None):
        with st.container(border=True):
            st.markdown(f"<div style='color: #8b949e; font-size: 13px; font-weight: 500;'>{label}</div>",
                        unsafe_allow_html=True)
            st.markdown(f"<div style='color: #c9d1d9; font-size: 24px; font-weight: 600;'>{value}</div>",
                        unsafe_allow_html=True)
            if delta:
                color = "#3fb950" if delta.startswith("+") else "#f85149" if delta.startswith("-") else "#8b949e"
                st.markdown(f"<div style='color: {color}; font-size: 12px;'>{delta}</div>", unsafe_allow_html=True)


class VisualizationEngine:

    @staticmethod
    def create_activity_impact_chart(data: pd.DataFrame, team_name: str):
        try:
            fig = go.Figure()

            # Silent architects
            silent_data = data[data["is_silent_architect"]]
            if not silent_data.empty:
                fig.add_trace(go.Scatter(
                    x=silent_data["visibility_score"],
                    y=silent_data["impact_score"],
                    mode="markers",
                    name="Silent Architects",
                    marker=dict(
                        size=12,
                        color="#3fb950",
                        symbol="diamond",
                        line=dict(width=1, color="white")
                    ),
                    text=silent_data["name"],
                    hovertemplate=(
                            "<b>%{text}</b><br>"
                            "Role: " + silent_data["role"] + "<br>"
                                                             "Visibility: %{x:.1f}<br>"
                                                             "Impact: %{y:.1f}<extra></extra>"
                    )
                ))

            # Other team members
            other_data = data[~data["is_silent_architect"]]
            if not other_data.empty:
                fig.add_trace(go.Scatter(
                    x=other_data["visibility_score"],
                    y=other_data["impact_score"],
                    mode="markers",
                    name="Team Members",
                    marker=dict(
                        size=10,
                        color="#58a6ff",
                        opacity=0.8
                    ),
                    text=other_data["name"],
                    hovertemplate=(
                            "<b>%{text}</b><br>"
                            "Role: " + other_data["role"] + "<br>"
                                                            "Visibility: %{x:.1f}<br>"
                                                            "Impact: %{y:.1f}<extra></extra>"
                    )
                ))

            # Add quadrant lines
            fig.add_hline(y=70, line_dash="dash", line_color="#6e7681", line_width=1)
            fig.add_vline(x=55, line_dash="dash", line_color="#6e7681", line_width=1)

            fig.update_layout(
                title=f"Activity vs Impact - {team_name}",
                xaxis_title="Visibility Score",
                yaxis_title="Impact Score",
                height=400,
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
                margin=dict(l=40, r=40, t=40, b=40)
            )

            fig.update_xaxes(gridcolor="#21262d", zerolinecolor="#30363d")
            fig.update_yaxes(gridcolor="#21262d", zerolinecolor="#30363d")

            return fig

        except Exception:
            return go.Figure()

    @staticmethod
    def create_performance_chart(employee_data: pd.Series):
        try:
            categories = ["Impact", "Quality", "Collaboration", "Consistency"]

            scores = [
                employee_data.get("impact_score", 70),
                employee_data.get("quality_score", 75),
                employee_data.get("collaboration_score", 65),
                100 - abs(employee_data.get("visibility_score", 50) - 50)
            ]

            fig = go.Figure(data=go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor="rgba(88, 166, 255, 0.2)",
                line=dict(color="#58a6ff", width=2),
                name="Performance"
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor="#21262d",
                        linecolor="#30363d",
                        tickfont=dict(color="#8b949e", size=11)
                    ),
                    angularaxis=dict(
                        gridcolor="#21262d",
                        linecolor="#30363d",
                        tickfont=dict(color="#c9d1d9", size=12)
                    ),
                    bgcolor="#0d1117"
                ),
                showlegend=False,
                height=300,
                paper_bgcolor="#0d1117",
                font=dict(color="#c9d1d9", size=13),
                margin=dict(l=40, r=40, t=20, b=40)
            )

            return fig

        except Exception:
            return go.Figure()

    @staticmethod
    def create_activity_timeline(daily_data: pd.DataFrame, employee_name: str):
        try:
            if daily_data.empty:
                return None

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=daily_data["date"],
                y=daily_data["commits"],
                name="Commits",
                marker_color="#3fb950"
            ))

            fig.add_trace(go.Bar(
                x=daily_data["date"],
                y=daily_data["prs_created"],
                name="PRs Created",
                marker_color="#58a6ff"
            ))

            fig.update_layout(
                title=f"Activity Timeline - {employee_name}",
                xaxis_title="Date",
                yaxis_title="Count",
                height=300,
                barmode="group",
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


class LoginPage:

    @staticmethod
    def show():
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

    @staticmethod
    def show():
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

    @staticmethod
    def show(team_name: str):
        # Header with navigation
        UIComponents.github_header(f"Team: {team_name}", show_back=True)

        # Load team data
        team_size = st.session_state.user["teams"][team_name]["size"]
        team_data = DataManager.generate_team_data(team_name, team_size)

        # Team metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            UIComponents.metric_card("Team Size", team_size)
        with col2:
            avg_score = team_data["contribution_score"].mean()
            UIComponents.metric_card("Avg Contribution", f"{avg_score:.1f}")
        with col3:
            silent_count = team_data["is_silent_architect"].sum()
            UIComponents.metric_card("Silent Architects", silent_count)
        with col4:
            active_members = len(team_data[team_data["status"] == "active"])
            UIComponents.metric_card("Active Members", active_members)

        st.markdown("---")

        # GitHub-style tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Silent Architects",
            "Team Members",
            "Project Structure",
            "Contribution Roles",
            "Activity vs Impact"
        ])

        with tab1:
            TeamDashboard._show_silent_architects(team_data, team_name)
        with tab2:
            TeamDashboard._show_team_members(team_data, team_name)
        with tab3:
            TeamDashboard._show_project_structure(team_name)
        with tab4:
            TeamDashboard._show_contribution_roles(team_data, team_name)
        with tab5:
            TeamDashboard._show_activity_vs_impact(team_data, team_name)

    @staticmethod
    def _show_silent_architects(data: pd.DataFrame, team_name: str):
        silent_archs = data[data["is_silent_architect"]]

        if silent_archs.empty:
            st.info(f"No silent architects identified in {team_name}")
            return

        st.markdown(f"<h3>Silent Architects in {team_name}</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='color: #8b949e; font-size: 14px; margin-bottom: 16px;'>High-impact contributors with lower visibility</div>",
            unsafe_allow_html=True)

        # Date range filter
        st.markdown("#### Filter by Activity Period")
        start_date, end_date = UIComponents.date_range_filter("silent_arch")

        # Display silent architects
        for _, arch in silent_archs.iterrows():
            UIComponents.member_card(arch)

        # Statistics
        with st.expander("View Statistics"):
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_impact = silent_archs["impact_score"].mean()
                st.metric("Average Impact Score", f"{avg_impact:.1f}")
            with col2:
                avg_visibility = silent_archs["visibility_score"].mean()
                st.metric("Average Visibility Score", f"{avg_visibility:.1f}")
            with col3:
                avg_quality = silent_archs["quality_score"].mean()
                st.metric("Average Quality Score", f"{avg_quality:.1f}")

    @staticmethod
    def _show_team_members(data: pd.DataFrame, team_name: str):
        st.markdown(f"<h3>Team Members - {team_name}</h3>", unsafe_allow_html=True)

        # Date range and sorting
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            start_date, end_date = UIComponents.date_range_filter("team_members")

        with col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Contribution Score", "Impact Score", "Visibility Score", "Name", "Join Date"],
                key="team_sort"
            )

        with col3:
            search = st.text_input("Search members", placeholder="Type to search...")

        # Apply filters and sorting
        filtered_data = data.copy()

        if search:
            filtered_data = filtered_data[filtered_data["name"].str.contains(search, case=False) |
                                          filtered_data["username"].str.contains(search, case=False)]

        # Apply sorting
        sort_columns = {
            "Contribution Score": "contribution_score",
            "Impact Score": "impact_score",
            "Visibility Score": "visibility_score",
            "Name": "name",
            "Join Date": "join_date"
        }

        if sort_by in sort_columns:
            sort_col = sort_columns[sort_by]
            filtered_data = filtered_data.sort_values(sort_col, ascending=(sort_by != "Name"))

        # Display members
        for _, member in filtered_data.iterrows():
            UIComponents.member_card(member)

        # Export option
        if st.button("Export to CSV", type="secondary"):
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{team_name}_members_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    @staticmethod
    def _show_project_structure(team_name: str):
        st.markdown("<h3>Project Structure</h3>", unsafe_allow_html=True)

        projects = DataManager.generate_project_structure()

        if not projects:
            st.info("No project data available")
            return

        # Project selection and date filter
        col1, col2 = st.columns([1, 1])

        with col1:
            project_options = {pid: f"{proj['name']} ({proj['status']})" for pid, proj in projects.items()}
            selected_project = st.selectbox(
                "Select Project",
                options=list(project_options.values()),
                key="project_select"
            )

        with col2:
            start_date, end_date = UIComponents.date_range_filter("project")

        # Find selected project
        selected_pid = None
        for pid, proj in projects.items():
            if project_options[pid] == selected_project:
                selected_pid = pid
                break

        if not selected_pid:
            return

        project = projects[selected_pid]

        # Project header
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**{project['name']}**")
                st.markdown(f"<div style='color: #8b949e; font-size: 14px;'>{project['description']}</div>",
                            unsafe_allow_html=True)

            with col2:
                st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>Status</div>", unsafe_allow_html=True)
                status_color = "#3fb950" if project["status"] == "active" else "#d29922"
                st.markdown(
                    f"<div style='color: {status_color}; font-size: 14px; font-weight: 500;'>{project['status'].title()}</div>",
                    unsafe_allow_html=True)

            with col3:
                st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>Owner</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #c9d1d9; font-size: 14px;'>{project['owner']}</div>",
                            unsafe_allow_html=True)

        # Subdivisions table
        st.markdown("#### Subdivisions & Teams")

        table_data = []
        for sub_id, subdivision in project.get("subdivisions", {}).items():
            for team_id, team in subdivision.get("teams", {}).items():
                table_data.append({
                    "Division": subdivision["name"],
                    "Team": team["name"],
                    "Members": ", ".join(team["members"]),
                    "Tech Stack": ", ".join(team["tech_stack"]),
                    "Progress": team["progress"],
                    "Start Date": team["start_date"],
                    "End Date": team["end_date"],
                    "Commits": team["commits"],
                    "PRs Merged": team["prs_merged"]
                })

        if table_data:
            df_table = pd.DataFrame(table_data)

            # Add sorting
            sort_column = st.selectbox(
                "Sort table by",
                ["Progress", "Start Date", "End Date", "Commits", "Division"],
                key="project_sort"
            )

            if sort_column:
                df_table = df_table.sort_values(sort_column,
                                                ascending=(sort_column not in ["Progress", "Commits", "PRs Merged"]))

            st.dataframe(
                df_table,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Progress": st.column_config.ProgressColumn(
                        format="%d%%",
                        min_value=0,
                        max_value=100
                    ),
                    "Start Date": st.column_config.DateColumn(),
                    "End Date": st.column_config.DateColumn(),
                    "Commits": st.column_config.NumberColumn(),
                    "PRs Merged": st.column_config.NumberColumn()
                }
            )
        else:
            st.info("No team data available for this project")

    @staticmethod
    def _show_contribution_roles(data: pd.DataFrame, team_name: str):
        st.markdown(f"<h3>Contribution Roles - {team_name}</h3>", unsafe_allow_html=True)

        # Date filter
        start_date, end_date = UIComponents.date_range_filter("roles")

        # Role analysis
        role_analysis = data.groupby("role").agg({
            "contribution_score": ["mean", "count"],
            "impact_score": "mean",
            "visibility_score": "mean",
            "quality_score": "mean"
        }).round(2)

        # Flatten columns
        role_analysis.columns = ['_'.join(col).strip() for col in role_analysis.columns.values]
        role_analysis = role_analysis.reset_index()

        # Display table
        st.dataframe(
            role_analysis.rename(columns={
                "role": "Role",
                "contribution_score_mean": "Avg Contribution",
                "contribution_score_count": "Count",
                "impact_score_mean": "Avg Impact",
                "visibility_score_mean": "Avg Visibility",
                "quality_score_mean": "Avg Quality"
            }),
            use_container_width=True,
            hide_index=True
        )

        # Visualization
        col1, col2 = st.columns(2)

        with col1:
            # Role distribution
            role_counts = data["role"].value_counts()
            fig = px.pie(
                values=role_counts.values,
                names=role_counts.index,
                title="Role Distribution",
                color_discrete_sequence=["#3fb950", "#58a6ff", "#bc8cff", "#d29922"]
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(
                paper_bgcolor="#0d1117",
                font=dict(color="#c9d1d9"),
                showlegend=True,
                legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(size=12))
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Contribution by role
            fig = px.box(
                data,
                x="role",
                y="contribution_score",
                title="Contribution Score by Role",
                color="role",
                color_discrete_sequence=["#58a6ff", "#3fb950", "#d29922"]
            )
            fig.update_layout(
                xaxis_title="Role",
                yaxis_title="Contribution Score",
                paper_bgcolor="#0d1117",
                plot_bgcolor="#0d1117",
                font=dict(color="#c9d1d9"),
                showlegend=False
            )
            fig.update_xaxes(gridcolor="#21262d")
            fig.update_yaxes(gridcolor="#21262d")
            st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _show_activity_vs_impact(data: pd.DataFrame, team_name: str):
        st.markdown(f"<h3>Activity vs Impact - {team_name}</h3>", unsafe_allow_html=True)

        # Date filter
        start_date, end_date = UIComponents.date_range_filter("activity_impact")

        # Create visualization
        fig = VisualizationEngine.create_activity_impact_chart(data, team_name)
        st.plotly_chart(fig, use_container_width=True)

        # Quadrant analysis
        st.markdown("#### Quadrant Analysis")

        quadrants = {
            "High Impact, Low Visibility": len(data[(data["impact_score"] > 70) & (data["visibility_score"] < 55)]),
            "High Impact, High Visibility": len(data[(data["impact_score"] > 70) & (data["visibility_score"] >= 55)]),
            "Low Impact, High Visibility": len(data[(data["impact_score"] <= 70) & (data["visibility_score"] >= 55)]),
            "Low Impact, Low Visibility": len(data[(data["impact_score"] <= 70) & (data["visibility_score"] < 55)])
        }

        cols = st.columns(4)
        quadrant_colors = ["#3fb950", "#58a6ff", "#d29922", "#f85149"]

        for idx, ((name, count), color) in enumerate(zip(quadrants.items(), quadrant_colors)):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>{name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: {color}; font-size: 24px; font-weight: 600;'>{count}</div>",
                                unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='color: #6e7681; font-size: 12px;'>{count / len(data) * 100:.1f}% of team</div>",
                        unsafe_allow_html=True)


class EmployeeProfile:

    @staticmethod
    def show(employee_id: str, team_name: str):
        # Load data
        team_size = st.session_state.user["teams"][team_name]["size"]
        team_data = DataManager.generate_team_data(team_name, team_size)
        employee = team_data[team_data["employee_id"] == employee_id].iloc[0]

        # Header
        UIComponents.github_header("Employee Profile", show_back=True)

        # Profile header
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            # Avatar and basic info
            st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 16px; margin-bottom: 16px;'>
                <div style='width: 80px; height: 80px; border-radius: 50%; 
                            background-color: {employee.get('avatar_color', '#6e7681')};
                            display: flex; align-items: center; justify-content: center;
                            color: white; font-size: 32px; font-weight: 600;'>
                    {employee['name'][0]}
                </div>
                <div>
                    <div style='font-size: 24px; font-weight: 600; color: #c9d1d9;'>
                        {employee['name']}
                    </div>
                    <div style='font-size: 16px; color: #8b949e;'>
                        {employee['role']} • {team_name}
                    </div>
                    <div style='font-size: 14px; color: #6e7681; margin-top: 4px;'>
                        @{employee['username']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<div style='color: #8b949e; font-size: 14px;'>Joined {employee['join_date']} • {employee['tenure_months']} months tenure</div>",
                unsafe_allow_html=True)
            st.markdown(f"<div style='color: #8b949e; font-size: 14px;'>{employee['email']}</div>",
                        unsafe_allow_html=True)

        with col2:
            # Performance metrics
            st.markdown("#### Performance Metrics")

            metrics = [
                ("Contribution Score", employee["contribution_score"], "#c9d1d9"),
                ("Impact Score", employee["impact_score"], "#3fb950"),
                ("Quality Score", employee["quality_score"], "#58a6ff"),
                ("Visibility Score", employee["visibility_score"], "#d29922")
            ]

            for label, value, color in metrics:
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"<div style='color: #8b949e; font-size: 14px;'>{label}</div>", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"<div style='color: {color}; font-size: 18px; font-weight: 600;'>{value:.1f}</div>",
                                unsafe_allow_html=True)

        with col3:
            # Ranking and status
            with st.container(border=True):
                st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>Team Ranking</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='color: #c9d1d9; font-size: 32px; font-weight: 600; text-align: center;'>#{employee['team_rank']}</div>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<div style='color: #6e7681; font-size: 12px; text-align: center;'>of {len(team_data)}</div>",
                    unsafe_allow_html=True)

                if employee["is_silent_architect"]:
                    st.markdown(
                        f"<div style='background-color: rgba(63, 185, 80, 0.1); color: #3fb950; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500; text-align: center; margin-top: 8px;'>Silent Architect</div>",
                        unsafe_allow_html=True)

        st.markdown("---")

        # Detailed sections
        tab1, tab2, tab3 = st.tabs(["Performance Analysis", "Activity Details", "Projects & Skills"])

        with tab1:
            EmployeeProfile._show_performance_analysis(employee, team_data)

        with tab2:
            EmployeeProfile._show_activity_details(employee)

        with tab3:
            EmployeeProfile._show_projects_skills(employee)

    @staticmethod
    def _show_performance_analysis(employee: pd.Series, team_data: pd.DataFrame):
        col1, col2 = st.columns(2)

        with col1:
            # Radar chart
            fig = VisualizationEngine.create_performance_chart(employee)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Team comparison
            st.markdown("#### Team Comparison")

            comparisons = [
                ("Contribution Score", employee["contribution_score"], team_data["contribution_score"].mean()),
                ("Impact Score", employee["impact_score"], team_data["impact_score"].mean()),
                ("Quality Score", employee["quality_score"], team_data["quality_score"].mean()),
                ("Visibility Score", employee["visibility_score"], team_data["visibility_score"].mean())
            ]

            for label, emp_score, team_avg in comparisons:
                diff = emp_score - team_avg
                diff_color = "#3fb950" if diff > 0 else "#f85149" if diff < 0 else "#8b949e"
                diff_symbol = "+" if diff > 0 else "" if diff == 0 else ""

                with st.container(border=True):
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>{label}</div>",
                                    unsafe_allow_html=True)
                    with col_b:
                        st.markdown(
                            f"<div style='color: #c9d1d9; font-size: 16px; font-weight: 600;'>{emp_score:.1f}</div>",
                            unsafe_allow_html=True)
                    with col_c:
                        st.markdown(
                            f"<div style='color: {diff_color}; font-size: 14px;'>{diff_symbol}{diff:+.1f}</div>",
                            unsafe_allow_html=True)

        # Key metrics
        st.markdown("#### Key Metrics")

        metrics = [
            ("Total Commits", employee["commits"], "count"),
            ("Critical Bugs Fixed", employee["critical_bugs_fixed"], "count"),
            ("Features Delivered", employee["features_delivered"], "count"),
            ("Code Reviews", employee["code_reviews"], "count"),
            ("Mentoring Sessions", employee["mentoring_sessions"], "count"),
            ("PR Approval Rate", f"{employee['pr_approval_rate'] * 100:.1f}%", "percent"),
            ("Code Coverage", f"{employee['code_coverage'] * 100:.1f}%", "percent")
        ]

        cols = st.columns(4)
        for idx, (label, value, unit) in enumerate(metrics):
            with cols[idx % 4]:
                with st.container(border=True):
                    st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>{label}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #c9d1d9; font-size: 18px; font-weight: 600;'>{value}</div>",
                                unsafe_allow_html=True)

    @staticmethod
    def _show_activity_details(employee: pd.Series):
        st.markdown("#### Activity Timeline")

        # Date range filter
        start_date, end_date = UIComponents.date_range_filter("employee_activity")

        if start_date and end_date:
            # Generate activity data
            daily_data = DataManager.get_activity_data(employee["employee_id"], start_date, end_date)

            if not daily_data.empty:
                # Timeline chart
                fig = VisualizationEngine.create_activity_timeline(daily_data, employee["name"])
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

                # Activity statistics
                st.markdown("#### Activity Statistics")

                stats = {
                    "Total Commits": daily_data["commits"].sum(),
                    "Average Daily Commits": f"{daily_data['commits'].mean():.1f}",
                    "PRs Created": daily_data["prs_created"].sum(),
                    "PRs Reviewed": daily_data["prs_reviewed"].sum(),
                    "Average Hours Active": f"{daily_data['hours_active'].mean():.1f}",
                    "Total Bugs Fixed": daily_data["bugs_fixed"].sum()
                }

                cols = st.columns(3)
                for idx, (label, value) in enumerate(stats.items()):
                    with cols[idx % 3]:
                        with st.container(border=True):
                            st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>{label}</div>",
                                        unsafe_allow_html=True)
                            st.markdown(
                                f"<div style='color: #c9d1d9; font-size: 16px; font-weight: 600;'>{value}</div>",
                                unsafe_allow_html=True)
            else:
                st.info("No activity data available for the selected period")

    @staticmethod
    def _show_projects_skills(employee: pd.Series):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Skills & Expertise")

            skills = [
                ("Primary Technology", employee["primary_tech"], "#58a6ff"),
                ("Current Project", employee["current_project"], "#3fb950"),
                ("Code Quality", f"{employee['quality_score']:.1f}/100", "#58a6ff"),
                ("Collaboration", f"{employee['collaboration_score']:.1f}/100", "#bc8cff")
            ]

            for skill_name, value, color in skills:
                with st.container(border=True):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"<div style='color: #8b949e; font-size: 13px;'>{skill_name}</div>",
                                    unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f"<div style='color: {color}; font-size: 14px; font-weight: 600;'>{value}</div>",
                                    unsafe_allow_html=True)

        with col2:
            st.markdown("#### Recent Activity")

            # Simulated recent activity
            activities = [
                ("Fixed critical bug in authentication service", "2 hours ago"),
                ("Completed API gateway redesign", "1 day ago"),
                ("Mentored junior developer on best practices", "2 days ago"),
                ("Reviewed 5 pull requests", "3 days ago"),
                ("Optimized database queries", "4 days ago")
            ]

            for activity, time_ago in activities:
                with st.container(border=True):
                    st.markdown(f"<div style='color: #c9d1d9; font-size: 14px;'>{activity}</div>",
                                unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #6e7681; font-size: 12px;'>{time_ago}</div>",
                                unsafe_allow_html=True)


def main():
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

        elif st.session_state.current_team and not st.session_state.current_employee:
            TeamDashboard.show(st.session_state.current_team)

        elif st.session_state.current_employee:
            EmployeeProfile.show(st.session_state.current_employee, st.session_state.current_team)

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
