import os
import time
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv


load_dotenv()

# Global cache for embeddings model (expensive to load)
_embeddings_cache = None
_db_cache = None


def get_embeddings():
    """Lazy-load embeddings model once and cache it."""
    global _embeddings_cache
    if _embeddings_cache is None:
        print("[AUDIT] Loading embeddings model (first time only, ~30s)...")
        _embeddings_cache = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embeddings_cache


def get_db():
    """Lazy-load Chroma DB once and cache it."""
    global _db_cache
    if _db_cache is None:
        print("[AUDIT] Loading Chroma DB...")
        embeddings = get_embeddings()
        _db_cache = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    return _db_cache


def audit_protocol(protocol_text, fast_mode=False):
    """Audit a clinical protocol.
    
    Args:
        protocol_text: The protocol text to audit.
        fast_mode: If True, only retrieve guidelines (no Gemini call). ~2-3s instead of 20-30s.
    
    Returns:
        Audit result string.
    """
    start = time.time()
    
    # Truncate very long protocols to avoid hitting token limits
    max_chars = 15000
    if len(protocol_text) > max_chars:
        protocol_text = protocol_text[:max_chars] + f"\n\n[... truncated, original was {len(protocol_text)} chars]"
        print(f"[AUDIT] Truncated protocol to {max_chars} chars")
    
    # Step 1: Retrieve guidelines
    print("[AUDIT] Retrieving relevant guidelines...")
    db = get_db()
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(protocol_text)
    context_text = "\n\n".join([d.page_content for d in docs])
    retrieval_time = time.time() - start
    print(f"[AUDIT] Retrieval done in {retrieval_time:.1f}s")
    
    if fast_mode:
        # Quick summary: just return the retrieved guidelines
        result = f"""FAST MODE AUDIT (guidelines-only, no LLM analysis)
Retrieved {len(docs)} relevant guidelines:
---
{context_text}
---
For full AI-powered analysis, disable Fast Mode in Settings."""
        print(f"[AUDIT] Fast mode complete in {time.time() - start:.1f}s")
        return result
    
    # Step 2: Call Gemini for full audit
    print("[AUDIT] Calling Gemini API for analysis...")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set. Use fast_mode=True to skip LLM analysis.")
    
    prompt = PromptTemplate(
        input_variables=["protocol", "context"],
        template="""You are a strict regulatory auditor. 
Guidelines: {context}
Protocol to audit: {protocol}
Identify any contradictions or safety gaps. Be concise."""
    )
    
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
        google_api_key=gemini_api_key,
    )
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"protocol": protocol_text, "context": context_text})
    total_time = time.time() - start
    print(f"[AUDIT] Full audit done in {total_time:.1f}s")
    return result