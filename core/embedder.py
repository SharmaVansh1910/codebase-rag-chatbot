import os
import shutil
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()


def embed_and_store(code_files: list, persist_dir: str = "./chroma_db"):
    """
    Takes code files, chunks them, embeds them, and stores them in ChromaDB.
    """

    # Delete old vector DB before creating a new one
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    # Text Splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )

    documents = []

    # Convert files into LangChain Documents
    for file in code_files:

        filename = file["filename"]
        content = file["content"]

        chunks = splitter.split_text(content)

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "filename": filename
                    }
                )
            )

    if len(documents) == 0:
        print("No documents found.")
        return None

    # Gemini Embeddings
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create Vector Store
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    print("=" * 50)
    print(f"Indexed {len(documents)} chunks")
    print(f"Vector DB saved at: {persist_dir}")
    print("=" * 50)

    return vectorstore