import streamlit as st
import openai
import os
import pandas as pd
from datetime import datetime
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# ✅ Must be first Streamlit command
st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="wide")

# ✅ Load OpenAI API Key
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    openai.api_key = os.getenv("OPENAI_API_KEY", "sk-missing-key")
    st.warning("Using fallback API key. Be sure to set one via st.secrets or .env.")

# ✅ Define agents
AGENTS = {
    "Jordan": {"emoji": "🏀", "system_prompt": "You are Jordan, the motivator..."},
    "Kobe": {"emoji": "🐍", "system_prompt": "You are Kobe, the discipline coach..."},
    "Lisa": {"emoji": "🎓", "system_prompt": "You are Lisa, the parent communicator..."},
    "Magic": {"emoji": "🎩", "system_prompt": "You are Magic, the connector..."},
    "Dawn": {"emoji": "🧘", "system_prompt": "You are Dawn, the emotional reset coach..."}
}

# ✅ Init session state
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Jordan"
    st.session_state.messages = [{"role": "system", "content": AGENTS["Jordan"]["system_prompt"]}]

for key in ["name", "sport", "grade", "gpa", "motivation", "outreach", "stat1", "stat2", "stat3", "video_link"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ✅ Sidebar agent picker
with st.sidebar:
    st.markdown("## 🤖 Choose Your Recruiting Coach")
    for agent_name, agent_info in AGENTS.items():
        if st.button(f"{agent_info['emoji']} {agent_name}"):
            if st.session_state.selected_agent != agent_name:
                st.session_state.selected_agent = agent_name
                st.session_state.messages = [
                    {"role": "system", "content": AGENTS[agent_name]["system_prompt"]}
                ]
                st.experimental_rerun()
    st.markdown(f"**Active Agent:** {AGENTS[st.session_state.selected_agent]['emoji']} {st.session_state.selected_agent}")

# ✅ Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📍 Step 1: Profile Setup",
    "🎥 Step 2: Film Room",
    "📬 Step 3: Coach Outreach",
    "🧠 Step 4: Recruiting Education",
    "🔍 Step 5: Match Finder",
    "📆 Step 6: Timeline Builder",
    "📊 Step 7: Daily Tracker (Candace)"
])

# ✅ Tab 1
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

# ✅ Tab 2
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

# ✅ Tab 3
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
    st.header("📆 Custom 4-Week Recruiting Timeline")
    if st.button("📅 Generate Weekly Plan"):
        context_summary = f"""
        Name: {st.session_state.name}
        Sport: {st.session_state.sport}
        Grade: {st.session_state.grade}
        GPA: {st.session_state.gpa}
        Motivation: {st.session_state.motivation}
        Contacted coaches: {st.session_state.outreach}
        Recent conversation: {full_chat}
        """
        prompt = f"""
        Based on this profile and chat, generate a 4-week recruiting timeline with 2–3 tasks per week.
        Keep the tone motivational.
        {context_summary}
        """
        with st.spinner("Building your timeline..."):
            timeline_response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a recruiting strategist."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.markdown("### 📝 Your 4-Week Action Plan")
            st.markdown(timeline_response["choices"][0]["message"]["content"])

# ✅ Tab 4
with tab4:
    st.header("📥 Set Up Your Follow-Up Assistant")
    with st.form("followup_form"):
        lead_name = st.text_input("Your Name", value=st.session_state.name)
        lead_email = st.text_input("Email Address")
        assistant_name = st.text_input("Name Your Assistant", value=st.session_state.get("assistant_name", "Ava"))
        if st.form_submit_button("📩 Send Me the Plan"):
            st.session_state.assistant_name = assistant_name
            try:
                with open("leads.csv", "a") as f:
                    f.write(f"{lead_name},{lead_email},{assistant_name}\n")
            except:
                st.info("📎 CSV not saved in this environment.")
            st.success(f"✅ Thanks, {lead_name}! {assistant_name} will follow up with you soon.")

# ✅ Tab 5 – Khloe memory
if "khloe_memory" not in st.session_state:
    st.session_state.khloe_memory = []

def log_khloe_checkin(status):
    st.session_state.khloe_memory.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status
    })

with tab5:
    st.header("📲 Weekly Check-In with Khloe")
    st.write("Hi, I’m **Khloe** — your consistency coach. Let’s see how you’re progressing this week.")
    khloe_checkin = st.radio("Did you complete your recruiting goals for this week?", ["Yes, I crushed it 💪", "Not yet, still working on it 😅"])
    if khloe_checkin == "Yes, I crushed it 💪":
        st.success("🔥 That’s awesome! Keep the momentum going.")
        st.write("Take 2 minutes to send another message to a coach today!")
        log_khloe_checkin("Yes")
    else:
        st.warning("⏳ No worries. Progress > perfection.")
        st.write("Khloe says: 'Choose one small thing to finish today — even if it’s just rewatching your highlight tape.'")
        log_khloe_checkin("Not Yet")
    if st.checkbox("🕐 Text me next week to check in (Beta)"):
        st.text_input("Phone number (optional for future SMS reminders)")
        st.caption("📬 This reminder will be added to your schedule. Coming soon via SMS.")
    st.markdown("### ⏳ Past Check-Ins")
    for entry in st.session_state.khloe_memory[::-1]:
        st.write(f"🗓️ {entry['timestamp']} — **{entry['status']}**")

# ✅ Tab 6 – Timeline Builder already covered in Tab 3

# ✅ Tab 7
with tab7:
    st.header("📊 Step 6: Daily Tracker (with Candace)")
    st.write("Candace says: _Let’s build your streak one day at a time._")
    today = datetime.now().strftime("%Y-%m-%d")
    if "recruiting_log" not in st.session_state:
        st.session_state.recruiting_log = {}
    st.subheader(f"Tasks for {today}")
    tasks = {
        "Message a coach": False,
        "Watch your game film": False,
        "Update recruiting profile": False,
        "Post highlight on social": False
    }
    for task in tasks:
        current_value = st.session_state.recruiting_log.get(today, {}).get(task, False)
        tasks[task] = st.checkbox(task, value=current_value)
    if st.button("✅ Save Today's Progress"):
        st.session_state.recruiting_log[today] = tasks
        st.success("Progress saved!")
    st.markdown("### 📈 Your Weekly Progress")
    if st.session_state.recruiting_log:
        progress_df = pd.DataFrame.from_dict(st.session_state.recruiting_log, orient="index")
        st.line_chart(progress_df.sum(axis=1))

