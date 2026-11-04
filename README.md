# Groww · Mutual Fund FAQ Assistant (facts-only RAG)

A small chat app that answers *factual* questions about four HDFC Mutual Fund schemes using only official public pages (HDFC Mutual Fund, SEBI, AMFI). Every answer is ≤3 sentences, carries exactly one source link and a "Last updated from sources" date. It refuses advice, does not quote returns/NAV, and rejects messages containing personal details.

- **Product context:** Groww (the assistant is the kind of FAQ widget a Groww-style app would embed).
- **AMC:** HDFC Mutual Fund. **Schemes:** HDFC Large Cap, Flexi Cap, ELSS Tax Saver, Mid Cap.
- **Corpus:** 25 public pages, see `sources.csv` / `sources.md`.

## Setup
```bash
pip install -r requirements.txt
python -m unittest test_engine      # 20 tests
streamlit run app.py
```
Optional wording layer: set `ANTHROPIC_API_KEY` (model via `MF_FAQ_MODEL`). Output is validated (≤3 sentences, no links, no new numbers) and falls back to the retrieved text. Without a key the app is fully deterministic.

## Host it
Push this folder to a GitHub repo, then deploy on Streamlit Community Cloud (main file `app.py`). Or record a ≤3-minute demo of the example questions.

## How it works
`engine.answer()` decides in this order: PII → advice refusal → performance/returns/NAV redirect → out-of-scope scheme → clarifying question → BM25 retrieval over curated chunks (scheme-isolated, topic-boosted) → answer with the chunk's single source URL.

## Files
`app.py` UI · `engine.py` guardrails + retrieval · `corpus_data.py` sources + facts · `llm.py` optional wording · `test_engine.py` · `sources.csv/.md` · `sample_qa.md` · `DISCLAIMER.md` · `scripts/make_outputs.py`

## Known limits
- The corpus is a **hand-curated snapshot dated 2026-11-04**; fees (TER, exit load) change, so re-check before relying on it. Nothing is scraped at runtime.
- TER shown is from the Direct Plan page; the Regular Plan differs.
- 16 of 25 sources were opened and checked on 2026-11-04. S13–S19 (other KIM/SID PDFs), S22 (SEBI investor page) and S25 (AMFI intro) are only linked from official pages; SEBI and AMFI investor pages could not be opened from the build sandbox, so please click them.
- KIM/SID PDFs are cited for "where is the document" questions but their text is not ingested.
- The benchmark riskometer level is not captured (image only).
- The optional LLM layer is untested. `app.py` was logic-checked with a stub, not run under real Streamlit (it could not be installed in the build sandbox).
- Not covered: other AMCs/schemes, performance, tax advice, account-specific queries.
