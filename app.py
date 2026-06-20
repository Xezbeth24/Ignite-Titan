import os
import re
import tempfile
from pathlib import Path

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

from src.auditor import audit_protocol
from src.utils import scrub_pii, summarize_redaction


st.set_page_config(
        page_title="The Auditor",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
:root {
    --bg: #f4f7fb;
    --panel: rgba(255, 255, 255, 0.84);
    --panel-strong: #ffffff;
    --border: rgba(16, 24, 40, 0.08);
    --text: #172033;
    --muted: #667085;
    --primary: #155eef;
    --primary-soft: rgba(21, 94, 239, 0.12);
    --success: #12b76a;
    --warning: #f79009;
    --danger: #f04438;
    --shadow: 0 18px 50px rgba(16, 24, 40, 0.10);
}

html, body, .stApp {
    background:
        radial-gradient(circle at top left, rgba(21, 94, 239, 0.12), transparent 30%),
        radial-gradient(circle at right center, rgba(18, 183, 106, 0.07), transparent 22%),
        linear-gradient(180deg, #f7f9fc 0%, #eef3f9 100%);
    color: var(--text);
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 2rem;
}

.hero {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 1rem;
    padding: 1.15rem 1.25rem;
    border: 1px solid var(--border);
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(255,255,255,0.78));
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0.1rem 0 0.35rem 0;
    font-size: 2rem;
    letter-spacing: -0.03em;
}

.hero p {
    margin: 0;
    color: var(--muted);
    max-width: 70ch;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.32rem 0.7rem;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.workflow-pill {
    align-self: center;
    padding: 0.9rem 1rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #101828, #344054);
    color: white;
    min-width: 220px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(16, 24, 40, 0.18);
}

.workflow-pill small {
    display: block;
    color: rgba(255,255,255,0.72);
    margin-top: 0.2rem;
}

.status-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.8rem;
    margin-bottom: 1rem;
}

.status-card {
    padding: 0.95rem 1rem;
    border-radius: 16px;
    background: var(--panel);
    border: 1px solid var(--border);
    box-shadow: 0 10px 25px rgba(16, 24, 40, 0.05);
}

.status-card .label {
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
}

.status-card .value {
    font-size: 1.3rem;
    font-weight: 800;
    margin-top: 0.35rem;
}

.status-card .hint {
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 0.15rem;
}

.panel {
    background: var(--panel-strong);
    border: 1px solid var(--border);
    border-radius: 20px;
    box-shadow: var(--shadow);
    padding: 1rem;
}

.panel-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.6rem;
    margin-bottom: 0.75rem;
}

.panel-title h3 {
    margin: 0;
    font-size: 1.05rem;
}

.muted {
    color: var(--muted);
}

.stage-tracker {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.65rem;
    margin: 0.8rem 0 0.2rem;
}

.stage {
    padding: 0.8rem 0.9rem;
    border-radius: 14px;
    border: 1px solid var(--border);
    background: #fff;
}

.stage.active {
    border-color: rgba(21, 94, 239, 0.32);
    background: linear-gradient(180deg, rgba(21, 94, 239, 0.11), rgba(255,255,255,1));
}

.stage strong {
    display: block;
    margin-bottom: 0.25rem;
}

.document-preview {
    max-height: 510px;
    overflow: auto;
    padding: 1rem 1rem;
    border-radius: 16px;
    background: linear-gradient(180deg, #fefefe, #f7f9fc);
    border: 1px solid rgba(16,24,40,0.08);
    line-height: 1.75;
    white-space: pre-wrap;
    font-size: 0.95rem;
}

.preview-chip {
    display: inline-block;
    margin: 0 0.2rem;
    padding: 0.1rem 0.45rem;
    border-radius: 999px;
    background: rgba(240, 68, 56, 0.12);
    color: var(--danger);
    font-weight: 700;
    font-size: 0.78rem;
}

.callout {
    padding: 0.9rem 1rem;
    border-radius: 16px;
    background: rgba(21, 94, 239, 0.08);
    border: 1px solid rgba(21, 94, 239, 0.16);
    color: #13338b;
}

.result-box {
    border-radius: 16px;
    border: 1px solid rgba(16,24,40,0.08);
    background: #0f172a;
    color: #e5eefb;
    padding: 1rem;
    white-space: pre-wrap;
    max-height: 420px;
    overflow: auto;
}

.soft-card {
    border: 1px solid var(--border);
    background: linear-gradient(180deg, #ffffff, #f7faff);
    border-radius: 18px;
    padding: 0.95rem 1rem;
}

.interactive-row {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
}

.tiny-label {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
}

.tiny-value {
    font-size: 1rem;
    font-weight: 750;
    margin-top: 0.2rem;
}

@media (max-width: 960px) {
    .hero, .status-grid, .interactive-row, .stage-tracker {
        grid-template-columns: 1fr;
        display: grid;
    }

    .hero {
        flex-direction: column;
    }

    .workflow-pill {
        width: 100%;
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_state() -> None:
        defaults = {
                "document_text": "",
                "document_name": "No document loaded",
                "page_count": 0,
                "redacted_text": "",
                "redaction_summary": "No PII patterns detected",
                "audit_result": "",
                "audit_state": "idle",
                "last_error": "",
                "preview_loaded": False,
                "last_mode": "",
        }
        for key, value in defaults.items():
                st.session_state.setdefault(key, value)


def load_pdf_text(file_bytes: bytes, file_label: str) -> tuple[str, int]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(file_bytes)
                temp_path = temp_file.name

        try:
                loader = PyPDFLoader(temp_path)
                pages = loader.load()
                text = "\n".join(page.page_content for page in pages).strip()
                return text, len(pages)
        finally:
                try:
                        os.remove(temp_path)
                except OSError:
                        pass


def normalize_document(file_name: str | None = None, file_bytes: bytes | None = None, source_label: str = "") -> None:
        if file_name is None or file_bytes is None:
                return

        text, page_count = load_pdf_text(file_bytes, file_name)
        st.session_state.document_text = text
        st.session_state.document_name = file_name
        st.session_state.page_count = page_count
        st.session_state.preview_loaded = True
        st.session_state.last_error = ""
        st.session_state.audit_result = ""
        st.session_state.audit_state = "ready"
        st.session_state.last_mode = source_label


def format_preview_text(text: str) -> str:
        sanitized = re.sub(r"(\[REDACTED_[A-Z_]+\])", r"<span class='preview-chip'>\1</span>", text)
        return sanitized.replace("\n", "<br>")


def fast_mode_summary(text: str, redaction_summary: str, page_count: int) -> str:
        word_count = len(text.split()) if text else 0
        return (
                "FAST PREVIEW MODE\n"
                f"Document pages: {page_count}\n"
                f"Approx. words: {word_count}\n"
                f"PII status: {redaction_summary}\n"
                "\n"
                "This preview mode skips LLM analysis to keep the workflow instant.\n"
                "Use Full Audit when you want protocol-specific guidance and risk flags."
        )


init_state()

with st.sidebar:
        st.header("Workflow Controls")
        workflow_mode = st.selectbox(
                "Dashboard mode",
                ["Identify", "Review", "Resolve"],
                index=["Identify", "Review", "Resolve"].index(st.session_state.last_mode) if st.session_state.last_mode in ["Identify", "Review", "Resolve"] else 0,
                help="Moves the interface toward the part of the workflow you want to complete next.",
        )
        enable_scrub = st.checkbox("Enable PII scrub", value=True)
        fast_mode = st.checkbox("Fast Preview mode", value=False)
        show_raw = st.checkbox("Show raw protocol text", value=False)
        confidence_floor = st.slider("Manual review threshold", 0, 100, 70, help="Lower values trust the AI more; higher values force more review.")
        retriever_k = st.number_input("Retriever k (top docs)", min_value=1, max_value=10, value=3)

        st.divider()
        st.caption("Clinical-grade tone, minimalist surfaces, and clear decision points reduce cognitive load during compliance review.")
        st.markdown("[Open NLP guidelines](NLP_GUIDELINES.md)")

        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key and not fast_mode:
                st.warning("Set `GEMINI_API_KEY` for full audit mode or enable Fast Preview.")


st.markdown(
        """
        <div class="hero">
            <div>
                <span class="eyebrow">Clinical compliance intelligence</span>
                <h1>The Auditor</h1>
                <p>
                    A focused clinical protocol review workspace built for Identify → Review → Resolve.
                    Split the document, the risks, and the next action so the user never has to hunt for context.
                </p>
            </div>
            <div class="workflow-pill">
                Medical-grade interface
                <small>PII-safe, decision-centered, and audit-friendly</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

st.markdown(
        """
        <div class="status-grid">
            <div class="status-card"><div class="label">Workflow</div><div class="value">Identify → Review → Resolve</div><div class="hint">One path, one decision at a time.</div></div>
            <div class="status-card"><div class="label">Protection</div><div class="value">PII Scrub</div><div class="hint">Redacts sensitive phrases before audit.</div></div>
            <div class="status-card"><div class="label">Mode</div><div class="value">Interactive</div><div class="hint">Progressive disclosure keeps the screen calm.</div></div>
            <div class="status-card"><div class="label">Confidence Gate</div><div class="value">{}%</div><div class="hint">Manual review above this threshold.</div></div>
        </div>
        """.format(confidence_floor),
        unsafe_allow_html=True,
)

upload_col, sample_col, reset_col = st.columns([2.1, 1, 1])

with upload_col:
        uploaded_file = st.file_uploader("Upload a clinical protocol PDF", type=["pdf"], label_visibility="visible")
with sample_col:
        load_sample = st.button("Load sample", use_container_width=True)
with reset_col:
        clear_session = st.button("Reset", use_container_width=True)

if clear_session:
        for key in [
                "document_text",
                "document_name",
                "page_count",
                "redacted_text",
                "redaction_summary",
                "audit_result",
                "audit_state",
                "last_error",
                "preview_loaded",
                "last_mode",
        ]:
                st.session_state.pop(key, None)
        st.rerun()

if uploaded_file is not None:
        normalize_document(uploaded_file.name, uploaded_file.getvalue(), source_label="Identify")

if load_sample:
        sample_path = Path("data") / "guideline.pdf"
        if sample_path.exists():
                normalize_document(sample_path.name, sample_path.read_bytes(), source_label="Identify")
                st.success("Sample protocol loaded.")
        else:
                st.error("Sample guideline PDF was not found.")

document_loaded = bool(st.session_state.document_text)
protocol_text = st.session_state.document_text

if document_loaded and enable_scrub:
        redacted_text, counts = scrub_pii(protocol_text)
        st.session_state.redacted_text = redacted_text
        st.session_state.redaction_summary = summarize_redaction(counts)
        preview_text = redacted_text
else:
        st.session_state.redacted_text = protocol_text
        preview_text = protocol_text

page_count = st.session_state.page_count or 0
word_count = len(protocol_text.split()) if protocol_text else 0
trust_label = "Ready" if document_loaded else "Waiting for upload"
trust_hint = st.session_state.redaction_summary if enable_scrub else "Raw content preview enabled"

st.markdown(
        """
        <div class="interactive-row">
            <div class="soft-card"><div class="tiny-label">Document state</div><div class="tiny-value">{}</div></div>
            <div class="soft-card"><div class="tiny-label">Pages / Words</div><div class="tiny-value">{} / {}</div></div>
            <div class="soft-card"><div class="tiny-label">PII posture</div><div class="tiny-value">{}</div></div>
        </div>
        """.format(trust_label, page_count, word_count, trust_hint),
        unsafe_allow_html=True,
)

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

tab_identify, tab_review, tab_resolve = st.tabs(["Identify", "Review", "Resolve"])

with tab_identify:
        left, right = st.columns([1.15, 0.85], gap="large")

        with left:
                st.markdown(
                        """
                        <div class="panel">
                            <div class="panel-title">
                                <h3>Document intake</h3>
                                <span class="muted">Clear entry point for new protocols</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                )
                if document_loaded:
                        st.success(f"Loaded: {st.session_state.document_name}")
                        st.caption(f"{page_count} pages • {word_count} words")
                else:
                        st.info("Upload a PDF to begin. The document preview, audit console, and fix workflow will activate automatically.")

                st.markdown(
                        f"""
                        <div class="stage-tracker">
                            <div class="stage {'active' if workflow_mode == 'Identify' else ''}"><strong>1. Identify</strong>Load and redact the protocol.</div>
                            <div class="stage {'active' if workflow_mode == 'Review' else ''}"><strong>2. Review</strong>Read the highlighted text and inspect risks.</div>
                            <div class="stage {'active' if workflow_mode == 'Resolve' else ''}"><strong>3. Resolve</strong>Apply fixes, export, or mark for human review.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                )

                st.markdown(
                        """
                        <div class="callout">
                            The interface is intentionally calm: status colors are reserved for decision points,
                            and all secondary details are tucked behind progressive disclosure.
                        </div>
                        """,
                        unsafe_allow_html=True,
                )

                st.markdown("</div>", unsafe_allow_html=True)

        with right:
                st.markdown(
                        """
                        <div class="panel">
                            <div class="panel-title">
                                <h3>Interaction controls</h3>
                                <span class="muted">Fast, visible decisions</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                )
                st.markdown("- `Fast Preview` skips AI latency for instant document inspection.")
                st.markdown("- `PII scrub` protects sensitive content before any audit run.")
                st.markdown("- `Manual review threshold` raises the confidence bar for approvals.")
                if fast_mode:
                        st.info("Fast Preview is active. Run a full audit whenever you want protocol-specific feedback.")
                st.markdown("</div>", unsafe_allow_html=True)

with tab_review:
        pdf_col, audit_col = st.columns([1.15, 0.95], gap="large")

        with pdf_col:
                st.markdown(
                        """
                        <div class="panel">
                            <div class="panel-title">
                                <h3>Left panel: protocol surface</h3>
                                <span class="muted">Sensitive text is highlighted before review</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                )

                if document_loaded:
                        preview_source = preview_text if enable_scrub else protocol_text
                        preview_html = format_preview_text((preview_source or "")[:15000])
                        st.markdown(f"<div class='document-preview'>{preview_html}</div>", unsafe_allow_html=True)
                        if show_raw:
                                st.expander("Raw text preview").write((protocol_text or "")[:12000])
                else:
                        st.info("The protocol preview appears here after upload. Sample documents work too.")

                st.markdown("</div>", unsafe_allow_html=True)

        with audit_col:
                st.markdown(
                        """
                        <div class="panel">
                            <div class="panel-title">
                                <h3>Right panel: audit console</h3>
                                <span class="muted">Interactive audit log and next action</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                )

                if document_loaded:
                        audit_mode_label = "Preview audit" if fast_mode else "Run full audit"
                        if st.button(audit_mode_label, use_container_width=True, type="primary"):
                                st.session_state.audit_state = "running"
                                if fast_mode:
                                        st.session_state.audit_result = fast_mode_summary(protocol_text, st.session_state.redaction_summary, page_count)
                                        st.session_state.audit_state = "complete"
                                        st.success("Fast Preview generated instantly.")
                                else:
                                        if not os.getenv("GEMINI_API_KEY"):
                                                st.session_state.last_error = "GEMINI_API_KEY is not configured."
                                                st.session_state.audit_state = "error"
                                                st.error("Set GEMINI_API_KEY to run the full audit, or switch on Fast Preview.")
                                        else:
                                                audit_input = st.session_state.redacted_text if enable_scrub else protocol_text
                                                with st.spinner("Analyzing the protocol against the guideline database..."):
                                                        try:
                                                                st.session_state.audit_result = audit_protocol(audit_input)
                                                                st.session_state.audit_state = "complete"
                                                                st.success("Audit complete.")
                                                        except Exception as exc:
                                                                st.session_state.last_error = str(exc)
                                                                st.session_state.audit_state = "error"
                                                                st.error(f"Audit failed: {exc}")

                        if st.session_state.audit_state == "running":
                                st.progress(70)

                        if st.session_state.audit_result:
                                st.markdown("#### Audit log")
                                st.markdown(
                                        f"""
                                        <div class="result-box">{st.session_state.audit_result}</div>
                                        """,
                                        unsafe_allow_html=True,
                                )
                                st.download_button(
                                        "Download audit output",
                                        data=st.session_state.audit_result,
                                        file_name=f"audit_{st.session_state.document_name.replace(' ', '_')}.txt",
                                        use_container_width=True,
                                )
                        else:
                                st.markdown(
                                        """
                                        <div class="callout">
                                            When you run the audit, this panel becomes the live decision surface: confidence, explanation,
                                            and the exact next action appear together so the user can trust the flow.
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                )
                else:
                        st.info("Upload a file first to unlock the audit console.")

                st.markdown("</div>", unsafe_allow_html=True)

with tab_resolve:
        action_col, trend_col = st.columns([1.05, 0.95], gap="large")

        with action_col:
                st.markdown(
                        """
                        <div class="panel">
                            <div class="panel-title">
                                <h3>Resolve actions</h3>
                                <span class="muted">Proactive compliance tools</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                )

                a1, a2, a3 = st.columns(3)
                with a1:
                        if st.button("Suggest fix", use_container_width=True):
                                st.info("The next version can surface a suggested clause rewrite for the highest-risk finding.")
                with a2:
                        if st.button("Mark for review", use_container_width=True):
                                st.info("The issue is routed to a human reviewer and stays visible in the audit trail.")
                with a3:
                        if st.button("Export summary", use_container_width=True):
                                if st.session_state.audit_result:
                                        st.download_button(
                                                "Download summary",
                                                data=st.session_state.audit_result,
                                                file_name="audit_summary.txt",
                                                use_container_width=True,
                                        )
                                else:
                                        st.warning("Run an audit first to create a summary.")

                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <div class="soft-card">
                            <div class="tiny-label">Audit confidence guidance</div>
                            <div class="tiny-value">{confidence_floor}% manual review threshold</div>
                            <div class="muted" style="margin-top:0.35rem;">
                                Green means low friction, yellow means inspect carefully, and red means stop and resolve before approval.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        with trend_col:
                st.markdown(
                        """
                        <div class="panel">
                            <div class="panel-title">
                                <h3>Proactive compliance</h3>
                                <span class="muted">Polished, hackathon-ready cues</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                )
                st.markdown("**1. Suggested fix cards** – surface a one-click or copy-ready resolution for the highest-risk item.")
                st.markdown("**2. Risk trend line** – show whether the protocol is improving across review cycles.")
                st.markdown("**3. Confidence pulse** – gently animate AI confidence so reviewers know when to trust or inspect.")

                if st.session_state.audit_state == "complete" and st.session_state.audit_result:
                        risk_hint = "Improving"
                elif st.session_state.audit_state == "error":
                        risk_hint = "Needs attention"
                else:
                        risk_hint = "Awaiting audit"

                st.markdown(
                        f"""
                        <div class="soft-card">
                            <div class="tiny-label">Current trend</div>
                            <div class="tiny-value">{risk_hint}</div>
                            <div class="muted" style="margin-top:0.35rem;">Use the next release to chart risk deltas after every resolve action.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.last_error:
        st.error(st.session_state.last_error)