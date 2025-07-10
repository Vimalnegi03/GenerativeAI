from graph2 import graph
from graph2 import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver
MONGODB_URI="mongodb+srv://@cluster0.up4jy8m.mongodb.net"
config={"configurable":{"thread_id":"1"}}
def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo=create_chat_graph(checkpointer=checkpointer)
        while True:
            user_input=input("> ")
            for event in graph_with_mongo.stream({"messages":[{"role":"user","content":user_input}]},config,stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()


init()        