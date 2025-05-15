#zero shot prompting
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)
response=client.chat.completions.create(
    model='gpt-4o',
    messages=[{"role":"system",'content':'you are an useful ai that resolves users doubt you are an expert at everything'},
              {"role":"user","content":"can you tell me how to get good marks"}
              ]
)
print(response.choices[0].message.content)