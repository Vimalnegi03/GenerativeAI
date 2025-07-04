from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
NEO4J_URL="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="reform-william-center-vibrate-press-5829"
QUADRANT_HOST="localhost"
config={
    "version":"v1.1",
    #vector embedding
    "embedder":{
        "provider":"openai",
        "config":{"api_key":OPENAI_API_KEY,"model":"text-embedding-3-small"},
    },
    #which llm to use
    "llm":{"provider":"openai","config":{"api_key":OPENAI_API_KEY,"model":"gpt-4.1"}},
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host":QUADRANT_HOST,
            "port":6333,
        },
    },
    "graph_store":{
        "provider":"neo4j",
        "config":{"url":NEO4J_URL,"username":NEO4J_USERNAME,"password":NEO4J_PASSWORD},
    },

}
# Create instance of memory
mem_client=Memory.from_config(config)
openai_client=OpenAI(api_key=OPENAI_API_KEY)
def chat(message):
    #to search particular message in memory
    mem_result=mem_client.search(query=message,user_id="p123")
    memories="\n".join([m["memory"]for m in mem_result.get("results")])
   

    SYSTEM_PROMPT=f"""
    You are a Memory-Aware Fact Extraction Agent , an advanced AI designed to systematically analyze input content,extract structured knowldege,and maintain an
    optimized memory store. Your primary function is information distillation and knowledge preservation with contextual awareness.
    Tone:Professional analytical,precison-focused,with clear uncertainity signaling
    {memories}
"""    
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":message}
    ]
    result=openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
    )

    messages.append(
        {
            "role":"assistant","content":result.choices[0].message.content
        }
    )
    #to add things to memory
    mem_client.add(messages,user_id="p123")

    return result.choices[0].message.content
while True:
    message=input(">>")
    print("BOT:",chat(message=message))