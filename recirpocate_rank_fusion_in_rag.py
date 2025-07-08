import re
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("ai.pdf")
pages = loader.load()
print(pages[0])

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(pages)
print(len(texts))


from langchain_openai import OpenAIEmbeddings
import os
api_key=os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(model="text-embedding-3-large",api_key=api_key)

from langchain_qdrant import QdrantVectorStore
# qdrant_store = QdrantVectorStore.from_documents(
#     documents=[],
#     embedding=embedder,
#     url="http://localhost:6333",
#     collection_name="ai",
# )
# qdrant_store.add_documents(documents=texts)
# print("injestion part completed")

import os
from openai import OpenAI
gemini_api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
user_query=input("Enter your question")
System_Prompt=f'''you are an smart agent that basically takes a user question and on the basis of user question you break the question into the parts and generate exactly three question from it
Example :
Input:
User asked What is machine learning ?
Answer:
What is machine ?
What is learning ?
What is machine learning?
Like this breakdown the user question into three related questions 
Only output the JSON array.
'''
import json
client=OpenAI(api_key=gemini_api_key,
              base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
questions=client.chat.completions.create(
    model='gemini-2.0-flash',
    messages=[{"role":"system","content":System_Prompt},{"role":"user","content":user_query}]
)
question_array=questions.choices[0].message.content
if question_array.startswith("```json") or question_array.startswith("```"):
    question_array = re.sub(r"```(?:json)?\n?", "", question_array)
    question_array =question_array.rstrip("`")
try:
    question_array = json.loads(question_array)
    print("User Question:", question_array[0])
    print("Q1:", question_array[1])
    print("Q2:", question_array[2])
   
except json.JSONDecodeError as e:
    print("❌ JSON parsing failed.")
    print("Raw content was:\n", question_array)
    print("Error:", e)    

retriever=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
 collection_name="ai",#table_name
embedding=embedder
)    

#data extraction 
relevant_chunks=[1,2,3,4]
relevant_chunks[0]=retriever.similarity_search(
    query=user_query,
    )
relevant_chunks[1]=retriever.similarity_search(
    query=question_array[0],
    )
relevant_chunks[2]=retriever.similarity_search(
    query=question_array[1],
)
relevant_chunks[3]=retriever.similarity_search(
    query=question_array[2],
)    

# print(relevant_chunks)
#RRF -:Reciprocate rank fusion 
from collections import defaultdict

def apply_rrf(lists, k=60):
    """Apply Reciprocal Rank Fusion to combine multiple ranked lists."""
    scores = defaultdict(float)
    
    for result_list in lists:
        for rank, doc in enumerate(result_list):
            doc_id = doc.metadata.get("source", "") + str(doc.metadata.get("page", "")) + doc.page_content[:50]
            scores[doc_id] += 1 / (k + rank)
    
    # Sort by combined score descending
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Retrieve the original Document objects (optional)
    id_to_doc = {}
    for result_list in lists:
        for doc in result_list:
            doc_id = doc.metadata.get("source", "") + str(doc.metadata.get("page", "")) + doc.page_content[:50]
            id_to_doc[doc_id] = doc

    fused_results = [id_to_doc[doc_id] for doc_id, _ in ranked_docs]
    return fused_results

all_results = []

for query in [user_query] + question_array[1:4]:
    result = retriever.similarity_search(query=query, k=5)  # Or `similarity_search_with_score`
    all_results.append(result)

fused_chunks = apply_rrf(relevant_chunks)
formatted_chunks = "\n\n".join(
    f"Page {doc.metadata.get('page', '?')}: {doc.page_content[:700]}..." for doc in fused_chunks
)


Main_prompt=f'''You are an smart ai agent that basically answer the user query on the basis of relevant chunks available. The relevant_chunk is basically in form of array 
so along with the content provide the user with page number  so that if they want more details they can refer to that pages in pdf and provide user with summary of relevant chunks.
The summary should include detail explanation of his query and short explanations of other relevant chunks .
{formatted_chunks}
Example :
User_query
What is an AI ?
Answer:
AI is the branch of science that deals with the creation of machine that have ability to think and make decison on their own . AI term was coined by Allen Turing in 1950 .AI can be implemented
using machine learning,neural newtorks, computer vision,Natural learning processing like this an detailed explanation
and the other topic in relevant chunks should be explained in short
for example if relative chunks include types of ai techniques name them and explain them in few lines and provide  page number of pdf for reference 
Like this provide a detailed answer 
 '''

response=client.chat.completions.create(
    model='gemini-2.0-flash',
    messages=[{"role":"system","content":Main_prompt},{"role":"user","content":user_query}]
)

print(response.choices[0].message.content)