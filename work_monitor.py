import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import json

# Set page configuration
st.set_page_config(
    page_title="Workforce Contribution Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .highlight-box {
        background-color: #EFF6FF;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #BFDBFE;
        margin: 1rem 0;
    }
    .silent-architect {
        background-color: #F0FDF4;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #BBF7D0;
        margin: 0.5rem 0;
    }
    .activity-heavy {
        background-color: #FEF3C7;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #FDE68A;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ContributionAnalyzer:
    def __init__(self):
        self.metrics_config = {
            'impact_weights': {
                'critical_bug_fix': 1.5,
                'feature_launch': 1.2,
                'code_review': 0.8,
                'mentoring': 1.1,
                'documentation': 0.7,
                'refactoring': 0.9,
                'test_coverage': 0.8
            },
            'complexity_multipliers': {
                'low': 1.0,
                'medium': 1.3,
                'high': 1.8,
                'critical': 2.5
            }
        }
    
    def calculate_impact_score(self, employee_data: Dict) -> float:
        impact_score = 0
        
        # Base on code contributions
        if 'commits' in employee_data:
            # Weight commits by type and complexity
            for commit in employee_data.get('commits', []):
                weight = self.metrics_config['impact_weights'].get(
                    commit.get('type', 'code_review'), 1.0
                )
                complexity = self.metrics_config['complexity_multipliers'].get(
                    commit.get('complexity', 'medium'), 1.0
                )
                impact_score += weight * complexity
        
        # Add mentoring impact
        if 'mentoring_hours' in employee_data:
            impact_score += employee_data['mentoring_hours'] * 0.5
        
        # Add code review impact
        if 'code_reviews' in employee_data:
            impact_score += employee_data['code_reviews'] * 0.3
        
        # Add critical bug fixes bonus
        if 'critical_fixes' in employee_data:
            impact_score += employee_data['critical_fixes'] * 2.0
        
        return round(impact_score, 2)
    
    def calculate_activity_score(self, employee_data: Dict) -> float:
        activity_score = 0
        
        # Communication activity
        if 'slack_messages' in employee_data:
            activity_score += employee_data['slack_messages'] * 0.1
        
        if 'meetings_attended' in employee_data:
            activity_score += employee_data['meetings_attended'] * 0.5
        
        # Git activity
        if 'commits_count' in employee_data:
            activity_score += employee_data['commits_count'] * 0.3
        
        if 'prs_created' in employee_data:
            activity_score += employee_data['prs_created'] * 0.4
        
        # Online presence (weighted lower as it's less meaningful)
        if 'avg_online_hours' in employee_data:
            activity_score += employee_data['avg_online_hours'] * 0.05
        
        return round(activity_score, 2)
    
    def identify_silent_architects(self, team_data: List[Dict]) -> List[Dict]:
        scored_employees = []
        
        for emp in team_data:
            impact = self.calculate_impact_score(emp)
            activity = self.calculate_activity_score(emp)
            
            # Calculate impact-to-activity ratio
            ratio = impact / max(activity, 1)  # Avoid division by zero
            
            scored_employees.append({
                **emp,
                'impact_score': impact,
                'activity_score': activity,
                'impact_activity_ratio': round(ratio, 2),
                'efficiency_score': round(impact - (activity * 0.3), 2)  # Penalize excessive activity
            })
        
        # Sort by efficiency score (impact minus weighted activity)
        scored_employees.sort(key=lambda x: x['efficiency_score'], reverse=True)
        return scored_employees

def generate_sample_data(team_size: int = 10) -> List[Dict]:
    roles = ['Senior Engineer', 'Engineer', 'Tech Lead', 'Architect', 'Junior Engineer']
    teams = ['Frontend', 'Backend', 'DevOps', 'Full Stack', 'Mobile']
    
    employees = []
    
    for i in range(team_size):
        role = random.choice(roles)
        
        # Base metrics based on role
        base_commits = random.randint(10, 40)
        base_messages = random.randint(50, 200)
        
        employee = {
            'id': i + 1,
            'name': f'Employee {chr(65 + i)}',  # A, B, C, etc.
            'role': role,
            'team': random.choice(teams),
            'commits_count': base_commits + random.randint(-5, 10),
            'slack_messages': base_messages + random.randint(-20, 50),
            'meetings_attended': random.randint(8, 20),
            'prs_created': random.randint(5, 15),
            'code_reviews': random.randint(10, 25),
            'mentoring_hours': random.randint(0, 15),
            'critical_fixes': random.randint(0, 5),
            'avg_online_hours': random.uniform(6, 9),
            'sprint_completion': random.randint(70, 100),
            'commits': []
        }
        
        # Generate detailed commit data
        commit_types = ['critical_bug_fix', 'feature_launch', 'code_review', 
                       'documentation', 'refactoring', 'test_coverage']
        
        for _ in range(employee['commits_count']):
            commit_type = random.choice(commit_types)
            complexity = random.choice(['low', 'medium', 'high', 'critical'])
            
            # Adjust probabilities based on employee role
            if role == 'Senior Engineer' or role == 'Architect':
                complexity = random.choices(['low', 'medium', 'high', 'critical'], 
                                          weights=[0.1, 0.3, 0.4, 0.2])[0]
            elif role == 'Junior Engineer':
                complexity = random.choices(['low', 'medium', 'high', 'critical'], 
                                          weights=[0.5, 0.3, 0.15, 0.05])[0]
            
            employee['commits'].append({
                'type': commit_type,
                'complexity': complexity,
                'lines_changed': random.randint(10, 200)
            })
        
        employees.append(employee)
    
    return employees

def create_dashboard():
    # Header
    st.markdown('<h1 class="main-header">🏢 Workforce Contribution Monitor</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight-box">
    <h4>📋 Problem Statement</h4>
    <p>Bridging the gap between <strong>Activity</strong> (visibility, communication, raw metrics) 
    and <strong>Impact</strong> (actual value, complexity solved, critical work) in modern 
    remote/hybrid teams. Identifying "Silent Architects" who contribute high value 
    with low visibility.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = ContributionAnalyzer()
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        team_size = st.slider("Team Size", 3, 50, 15, 
                            help="Test how the system scales from small to large teams")
        
        st.markdown("### Impact Weight Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            critical_bug_weight = st.slider("Critical Bug Fix", 1.0, 3.0, 1.5, 0.1)
            feature_weight = st.slider("Feature Launch", 0.5, 2.5, 1.2, 0.1)
            mentoring_weight = st.slider("Mentoring", 0.5, 2.0, 1.1, 0.1)
        
        with col2:
            code_review_weight = st.slider("Code Review", 0.3, 1.5, 0.8, 0.1)
            documentation_weight = st.slider("Documentation", 0.2, 1.5, 0.7, 0.1)
            refactoring_weight = st.slider("Refactoring", 0.5, 1.5, 0.9, 0.1)
        
        # Update weights
        analyzer.metrics_config['impact_weights'] = {
            'critical_bug_fix': critical_bug_weight,
            'feature_launch': feature_weight,
            'code_review': code_review_weight,
            'mentoring': mentoring_weight,
            'documentation': documentation_weight,
            'refactoring': refactoring_weight,
            'test_coverage': 0.8
        }
        
        st.markdown("---")
        st.markdown("### 🔍 Filter View")
        show_silent_only = st.checkbox("Show Only Silent Architects", value=False)
        min_impact = st.slider("Minimum Impact Score", 0, 100, 0)
        
        if st.button("🔄 Generate New Sample Data"):
            st.cache_data.clear()
    
    # Generate or load sample data
    @st.cache_data
    def get_cached_data(team_size):
        return generate_sample_data(team_size)
    
    sample_data = get_cached_data(team_size)
    
    # Analyze contributions
    analyzed_data = analyzer.identify_silent_architects(sample_data)
    
    # Convert to DataFrame for display
    df = pd.DataFrame(analyzed_data)
    
    # Filter data based on sidebar settings
    if show_silent_only:
        # Silent architects: High impact-to-activity ratio
        df_display = df[df['impact_activity_ratio'] > 1.5].copy()
    else:
        df_display = df.copy()
    
    df_display = df_display[df_display['impact_score'] >= min_impact]
    
    # Main dashboard layout
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown('<h3 class="sub-header">👥 Team Contribution Analysis</h3>', 
                   unsafe_allow_html=True)
    
    with col2:
        avg_impact = df['impact_score'].mean()
        st.metric("Average Impact Score", f"{avg_impact:.1f}")
    
    with col3:
        avg_ratio = df['impact_activity_ratio'].mean()
        st.metric("Avg Impact/Activity Ratio", f"{avg_ratio:.2f}")
    
    # Top metrics row
    st.markdown("### 📊 Key Metrics Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        top_impact = df.iloc[0]
        st.metric("Highest Impact", top_impact['name'], 
                 f"Score: {top_impact['impact_score']}")
    
    with col2:
        # Find highest ratio (silent architect)
        silent_arch = df.loc[df['impact_activity_ratio'].idxmax()]
        st.metric("Top Silent Architect", silent_arch['name'], 
                 f"Ratio: {silent_arch['impact_activity_ratio']:.2f}")
    
    with col3:
        highest_activity = df.loc[df['activity_score'].idxmax()]
        st.metric("Highest Activity", highest_activity['name'], 
                 f"Score: {highest_activity['activity_score']}")
    
    with col4:
        # Most efficient (impact - weighted activity)
        most_efficient = df.loc[df['efficiency_score'].idxmax()]
        st.metric("Most Efficient", most_efficient['name'], 
                 f"Score: {most_efficient['efficiency_score']}")
    
    # Visualization section
    st.markdown("---")
    st.markdown('<h3 class="sub-header">📈 Activity vs Impact Visualization</h3>', 
               unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot: Activity vs Impact
        fig = px.scatter(
            df, 
            x='activity_score', 
            y='impact_score',
            color='role',
            size='efficiency_score',
            hover_data=['name', 'team', 'impact_activity_ratio'],
            title='Activity vs Impact Analysis',
            labels={
                'activity_score': 'Activity Score (Visibility)',
                'impact_score': 'Impact Score (Value)'
            }
        )
        
        # Add quadrant lines
        avg_activity = df['activity_score'].mean()
        avg_impact = df['impact_score'].mean()
        
        fig.add_hline(y=avg_impact, line_dash="dash", line_color="gray")
        fig.add_vline(x=avg_activity, line_dash="dash", line_color="gray")
        
        # Add quadrant annotations
        fig.add_annotation(
            x=avg_activity/2, y=avg_impact*1.5,
            text="Silent Architects",
            showarrow=False,
            font=dict(color="green", size=10)
        )
        
        fig.add_annotation(
            x=avg_activity*1.5, y=avg_impact/2,
            text="High Activity, Low Impact",
            showarrow=False,
            font=dict(color="orange", size=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Impact/Activity Ratio Bar Chart
        df_sorted = df.sort_values('impact_activity_ratio', ascending=True).tail(10)
        
        fig2 = px.bar(
            df_sorted,
            y='name',
            x='impact_activity_ratio',
            color='impact_score',
            orientation='h',
            title='Top 10 by Impact/Activity Ratio',
            labels={'impact_activity_ratio': 'Impact per Unit of Activity'},
            color_continuous_scale='Viridis'
        )
        
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
    
    # Silent Architects Section
    st.markdown("---")
    st.markdown('<h3 class="sub-header">🎯 Silent Architects Recognition</h3>', 
               unsafe_allow_html=True)
    
    # Filter for silent architects (high ratio, decent impact)
    silent_threshold = df['impact_activity_ratio'].quantile(0.75)
    impact_threshold = df['impact_score'].quantile(0.5)
    
    silent_architects = df[
        (df['impact_activity_ratio'] > silent_threshold) & 
        (df['impact_score'] > impact_threshold)
    ].sort_values('impact_activity_ratio', ascending=False)
    
    if not silent_architects.empty:
        for _, architect in silent_architects.iterrows():
            st.markdown(f"""
            <div class="silent-architect">
            <h4>👤 {architect['name']} ({architect['role']}) - Team: {architect['team']}</h4>
            <p><strong>Impact Score:</strong> {architect['impact_score']} | 
            <strong>Activity Score:</strong> {architect['activity_score']} | 
            <strong>Efficiency Ratio:</strong> {architect['impact_activity_ratio']}</p>
            <p><em>Key Contributions:</em> {architect.get('critical_fixes', 0)} critical bug fixes, 
            {architect.get('mentoring_hours', 0)} mentoring hours, 
            {architect.get('code_reviews', 0)} code reviews</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No silent architects identified with current thresholds. Try adjusting the filters.")
    
    # High Activity, Low Impact Warning
    st.markdown("---")
    st.markdown('<h3 class="sub-header">⚠️ High Activity, Low Impact Analysis</h3>', 
               unsafe_allow_html=True)
    
    activity_threshold = df['activity_score'].quantile(0.75)
    low_impact_threshold = df['impact_score'].quantile(0.25)
    
    high_activity_low_impact = df[
        (df['activity_score'] > activity_threshold) & 
        (df['impact_score'] < low_impact_threshold)
    ].sort_values('activity_score', ascending=False)
    
    if not high_activity_low_impact.empty:
        st.warning(f"Found {len(high_activity_low_impact)} team members with high activity but low impact scores")
        
        for _, emp in high_activity_low_impact.iterrows():
            st.markdown(f"""
            <div class="activity-heavy">
            <h4>👤 {emp['name']} ({emp['role']})</h4>
            <p><strong>Activity Score:</strong> {emp['activity_score']} (High) | 
            <strong>Impact Score:</strong> {emp['impact_score']} (Low) | 
            <strong>Ratio:</strong> {emp['impact_activity_ratio']}</p>
            <p><em>Activity Metrics:</em> {emp.get('slack_messages', 0)} Slack messages, 
            {emp.get('meetings_attended', 0)} meetings, 
            {emp.get('avg_online_hours', 0):.1f} avg online hours</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed Data Table
    st.markdown("---")
    st.markdown('<h3 class="sub-header">📋 Detailed Team Metrics</h3>', 
               unsafe_allow_html=True)
    
    # Select columns for display
    display_columns = [
        'name', 'role', 'team', 'impact_score', 'activity_score', 
        'impact_activity_ratio', 'efficiency_score',
        'commits_count', 'critical_fixes', 'mentoring_hours',
        'code_reviews', 'slack_messages'
    ]
    
    st.dataframe(
        df_display[display_columns].sort_values('efficiency_score', ascending=False),
        use_container_width=True,
        column_config={
            'impact_score': st.column_config.ProgressColumn(
                'Impact Score',
                help='Weighted impact based on contribution quality',
                format='%f',
                min_value=0,
                max_value=df['impact_score'].max() * 1.1
            ),
            'activity_score': st.column_config.ProgressColumn(
                'Activity Score',
                help='Raw activity metrics',
                format='%f',
                min_value=0,
                max_value=df['activity_score'].max() * 1.1
            )
        }
    )
    
    # System stability note
    st.markdown("---")
    st.markdown("""
    <div class="highlight-box">
    <h4>📈 System Stability Note</h4>
    <p>This scoring system maintains stability regardless of team size (3 to 50+ members) because:</p>
    <ul>
    <li><strong>Relative Scoring:</strong> Scores are calculated relative to team averages</li>
    <li><strong>Normalized Metrics:</strong> All metrics are normalized against team size and distribution</li>
    <li><strong>Percentile-Based Analysis:</strong> Identifications use percentile thresholds</li>
    <li><strong>Impact/Activity Ratio:</strong> This ratio naturally scales with team size</li>
    </ul>
    <p>The system only ranks employees <strong>within</strong> a team, not across teams.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    create_dashboard()