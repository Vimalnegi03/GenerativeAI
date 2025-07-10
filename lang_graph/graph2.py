from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
llm=init_chat_model(model_provider="openai",model="gpt-4.1")
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

graph=graph_builder.compile()

