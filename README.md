# GenerativeAI Experiments

A modular and extensible playground for experimenting with various Generative AI strategies including chain-of-thought reasoning, custom tokenization, embeddings, memory-augmented retrieval (RAG), and multi-provider LLM integration.

## 📁 Project Structure

```
GenerativeAI/
│
├── chainOfThoughtsAuto.gemini.py         # Automatic CoT with Gemini
├── chainOfThoughtsAuto.openAI.py         # Automatic CoT with OpenAI
├── chainOfThoughtsmanual.gemini.py       # Manual CoT with Gemini
├── chainOfThoughtsmanual.openAI.py       # Manual CoT with OpenAI
│
├── few_shots.gemini.py                   # Few-shot prompting with Gemini
├── few_shots.openAI.py                   # Few-shot prompting with OpenAI
│
├── tokenizer.huggingface.ipynb           # Tokenizer setup using HuggingFace
├── own_Tokenizer.huggingFace.ipynb       # Custom tokenizer example
│
├── embeddings.py                         # Embedding generation utilities
├── memory_rag.py                         # RAG (Retrieval Augmented Generation)
│
├── ollama_api.py                         # Integration with Ollama API
├── cursor.auto.gemini.py                 # Gemini integration (possibly cursor-like)
│
├── docker-compose.yaml                   # Base Compose setup
├── docker-compose.db.yml                 # DB-specific services
├── docker-compose.graph.yml              # Graph DB services
│
├── Node.pdf                              # Possibly documentation or architecture
├── check.py                              # Utility script
├── .gitignore
```

## 🔧 Requirements

- Python 3.8+
- Jupyter (for notebooks)
- Docker & Docker Compose
- LLM API access (e.g., OpenAI, Gemini, Ollama)

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

## 🧠 Key Features

- ✅ Chain-of-Thought prompting (manual & automated)
- ✅ Few-shot learning with prompt templates
- ✅ HuggingFace tokenizer training
- ✅ Embedding generation
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Docker-based backend (DB/Graph support)
- ✅ Multi-provider LLM integration (OpenAI, Gemini, Ollama)

## 📄 License

MIT License (or specify if different)

## ✍️ Author

- Vimal Negi
- Contact: [vimalnegi2003@gmail.com]
