from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)

text="the cat sat on mat"

response=client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)
print(response.data[0].embedding )