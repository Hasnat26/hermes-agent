# Procurement Auditor (Local / Zero-API-Cost MVP)

A self-contained technical-commercial quotation auditor designed to run with local models such as Ollama/Qwen3-8B. It is intentionally independent of Hermes internals so the business logic can later be exposed through Hermes, Open WebUI, n8n, or a dedicated UI.

## MVP

Input:
- one requirement/specification document (optional)
- 2–5 vendor quotation documents in PDF/DOCX/XLSX/Markdown/text after conversion

Output:
- normalized quotation data
- deterministic technical/commercial comparison
- PASS / WARNING / CRITICAL findings
- evidence references to source documents/pages where supplied
- JSON and Markdown audit report

## Design rule

The local LLM is used for extraction, normalization and semantic interpretation. Deterministic Python rules make numerical/control decisions. Never ask the LLM to decide a price/quantity variance when the values can be calculated exactly.

## First implementation

The package currently accepts already-extracted Markdown/text so the rule engine can be tested without any paid OCR/API. MarkItDown is the planned ingestion adapter.

```bash
python -m procurement_auditor.cli demo
python -m procurement_auditor.cli audit sample_data/requirements.json sample_data/quotations.json --out report.md
```

Ollama integration is optional and isolated in `llm.py`; the deterministic engine works without an LLM.
