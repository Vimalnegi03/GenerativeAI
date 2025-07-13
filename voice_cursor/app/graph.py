from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import StateGraph, START, END
import os
from langchain_core.tools import tool
from langchain.schema import SystemMessage 
import subprocess
from dotenv import load_dotenv
load_dotenv()
class State(TypedDict):
    messages:Annotated[list,add_messages]
from langchain.chat_models import init_chat_model



@tool
def run_command(cmd: str) -> str:
    """Executes a command on user's system and returns the output."""
    try:
        print(cmd)
        # This will work for both terminal commands and GUI apps
        completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return completed.stdout if completed.stdout else completed.stderr
    except Exception as e:
        return str(e)


llm= init_chat_model( model_provider="openai",model="gpt-4.1")
llm_with_tool=llm.bind_tools(tools=[run_command])

def chatbot(state:State):
    system_prompt=SystemMessage(content="""Your name is Vicky.You are an AI coding assistant who takes an input from user and based on available tools you choose correct tool and execute commands.ALways make sure 
                                to keep your files in chat_gpt/folder .You can create one if it is already not present there .You can even execute commands and help user with the output of the command.You have access to open applications on my system too""")
    message=llm_with_tool.invoke([system_prompt]+state["messages"])
    assert len(message.tool_calls)<=1
    return {"messages":[message]}


tool_node=ToolNode(tools=[run_command])


graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",tool_node)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
graph_builder.add_edge("tools","chatbot")
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)