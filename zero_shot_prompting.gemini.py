#zero short prompting
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
client=OpenAI(api_key=api_key,
              base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
response=client.chat.completions.create(
    model='gemini-2.0-flash',
    messages=[{"role":"system",'content':'you are an useful ai that resolves users doubt you are an expert at everything'},
              {"role":"user","content":"can you tell me how to get good marks"}
              ]
              ,max_tokens=30
)
print(response.choices[0].message.content)