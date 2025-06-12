
import streamlit as st
import openai
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# ✅ Load environment variables
load_dotenv()

# ✅ Assign OpenAI key
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("🚫 OpenAI API key is missing.")
    st.stop()
openai.api_key = api_key
client = openai.OpenAI()

# ✅ Streamlit page config
st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="wide")

# ✅ Define agents
AGENTS = {
    "Jordan": {"emoji": "🏀", "system_prompt": "You are Jordan, the motivator..."},
    "Kobe": {"emoji": "🐍", "system_prompt": "You are Kobe, the discipline coach..."},
    "Lisa": {"emoji": "🎓", "system_prompt": "You are Lisa, the parent communicator..."},
    "Magic": {"emoji": "🎩", "system_prompt": "You are Magic, the connector..."},
    "Dawn": {"emoji": "🧘", "system_prompt": "You are Dawn, the emotional reset coach..."}
}

if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Jordan"
    st.session_state.messages = [{"role": "system", "content": AGENTS["Jordan"]["system_prompt"]}]

for key in ["name", "sport", "grade", "gpa", "motivation", "outreach", "stat1", "stat2", "stat3", "video_link"]:
    st.session_state.setdefault(key, "")

with st.sidebar:
    st.markdown("## 🤖 Choose Your Recruiting Coach")
    for agent_name, agent_info in AGENTS.items():
        if st.button(f"{agent_info['emoji']} {agent_name}"):
            if st.session_state.selected_agent != agent_name:
                st.session_state.selected_agent = agent_name
                st.session_state.messages = [{"role": "system", "content": AGENTS[agent_name]["system_prompt"]}]
                st.experimental_rerun()
    st.markdown(f"**Active Agent:** {AGENTS[st.session_state.selected_agent]['emoji']} {st.session_state.selected_agent}")

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
    st.header("📋 Step 1: Build Your Recruiting Profile")
    with st.form("recruiting_form"):
        st.session_state.name = st.text_input("First Name", value=st.session_state.name)
        st.session_state.sport = st.text_input("Your Sport", value=st.session_state.sport)
        st.session_state.grade = st.selectbox("Grade", ["8th", "9th", "10th", "11th", "12th", "Post-grad"])
        st.session_state.gpa = st.number_input("GPA", 0.0, 4.5, step=0.1)
        st.session_state.motivation = st.slider("Motivation (1–10)", 1, 10, 5)
        st.session_state.outreach = st.radio("Have you contacted coaches?", ["Yes", "No"])
        st.subheader("🎯 Athletic Stats")
        st.session_state.stat1 = st.number_input("Stat 1", step=0.1)
        st.session_state.stat2 = st.number_input("Stat 2", step=0.1)
        st.session_state.stat3 = st.number_input("Stat 3", step=0.1)
        st.session_state.video_link = st.text_input("🎥 Highlight Video Link")
        if st.form_submit_button("🔒 Save Info"):
            st.success("✅ Info saved.")

with tab2:
    selected_agent = st.session_state.selected_agent
    st.header(f"{AGENTS[selected_agent]['emoji']} Chat with {selected_agent}")
    user_input = st.chat_input(f"What do you want to ask {selected_agent}?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner(f"{selected_agent} is responding..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).markdown(msg["content"])

with tab3:
    st.header("📄 Download Your AI-Powered Recruiting Report")
    full_chat = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages[1:]])
    if st.button("📥 Generate PDF"):
        pdf_bytes = generate_pdf_from_chat(
            name=st.session_state.name,
            sport=st.session_state.sport,
            video_link=st.session_state.video_link,
            chat_transcript=full_chat
        )
        st.download_button("⬇️ Download Report", data=pdf_bytes, file_name=f"{st.session_state.name}_recruiting_plan.pdf")
