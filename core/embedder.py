# core/embedder.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

def embed_and_store(code_files: list, persist_dir: str = "./chroma_db"):
    """
    Takes code files, chunks them, embeds them, and stores in ChromaDB.
    """
    # 1. Initialize text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    documents = []
    # 2. Convert each file into chunks
    for file in code_files:
        filename = file["filename"]
        content = file["content"]
        chunks = splitter.split_text(content)
        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={"filename": filename}
                )
            )
    if not documents:
        print("No documents to embed.")
        return None
    # 3. Initialize Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )
    # 4. Store in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    # 5. Persist to disk
    # vectorstore.persist()
    print(f"Stored {len(documents)} chunks in ChromaDB at '{persist_dir}'")
    return vectorstore