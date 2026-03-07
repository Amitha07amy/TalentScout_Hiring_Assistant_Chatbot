from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from hiring_assistant.engine import HiringAssistantEngine
from hiring_assistant.models import ConversationState

load_dotenv()

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="centered")

st.title("TalentScout Hiring Assistant")
st.caption("Initial candidate screening powered by prompt-driven AI")

if "engine" not in st.session_state:
    st.session_state.engine = HiringAssistantEngine()
if "state" not in st.session_state:
    st.session_state.state = ConversationState()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome to TalentScout. I can collect your profile and generate technical "
                "screening questions from your tech stack."
            ),
        }
    ]

with st.sidebar:
    st.subheader("Configuration")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    key_set = "Yes" if os.getenv("OPENAI_API_KEY") else "No"
    smtp_set = "Yes" if all(
        os.getenv(k) for k in ["SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "MAIL_FROM"]
    ) else "No"
    st.write(f"OpenAI model: `{model}`")
    st.write(f"OPENAI_API_KEY set: `{key_set}`")
    st.write(f"SMTP configured: `{smtp_set}`")
    st.write("If API key is not set, the app uses curated fallback questions.")
    if st.button("Start New Conversation"):
        st.session_state.state = ConversationState()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "New session started. Send any message to begin the TalentScout screening flow."
                ),
            }
        ]
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your response..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    engine: HiringAssistantEngine = st.session_state.engine
    state: ConversationState = st.session_state.state
    new_state, response = engine.handle_user_message(state, prompt)
    st.session_state.state = new_state
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
