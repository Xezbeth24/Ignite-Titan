#!/usr/bin/env python3
import os
from datetime import date

TEMPLATE = """# Model Card

Model: {model}

Date: {date}

Source: {source}

Intended Use
------------
Primary intended use: auditing clinical protocols for compliance and safety.

Model Details
-------------
- LLM: {model}
- Embeddings: {embeddings}

Notes
-----
This file was generated automatically. Edit to add evaluation metrics, data provenance, and limitations.
"""


def main():
    model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
    embeddings = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    source = os.getenv("MODEL_SOURCE", "Google Gemini / local embeddings")

    out = TEMPLATE.format(model=model, date=date.today().isoformat(), source=source, embeddings=embeddings)

    with open("MODEL_CARD.md", "w") as f:
        f.write(out)

    print("MODEL_CARD.md generated")


if __name__ == "__main__":
    main()
