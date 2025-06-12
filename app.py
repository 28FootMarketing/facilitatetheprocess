import streamlit as st
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="Athletic Recruiting Assistant", layout="centered")
st.image("https://recruit.facilitatetheprocess.com/images/logo.png", width=220)
st.title("🏈 ScoutBot: Recruiting Assistant – Phase 2")
st.subheader("Let’s match you with a plan and score your recruiting strength.")

with st.form("recruiting_form"):
    name = st.text_input("What is your first name?")
    grade = st.selectbox("What is your current grade level?", ["8th", "9th", "10th", "11th", "12th", "Post-grad"])
    sport = st.selectbox("What is your primary sport?", ["Football", "Basketball", "Volleyball", "Soccer", "Track", "Other"])
    motivation = st.slider("How motivated are you to get recruited?", 1, 10, 7)
    outreach = st.radio("Have you already contacted any college coaches?", ["Yes", "No"])
    gpa = st.number_input("What is your current GPA?", min_value=0.0, max_value=4.5, step=0.1)

    st.markdown("### Enter 3 Performance Stats for Your Sport")
    stat1 = st.number_input("Stat 1 (e.g., PPG, Goals, PRs)", step=0.1)
    stat2 = st.number_input("Stat 2", step=0.1)
    stat3 = st.number_input("Stat 3", step=0.1)

    submitted = st.form_submit_button("Generate My Plan & Report")

if submitted:
    plan = recommend_package(grade, motivation, outreach, gpa)
    score = calculate_strength_score(stat1, stat2, stat3)
    summary = build_summary(name, sport, plan, score)

    st.success(summary)
    st.download_button("📥 Download My PDF Report", generate_pdf(name, sport, grade, gpa, plan, score), file_name=f"{name}_recruiting_report.pdf")
