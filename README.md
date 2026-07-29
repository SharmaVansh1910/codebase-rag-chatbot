# 🚀 Codebase RAG Chatbot

> AI-powered GitHub Codebase Assistant that lets you chat with any public GitHub repository using Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

Codebase RAG Chatbot is an AI-powered developer assistant that enables users to understand any public GitHub repository through natural language.

Instead of manually exploring hundreds of files, users simply provide a GitHub repository URL, and the application indexes the repository, creates semantic embeddings, and answers questions about the codebase using Retrieval-Augmented Generation (RAG).

---

# ✨ Features

- 🔗 Index any public GitHub repository
- 📂 Automatic repository cloning
- 🧠 Semantic code search using embeddings
- ⚡ Fast Retrieval-Augmented Generation (RAG)
- 💬 Chat with an entire codebase
- 📄 Source file attribution
- 🗄️ Chroma Vector Database
- 🚀 Groq LLM Integration
- 🎯 Streamlit Interactive UI

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|-------------|
| Language | Python |
| LLM | Groq (Llama 3.3 70B) |
| Embeddings | HuggingFace Sentence Transformers |
| Vector Database | ChromaDB |
| Framework | LangChain |
| Frontend | Streamlit |
| Repository Loader | GitPython |
| Environment | python-dotenv |

---

# 🏗 Architecture

```text
                Public GitHub Repository
                         │
                         ▼
                Clone Repository
                  (GitPython)
                         │
                         ▼
                Load Code Files
                         │
                         ▼
                Chunk Source Code
                         │
                         ▼
          HuggingFace Embeddings
                         │
                         ▼
                 Chroma Vector DB
                         │
        ┌──────────────────────────┐
        │                          │
        ▼                          ▼
 User Question              Similarity Search
        │                          │
        └──────────────┬───────────┘
                       ▼
                 Retrieved Context
                       │
                       ▼
                 Groq Llama 3.3
                       │
                       ▼
          AI Answer + Source Files
```

---

# 📂 Project Structure

```text
codebase-rag-chatbot/

│
├── core/
│   ├── loader.py
│   ├── embedder.py
│   └── retriever.py
│
├── ui/
│   └── app.py
│
├── chroma_db/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/codebase-rag-chatbot.git

cd codebase-rag-chatbot
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

## Run

```bash
streamlit run ui/app.py
```

---

# 🚀 Usage

### Step 1

Paste any public GitHub Repository URL

Example

```
https://github.com/langchain-ai/langchain
```

---

### Step 2

Click

```
Index Codebase
```

The application will

- Clone the repository
- Read source files
- Chunk code
- Generate embeddings
- Store vectors in ChromaDB

---

### Step 3

Ask questions like

```
Explain the architecture.

How does authentication work?

Which file handles embeddings?

Where is the API routing implemented?

How is retrieval implemented?
```

---

# 📷 Screenshots

### Home Page

(Add Screenshot Here)

---

### Repository Indexing

(Add Screenshot Here)

---

### AI Chat

(Add Screenshot Here)

---

# 🎥 Demo

(Add Google Drive / YouTube Demo Link)

---

# 💡 Future Improvements

- Multi Repository Support
- Hybrid Search (BM25 + Dense Retrieval)
- Cross Repository Reasoning
- Conversation Memory
- Local LLM Support
- Code Graph Retrieval
- Repository Summarization
- PDF Documentation Generation

---

# 🤝 Contributing

Contributions are always welcome.

Fork the repository and submit a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Vansh Sharma**

GitHub:
https://github.com/SharmaVansh1910

LinkedIn:
(Add LinkedIn)

Portfolio:
(Add Portfolio)

---

⭐ If you found this project useful, don't forget to star the repository.
