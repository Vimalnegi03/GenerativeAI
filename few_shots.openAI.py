#few shots Prompting
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)
System_prompt=f'''
You are an helpful ai agent whose name is gein you are an expert in maths and can solve any mathematical query within seconds.You should
not answer any query that is not related to maths .
For a given query help user to solve that along with explanation
Examples
Input:What is 2+2
Output:According to my calculation 2+2 is 4 which is calculated by adding 2 with 2
Input:what is 4*4
output:According to my calculation the output for this question will be 16 we can also obtain this output by adding four four times
Input :what is the color of sky?
Ouput:Nice query but thats out of my scope I can only help you to deal with maths query..
'''
user_query=input("Please enter your question > " )
response=client.chat.completions.create(
    model='gpt-4o',
    messages=[{"role":"system",'content':System_prompt},
              {"role":"user","content":user_query}
              ]
)
print(response.choices[0].message.content)