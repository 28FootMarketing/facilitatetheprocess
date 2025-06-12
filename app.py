import streamlit as st
import openai
from utils.logic import recommend_package, calculate_strength_score
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="ScoutBot AI Assistant", layout="centered")
st.title("🎙️ ScoutBot AI: Your Recruiting Companion")

# Step 1: Setup session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are ScoutBot, a helpful assistant for high school athletes navigating college recruiting. Offer tips, encouragement, and recruiting advice when asked."}
    ]

# Step 2: User Input + GPT Chat
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

# Step 3: Display full conversation
for msg in st.session_state.messages[1:]:  # skip system message
    st.chat_message(msg["role"]).markdown(msg["content"])
import os
openai.api_key = os.getenv("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")
