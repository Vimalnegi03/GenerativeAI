from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
pdf_path=Path(__file__).parent /"resume.pdf"  #current directory mai jo resume_(2).pdf naam ki file hai
api_key=os.getenv("OPENAI_API_KEY")
loader=PyPDFLoader(file_path=pdf_path)
docs=loader.load()
#to create documents (chunking')
# print(docs[0]) #docs is an array that have pagecontent and metadata 
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,# this is the number of characters in chunnk
    chunk_overlap=200, #no. of overlapping characters
)

split_docs=text_splitter.split_documents(documents=docs)
# print(len(split_docs))


#embeddings
embedder=OpenAIEmbeddings(
    model='text-embedding-3-large',
    api_key=api_key
)
#vector store
# vector_store=QdrantVectorStore.from_documents(
# documents=[],
# url="http://localhost:6333",
# collection_name="resume1",#table_name
# embedding=embedder #which embedding model to use
# )

# vector_store.add_documents(documents=split_docs) #done with ingestion over here

#now retrieval
retriever=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
 collection_name="resume1",#table_name
embedding=embedder
)
relevant_chunks=retriever.similarity_search(
    query="What are skills in this resume ?"
    ) #creating embedding of what user asked and gives relevant chunks as output

# print("Relevant chunks",relevant_chunks)
SYSTEM_PROMPT=f"""
you are an helpful ai assistant who responds base on the available context provide answer to the user based on the available context you provide the page_number and page_content to the user 
Context:
{relevant_chunks}
"""

client=OpenAI(api_key=api_key)

res=client.chat.completions.create(
    model='gpt-4o',
    messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":"What are the skills in this resume ?"}]
)
print(res.choices[0].message.content)