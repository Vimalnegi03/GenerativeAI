import streamlit as st
import re
import json
from collections import defaultdict
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os

# ------------------------- CONFIG -------------------------
st.set_page_config(page_title="AI PDF Assistant", layout="wide")

# Load API keys
openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY")

loader = PyPDFLoader("ai.pdf")
pages = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = splitter.split_documents(pages)

api_key = os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)
# Clients

client = OpenAI(api_key=gemini_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# Load retriever
retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="ai",
    embedding=embedder
)

# ------------------------ FUNCTIONS ------------------------
def break_question_with_gemini(query):
    system_prompt = '''you are an smart agent that basically takes a user question and on the basis of user question you break the question into the parts and generate exactly three question from it
Example:
Input: What is machine learning?
Answer:
["What is machine?", "What is learning?", "What is machine learning?"]
Only output the JSON array.
'''
    res = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": query}]
    )
    content = res.choices[0].message.content
    if content.startswith("```"):
        content = re.sub(r"```(?:json)?\n?", "", content).rstrip("`")
    return json.loads(content)


def apply_rrf(lists, k=60):
    scores = defaultdict(float)
    id_to_doc = {}
    for result_list in lists:
        for rank, doc in enumerate(result_list):
            doc_id = doc.metadata.get("source", "") + str(doc.metadata.get("page", "")) + doc.page_content[:50]
            scores[doc_id] += 1 / (k + rank)
            id_to_doc[doc_id] = doc
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [id_to_doc[doc_id] for doc_id, _ in ranked_docs]


def build_response(user_query, fused_chunks):
    formatted_chunks = "\n\n".join(
        f"Page {doc.metadata.get('page', '?')}: {doc.page_content[:700]}..." for doc in fused_chunks
    )

    prompt = f'''You are a smart AI agent that answers the user query based on relevant PDF chunks.
Relevant chunks are listed below with page numbers. Provide:
1. A detailed answer to the user question.
2. A brief summary of other related content.
3. Page numbers for deeper reference.

{formatted_chunks}

User Query:
{user_query}
'''

    res = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_query}]
    )
    return res.choices[0].message.content


# ------------------------ UI ------------------------
st.title("📘 AI PDF Assistant")
st.write("Ask a question related to your `ai.pdf`, and get a detailed, referenced answer.")

user_query = st.text_input("🔍 Enter your question")

if user_query:
    with st.spinner("Analyzing and generating response..."):
        try:
            # Step 1: Break into subquestions
            question_array = break_question_with_gemini(user_query)
            all_questions = [user_query] + question_array[:3]

            # Step 2: Retrieve from Qdrant
            all_results = [retriever.similarity_search(query=q, k=5) for q in all_questions]

            # Step 3: Fuse with RRF
            fused_chunks = apply_rrf(all_results)

            # Step 4: Build final response
            final_answer = build_response(user_query, fused_chunks)

            # Show output
            st.markdown("### 🤖 Answer")
            st.markdown(final_answer)

        except Exception as e:
            st.error(f"❌ Error: {e}")
