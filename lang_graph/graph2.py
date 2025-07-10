from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
#to pause flow by ai (tool is decorator over here) 
from langchain_core.tools import tool
from langgraph.types import interrupt
from langgraph.prebuilt import ToolNode,tools_condition
llm=init_chat_model(model_provider="openai",model="gpt-4.1")
MONGODB_URI="mongodb+srv://vimalnegi2003:Vimal@cluster0.up4jy8m.mongodb.net"

#AI will call this function 
@tool()
def human_assistance_tool(query:str):
    '''Request assistance from a human.'''
    human_response=interrupt({"query":query}) #graph will exit out after saving data in DB
    return human_response["data"] #resume with data then call will be forwaded from here only

tools=[human_assistance_tool]
tool_node=ToolNode(tools=[tool])
llm_with_tools=llm.bind_tools(tools=tools)
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages] #rather than overriding we can just append the message
def chatbot(state:State):
    message=llm_with_tools.invoke(state['messages'])
    assert len(message.tool_calls)<=1
    return {"messages":[message]}

tool_node=ToolNode(tools=tools)
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

#without any memory
graph=graph_builder.compile()
#human in loop basically when we want to interrupt execution for example you want to comfirm something then it is used
# graph.interrupt_after_nodes("confirm_transaction")

#basically adds memory
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
