import streamlit as st
from dotenv import load_dotenv
import os
import json
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

# Initialize Gemini Client
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# System prompt that drives the chain-of-thought logic
SYSTEM_PROMPT = """
You are a helpful AI assistant named Gein. For each question, follow a logical thought process using these steps:

- analyse
- think
- output
- validate
- result

Always break things down first, before rushing to answer. Return output in strict JSON format:
{"step": "string", "content": "string"}
"""

# --- Streamlit App Config ---
st.set_page_config(page_title="Gein AI - Reasoning Chat", layout="centered")

# --- Modern UI Styling ---
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .stButton > button {
            background-color: #00a86b;
            color: white;
            border-radius: 5px;
        }
        .stTextInput > div > input {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 0.75rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title Section ---
st.markdown("<h1 style='text-align:center;'>🧠 Gein</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>AI that thinks before it speaks.</p>",
    unsafe_allow_html=True
)

# --- User Input Section ---
user_query = st.text_input("💬 Enter your question:")
submit = st.button("Generate Answer")

if submit and user_query:
    # Storage for messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    result_output = None
    outputs = []

    # Show loader while working
    with st.spinner("Thinking through the steps..."):
        try:
            while True:
                response = client.chat.completions.create(
                    model="gemini-2.0-flash",
                    response_format={"type": "json_object"},
                    messages=messages,
                )

                response_text = response.choices[0].message.content
                messages.append({
                    "role": "assistant",
                    "content": response_text
                })

                parsed = json.loads(response_text)

                # Sometimes we get a list of outputs instead of one dict
                if isinstance(parsed, list):
                    for output in parsed:
                        if output.get("step") == "result":
                            result_output = output["content"]
                            break
                elif isinstance(parsed, dict):
                    if parsed.get("step") == "result":
                        result_output = parsed["content"]
                        break

                if result_output:
                    break

        except Exception as e:
            st.error("❌ Error parsing Gemini response. See details below:")
            st.code(str(e))
            st.markdown("**Raw Response:**")
            st.code(response_text)
            st.stop()

    # --- Show Final Result ---
    if result_output:
        st.markdown("---")
        st.success("✅ Gein has thought it through!")
        st.markdown(
            f"""
            <div style="
                background-color: #e6f7ea;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #cde0d6;
                font-size: 18px;
                color: #0e2f2f;
            ">
                {result_output}
            </div>
            """,
            unsafe_allow_html=True
        )
