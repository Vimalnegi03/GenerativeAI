import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = '''
You are tony stark
My armor, it was never a distraction or a hobby, it was a cocoon. And now, I'm a changed man. You can take away my house, all my tricks and toys. But one thing you can't take away… I am Iron Man."
―Tony Stark[src]
Anthony Edward "Tony" Stark was a billionaire industrialist, a founding member of the Avengers, and the former CEO of Stark Industries. A brash but brilliant inventor, Stark was self-described as a genius, billionaire, playboy, and philanthropist. With his great wealth and exceptional technical knowledge, Stark was one of the world's most powerful men following the deaths of his parents and enjoyed the playboy lifestyle for many years until he was kidnapped by the Ten Rings in Afghanistan, while demonstrating a fleet of Jericho missiles. With his life on the line, Stark created an armored suit which he used to escape his captors. Upon returning home, he utilized several more armors to use against terrorists, as well as Obadiah Stane who turned against Stark. Following his fight against Stane, Stark publicly revealed himself as Iron Man.

[... Truncated for brevity: Include your entire Marvel backstory here as before ...]

you have knowledge about tech related stuffs and only of Marvel universe. Don't answer anything that is not related to you or tech.
'''

# --- UI Design ---
st.set_page_config(page_title="Iron Man • Marvel Tech AI", layout="centered")
st.markdown(
    """
    <style>
    .streamlit-expanderHeader {font-size:22px; color:#e23636;}
    .stTextInput > div > input {
        background: #282828;
        color: #e23636;
        font-size: 18px;
        border-radius: 9px;
        border: 2px solid #e23636;
        font-family: 'Orbitron', sans-serif;
    }
    .stButton>button {background-color:#ffc600; color:#191919; font-weight:700; border-radius:8px; border:none;}
    .stSuccess {background-color: #171717;}
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align:center; color:#e23636;font-family:Orbitron,sans-serif;'>🦾 Iron Man AI</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<center><img src='https://pngimg.com/d/ironman_PNG15.png' width='130'/></center>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align:center; color:#ffc600;font-family:Orbitron,sans-serif;'>Ask me anything about Marvel Tech or the world of Iron Man</h3>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; font-size:17px; color:#515151;'>Ask about suits, gadgets, Avengers, or any technical challenge that an AI Tony Stark would know.<br><b>If your query isn't related to tech or Marvel, expect a brash (but polite) Starkian refusal!</b></p>",
    unsafe_allow_html=True
)

# User input form
with st.form("ironman_form"):
    user_query = st.text_input(
        "💬 Enter your Marvel or tech question (Iron Man at your service!):",
        max_chars=250,
        help="Ask about armor, Avengers tech, or in-universe gadgets."
    )
    ask = st.form_submit_button("🚀 Ask Tony")

if ask and user_query.strip():
    with st.spinner("Running diagnostics... booting up J.A.R.V.I.S..."):
        try:
            response = client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(
                f"""<div style='background:#15181e; border-left:7px solid #e23636; padding:23px 22px; border-radius:14px; font-size:18.5px; color:#ffc600; margin-top:19px; font-family:Orbitron,sans-serif; letter-spacing:0.03em;'>{reply}</div>""",
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Sorry! Something malfunctioned in the arc reactor: {e}")

st.markdown(
    "<hr><p style='text-align:center; color:#989898; font-size:13px; margin-top:28px;'>Built with 👨‍💻, Arc Reactor, and J.A.R.V.I.S. by Stark Industries. Marvel content for demo purposes only.</p>",
    unsafe_allow_html=True
)
