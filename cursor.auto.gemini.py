from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json
import platform
api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
client=OpenAI(api_key=api_key,
              base_url="https://generativelanguage.googleapis.com/v1beta/openai/")


import speech_recognition as sr
import time

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🔧 Calibrating for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print("✅ Calibration done.")

    print("🎤 You can speak after this countdown:")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

    print("🎙️ Listening now (speak up to 30 seconds)...")

    try:
        audio = recognizer.listen(
            source,
            timeout=60,               # wait up to 60s for user to start talking
            phrase_time_limit=30      # let them speak up to 30s max
        )

        print("🔍 Recognizing...")
        text = recognizer.recognize_google(audio)
        print("✅ You said:", text)

    except sr.WaitTimeoutError:
        print("⌛ Timeout: No speech detected within the time window.")
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ Recognition error: {e}")


messages=[]


def run_command(command:str):
   print(platform.system())
   os.system(command=command)
available_tools={
   
    'run_command':{
       "fn":run_command,
       "description":"takes a command from user and execute that"
    }

}
System_prompt=f"""You are a powerful ai agent who is specialized in resolving user query.
 You work on start,plan,action,observe mode.
For the given user query and available tools plan step by step execution,based on the planning select the relevant tools from the avilable 
tools and based on the tool selction you perfom an action to call the tool wait for observation and based on observation from the tool call resolve the user query

Rules-:
- Follow the output JSON format.
- Always Perform one step at a time and wait for next input.
- Carefully analyse the user query

Output JSON Format:
{{
    "step":"string",
"content":"string",
"function":"the name of function if the step is action",
"input":"the input parameter for the function"
}}
Available Tools:
-run_command:Takes a command and execute that command on windows or linux system according to a system configuration
Example:
User Query:what is the weather of new york?
Output:{{"step":"plan","content":"the user is interested in weather data of new york}}
Output:{{"step""plan","content":"From the available tools I should call get_weather"}}
Output:{{"step":"action","function":"get_weather","input":"new york"}}
Output:{{"step":"observe","output":"12 degree celsius"}}
Output:{{"step":"output","The weather of new york is 12 degree celsius"}}

"""
messages.append({
            'role':"system",'content':System_prompt})

user_query=text
messages.append({"role":"user","content":user_query})
outputs=[]
while True:
    response=client.chat.completions.create(
        model='gemini-2.0-flash',
        messages=messages,
        response_format={"type":"json_object"},
        
    )
    output=response.choices[0].message.content
    messages.append({"role":"assistant",'content':json.dumps(output)})
    extracted_output=json.loads(output)
    if(extracted_output.get("step")=='plan'):
     print(extracted_output.get("content"))
     continue
    if(extracted_output.get("step")=='action'):
       tool_name=extracted_output.get("function") #get weather
       tool_input=extracted_output.get("input") #city name
       if(available_tools.get(tool_name,False).get("fn")(tool_input))!=False:
          output=available_tools[tool_name].get("fn")(tool_input)
          messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})

    if(extracted_output.get("step")=="output"):
       print(extracted_output.get("content"))
       break