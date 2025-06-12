import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# Load environment variables
load_dotenv()

# Show diagnostic info (remove in production)
st.warning("🔐 Checking OpenAI API Key setup...")

# Try secrets first, then env
api_key_from_secrets = st.secrets.get("OPENAI_API_KEY")
api_key_from_env = os.getenv("OPENAI_API_KEY")

if api_key_from_secrets:
    st.success("✅ Found API key in st.secrets!")
elif api_key_from_env:
    st.info("ℹ️ Found API key in environment variables.")
else:
    st.error("🚫 No valid API key found. Set via .streamlit/secrets.toml or .env file.")
    st.stop()

# Set API key
openai.api_key = api_key_from_secrets or api_key_from_env
