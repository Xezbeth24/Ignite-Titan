import re
from typing import Tuple, Dict


def scrub_pii(text: str) -> Tuple[str, Dict[str,int]]:
    """Redact common PII from a text blob and return (redacted_text, counts).

    Patterns redacted:
    - Emails
    - Phone numbers (various formats)
    - US SSN-like patterns (XXX-XX-XXXX)
    - Long digit sequences that may be IDs (6+ digits)
    - Simple DOB patterns (MM/DD/YYYY, YYYY-MM-DD)
    """
    counts = {"emails": 0, "phones": 0, "ssn": 0, "ids": 0, "dates": 0}

    # Emails
    email_re = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    text, n = email_re.subn("[REDACTED_EMAIL]", text)
    counts["emails"] = n

    # Phone numbers (simple)
    phone_re = re.compile(r"(\+?\d{1,3}[\s-])?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}")
    text, n = phone_re.subn("[REDACTED_PHONE]", text)
    counts["phones"] = n

    # SSN-like
    ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    text, n = ssn_re.subn("[REDACTED_SSN]", text)
    counts["ssn"] = n

    # Dates (MM/DD/YYYY or YYYY-MM-DD)
    date_re = re.compile(r"\b(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{1,2}-\d{1,2})\b")
    text, n = date_re.subn("[REDACTED_DATE]", text)
    counts["dates"] = n

    # Long digit sequences (IDs) - avoid redacting short numbers
    id_re = re.compile(r"\b\d{6,}\b")
    text, n = id_re.subn("[REDACTED_ID]", text)
    counts["ids"] = n

    return text, counts


def summarize_redaction(counts: Dict[str,int]) -> str:
    parts = []
    for k,v in counts.items():
        if v:
            parts.append(f"{v} {k}")
    if parts:
        return ", ".join(parts) + " redacted"
    return "No PII patterns detected"
