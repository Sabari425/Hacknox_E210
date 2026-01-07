import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import json
from typing import Dict, List, Tuple, Optional
import sys

st.set_page_config(
    page_title="Workforce Contribution Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* GitHub 2025 Dark Theme */
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #21262d;
    --border-color: #30363d;
    --text-primary: #f0f6fc;
    --text-secondary: #8b949e;
    --text-tertiary: #6e7681;
    --accent-blue: #58a6ff;
    --accent-green: #238636;
    --accent-red: #f85149;
    --accent-yellow: #e3b341;
    --accent-purple: #bc8cff;
}

/* Base styling */
.stApp {
    background-color: var(--bg-primary);
    color: var(--text-primary);
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

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
h1 { border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }

/* Cards and containers */
.stContainer, .stTabs, .stExpander {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
}

/* Metrics */
.stMetric {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 12px;
}
.stMetric label {
    color: var(--text-secondary) !important;
}
.stMetric div {
    color: var(--text-primary) !important;
}

/* Buttons */
.stButton button {
    background-color: var(--accent-green) !important;
    color: white !important;
    border: 1px solid var(--accent-green) !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    background-color: #2ea043 !important;
    border-color: #2ea043 !important;
    transform: translateY(-1px);
}
.stButton button[kind="secondary"] {
    background-color: var(--bg-tertiary) !important;
    border-color: var(--border-color) !important;
    color: var(--text-primary) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: var(--bg-secondary);
}
.stTabs [data-baseweb="tab"] {
    background-color: var(--bg-tertiary);
    border-radius: 6px 6px 0 0;
    padding: 8px 16px;
    color: var(--text-secondary);
    border: 1px solid transparent;
}
.stTabs [aria-selected="true"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    border-bottom-color: var(--bg-primary) !important;
}

/* Dataframes */
.dataframe {
    background-color: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
}
.dataframe th {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
}
.dataframe td {
    border-color: var(--border-color) !important;
    color: var(--text-secondary) !important;
}

/* Inputs */
.stTextInput input, .stSelectbox select, .stMultiselect div {
    background-color: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    border-radius: 6px !important;
}
.stTextInput label, .stSelectbox label, .stMultiselect label {
    color: var(--text-secondary) !important;
}

/* Progress bars */
.stProgress > div > div {
    background-color: var(--accent-green) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
}

/* Success/Error/Info/Warning */
.stAlert {
    border-radius: 6px !important;
    border: 1px solid var(--border-color) !important;
}
.stAlert[data-kind="success"] {
    background-color: rgba(35, 134, 54, 0.1) !important;
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
    background-color: rgba(227, 179, 65, 0.1) !important;
    border-color: var(--accent-yellow) !important;
}

/* Custom animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeIn 0.3s ease-out;
}

/* GitHub-like badges */
.badge {
    display: inline-block;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 500;
    border-radius: 12px;
    margin: 2px;
}
.badge-green { background-color: var(--accent-green); color: white; }
.badge-blue { background-color: var(--accent-blue); color: white; }
.badge-red { background-color: var(--accent-red); color: white; }
.badge-yellow { background-color: var(--accent-yellow); color: black; }
.badge-purple { background-color: var(--accent-purple); color: white; }

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

/* Loading animation */
.loading-pulse {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: var(--accent-blue);
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.7; }
    50% { transform: scale(1); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.7; }
}
</style>
""", unsafe_allow_html=True)

class DataManager:
    """Centralized data management with error handling"""

    @staticmethod
    @st.cache_data(ttl=300)
    def generate_team_data(_team_name: str, size: int) -> pd.DataFrame:
        """Generate realistic team data with error handling"""
        try:
            # Fixed seed for consistency
            random.seed(hash(_team_name) % 10000)
            np.random.seed(hash(_team_name) % 10000)

            # Employee definitions
            first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley",
                           "Avery", "Quinn", "Blake", "Hayden", "Drew", "Cameron",
                           "Jamie", "Robin", "Skyler", "Dakota", "Rowan", "Sage"]

            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                          "Miller", "Davis", "Rodriguez", "Martinez", "Lee", "Gonzalez"]

            roles = ["Senior Developer", "Junior Developer", "Tech Lead",
                     "Software Architect", "DevOps Engineer", "QA Engineer",
                     "Product Manager", "Scrum Master"]

            employees = []

            for i in range(size):
                emp_id = f"{_team_name[:3].upper()}{i + 1:03d}"
                first = random.choice(first_names)
                last = random.choice(last_names)
                role = random.choice(roles)

                # Generate base metrics with realistic distributions
                base_performance = np.random.beta(2, 2)  # Bell curve distribution

                # Activity metrics (visibility)
                commits = int(np.random.gamma(shape=2, scale=15) * base_performance)
                slack_messages = int(np.random.gamma(shape=1.5, scale=50) * base_performance)
                meetings = int(np.random.gamma(shape=1, scale=20) * base_performance)

                # Impact metrics (actual value)
                critical_fixes = int(np.random.poisson(8) * base_performance)
                features = int(np.random.poisson(5) * base_performance)
                design_docs = int(np.random.poisson(3) * base_performance)
                code_reviews = int(np.random.gamma(shape=2, scale=10) * base_performance)
                mentoring = int(np.random.poisson(4) * (1.5 if "Senior" in role or "Lead" in role else 1))

                # Calculate scores using stable algorithm
                visibility_score = min(100, (
                        np.log1p(commits) * 15 +
                        np.log1p(slack_messages) * 10 +
                        meetings * 0.5
                ))

                impact_score = min(100, (
                        critical_fixes * 3 +
                        features * 4 +
                        design_docs * 5 +
                        np.log1p(code_reviews) * 10 +
                        mentoring * 2
                ))

                # Quality metrics
                pr_approval = np.clip(base_performance * 0.8 + np.random.normal(0.1, 0.05), 0.6, 0.99)
                bug_rate = np.clip((1 - base_performance) * 0.3 + np.random.normal(0.05, 0.02), 0.01, 0.2)

                # Determine silent architect
                visibility_percentile = visibility_score / 100
                impact_percentile = impact_score / 100
                is_silent_architect = (impact_percentile > 0.75 and
                                       visibility_percentile < 0.5 and
                                       pr_approval > 0.85)

                # Contribution score (scale-invariant algorithm)
                # Normalize within team using percentile ranks
                contribution_raw = (
                        impact_score * 0.4 +
                        (pr_approval * 100) * 0.3 +
                        (100 - bug_rate * 500) * 0.2 +
                        np.log1p(mentoring + code_reviews) * 10 * 0.1
                )

                employees.append({
                    "employee_id": emp_id,
                    "name": f"{first} {last}",
                    "email": f"{first.lower()}.{last.lower()}@company.com",
                    "role": role,
                    "team": _team_name,
                    "join_date": (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d"),

                    # Activity metrics
                    "commits": commits,
                    "slack_messages": slack_messages,
                    "meetings_attended": meetings,
                    "prs_created": int(commits * 0.3),
                    "prs_reviewed": code_reviews,

                    # Impact metrics
                    "critical_bugs_fixed": critical_fixes,
                    "features_delivered": features,
                    "design_docs_created": design_docs,
                    "mentoring_sessions": mentoring,
                    "code_reviews": code_reviews,

                    # Quality metrics
                    "pr_approval_rate": pr_approval,
                    "bug_introduction_rate": bug_rate,
                    "code_coverage": np.clip(base_performance * 0.8 + np.random.normal(0.1, 0.05), 0.6, 0.95),

                    # Scores
                    "visibility_score": round(visibility_score, 1),
                    "impact_score": round(impact_score, 1),
                    "quality_score": round(pr_approval * 100 * 0.7 + (1 - bug_rate) * 100 * 0.3, 1),
                    "collaboration_score": round(np.log1p(mentoring + code_reviews) * 20, 1),
                    "raw_contribution": round(contribution_raw, 1),

                    # Flags
                    "is_silent_architect": is_silent_architect,
                    "tenure_months": random.randint(6, 60),

                    # Additional info
                    "primary_tech": random.choice(["Python", "Java", "JavaScript", "Go", "Rust"]),
                    "current_project": random.choice(["Platform Modernization", "API Gateway", "Database Migration",
                                                      "Mobile App", "Analytics Platform"])
                })

            df = pd.DataFrame(employees)

            # Apply scale-invariant ranking
            df = DataManager._calculate_scale_invariant_scores(df)

            return df

        except Exception as e:
            st.error(f"Error generating team data: {str(e)}")
            # Return minimal dummy data
            return pd.DataFrame([{
                "employee_id": "ERR001",
                "name": "Error - Check Data",
                "role": "System",
                "team": _team_name,
                "visibility_score": 0,
                "impact_score": 0,
                "raw_contribution": 0
            }])

    @staticmethod
    def _calculate_scale_invariant_scores(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate scores that are stable across team sizes"""
        try:
            # Normalize raw scores within team using percentiles
            for col in ['visibility_score', 'impact_score', 'quality_score',
                        'collaboration_score', 'raw_contribution']:
                if col in df.columns:
                    df[f'{col}_percentile'] = df[col].rank(pct=True)

            # Final contribution score (0-100 scale)
            # Weighted combination of percentiles ensures scale invariance
            weights = {
                'impact_score_percentile': 0.35,
                'quality_score_percentile': 0.25,
                'collaboration_score_percentile': 0.20,
                'visibility_score_percentile': 0.10,
                'raw_contribution_percentile': 0.10
            }

            df['contribution_score'] = 0
            for col, weight in weights.items():
                if col in df.columns:
                    df['contribution_score'] += df[col] * weight * 100

            # Round and sort
            df['contribution_score'] = df['contribution_score'].round(1)
            df = df.sort_values('contribution_score', ascending=False)
            df['team_rank'] = range(1, len(df) + 1)

            return df

        except Exception:
            # Fallback to simple ranking
            df['contribution_score'] = df['raw_contribution']
            df = df.sort_values('contribution_score', ascending=False)
            df['team_rank'] = range(1, len(df) + 1)
            return df

    @staticmethod
    @st.cache_data(ttl=600)
    def generate_project_structure():
        """Generate detailed project structure"""
        try:
            projects = {
                "Platform Modernization": {
                    "description": "Migrating legacy monolith to microservices architecture",
                    "status": "active",
                    "priority": "high",
                    "start_date": "2024-01-15",
                    "eta": "2024-12-31",
                    "budget": "$2.5M",
                    "subdivisions": {
                        "Backend Services": {
                            "API Gateway": {
                                "members": ["Alex Smith", "Jordan Johnson"],
                                "tech_stack": ["Go", "gRPC", "Redis"],
                                "completed": 75,
                                "last_updated": "2024-06-15"
                            },
                            "User Service": {
                                "members": ["Taylor Williams"],
                                "tech_stack": ["Python", "FastAPI", "PostgreSQL"],
                                "completed": 60,
                                "last_updated": "2024-06-10"
                            },
                            "Payment Service": {
                                "members": ["Morgan Brown", "Casey Jones"],
                                "tech_stack": ["Java", "Spring Boot", "MySQL"],
                                "completed": 45,
                                "last_updated": "2024-06-05"
                            }
                        },
                        "Frontend Applications": {
                            "Admin Dashboard": {
                                "members": ["Riley Garcia", "Avery Miller"],
                                "tech_stack": ["React", "TypeScript", "Tailwind"],
                                "completed": 85,
                                "last_updated": "2024-06-18"
                            },
                            "Customer Portal": {
                                "members": ["Quinn Davis"],
                                "tech_stack": ["Vue.js", "JavaScript", "Bootstrap"],
                                "completed": 70,
                                "last_updated": "2024-06-12"
                            }
                        },
                        "DevOps & Infrastructure": {
                            "CI/CD Pipeline": {
                                "members": ["Blake Rodriguez"],
                                "tech_stack": ["Docker", "Kubernetes", "GitHub Actions"],
                                "completed": 90,
                                "last_updated": "2024-06-20"
                            },
                            "Monitoring & Logging": {
                                "members": ["Hayden Martinez", "Drew Lee"],
                                "tech_stack": ["Prometheus", "Grafana", "ELK Stack"],
                                "completed": 65,
                                "last_updated": "2024-06-08"
                            }
                        }
                    }
                },
                "API Gateway Redesign": {
                    "description": "Redesigning API gateway for improved performance and security",
                    "status": "planning",
                    "priority": "medium",
                    "start_date": "2024-07-01",
                    "eta": "2024-10-31",
                    "budget": "$800K",
                    "subdivisions": {
                        "API Design": {
                            "REST APIs": {
                                "members": ["Alex Smith", "Morgan Brown"],
                                "tech_stack": ["OpenAPI", "Swagger"],
                                "completed": 30,
                                "last_updated": "2024-06-01"
                            },
                            "GraphQL APIs": {
                                "members": ["Taylor Williams"],
                                "tech_stack": ["GraphQL", "Apollo"],
                                "completed": 20,
                                "last_updated": "2024-05-28"
                            }
                        },
                        "Security Implementation": {
                            "Authentication": {
                                "members": ["Jordan Johnson"],
                                "tech_stack": ["OAuth2", "JWT", "Keycloak"],
                                "completed": 40,
                                "last_updated": "2024-06-05"
                            },
                            "Rate Limiting": {
                                "members": ["Casey Jones"],
                                "tech_stack": ["Redis", "Nginx"],
                                "completed": 25,
                                "last_updated": "2024-05-30"
                            }
                        }
                    }
                }
            }
            return projects
        except Exception:
            return {"Error": {"description": "Failed to load project structure"}}

    @staticmethod
    def get_daily_activity(employee_id: str) -> pd.DataFrame:
        """Generate daily activity data"""
        try:
            days = 30
            dates = [datetime.now() - timedelta(days=i) for i in range(days)]
            dates.reverse()

            activities = []
            for date in dates:
                is_weekend = date.weekday() >= 5
                base = 0.3 if is_weekend else 1.0

                activities.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "commits": int(np.random.poisson(3) * base),
                    "prs_created": int(np.random.poisson(1.5) * base),
                    "prs_reviewed": int(np.random.poisson(2) * base),
                    "code_reviews": int(np.random.poisson(3) * base),
                    "hours_active": round(np.random.uniform(4, 9) * base, 1),
                    "slack_messages": int(np.random.poisson(25) * base),
                    "meetings": int(np.random.poisson(2) * base),
                    "bugs_fixed": int(np.random.poisson(1) * base),
                    "is_weekend": is_weekend,
                    "day_of_week": date.strftime("%A")
                })

            return pd.DataFrame(activities)
        except Exception:
            return pd.DataFrame()  # Return empty dataframe on error

class AuthenticationSystem:
    """Secure authentication system"""

    USER_DB = {
        "manager_a": {
            "password": "manager123",
            "name": "Sarah Johnson",
            "title": "Senior Engineering Manager",
            "department": "Platform Engineering",
            "access_level": "manager",
            "teams": {
                "Team A": {"size": 12, "focus": "Backend Services"},
                "Team B": {"size": 8, "focus": "Frontend Development"}
            }
        },
        "manager_b": {
            "password": "manager456",
            "name": "Michael Chen",
            "title": "Product Engineering Manager",
            "department": "Product Development",
            "access_level": "manager",
            "teams": {
                "Team C": {"size": 15, "focus": "Mobile Applications"},
                "Team D": {"size": 10, "focus": "Data Platform"}
            }
        }
    }

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict]:
        """Authenticate user with error handling"""
        try:
            if username in AuthenticationSystem.USER_DB:
                if AuthenticationSystem.USER_DB[username]["password"] == password:
                    return AuthenticationSystem.USER_DB[username]
            return None
        except Exception:
            return None

class VisualizationEngine:
    """Create professional visualizations"""

    @staticmethod
    def create_activity_impact_chart(data: pd.DataFrame, team_name: str) -> go.Figure:
        """Create Activity vs Impact scatter plot"""
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
                        size=15,
                        color="#238636",  # GitHub green
                        symbol="diamond",
                        line=dict(width=2, color="white")
                    ),
                    text=silent_data["name"],
                    hovertemplate=(
                            "<b>%{text}</b><br>"
                            "Role: " + silent_data["role"] + "<br>"
                                                             "Visibility: %{x:.1f}<br>"
                                                             "Impact: %{y:.1f}<br>"
                                                             "Contribution: " + silent_data[
                                "contribution_score"].astype(str) + "<extra></extra>"
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
                        size=12,
                        color="#58a6ff",  # GitHub blue
                        opacity=0.8,
                        line=dict(width=1, color="white")
                    ),
                    text=other_data["name"],
                    hovertemplate=(
                            "<b>%{text}</b><br>"
                            "Role: " + other_data["role"] + "<br>"
                                                            "Visibility: %{x:.1f}<br>"
                                                            "Impact: %{y:.1f}<br>"
                                                            "Contribution: " + other_data["contribution_score"].astype(
                        str) + "<extra></extra>"
                    )
                ))

            # Add quadrant lines
            fig.add_hline(y=75, line_dash="dash", line_color="#6e7681", line_width=1)
            fig.add_vline(x=50, line_dash="dash", line_color="#6e7681", line_width=1)

            # Add quadrant labels
            fig.add_annotation(x=25, y=90, text="Silent Architects", showarrow=False, font=dict(color="#238636"))
            fig.add_annotation(x=75, y=90, text="Visible Leaders", showarrow=False, font=dict(color="#58a6ff"))
            fig.add_annotation(x=75, y=40, text="Busy Workers", showarrow=False, font=dict(color="#e3b341"))
            fig.add_annotation(x=25, y=40, text="Under Performers", showarrow=False, font=dict(color="#f85149"))

            fig.update_layout(
                title=f"Activity vs Impact Analysis - {team_name}",
                xaxis_title="Visibility Score (Perceived Activity)",
                yaxis_title="Impact Score (Actual Contribution)",
                height=500,
                hovermode="closest",
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font=dict(color="#f0f6fc"),
                legend=dict(
                    bgcolor="#161b22",
                    bordercolor="#30363d",
                    borderwidth=1
                )
            )

            fig.update_xaxes(gridcolor="#21262d", zerolinecolor="#30363d")
            fig.update_yaxes(gridcolor="#21262d", zerolinecolor="#30363d")

            return fig

        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
            return go.Figure()  # Return empty figure

    @staticmethod
    def create_performance_radar(employee_data: pd.Series) -> go.Figure:
        """Create radar chart for performance breakdown"""
        try:
            categories = ["Impact", "Quality", "Collaboration", "Visibility", "Consistency"]

            scores = [
                employee_data.get("impact_score", 70),
                employee_data.get("quality_score", 75),
                employee_data.get("collaboration_score", 65),
                employee_data.get("visibility_score", 50),
                100 - abs(employee_data.get("visibility_score", 50) - 50)  # Consistency proxy
            ]

            fig = go.Figure(data=go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor="rgba(88, 166, 255, 0.3)",
                line=dict(color="#58a6ff", width=2),
                name="Performance"
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor="#21262d",
                        linecolor="#30363d"
                    ),
                    angularaxis=dict(
                        gridcolor="#21262d",
                        linecolor="#30363d"
                    ),
                    bgcolor="#0d1117"
                ),
                showlegend=False,
                title="Performance Breakdown",
                height=300,
                paper_bgcolor="#0d1117",
                font=dict(color="#f0f6fc")
            )

            return fig

        except Exception:
            return go.Figure()

    @staticmethod
    def create_activity_timeline(daily_data: pd.DataFrame, employee_name: str) -> go.Figure:
        """Create activity timeline chart"""
        try:
            if daily_data.empty:
                return None

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=daily_data["date"],
                y=daily_data["commits"],
                mode="lines+markers",
                name="Commits",
                line=dict(color="#238636", width=2),
                marker=dict(size=6)
            ))

            fig.add_trace(go.Scatter(
                x=daily_data["date"],
                y=daily_data["prs_created"],
                mode="lines+markers",
                name="PRs Created",
                line=dict(color="#58a6ff", width=2),
                marker=dict(size=6)
            ))

            fig.add_trace(go.Scatter(
                x=daily_data["date"],
                y=daily_data["prs_reviewed"],
                mode="lines+markers",
                name="PRs Reviewed",
                line=dict(color="#bc8cff", width=2),
                marker=dict(size=6)
            ))

            fig.update_layout(
                title=f"Activity Timeline - {employee_name}",
                xaxis_title="Date",
                yaxis_title="Activity Count",
                height=300,
                hovermode="x unified",
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font=dict(color="#f0f6fc"),
                legend=dict(
                    bgcolor="#161b22",
                    bordercolor="#30363d",
                    borderwidth=1
                )
            )

            fig.update_xaxes(gridcolor="#21262d")
            fig.update_yaxes(gridcolor="#21262d")

            return fig

        except Exception:
            return None

class LoginPage:
    """Login page with GitHub-like styling"""

    @staticmethod
    def show():
        """Display login page"""
        st.markdown("""
        <div style='max-width: 400px; margin: 100px auto; padding: 40px; 
                    background-color: #161b22; border: 1px solid #30363d; 
                    border-radius: 6px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);'>
            <h2 style='text-align: center; color: #f0f6fc; margin-bottom: 30px;'>
                Workforce Contribution Monitor
            </h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            with st.container():
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="Enter username")
                    password = st.text_input("Password", type="password", placeholder="Enter password")

                    submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)

                    if submit:
                        with st.spinner("Authenticating..."):
                            time.sleep(0.5)
                            user = AuthenticationSystem.authenticate(username, password)
                            if user:
                                st.session_state.user = user
                                st.session_state.username = username
                                st.session_state.authenticated = True
                                st.session_state.current_team = None
                                st.session_state.current_employee = None
                                st.rerun()
                            else:
                                st.error("Invalid username or password")

                st.markdown("---")
                st.markdown("""
                <div style='text-align: center; color: #8b949e;'>
                    <strong>Demo Credentials:</strong><br>
                    • manager_a / manager123<br>
                    • manager_b / manager456
                </div>
                """, unsafe_allow_html=True)


class ManagerDashboard:
    """Manager dashboard showing all teams"""

    @staticmethod
    def show():
        """Display manager dashboard"""
        try:
            st.title(f"Manager Dashboard")
            st.markdown(f"**{st.session_state.user['name']}** | *{st.session_state.user['title']}*")
            st.markdown(f"Department: {st.session_state.user['department']}")

            st.markdown("---")

            st.subheader("Your Teams")

            # Display teams
            teams = st.session_state.user["teams"]
            cols = st.columns(min(len(teams), 3))

            for idx, (team_name, team_info) in enumerate(teams.items()):
                with cols[idx % len(cols)]:
                    with st.container(border=True):
                        st.markdown(f"### {team_name}")
                        st.markdown(f"**Focus:** {team_info['focus']}")
                        st.markdown(f"**Team Size:** {team_info['size']} members")

                        if st.button(f"Analyze Team", key=f"btn_{team_name}", use_container_width=True):
                            st.session_state.current_team = team_name
                            st.rerun()

            st.markdown("---")

            # Quick stats
            col1, col2, col3 = st.columns(3)
            total_teams = len(teams)
            total_members = sum(team["size"] for team in teams.values())

            with col1:
                st.metric("Total Teams", total_teams)
            with col2:
                st.metric("Total Members", total_members)
            with col3:
                if st.button("Sign Out", type="secondary", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

        except Exception as e:
            st.error(f"Error loading dashboard: {str(e)}")
            st.info("Please refresh the page or contact support.")


class TeamDashboard:
    """Team-specific analysis dashboard"""

    @staticmethod
    def show(team_name: str):
        """Display team dashboard"""
        try:
            # Navigation
            col1, col2 = st.columns([6, 1])
            with col1:
                st.title(f"Team Analysis: {team_name}")
            with col2:
                if st.button("← Back", type="secondary", use_container_width=True):
                    st.session_state.current_team = None
                    st.session_state.current_employee = None
                    st.rerun()

            st.markdown("---")

            # Load team data
            team_size = st.session_state.user["teams"][team_name]["size"]
            team_data = DataManager.generate_team_data(team_name, team_size)

            # Team overview metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_contrib = team_data["contribution_score"].mean()
                st.metric("Avg Contribution", f"{avg_contrib:.1f}")
            with col2:
                silent_count = team_data["is_silent_architect"].sum()
                st.metric("Silent Architects", silent_count)
            with col3:
                top_score = team_data["contribution_score"].max()
                st.metric("Top Score", f"{top_score:.1f}")
            with col4:
                visibility_gap = abs(team_data["visibility_score"] - team_data["impact_score"]).mean()
                st.metric("Avg Visibility Gap", f"{visibility_gap:.1f}")

            st.markdown("---")

            # Main tabs following exact structure
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Silent Architects",
                "Team Members Ranking",
                "Project Structure",
                "Contribution Roles",
                "Activity vs Impact"
            ])

            with tab1:
                TeamDashboard._show_silent_architects(team_data, team_name)
            with tab2:
                TeamDashboard._show_team_ranking(team_data, team_name)
            with tab3:
                TeamDashboard._show_project_structure(team_name)
            with tab4:
                TeamDashboard._show_contribution_roles(team_data, team_name)
            with tab5:
                TeamDashboard._show_activity_vs_impact(team_data, team_name)

        except Exception as e:
            st.error(f"Error loading team data: {str(e)}")
            st.info("The system will attempt to recover...")
            time.sleep(1)
            st.session_state.current_team = None
            st.rerun()

    @staticmethod
    def _show_silent_architects(data: pd.DataFrame, team_name: str):
        """Show silent architects section"""
        silent_archs = data[data["is_silent_architect"]]

        if silent_archs.empty:
            st.info(f"No silent architects identified in {team_name}")
            st.markdown("""
            **What are Silent Architects?**
            These are team members with:
            - High impact scores (>75)
            - Lower visibility scores (<50)
            - Excellent quality metrics
            - Often overlooked in traditional reviews
            """)
            return

        st.subheader(f"Silent Architects in {team_name}")
        st.markdown("*High-impact contributors who may be overlooked due to lower visibility*")

        for _, arch in silent_archs.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 2, 1])

                with col1:
                    st.markdown(f"### {arch['name']}")
                    st.markdown(f"**{arch['role']}**")
                    st.markdown(f"*{arch['current_project']}*")

                    # Skills
                    st.markdown(f"**Primary Skill:** `{arch['primary_tech']}`")

                with col2:
                    # Scores
                    st.markdown("**Performance Scores:**")
                    st.markdown(f"Impact: **{arch['impact_score']}**")
                    st.markdown(f"Visibility: **{arch['visibility_score']}**")
                    st.markdown(f"Quality: **{arch['quality_score']}**")
                    st.markdown(f"Contribution: **{arch['contribution_score']}**")

                with col3:
                    st.markdown("**Team Rank**")
                    st.markdown(f"# {arch['team_rank']}")

                    if st.button("View Profile", key=f"profile_{arch['employee_id']}", use_container_width=True):
                        st.session_state.current_employee = arch['employee_id']
                        st.rerun()

        # Insights
        with st.expander("📈 Silent Architects Insights"):
            st.markdown("""
            **Key Characteristics:**
            1. **High Impact Work**: Fix critical bugs, design complex systems
            2. **Low Visibility**: Less active in meetings/chats, focus on deep work
            3. **High Quality**: Excellent code reviews, low bug introduction
            4. **Team Mentors**: Often help others without seeking recognition

            **Recommendations:**
            - Ensure recognition in performance reviews
            - Consider for technical leadership roles
            - Protect their focus time from interruptions
            """)

    @staticmethod
    def _show_team_ranking(data: pd.DataFrame, team_name: str):
        """Show team ranking table"""
        st.subheader(f"Team Members Ranking - {team_name}")

        # Filters
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("Search by name", placeholder="Type to filter...", key="search_ranking")
        with col2:
            role_filter = st.multiselect(
                "Filter by role",
                options=data["role"].unique(),
                default=[],
                key="role_filter"
            )

        # Apply filters
        filtered_data = data.copy()
        if search:
            filtered_data = filtered_data[filtered_data["name"].str.contains(search, case=False)]
        if role_filter:
            filtered_data = filtered_data[filtered_data["role"].isin(role_filter)]

        # Display table with config
        display_columns = {
            "team_rank": st.column_config.NumberColumn("Rank", width="small"),
            "name": "Name",
            "role": "Role",
            "contribution_score": st.column_config.ProgressColumn(
                "Contribution",
                format="%.1f",
                min_value=0,
                max_value=100,
                width="medium"
            ),
            "impact_score": st.column_config.NumberColumn("Impact", format="%.1f"),
            "visibility_score": st.column_config.NumberColumn("Visibility", format="%.1f"),
            "commits": "Commits",
            "critical_bugs_fixed": "Critical Fixes"
        }

        try:
            st.dataframe(
                filtered_data[list(display_columns.keys())],
                column_config=display_columns,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )

            # Show selected row details
            if st.session_state.get("dataframe_selection"):
                selected_idx = st.session_state.dataframe_selection["selection"]["rows"][0]
                selected_emp = filtered_data.iloc[selected_idx]

                with st.expander(f"Details for {selected_emp['name']}", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Current Project", selected_emp["current_project"])
                        st.metric("PR Approval Rate", f"{selected_emp['pr_approval_rate'] * 100:.1f}%")
                    with col2:
                        st.metric("Code Reviews", selected_emp["code_reviews"])
                        st.metric("Mentoring Sessions", selected_emp["mentoring_sessions"])

                    if st.button("View Full Profile", key=f"full_{selected_emp['employee_id']}"):
                        st.session_state.current_employee = selected_emp["employee_id"]
                        st.rerun()

        except Exception:
            # Fallback display
            st.dataframe(
                filtered_data[["team_rank", "name", "role", "contribution_score"]],
                use_container_width=True,
                hide_index=True
            )

    @staticmethod
    def _show_project_structure(team_name: str):
        """Show project structure with sorting options"""
        st.subheader(f"Project Structure - {team_name}")

        projects = DataManager.generate_project_structure()

        # Sorting options
        sort_by = st.selectbox(
            "Sort Projects By",
            ["Priority", "Status", "Progress", "Alphabetical"],
            key="project_sort"
        )

        # Apply sorting
        if sort_by == "Priority":
            project_list = list(projects.items())
        elif sort_by == "Status":
            project_list = sorted(projects.items(), key=lambda x: x[1].get("status", ""))
        elif sort_by == "Progress":
            # Need to calculate overall progress
            project_list = list(projects.items())
        else:  # Alphabetical
            project_list = sorted(projects.items(), key=lambda x: x[0])

        for project_name, project_data in project_list:
            with st.expander(f"{project_name} - {project_data.get('description', 'No description')}", expanded=True):

                # Project header
                col1, col2, col3 = st.columns(3)
                with col1:
                    status_color = {
                        "active": "#238636",
                        "planning": "#e3b341",
                        "completed": "#58a6ff"
                    }.get(project_data.get("status", ""), "#8b949e")
                    st.markdown(
                        f"**Status:** <span style='color:{status_color}'>{project_data.get('status', 'Unknown')}</span>",
                        unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**Priority:** {project_data.get('priority', 'Not set')}")
                with col3:
                    st.markdown(f"**ETA:** {project_data.get('eta', 'Not set')}")

                # Progress bar
                overall_progress = project_data.get("completion", 0)
                if not overall_progress:
                    # Calculate from subdivisions
                    total_tasks = 0
                    completed_tasks = 0
                    for division in project_data.get("subdivisions", {}).values():
                        for task in division.values():
                            total_tasks += 1
                            completed_tasks += task.get("completed", 0) / 100
                    overall_progress = int((completed_tasks / max(total_tasks, 1)) * 100)

                st.progress(overall_progress / 100, text=f"Overall Progress: {overall_progress}%")

                # Subdivisions table
                st.markdown("### Subdivisions & Members")

                # Prepare table data
                table_data = []
                for division_name, tasks in project_data.get("subdivisions", {}).items():
                    for task_name, task_details in tasks.items():
                        table_data.append({
                            "Division": division_name,
                            "Task": task_name,
                            "Members": ", ".join(task_details.get("members", [])),
                            "Tech Stack": ", ".join(task_details.get("tech_stack", [])),
                            "Progress": f"{task_details.get('completed', 0)}%",
                            "Last Updated": task_details.get("last_updated", "Unknown")
                        })

                if table_data:
                    st.dataframe(
                        pd.DataFrame(table_data),
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Progress": st.column_config.ProgressColumn(
                                format="%d%%",
                                min_value=0,
                                max_value=100
                            )
                        }
                    )
                else:
                    st.info("No subdivision data available for this project")

                # Member contributions visualization
                if table_data:
                    st.markdown("### Member Contributions")

                    # Extract all members and their tasks
                    member_tasks = {}
                    for row in table_data:
                        members = row["Members"].split(", ")
                        for member in members:
                            if member:
                                if member not in member_tasks:
                                    member_tasks[member] = []
                                member_tasks[member].append(row["Task"])

                    # Display member cards
                    cols = st.columns(3)
                    member_list = list(member_tasks.items())

                    for idx, (member, tasks) in enumerate(member_tasks.items()):
                        with cols[idx % 3]:
                            with st.container(border=True):
                                st.markdown(f"**{member}**")
                                st.markdown(f"*{len(tasks)} task(s)*")

                                # Show first few tasks
                                for task in tasks[:2]:
                                    st.markdown(f"- {task}")
                                if len(tasks) > 2:
                                    st.markdown(f"*+{len(tasks) - 2} more...*")

    @staticmethod
    def _show_contribution_roles(data: pd.DataFrame, team_name: str):
        """Show contribution analysis by roles"""
        st.subheader(f"Contribution Roles Analysis - {team_name}")

        # Role-based metrics
        role_metrics = data.groupby("role").agg({
            "contribution_score": ["mean", "std", "count"],
            "impact_score": "mean",
            "visibility_score": "mean",
            "quality_score": "mean"
        }).round(2)

        # Flatten column names
        role_metrics.columns = ['_'.join(col).strip() for col in role_metrics.columns.values]
        role_metrics = role_metrics.reset_index()

        # Display metrics
        st.dataframe(
            role_metrics.rename(columns={
                "role": "Role",
                "contribution_score_mean": "Avg Contribution",
                "contribution_score_std": "Std Dev",
                "contribution_score_count": "Count",
                "impact_score_mean": "Avg Impact",
                "visibility_score_mean": "Avg Visibility",
                "quality_score_mean": "Avg Quality"
            }),
            use_container_width=True,
            hide_index=True
        )

        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Role distribution pie chart
            role_counts = data["role"].value_counts()
            fig = px.pie(
                values=role_counts.values,
                names=role_counts.index,
                title="Role Distribution",
                color_discrete_sequence=["#238636", "#58a6ff", "#bc8cff", "#e3b341", "#f85149"]
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(
                paper_bgcolor="#0d1117",
                font=dict(color="#f0f6fc"),
                showlegend=True,
                legend=dict(bgcolor="#161b22", bordercolor="#30363d")
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Box plot of contributions by role
            fig = px.box(
                data,
                x="role",
                y="contribution_score",
                title="Contribution Score Distribution by Role",
                color="role",
                color_discrete_sequence=["#58a6ff", "#238636", "#e3b341", "#bc8cff"]
            )
            fig.update_layout(
                xaxis_title="Role",
                yaxis_title="Contribution Score",
                paper_bgcolor="#0d1117",
                plot_bgcolor="#0d1117",
                font=dict(color="#f0f6fc"),
                showlegend=False
            )
            fig.update_xaxes(gridcolor="#21262d")
            fig.update_yaxes(gridcolor="#21262d")
            st.plotly_chart(fig, use_container_width=True)

        # Role-specific insights
        with st.expander("📋 Role Analysis Insights"):
            st.markdown("""
            **Role Performance Analysis:**

            **Senior Developers & Tech Leads:**
            - Typically show highest impact scores
            - Balance between visibility and deep work
            - Key for mentoring and code quality

            **Junior Developers:**
            - Often higher visibility (asking questions, participating)
            - Impact grows with experience
            - Focus on learning and code quality

            **Specialists (DevOps, QA):**
            - Critical but often lower visibility
            - High impact on system stability
            - Need recognition for infrastructure work

            **Recommendations:**
            - Set role-appropriate expectations
            - Recognize different contribution types
            - Balance team composition
            """)

    @staticmethod
    def _show_activity_vs_impact(data: pd.DataFrame, team_name: str):
        """Show activity vs impact analysis"""
        st.subheader(f"Activity vs Impact Analysis - {team_name}")

        # Create visualization
        fig = VisualizationEngine.create_activity_impact_chart(data, team_name)
        st.plotly_chart(fig, use_container_width=True)

        # Quadrant analysis
        st.markdown("### Quadrant Analysis")

        # Calculate counts
        quadrants = {
            "High Impact, Low Visibility": len(data[
                                                   (data["impact_score"] > 75) & (data["visibility_score"] < 50)
                                                   ]),
            "High Impact, High Visibility": len(data[
                                                    (data["impact_score"] > 75) & (data["visibility_score"] >= 50)
                                                    ]),
            "Low Impact, High Visibility": len(data[
                                                   (data["impact_score"] <= 75) & (data["visibility_score"] >= 50)
                                                   ]),
            "Low Impact, Low Visibility": len(data[
                                                  (data["impact_score"] <= 75) & (data["visibility_score"] < 50)
                                                  ])
        }

        # Display quadrant metrics
        cols = st.columns(4)
        quadrant_colors = ["#238636", "#58a6ff", "#e3b341", "#f85149"]

        for idx, ((name, count), color) in enumerate(zip(quadrants.items(), quadrant_colors)):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"**{name}**")
                    st.markdown(f"<h2 style='color:{color}'>{count}</h2>", unsafe_allow_html=True)
                    st.markdown(f"{count / len(data) * 100:.1f}% of team")

        # Detailed analysis
        with st.expander("🔍 Detailed Quadrant Analysis"):
            st.markdown("""
            **Quadrant 1: Silent Architects (High Impact, Low Visibility)**
            - Critical contributors often overlooked
            - Focus on deep work, avoid meetings/chats
            - Need recognition and protection

            **Quadrant 2: Visible Leaders (High Impact, High Visibility)**
            - Strong communicators and leaders
            - Balance visibility with substance
            - Ideal for leadership roles

            **Quadrant 3: Busy Workers (Low Impact, High Visibility)**
            - High activity but low impact
            - May need focus training
            - Review workload priorities

            **Quadrant 4: Under Performers (Low Impact, Low Visibility)**
            - Need performance support
            - May be disengaged or struggling
            - Schedule improvement plans
            """)

            # Show members in each quadrant
            for quadrant_name, condition in [
                ("Silent Architects", (data["impact_score"] > 75) & (data["visibility_score"] < 50)),
                ("Visible Leaders", (data["impact_score"] > 75) & (data["visibility_score"] >= 50)),
                ("Busy Workers", (data["impact_score"] <= 75) & (data["visibility_score"] >= 50)),
                ("Under Performers", (data["impact_score"] <= 75) & (data["visibility_score"] < 50))
            ]:
                quadrant_members = data[condition]
                if not quadrant_members.empty:
                    with st.expander(f"{quadrant_name} ({len(quadrant_members)} members)"):
                        for _, member in quadrant_members.iterrows():
                            st.markdown(f"- **{member['name']}** ({member['role']})")


class EmployeeProfile:
    """Individual employee profile page"""

    @staticmethod
    def show(employee_id: str, team_name: str):
        """Display employee profile"""
        try:
            # Load team data
            team_data = DataManager.generate_team_data(team_name,
                                                       st.session_state.user["teams"][team_name]["size"])
            employee = team_data[team_data["employee_id"] == employee_id].iloc[0]

            # Navigation
            col1, col2 = st.columns([6, 1])
            with col1:
                st.title("Employee Profile")
            with col2:
                if st.button("← Back to Team", type="secondary", use_container_width=True):
                    st.session_state.current_employee = None
                    st.rerun()

            st.markdown("---")

            # Profile header with ranking
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown(f"### {employee['name']}")
                st.markdown(f"**{employee['role']}** | {team_name}")
                st.markdown(f"Employee ID: `{employee['employee_id']}`")
                st.markdown(f"Email: {employee['email']}")
                st.markdown(f"Joined: {employee['join_date']} ({employee['tenure_months']} months tenure)")
                st.markdown(f"Current Project: **{employee['current_project']}**")

            with col2:
                # Key metrics
                st.markdown("#### Performance Metrics")
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Contribution Score", f"{employee['contribution_score']:.1f}")
                    st.metric("Impact Score", f"{employee['impact_score']:.1f}")
                with metric_col2:
                    st.metric("Quality Score", f"{employee['quality_score']:.1f}")
                    st.metric("Visibility Score", f"{employee['visibility_score']:.1f}")

            with col3:
                # Ranking card
                with st.container(border=True):
                    st.markdown("#### Team Ranking")
                    st.markdown(f"<h1 style='text-align: center; color: #58a6ff;'>#{employee['team_rank']}</h1>",
                                unsafe_allow_html=True)
                    st.markdown(f"out of {len(team_data)} team members")

                    if employee["is_silent_architect"]:
                        st.success("**Silent Architect** - High impact, low visibility")

                    # Performance trend (simulated)
                    trend = random.choice(["↑ Improving", "→ Stable", "↓ Declining"])
                    trend_color = "#238636" if "Improving" in trend else "#e3b341" if "Stable" in trend else "#f85149"
                    st.markdown(f"Trend: <span style='color:{trend_color}'>{trend}</span>", unsafe_allow_html=True)

            st.markdown("---")

            # Detailed tabs
            tab1, tab2, tab3 = st.tabs(["Performance Analysis", "Activity Details", "Skills & Projects"])

            with tab1:
                EmployeeProfile._show_performance_analysis(employee, team_data)

            with tab2:
                EmployeeProfile._show_activity_details(employee)

            with tab3:
                EmployeeProfile._show_skills_projects(employee)

        except Exception as e:
            st.error(f"Error loading employee profile: {str(e)}")
            if st.button("Return to Team Dashboard"):
                st.session_state.current_employee = None
                st.rerun()

    @staticmethod
    def _show_performance_analysis(employee: pd.Series, team_data: pd.DataFrame):
        """Show performance analysis"""
        col1, col2 = st.columns(2)

        with col1:
            # Radar chart
            fig = VisualizationEngine.create_performance_radar(employee)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Performance chart unavailable")

        with col2:
            # Comparison with team
            st.markdown("#### Team Comparison")

            comparisons = [
                ("Contribution Score", employee["contribution_score"], team_data["contribution_score"].mean()),
                ("Impact Score", employee["impact_score"], team_data["impact_score"].mean()),
                ("Quality Score", employee["quality_score"], team_data["quality_score"].mean()),
                ("Visibility Score", employee["visibility_score"], team_data["visibility_score"].mean())
            ]

            for label, emp_score, team_avg in comparisons:
                diff = emp_score - team_avg
                diff_color = "#238636" if diff > 0 else "#f85149" if diff < 0 else "#8b949e"
                diff_symbol = "↑" if diff > 0 else "↓" if diff < 0 else "→"

                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.markdown(f"**{label}:**")
                with col_b:
                    st.markdown(f"{emp_score:.1f}")
                with col_c:
                    st.markdown(f"<span style='color:{diff_color}'>{diff_symbol}{abs(diff):.1f}</span>",
                                unsafe_allow_html=True)

            # Percentile ranks
            st.markdown("#### Percentile Ranks")
            for score_type in ["contribution_score", "impact_score", "quality_score"]:
                if score_type in team_data.columns:
                    percentile = (team_data[score_type] < employee[score_type]).sum() / len(team_data) * 100
                    label = score_type.replace("_", " ").title()
                    st.progress(percentile / 100, text=f"{label}: Top {percentile:.1f}%")

        # Performance insights
        st.markdown("### Performance Insights")

        insights = []

        if employee["contribution_score"] > 80:
            insights.append(("✅", "High contributor consistently delivering value"))
        elif employee["contribution_score"] < 60:
            insights.append(("⚠️", "Below average contribution - consider support"))

        if employee["is_silent_architect"]:
            insights.append(("🎯", "Silent Architect - high impact work with low visibility"))

        impact_vs_visibility = employee["impact_score"] - employee["visibility_score"]
        if impact_vs_visibility > 20:
            insights.append(("📈", "Impact significantly exceeds visibility"))
        elif impact_vs_visibility < -20:
            insights.append(("💬", "Visibility exceeds impact - consider focus areas"))

        if employee["pr_approval_rate"] > 0.9:
            insights.append(("👍", "Excellent code quality and PR approval rate"))

        if employee["mentoring_sessions"] > 10:
            insights.append(("👥", "Strong mentoring contribution"))

        # Display insights
        cols = st.columns(3)
        for idx, (icon, insight) in enumerate(insights):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"{icon} **{insight}**")

    @staticmethod
    def _show_activity_details(employee: pd.Series):
        """Show detailed activity metrics"""
        # Generate daily activity
        daily_data = DataManager.get_daily_activity(employee["employee_id"])

        # Activity timeline
        fig = VisualizationEngine.create_activity_timeline(daily_data, employee["name"])
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Activity timeline data unavailable")

        # Activity metrics
        st.markdown("#### Activity Metrics (Last 30 Days)")

        if not daily_data.empty:
            # Calculate statistics
            stats = {
                "Total Commits": daily_data["commits"].sum(),
                "Average Daily Commits": daily_data["commits"].mean(),
                "PRs Created": daily_data["prs_created"].sum(),
                "PRs Reviewed": daily_data["prs_reviewed"].sum(),
                "Average Hours Active": daily_data["hours_active"].mean(),
                "Weekend Activity Ratio": f"{daily_data[daily_data['is_weekend']]['hours_active'].sum() / daily_data['hours_active'].sum() * 100:.1f}%",
                "Most Active Day": daily_data.groupby("day_of_week")["hours_active"].mean().idxmax()
            }

            # Display in columns
            cols = st.columns(3)
            for idx, (label, value) in enumerate(stats.items()):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.markdown(f"**{label}**")
                        if isinstance(value, float):
                            st.markdown(f"{value:.1f}")
                        else:
                            st.markdown(f"{value}")

        # Detailed activity breakdown
        with st.expander("📋 Detailed Activity Breakdown"):
            if not daily_data.empty:
                st.dataframe(
                    daily_data,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "date": "Date",
                        "commits": "Commits",
                        "prs_created": "PRs Created",
                        "prs_reviewed": "PRs Reviewed",
                        "hours_active": "Hours Active",
                        "day_of_week": "Day"
                    }
                )
            else:
                st.info("No detailed activity data available")

    @staticmethod
    def _show_skills_projects(employee: pd.Series):
        """Show skills and projects"""
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Skills & Expertise")

            skills = [
                ("Primary Technology", employee["primary_tech"], "#58a6ff"),
                ("Code Quality", f"{employee['quality_score']:.1f}/100", "#238636"),
                ("PR Approval Rate", f"{employee['pr_approval_rate'] * 100:.1f}%", "#238636"),
                ("Code Reviews", f"{employee['code_reviews']} completed", "#bc8cff"),
                ("Mentoring", f"{employee['mentoring_sessions']} sessions", "#e3b341"),
                ("Bug Resolution", f"{employee['critical_bugs_fixed']} critical fixes", "#f85149")
            ]

            for skill_name, level, color in skills:
                with st.container(border=True):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"**{skill_name}**")
                    with col_b:
                        st.markdown(f"<span style='color:{color}'>{level}</span>", unsafe_allow_html=True)

        with col2:
            st.markdown("#### Project Contributions")

            # Simulated project contributions
            projects = [
                ("Platform Modernization", "Backend Services", 85, "2024-06-15"),
                ("API Gateway", "Security Implementation", 60, "2024-06-10"),
                ("Mobile App", "Performance Optimization", 75, "2024-05-28")
            ]

            for project_name, role, progress, last_update in projects:
                with st.container(border=True):
                    st.markdown(f"**{project_name}**")
                    st.markdown(f"*{role}*")

                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.progress(progress / 100, text=f"{progress}%")
                    with col_b:
                        st.caption(f"Updated: {last_update}")

        # Work patterns
        st.markdown("#### Work Patterns & Availability")

        patterns = [
            ("Preferred Work Hours", "9:00 AM - 5:00 PM"),
            ("Focus Time Blocks", "3 hours daily"),
            ("Meeting Preference", "Afternoons"),
            ("Communication Style", "Written (Slack/Email)"),
            ("Response Time", "Within 2 hours"),
            ("Weekly Availability", "40 hours")
        ]

        cols = st.columns(3)
        for idx, (pattern, value) in enumerate(patterns):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"**{pattern}**")
                    st.markdown(f"{value}")


# ======================
# MAIN APPLICATION CONTROLLER
# ======================
def main():
    """Main application controller with error handling"""
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

        # Clear caches if needed (for debugging)
        if st.session_state.get("clear_cache", False):
            st.cache_data.clear()
            st.session_state.clear_cache = False

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
        st.info(f"Error details: {str(e)}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Restart Application", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.cache_data.clear()
                st.rerun()
        with col2:
            if st.button("Return to Login"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()


if __name__ == "__main__":
    main()
