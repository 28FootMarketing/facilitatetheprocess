import streamlit as st
import openai
import os

# ✅ MUST BE FIRST Streamlit command
st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="wide")

from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# ✅ OpenAI API Key Handling (Cloud + Local Dev)
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    openai.api_key = os.getenv("OPENAI_API_KEY", "sk-missing-key")
    st.warning("Using fallback API key. Make sure it's set via st.secrets or .env.")

# ✅ Agent Configuration (Phase 5)
AGENTS = {
    "Jordan": {
        "emoji": "🏀",
        "system_prompt": "You are Jordan, the ultimate motivator. Encourage confidence and explain recruiting simply and powerfully."
    },
    "Kobe": {
        "emoji": "🐍",
        "system_prompt": "You are Kobe, the discipline coach. Push athletes to commit, prepare, and stay sharp in their recruiting journey."
    },
    "Lisa": {
        "emoji": "🎓",
        "system_prompt": "You are Lisa, the guide for parents and athletes. Help them organize, communicate, and stay clear on next steps."
    },
    "Magic": {
        "emoji": "🎩",
        "system_prompt": "You are Magic, the opportunity finder. Help athletes expand their network and unlock new options for recruiting."
    },
    "Dawn": {
        "emoji": "🧘",
        "system_prompt": "You are Dawn, the emotional reset coach. Help athletes reflect, reset, and stay focused through mental check-ins."
    }
}

# ✅ Session State Init
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Jordan"
    st.session_state.messages = [
        {"role": "system", "content": AGENTS["Jordan"]["system_prompt"]}
    ]

if "name" not in st.session_state:
    st.session_state.name = ""
    st.session_state.sport = ""
    st.session_state.grade = ""
    st.session_state.gpa = 0.0
    st.session_state.motivation = 5
    st.session_state.outreach = "No"
    st.session_state.stat1 = 0.0
    st.session_state.stat2 = 0.0
    st.session_state.stat3 = 0.0
    st.session_state.video_link = ""

# ✅ Agent Picker (Sidebar)
with st.sidebar:
    st.markdown("## 🤖 Choose Your Recruiting Coach")
    for agent_name, agent_info in AGENTS.items():
        if st.button(f"{agent_info['emoji']} {agent_name}"):
            st.session_state.selected_agent = agent_name
            st.session_state.messages = [
                {"role": "system", "content": AGENTS[agent_name]["system_prompt"]}
            ]
            st.experimental_rerun()

    st.sidebar.markdown(f"**Active Agent:** {AGENTS[st.session_state.selected_agent]['emoji']} **{st.session_state.selected_agent}**")

# ✅ Main UI Tabs
tab1, tab2, tab3 = st.tabs(["📋 Step 1: My Recruiting Info", "💬 Step 2: Ask Your Coach", "📄 Step 3: Download Report"])

# 📋 STEP 1 — Recruiting Profile Form
with tab1:
    st.header("📋 Step 1: Build Your Recruiting Profile")
    with st.form("recruiting_form"):
        st.session_state.name = st.text_input("First Name", value=st.session_state.name)
        st.session_state.sport = st.text_input("Sport", value=st.session_state.sport)
        st.session_state.grade = st.selectbox("Grade", ["8th", "9th", "10th", "11th", "12th", "Post-grad"], index=2)
        st.session_state.gpa = st.number_input("GPA", min_value=0.0, max_value=4.5, step=0.1, value=st.session_state.gpa)
        st.session_state.motivation = st.slider("Motivation (1–10)", 1, 10, value=st.session_state.motivation)
        st.session_state.outreach = st.radio("Have you contacted any college coaches?", ["Yes", "No"], index=1)

        st.subheader("🎯 Athletic Stats")
        st.session_state.stat1 = st.number_input("Stat 1", step=0.1, value=st.session_state.stat1)
        st.session_state.stat2 = st.number_input("Stat 2", step=0.1, value=st.session_state.stat2)
        st.session_state.stat3 = st.number_input("Stat 3", step=0.1, value=st.session_state.stat3)

        st.session_state.video_link = st.text_input("🎥 Highlight Video (Hudl, YouTube)", value=st.session_state.video_link)

        if st.form_submit_button("🔒 Save Info"):
            st.success("✅ Info saved. Go to Step 2 to talk to your coach.")

# 💬 STEP 2 — GPT Chat With Selected Agent
with tab2:
    selected_agent = st.session_state.selected_agent
    st.header(f"{AGENTS[selected_agent]['emoji']} Chat with {selected_agent}")

    user_input = st.chat_input(f"What do you want to ask {selected_agent}?")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner(f"{selected_agent} is responding..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).markdown(msg["content"])

# 📄 STEP 3 — Generate PDF Report
with tab3:
    st.header("📄 Download Your AI-Powered Recruiting Report")

    # Combine all messages for context
    full_chat = "\n".join([
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.messages[1:]
    ])

    # Generate PDF report from chat + user info
    if st.button("📥 Generate PDF"):
        pdf_bytes = generate_pdf_from_chat(
            name=st.session_state.name,
            sport=st.session_state.sport,
            video_link=st.session_state.video_link,
            chat_transcript=full_chat
        )
        st.download_button(
            label="⬇️ Download Report",
            data=pdf_bytes,
            file_name=f"{st.session_state.name}_recruiting_plan.pdf"
        )

    # === Recruiting Timeline Section ===
    st.header("📆 Custom 4-Week Recruiting Timeline")

    if st.button("📅 Generate Weekly Plan"):
        context_summary = f"""
        Name: {st.session_state.name}
        Sport: {st.session_state.sport}
        Grade: {st.session_state.grade}
        GPA: {st.session_state.gpa}
        Motivation: {st.session_state.motivation}
        Has contacted coaches: {st.session_state.outreach}
        Recent Conversation:
        {full_chat}
        """

        prompt = f"""
        Based on the following student-athlete profile and conversation, generate a 4-week recruiting timeline.
        Break it into Week 1, Week 2, Week 3, and Week 4.
        Each week should have 2–3 actionable recruiting tasks.
        Keep the tone motivational and simple.
        ===
        {context_summary}
        """

        with st.spinner("Building your timeline..."):
            timeline_response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a recruiting strategist who helps student-athletes build weekly action plans to increase exposure and coach interaction."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            timeline_text = timeline_response["choices"][0]["message"]["content"]
            st.markdown("### 📝 Your 4-Week Action Plan")
            st.markdown(timeline_text)
