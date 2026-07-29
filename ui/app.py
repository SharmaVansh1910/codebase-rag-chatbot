import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from core.loader import load_github_repo
from core.embedder import embed_and_store
from core.retriever import ask_question


if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False


st.sidebar.title("📂 Index Codebase")

repo_url = st.sidebar.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/user/repo"
)

if st.sidebar.button("Index Codebase"):

    if not repo_url:
        st.sidebar.error("Please enter a GitHub repository URL.")

    else:

        with st.sidebar.spinner("Cloning repository..."):

            try:

                code_files = load_github_repo(repo_url)

                embed_and_store(code_files)

                st.session_state.indexed = True

                st.sidebar.success(f"Indexed {len(code_files)} files!")

            except Exception as e:

                st.sidebar.error(str(e))


st.title("💬 Codebase Q&A (RAG)")


for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if not st.session_state.indexed:

    st.info("Index a GitHub repository first.")

    prompt = st.chat_input("Ask about the repository...", disabled=True)

else:

    prompt = st.chat_input("Ask about the repository...")


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = ask_question(prompt)

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )