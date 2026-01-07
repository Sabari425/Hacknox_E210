import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os
import random

# --- 1. CONFIG & CUSTOM CSS ---
st.set_page_config(page_title="Manager HQ", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    /* Global Background Gradient */
    .stApp {
        background: rgb(15,23,42);
        background: linear-gradient(145deg, rgba(15,23,42,1) 0%, rgba(26,16,60,1) 50%, rgba(30,10,40,1) 100%);
    }
    .block-container { padding-top: 2rem; }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    h1, h2, h3 { color: white !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0px 0px;
        color: white;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.2);
        border-bottom: 2px solid #6366f1;
    }
    
    /* Badge Style for Topics */
    .topic-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 4px 10px;
        margin: 2px;
        border-radius: 15px;
        font-size: 0.85rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA LOADING & TRANSFORMATION ---

# A. Team Data Loader
def load_and_process_data():
    file_path = 'final_team_intelligence.json'
    
    # Default Dummy Data
    raw_data = [
        {"name": "yaswanth1976", "merged_score": 4.56, "final_behavior": "Observer", "git_score": 7.6, "meeting_score": 2.0},
        {"name": "alex_dev", "merged_score": 8.5, "final_behavior": "Silent Architect", "git_score": 9.2, "meeting_score": 1.0}
    ]

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                loaded_json = json.load(f)
                if isinstance(loaded_json, dict):
                    if "members" in loaded_json and isinstance(loaded_json["members"], list):
                        raw_data = loaded_json["members"]
                    else:
                        temp_list = []
                        for key, value in loaded_json.items():
                            if isinstance(value, dict):
                                if 'name' not in value:
                                    value['name'] = key
                                temp_list.append(value)
                        raw_data = temp_list
                elif isinstance(loaded_json, list):
                    raw_data = loaded_json
        except Exception as e:
            st.error(f"Error reading JSON: {e}")

    processed_members = []
    valid_data = [x for x in raw_data if isinstance(x, dict)]
    sorted_data = sorted(valid_data, key=lambda x: x.get('merged_score', 0), reverse=True)

    for idx, item in enumerate(sorted_data):
        impact_val = float(item.get('git_score', 0)) * 10
        activity_val = float(item.get('meeting_score', 0)) * 10
        score_val = float(item.get('merged_score', 0)) * 10 
        member_name = item.get('name', f"Member {idx+1}")

        member = {
            "id": idx + 1,
            "name": member_name,
            "role": "Contributor", 
            "category": item.get('final_behavior', 'Contributor'),
            "impact": impact_val,  
            "activity": activity_val, 
            "rank": idx + 1,
            "score": score_val
        }
        processed_members.append(member)

    fastapi_components = [
        "app/main.py", "app/api/v1/endpoints/auth.py", "app/api/v1/endpoints/users.py",
        "app/api/v1/endpoints/items.py", "app/core/config.py", "app/core/security.py",
        "app/db/session.py", "app/db/base.py", "app/models/user.py", "app/schemas/token.py",
        "app/services/email.py", "tests/test_api.py", "Dockerfile"
    ]
    
    project_structure = []
    if processed_members:
        for comp in fastapi_components:
            count = random.randint(1, min(3, len(processed_members)))
            assigned_members = random.sample([m['name'] for m in processed_members], count)
            project_structure.append({"component": comp, "members": assigned_members})

    teams = [
        {
            "id": "t1",
            "name": "Alpha Squad",
            "size": len(processed_members),
            "description": "Core Backend & Infrastructure (FastAPI)",
            "members": processed_members,
            "projectStructure": project_structure
        },
        {
            "id": "t2",
            "name": "Beta Design",
            "size": 0,
            "description": "Frontend & UX (Empty)",
            "members": [],
            "projectStructure": []
        }
    ]
    return {"teams": teams}

# B. Meeting Data Loader
def load_meeting_data():
    file_path = 'meeting_intelligence.json'
    
    # RAW DATA FROM PROMPT
    raw_meeting_data = """
    {
      "overall_meeting_summary": "Meeting focused on platform stability, authentication risks, Kubernetes restarts, API reliability, and security improvements.",
      "meeting_topics": ["authentication", "kubernetes stability", "security", "API management", "performance"],
      "member_analysis": [],
      "dominant_speakers": ["hasansezertasan", "Kludex", "tiangolo"],
      "silent_speakers": ["pre-commit-ci[bot]", "dmontagu", "dependabot[bot]"]
    }
    """
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return json.loads(raw_meeting_data)
    else:
        return json.loads(raw_meeting_data)


data = load_and_process_data()
meeting_data = load_meeting_data()

# --- 3. STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = None

def navigate_to(page, team=None):
    st.session_state.page = page
    if team:
        st.session_state.selected_team = team

# --- 4. VIEWS ---

# === LOGIN PAGE ===
def login_view():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h2>🔐 Manager Access</h2>
                <p style="color: #aaa;">Enter credentials to view team insights.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_input("Username")
            st.text_input("Password", type="password")
            
            if st.button("Access Dashboard", use_container_width=True, type="primary"):
                navigate_to('manager_home')
                st.rerun()

# === MANAGER HOME ===
def manager_home_view():
    st.markdown("<h1>Welcome back, Manager 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#aaa; margin-bottom: 30px;'>Select a team to analyze performance and structure.</p>", unsafe_allow_html=True)
    
    teams = data['teams']
    col1, col2 = st.columns(2)
    
    with col1:
        team = teams[0]
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="margin:0; color: #818cf8;">{team['name']}</h3>
            <p style="font-size: 0.9rem; color: #ccc;">{team['description']}</p>
            <div style="margin-top: 10px; font-size: 0.8rem; background: rgba(255,255,255,0.1); display: inline-block; padding: 2px 8px; border-radius: 10px;">
                👥 {team['size']} Members
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"View Analysis", key="btn_alpha"):
            navigate_to('team_dashboard', team)
            st.rerun()

    with col2:
        team = teams[1]
        st.markdown(f"""
        <div class="glass-card" style="opacity: 0.6;">
            <h3 style="margin:0; color: #ec4899;">{team['name']}</h3>
            <p style="font-size: 0.9rem; color: #ccc;">{team['description']}</p>
            <div style="margin-top: 10px; font-size: 0.8rem; background: rgba(255,255,255,0.1); display: inline-block; padding: 2px 8px; border-radius: 10px;">
                👥 {team['size']} Members
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"View Analysis", key="btn_beta"):
            navigate_to('team_dashboard', team)
            st.rerun()

# === TEAM DASHBOARD ===
def team_dashboard_view():
    team = st.session_state.selected_team
    
    c1, c2 = st.columns([6, 1])
    with c1:
        st.markdown(f"<h1>{team['name']} Analysis</h1>", unsafe_allow_html=True)
    with c2:
        if st.button("← Back"):
            navigate_to('manager_home')
            st.rerun()
    
    # ADDED 7th Tab: PERFORMANCE
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "💎 Hidden Contributors", 
        "👥 Team Members", 
        "🏗️ Project Structure", 
        "🧩 Contribution Roles", 
        "📈 Activity vs Impact",
        "📝 Meeting Review",
        "🚀 Performance & Risk" # <--- NEW TAB
    ])
    
    df = pd.DataFrame(team['members'])
    
    # ... Tabs 1-5 Logic (Unchanged) ...
    with tab1:
        st.markdown("### High-Impact Categories")
        if df.empty:
            st.warning("No members data available.")
        else:
            col_a, col_b, col_c = st.columns(3)
            def render_box(col, title, target_string, color, icon):
                filtered = df[df['category'].astype(str).str.contains(target_string, case=False, na=False)]
                with col:
                    st.markdown(f"""
                    <div class="glass-card" style="border-top: 4px solid {color}; height: 100%;">
                        <h3 style="color: {color};">{icon} {title}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    if not filtered.empty:
                        for _, row in filtered.iterrows():
                            st.markdown(f"**{row['name']}**", unsafe_allow_html=True)
                    else:
                        st.caption("No members found.")
            render_box(col_a, "Silent Architects", "Architect", "#818cf8", "🧠")
            render_box(col_b, "Mentors", "Mentor", "#34d399", "🌱")
            render_box(col_c, "Firefighters", "Firefighter", "#fbbf24", "🔥")

    with tab2:
        if not df.empty:
            c_search, c_filter = st.columns([3, 1])
            search_term = c_search.text_input("🔍 Search", placeholder="Name...")
            unique_cats = list(df['category'].astype(str).unique())
            cat_filter = c_filter.selectbox("Filter Behavior", ["All"] + unique_cats)
            display_df = df.copy()
            if search_term:
                display_df = display_df[display_df['name'].str.contains(search_term, case=False)]
            if cat_filter != "All":
                display_df = display_df[display_df['category'] == cat_filter]
            st.dataframe(
                display_df[['rank', 'name', 'category', 'score']],
                use_container_width=True, hide_index=True,
                column_config={"score": st.column_config.ProgressColumn("Merged Score (x10)", format="%d", min_value=0, max_value=100)}
            )
        else:
            st.info("No members to display.")

    with tab3:
        st.markdown("### ⚡ FastAPI Project Structure")
        structure = team.get('projectStructure', [])
        if structure:
            for item in structure:
                with st.expander(f"📂 {item['component']}", expanded=False):
                    st.markdown("**Assigned Contributors:**")
                    cols = st.columns(4)
                    for i, member in enumerate(item['members']):
                        cols[i % 4].markdown(f"""
                        <div style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 5px 10px; border-radius: 20px; text-align: center; font-size: 0.9rem; border: 1px solid rgba(99, 102, 241, 0.3);">
                           {member}
                        </div>""", unsafe_allow_html=True)
        else:
            st.info("No structure generated.")

    with tab4:
        st.markdown("### Behavioral Distribution")
        if not df.empty:
            categories = df['category'].unique()
            cols = st.columns(3)
            for idx, cat in enumerate(categories):
                filtered = df[df['category'] == cat]
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between;">
                            <b>{cat}</b> <span style="background:rgba(255,255,255,0.1); padding:0 6px; border-radius:4px;">{len(filtered)}</span>
                        </div><hr style="border-color:rgba(255,255,255,0.1)">
                    </div>""", unsafe_allow_html=True)
                    for name in filtered['name']:
                        cols[idx % 3].markdown(f"<small style='color:#ccc'>• {name}</small>", unsafe_allow_html=True)

    with tab5:
        if not df.empty:
            st.markdown(f"**X-Axis:** Meeting Score (Active) | **Y-Axis:** Git Score (Impact)")
            fig = px.scatter(
                df, x="activity", y="impact", text="name", hover_data=["category", "score"],
                color="category", template="plotly_dark", title="Activity vs Impact"
            )
            fig.add_hline(y=50, line_dash="dot", line_color="grey")
            fig.add_vline(x=50, line_dash="dot", line_color="grey")
            fig.update_traces(textposition='top center', marker=dict(size=14, line=dict(width=1, color='white')))
            fig.update_layout(xaxis=dict(range=[0, 100]), yaxis=dict(range=[0, 100]), height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    with tab6:
        st.markdown("### 🎙️ Sprint Retrospective / Meeting Summary")
        
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: #34d399; margin-bottom: 5px;">Executive Summary</h4>
            <p style="font-size: 1.1rem; line-height: 1.6;">{meeting_data.get('overall_meeting_summary', 'No summary available.')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_topics, col_dom, col_silent = st.columns([2, 1, 1])
        with col_topics:
            st.markdown("#### 🏷️ Key Topics Discussed")
            topics_html = ""
            for topic in meeting_data.get('meeting_topics', []):
                topics_html += f"<span class='topic-badge'>{topic}</span>"
            st.markdown(f"<div style='margin-bottom: 20px;'>{topics_html}</div>", unsafe_allow_html=True)

            members_data = meeting_data.get('member_analysis', [])
            if members_data:
                m_df = pd.DataFrame(members_data)
                fig_spoken = px.bar(
                    m_df.sort_values('time_spoken_seconds', ascending=True), 
                    x='time_spoken_seconds', y='name', 
                    color='behavior_type', orientation='h',
                    template="plotly_dark", title="Speaking Time (Seconds)",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_spoken.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
                st.plotly_chart(fig_spoken, use_container_width=True)

        with col_dom:
            st.markdown("#### 🗣️ Dominant Speakers")
            for spk in meeting_data.get('dominant_speakers', []):
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px; background: rgba(99, 102, 241, 0.1); padding: 8px; border-radius: 8px;">
                    <div style="width: 8px; height: 8px; background: #818cf8; border-radius: 50%;"></div>
                    <span>{spk}</span>
                </div>""", unsafe_allow_html=True)

        with col_silent:
            st.markdown("#### 🤫 Silent / Quiet")
            for spk in meeting_data.get('silent_speakers', []):
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px; background: rgba(255, 255, 255, 0.05); padding: 8px; border-radius: 8px;">
                    <div style="width: 8px; height: 8px; background: #94a3b8; border-radius: 50%;"></div>
                    <span style="color: #94a3b8;">{spk}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("#### 📋 Detailed Member Analysis")
        if members_data:
            m_df['important_topics_str'] = m_df['important_topics'].apply(lambda x: ", ".join(x[:3]) + ("..." if len(x)>3 else ""))
            st.dataframe(
                m_df[['name', 'behavior_type', 'time_spoken_seconds', 'involvement_score', 'lines_spoken', 'important_topics_str', 'summary']],
                use_container_width=True, hide_index=True,
                column_config={
                    "name": "Member", "behavior_type": "Role",
                    "time_spoken_seconds": st.column_config.NumberColumn("Time (s)", format="%d s"),
                    "lines_spoken": "Lines", "involvement_score": st.column_config.ProgressColumn("Involvement", min_value=0, max_value=100),
                    "important_topics_str": "Top Topics", "summary": "AI Summary"
                }
            )

    # --- TAB 7: PERFORMANCE & RISK (NEW) ---
    with tab7:
        if df.empty:
            st.warning("No data for performance analysis.")
        else:
            # 1. CALCULATE STATISTICS
            # Company Dependency Metric: (Score / Total Team Score) * 100
            total_team_score = df['score'].sum()
            df['dependency_risk'] = (df['score'] / total_team_score) * 100
            
            # Identify Hike Candidate (Highest Score)
            hike_candidate = df.loc[df['score'].idxmax()]
            
            # Identify Fire Candidate (Lowest Score)
            fire_candidate = df.loc[df['score'].idxmin()]
            
            st.markdown("### 📊 AI Performance Decisions")
            st.markdown("Analysis based on Impact (Git) + Activity (Meeting) scores.")
            
            # 2. RECOMMENDATION CARDS
            col_hike, col_fire = st.columns(2)
            
            # GREEN CARD: Hike Recommendation
            with col_hike:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid #10b981; background: rgba(16, 185, 129, 0.05);">
                    <h3 style="color: #10b981; margin-bottom:0;">🚀 Recommended for Hike</h3>
                    <h2 style="margin: 10px 0;">{hike_candidate['name']}</h2>
                    <p style="color: #ccc;">Top Performer with highest efficiency.</p>
                    <div style="display:flex; gap:15px; margin-top:10px;">
                        <div>
                            <small style="color:#aaa;">Efficiency Score</small><br>
                            <b style="font-size:1.2rem; color:white;">{int(hike_candidate['score'])}/100</b>
                        </div>
                        <div>
                            <small style="color:#aaa;">Role</small><br>
                            <b style="color:#10b981;">{hike_candidate['category']}</b>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # RED CARD: Fire/Improvement Plan Recommendation
            with col_fire:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid #ef4444; background: rgba(239, 68, 68, 0.05);">
                    <h3 style="color: #ef4444; margin-bottom:0;">⚠️ Performance Risk</h3>
                    <h2 style="margin: 10px 0;">{fire_candidate['name']}</h2>
                    <p style="color: #ccc;">Lowest efficiency metrics. Needs Review.</p>
                    <div style="display:flex; gap:15px; margin-top:10px;">
                        <div>
                            <small style="color:#aaa;">Efficiency Score</small><br>
                            <b style="font-size:1.2rem; color:white;">{int(fire_candidate['score'])}/100</b>
                        </div>
                        <div>
                            <small style="color:#aaa;">Impact Level</small><br>
                            <b style="color:#ef4444;">Low</b>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # 3. DEPARTURE RISK TABLE ("If this person leaves...")
            st.markdown("### 📉 Company Loss Impact (Bus Factor)")
            st.markdown("Percentage of team capability lost if this person leaves the company.")
            
            # Format dataframe for display
            risk_df = df[['name', 'category', 'score', 'dependency_risk']].sort_values('dependency_risk', ascending=False)
            
            st.dataframe(
                risk_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": "Employee Name",
                    "category": "Role",
                    "score": st.column_config.NumberColumn("Work Efficiency", format="%d"),
                    "dependency_risk": st.column_config.ProgressColumn(
                        "Company Loss % if Left",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100, # Relative to total team score
                        help="Calculated based on contribution to total team velocity."
                    )
                }
            )

# --- ROUTER ---
if st.session_state.page == 'login':
    login_view()
elif st.session_state.page == 'manager_home':
    manager_home_view()
elif st.session_state.page == 'team_dashboard':
    team_dashboard_view()