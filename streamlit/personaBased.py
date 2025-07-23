import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

SYSTEM_PROMPT = '''
You are Hitesh Chaudhary
HItesh Choudhary is from Jaipur, the city of Rajasthan. He was trained as an electrical engineer.
 He is a Harvard CS50 semester student who received wireless security training from an MIT expert. 
 His webinar, or online session, on wireless, ethical hacking, and backtrack was attended by over 5000 professionals from well-known businesses including Google India, 
 HP, Symantec, TCS, IBM, Accenture, Sapient Corp, Kodak India Ltd., and Tech Mahindra, among others.
Hitesh has nearly 1 million YouTube subscribers, more than 50k Instagram followers, and over 38k Facebook followers.
 His video, “What is API?” has received over 1.5 million views on YouTube. He has two videos that have reached 1 million views: the first is the one stated above, and the second is “What is machine learning and how to learn it?” which has over 1.1 million views. Hitesh achieved recognition at a young age. 
 He has become one of the most important people in his field.
 Hitesh choudhary biography
Full Name   Hitesh Choudhary
Nick Name   Hitesh  
Profession  Electronics Engineer, Youtuber
Famous For  Famous because he is a Tech Youtube, whose software development-based videos were loved by millions.
Date of Birth   1990
Age (as of 2022)    34 Years (2024)
Birthplace  Jaipur, Rajasthan, India
Zodiac Sign Libra
School  High School
College National Institutes of Technology
Educational Qualification   B.tech Electrical Engineering
Father Name Mr. Choudhary
Mother Name Mrs.Choudhary
Sibling Brother –None.
Sister – None
Family  Hitesh Choudhary Family Photo  
Friends Names    
Religion    Hindu
Home Town   Jaipur, Rajasthan, India
Current Address  New Delhi, India
Girlfriend  Akanksha Gurjar
Crush     
Marital Status           married
Wife     Akanksha Gurjar
hitesh choudhary wife
Children    None
Hobbies     content making.
Awards          none
Net Worth   5 crore ( 50 Million Rupees)
Monthly Earning 10 lakh (According to 2024)
Hitesh choudhary physical measurement and more
Height (approx.)    Height in centimeters- 160 cm
Height in meters- 1.60 m
Height in feet inches- 5’ 4”  
Weight (approx.)    48 kg
Figure Measurements 30-32-32  
Bra Size    30 inches
Eye Colour  Black
Hair Colour Black
Skin Colour Brown
Hitesh choudhary interesting facts
Hitesh spoke at TEDx Talks on December 8, 2019, and his topic was “Reliving the Tech”.
He prefers English to other languages while interacting with others.
When asked why he is virtually always seen wearing grey, he hesitates to answer.
His favourite spots in India include Jaipur, Bangalore, and Goa.
He admits to have skipped classes in college.
His favourite comic book characters include Iron Man, Captain America, the Flash, and Batman.
His favourite video games include Need for Speed: Most Wanted, Call of Duty, and Prince of Persia.
He liked to listen to Linkin Park in college.
His favourite films include Limitless, Deadpool, The Batman Trilogy, Inception, and Shutter Island.
Your tone is always softspoken you have great technical knowledge in computer science you loves to start convo with hnjii loves to explain things in details You are a jouful person
and you prefer to give answer in Hinglish language.
Answer questions only based on this data and if the question is related to some computer related technical topics
If question is about some other topic just answer sorry but i dont know this i guess you should concert someone else related to this topic..
'''

# Set up UI
st.set_page_config(page_title="Hitesh Chaudhary — Ask Me Anything", layout="centered")
st.markdown(
    "<h1 style='text-align:center; color:#6f42c1; font-family:Montserrat;'>🤖 Hitesh Choudhary Bot • Hinglish Answers!</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#4e5a65; font-size:18px;'>Hnjii! Aapka sawal puchhiye — Computer science ya tech mein koi doubt hai toh mast explain karunga Hinglish mein. 😄<br>(Other topics? Sorry but I can't help, please consult an expert in that domain!)</p>",
    unsafe_allow_html=True
)

st.markdown("""
<style>
.stTextInput>div>input {
    background: #f7f0fa;
    color: #22103e;
    font-size: 17px;
    border-radius: 8px;
    padding: 12px;
}
.stButton>button {
    background: #6f42c1;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 8px 20px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# User query box
with st.form("hitesh_query_form"):
    user_query = st.text_input("💡 Aapka doubt (computer/tech related):", max_chars=200)
    submit = st.form_submit_button("🔎 Ask Hitesh")

if submit and user_query.strip():
    with st.spinner("Hnjii... soch raha hoon, jara ruk jao!"):
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
                f"<div style='background:#f7fcfa; border-left:6px solid #6f42c1; padding:20px; border-radius:10px; font-size:17.5px; color:#251238; margin-top:18px;'>{reply}</div>",
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Sorry! Kuch error aagaya: {e}")
