import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load the API key from .env
load_dotenv()

# Create the Gemini client once
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Helper function: reusable API call, with retry + error handling ---
def ask_gemini(system_prompt, user_content, max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                )
            )
            return response.text
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2)  # wait a couple seconds before retrying
                continue
            else:
                # All retries failed — return a friendly message instead of crashing
                return f"⚠️ Sorry, the AI service is temporarily unavailable. Please try again in a moment.\n\n(Technical detail: {e})"

# --- Page setup ---
st.title("📧 AI Email Assistant")

tab1, tab2, tab3 = st.tabs(["✍️ Rewrite Email", "📝 Summarize Email", "💡 Subject Lines"])

# ============ TAB 1: Rewrite ============
with tab1:
    st.write("Turn your rough notes into a polished email.")

    user_input = st.text_area(
        "What do you want to say?",
        placeholder="e.g. tell my boss I'll be late tomorrow because of a doctor appointment",
        key="rewrite_input"
    )

    tone = st.selectbox(
        "Choose a tone",
        ["Professional", "Friendly", "Formal", "Concise"]
    )

    tone_instructions = {
        "Professional": "Write in a professional, polished, workplace-appropriate tone.",
        "Friendly": "Write in a warm, friendly, approachable tone, while still being clear.",
        "Formal": "Write in a formal, respectful, traditional tone, suitable for official correspondence.",
        "Concise": "Write as briefly and directly as possible, cutting all unnecessary words."
    }

    if st.button("Generate Email"):
        if user_input.strip() == "":
            st.warning("Please type something first.")
        else:
            with st.spinner("Writing your email..."):
                system_prompt = (
                    "You are an email-writing assistant. Rewrite the user's message as a complete email. "
                    + tone_instructions[tone]
                    + " Only output the email, nothing else."
                )
                result = ask_gemini(system_prompt, user_input)
            st.subheader("Your Email")
            st.write(result)

# ============ TAB 2: Summarize ============
with tab2:
    st.write("Paste a long email and get a short summary.")

    long_email = st.text_area(
        "Paste the email you want summarized",
        height=200,
        key="summarize_input"
    )

    if st.button("Summarize Email"):
        if long_email.strip() == "":
            st.warning("Please paste an email first.")
        else:
            with st.spinner("Summarizing..."):
                system_prompt = (
                    "You summarize emails. Read the email and produce a short summary "
                    "(2-4 sentences) capturing the key points and any action items. "
                    "Only output the summary, nothing else."
                )
                result = ask_gemini(system_prompt, long_email)
            st.subheader("Summary")
            st.write(result)

# ============ TAB 3: Subject Lines ============
with tab3:
    st.write("Get subject line suggestions for your email.")

    email_for_subject = st.text_area(
        "Paste your email content",
        height=200,
        key="subject_input"
    )

    if st.button("Suggest Subject Lines"):
        if email_for_subject.strip() == "":
            st.warning("Please paste an email first.")
        else:
            with st.spinner("Thinking of subject lines..."):
                system_prompt = (
                    "You write email subject lines. Read the email and suggest 5 short, "
                    "clear subject line options, numbered 1-5. Only output the numbered list, nothing else."
                )
                result = ask_gemini(system_prompt, email_for_subject)
            st.subheader("Subject Line Suggestions")
            st.write(result)