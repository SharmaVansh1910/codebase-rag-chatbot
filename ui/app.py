# ui/app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



import streamlit as st
from core.loader import load_code_files
from core.embedder import embed_and_store
from core.retriever import ask_question
# -------------------------
# Session State Init
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed" not in st.session_state:
    st.session_state.indexed = False
# -------------------------
# Sidebar — Index Codebase
# -------------------------
st.sidebar.title("📂 Index Codebase")
folder_path = st.sidebar.text_input("Enter folder path")
if st.sidebar.button("Index Codebase"):
    if not folder_path:
        st.sidebar.error("Please enter a valid folder path.")
    else:
        with st.sidebar.spinner("Indexing codebase..."):
            try:
                code_files = load_code_files(folder_path)
                embed_and_store(code_files)
                st.session_state.indexed = True
                st.sidebar.success(f"Indexed {len(code_files)} files successfully!")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
# -------------------------
# Main UI — Chat Interface
# -------------------------
st.title("💬 Codebase Q&A (RAG)")
# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# -------------------------
# Chat Input
# -------------------------
if not st.session_state.indexed:
    st.info("Index a codebase first from the sidebar to start asking questions.")
    user_input = st.chat_input("Ask about your code...", disabled=True)
else:
    user_input = st.chat_input("Ask about your code...")
if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching codebase..."):
            try:
                answer = ask_question(user_input)
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })