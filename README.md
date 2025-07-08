# GenerativeAI Experiments

A modular and extensible playground for experimenting with various Generative AI strategies including chain-of-thought reasoning, custom tokenization, embeddings, memory-augmented retrieval (RAG), and multi-provider LLM integration.

## 📁 Project Structure

```
GenerativeAI/
├── chainOfThoughts*.py # CoT prompts (manual & auto, OpenAI & Gemini)
├── few_shots*.py # Few-shot examples
├── zero_shot_prompting*.py # Zero-shot examples
├── personaBasedPrompting*.py # Persona-based prompting
├── role_playing*.py # Role-playing prompt agents
├── embeddings.py # Embedding generation utility
├── memory_rag.py # Memory-augmented RAG
├── recirpocate_rank_fusion_in_rag.py # RRF scoring for RAG
├── tokenizer*.py # Tokenizer setup (HuggingFace)
├── ollama_api.py # Ollama integration
├── weather_agent*.py # Sample agent for weather queries
├── read*.py # Sample agent used to basically generate markdown of code explanation of each line
├── sql*.py # Sample agent used to basically used to interact with database using NLP
├── webscrapper*.py #used to scrap chai_code_docs and generate output used query_routing in this
├── docker-compose.*.yml # Docker configs
├── requirements.txt # Dependencies
├── *.ipynb # Tokenizer experiments
├── *.pdf # Reference docs

```
## 🚀 Features

✅ Chain-of-Thought reasoning with OpenAI & Gemini  
✅ Few-shot and zero-shot prompt engineering  
✅ Persona-based and role-playing bots  
✅ Custom tokenizer using HuggingFace  
✅ Retrieval-Augmented Generation (RAG) pipelines  
✅ Reciprocal Rank Fusion scoring for better document retrieval  
✅ Dockerized microservice-ready setup  
✅ Integration with Gemini, OpenAI, Ollama APIs  
✅ Real-world agent demo: Weather Bot,Sql query writer,Mini Cursor,Read me generator
✅ Web Scrapping with Multi query routing
✅ Avanced Rags with query translation  

---

## 🌐 APIs Integrated
OpenAI GPT-3.5 / GPT-4

Gemini Pro

HuggingFace Transformers

Ollama (local LLM APIs)

## 🧾 Requirements
All dependencies are listed in requirements.txt. Major libraries:

openai

google-generativeai

langchain

huggingface_hub

transformers

faiss-cpu / chromadb

## 🚀 How to Run

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Vimalnegi03/GenerativeAI/
   cd GenerativeAI
   ```

2. **Set up environment:**
   Install dependencies via pip or poetry:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Docker services (optional):**
   ```bash
   docker-compose up -d
   ```

4. **Experiment with scripts or notebooks:**
   - Launch Jupyter: `jupyter notebook`
   - Or run any `.py` script directly with proper API keys configured.

## 📊 Example Use Cases
🔁 Chain-of-Thought Prompting
```
python chainOfThoughtsAuto.openAI.py

```
🧠 Retrieval-Augmented Generation

```
python memory_rag.py

```
🎭 Persona Prompting (Gemini)
```
python personaBasedPrompting.gemini.py

```
## 🧪 Notebooks

Tokenizer.huggingface.ipynb: Tokenizer setup using pretrained models

own_Tokenizer.huggingFace.ipynb: Custom tokenizer for domain-specific vocab

# 📌 Notes
API keys must be stored as environment variables:

OPENAI_API_KEY

GOOGLE_GEMINI_API_KEY

Docker setup supports additional services like vector DB and graph DB.

## 📄 License

MIT License (or specify if different)

## ✍️ Author

- Vimal Negi
- Contact: [vimalnegi2003@gmail.com]
