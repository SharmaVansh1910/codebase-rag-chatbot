import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage

# Load .env
load_dotenv()


def load_vectorstore(persist_dir: str = "./chroma_db"):
    """
    Load existing ChromaDB.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
    )

    return vectorstore


def ask_question(question: str, persist_dir: str = "./chroma_db"):
    """
    Full RAG Pipeline

    1. Load Chroma
    2. Retrieve relevant chunks
    3. Build prompt
    4. Query Gemini
    5. Return answer + source files
    """

    # Load Vector DB
    vectorstore = load_vectorstore(persist_dir)

    # Better Retriever (MMR)
    # retriever = vectorstore.as_retriever(
    #     search_type="mmr",
    #     search_kwargs={
    #         "k": 6,
    #         "fetch_k": 20,
    #     },
    # )

    results = vectorstore.similarity_search_with_score(
        question,
        k=6
        )    
    if len(results) == 0:
        return "No relevant code found."

    context_parts = []
    source_files = []

    for doc, score in results:

        filename = doc.metadata.get("filename", "Unknown File")
        confidence = max(0, min(100, int((1 - score) * 100)))

        source_files.append((filename, score))

        context_parts.append(
            f"""
    FILE: {filename}

    {doc.page_content}
    """
        )
        
    context = "\n\n".join(context_parts)

    prompt = f"""
You are an expert Software Engineer helping developers understand an unfamiliar codebase.Always infer the overall architecture by combining information from multiple files if needed.If the answer spans multiple files, summarize across all retrieved files.
IMPORTANT:
- Only use information explicitly present in the retrieved context.
- Never mention Google Generative AI, Gemini Embeddings, or any library/framework unless it appears in the retrieved code.
- If unsure, say "I couldn't find that information in the indexed codebase."

Base your answer strictly on the retrieved code snippets.
Strict Rules:

- Answer ONLY using the provided context.
- If the answer is not present, clearly say you couldn't find it.
- Mention filenames whenever possible.
- Do not hallucinate.
- Keep the answer concise but technically accurate.

==========================
CODE CONTEXT
==========================

{context}

==========================
QUESTION
==========================

{question}

==========================
ANSWER
==========================
"""

    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0.2,
    )
    response = llm.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    answer = response.content

    answer += "\n\n---\n"
    answer += "📄 Sources Used:\n"

    seen = set()

    for filename, _ in source_files:
        if filename in seen:
            continue
        seen.add(filename)
        answer += f"✅ {filename}\n"

    return answer