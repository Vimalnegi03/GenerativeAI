import streamlit as st
import os
import json
import platform
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

# Initialize Gemini Client
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Tool function
def run_command(command: str):
    try:
        result = os.popen(command).read()
        return result or "✅ Command executed (no output)"
    except Exception as e:
        return f"❌ Error: {e}"

# Available tools
available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Run system commands on Linux/Windows"
    }
}

# System Prompt
System_prompt = """
You are an AI agent named Gein. You plan step-by-step to solve user queries using available tools.

Steps:
- "plan": Analyze the query
- "action": Use a tool
- "observe": Capture tool output
- "output": Final response

Respond using strict JSON:
{
  "step": "plan" | "action" | "observe" | "output",
  "content": "string",
  "function": "optional string (if step is action)",
  "input": "optional string (for action)"
}
"""

# Streamlit UI setup
st.set_page_config(page_title="Gein Terminal Agent", layout="centered")
st.markdown("<h2 style='text-align:center;'>🎙️ Gein - Voice Assistant</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Understands, plans, and executes — and gives you the final answer.</p>", unsafe_allow_html=True)
st.divider()

# Voice recording
st.markdown("### Speak your command:")
listen = st.button("🎤 Start Listening")

user_query = None
if listen:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("Calibrating microphone..."):
            r.adjust_for_ambient_noise(source, duration=1)

        st.success("Listening... Speak now!")

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=20)
            user_query = r.recognize_google(audio)
            st.success(f"✅ You said: {user_query}")
        except sr.WaitTimeoutError:
            st.error("⌛ Timeout - no speech detected.")
        except sr.UnknownValueError:
            st.error("❌ Couldn't understand your speech.")
        except sr.RequestError as e:
            st.error(f"⚠️ Recognition error: {e}")

# Reasoning agent loop
if user_query:
    st.markdown("### 🤖 Final Response")
    messages = [
        {"role": "system", "content": System_prompt},
        {"role": "user", "content": user_query}
    ]

    MAX_STEPS = 10
    step_counter = 0
    final_result = None

    with st.spinner("💭 Gein is reasoning..."):
        while step_counter < MAX_STEPS:
            step_counter += 1
            try:
                response = client.chat.completions.create(
                    model="gemini-2.0-flash",
                    messages=messages,
                    response_format={"type": "json_object"}
                )
                response_text = response.choices[0].message.content
                parsed = json.loads(response_text)
            except Exception as e:
                st.error(f"❌ Invalid response from Gemini.\n\n{e}")
                break

            # Normalize to list of steps
            steps = parsed if isinstance(parsed, list) else [parsed]

            for step in steps:
                messages.append({"role": "assistant", "content": json.dumps(step)})

                if step["step"] == "action":
                    function = step.get("function")
                    input_val = step.get("input")
                    if function in available_tools:
                        result = available_tools[function]["fn"](input_val)
                        # Add observation for the next round
                        observe = {"step": "observe", "output": result}
                        messages.append({
                            "role": "assistant",
                            "content": json.dumps(observe)
                        })

                if step["step"] == "output":
                    final_result = step.get("content")
                    break

            if final_result:
                break

    if final_result:
        st.success("✅ Gein has resolved your request.")
        st.markdown(
            f"""<div style='padding: 18px; background-color: #f1f8f6;
                  border-left: 6px solid #00a86b;
                  border-radius: 8px;
                  font-size: 18px; color: #0e2f2f;'>
                {final_result}
                </div>""",
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Gein couldn't complete the reasoning in time.")
