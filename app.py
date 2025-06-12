import streamlit as st
from utils.logic import recommend_package, build_summary

st.set_page_config(page_title="Athletic Recruiting Assistant", layout="centered")

# Logo and header
st.image("https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/lvuhyrRsvUd75dVxBxM2/media/65f2015a1a919560617dd346.png", width=220)
st.title("🏈 ScoutBot: Your Recruiting Assistant")
st.subheader("Let’s find the right path for your athletic journey.")

# Input questions
with st.form("recruiting_form"):
    name = st.text_input("What's your first name?")
    grade = st.selectbox("What is your current grade level?", ["8th", "9th", "10th", "11th", "12th", "Post-grad"])
    sport = st.text_input("What is your primary sport?")
    motivation = st.slider("How motivated are you to get recruited? (1 = Curious, 10 = All-in)", 1, 10, 7)
    outreach = st.radio("Have you already contacted any college coaches?", ["Yes", "No"])
    gpa = st.number_input("What is your current GPA?", min_value=0.0, max_value=4.5, step=0.1)

    submitted = st.form_submit_button("Show Me My Plan")

if submitted:
    plan = recommend_package(grade, motivation, outreach, gpa)
    summary = build_summary(name, sport, plan)

    st.success(f"✅ {summary}")

    if plan == "Role Player":
        st.markdown("[Start with the Role Player Plan →](https://recruit.facilitatetheprocess.com/order-form-roleplayermothly)")
    elif plan == "Starter":
        st.markdown("[Check Out the Starter Plan →](https://recruit.facilitatetheprocess.com/order-form-starterpackage)")
    else:
        st.markdown("[Go All-In with the Captain Plan →](https://recruit.facilitatetheprocess.com/order-form-captainpackage)")
