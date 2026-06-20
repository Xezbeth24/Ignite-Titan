# NLP Project Guidelines Checklist

This checklist documents best-practices and required items for NLP projects. Use it to verify the project meets standards and to track remediation.

- **Data & Privacy:**
  - [ ] Only store minimal personal data; remove PHI/PII.
  - [ ] Have explicit dataset provenance and licenses for all data.
  - [ ] Apply access controls for `chroma_db` and any stored documents.

- **Reproducibility:**
  - [ ] Pin package versions in `requirements.txt`.
  - [ ] Provide a `README.md` with setup and usage steps.
  - [ ] Record random seeds and model/config versions.

- **Evaluation & Metrics:**
  - [ ] Define metrics for model behavior (accuracy, F1, safety checks).
  - [ ] Include test protocols and sample inputs/expected outputs.

- **Model Card & Documentation:**
  - [ ] Publish a model card describing intended use, limitations, and risks.
  - [ ] Document prompts, prompt-engineering decisions, and chain behavior.

- **Bias, Fairness & Safety:**
  - [ ] Run bias checks on representative datasets.
  - [ ] Document mitigations and failure modes.

- **Security & Secrets:**
  - [ ] Do not commit API keys; use environment variables (`.env`).
  - [ ] Validate and sanitize user uploads.

- **Licensing & Legal:**
  - [ ] Verify licenses for third-party models and datasets.

- **Monitoring & Ops:**
  - [ ] Add logging and error reporting for audits.
  - [ ] Plan for model updates and dataset drift monitoring.

- **UX & Accessibility:**
  - [ ] Provide clear error states and guidance in the UI.
  - [ ] Ensure UI is keyboard accessible and mobile-friendly.

Use this file as the canonical checklist; update it when you make changes. Link to it from the app sidebar for quick access.
