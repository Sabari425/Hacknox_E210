import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json
from typing import Dict, List, Tuple
import hashlib
import time

# Set page config
st.set_page_config(
    page_title="Workforce Contribution Monitor",
    page_icon="📊",
    layout="wide"
)

def generate_employee_data(num_employees: int, team_name: str):
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", 
                   "Avery", "Quinn", "Blake", "Hayden", "Drew", "Cameron",
                   "Jamie", "Robin", "Skyler", "Dakota", "Rowan", "Sage"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Miller", "Davis", "Rodriguez", "Martinez", "Lee", "Gonzalez"]
    
    roles = ["Senior Developer", "Junior Developer", "Tech Lead", "Architect",
             "DevOps Engineer", "QA Engineer", "Product Manager", "Scrum Master"]
    
    data = []
    for i in range(num_employees):
        emp_id = f"{team_name[:3].upper()}{i+1:03d}"
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}@company.com"
        
        # Generate realistic metrics
        activity_score = random.randint(30, 95)
        
        # Silent architects have high impact but lower visibility
        is_silent_architect = random.random() < 0.3
        if is_silent_architect:
            impact_score = random.randint(80, 98)
            visibility_score = random.randint(20, 60)
        else:
            impact_score = random.randint(40, 90)
            visibility_score = random.randint(50, 95)
        
        # Contribution score - weighted combination
        contribution_score = (impact_score * 0.7 + activity_score * 0.3)
        
        # Generate project contributions
        projects = random.sample(["Project Alpha", "Project Beta", "Project Gamma", 
                                 "Project Delta", "Project Epsilon"], k=random.randint(1, 3))
        
        # Generate role-based metrics
        if "Senior" in roles[i % len(roles)] or "Architect" in roles[i % len(roles)]:
            mentoring_hours = random.randint(5, 20)
            code_reviews = random.randint(10, 40)
        else:
            mentoring_hours = random.randint(0, 10)
            code_reviews = random.randint(5, 20)
        
        data.append({
            "employee_id": emp_id,
            "name": f"{first} {last}",
            "email": email,
            "role": roles[i % len(roles)],
            "team": team_name,
            "activity_score": activity_score,
            "impact_score": impact_score,
            "visibility_score": visibility_score,
            "contribution_score": round(contribution_score, 1),
            "commits": random.randint(50, 300),
            "lines_code": random.randint(5000, 50000),
            "bugs_fixed": random.randint(5, 50),
            "features_delivered": random.randint(1, 15),
            "mentoring_hours": mentoring_hours,
            "code_reviews": code_reviews,
            "critical_fixes": random.randint(1, 10),
            "prs_merged": random.randint(10, 60),
            "projects": ", ".join(projects),
            "join_date": (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")
        })
    
    return pd.DataFrame(data)

def generate_project_structure(team_name: str):
    projects = {
        "Project Alpha": {
            "description": "Core platform development",
            "subdivisions": {
                "Backend API": ["API Gateway", "Microservices", "Database Layer"],
                "Frontend": ["User Interface", "State Management", "API Integration"],
                "DevOps": ["CI/CD Pipeline", "Infrastructure", "Monitoring"]
            },
            "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Kubernetes"]
        },
        "Project Beta": {
            "description": "Mobile application",
            "subdivisions": {
                "iOS": ["SwiftUI Components", "Networking", "Core Data"],
                "Android": ["Kotlin Modules", "UI/UX", "Performance"],
                "Backend": ["REST API", "Authentication", "Data Sync"]
            },
            "tech_stack": ["Swift", "Kotlin", "Node.js", "MongoDB", "Firebase"]
        },
        "Project Gamma": {
            "description": "Data analytics platform",
            "subdivisions": {
                "Data Pipeline": ["ETL Processes", "Data Quality", "Scheduling"],
                "Analytics": ["Dashboards", "Reports", "Machine Learning"],
                "Infrastructure": ["Data Warehouse", "Stream Processing", "Security"]
            },
            "tech_stack": ["Python", "Spark", "Airflow", "Snowflake", "Tableau"]
        }
    }
    
    return projects

def generate_activity_logs(num_logs: int = 100):
    activities = ["Commit", "Pull Request", "Code Review", "Bug Fix", "Feature Development",
                  "Documentation", "Meeting", "Mentoring", "Design Review", "Testing"]
    
    platforms = ["GitHub", "Jira", "Slack", "Teams", "Confluence", "Figma"]
    
    logs = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(num_logs):
        log_date = start_date + timedelta(days=random.randint(0, 30),
                                          hours=random.randint(0, 23),
                                          minutes=random.randint(0, 59))
        
        logs.append({
            "timestamp": log_date,
            "employee_id": f"EMP{random.randint(1, 20):03d}",
            "activity": random.choice(activities),
            "platform": random.choice(platforms),
            "duration_min": random.randint(5, 180),
            "project": random.choice(["Project Alpha", "Project Beta", "Project Gamma"]),
            "impact_level": random.choice(["Low", "Medium", "High", "Critical"])
        })
    
    return pd.DataFrame(logs).sort_values("timestamp")

class ContributionScorer:
    @staticmethod
    def calculate_contribution_score(employee_data: pd.Series) -> Dict:
        # Weights for different factors
        weights = {
            "code_quality": 0.25,
            "impact": 0.30,
            "collaboration": 0.20,
            "leadership": 0.15,
            "innovation": 0.10
        }
        
        # Normalize metrics
        metrics = {}
        
        # Code Quality Score (based on PR merge rate, code reviews)
        pr_success_rate = min(employee_data['prs_merged'] / max(employee_data['prs_merged'] + 5, 1), 1)
        metrics["code_quality"] = (pr_success_rate * 0.6 + 
                                  min(employee_data['code_reviews'] / 40, 1) * 0.4) * 100
        
        # Impact Score (bug fixes, features, critical work)
        bugs_weight = employee_data['critical_fixes'] * 2 + employee_data['bugs_fixed']
        features_weight = employee_data['features_delivered'] * 3
        total_impact = bugs_weight + features_weight
        metrics["impact"] = min(total_impact / 100 * 100, 100)
        
        # Collaboration Score (mentoring, team involvement)
        metrics["collaboration"] = min(
            (employee_data['mentoring_hours'] * 2 + 
             employee_data['code_reviews'] * 0.5) / 60 * 100, 100
        )
        
        # Leadership Score (based on role and mentoring)
        role_multiplier = 1.0
        if "Senior" in employee_data['role'] or "Lead" in employee_data['role']:
            role_multiplier = 1.3
        elif "Architect" in employee_data['role']:
            role_multiplier = 1.5
            
        metrics["leadership"] = min(
            (employee_data['mentoring_hours'] * role_multiplier + 
             employee_data['code_reviews'] * 0.3) / 40 * 100, 100
        )
        
        # Innovation Score (lines of code, project diversity)
        projects_count = len(employee_data['projects'].split(", "))
        metrics["innovation"] = min(
            (employee_data['lines_code'] / 10000 + 
             projects_count * 10) * 10, 100
        )
        
        # Calculate weighted total score
        total_score = sum(metrics[key] * weights[key] for key in metrics.keys())
        
        # Adjust for silent architects (high impact, low visibility)
        visibility_penalty = 0
        if employee_data['visibility_score'] < 40 and employee_data['impact_score'] > 70:
            # Silent architect bonus
            visibility_penalty = -5  # Actually a bonus since we subtract negative
        
        final_score = total_score - visibility_penalty
        
        return {
            "total_score": round(final_score, 1),
            "breakdown": metrics,
            "weights": weights,
            "is_silent_architect": (employee_data['visibility_score'] < 50 and 
                                   employee_data['impact_score'] > 75)
        }

class Authentication:
    USERS = {
        "manager_a": {
            "password": "password123",
            "name": "Sarah Johnson",
            "teams": ["Team A", "Team B"],
            "role": "Senior Engineering Manager"
        },
        "manager_b": {
            "password": "password456",
            "name": "Michael Chen",
            "teams": ["Team C", "Team D"],
            "role": "Product Engineering Manager"
        },
        "admin": {
            "password": "admin123",
            "name": "Admin User",
            "teams": ["All Teams"],
            "role": "System Administrator"
        }
    }
    
    @staticmethod
    def login(username, password):
        if username in Authentication.USERS:
            if Authentication.USERS[username]["password"] == password:
                return Authentication.USERS[username]
        return None

def create_radar_chart(metrics: Dict, title: str):
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],  # Close the polygon
        theta=categories + [categories[0]],
        fill='toself',
        name=title
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title=title,
        height=300
    )
    
    return fig

def create_activity_vs_impact_chart(data: pd.DataFrame):
    fig = px.scatter(data, 
                     x='visibility_score', 
                     y='impact_score',
                     size='contribution_score',
                     color='role',
                     hover_name='name',
                     hover_data=['team', 'commits', 'features_delivered'],
                     title='Activity vs Impact Analysis',
                     labels={
                         'visibility_score': 'Perceived Activity (Visibility)',
                         'impact_score': 'Actual Impact',
                         'contribution_score': 'Contribution Score'
                     })
    
    # Add quadrant lines
    fig.add_hline(y=75, line_dash="dash", line_color="gray")
    fig.add_vline(x=50, line_dash="dash", line_color="gray")
    
    # Add quadrant labels
    fig.add_annotation(x=25, y=90, text="Silent Architects", showarrow=False, font=dict(color="green"))
    fig.add_annotation(x=75, y=90, text="Visible Leaders", showarrow=False, font=dict(color="blue"))
    fig.add_annotation(x=25, y=40, text="Under Performers", showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=75, y=40, text="Busy Workers", showarrow=False, font=dict(color="orange"))
    
    return fig

def create_contribution_timeline(employee_id: str, logs: pd.DataFrame):
    employee_logs = logs[logs['employee_id'] == employee_id]
    
    if employee_logs.empty:
        return None
    
    # Group by date and activity type
    daily_activity = employee_logs.groupby(
        [employee_logs['timestamp'].dt.date, 'activity']
    )['duration_min'].sum().unstack(fill_value=0)
    
    fig = go.Figure()
    
    for activity in daily_activity.columns:
        fig.add_trace(go.Scatter(
            x=daily_activity.index,
            y=daily_activity[activity],
            mode='lines+markers',
            name=activity,
            stackgroup='one'
        ))
    
    fig.update_layout(
        title=f'Activity Timeline - {employee_id}',
        xaxis_title='Date',
        yaxis_title='Activity Duration (minutes)',
        hovermode='x unified',
        height=300
    )
    
    return fig

def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'selected_team' not in st.session_state:
        st.session_state.selected_team = None
    if 'selected_employee' not in st.session_state:
        st.session_state.selected_employee = None
    
    # Login page
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    # Main dashboard
    show_dashboard()

def show_login_page():
    st.title("🔐 Workforce Contribution Monitor")
    st.markdown("### Manager Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                user = Authentication.login(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown("---")
        st.markdown("**Demo Accounts:**")
        st.markdown("- **manager_a** / password123")
        st.markdown("- **manager_b** / password456")
        st.markdown("- **admin** / admin123")

def show_dashboard():
    # Sidebar navigation
    with st.sidebar:
        st.title(f"👤 {st.session_state.user['name']}")
        st.caption(f"Role: {st.session_state.user['role']}")
        
        st.markdown("---")
        
        # Team selection
        selected_team = st.selectbox(
            "Select Team",
            st.session_state.user['teams'],
            key="team_selector"
        )
        
        if selected_team != st.session_state.selected_team:
            st.session_state.selected_team = selected_team
            st.session_state.selected_employee = None
            st.rerun()
        
        # Logout button
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.selected_team = None
            st.session_state.selected_employee = None
            st.rerun()
    
    # Generate sample data for selected team
    team_data = generate_employee_data(
        random.randint(8, 15) if st.session_state.selected_team != "All Teams" else 50,
        st.session_state.selected_team
    )
    
    # Calculate scores for all employees
    scores = []
    for _, emp in team_data.iterrows():
        score_result = ContributionScorer.calculate_contribution_score(emp)
        scores.append({
            "employee_id": emp["employee_id"],
            "total_score": score_result["total_score"],
            "is_silent_architect": score_result["is_silent_architect"],
            "breakdown": score_result["breakdown"]
        })
    
    scores_df = pd.DataFrame(scores)
    team_data = team_data.merge(scores_df, on="employee_id")
    
    # Sort by contribution score
    team_data = team_data.sort_values("total_score", ascending=False)
    team_data["rank"] = range(1, len(team_data) + 1)
    
    # Generate activity logs
    activity_logs = generate_activity_logs(200)
    
    # Main content area
    st.title(f"📊 Workforce Contribution Monitor - {st.session_state.selected_team}")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Silent Architects", 
        "Team Members", 
        "Project Structure",
        "Contribution Roles",
        "Activity vs Impact",
        "Individual Profile"
    ])
    
    # Tab 1: Silent Architects
    with tab1:
        st.header("🎯 Silent Architects")
        st.markdown("""
        These team members have **high impact** but **lower visibility**. 
        They often work on critical systems without seeking recognition.
        """)
        
        silent_architects = team_data[team_data['is_silent_architect']]
        
        if len(silent_architects) > 0:
            cols = st.columns(3)
            for idx, (_, architect) in enumerate(silent_architects.iterrows()):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.markdown(f"### {architect['name']}")
                        st.markdown(f"**Role:** {architect['role']}")
                        st.markdown(f"**Rank:** #{architect['rank']}")
                        st.markdown(f"**Contribution Score:** {architect['total_score']}/100")
                        
                        # Radar chart for skills
                        fig = create_radar_chart(architect['breakdown'], "Skill Breakdown")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        if st.button(f"View Profile", key=f"view_{architect['employee_id']}"):
                            st.session_state.selected_employee = architect['employee_id']
                            st.rerun()
        else:
            st.info("No silent architects identified in this team. Consider reviewing visibility metrics.")
    
    # Tab 2: Team Members with Ranking
    with tab2:
        st.header("👥 Team Members Ranking")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Team Size", len(team_data))
        with col2:
            avg_score = team_data['total_score'].mean()
            st.metric("Avg Contribution Score", f"{avg_score:.1f}")
        with col3:
            silent_count = len(silent_architects)
            st.metric("Silent Architects", silent_count)
        with col4:
            top_performer = team_data.iloc[0]
            st.metric("Top Contributor", top_performer['name'])
        
        # Team ranking table
        st.subheader("Team Ranking")
        
        # Add search and filter
        search_col, filter_col = st.columns(2)
        with search_col:
            search_query = st.text_input("Search by name", placeholder="Type to filter...")
        with filter_col:
            role_filter = st.multiselect(
                "Filter by role",
                options=team_data['role'].unique(),
                default=[]
            )
        
        # Apply filters
        filtered_data = team_data.copy()
        if search_query:
            filtered_data = filtered_data[filtered_data['name'].str.contains(search_query, case=False)]
        if role_filter:
            filtered_data = filtered_data[filtered_data['role'].isin(role_filter)]
        
        # Display ranking table
        display_cols = ['rank', 'name', 'role', 'total_score', 'impact_score', 
                       'visibility_score', 'commits', 'features_delivered']
        
        st.dataframe(
            filtered_data[display_cols].rename(columns={
                'rank': 'Rank',
                'name': 'Name',
                'role': 'Role',
                'total_score': 'Contribution',
                'impact_score': 'Impact',
                'visibility_score': 'Visibility',
                'commits': 'Commits',
                'features_delivered': 'Features'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    # Tab 3: Project Structure
    with tab3:
        st.header("🏗️ Project Structure")
        
        projects = generate_project_structure(st.session_state.selected_team)
        
        for project_name, project_data in projects.items():
            with st.expander(f"📁 {project_name} - {project_data['description']}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Project subdivisions
                    for subdivision, components in project_data['subdivisions'].items():
                        st.subheader(f"• {subdivision}")
                        
                        for component in components:
                            with st.container(border=True):
                                st.markdown(f"**{component}**")
                                
                                # Find team members working on this component
                                # (In a real app, this would come from actual project assignments)
                                component_members = team_data.sample(random.randint(1, 4))
                                
                                for _, member in component_members.iterrows():
                                    member_col, score_col = st.columns([3, 1])
                                    with member_col:
                                        st.markdown(f"- {member['name']} ({member['role']})")
                                    with score_col:
                                        st.markdown(f"`{member['total_score']}`")
                
                with col2:
                    st.markdown("**Tech Stack:**")
                    for tech in project_data['tech_stack']:
                        st.markdown(f"- {tech}")
                    
                    st.markdown("---")
                    st.markdown("**Project Metrics:**")
                    
                    # Generate random project metrics
                    metrics = {
                        "Completion": f"{random.randint(60, 95)}%",
                        "Bugs": random.randint(5, 50),
                        "Active Contributors": random.randint(3, 8),
                        "Last Deployment": (datetime.now() - timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
                    }
                    
                    for metric, value in metrics.items():
                        st.markdown(f"**{metric}:** {value}")
    
    # Tab 4: Contribution Roles
    with tab4:
        st.header("🎭 Contribution Roles Analysis")
        
        # Role-based analysis
        role_analysis = team_data.groupby('role').agg({
            'total_score': 'mean',
            'impact_score': 'mean',
            'visibility_score': 'mean',
            'employee_id': 'count'
        }).round(1).reset_index()
        
        role_analysis = role_analysis.rename(columns={
            'employee_id': 'count',
            'total_score': 'avg_contribution',
            'impact_score': 'avg_impact',
            'visibility_score': 'avg_visibility'
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Role Performance")
            st.dataframe(
                role_analysis.sort_values('avg_contribution', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.subheader("Role Distribution")
            fig = px.pie(role_analysis, values='count', names='role', title='Team Composition by Role')
            st.plotly_chart(fig, use_container_width=True)
        
        # Role comparison visualization
        st.subheader("Role Comparison")
        
        fig = go.Figure(data=[
            go.Bar(name='Avg Contribution', x=role_analysis['role'], y=role_analysis['avg_contribution']),
            go.Bar(name='Avg Impact', x=role_analysis['role'], y=role_analysis['avg_impact']),
            go.Bar(name='Avg Visibility', x=role_analysis['role'], y=role_analysis['avg_visibility'])
        ])
        
        fig.update_layout(
            barmode='group',
            title='Role Performance Metrics',
            yaxis_title='Score',
            xaxis_title='Role',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 5: Activity vs Impact
    with tab5:
        st.header("⚖️ Activity vs Impact Analysis")
        
        # Main scatter plot
        fig = create_activity_vs_impact_chart(team_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Quadrant analysis
        st.subheader("Quadrant Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate quadrant counts
        silent_archs = team_data[(team_data['impact_score'] > 75) & (team_data['visibility_score'] < 50)]
        visible_leaders = team_data[(team_data['impact_score'] > 75) & (team_data['visibility_score'] >= 50)]
        busy_workers = team_data[(team_data['impact_score'] <= 75) & (team_data['visibility_score'] >= 50)]
        under_performers = team_data[(team_data['impact_score'] <= 75) & (team_data['visibility_score'] < 50)]
        
        with col1:
            st.metric("Silent Architects", len(silent_archs), delta=f"{len(silent_archs)/len(team_data)*100:.1f}%")
        with col2:
            st.metric("Visible Leaders", len(visible_leaders), delta=f"{len(visible_leaders)/len(team_data)*100:.1f}%")
        with col3:
            st.metric("Busy Workers", len(busy_workers), delta=f"{len(busy_workers)/len(team_data)*100:.1f}%")
        with col4:
            st.metric("Under Performers", len(under_performers), delta=f"{len(under_performers)/len(team_data)*100:.1f}%")
        
        # Time series analysis
        st.subheader("Team Performance Trend")
        
        # Generate trend data (simplified)
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        trend_data = []
        
        for date in dates:
            month_avg = team_data['total_score'].mean() + random.uniform(-5, 5)
            trend_data.append({
                'month': date.strftime('%b %Y'),
                'avg_score': month_avg,
                'silent_architect_ratio': len(silent_archs)/len(team_data) * 100 + random.uniform(-10, 10)
            })
        
        trend_df = pd.DataFrame(trend_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trend_df['month'], y=trend_df['avg_score'],
                                mode='lines+markers', name='Avg Contribution Score'))
        fig.add_trace(go.Scatter(x=trend_df['month'], y=trend_df['silent_architect_ratio'],
                                mode='lines+markers', name='Silent Architect Ratio', yaxis='y2'))
        
        fig.update_layout(
            title='Team Performance Trends',
            yaxis=dict(title='Avg Contribution Score'),
            yaxis2=dict(title='Silent Architect %', overlaying='y', side='right'),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 6: Individual Profile
    with tab6:
        st.header("👤 Individual Profile")
        
        if st.session_state.selected_employee:
            employee = team_data[team_data['employee_id'] == st.session_state.selected_employee].iloc[0]
        else:
            # Let user select an employee
            employee_options = team_data[['employee_id', 'name']].values.tolist()
            selected_option = st.selectbox(
                "Select Employee",
                options=[f"{e[0]} - {e[1]}" for e in employee_options],
                index=0
            )
            selected_id = selected_option.split(" - ")[0]
            employee = team_data[team_data['employee_id'] == selected_id].iloc[0]
        
        # Display employee profile
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.metric("Rank", f"#{employee['rank']}")
            st.metric("Contribution Score", f"{employee['total_score']}/100")
            st.metric("Impact Score", f"{employee['impact_score']}/100")
            st.metric("Visibility Score", f"{employee['visibility_score']}/100")
            
            if employee['is_silent_architect']:
                st.success("🎯 Identified as Silent Architect")
        
        with col2:
            st.subheader(f"{employee['name']}")
            st.markdown(f"**Role:** {employee['role']}")
            st.markdown(f"**Employee ID:** {employee['employee_id']}")
            st.markdown(f"**Email:** {employee['email']}")
            st.markdown(f"**Team:** {employee['team']}")
            st.markdown(f"**Join Date:** {employee['join_date']}")
            st.markdown(f"**Projects:** {employee['projects']}")
            
            # Radar chart
            fig = create_radar_chart(employee['breakdown'], "Contribution Breakdown")
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.subheader("Key Metrics")
            
            metrics = {
                "Commits": employee['commits'],
                "Lines of Code": f"{employee['lines_code']:,}",
                "Bugs Fixed": employee['bugs_fixed'],
                "Features Delivered": employee['features_delivered'],
                "Critical Fixes": employee['critical_fixes'],
                "PRs Merged": employee['prs_merged'],
                "Mentoring Hours": employee['mentoring_hours'],
                "Code Reviews": employee['code_reviews']
            }
            
            for metric, value in metrics.items():
                st.metric(metric, value)
        
        # Activity timeline
        st.subheader("Recent Activity Timeline")
        timeline_fig = create_contribution_timeline(employee['employee_id'], activity_logs)
        
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)
        else:
            st.info("No recent activity data available for this employee.")
        
        # Comparative analysis
        st.subheader("Comparative Analysis")
        
        # Compare with team average
        team_avg = team_data[['total_score', 'impact_score', 'visibility_score']].mean()
        
        comparison_data = pd.DataFrame({
            'Metric': ['Contribution Score', 'Impact Score', 'Visibility Score'],
            'Employee': [employee['total_score'], employee['impact_score'], employee['visibility_score']],
            'Team Average': [team_avg['total_score'], team_avg['impact_score'], team_avg['visibility_score']]
        })
        
        fig = go.Figure(data=[
            go.Bar(name='Employee', x=comparison_data['Metric'], y=comparison_data['Employee']),
            go.Bar(name='Team Average', x=comparison_data['Metric'], y=comparison_data['Team Average'])
        ])
        
        fig.update_layout(
            barmode='group',
            title='Employee vs Team Average',
            yaxis_title='Score',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance summary
        st.subheader("Performance Summary")
        
        summary = []
        if employee['total_score'] > team_avg['total_score']:
            summary.append("✅ Above average contribution score")
        else:
            summary.append("📊 At or below average contribution score")
        
        if employee['impact_score'] > 80:
            summary.append("🚀 High impact contributor")
        elif employee['impact_score'] > 60:
            summary.append("📈 Moderate impact contributor")
        else:
            summary.append("📉 Low impact contributor")
        
        if employee['visibility_score'] < 40:
            summary.append("🔇 Low visibility - Consider increasing communication")
        elif employee['visibility_score'] > 80:
            summary.append("📢 High visibility - Strong communicator")
        
        if employee['mentoring_hours'] > 10:
            summary.append("👨‍🏫 Active mentor - Valuable for team growth")
        
        for item in summary:
            st.markdown(f"- {item}")

if __name__ == "__main__":
    main()
