
import streamlit as st
import openai
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# Load environment variables
load_dotenv()

# Securely get API Key
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("🚫 OpenAI API key is missing.")
    st.stop()
openai.api_key = api_key

# Page setup
st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="wide")

# Define AI Agents
AGENTS = {
    "Jordan": {"emoji": "🏀", "system_prompt": "You are Jordan, the motivator..."},
    "Kobe": {"emoji": "🐍", "system_prompt": "You are Kobe, the discipline coach..."},
    "Lisa": {"emoji": "🎓", "system_prompt": "You are Lisa, the parent communicator..."},
    "Magic": {"emoji": "🎩", "system_prompt": "You are Magic, the connector..."},
    "Dawn": {"emoji": "🧘", "system_prompt": "You are Dawn, the emotional reset coach..."}
}

# Set default session state
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Jordan"
    st.session_state.messages = [{"role": "system", "content": AGENTS["Jordan"]["system_prompt"]}]

# Initialize form fields
for key in ["name", "sport", "grade", "gpa", "motivation", "outreach", "stat1", "stat2", "stat3", "video_link"]:
    st.session_state.setdefault(key, "")

# Sidebar – Agent selection
with st.sidebar:
    st.markdown("## 🤖 Choose Your Recruiting Coach")
    for agent_name, agent_info in AGENTS.items():
        if st.button(f"{agent_info['emoji']} {agent_name}"):
            if st.session_state.selected_agent != agent_name:
                st.session_state.selected_agent = agent_name
                st.session_state.messages = [{"role": "system", "content": AGENTS[agent_name]["system_prompt"]}]
                st.experimental_rerun()
    st.markdown(f"**Active Agent:** {AGENTS[st.session_state.selected_agent]['emoji']} {st.session_state.selected_agent}")

# Main tab interface
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📍 Step 1: Profile Setup",
    "🎥 Step 2: Film Room",
    "📬 Step 3: Coach Outreach",
    "🧠 Step 4: Recruiting Education",
    "🔍 Step 5: Match Finder",
    "📆 Step 6: Timeline Builder",
    "📊 Step 7: Daily Tracker (Candace)"
])

with tab1:
    st.subheader("Step 1: Profile Setup")
    st.text_input("Full Name", key="name")
    st.selectbox("Sport", ["Football", "Basketball", "Soccer", "Track", "Other"], key="sport")
    st.selectbox("Current Grade", ["9", "10", "11", "12", "Graduated"], key="grade")
    st.text_input("GPA", key="gpa")
    st.text_area("Motivation Level (1–10 scale)", key="motivation")
    st.text_area("Coach Outreach Status", key="outreach")

with tab3:
    st.subheader("Step 3: Coach Outreach")
    st.markdown("⚠️ Outreach automation in progress. You’ll be able to track messages, status, and follow-ups here.")

with tab4:
    st.subheader("Step 4: Recruiting Education")
    st.markdown("🎓 Lessons, webinars, and prep modules will appear here.")

with tab5:
    st.subheader("Step 5: Match Finder")
    st.markdown("🔍 AI-assisted matchmaking with colleges — COMING SOON.")

with tab6:
    st.subheader("Step 6: Timeline Builder")
    st.markdown("📆 Recruiting timeline, reminders, and task planner setup will show here.")

with tab7:
    st.subheader("Step 7: Daily Tracker (Candace)")
    st.markdown("📊 Track your workouts, emails, film sent, and more here.")

# Agent chat tab
with tab2:
    selected_agent = st.session_state.selected_agent
    st.header(f"{AGENTS[selected_agent]['emoji']} Chat with {selected_agent}")

    # User input
    user_input = st.chat_input(f"What do you want to ask {selected_agent}?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Validation check
        for msg in st.session_state.messages:
            if "role" not in msg or "content" not in msg:
                st.error("❌ Invalid message format.")
                st.stop()

        # OpenAI chat completion
        with st.spinner(f"{selected_agent} is responding..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message["content"]
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"🚫 OpenAI API call failed: {e}")

    # Chat display
    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).markdown(msg["content"])
