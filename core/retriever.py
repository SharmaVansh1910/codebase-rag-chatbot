# core/retriever.py
import os
from dotenv import load_dotenv
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
# Load environment variables
load_dotenv()
def load_vectorstore(persist_dir: str = "./chroma_db"):
    """
    Loads existing ChromaDB vectorstore from disk.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
       model="models/text-embedding-004",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    return vectorstore
def ask_question(question: str, persist_dir: str = "./chroma_db"):
    """
    Full RAG pipeline:
    - Load DB
    - Retrieve relevant chunks
    - Build prompt
    - Query Gemini
    - Return answer
    """
    # 1. Load vectorstore
    vectorstore = load_vectorstore(persist_dir)
    # 2. Retrieve top 4 relevant chunks
    results = vectorstore.similarity_search(question, k=4)
    if not results:
        return "No relevant code found."
    # 3. Build context
    context_parts = []
    for doc in results:
        filename = doc.metadata.get("filename", "unknown")
        content = doc.page_content
        context_parts.append(
            f"--- {filename} ---\n{content}"
        )
    context = "\n\n".join(context_parts)
    # 4. Build prompt
    prompt = f"""
You are a code assistant. Use the following code snippets to answer the question.
Code context:
{context}
Question: {question}
Answer:
"""
    # 5. Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    )
    # 6. Get response
    response = llm.invoke([
        HumanMessage(content=prompt)
    ])
    return response.content