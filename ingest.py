from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

# 1. Use the exact same embedding model as your auditor.py
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Define the path to your regulatory document
# Ensure this file exists in your root folder
file_path = "data/guideline.pdf"
if not os.path.exists(file_path):
    print(f"❌ Error: {file_path} not found. Please place your PDF in the root folder.")
else:
    # 3. Load and split the document
    print("📖 Loading PDF...")
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 4. Ingest into ChromaDB
    print("🚀 Ingesting into Vector Database...")
    db = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory="chroma_db"
    )
    print("✅ Successfully created chroma_db!")