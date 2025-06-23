import os
import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# UI title
st.title("🧠 Codebase Navigator (Node.js Edition)")
st.markdown("Ask questions about your codebase using AI.")

# Input for OpenAI API Key and directory path
openai_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")
directory_path = st.text_input("📁 Path to your codebase:", value="./your-codebase")

# Proceed only if both values are provided
if openai_key and directory_path:
    os.environ["OPENAI_API_KEY"] = openai_key

    @st.cache_resource
    def load_index():
        exclude_dirs = {'node_modules', 'dist', 'build', '.git', '__pycache__', 'coverage'}
        included_extensions = {'.js', '.ts', '.json', '.md'}
        base_path = Path(directory_path)

        code_files = [
            f for f in base_path.rglob("*")
            if f.suffix in included_extensions and not any(part in exclude_dirs for part in f.parts)
        ]

        documents = []
        for file_path in code_files:
            try:
                loader = TextLoader(str(file_path), encoding='utf-8')
                documents.extend(loader.load())
            except Exception:
                continue

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.split_documents(documents)

        embedding = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embedding)
        retriever = vectorstore.as_retriever(search_type="similarity", k=5)

        return RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-4", temperature=0),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

    qa_chain = load_index()

    # User interaction
    query = st.text_input("💬 Ask a question about the codebase:")
    if query:
        with st.spinner("Searching the codebase..."):
            result = qa_chain(query)
            st.markdown("### 📘 Answer")
            st.write(result["result"])

            st.markdown("### 📁 Sources")
            for doc in result["source_documents"]:
                st.code(doc.metadata.get("source", "Unknown"), language='text')
