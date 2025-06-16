
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
import openai
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# Load .env variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Ensure API key is set
if not api_key:
    st.error("🚫 OpenAI API key is missing.")
    st.stop()

# Configure OpenAI client (v1.x+ syntax)
client = openai.OpenAI(api_key=api_key)

# Set Streamlit page config FIRST
st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="wide")

# Define NFHS sports list
NFHS_SPORTS = [
    "Baseball", "Basketball", "Bowling", "Cheerleading", "Cross Country",
    "Esports", "Field Hockey", "Football", "Golf", "Gymnastics", "Ice Hockey",
    "Lacrosse", "Rifle", "Soccer", "Softball", "Spirit", "Swimming & Diving",
    "Tennis", "Track & Field", "Volleyball", "Water Polo", "Weightlifting",
    "Wrestling", "Girls Flag Football"
]

# AI agents setup
AGENTS = {
    "Jordan": {"emoji": "🏀", "system_prompt": "You are Jordan, the motivator..."},
    "Kobe": {"emoji": "🐍", "system_prompt": "You are Kobe, the discipline coach..."},
    "Lisa": {"emoji": "🎓", "system_prompt": "You are Lisa, the parent communicator..."},
    "Magic": {"emoji": "🎩", "system_prompt": "You are Magic, the connector..."},
    "Dawn": {"emoji": "🧘", "system_prompt": "You are Dawn, the emotional reset coach..."}
}

# Initialize session state
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Jordan"
    st.session_state.messages = [{"role": "system", "content": AGENTS["Jordan"]["system_prompt"]}]
for key in ["name", "sport", "grade", "gpa", "motivation", "outreach", "stat1", "stat2", "stat3", "video_link"]:
    st.session_state.setdefault(key, "")

# Sidebar - agent selector
with st.sidebar:
    st.markdown("## 🤖 Choose Your Recruiting Coach")
    for agent_name, info in AGENTS.items():
        if st.button(f"{info['emoji']} {agent_name}"):
            if st.session_state.selected_agent != agent_name:
                st.session_state.selected_agent = agent_name
                st.session_state.messages = [{"role": "system", "content": info["system_prompt"]}]
                st.experimental_rerun()
    st.markdown(f"**Active Agent:** {AGENTS[st.session_state.selected_agent]['emoji']} {st.session_state.selected_agent}")

# Tab Layout
tabs = st.tabs([
    "📍 Step 1: Profile Setup", "🎥 Step 2: Film Room", "📬 Step 3: Coach Outreach",
    "🧠 Step 4: Recruiting Education", "🔍 Step 5: Match Finder",
    "📆 Step 6: Timeline Builder", "📊 Step 7: Daily Tracker"
])
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = tabs

# STEP 1: Profile Setup
with tab1:
    st.subheader("📍 Step 1: Profile Setup")
    st.session_state.name = st.text_input("Athlete Name", st.session_state.name)
    st.session_state.sport = st.selectbox("Sport", NFHS_SPORTS, index=0)
    st.session_state.grade = st.selectbox("Current Grade", ["9th", "10th", "11th", "12th"], index=0)
    st.session_state.gpa = st.text_input("Current GPA", st.session_state.gpa)
    st.session_state.motivation = st.slider("Motivation Level", 1, 10, 5)
    st.session_state.outreach = st.radio("Have you contacted any college coaches yet?", ["Yes", "No"])

# STEP 2: Film Room
with tab2:
    st.subheader("🎥 Step 2: Film Room")
    agent = st.session_state.selected_agent
    st.session_state.video_link = st.text_input("Highlight Video Link", st.session_state.video_link)
    if st.session_state.video_link:
        st.video(st.session_state.video_link)

    user_input = st.chat_input(f"What do you want to ask {agent}?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner(f"{agent} is responding..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"🚫 OpenAI API call failed: {e}")
    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).markdown(msg["content"])

# STEP 3: Coach Outreach
with tab3:
    st.subheader("📬 Step 3: Coach Outreach")
    email_template = f"""Subject: {st.session_state.name} | {st.session_state.sport} Student-Athlete

Dear Coach,

My name is {st.session_state.name}, and I am currently in {st.session_state.grade} grade. I am passionate about {st.session_state.sport} and would love the opportunity to learn more about your program.

Sincerely,
{st.session_state.name}"""
    st.code(email_template)

# STEP 4: Recruiting Education
with tab4:
    st.subheader("🧠 Step 4: Recruiting Education")
    st.markdown("- NCAA/NAIA Eligibility")
    st.markdown("- Highlight Tape Strategy")
    st.markdown("- When to Email vs. Call Coaches")
    st.markdown("- Unofficial vs. Official Visits")

# STEP 5: Match Finder
with tab5:
    st.subheader("🔍 Step 5: Match Finder")
    st.session_state.stat1 = st.text_input("Key Stat #1")
    st.session_state.stat2 = st.text_input("Key Stat #2")
    st.session_state.stat3 = st.text_input("Key Stat #3")
    score = calculate_strength_score(st.session_state.stat1, st.session_state.stat2, st.session_state.stat3)
    package = recommend_package(score)
    st.success(f"Suggested Match Strength: {score} | Recommended Package: {package}")

# STEP 6: Timeline Builder
with tab6:
    st.subheader("📆 Step 6: Timeline Builder")
    today = datetime.now().date()
    st.date_input("Coach Evaluation Date", today)
    st.date_input("Target Commitment Date")

# STEP 7: Daily Tracker
with tab7:
    st.subheader("📊 Step 7: Daily Tracker")
    checklist = [
        "Sent follow-up email to coach",
        "Updated highlight video",
        "Reviewed recruiting tips",
        "Trained or conditioned today"
    ]
    checked = [st.checkbox(item) for item in checklist]
    st.write(f"✅ Tasks completed: {sum(checked)} / {len(checklist)}")
