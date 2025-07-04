from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Node.pdf")
print(loader)
pages = loader.load()
print(len(pages))
# print(pages[0])

#document loaded now split text

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(pages)
print(len(texts))
print(texts[0])

#now create embedding
import os
api_key=os.getenv("OPENAI_API_KEY")
from langchain_openai import OpenAIEmbeddings
embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=api_key,
)

#now we have embedder

#now vector store
from langchain_qdrant import QdrantVectorStore
# vector_store=QdrantVectorStore.from_documents(
# documents=[],
# url="http://localhost:6333",
# collection_name="nodejs",#table_name
# embedding=embedder #which embedding model to use
# )
# vector_store.add_documents(documents=texts)
print("injestion done")





# *************************************************************
#now retrival phase
user_query=input("Enter your query")
retriever=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
 collection_name="nodejs",#table_name
embedding=embedder
)

#To extract data
relevant_chunks=retriever.similarity_search(
    query=user_query,
    )

SYSTEM_PROMPT=f"""
you are an helpful ai assistant who responds base on the available context provide answer to the user based on the available context you provide the page_number and page_content to the user 
Context:
{relevant_chunks}
"""
from openai import OpenAI
client=OpenAI(api_key=api_key)

res=client.chat.completions.create(
    model='gpt-4o',
    messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_query}]
)
print(res.choices[0].message.content)