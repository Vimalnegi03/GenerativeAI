from graph2 import graph


def init():
    while True:
        user_input=input("> ")
        for event in graph.stream({"messages":[{"role":"user","content":user_input}]},stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()


init()        