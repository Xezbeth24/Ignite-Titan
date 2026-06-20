import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from src.auditor import audit_protocol
from src.utils import scrub_pii, summarize_redaction


# Page Config
st.set_page_config(
    page_title="The Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* Center title */
.stApp .css-1v3fvcr h1{font-size:34px}
.title{display:flex;align-items:center;gap:12px}
.card{background:#ffffff; padding:18px; border-radius:8px; box-shadow:0 4px 18px rgba(0,0,0,0.06)}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='title'>🛡️ <strong>The Auditor: Clinical Protocol Checker</strong></div>", unsafe_allow_html=True)


# Sidebar: settings and guidance
with st.sidebar:
    st.header("Settings")
    k = st.number_input("Retriever k (top docs)", min_value=1, max_value=10, value=3)
    show_raw = st.checkbox("Show raw protocol text after upload", value=False)
    enable_scrub = st.checkbox("Enable PII scrub (recommended)", value=True)
    fast_mode = st.checkbox("Fast Mode (guidelines only, ~2-3s)", value=False)
    if fast_mode:
        st.info("Fast mode skips AI analysis. Run full audit for detailed feedback.")
    st.markdown("---")
    st.header("NLP Guidelines")
    st.markdown("Refer to the project checklist: [NLP Guidelines](NLP_GUIDELINES.md)")
    st.markdown("---")
    gemini_key = os.getenv("GEMINI_API_KEY")
    model_default = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
    st.text_input("LLM Model (env override)", value=model_default, key="model_name")
    if not gemini_key and not fast_mode:
        st.warning("GEMINI_API_KEY is not set; full audits will fail. Use Fast Mode instead.")


# Main area: file uploader + actions
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("Upload Clinical Protocol (PDF)", type=["pdf"]) 
    st.info("Upload a PDF and click Run Audit. Use sidebar to tune settings.")
    sample_btn = st.button("Use sample guideline PDF")

with col2:
    st.write("")

temp_path = None

if sample_btn:
    sample_path = os.path.join("data", "guideline.pdf")
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            uploaded_bytes = f.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_bytes)
            temp_path = tmp.name
    else:
        st.error("Sample guideline not found in data/guideline.pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

if temp_path:
    try:
        loader = PyPDFLoader(temp_path)
        pages = loader.load()
        protocol_text = "\n".join([page.page_content for page in pages])
        if show_raw:
            st.expander("Raw protocol text").write(protocol_text[:10000])

        if st.button("Run Audit", key="run_audit"):
            if enable_scrub:
                redacted, counts = scrub_pii(protocol_text)
                st.info(summarize_redaction(counts))
                protocol_to_audit = redacted
            else:
                protocol_to_audit = protocol_text

            if not fast_mode and not os.getenv("GEMINI_API_KEY"):
                st.error("GEMINI_API_KEY is not configured. Set it or use Fast Mode to run audits.")
            else:
                with st.spinner("🔍 Running audit..."):
                    try:
                        result = audit_protocol(protocol_to_audit, fast_mode=fast_mode)
                        st.success("✅ Audit complete")
                        st.markdown("### 📋 Audit Results")
                        st.download_button("Download results", data=result, file_name="audit_results.txt")
                        st.expander("Full audit output").write(result)
                    except Exception as e:
                        st.error(f"❌ Error during audit: {e}")
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

else:
    st.info("No protocol loaded — upload a PDF or use the sample from the sidebar.")