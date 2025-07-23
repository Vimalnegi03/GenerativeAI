import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

# Initialize the OpenAI (Gemini) client
client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# System prompt for Gein, the math expert
SYSTEM_PROMPT = '''
You are an helpful ai agent whose name is gein you are an expert in maths and can solve any mathematical query within seconds.You should
not answer any query that is not related to maths 
Examples
Input:What is 2+2
Output:According to my calculation 2+2 is 4
Input:what is 4*4
output:According to my calculation the output for this question will be 16 we can also obtain this output by adding four four times
Input :what is the color of sky?
Ouput:Nice query but thats out of my scope I can only help you to deal with maths query
'''

# Streamlit UI starts here
st.set_page_config(page_title="Gein Math Expert", layout="centered")
st.markdown(
    "<h1 style='text-align:center; color:#4891f3; font-family:Montserrat;'>🤖 Gein - Math Expert AI</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; font-size:18px; color:#232e3c;'>Ask a math question—Gein will solve it instantly.<br>If you ask something else, you'll get a friendly response.</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
      .stTextInput>div>input {
        background: #eef2fb;
        color: #15213a;
        font-size: 18px;
        border-radius: 8px;
        padding: 12px;
      }
      .stButton>button {
        background-color: #43cc95;
        color: white;
        font-weight: 600;
        font-size: 16px;
        border-radius: 7px;
        padding: 12px 26px;
        border: none;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# User input form
with st.form("math_form"):
    user_query = st.text_input("🔢 Enter your math question:")
    ask = st.form_submit_button("🧮 Get Answer")

if ask and user_query.strip():
    with st.spinner("Gein is thinking..."):
        try:
            response = client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query}
                ]
            )
            answer = response.choices[0].message.content
            st.markdown(
                f"<div style='background:#e7fcee; border-left:6px solid #43cc95; padding:20px 22px; border-radius:10px; font-size:18px; color:#113a27; margin-top:18px;'>{answer}</div>",
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Sorry, there was an error: {e}")
