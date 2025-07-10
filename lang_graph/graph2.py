from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
#to pause flow by ai (tool is decorator over here) 
from langchain_core.tools import tool
llm=init_chat_model(model_provider="openai",model="gpt-4.1")
MONGODB_URI="mongodb+srv://@cluster0.up4jy8m.mongodb.net"
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages] #rather than overriding we can just append the message
def chatbot(state:State):
    messages=state.get("messages")
    response=llm.invoke(messages)
    return {"messages":[response]}

graph_builder=StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

#without any memory
graph=graph_builder.compile()
#human in loop basically when we want to interrupt execution for example you want to comfirm something then it is used
# graph.interrupt_after_nodes("confirm_transaction")

#basically adds memory
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
