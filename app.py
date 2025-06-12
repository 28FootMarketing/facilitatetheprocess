import streamlit as st
import openai
from utils.pdf_generator import generate_pdf_from_chat

st.set_page_config(page_title="ScoutBot Recruiting Assistant", layout="centered")
st.title("🎯 ScoutBot: Phase 4 Recruiting Assistant")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are ScoutBot, a friendly recruiting expert for high school athletes. Ask questions, give clear advice, and help create a recruiting action plan."}
    ]

with st.expander("🧑‍💻 Optional: Personal Info for Recruiting Report"):
    user_name = st.text_input("Your Name:")
    sport = st.text_input("Your Sport:")
    video_url = st.text_input("Your Highlight Video Link (Hudl, YouTube, etc.):")

user_input = st.chat_input("Ask ScoutBot anything about recruiting…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("ScoutBot is thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

if st.button("📄 Generate My Recruiting PDF"):
    full_chat = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages[1:]])
    pdf_bytes = generate_pdf_from_chat(user_name, sport, video_url, full_chat)
    st.download_button("⬇️ Download Recruiting Report", data=pdf_bytes, file_name=f"{user_name}_recruiting_plan.pdf")
