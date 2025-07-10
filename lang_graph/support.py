from graph2 import graph
from graph2 import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver
import json
#to return or resume back to ai we use command
from langgraph.types import Command 
MONGODB_URI="mongodb+srv://vimalnegi2003:Vimal@cluster0.up4jy8m.mongodb.net"
config={"configurable":{"thread_id":"6"}}
def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo=create_chat_graph(checkpointer=checkpointer)
        state=graph_with_mongo.get_state(config=config)
        for message in state.values['messages']:
            message.pretty_print()
        last_message=state.values['messages'][-1]
        tool_calls=last_message.additional_kwargs.get("tool_calls",[])
        print("Tool calls:", tool_calls)
        user_query=None
        for call in tool_calls:
            if call.get("function",{}).get("name")=="human_assistance_tool":
                args=call["function"].get("arguments","{}")
                try:
                    args_dict=json.loads(args)
                    user_query=args_dict.get("query")
                except json.JSONDecodeError:
                    print("Failed to deccode")
        print("user is trying to ask :",user_query)  
        #support person giving answer 
        ans=input("Resolution >")  
        resume_command=Command(resume={"data":ans})     
        for event in graph_with_mongo.stream(resume_command,config,stream_mode="values") :
            if "messages" in event:
                event["messages"][-1].pretty_print()


init()        