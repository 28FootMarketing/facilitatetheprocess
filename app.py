import streamlit as st
import openai
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="wide")
st.title("🏆 ScoutBot: All-in-One Recruiting Assistant")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state for form inputs
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
    st.session_state.messages = [
        {"role": "system", "content": "You are ScoutBot, a helpful recruiting assistant. Offer college recruiting tips and encouragement to student-athletes."}
    ]

# --- Tabs Layout ---
tab1, tab2, tab3 = st.tabs(["📋 Step 1: My Recruiting Info", "💬 Step 2: Ask ScoutBot", "📄 Step 3: My Recruiting Report"])

# --- Tab 1: Form ---
with tab1:
    st.header("📋 Complete Your Recruiting Profile")
    with st.form("recruiting_form"):
        st.session_state.name = st.text_input("First Name", value=st.session_state.name)
        st.session_state.sport = st.text_input("Your Sport", value=st.session_state.sport)
        st.session_state.grade = st.selectbox("Current Grade", ["8th", "9th", "10th", "11th", "12th", "Post-grad"], index=2)
        st.session_state.gpa = st.number_input("GPA", min_value=0.0, max_value=4.5, step=0.1, value=st.session_state.gpa)
        st.session_state.motivation = st.slider("Motivation Level (1-10)", 1, 10, value=st.session_state.motivation)
        st.session_state.outreach = st.radio("Contacted Coaches?", ["Yes", "No"], index=1)

        st.subheader("🎯 Athletic Stats")
        st.session_state.stat1 = st.number_input("Stat 1", step=0.1, value=st.session_state.stat1)
        st.session_state.stat2 = st.number_input("Stat 2", step=0.1, value=st.session_state.stat2)
        st.session_state.stat3 = st.number_input("Stat 3", step=0.1, value=st.session_state.stat3)

        st.session_state.video_link = st.text_input("🎥 Highlight Video Link (YouTube or Hudl)", value=st.session_state.video_link)

        submitted = st.form_submit_button("🔒 Save Info")
        if submitted:
            st.success("✅ Your info has been saved. Now ask ScoutBot or generate your report.")

# --- Tab 2: GPT Chat ---
with tab2:
    st.header("💬 Ask ScoutBot Anything About Recruiting")
    user_input = st.chat_input("Type your recruiting question here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("ScoutBot is typing..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).markdown(msg["content"])

# --- Tab 3: PDF Report ---
with tab3:
    st.header("📄 Download Your AI-Powered Recruiting Report")
    if st.button("📥 Generate Report PDF"):
        full_chat = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages[1:]])
        pdf_bytes = generate_pdf_from_chat(
            name=st.session_state.name,
            sport=st.session_state.sport,
            video_link=st.session_state.video_link,
            chat_transcript=full_chat
        )
        st.download_button(
            label="⬇️ Click to Download",
            data=pdf_bytes,
            file_name=f"{st.session_state.name}_recruiting_report.pdf"
        )

