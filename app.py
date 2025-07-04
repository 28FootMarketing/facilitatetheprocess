
import streamlit as st
import ollama
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# ✅ Set page config early
st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="wide")

# ✅ Load environment
load_dotenv()

# ✅ Define NFHS Sports
NFHS_SPORTS = [
    "Baseball", "Basketball", "Bowling", "Cheerleading", "Cross Country",
    "Esports", "Field Hockey", "Football", "Golf", "Gymnastics",
    "Ice Hockey", "Lacrosse", "Rifle", "Soccer", "Softball",
    "Spirit", "Swimming & Diving", "Tennis", "Track & Field", "Volleyball",
    "Water Polo", "Weightlifting", "Wrestling", "Girls Flag Football"
]

# ✅ Define AI Agents
AGENTS = {
    "Jordan": {"emoji": "🏀", "system_prompt": "You are Jordan, the motivator who builds athlete confidence."},
    "Kobe": {"emoji": "🐍", "system_prompt": "You are Kobe, the disciplined coach who emphasizes preparation."},
    "Lisa": {"emoji": "🎓", "system_prompt": "You are Lisa, the parent communicator who bridges family engagement."},
    "Magic": {"emoji": "🎩", "system_prompt": "You are Magic, the connector who links athletes with opportunities."},
    "Dawn": {"emoji": "🧘", "system_prompt": "You are Dawn, the emotional coach who helps reset focus and calm nerves."}
}

# ✅ Session defaults
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Jordan"
    st.session_state.messages = [{"role": "system", "content": AGENTS["Jordan"]["system_prompt"]}]

for key in ["name", "sport", "grade", "gpa", "motivation", "outreach", "stat1", "stat2", "stat3", "video_link"]:
    st.session_state.setdefault(key, "")

# ✅ Sidebar agent selection
with st.sidebar:
    st.markdown("## 🤖 Choose Your Recruiting Coach")
    for agent_name, agent_info in AGENTS.items():
        if st.button(f"{agent_info['emoji']} {agent_name}"):
            if st.session_state.selected_agent != agent_name:
                st.session_state.selected_agent = agent_name
                st.session_state.messages = [{"role": "system", "content": AGENTS[agent_name]["system_prompt"]}]
                st.experimental_rerun()
    st.markdown(f"**Active Agent:** {AGENTS[st.session_state.selected_agent]['emoji']} {st.session_state.selected_agent}")

# ✅ Layout Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📍 Step 1: Profile Setup",
    "🎥 Step 2: Film Room",
    "📬 Step 3: Coach Outreach",
    "🧠 Step 4: Recruiting Education",
    "🔍 Step 5: Match Finder",
    "📆 Step 6: Timeline Builder",
    "📊 Step 7: Daily Tracker"
])

# ✅ Step 1: Profile Setup
with tab1:
    st.subheader("📍 Step 1: Profile Setup")
    st.session_state.name = st.text_input("Athlete Name", st.session_state.name)
    st.session_state.sport = st.selectbox("Sport", NFHS_SPORTS, index=0)
    st.session_state.grade = st.selectbox("Current Grade", ["9th", "10th", "11th", "12th"], index=0)
    st.session_state.gpa = st.text_input("Current GPA", st.session_state.gpa)
    st.session_state.motivation = st.slider("Motivation Level", 1, 10, 5)
    st.session_state.outreach = st.radio("Have you contacted any college coaches yet?", ["Yes", "No"])

# ✅ Step 2: Film Room
with tab2:
    selected_agent = st.session_state.selected_agent
    st.header(f"{AGENTS[selected_agent]['emoji']} Chat with {selected_agent}")
    st.session_state.video_link = st.text_input("Highlight Video Link (YouTube, Hudl, etc.)", st.session_state.video_link)
    if st.session_state.video_link:
        st.video(st.session_state.video_link)
    user_input = st.chat_input(f"What do you want to ask {selected_agent}?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner(f"{selected_agent} is responding..."):
            try:
                response = ollama.chat(model="llama3", messages=st.session_state.messages)
                reply = response["message"]["content"]
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"🚫 Ollama call failed: {e}")
    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).markdown(msg["content"])
    st.button("🔗 Go to Dashboard")
