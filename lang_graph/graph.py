from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from typing import Literal
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv() #This is basically used to use .env varables here for tracing langsmith will automatically trace
api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
client=OpenAI(api_key=api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
System_Prompt=f'''You are a good AI agent that basically decides whether a question is coding related or not.
You must output in specified JSON boolean only.
'''
Main_Prompt="You are an AI agent that basically takes a coding question as an input and returns the code output of that"

#Schema
class DetectCallResponse(BaseModel):
    is_question_ai:bool
class State(TypedDict):
    user_message:str
    is_coding_question:bool
    ai_message:str


def detect_query(state: State):
    user_message = state.get("user_message")
    res = client.beta.chat.completions.parse(
        model='gemini-2.0-flash',
        response_format=DetectCallResponse,
        messages=[
            {"role": "system", "content": System_Prompt},
            {"role": "user", "content": user_message}
        ]
    ) #used beta because in beta we can have a structured output we can pass a pydantic model to it
    # Normalize and parse response to actual boolean
    response = res.choices[0].message.parsed
    state["is_coding_question"] = response 
    print("Parsed is_coding_question:", state["is_coding_question"])
    return state

#We always have to inform routing edge that what are possible ways wherre it can go
def route_edge(state:State) ->Literal["solve_coding_question","solve_simple_query"] :
    is_coding_question=state.get("is_coding_question")
    if is_coding_question:
        return "solve_coding_question"
    else:
        return "solve_simple_query"

def solve_coding_question(state:State):
    user_message=state.get("user_message")
    print("ye code hua run")
    res=client.chat.completions.create(
        model='gemini-2.0-flash',
        messages=[{"role":"system","content":Main_Prompt},{"role":"user","content":user_message}],
    )
    #OpenAI call
    state["ai_message"]=res.choices[0].message.content
    return state

def solve_simple_query(state:State):
    #OpenAI call uses mini model
    user_message=state.get("user_message")
    state["ai_message"]="Please ask some coding related question"
    return state

#now we have created nodes so lets go on to create graphs
graph_builder=StateGraph(State)

#we have name of every node and their functions name
graph_builder.add_node("detect_query",detect_query)
graph_builder.add_node("solve_coding_question",solve_coding_question)
graph_builder.add_node("solve_simple_query",solve_simple_query)
graph_builder.add_node("route_edge",route_edge)


#Now create edges

#first edge is start edge

graph_builder.add_edge(START,"detect_query")
#as after route_edge we have to go to conditionals
graph_builder.add_conditional_edges("detect_query",route_edge) #in conditional edge you basically pass the whole function 


graph_builder.add_edge("solve_coding_question",END)
graph_builder.add_edge("solve_simple_query",END)

graph=graph_builder.compile()


#now its time to use the graph
def call_graph():
    user_message=input("enter your questions ? ")
    state={
        "user_message":user_message,
        "ai_message":"",
         "is_coding_question":False,
    }
    result=graph.invoke(
     state
    )
    print("Final Result",result.get("ai_message"))
    
call_graph()    