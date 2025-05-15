#few shots prompting
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
client=OpenAI(api_key=api_key,
              base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

System_prompt=f'''
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
user_query=input("Please enter your question > " )
response=client.chat.completions.create(
      model='gemini-2.0-flash',
    messages=[{"role":"system",'content':System_prompt},
              {"role":"user","content":user_query}
              ]
)
print(response.choices[0].message.content)