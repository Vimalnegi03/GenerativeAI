from openai import OpenAI
from dotenv import load_dotenv
import os
import json

import pymysql
# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

# Set up OpenAI client
client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

def get_weather(city:str):
        print("Tool called")
        return "31 degree"

import pymysql
import datetime

def execute_sql_query(query: str):
    conn = pymysql.connect(
        host='mt-uat-lighthouse.cal82oikkybf.ap-south-1.rds.amazonaws.com',
        user='FaceRecongition',
        password='password@123',
        db='FaceRecognition',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            employees = cursor.fetchall()

            # Convert date/datetime objects to strings
            for row in employees:
                for key, value in row.items():
                    if isinstance(value, (datetime.date, datetime.datetime)):
                        row[key] = value.isoformat()

        conn.close()
        return employees, 200

    except Exception as e:
        print(f"Error: {e}")
        return [], 500


     
available_tools={
     "get_weather":{
          "fn":get_weather,
          "description":"takes a city name as an input and returns current weather for a city"
     },
      "execute_sql_query":{
          "fn":execute_sql_query,
          "description":"takes a table name as input and perform the query he is asking to perform"
     }
}



system_prompt=f'''
you are an helpful ai assistant who is specialized in resolving user query.
you work on start,plan,action,observe,mode
for the given user query and available tools,plan the step by step execution,based on the planning select the relevant tool from the available tools
and based on the tool selction you perform an action to call the tool wait for observation and based on observation from tool call resolve the user query

Rules:
Follow the strict JSON ouput as per output schema
ALways perform one step at a time and wait for next input
carefully analayse the user query

Output JSON Format:
{{"step":"string","content":"string","function":"the name of the function if the step is action","input":"the input parameter for the function"}}

Available Tools:
get_weather:Tool to get weather of a city
execute_sql_query:Tool to execute database query on a table
run_command :Takes a command as input execute on system and returns output
Example:
User Query:What is weather of new york
Output :{{"step":"plan","content":"The user is interested in weather data of new york" }}
Output :{{"step":"plan","content":"From the available tools I should call get_weather"}}
Output :{{"step":"action","function":"get_weather","input":"new york"}}
Output :{{"step":"observe","output":"12 Degree Cel"}}
Output :{{"step":"output","content":"the weather of new york is 12 degree celsius"}}
'''
# Text input with placeholder
user_query=input("enter your query> ")
messages=[]
messages.append( {"role": "system", "content": system_prompt})
messages.append({"role": "user", "content": user_query})
while True:
    response = client.chat.completions.create(
                        model="gemini-2.5-flash",
                        response_format={"type":"json_object"},
                        messages=messages
                    )
    parsed_response=json.loads(response.choices[0].message.content)
    print(parsed_response)
    if parsed_response.get("step")=="plan":
     messages.append({"role":"assistant", "content": json.dumps(parsed_response)})
     continue
    elif parsed_response.get("step")=="action":
          tool_name=parsed_response.get("function") #get_weather
          tool_input=parsed_response.get("input") #tool_input
          output=available_tools.get(tool_name).get("fn")(tool_input)
          messages.append({"role":"assistant", "content": json.dumps({"step":"observe","output":output})})
          continue
    else:
         messages.append({"role":"assistant", "content": json.dumps(parsed_response)})
         break
reply = messages[-1]["content"]
reply=json.loads(reply) 
print(reply["content"])