
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

# ✅ Load environment (optional for other config, not used for Ollama)
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

# ✅ Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📍 Step 1: Profile Setup",
    "🎥 Step 2: Film Room",
    "📬 Step 3: Coach Outreach",
    "🧠 Step 4: Recruiting Education",
    "🔍 Step 5: Match Finder",
    "📆 Step 6: Timeline Builder",
    "📊 Step 7: Daily Tracker (Candace)"
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
                response = ollama.chat(
                    model="llama3",
                    messages=st.session_state.messages
                )
                reply = response["message"]["content"]
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"🚫 Ollama chat failed: {e}")
    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).markdown(msg["content"])

# Step 3: Coach Outreach
with tab3:
    st.subheader("📬 Step 3: Coach Outreach")
    st.write("Use this draft as a starting point. Add your voice!")

    subject = f"{st.session_state.name} | {st.session_state.sport} Recruit | Class of {st.session_state.grade}"
    body = f"""
Hi Coach,

My name is {st.session_state.name}, a {st.session_state.grade} grade student-athlete passionate about {st.session_state.sport}. I have been training consistently and am looking for a program where I can grow both athletically and academically.

Here's my highlight video: {st.session_state.video_link or 'Insert Link'}

I’d love to know:
- What kind of athletes do you prioritize in your program?
- When would be a good time to speak with you or a staff member?
- Are you currently recruiting for my position?

Looking forward to hearing from you.

Best,  
{st.session_state.name}
"""

    st.text_area("📧 Email Subject", subject)
    st.text_area("📧 Email Body", body, height=200)
    st.download_button("📤 Download Email Draft", body, file_name="coach_outreach_email.txt")

# Step 4: Recruiting Education
with tab4:
    st.subheader("🧠 Step 4: Recruiting Education")
    st.markdown("Choose a category to explore:")
    edu_topic = st.selectbox("📘 Recruiting Topic", [
        "NCAA/NAIA Eligibility",
        "Highlight Tape Strategy",
        "Coach Communication Do’s & Don’ts",
        "Unofficial vs. Official Visits"
    ])

    edu_info = {
        "NCAA/NAIA Eligibility": "You’ll need a Core GPA of 2.3+ and 16 core courses...",
        "Highlight Tape Strategy": "Your tape should open with 3-5 standout plays...",
        "Coach Communication Do’s & Don’ts": "DO personalize your message. DON’T copy-paste the same email...",
        "Unofficial vs. Official Visits": "Unofficial visits are paid by you. Official visits include travel & lodging..."
    }

    st.info(edu_info.get(edu_topic, "Select a topic to get started."))
    st.download_button("📝 Download Recruiting Checklist", "\n".join(edu_info.values()), file_name="recruiting_education.txt")

# Step 5: Match Finder
with tab5:
    st.subheader("🔍 Step 5: Match Finder")
    st.markdown("Input three key performance metrics for your sport (e.g., PPG, 40-yard dash, vertical jump).")

    st.session_state.stat1 = st.text_input("Key Stat #1 (e.g., Points Per Game)", st.session_state.get("stat1", ""), key="stat_input_1")
    st.session_state.stat2 = st.text_input("Key Stat #2 (e.g., 40-Yard Dash Time)", st.session_state.get("stat2", ""), key="stat_input_2")
    st.session_state.stat3 = st.text_input("Key Stat #3 (e.g., Vertical Jump)", st.session_state.get("stat3", ""), key="stat_input_3")

    if st.session_state.stat1 and st.session_state.stat2 and st.session_state.stat3:
        try:
            score = calculate_strength_score(st.session_state.stat1, st.session_state.stat2, st.session_state.stat3)
            package = recommend_package(score)
            st.success(f"🏅 Match Strength Score: **{score}**")
            st.info(f"📦 Recommended Recruiting Package: **{package}**")
        except Exception as e:
            st.error(f"❌ Error calculating match score: {e}")
    else:
        st.warning("⚠️ Please enter all three stats to calculate your match strength.")

# Step 6: Timeline Builder
with tab6:
    st.subheader("📆 Step 6: Timeline Builder")
    today = datetime.now().date()
    eval_date = st.date_input("📌 Coach Evaluation Target", today)
    visit_window = st.date_input("🏫 Ideal Visit Window", today)
    commit_goal = st.date_input("✍️ Commitment Goal", today)

    st.markdown("**🧭 Suggested Timeline Milestones:**")
    st.markdown("- 📅 Every 60 days: Send update emails to coaches")
    st.markdown("- 🎥 Quarterly: Update highlight video")
    st.markdown("- 📝 Before Evaluation: Review eligibility & transcripts")

    timeline_text = f"""
📌 Evaluation Date: {eval_date}
🏫 Visit Window: {visit_window}
✍️ Commitment Goal: {commit_goal}
Milestones:
- Send coach updates every 60 days.
- Film review every 3 months.
- Academic check before visits.
"""

    st.download_button("📥 Export Timeline", timeline_text, file_name="recruiting_timeline.txt")

# Step 7: Daily Tracker (Candace)
with tab7:
    st.subheader("📊 Step 7: Daily Tracker")

    st.markdown("**📝 Daily Action Checklist**")
    daily_checklist = [
        "Sent follow-up email to a coach",
        "Trained or conditioned today",
        "Watched game film",
        "Updated recruiting profile or video",
        "Reviewed academic progress"
    ]
    completed_tasks = [st.checkbox(task) for task in daily_checklist]
    task_count = sum(completed_tasks)
    st.success(f"✅ {task_count} / {len(daily_checklist)} tasks completed today")

    st.markdown("---")
    st.markdown("**📓 Daily Reflection Journal**")
    st.session_state.mood = st.selectbox("Mood Today", ["😃 Great", "🙂 Okay", "😐 Meh", "😔 Struggling"])
    st.session_state.reflection = st.text_area("What went well today? What needs work?")

    # Generate AI feedback using Dawn (Emotional Reset Agent)
    if st.button("💬 Get Feedback from Dawn"):
        with st.spinner("Dawn is reflecting..."):
            response = client.chat.completions.create(
                model="ollama/llama3",
                messages=[
                    {"role": "system", "content": AGENTS["Dawn"]["system_prompt"]},
                    {"role": "user", "content": f"My mood today: {st.session_state.mood}. Reflection: {st.session_state.reflection}"}
                ]
            )
            dawn_reply = response.choices[0].message.content.strip()
            st.markdown(f"**🧘 Dawn says:**\n\n{dawn_reply}")

    st.markdown("---")
    st.markdown("**📎 Export Today’s Summary**")
    summary_text = f"""
🗓️ Date: {datetime.now().strftime('%Y-%m-%d')}
Mood: {st.session_state.mood}
Tasks Completed: {task_count} / {len(daily_checklist)}

Reflection:
{st.session_state.reflection or 'N/A'}
"""
    st.download_button("📥 Download Tracker Summary", summary_text, file_name="daily_tracker_summary.txt")
