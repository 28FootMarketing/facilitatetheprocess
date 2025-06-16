
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

# Step 1: Profile Setup (Enhanced)
with tab1:
    st.subheader("📍 Step 1: Build Your Athletic Profile")

    st.markdown("""
    🧾 This is your **foundation**. Coaches and our AI agents use this info to personalize your recruiting plan.  
    🎯 Fill in everything honestly — this becomes your blueprint.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.name = st.text_input("Full Name", st.session_state.name)
        st.session_state.grade = st.selectbox("Current Grade Level", ["9th", "10th", "11th", "12th"], index=0)
        st.session_state.gpa = st.text_input("GPA (e.g., 3.5)", st.session_state.gpa)
        st.session_state.outreach = st.radio("Have you contacted college coaches yet?", ["Yes", "No"])
    with col2:
        st.session_state.sport = st.selectbox("Your Sport", NFHS_SPORTS, index=0)
        st.session_state.motivation = st.slider("Motivation Level (1–10)", 1, 10, 5)
        st.session_state.video_link = st.text_input("Highlight Video Link (optional)", st.session_state.video_link)

    st.markdown("🔐 **Your Info is Saved** — Log in anytime to update or improve your profile.")

    # Optional CTA or validation check
    if all([st.session_state.name, st.session_state.gpa, st.session_state.sport]):
        st.success("✅ Your profile is off to a strong start! Continue to the next step.")
    else:
        st.warning("⚠️ Fill in all key fields to unlock personalized recommendations.")

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

    st.markdown("### 🎯 Personalized Learning for Your Recruiting Journey")

    # Track completion and quiz performance
    if "edu_completed" not in st.session_state:
        st.session_state.edu_completed = set()
    if "quiz_incorrect" not in st.session_state:
        st.session_state.quiz_incorrect = 0
    if "quiz_trigger_sent" not in st.session_state:
        st.session_state.quiz_trigger_sent = False

    education_modules = {
        "Eligibility Rules": {
            "tip": "Understand the core GPA and test score requirements for NCAA/NAIA.",
            "quiz": {"question": "What is the minimum NCAA GPA requirement?", "answer": "2.3"}
        },
        "Highlight Tape Tips": {
            "tip": "Your first 30 seconds must showcase your best plays—start fast.",
            "quiz": {"question": "What should go first in your tape?", "answer": "Best plays"}
        },
        "Coach Communication": {
            "tip": "Emails are for intros. Calls build relationships.",
            "quiz": {"question": "What is best for building rapport?", "answer": "Phone call"}
        },
        "Visits Explained": {
            "tip": "Official visits are paid for by the college. Unofficial are out-of-pocket.",
            "quiz": {"question": "Who pays for unofficial visits?", "answer": "The athlete/family"}
        }
    }

    selected_module = st.selectbox("Choose a Topic", list(education_modules.keys()))
    st.info(education_modules[selected_module]["tip"])

    # Quiz component
    with st.expander("🧪 Try a Quick Quiz"):
        user_answer = st.text_input("Answer this:", education_modules[selected_module]["quiz"]["question"])
        if user_answer:
            correct = education_modules[selected_module]["quiz"]["answer"].lower()
            if user_answer.lower().strip() == correct:
                st.success("✅ Correct!")
                st.session_state.edu_completed.add(selected_module)
            else:
                st.error(f"❌ Not quite. The correct answer is: **{correct.title()}**")
                st.session_state.quiz_incorrect += 1

    # Kobe quote
    if st.session_state.selected_agent == "Kobe":
        st.markdown("----")
        st.markdown("🗣️ **Kobe says:**")
        st.info("Every inch of prep matters. Study recruiting like you study film. —The Mamba Mentor")

    # GHL Trigger Condition
    if (
        (len(st.session_state.edu_completed) >= 2 or st.session_state.quiz_incorrect >= 3)
        and not st.session_state.quiz_trigger_sent
    ):
        import requests

        try:
            webhook_url = "https://hooks.zapier.com/hooks/catch/123456/ghledu/"  # Replace with actual Zap or GHL webhook
            payload = {
                "name": st.session_state.name,
                "email": st.session_state.get("email", ""),
                "trigger": "Education Module Completed",
                "completed_modules": list(st.session_state.edu_completed),
                "incorrect_count": st.session_state.quiz_incorrect
            }
            requests.post(webhook_url, json=payload)
            st.session_state.quiz_trigger_sent = True
            st.success("🎯 Your recruiting progress has been logged for follow-up!")
        except Exception as e:
            st.warning(f"⚠️ Trigger failed to send: {e}")

# Step 5: Match Finder
with tab5:
    st.subheader("🔍 Step 5: Match Finder")

    # Sport-specific stat presets
    SPORT_STATS = {
        "Baseball": ["Batting Avg", "ERA", "Home Runs"],
        "Basketball": ["PPG", "Assists", "Rebounds"],
        "Bowling": ["Avg Score", "Strike Rate", "Spare Conversion"],
        "Cheerleading": ["Tumbling Score", "Stunt Difficulty", "Synchronization"],
        "Cross Country": ["5K Time", "Mile Pace", "Finish Rank"],
        "Esports": ["K/D Ratio", "Win %", "Team Communication Score"],
        "Field Hockey": ["Goals", "Assists", "Saves"],
        "Football": ["40-Yard Dash", "Tackles", "Touchdowns"],
        "Golf": ["Avg Round", "Driving Accuracy", "Greens in Reg"],
        "Gymnastics": ["Vault Score", "Bars Score", "Floor Score"],
        "Ice Hockey": ["Goals", "Assists", "Penalty Minutes"],
        "Lacrosse": ["Goals", "Assists", "Ground Balls"],
        "Rifle": ["Prone Score", "Standing Score", "Aggregate"],
        "Soccer": ["Goals", "Assists", "Saves"],
        "Softball": ["Batting Avg", "ERA", "RBIs"],
        "Spirit": ["Execution", "Choreography", "Impact"],
        "Swimming & Diving": ["100m Time", "200m Time", "Diving Score"],
        "Tennis": ["Win %", "Aces", "Unforced Errors"],
        "Track & Field": ["100m Time", "Shot Put Distance", "Long Jump"],
        "Volleyball": ["Kills", "Blocks", "Digs"],
        "Water Polo": ["Goals", "Saves", "Steals"],
        "Weightlifting": ["Snatch", "Clean & Jerk", "Bodyweight Ratio"],
        "Wrestling": ["Win-Loss", "Takedowns", "Pins"],
        "Girls Flag Football": ["Passing Yards", "Interceptions", "Touchdowns"]
    }

    selected_sport = st.session_state.get("sport", "Basketball")
    sport_stats = SPORT_STATS.get(selected_sport, ["Stat 1", "Stat 2", "Stat 3"])

    # Collect sport-specific stats
    st.markdown(f"### Sport: {selected_sport}")
    st.session_state.stat1 = st.text_input(f"{sport_stats[0]}", st.session_state.get("stat1", ""))
    st.session_state.stat2 = st.text_input(f"{sport_stats[1]}", st.session_state.get("stat2", ""))
    st.session_state.stat3 = st.text_input(f"{sport_stats[2]}", st.session_state.get("stat3", ""))

    # Calculate score and package
    try:
        score = calculate_strength_score(
            float(st.session_state.stat1),
            float(st.session_state.stat2),
            float(st.session_state.stat3)
        )
        package = recommend_package(score)
        st.success(f"💪 Match Strength Score: **{score}**")
        st.info(f"📦 Recommended Recruiting Package: **{package}**")
    except ValueError:
        st.warning("⚠️ Please enter numeric values for all three stats to calculate your match score.")
# Visual Explanation Dropdown
with st.expander("📊 What does my score and package mean?"):
    st.markdown("### 💡 Match Strength Breakdown")
    st.markdown("""
| Score Range | Match Strength      | Meaning                                           |
|-------------|---------------------|---------------------------------------------------|
| 9.0 - 10.0  | 🔥 Elite Prospect    | You are highly competitive at the national level. |
| 7.0 - 8.9   | 💪 Strong Prospect   | Likely to attract interest from D1/D2 programs.   |
| 5.0 - 6.9   | 📈 Developing Talent | Solid foundation, room to grow for recruitment.   |
| 3.0 - 4.9   | 🌱 Growth Stage      | Focus on fundamentals, increase exposure.         |
| 0.0 - 2.9   | 🛠️ Starter Level     | Just getting started or stats need context.       |
    """, unsafe_allow_html=True)

    st.markdown("### 🧭 Package Recommendation Guide")
    st.markdown("""
- **Elite Prospect (🔥)** → **Captain Package**: Full-service recruiting support, maximum exposure, 1-on-1 guidance.
- **Strong Prospect (💪)** → **Starter Package**: Email automation, timeline builder, match insights, film audits.
- **Developing Talent (📈)** → **Role Player Package**: Ideal for learning the process, building film, and getting reps.
- **Growth Stage or Starter (🌱/🛠️)** → **Access Plan**: Self-paced recruiting assistant and educational support.
    """)
# Step 6: Timeline Builder (Enhanced)
with tab6:
    st.subheader("📆 Step 6: Timeline Builder")

    st.markdown("""
    🛠️ **Plan Smart, Stay Connected**

    Your recruiting timeline is only as powerful as the system you use to manage it.  
    🎯 **Keep all your key milestones, communication records, and updates inside the Facilitate The Process platform**.

    > 📌 *Avoid relying solely on personal notes or outside calendars—this platform keeps your process aligned, visible, and optimized.*
    """)

    today = datetime.now().date()
    eval_date = st.date_input("Coach Evaluation Date", today)
    commit_date = st.date_input("Target Commitment Date")

    st.success("✅ These milestones are saved and work best when monitored through your recruiting dashboard.")

    st.button("🔗 View Full Timeline Dashboard")

# Step 7: Daily Tracker (Enhanced with Candace Assistant)
with tab7:
    st.subheader("📊 Step 7: Daily Tracker — Stay On Track with Candace")

    st.markdown("""
    👟 **Every Day Counts.**
    
    Let Candace help you track the daily habits that move you closer to a scholarship.  
    📲 *Remember: Staying consistent inside the platform means your data is always available to you — and your support team.*

    🔄 You can reset this checklist each day to keep yourself focused.
    """)

    st.info("✅ *Use this tracker every day from your mobile or desktop — all activity stays inside your Facilitate The Process profile.*")

    # Daily habit tracker
    daily_checklist = {
        "Followed up with a college coach": "📬",
        "Watched a new recruiting video": "🎥",
        "Improved your highlight video": "✂️",
        "Trained or conditioned today": "💪",
        "Logged a new stat or academic update": "🧠",
        "Checked your recruiting timeline": "🗓️",
    }

    completed = []
    for task, emoji in daily_checklist.items():
        is_checked = st.checkbox(f"{emoji} {task}")
        completed.append(is_checked)

    st.success(f"📈 Tasks Completed Today: {sum(completed)} of {len(daily_checklist)}")

    st.markdown("---")
    st.markdown("🧭 **View Your Full Tracker Dashboard Inside Your Profile** *(syncs with your recruiting journey)*")
    st.button("🔗 Go to Dashboard")
